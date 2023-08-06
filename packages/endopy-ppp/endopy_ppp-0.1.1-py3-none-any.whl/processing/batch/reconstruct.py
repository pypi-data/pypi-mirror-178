import os
import time

import numpy as np
from tifffile import imwrite

from processing.core.recon import EndoImages
from processing.files.files import EndoFiles


class EndoStack:
    _authorized_channels = ['PSD', 'PMT1', 'PMT2']
    _default_stack_name = 'stacked_recon'
    _default_stack_ext = '.tiff'
    _defaut_stack_path = 'C:\\Temp'
    _imagej_axes = 'TCYX'

    def __init__(self, files: EndoFiles, channels: list[str] = ['PMT1'], fill_unsampled: bool = False,
                 image_size: int = 0):
        self.filelist = files
        self.image_size = image_size if image_size else EndoImages.default_image_size
        self.timestamps = []
        self.channels = channels
        self.fill_unsampled = fill_unsampled
        self.stack = None
        self.stack_shape = None
        self._current = None

    def build(self, display_progress: bool = True):
        self.__set_stack_shape()
        self.stack = np.zeros(shape=self.stack_shape).astype('float32')
        n_files = len(self.filelist.selected_files)

        for idx_file, filepath in enumerate(self.filelist.selected_files):
            if display_progress:
                start = time.time()
                self.__build_task(idx_file, filepath)
                stop = time.time()
                print(f"Reconstructed image {idx_file+1}/{n_files} ({(stop-start)*1e3:.2f} ms)")
            else:
                self.__build_task(idx_file, filepath)

    def __build_task(self, idx_file, filepath):
        self._current = EndoImages(filepath, image_size=self.image_size)
        self._current.read()

        if self._current:
            self.timestamps.append(self._current.timestamp)
            self._current.reconstruct(channels=self.channels)

        for idx_chan, channel in enumerate(self.channels):
            self.stack[idx_file, idx_chan, :, :] = self._current.reconstructed[channel]

    def __set_stack_shape(self):
        # Dimensions are 'TCYX' to comply with ImageJ
        dimX = self.image_size
        dimY = self.image_size
        dimC = len(self.channels)
        dimT = len(self.filelist.selected_files)
        self.stack_shape = (dimT, dimC, dimY, dimX)

    def save(self, savedir: str = '', savename: str = ''):
        savedir = EndoStack._defaut_stack_path if not savedir else savedir
        savename = self._construct_savename(savename=savename)
        imwrite(
            os.path.join(savedir, savename),
            self.stack,
            imagej=True,
            metadata={'axes': EndoStack._imagej_axes},
        )

    def _construct_savename(self, savename: str = '') -> str:
        if savename:
            return savename + EndoStack._default_stack_ext
        else:
            start_str = str(self.timestamps[0])
            stop_str = str(self.timestamps[-1])
            imsize = f"_imgsize={self.image_size}"
            tstamps = f"_start={start_str[0:5]}_stop={stop_str[0:5]}"
            filled = f"_filled={self.fill_unsampled}"
            suffix = imsize + tstamps + filled
            return EndoStack._default_stack_name + suffix + EndoStack._default_stack_ext


if __name__ == "__main__":
    fs = EndoFiles(
        path='C:/Users/jerem/Downloads/tufts_20221114/raw_G202207-06_obj=2100um4fps/'
    )
    fs.filter_days(days=['20221114'])
    fs.filter_times(between=['231300', '231359'])
    print(fs)

    stack = EndoStack(files=fs, channels=['PMT1', 'PMT2'], image_size=250, fill_unsampled=False)
    start = time.time()
    stack.build(display_progress=True)
    stop = time.time()
    print(stop-start)
    stack.save()
