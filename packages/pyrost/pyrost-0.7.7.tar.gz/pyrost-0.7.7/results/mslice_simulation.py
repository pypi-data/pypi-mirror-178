import pyrost as rst
import pyrost.simulation as st_sim
import numpy as np
import h5py
from tqdm.auto import tqdm
import argparse

def main(out_path, en=60.0e3, mll_d=10e-3, mll_z=75.0, mll_ap=30.0, wedge=0.0, strain=0.0,
         th_max=1.5e-3, n_thetas=50, verbose=True):
    wl = st_sim.MLL.en_to_wl / en
    mll_mat1 = st_sim.Material(formula='SiC', density=2.67)
    mll_mat2 = st_sim.Material(formula='WC', density=13.87)
    bragg = np.arcsin(0.5 * wl / mll_d)
    x_mgn = 5.
    params = st_sim.MSParams.import_default(x_step=1e-4, z_step=2e-2, n_min=x_mgn / mll_d,
                                            n_max=(x_mgn + mll_ap) / mll_d, mll_sigma=1e-4, wl=wl,
                                            x_min=0., x_max=40., mll_depth=mll_z,
                                            mll_mat1=mll_mat1, mll_mat2=mll_mat2,
                                            focus=30 / np.tan(bragg))

    ml_ds = (x_mgn + np.cumsum(0.5 * mll_d * np.linspace(1.0 - strain, 1.0,
                                                         2 * (params.n_max - params.n_min))))
    ml_zs = params.z_step * np.arange(params.mll_depth // params.z_step)
    layers = ml_ds - ml_zs[:, None] * np.tan(np.linspace(0, wedge, ml_ds.size))
    mll = st_sim.MLL(mat1_r=params.get_mat1_r(en), mat2_r=params.get_mat2_r(en),
                    sigma=params.mll_sigma, layers=layers)

    ms_prgt = st_sim.MSPropagator(params, mll)

    ksize = 0.33 * (ms_prgt.x_arr[1] - ms_prgt.x_arr[0])**-1 # 3 sigma = 1 um
    x_lb, x_ub = x_mgn + 1., x_mgn + mll_ap - 1.
    wf_inc = np.ones(ms_prgt.x_arr.shape, dtype=np.complex128)
    wf_inc[(ms_prgt.x_arr < x_lb) | (ms_prgt.x_arr > x_ub)] = 0.
    wf_inc = rst.bin.gaussian_filter(wf_inc.real, ksize) + \
            1j * rst.bin.gaussian_filter(wf_inc.imag, ksize)

    bin_ratio = ms_prgt.size // 1000
    z_arr = ms_prgt.z_arr[::int((ms_prgt.z_arr[1] - ms_prgt.z_arr[0])**-1)] # every 1 um
    thetas = bragg + np.linspace(-th_max, th_max, n_thetas)
    mll_beam = np.array([params.x_min, params.x_max])
    diff_beam = mll_beam + np.tan(thetas - 2 * bragg)[:, None] * params.focus
    drct_beam = mll_beam + np.tan(thetas)[:, None] * params.focus
    ratio = np.ceil(2 * (np.tan(2 * bragg) + th_max) * params.focus / (params.x_max - params.x_min) + 1)
    xs_foc = ratio * params.x_step * (np.arange(ms_prgt.size) - ms_prgt.size // 2) + np.mean(ms_prgt.x_arr)
    xs_foc = xs_foc.reshape((bin_ratio, -1)).mean(axis=1)

    wfts = []
    size = int((ratio * (1 + ratio) * params.x_step**2 / params.wl / params.focus)**-1)
    for theta in tqdm(thetas, disable=not verbose,
                    bar_format='{desc} {percentage:3.0f}% {bar} Angle {n_fmt} / {total_fmt} '\
                                '[{elapsed}<{remaining}, {rate_fmt}{postfix}]'):
        ms_prgt.update_inc_wavefront.inplace_update(wf_inc * np.exp(2j * np.pi / params.wl * theta * ms_prgt.x_arr))
        ms_prgt.beam_propagate(verbose=False)
        wfts_theta = []
        for z, wft in zip(z_arr, ms_prgt.beam_profile[::int((ms_prgt.z_arr[1] - ms_prgt.z_arr[0])**-1)]):
            wft_foc = rst.bin.rsc_wp(wft, params.x_step, ratio * params.x_step,
                                    params.focus - z, params.wl)
            if size < wft.size:
                wft_foc[:(wft.size - size) // 2] = 0.0
                wft_foc[(size - wft.size) // 2:] = 0.0
            wfts_theta.append((np.abs(wft_foc)**2).reshape((bin_ratio, -1)).mean(axis=1))
        wfts.append(np.stack(wfts_theta, axis=0))
    wfts = np.stack(wfts, axis=1)

    diff_mask = np.tile((xs_foc > diff_beam[:, 0, None]) & (xs_foc < diff_beam[:, 1, None])[None, ...],
                        (z_arr.size, 1, 1))
    drct_mask = np.tile((xs_foc > drct_beam[:, 0, None]) & (xs_foc < drct_beam[:, 1, None])[None, ...],
                        (z_arr.size, 1, 1))
    diff_sum = np.sum(wfts * diff_mask, axis=-1)
    drct_sum = np.sum(wfts * drct_mask, axis=-1)
    effs = diff_sum / (diff_sum + drct_sum)

    with h5py.File(out_path, 'w') as h5_file:
        h5_file.create_dataset('entry/wavefronts', data=wfts)
        h5_file.create_dataset('entry/xcoordinates', data=xs_foc)
        h5_file.create_dataset('entry/efficiencies', data=effs)
        h5_file.create_dataset('entry/thicknesses', data=z_arr)
        h5_file.create_dataset('entry/thetas', data=thetas)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Multislice simulation.")
    parser.add_argument('out_path', type=str, help="Path to the output file.")
    parser.add_argument('--en', default=60.0e3, type=float, help="Photon energy in eV")
    parser.add_argument('--mll_d', default=10e-3, type=float, help="Grating's period in um")
    parser.add_argument('--mll_z', default=75., type=float, help="Grating's thickness in um")
    parser.add_argument('--mll_ap', default=30., type=float, help="Grating's aperture size in um")
    parser.add_argument('--wedge', default=0.0, type=float, help="Wedge of the grating's layers in radians")
    parser.add_argument('--strain', default=0.0, type=float, help="Strain of the grating's layers")
    parser.add_argument('--th_max', default=1.5e-3, type=float,
                        help="Span of the angles of incidence in radians")
    parser.add_argument('--n_thetas', default=50, type=int,
                        help="Number of the angles of incidence")
    parser.add_argument('-v', '--verbose', action='store_true', help="Set the verbosity")

    args = vars(parser.parse_args())
    main(**args)
