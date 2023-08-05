"""
This script is from https://github.com/lupitatovar/Llamaradas-Estelares.
"""

import numpy as np
from scipy import special
from scipy.stats import binned_statistic


def flare_eqn(t, ampl):
    """
    The equation that defines the shape for the Continuous Flare Model
    """
    # Values were fit & calculated using MCMC 256 walkers and 30000 steps

    A, B, C, D1, D2, f1 = [
        0.9687734504375167,
        -0.251299705922117,
        0.22675974948468916,
        0.15551880775110513,
        1.2150539528490194,
        0.12695865022878844,
    ]

    f2 = 1 - f1

    eqn = (
        (1 / 2)
        * np.sqrt(np.pi)
        * A
        * C
        * f1
        * np.exp(-D1 * t + ((B / C) + (D1 * C / 2)) ** 2)
        * special.erfc(((B - t) / C) + (C * D1 / 2))
    ) + (
        (1 / 2)
        * np.sqrt(np.pi)
        * A
        * C
        * f2
        * np.exp(-D2 * t + ((B / C) + (D2 * C / 2)) ** 2)
        * special.erfc(((B - t) / C) + (C * D2 / 2))
    )
    return eqn * ampl


def flare_model(t, tpeak, fwhm, ampl, upsample=False, uptime=10):
    """
    The Continuous Flare Model evaluated for single-peak (classical) flare events.
    Use this function for fitting classical flares with most curve_fit
    tools.

    References
    --------------
    Davenport et al. (2014) http://arxiv.org/abs/1411.3723
    Jackman et al. (2018) https://arxiv.org/abs/1804.03377

    Parameters
    ----------
    t : 1-d array
        The time array to evaluate the flare over

    tpeak : float
        The center time of the flare peak

    fwhm : float
        The Full Width at Half Maximum, timescale of the flare

    ampl : float
        The amplitude of the flare


    Returns
    -------
    flare : 1-d array
        The flux of the flare model evaluated at each time

        A continuous flare template whose shape is defined by the convolution of a Gaussian and double exponential
        and can be parameterized by three parameters: center time (tpeak), FWHM, and ampitude
    """

    t_new = (t - tpeak) / fwhm

    if upsample:
        dt = np.nanmedian(np.diff(np.abs(t_new)))
        timeup = np.linspace(min(t_new) - dt, max(t_new) + dt, t_new.size * uptime)

        flareup = flare_eqn(timeup, ampl)

        # and now downsample back to the original time...

        downbins = np.concatenate((t_new - dt / 2.0, [max(t_new) + dt / 2.0]))
        flare, _, _ = binned_statistic(timeup, flareup, statistic="mean", bins=downbins)
    else:

        flare = flare_eqn(t_new, ampl)

    return flare
