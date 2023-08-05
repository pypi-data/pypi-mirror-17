#! python
""" sspals: python tools for analysing single-shot positron annihilation lifetime spectra

    Copyright (c) 2015-2016, UNIVERSITY COLLEGE LONDON
    @author: Adam Deller
"""
from __future__ import print_function, division
from math import floor, ceil
from scipy import integrate
from scipy.special import erf                               # the error function
import numpy as np
import pandas as pd

#    ---------------
#    simulate SSPALS
#    ---------------

def sim(arr, amp=1.0, sigma=2.0E-9, eff=0.3, tau=1.420461E-7, kappa=1.0E-8, **kwargs):
    ''' Approximate a realistic SSPALS spectra, f(t), where arr is an array of 't' (in seconds).

        Gaussian(V_0, sigma) implantation time distribution and formation of o-Ps,
        convolved with detector function -- see below.

        return:
            f(t)

        defaults:
            amp = 1.0                 # scaling factor
            sigma = 2 ns              # Gaussian width
            eff = 0.3                 # o-Ps re-emmission efficiency
            tau = 142.0461 ns         # o-Ps lifetime
            kappa = 10 ns             # detector decay time

        kwargs:
            norm = True               # normalise to max value

    '''
    norm = kwargs.get('norm', True)
    # sim.
    yvals = np.exp(-arr *(1.0 / tau + 1.0 / kappa)) * ( \
            eff * \
            np.exp((sigma**2.0/(2.0 * tau**2.0)) + arr/ kappa) * \
            (1.0 + erf((arr * tau - sigma**2.0)/(np.sqrt(2.0) * sigma * tau))) - \
            (1 + tau * (eff - 1) / kappa) * \
            np.exp((sigma**2.0/(2.0 * kappa**2.0)) + arr/ tau) * \
            (1.0 + erf((arr * kappa - sigma**2.0)/(np.sqrt(2.0) * sigma * kappa))))
    if norm:
        # normalise to peak value
        yvals = yvals / max(yvals)
    return amp * yvals

#    ------------
#    process data
#    ------------

def sub_offset(arr, n_bsub=100):
    ''' Subtract the mean of the first 'n_bsub' number of points for each row in arr.

        return:
            2D numpy array, offset

        defaults:
            n_bsub = 100
    '''
    offset = np.array([np.mean(arr[:, :n_bsub], axis=1)])
    arr = np.subtract(arr, offset.T)
    return arr, offset

def saturated(arr):
    ''' Find where arr (1D) is equal to its own max and min value.

        return:
            1D numpy array (Boolean)
    '''
    sat = np.logical_or(arr == arr.max(), arr == arr.min())
    return sat

def splice(high, low):
    ''' Splice together the high and low gain values of a 2D dataset (swap saturated sections
        in the high-gain channel for the corresponding values in the low-gain channel).

        return:
            2D numpy array
    '''
    mask = np.apply_along_axis(saturated, 1, high)
    flask = mask.flatten()
    vals = low.flatten()[np.where(flask)]          # replacement values
    tmp = high.flatten()
    tmp[flask] = vals
    arr = np.reshape(tmp, np.shape(high))
    return arr

#    -------------
#    validate data
#    -------------

def val_test(arr, min_range):
    ''' Validation test: does arr (1D) contain a signal? i.e., does the vertical range
        exceed min_range?

        return:
            test (Boolean)
    '''
    rng = abs(arr.max() - arr.min())
    return rng > min_range

def validate(arr, **kwargs):
    ''' Filter out rows from arr (2D) that have a vertical range < min_range.

        return:
            2D numpy array

        defaults:
            min_range = 0.1
    '''
    min_range = kwargs.get('min_range', 0.1)
    mask = np.apply_along_axis(val_test, 1, arr, min_range)
    return arr[mask]

#    ------------------------------
#    combine high and low gain data
#    ------------------------------

def chmx(high, low, **kwargs):
    ''' Remove zero offset from high and low gain data, invert and splice
        together by swapping saturated values from the hi-gain channel
        for those from the low-gain channel.  Apply along rows of 2D arrays.

        return:
            2D numpy array

        defaults:
            n_bsub = 100      # number of points to use to find offset
            invert = True     # assume a negative (PMT) signal
            validate = False  # only return rows with a vertical range > min_range
            min_range = 0.1   # see above
    '''
    # options
    invert = kwargs.get('invert', True)
    vtest = kwargs.get('validate', False)
    n_bsub = kwargs.get('n_bsub', 100)
    # remove offsets
    if n_bsub > 0:
        high = sub_offset(high, n_bsub)[0]
        low = sub_offset(low, n_bsub)[0]
    # combine hi/low data
    arr = splice(high, low)
    if invert:
        arr = np.negative(arr)
    if vtest:
        # validate data
        arr = validate(arr, **kwargs)
    return arr

#    --------
#    triggers
#    --------

def cfd(arr, dt, **kwargs):
    ''' Apply cfd algorithm to arr (1D) to find trigger time (t0).

        return:
            trigger (float)

        defaults:
            cfd_scale = 0.8
            cfd_offset = 1.4E-8
            cfd_threshold = 0.04
    '''
    # options
    scale = kwargs.get('cfd_scale', 0.8)
    offset = kwargs.get('cfd_offset', 1.4E-8)
    threshold = kwargs.get('cfd_threshold', 0.04)
    debug = kwargs.get('debug', False)
    # offset number of points
    sub = int(offset /dt)
    x = np.arange(len(arr)) * dt
    # add orig to inverted, rescaled and offset
    z = arr[:-sub]-arr[sub:]*scale
    # find where greater than threshold and passes through zero
    test = np.where(np.logical_and(arr[:-sub-1] > threshold,
                                   np.bool_(np.diff(np.sign(z)))))[0]
    if len(test) > 0:
        ix = test[0]
        # interpolate to find t0
        t0 = z[ix]*(x[ix]-x[ix+1])/(z[ix+1]-z[ix])+x[ix]
    else:
        # no triggers found
        if not debug:
            # fail quietly
            t0 = np.nan
        else:
            raise Warning("cfd failed to find a trigger.")
    return t0

