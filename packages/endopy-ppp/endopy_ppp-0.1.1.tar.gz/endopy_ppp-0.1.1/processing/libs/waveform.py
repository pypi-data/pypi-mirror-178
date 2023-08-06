"""endoscope.hw.waveform -- This module handles scan+brake parameters and the corresponding waveforms of Time and Voltages.
"""
import logging
import warnings
from dataclasses import asdict, dataclass

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Waveform:
    """This constructs a set of Time and Voltage waveforms based on a set of parameters."""

    # Public parameters, and default values (way to small, so good for display/testing purposes)
    samplefreq: float = 5e2
    sfreq: float = 1
    stime: float = 1
    sampcos: float = 0.9
    sampsin: float = 0.9
    stheta: float = 22.5
    sphaserel: float = 0.2
    bfreqcos: float = 5.0
    bfreqsin: float = 5.0
    btimecos: float = 1.0
    btimesin: float = 1.0
    btimerest: float = 1.0
    bampcos: float = 0.9
    bampsin: float = 0.9
    btheta: float = 22.5
    bphase: float = 0.0
    bphaserel: float = 0.0
    __Computed: bool = False

    def get_params(self):
        return asdict(self)

    def Update(self, **kwargs):
        warnings.warn("Upercase Update method is deprecated")
        self.update(**kwargs)

    def update(self, **kwargs):
        """Set one or more waveform parameters."""
        for key, value in kwargs.items():
            oldval = getattr(self, key)
            if value != oldval:
                # print('Waveform.update(): setting %s, value %f'% (key, value))
                setattr(self, key, value)
                self.__Computed = False

        if not self.__Computed:
            try:
                self.compute_scan()
            except Exception as e:
                print("Waveform.update(): Glitched.")
                print(e)

    def ComputeScan(self):
        """Compute time vector and voltage waveforms ... """
        warnings.warn("Upercase ComputeScan method is deprecated")
        return self.compute_scan()

    def compute_scan(self):

        # Derive time variables etc
        self._spts = np.int(np.ceil(self.stime * self.samplefreq))
        self._bptscos = np.int(np.ceil(self.btimecos * self.samplefreq))
        self._bptssin = np.int(np.ceil(self.btimesin * self.samplefreq))
        self._bpts = np.int(np.ceil(np.max([self._bptscos, self._bptssin])))
        self._rpts = np.int(np.ceil(self.btimerest * self.samplefreq))
        self._totaltimestep = np.divide(1.0, self.samplefreq)
        self._pts = self._spts + self._bpts + self._rpts
        self._totaltime = self._totaltimestep * self._pts

        # Modulation, resonance, and brake frequencies
        if self.stime > 0:
            modfreq2pi = 2.0 * np.pi * 1 / (4.0 * self.stime)
        else:
            modfreq2pi = 2.0 * np.pi / 2

        sfreq2pi = 2.0 * np.pi * self.sfreq
        bfreqcos2pi = 2.0 * np.pi * self.bfreqcos
        bfreqsin2pi = 2.0 * np.pi * self.bfreqsin
        # Offsets
        sphaserelrad = np.deg2rad(self.sphaserel)
        bphaserelrad = np.deg2rad(self.bphaserel)
        bphaserad = np.deg2rad(self.bphase)
        sthetarad = np.deg2rad(self.stheta)

        bthetarad = np.deg2rad(self.stheta)
        binitphaserad = sfreq2pi * self.stime + bphaserad + np.pi / 2

        # Time vector
        self._time = np.arange(0, self._totaltime, self._totaltimestep, dtype=float)

        # Virtual Voltages x (cosine wave) and y (sine wave)
        # copy time array
        Vx = np.zeros_like(self._time)
        Vy = np.zeros_like(self._time)
        # scan expansion section of Vx and Vy
        Vx[: self._spts] = (
            self.sampcos
            * np.cos(sfreq2pi * self._time[: self._spts] + sphaserelrad)
            * np.sin(modfreq2pi * self._time[: self._spts])
        )
        Vy[: self._spts] = (
            self.sampsin
            * np.sin(sfreq2pi * self._time[: self._spts])
            * np.sin(modfreq2pi * self._time[: self._spts])
        )
        # braking section of Vx and Vy
        Vx[self._spts : self._spts + self._bptscos] = self.bampcos * np.cos(
            bfreqcos2pi * self._time[self._spts : self._spts + self._bptscos]
            + binitphaserad
            + bphaserelrad
        )
        Vy[self._spts : self._spts + self._bptssin] = self.bampsin * np.sin(
            bfreqsin2pi * self._time[self._spts : self._spts + self._bptssin]
            + binitphaserad
        )
        # rest is the remainder, already zeros.

        # Real Voltages
        # copy time array
        self._Vx_r = np.zeros_like(self._time)
        self._Vy_r = np.zeros_like(self._time)
        self._Vx_r[: self._spts] = Vx[: self._spts] * np.cos(sthetarad) - Vy[
            : self._spts
        ] * np.sin(sthetarad)
        self._Vy_r[: self._spts] = Vx[: self._spts] * np.sin(sthetarad) + Vy[
            : self._spts
        ] * np.cos(sthetarad)

        self._Vx_r[self._spts : self._spts + self._bpts] = Vx[
            self._spts : self._spts + self._bpts
        ] * np.cos(bthetarad) - Vy[self._spts : self._spts + self._bpts] * np.sin(
            bthetarad
        )
        self._Vy_r[self._spts : self._spts + self._bpts] = Vx[
            self._spts : self._spts + self._bpts
        ] * np.sin(bthetarad) + Vy[self._spts : self._spts + self._bpts] * np.cos(
            bthetarad
        )

        # print('Waveform.compute_scan(): done')
        self.__Computed = True

    @property
    def Vx_r(self):
        """Return Vx (real voltage x)."""
        if not self.__Computed:
            self.compute_scan()
        return self._Vx_r

    @property
    def Vy_r(self):
        """Return Vy (real voltage y)."""
        if not self.__Computed:
            self.compute_scan()
        return self._Vy_r

    @property
    def Time(self):
        """Return Time (Time vector)."""
        if not self.__Computed:
            self.compute_scan()
        return self._time

    # Figure Plotting Methods
    def get_timeslice_by_word(self, word="all"):
        word = word.lower()
        if word in ["timeslice", "all", "all time"]:
            return slice(None)

        elif word in ["expansion", "scan", "scan phase"]:
            return slice(0, self._spts)

        elif word in ["expansion_mid"]:
            return slice(
                self._spts // 4, self._spts // 4 + self._spts // 4
            )  # second quarter

        elif word in ["expansion_end", "expansion_end16"]:
            return slice(self._spts - self._spts // 16, self._spts)  # last sixteenth

        elif word in ["expansion_end1024"]:
            return slice(self._spts - 1024, self._spts)  # last 1024 points

        elif word in ["expansion_end4"]:
            return slice(self._spts - self._spts // 4, self._spts)  # last quarter

        elif word in ["expansion_end2", "expansion_half"]:
            return slice(self._spts - self._spts // 2, self._spts)  # last half

        elif word in ["brake+rest"]:
            return slice(
                self._spts, self._spts + self._bpts + self._rpts
            )  # brake plus rest

        elif word in ["brake", "brake phase"]:
            return slice(self._spts, self._spts + self._bpts)  # brake

        elif word in ["brake_start", "brake_start16"]:
            return slice(
                self._spts, self._spts + self._bpts // 16
            )  # brake first sixteenth

        elif word in ["brake_end", "brake_end16"]:
            return slice(
                self._spts + self._bpts - self._bpts // 16, self._spts + self._bpts
            )  # brake last sixteenth
        elif word in ["brake_end+rest"]:
            return slice(
                self._spts + self._bpts - self._bpts // 8,
                self._spts + self._bpts + self._rpts,
            )  # brake end plus rest
        elif word in ["rest", "rest phase"]:
            return slice(
                self._spts + self._bpts, self._spts + self._bpts + self._rpts
            )  # rest
        elif word in ["rest2", "rest half"]:
            return slice(
                self._spts + self._bpts - self._bpts // 4,
                self._spts + self._bpts + self._rpts,
            )  # rest half
        elif word in ["rest_end", "rest_end16"]:
            return slice(
                self._spts + self._bpts + self._rpts - self._rpts // 16,
                self._spts + self._bpts + self._rpts,
            )  # rest last sixteenth
        elif word in ["rest_end8"]:
            return slice(
                self._spts + self._bpts + self._rpts - self._rpts // 8,
                self._spts + self._bpts + self._rpts,
            )  # rest last eighth
        else:
            raise ValueError("that word has no meaningful timeslice: %s" % word)

    def GetStartStopPoints(self, points="all"):
        """Calculate the start and stop points of the measured data."""
        points = points.lower()
        if points in ["timeslice", "all", "all time"]:
            start = 0
            stop = self._pts
        elif points in ["expansion"]:
            start = 0
            stop = self._spts
        elif points in ["expansion_mid"]:
            n_points = self._spts // 4
            start = n_points // 4  # self.w._spts//32 - n_points//2
            stop = start + n_points
        elif points in ["expansion_end"]:
            n_points = self._spts // 16
            start = self._spts - n_points // 2
            stop = start + n_points
        elif points in ["brake"]:
            start = self._spts - self._bpts // 4
            stop = start + self._bpts + self._rpts
        elif points in ["rest"]:
            start = self._spts + self._bpts
            stop = start + self._rpts
        else:
            raise ValueError(
                "Waveform.GetStartStopPoints(points): illegal value in points argument."
            )
        return (start, stop)

    def GetPlotXY(self):
        """Return a plot figure of the Waveform in an XY graph."""
        fig, ax = plt.subplots()
        ax.plot(self.Vx_r, self.Vy_r, "y+-")
        ax.set_xlabel("X (a.u.)")
        ax.set_ylabel("Y (a.u.)")
        return fig

    def PlotXY(self):
        """Show a plot of the Waveform in an XY graph."""
        f = self.GetPlotXY()
        f.show()

    def GetPlotWaveforms(self):
        """Return a plot figure of the Waveforms ."""
        plt.plot(self.Time, self.Vx_r, "b-")
        plt.plot(self.Time, self.Vy_r, "r-")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude (a.u.)")
        return plt.gcf()

    def PlotWaveforms(self):
        """Show a plot of the Waveforms ."""
        f = self.GetPlotWaveforms()
        f.show()
