from typing import Any, Iterable, Optional
import pyrost as rst
import numpy as np
import os
import h5py
import hdf5plugin
import argparse

def cxi_converter_petra(scan_num: int, wavelength: float, distance: float,
                        dir_path: str='/asap3/petra3/gpfs/p11/2021/data/11010570/raw/',
                        idxs: Optional[Iterable[int]]=None, transform: Optional[rst.Transform]=None,
                        **attributes: Any) -> rst.STData:
    """Convert measured frames and log files from the
    Sigray laboratory to a :class:`pyrost.STData` data
    container.

    Parameters
    ----------
    scan_num : int
        Scan number.
    roi : iterable of ints
        Region of interest.
    wavelength : float
        X-ray beam wavelength [m].
    distance : float, optional
        Detector distance [m].

    Returns
    -------
    STData
        Data container with the extracted data.
    """


    fs_vec = np.array([-1., 0., 0.])
    ss_vec = np.array([0., -1., 0.])

    frames_dir = [folder for folder in os.listdir(dir_path)
                  if folder.endswith('frames') and folder.startswith('scan')][0]
    h5_dir = os.path.join(dir_path, frames_dir, f'Scan_{scan_num:d}')
    log_path = os.path.join(dir_path, f'server_log/Scan_logs/Scan_{scan_num:d}.log')
    h5_files = sorted([os.path.join(h5_dir, path) for path in os.listdir(h5_dir)
                       if path.endswith(('LambdaFar.nxs', '.h5')) and not path.endswith('master.h5')])

    files = rst.CXIStore(h5_files, mode='r')

    log_prt = rst.LogProtocol.import_default()
    log_attrs = log_prt.load_attributes(log_path)
    log_data, idxs = log_prt.load_data(log_path, idxs=idxs, return_idxs=True)

    x_pixel_size = 75e-6
    y_pixel_size = 75e-6

    n_frames = idxs.size
    pix_vec = np.tile(np.array([[x_pixel_size, y_pixel_size, 0]]), (n_frames, 1))
    basis_vectors = np.stack([pix_vec * ss_vec, pix_vec * fs_vec], axis=1)

    x_sample = log_attrs['Session logged attributes'].get('x_sample', 0.0)
    y_sample = log_attrs['Session logged attributes'].get('y_sample', 0.0)
    z_sample = log_attrs['Session logged attributes'].get('z_sample', 0.0)
    translations = np.nan_to_num(np.tile([[x_sample, y_sample, z_sample]], (n_frames, 1)))
    for data_key, log_dset in log_data.items():
        for log_key in log_prt.log_keys['x_sample']:
            if log_key in data_key:
                translations[:log_dset.size, 0] = log_dset
        for log_key in log_prt.log_keys['y_sample']:
            if log_key in data_key:
                translations[:log_dset.size, 1] = log_dset
        for log_key in log_prt.log_keys['z_sample']:
            if log_key in data_key:
                translations[:log_dset.size, 2] = log_dset

    data = rst.STData(files, basis_vectors=basis_vectors, translations=translations,
                      distance=distance, x_pixel_size=x_pixel_size, y_pixel_size=y_pixel_size,
                      wavelength=wavelength, **attributes)
    if transform:
        data = data.update_transform(transform)
    data = data.load('data', idxs=idxs)
    return data

def cxi_writer_petra(dir_path, scan_num, out_path, roi, wavelength, distance):
    """Extracts measured frames and log files from the
    Sigray laboratory and writes to a cxi file at the given path.

    Parameters
    ----------
    scan_num : int
        Scan number.
    wavelength : float
        X-ray beam wavelength [m].
    distance : float, optional
        Detector distance [m].
    """
    st_data = cxi_converter_petra(dir_path, scan_num, roi, wavelength, distance)
    with h5py.File(out_path, 'w') as cxi_file:
        st_data.write_cxi(cxi_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File converter for PETRA P11 PXST datasets.")
    parser.add_argument('dir_path', type=str, help="Path to the experiment's root folder") 
    parser.add_argument('scan_num', type=int, help="Scan number.")
    parser.add_argument('out_path', type=str, help="Output CXI file path.")
    parser.add_argument('--roi', type=int, nargs=4, help="Region of interest.")
    parser.add_argument('--wavelength', type=float, default=0.709291721831675e-10,
                        help="Wavelength of the X-ray beam [m].")
    parser.add_argument('--distance', type=float, default=2.37,
                        help="Sample-to-detector distance [m].")

    args = vars(parser.parse_args())
    cxi_writer_petra(**args)
