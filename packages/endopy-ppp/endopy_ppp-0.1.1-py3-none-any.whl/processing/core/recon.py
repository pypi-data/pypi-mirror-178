import configparser
import os

import matplotlib.pyplot as plt
import numpy
import numpy as np
import scipy
from matplotlib.colors import LogNorm
from numpy import uint
from scipy import ndimage

import processing.libs.imagecalculator
from processing.files.files import EndoFiles, EndoRawData
from processing.libs.waveform import Waveform


class EndoParams:
    default_params_filename = 'state_parameters.ini'

    def __init__(self, path, file=''):
        self.path = path
        if file:
            self.file = file
        else:
            self.file = EndoParams.default_params_filename
        self._params_dict = None
        self.params = {}

        self._read_params_file()
        self._convert_params_dict()
        self._compute_global_params()

    def _read_params_file(self):
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(self.path, self.file), encoding='utf-8')

        self._params_dict = {s: dict(cfg.items(s)) for s in cfg.sections()}

    def _convert_params_dict(self):
        self.params['scan'] = self._params_dict['Scan Parameters']
        self.params['brake'] = self._params_dict['Brake Parameters']

        for key in list(self.params['scan'].keys()):
            self.params['scan'][key] = float(self.params['scan'][key])

        for key in list(self.params['brake'].keys()):
            self.params['brake'][key] = float(self.params['brake'][key])

    def _compute_global_params(self):
        self.params['globals'] = {}
        self.params['globals']['duration'] = self.params['scan']['time'] \
                                             + np.max(
            [self.params['brake']['timecos'], self.params['brake']['timesin']]) \
                                             + self.params['brake']['timerest']


class EndoCalib(EndoParams):

    def __init__(self, path):
        EndoParams.__init__(self, path)
        self.path = path
        self.files = EndoFiles(path)
        self.rawdata = None
        self.averaged_data = None

        self.read()
        self.average()

    def read(self):
        self._read_raw_data()
        self._read_params_file()

    def _read_raw_data(self):
        rawdata = []
        for file in self.files.all_files:
            tmp = EndoRawData(file)
            rawdata.append(tmp.read())
        self.rawdata = rawdata

    def average(self):
        tmp = self.rawdata[0]

        for i in range(1, len(self.rawdata) - 1):
            current_data = self.rawdata[i]

            for key in current_data:
                tmp[key] = tmp[key] + current_data[key]

        for key in tmp.keys():
            tmp[key] = tmp[key] / len(self.rawdata)

        self.averaged_data = tmp


class DwellTime:

    def __init__(self, fov: float = 0, psf: float = 2):
        self.fov = fov
        self.psf = psf
        self.t_tot = None
        self.t_vec = None
        self.td_vec = None
        self.dt = None
        self.x_vec = None
        self.y_vec = None
        self.vx_vec = None
        self.vy_vec = None
        self.scan_idx = None
        self.td0_idx = None
        self.dwell_time = None

    @property
    def r_vec(self):
        return np.sqrt(np.square(self.x_vec) + np.square(self.y_vec))

    @property
    def vt_vec(self):
        return np.sqrt(np.square(self.vx_vec) + np.square(self.vy_vec))

    def _compute_times(self):
        """Define in subclass"""
        pass

    def _compute_positions(self):
        self._convert_voltages_to_positions()
        self._normalize_and_center_fov()

    def _convert_voltages_to_positions(self):
        """Define in subclass"""
        pass

    def _normalize_and_center_fov(self):
        self.x_vec = self.x_vec - np.mean(self.x_vec)
        self.y_vec = self.y_vec - np.mean(self.y_vec)
        self.x_vec = self.x_vec[self.scan_idx] / np.max(self.x_vec[self.scan_idx]) * self.fov / 2
        self.y_vec = self.y_vec[self.scan_idx] / np.max(self.y_vec[self.scan_idx]) * self.fov / 2

    def _compute_speeds(self):
        dx_vec = np.diff(self.x_vec)
        dy_vec = np.diff(self.y_vec)
        self.vx_vec = dx_vec / self.dt
        self.vy_vec = dy_vec / self.dt

    def _compute_dwell_time(self):
        self.td0_idx = np.where(self.vt_vec != 0)
        self.dwell_time = self.psf / self.vt_vec[self.td0_idx]
        self.statistics(self.dwell_time, mult=1e6, unit='us', name='PSF dwell time')

    def _compute(self):
        self._compute_times()
        self._compute_positions()
        self._compute_speeds()
        self._compute_dwell_time()

    @staticmethod
    def statistics(arr: np.ndarray, mult: float = 1e6, unit: str = 'us', name: str = 'Array'):
        print(name + ' statistics')
        print("\t Average = %3.2f %s" % (np.mean(arr) * mult, unit))
        print("\t Standard deviation = %3.2f %s" % (np.std(arr) * mult, unit))
        print("\t Median = %3.2f %s" % (np.median(arr) * mult, unit))
        print("\t Maximum = %3.2f %s" % (np.max(arr) * mult, unit))
        print("\t Minimum = %3.2f %s" % (np.min(arr) * mult, unit))


