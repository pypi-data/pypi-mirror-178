import sys
import warnings
import logging

import numpy as np


# Rewrite attempt of volts to pixels.
log = {}


class ImageCalculator:
    """The ImageCalculator class handles the computation
    """

    def __init__(
        self,
        imgsize=385,
        timeslice=None,
        samples=None,
        samples_auto=True,
        xvolts=None,
        yvolts=None,
    ):
        """Constructor.
        imgsize : int, the size of the square image (default 385)
        timeslice : slice, time slice to look at (default None)
        samples : int, the number of samples
        sample_auto : bool, default True
            indicates if samples can(not) auto update
        xvolts, yvolts : np.ndarray, default None
            x and y voltages arrays on which interpolation is based on
        """
        self._imgsize = imgsize
        self._samples = samples
        self.samples_auto = samples_auto
        self._timeslice = timeslice
        self._xvolts = np.asarray(xvolts).copy()
        self._yvolts = np.asarray(yvolts).copy()
        self._xv = None  # x voltages (interpolated to self.samples)
        self._yv = None  # y voltages (interpolated to self.samples)
        self._xmean = None  # x center offset factor
        self._ymean = None  # y center offset factor
        self._ppv = None  # scale factor (pixel per volt)
        self._xp = None  # x pixel list (1D array)
        self._yp = None  # y pixel list (1D array)
        self._xycomplex = None  # repetition list (1D array)
        self._replist = None  # repetition list (1D array)
        self._repmat = None  # repetition matrix (2D array)
        self._intensities = None  # last image data (1D array)
        self._image = None  # last image data (2D array)
        self.log = logging.getLogger("endoscope.ImageCalculator")

        log["imgcalc"] = self.log
        self.log.debug("instanciated")

    def update(self, **kwargs):

        """Set one or more attributes."""
        warnings.warn("the ImagCalculator.update() method is deprecated")

        for key, value in kwargs.items():
            if key in {
                "imgsize",
                "samples",
                "samples_auto",
                "timeslice",
                "xvolts",
                "yvolts",
            }:
                self.__setattr__(key, value)
        return True

    def unset(self, *args):
        """Unset one or more attributes."""
        self.log.debug("unsetting %s.", args)
        for att in args:
            self.__setattr__(att, None)
        return True

    def xy_data_ready(self):
        if None in (self.xvolts, self.yvolts, self._samples) and None in (
            self._xv,
            self._yv,
            self._xmean,
        ):
            return False
        return True

    def clear(self):
        """Erase history, forcing to start calculations anew."""
        self.xvolts = None
        self.yvolts = None

    # TODO: implement time slice as an __index__ method
    # TODO: Extra feature: supporting fractional slices to be interpreted as a percentage

    # Data variables (and +parameter) dependency tree:
    #
    # xvolts => (+samples) => xvmean,xv  (interpolated (double) voltage list)
    # xv => (+imgsize) => xppv
    # xv => (+timeslice) => xp  (pixel list)
    # xp,yp => replist  (repetition list depends on time slice!)
    # xp,yp,replist => repmat
    # xp,yp,replist,intensity => intmat

    def calc_xyv(self):
        """Calculate x, y volts interpolated."""
        _timeo = np.linspace(
            0, np.size(self.xvolts) - 1, np.size(self.xvolts)
        )  # time original
        _timei = np.linspace(
            0, np.size(self.xvolts) - 1, self.samples
        )  # time interpolated
        if self.xvolts is None:
            raise ValueError("Forgot to set xvolts?")  # prevent errors later on
        if self.yvolts is None:
            raise ValueError("Forgot to set yvolts?")  # prevent errors later on
        self._xv = np.interp(_timei, _timeo, self.xvolts)
        self._yv = np.interp(_timei, _timeo, self.yvolts)
        return (self.xv, self.yv)

    def calc_ppv(self):
        """Calculate pixels per volt."""
        _diffx = np.abs(np.amax(self.xv) - np.amin(self.xv))
        _diffy = np.abs(np.amax(self.yv) - np.amin(self.yv))
        _max = np.amax([_diffx, _diffy])
        self._ppv = (self.imgsize - 1) / _max  # pixels per volt
        return self._ppv

    def calc_xp(self):
        """Calculate x pixel list from voltage positions."""
        _x = (self.xv[self.timeslice] - self.xmean) * self.ppv + self.imgsize / 2
        self._xp = np.floor(_x).astype(int, copy=False)
        return self._xp

    def calc_yp(self):
        """Calculate y pixel list from voltage positions."""
        _y = (self.yv[self.timeslice] - self.ymean) * self.ppv + self.imgsize / 2
        self._yp = np.floor(_y).astype(int, copy=False)
        return self._yp

    def calc_replist(self):
        """Calculate repetition list from x,y pixel lists"""
        # Combine xp and yp into one 1D complex array
        self._xycomplex = self.xp + self.yp * 1j
        # These values thus are unique numbers for each pixel (x,y), and we want to count them
        # Get the unique values, their indices and counts of them
        _uvals, _uid, _ucnts = np.unique(
            self._xycomplex, return_inverse=True, return_counts=True
        )
        # _uvals contains unique values (shorter array), _uid, _ucnts are equal in length to _xy,
        # containing the indices to reproduce the original array and the counts of each, resp.
        # so that _xy = _uvals[_uid] returns the original array, and
        self._replist = _ucnts[_uid]  # occurences of each item in the original array
        return self._replist

    def calc_repmat(self):
        self._repmat = self.get_hist()
        return self._repmat

    def calc_image(self, intensities=None):
        """Calculate image pixels, assume intensities total is of size samples."""
        if intensities is not None and np.all(intensities == 0):
            self._image = None
            return None
        if np.size(intensities) != self.samples:
            if self.samples_auto:
                # auto adjust samples to trigger auto-recalculation (interpolation)
                self.log.debug("auto adjust samples to %s.", np.size(intensities))
                self.samples = np.size(intensities)
            else:
                raise ValueError(
                    "calc_image: intensities must be of size equal to samples."
                )  # prevent errors later on
        elif (
            self._intensities is not None
            and self._image is not None
            and np.all(self._intensities == intensities)
        ):
            # Same as previous image
            self.log.debug("same.")
            return self._image

        # Save for later comparison.
        self._intensities = intensities.copy()  # COPY IS CRAZY IMPORTANT
        # Calculate 2d histogram of the slice of intensities and normalize by repetition list
        self._image = self.get_hist(self._intensities[self.timeslice] / self.replist)
        return self._image

    def get_hist(self, intensities=None):
        """Get the repetition matrix or image matrix, which are
        2d histograms of pixelslist (with intensities as weights)."""
        if intensities is None:
            (hist, x, y) = np.histogram2d(
                self.xp,
                self.yp,
                bins=self.imgsize,
                range=np.multiply([[0, 1], [0, 1]], self.imgsize),
            )
        else:
            (hist, x, y) = np.histogram2d(
                self.xp,
                self.yp,
                weights=intensities,
                bins=self.imgsize,
                range=np.multiply([[0, 1], [0, 1]], self.imgsize),
            )
        return hist

    @property
    def samples(self):
        if self._samples is not None:
            return self._samples
        else:
            if isinstance(self.xvolts, np.ndarray):
                # obtain samples from original xvolts,yvolts (assume no interpolation)
                self._samples = np.size(self.xvolts)
                return self._samples
            else:
                raise ValueError(
                    "samples: cannot infer samples from xvolts (forgot to set xvolts?)."
                )

    @samples.setter
    def samples(self, samples):
        if samples is None or samples < 1:  # unsetting samples
            self._samples = None
            self.xv = None
            self.yv = None
        elif self._samples is not None and samples != self._samples:
            self._samples = samples
            self.xv = None
            self.yv = None  # unset dependencies, must be recalculated
        else:
            self._samples = samples  # first time or no change

    @property
    def imgsize(self):
        if self._imgsize is not None:
            return self._imgsize
        else:
            raise ValueError(
                "None: imgsize (forgot to set?)."
            )  # prevent errors later on

    @imgsize.setter
    def imgsize(self, imgsize):
        if imgsize is None or imgsize < 1:
            self._imgsize = None
            self.ppv = None
        elif self._imgsize is not None and self._imgsize == imgsize:
            pass  # no change, keep values
        elif imgsize > 4096:
            raise ValueError(
                "cannot accept imgsize above 4096."
            )  # prevent errors later on
        else:
            self._imgsize = imgsize
            self.ppv = None

    @property
    def timeslice(self):
        if self._timeslice is not None:
            return self._timeslice
        else:
            self._timeslice = slice(
                None
            )  # default: no slicing, meaning the whole cake.
            return self._timeslice

    @timeslice.setter
    def timeslice(self, timeslice):
        if timeslice is None:
            self._timeslice = None
            self.xp = None
            self.yp = None  # unset dependencies, must be recalculated
        elif not isinstance(timeslice, slice):
            raise ValueError(
                "Expected a slice while setting timeslice, got %s." % type(timeslice)
            )
        elif self._timeslice is not None and self._timeslice == timeslice:
            pass  # no change
        else:
            self._timeslice = timeslice
            self.xp = None
            self.yp = None  # unset dependencies, must be recalculated

    @property
    def xvolts(self):
        return self._xvolts

    @xvolts.setter
    def xvolts(self, xvolts):
        if xvolts is None:
            self.log.debug("resetting xvolts")
            self._xvolts = None
            self.xvmean = None
            self.xv = None
            # self.unset("xvmean", "xv")  # unset dependencies
        elif isinstance(xvolts, np.ndarray):
            if isinstance(self._xvolts, np.ndarray) and np.all(self._xvolts == xvolts):
                self.log.debug("setting same...")
            else:
                self.xvmean = None
                self.xv = None
                self._xvolts = xvolts.copy()  # COPY IS CRAZY IMPORTANT
        else:
            raise ValueError(
                "Expected numpy.ndarray while setting xvolts, got %s." % type(xvolts)
            )  # prevent errors later on

    @property
    def yvolts(self):
        return self._yvolts

    @yvolts.setter
    def yvolts(self, yvolts):
        if yvolts is None:
            self._yvolts = None
            self.yvmean = None
            self.yv = None
            # self.unset("yvmean", "yv")  # unset dependencies
        elif isinstance(yvolts, np.ndarray):
            if isinstance(self._yvolts, np.ndarray) and np.all(self._yvolts == yvolts):
                self.log.debug("setting same...")
            else:
                self.yvolts = None  # unset dependencies (see above in this setter)
                self._yvolts = yvolts.copy()  # COPY IS CRAZY IMPORTANT
        else:
            raise ValueError(
                "Expected numpy.ndarray while setting yvolts, got %s." % type(yvolts)
            )  # prevent errors later on

    @property
    def xmean(self):
        # if self._xmean is not None:
        #     return self._xmean
        # else:
        self._xmean = np.mean(self.xvolts)
        return self._xmean

    @xmean.setter
    def xmean(self, xmean):
        if xmean is None:
            self._xmean = None
            self.unset("xv")  # unset dependencies

    @property
    def ymean(self):
        # if self._ymean is not None:
        #     return self._ymean
        # else:
        self._ymean = np.mean(self.yvolts)
        return self._ymean

    @ymean.setter
    def ymean(self, ymean):
        if ymean is None:
            self._ymean = None
            self.unset("yv")  # unset dependencies

    @property
    def xv(self):
        if self._xv is not None:
            return self._xv
        else:
            self.calc_xyv()  # calculate xv and yv at once
            return self._xv

    @xv.setter
    def xv(self, xv):
        if xv is None:
            self._xv = None
            self.ppv = None  # unset dependencies
        else:
            raise ValueError("Use calc_xyv() instead of setting xv directly.")

    @property
    def yv(self):
        if self._yv is not None:
            return self._yv
        else:
            self.calc_xyv()  # calculate xv and yv at once
            return self._yv

    @yv.setter
    def yv(self, yv):
        if yv is None:
            self._yv = None
            self.ppv = None  # unset dependencies
        else:
            raise ValueError("Use calc_xyv() instead of setting yv directly.")

    @property
    def ppv(self):
        if self._ppv is not None:
            return self._ppv
        else:
            return self.calc_ppv()

    @ppv.setter
    def ppv(self, ppv):
        if ppv is None:
            self._ppv = None
            self.xp = None
            self.yp = None
        else:
            raise ValueError("Use calc_ppv() instead of setting ppv directly.")

    @property
    def yp(self):
        if self._yp is not None:
            return self._yp
        else:
            return self.calc_yp()

    @yp.setter
    def yp(self, yp):
        if yp is None:
            self._yp = None
            self.replist = None  # unset dependencies
        else:
            raise ValueError("Use calc_yp() instead of setting yp directly.")

    @property
    def xp(self):
        if self._xp is not None:
            return self._xp
        else:
            return self.calc_xp()

    @xp.setter
    def xp(self, xp):
        if xp is None:
            self._xp = None
            self.replist = None  # unset dependencies
        else:
            raise ValueError("Use calc_xp() instead of setting xp directly.")

    @property
    def replist(self):
        if self._replist is not None:
            return self._replist
        else:
            return self.calc_replist()

    @replist.setter
    def replist(self, replist):
        if replist is None:
            self._replist = None
            self.image = None
            self.repmat = None
        else:
            raise ValueError("Use calc_replist() instead of setting replist directly.")

    @property
    def repmat(self):
        if self._repmat is not None:
            return self._repmat
        else:
            return self.calc_repmat()

    @repmat.setter
    def repmat(self, repmat):
        if repmat is None:
            self._repmat = None
        else:
            raise ValueError("Use calc_repmat() instead of setting repmat directly.")

    @property
    def image(self):
        if self._image is not None:
            return self._image
        elif self._intensities is not None:
            return self.calc_image(self._intensities)
        else:
            raise ValueError("Use calc_image(intensities) to populate image.")

    @image.setter
    def image(self, image):
        if image is None:
            self._image = None
        else:
            raise ValueError(
                "Use calc_image(intensities) instead of setting image directly."
            )


## Test this module
if __name__ == "__main__":
    pass