def triggers(arr, dt, **kwargs):
    ''' Apply cfd to each row of arr (2D).

        return:
            1D numpy array

        defaults:
            cfd_scale = 0.8
            cfd_offset = 1.4E-8
            cfd_threshold = 0.04
    '''
    # apply cfd
    trigs = np.apply_along_axis(cfd, 1, arr, dt, **kwargs)
    return trigs

#    ----------------
#    delayed fraction
#    ----------------

def integral(arr, dt, t0, lim_a, lim_b, **kwargs):
    ''' Simpsons integration of arr (1D) between limits=[a, b].

        return:
            float

        defaults:
            corr = True         # apply boundary corrections
            debug = False       # fail quietly, or not if True
    '''
    corr = kwargs.get('corr', True)
    debug = kwargs.get('debug', False)
    if lim_b <= lim_a:
        raise ValueError("upper integration limit should be higher than lower limit.")
    # fractional index
    frac_a = (lim_a + t0) / dt
    frac_b = (lim_b + t0) / dt
    # nearest index
    ix_a = int(round(frac_a))
    ix_b = int(round(frac_b))
    try:
        int_ab = integrate.simps(arr[ix_a:ix_b], None, dt)
        if corr:
            # boundary corrections (trap rule)
            corr_a = dt * (ix_a - frac_a) * (arr[int(floor(frac_a))] + arr[int(ceil(frac_a))]) / 2.0
            corr_b = dt * (ix_b - frac_b) * (arr[int(floor(frac_b))] + arr[int(ceil(frac_b))]) / 2.0
            int_ab = int_ab + corr_a - corr_b
    except:
        if not debug:
            # fail quietly
            int_ab = np.nan
        else:
            raise Warning("Unable to integrate spectra. Check bounday and cfd settings. debug: t0 = ", str(t0))
    return int_ab

def dfrac(arr, dt, t0, **kwargs):
    ''' Calculate the delayed fraction (DF) (int B->C/ int A->C) for arr (1D).

        return:
            AC, BC, DF

        defaults:
            limits = [-1.0E-8, 3.5E-8, 6.0E-7]      # ABC
            corr = True                             # apply boundary corrections
    '''
    lims = kwargs.get('limits', [-1.0E-8, 3.5E-8, 6.0E-7])
    int_ac = integral(arr, dt, t0, lims[0], lims[2], **kwargs)
    int_bc = integral(arr, dt, t0, lims[1], lims[2], **kwargs)
    df = int_bc / int_ac
    return int_ac, int_bc, df

def sspals_1D(arr, dt, **kwargs):
    ''' Calculate the trigger time (cfd) and delayed fraction (BC/AC) for
        arr (1D).

        return:
            np.array([(t0, AC, BC, DF)])

        defaults:
            cfd_scale = 0.8                       # cfd
            cfd_offset = 1.4E-8
            cfd_threshold = 0.04
            limits = [-1.0E-8, 3.5E-8, 6.0E-7]    # delayed fraction ABC
            corr = True                           # apply boundary corrections
            debug = False                         # nans in output? try debug=True.
    '''
    dtype = [('t0', 'float64'), ('AC', 'float64'), ('BC', 'float64'), ('DF', 'float64')]
    t0 = cfd(arr, dt, **kwargs)
    if not np.isnan(t0):
        int_ac, int_bc, df = dfrac(arr, dt, t0, **kwargs)
        output = np.array([(t0, int_ac, int_bc, df)], dtype=dtype)
    else:
        output = np.array([(np.nan, np.nan, np.nan, np.nan)], dtype=dtype)
    return output

def sspals(arr, dt, **kwargs):
    ''' Apply sspals_1D to each row of arr (2D).

        return:
            pandas.DataFrame

            columns=[('t0','float64'),
                     ('AC','float64'),
                     ('BC','float64'),
                     ('DF','float64')]

        defaults:
            dropna = False                     # remove empty rows
            cfd_scale = 0.8                    # cfd
            cfd_offset = 1.4E-8
            cfd_threshold = 0.04
            limits=[-1.0E-8, 3.5E-8, 6.0E-7]   # delayed fraction ABC
            corr = True                        # apply boundary corrections
            debug = False                      # nans in output? try debug=True.
    '''
    dropna = kwargs.get('dropna', False)
    dfracs = pd.DataFrame(np.apply_along_axis(sspals_1D, 1, arr, dt, **kwargs)[:, 0])
    if dropna:
        dfracs = dfracs.dropna(axis=0, how='any')
    return dfracs

#    -------
#    S_gamma
#    -------

def signal(a_val, a_err, b_val, b_err, rescale=100.0):
    ''' Calculate S = (b - a)/ b and the uncertainty.

        return:
            rescale * (S, S_err)

        default:
            rescale = 100.0                # e.g., for percentage units.
    '''
    sig = rescale * (b_val - a_val) / b_val
    sig_err = rescale * np.sqrt((a_err / b_val)**2.0 + (a_val*b_err/(b_val**2.0))**2.0)
    return sig, sig_err