class DwellTimeFromMeasurement(DwellTime):

    def __init__(self, calib: EndoCalib, fov: float = 0, psf: float = 2):
        super().__init__(fov=fov, psf=psf)
        self.calib = calib
        self._compute()

    def _convert_voltages_to_positions(self):
        self.x_vec = self.calib.averaged_data['xpos']
        self.y_vec = self.calib.averaged_data['ypos']

    def _compute_times(self):
        self.t_tot = self.calib.params['globals']['duration']
        self.dt = self.t_tot / len(self.calib.averaged_data['xpos'])
        self.t_vec = np.linspace(0, self.t_tot, len(self.calib.averaged_data['xpos']))
        self.scan_idx = np.where(self.t_vec <= self.calib.params['scan']['time'])
        self.t_vec = self.t_vec[self.scan_idx]
        self.td_vec = self.t_vec[1:] - self.dt  # For derivatives


class DwellTimeFromSimulation(DwellTime):

    def __init__(self, waveform, fov: float = 0, psf: float = 2, points: str = 'expansion'):
        super().__init__(fov=fov, psf=psf)
        self.points = points
        self.waveform = waveform
        self.waveform.compute_scan()
        self._compute()

    def _compute_times(self):
        self.dt = 1 / self.waveform.samplefreq
        self.t_tot = len(self.waveform.Time) * self.waveform.samplefreq
        self.t_vec = self.waveform.Time[self.scan_idx]
        self.td_vec = self.t_vec[1:] - self.dt  # For derivatives

    def _convert_voltages_to_positions(self):
        _start, _stop = self.waveform.GetStartStopPoints(points=self.points)
        self.x_vec = self.waveform.Vx_r[_start:_stop]
        self.y_vec = self.waveform.Vy_r[_start:_stop]
        self.scan_idx = np.arange(start=_start, stop=_stop)


