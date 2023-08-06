from typing import Optional
from cxi_converter import cxi_converter_petra
import pyrost as rst
import numpy as np
import os
import h5py
import argparse

def tilt_converter_petra(scan_num: int, energy: float, distance: float,
                         dir_path: str='/asap3/petra3/gpfs/p11/2021/data/11010570/raw/',
                         mask: Optional[np.ndarray]=None, flip: bool=False, axis: int=1):
    """Save measured frames and log files from a tilt
    scan to a h5 file.

    Parameters
    ----------
    scan_num : int
        Scan number.
    out_path : str
        Path of the output file
    target : {'Mo', 'Cu', 'Rh'}, optional
        Sigray X-ray source target used.
    distance : float, optional
        Detector distance in meters.
    """

    log_prt = rst.LogProtocol.import_default(log_keys={'start': ['Type: Scan', 'Start point'],
                                                       'end': ['Type: Scan', 'End point'],
                                                       'x_sample': ['Session logged attributes', 'SAM-X'],
                                                       'y_sample': ['Session logged attributes', 'SAM-Y'],
                                                       'z_sample': ['Session logged attributes', 'SAM-Z']},
                                             datatypes={'start': 'float', 'end': 'float'})

    frames_dir = [folder for folder in os.listdir(dir_path)
                  if folder.endswith('frames') and folder.startswith('scan')][0]
    h5_dir = os.path.join(dir_path, frames_dir, f'Scan_{scan_num:d}')
    log_path = os.path.join(dir_path, f'server_log/Scan_logs/Scan_{scan_num:d}.log')
    h5_files = sorted([os.path.join(h5_dir, path) for path in os.listdir(h5_dir)
                       if path.endswith(('LambdaFar.nxs', '.h5')) and not path.endswith('master.h5')])
    h5_master = sorted([os.path.join(h5_dir, path) for path in os.listdir(h5_dir)
                        if path.endswith('master.h5')])

    files = rst.CXIStore(h5_files, mode='r')
    fmaster = rst.CXIStore(h5_master, mode='r')

    with files:
        data = files.load_attribute('data')

    with fmaster:
        x_pixel_size = fmaster.load_attribute('x_pixel_size')
        y_pixel_size = fmaster.load_attribute('y_pixel_size')

    whitefield = rst.bin.make_whitefield(data, mask, axis=0)
    db_coord = np.unravel_index(np.argmax(whitefield), whitefield.shape)

    # translations = log_data[scan_type][:n_steps]
    if axis == 1:
        data = np.sum(data[:, :, db_coord[1] - 10:db_coord[1] + 10], axis=2)
        theta = np.linspace(0, data.shape[1], data.shape[1]) - db_coord[0]
        theta *= 36e-5 * attrs['x_pixel_size'] / (2 * np.pi * distance)
    elif axis == 0:
        data = np.sum(data[:, db_coord[0] - 10:db_coord[0] + 10], axis=1)
        theta = np.linspace(data.shape[1], 0, data.shape[1]) - db_coord[1]
        theta *= 36e-5 * attrs['y_pixel_size'] / (2 * np.pi * distance)
    else:
        raise ValueError('axis must be either 0 (vertical axis) or 1 (horizontal axis).')
    if flip:
        data = np.flip(data, axis=0)

    with h5py.File(out_path, 'w') as out_file:
        out_file.create_dataset("Data", data=data)
        # out_file.create_dataset("Omega", data=translations * 1e9) # must be in ndeg for some reason
        out_file.create_dataset("2Theta", data=theta)
        out_file.create_dataset("Energy", data=energy)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File converter for PETRA P11 tiltscan datasets.")
    # parser.add_argument('h5_dir', type=str, help="Path to the folder where the Eiger data files are located.")
    # parser.add_argument('log_path', type=str, help="Path to the log file")

    args = vars(parser.parse_args())
    tilt_converter_petra(**args)