import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


class Filtering:
    default_window = 11
    default_polyorder = 3

    @classmethod
    def savgol(data, window: int = 0, order: int = 0):
        applied_window = window if window else Filtering.default_window
        applied_polyorder = order if order else Filtering.default_polyorder
        savgol_filter(data, applied_window, applied_polyorder)



class DwellTimePlots:
    @staticmethod
    def waveform_r_vs_t(t: list(), r: list(), unit_str: str = 'um', unit_multiplier: float = 1e6) -> None:
        plt.figure()
        plt.plot(t, r * unit_multiplier, label='r')
        plt.title('Probe position during scan phase')
        plt.xlabel('Time [s]')
        plt.ylabel('Position [' + unit_str + ']')

    @staticmethod
    def waveform_xyr_vs_t(t: list(), x: list(), y: list(), unit_str: str = 'um', unit_multiplier: float = 1e6) -> None:
        plt.figure()
        plt.plot(t, x * unit_multiplier, label='x')
        plt.plot(t, y * unit_multiplier, label='y')
        plt.plot(t, np.sqrt(x ** 2 + y ** 2) * unit_multiplier, label='r = sqrt(x^2 +y^2)')
        plt.title('Probe position during scan phase')
        plt.xlabel('Time [s]')
        plt.ylabel('Position [' + unit_str + ']')
        plt.legend()

    @staticmethod
    def xy_plane(x: list(), y: list(), unit_str: str = 'um', unit_multiplier: float = 1e6, color: str = 'g'):
        plt.figure()
        plt.axis('equal')
        plt.plot(x * unit_multiplier, y * unit_multiplier, color=color)
        plt.title('Probe position during scan phase')
        plt.xlabel('x [' + unit_str + ']')
        plt.xlabel('y [' + unit_str + ']')

    @staticmethod
    def speeds_xytot_vs_t(t: list(),
                          vx: list(), vy: list(), vt: list(),
                          filter: bool = True, normalize_x: bool = False
                          ) -> None:

        t = t / np.max(t) if normalize_x else t
        xlabel = 'Normalized time' if normalize_x else 'Time [s]'
        vx = Filtering.savgol(vx) if filter else vx
        vy = Filtering.savgol(vy) if filter else vy
        vt = Filtering.savgol(vt) if filter else vt

        plt.figure()
        plt.plot(t, vx, label='vx')
        plt.plot(t, vy, label='vy')
        plt.plot(t, vt, label='v = sqrt(vx^2 + vy^2)')
        plt.title('PSF speed during scan phase')
        plt.xlabel(xlabel)
        plt.ylabel('Speed [m/s]')
        plt.legend()

    @staticmethod
    def dwell_time_vs_t(t: list(), dw: list(),
                        unit_str: str = 'us', unit_multiplier: float = 1e6,
                        filter: bool = True, normalize_x: bool = False,
                        yscale: str = 'log',
                        color: str = 'k') -> None:

        t = t / np.max(t) if normalize_x else t
        dw = Filtering.savgol(dw) if filter else dw
        xlabel = 'Normalized time' if normalize_x else 'Time [s]'

        plt.figure()
        plt.plot(t, dw * unit_multiplier, color=color)
        plt.gca().set_yscale(yscale)
        plt.title('PSF dwell time')
        plt.xlabel(xlabel)
        plt.ylabel('Exposure [' + unit_str + ']')

    @staticmethod
    def dwell_time_vs_r(r: list(), dw: list(),
                        unit_str: str = 'us', unit_multiplier: float = 1e6,
                        filter: bool = True, normalize_x: bool = False,
                        yscale: str = 'log',
                        color: str = 'k') -> None:

        r = r / np.max(r) if normalize_x else r*1e6
        dw = Filtering.savgol(dw) if filter else dw
        xlabel = 'Normalized radius' if normalize_x else 'Radius [um]'

        plt.figure()
        plt.plot(r, dw * unit_multiplier, color=color)
        plt.gca().set_yscale(yscale)
        plt.title('PSF dwell time')
        plt.xlabel(xlabel)
        plt.ylabel('Exposure [' + unit_str + ']')


    @staticmethod
    def show():
        plt.show()

