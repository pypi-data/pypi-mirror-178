from typing import Tuple
from tqdm.auto import tqdm
import numpy as np
import pyrost as rst

EPSILON = 1.4901161193847656e-08

def main(scan_num: int=35, ds_y: float=10.0, ds_x: float=10.0, h_min: float=0.3,
         h_max: float=3.0, n_h: int=25, search_window: Tuple[float, float, float]=(5.0, 5.0, 0.1),
         h0: float=1.99, n_iter: int=20, f_tol: float=1e-6, blur: float=8.0):

    fname = f'/asap3/petra3/gpfs/p11/2021/data/11010570/shared/Scan_{scan_num:d}.cxi'
    files = rst.CXIStore(fname, fname)
    data = rst.STData(files, transform=rst.Crop(roi=np.array([[1180, 1120], [2130, 2020]])))
    data = data.load(processes=4)
    st_obj = data.get_st(ds_y=ds_y, ds_x=ds_x, aberrations=False, ff_correction=False)

    cv_hvals = np.geomspace(h_min, h_max, n_h)
    obj = st_obj.update_reference(h0)

    optimizer = rst.BFGS(obj.CV, h0, epsilon=1e-4)

    obj.update_errors.inplace_update()
    cv_curve = obj.CV_curve(cv_hvals)

    errors = [obj.error,]
    hvals = [h0,]
    cv_curves = [cv_curve,]

    itor = tqdm(range(1, n_iter + 1),
                bar_format='{desc} {percentage:3.0f}% {bar} ' \
                'Iteration {n_fmt} / {total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]')

    print(f"Initial error = {errors[-1]:.6f}, Initial h0 = {hvals[-1]:.2f}")

    for _ in itor:
        new_obj = obj.update_pixel_map(search_window=search_window, blur=blur, method='rsearch')

        # Update hval and step
        optimizer.update_loss(new_obj.CV)
        optimizer.step()
        h0 = optimizer.state_dict()['xk'].item()
        hvals.append(h0)

        # Update reference_image
        new_obj.update_reference.inplace_update(hval=h0)

        new_obj.update_errors.inplace_update()
        errors.append(new_obj.error)

        cv_curve = new_obj.CV_curve(cv_hvals)
        cv_curves.append(cv_curve)

        itor.set_description(f"Error = {errors[-1]:.6f}, hval = {hvals[-1]:.2f}")

        # Break if function tolerance is satisfied
        if (errors[-2] - errors[-1]) / max(errors[-2], errors[-1]) > f_tol:
            obj = new_obj

        else:
            break

    np.savez(f'Scan_{scan_num:d}_errors.npz', cv_curves=cv_curves, errors=errors, cv_hvals=cv_hvals,
             hvals=hvals)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Calculate error curves for the R-PXST iterative update')
    parser.add_argument('scan_num', type=int, help="Scan number.")
    parser.add_argument('--ds_y', default=10.0, type=float,
                        help="Reference image sampling interval along the vertical axis.")
    parser.add_argument('--ds_x', default=10.0, type=float,
                        help="Reference image sampling interval along the horizontal axis.")
    parser.add_argument('--h_min', default=0.3, type=float,
                        help="Lower bound of the error profiles.")
    parser.add_argument('--h_max', default=3.0, type=float,
                        help="Upper bound of the error profiles.")
    parser.add_argument('--n_h', default=25, type=int,
                        help="Number of point in the error profiles.")
    parser.add_argument('--search_window', default=(5.0, 5.0, 0.1), type=float, nargs=3,
                        help="Search window size in the vertical axis.")
    parser.add_argument('--h0', default=1.99, type=float, help="Initial kernel bandwidth.")
    parser.add_argument('--n_iter', default=20, type=int, help="Maximum number of iterations.")
    parser.add_argument('--f_tol', default=1e-6, type=float,
                        help="Tolerance of termination by the change of the error.")
    parser.add_argument('--blur', default=8.0, type=float,
                        help="Post-update gaussian smoothing bandwidth.")

    args = vars(parser.parse_args())

    main(**args)