class EndoImages(EndoRawData):
    default_image_size = 300
    mapped_keys = {'intensity': 'PSD', 'PMT1': 'PMT1', 'PMT2': 'PMT2'}

    def __init__(self, filepath, image_size: int = 0):
        super().__init__(filepath=filepath)
        self.image_size = image_size if image_size else EndoImages.default_image_size
        self.sampled_pixels_image = None
        self.sampled_pixels_idx = None
        self.unsampled_pixels_image = None
        self.unsampled_pixels_idx = None
        self.reconstructed = {'intensity': None, 'PMT1': None, 'PMT2': None}

    def plot_signal(self, channel: str = 'PMT1'):
        if self.check_signal(channel=channel):
            plt.figure()
            plt.plot(self.rawdata[channel])

    def get_sampled_pixels(self, channel: str = 'intensity'):
        calc = endoscope.hw.imagecalculator.ImageCalculator(
            imgsize=self.image_size,
            timeslice=slice(0, int(len(self.rawdata[channel]) / 2.1)),
            samples=len(self.rawdata[channel]),
            samples_auto=True,
            xvolts=self.rawdata['xpos'],
            yvolts=self.rawdata['ypos'],
        )

        self.sampled_pixels_image = calc.calc_image(intensities=np.ones(shape=self.rawdata[channel].shape))
        self.sampled_pixels_idx = np.where(self.sampled_pixels_image == 1)

    def get_unsampled_pixels(self, sigma: float = 2, trsh: float = 0.02):
        fov_image = ndimage.gaussian_filter(self.sampled_pixels_image, sigma=sigma)
        self.unsampled_pixels_idx = np.where((fov_image >= trsh) & (self.sampled_pixels_image == 0))
        self.unsampled_pixels_image = np.zeros(shape=self.sampled_pixels_image.shape)
        self.unsampled_pixels_image[self.unsampled_pixels_idx] = 1

    @property
    def fullsampled_image(self):
        return self.sampled_pixels_image + self.unsampled_pixels_image

    def fill_unsampled_pixels1(self, channel: str = 'PMT1', sigmas: list[float] = [3, 1], kern_size: int = 9):
        # Get the full gaussian filter and apply it only on the stripes mask
        im_gauss = ndimage.gaussian_filter(self.reconstructed[channel], sigma=sigmas[0])
        im_gauss_mask = self.reconstructed[channel].copy()
        im_gauss_mask[self.unsampled_pixels_idx] = im_gauss[self.unsampled_pixels_idx]

        # Create a "pinhole" kernel and convolve with the original image
        kern = self.hole_kernel(kern_size)
        im_conv = scipy.signal.convolve2d(self.reconstructed[channel], kern, mode='same', boundary='fill', fillvalue=0)
        im_conv = im_conv / np.max(im_conv) * np.max(
            self.reconstructed[channel])  # Normalization needed after convolution

        # Apply the convolution on the mask
        im_conv_mask = self.reconstructed[channel].copy()
        im_conv_mask[self.unsampled_pixels_image] = im_conv[self.unsampled_pixels_idx]

        # Apply a gaussian filter to the convolved image on the mask
        im_gauss_tmp = ndimage.gaussian_filter(self.reconstructed[channel], sigma=sigmas[1])
        im_conv_gauss_mask = self.reconstructed[channel].copy()
        im_conv_gauss_mask[self.unsampled_pixels_idx] = im_gauss_tmp[self.unsampled_pixels_idx]

        return im_conv_gauss_mask

    def hole_kernel(width: uint) -> np.ndarray:
        center = np.uint32(np.around(width / 2, decimals=0))
        kernel = np.ones((width, width))
        kernel[center, center] = 0
        return kernel

    def reconstruct(self, channels: list[str] = ['PMT1']):
        for chan in channels:
            if self.check_channel(chan):
                calc = endoscope.hw.imagecalculator.ImageCalculator(
                    imgsize=self.image_size,
                    timeslice=slice(0, int(len(self.rawdata[chan]))),
                    samples=len(self.rawdata[chan]),
                    samples_auto=True,
                    xvolts=self.rawdata['xpos'],
                    yvolts=self.rawdata['ypos'],
                )
                self.reconstructed[chan] = calc.calc_image(intensities=self.rawdata[chan])
            else:
                self.reconstructed[chan] = np.zeros(shape=(self.image_size, self.image_size))

    def plot_image(self, channel: str = 'PMT1', title: str = '', logscale: bool = False):
        extent = np.array([0, self.image_size - 1, 0, self.image_size - 1])
        img = self.reconstructed[channel]

        fig = plt.figure()
        ax = plt.gca()
        if logscale:
            im = ax.imshow(img, norm=LogNorm(), extent=extent, interpolation='none')
        else:
            im = ax.imshow(img, extent=extent)
        if title:
            plt.title(title)
        fig.colorbar(im)

    @staticmethod
    def show_plots():
        plt.show()


if __name__ == "__main__":
    ### Load calibrated data
    # path = "C:\\Users\\jerem\\OneDrive - Lightcore Technologies\\Documents - www.lightcoreteams.com\\Jérémy\\cal_G202207-05_grin"
    # cal = EndoCalib(path=path)
    # dw = DwellTimeFromMeasurement(calib=cal, fov_um=150, psf_um=2)
    # # print(cal.averaged_data)
    # print(cal.params)

    # plt.figure()
    # plt.plot(cal.averaged_data['intensity'])
    # plt.show()

    ### Load raw data for images
    img = EndoImages(
        filepath='C:/Users/jerem/Downloads/tufts_20221114/raw_G202207-06_obj=2100um4fps/Raw-20221115-014830-198.npy',
    )

    img.read()
    img.get_sampled_pixels()
    img.get_unsampled_pixels()


    plt.figure()
    plt.imshow(img.sampled_pixels_image)
    plt.colorbar()

    plt.figure()
    plt.imshow(img.unsampled_pixels_image)
    plt.colorbar()

    plt.figure()
    #plt.imshow(fullimg)
    plt.imshow(img.fullsampled_image)
    plt.colorbar()


    img.reconstruct(channels=['PMT1'])
    img.plot_image()
    img.show_plots()
