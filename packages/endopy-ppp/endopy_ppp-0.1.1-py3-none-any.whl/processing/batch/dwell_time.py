import matplotlib.pyplot as plt
import numpy as np

from processing.core.recon import DwellTimeFromSimulation
from processing.libs.waveform import Waveform


def default_waveform() -> Waveform:
    W = Waveform(
        samplefreq=250_000,
        stime=0.3,
        sfreq=1230,
        sampcos=0.5,
        sampsin=0.5,
        stheta=0,
        sphaserel=0,
        btimecos=0.05,
        bfreqcos=1233,
        bampcos=0.0,
        btimesin=0.05,
        bfreqsin=1227,
        bampsin=0.0,
        bphaserel=45,
        btheta=-10,
        bphase=61.7819,
        btimerest=0.06,
    )
    return W


def batch_dwelltime_simulation_from_psf(waveform: Waveform, fov: float, psfs: np.array(float),
                                        normalize_xaxis: bool = True) -> list:
    sims = []

    for psf in psfs:
        sims.append(DwellTimeFromSimulation(waveform=waveform, psf=psf, fov=fov, points='expansion'))

    fig = plt.figure()
    for i in range(0, len(sims)):
        if normalize_xaxis:
            x = sims[i].r_vec[sims[i].td0_idx] / np.max(sims[i].r_vec[sims[i].td0_idx]) * 100
            plt.xlabel('Radius / Max radius [%]')

        else:
            x = sims[i].r_vec[sims[i].td0_idx] * 1e6
            plt.xlabel('Radius [us]')

        plt.plot(x, sims[i].dwell_time * 1e6,
                 label=('PSF = ' + str(psfs[i] * 1e6) + ' um'))

    plt.gca().set_yscale('log')
    plt.title(f"PSF dwell time during scan phase \n (FOV = {fov * 1e6} um, scan time = {waveform.stime * 1e3} ms)")
    plt.ylabel('PSF dwell time [us]')
    plt.legend()

    return sims, fig


def batch_dwelltime_simulation_from_fov(waveform: Waveform, fovs: np.array(float), psf: float,
                                        normalize_xaxis: bool = True) -> list:
    sims = []

    for fov in fovs:
        sims.append(DwellTimeFromSimulation(waveform=waveform, psf=psf, fov=fov, points='expansion'))

    fig = plt.figure()
    for i in range(0, len(fovs)):
        if normalize_xaxis:
            x = sims[i].r_vec[sims[i].td0_idx] / np.max(sims[i].r_vec[sims[i].td0_idx]) * 100
            plt.xlabel('Radius / Max radius [%]')

        else:
            x = sims[i].r_vec[sims[i].td0_idx] * 1e6
            plt.xlabel('Radius [us]')

        plt.plot(x, sims[i].dwell_time * 1e6,
                 label=('FOV = ' + str(int(np.ceil(fovs[i] * 1e6))) + ' um'),
                 )

    plt.gca().set_yscale('log')
    plt.title(f"PSF dwell time during scan phase \n (PSF = {psf * 1e6} um, scan time = {waveform.stime * 1e3} ms)")
    plt.ylabel('PSF dwell time [us]')
    plt.legend()

    return (sims, fig)


def batch_dwelltime_simulation_from_stime(waveform: Waveform, stimes: np.array(float), fov: np.array(float), psf: float,
                                          normalize_xaxis: bool = True) -> list:
    sims = []

    for stime in stimes:
        waveform.stime = stime
        sims.append(DwellTimeFromSimulation(waveform=waveform, psf=psf, fov=fov, points='expansion'))

    fig = plt.figure()
    for i in range(0, len(stimes)):
        if normalize_xaxis:
            x = sims[i].r_vec[sims[i].td0_idx] / np.max(sims[i].r_vec[sims[i].td0_idx]) * 100
            plt.xlabel('Radius / Max radius [%]')

        else:
            x = sims[i].r_vec[sims[i].td0_idx] * 1e6
            plt.xlabel('Radius [us]')

        plt.plot(x, sims[i].dwell_time * 1e6,
                 label=('Scan time = ' + str(int(np.ceil(stimes[i] * 1e3))) + ' ms'),
                 )

    plt.gca().set_yscale('log')
    plt.title(f"PSF dwell time during scan phase \n (FOV = {fov * 1e6} um, PSF = {psf * 1e6} um)")
    plt.ylabel('PSF dwell time [us]')
    plt.legend()

    return (sims, fig)


if __name__ == '__main__':
    wf = default_waveform()
    fov = 400e-6
    psf = 2e-6

    sims1, figs1 = batch_dwelltime_simulation_from_psf(
        waveform=wf,
        psfs=[1e-6, 2e-6, 3e-6],
        fov=fov,
        normalize_xaxis=True,
    )

    sims2, figs2 = batch_dwelltime_simulation_from_fov(
        waveform=wf,
        psf=psf,
        fovs=[100e-6, 200e-6, 300e-6, 400e-6],
        normalize_xaxis=True,
    )

    sims3, figs3 = batch_dwelltime_simulation_from_stime(
        waveform=wf,
        stimes=[0.1, 0.2, 0.5, 0.8],
        fov=fov,
        psf=psf,
        normalize_xaxis=True,
    )

    plt.show()
