import os

import matplotlib.pyplot as plt

from gausspyplus.prepare import GaussPyPrepare
from gausspyplus.decompose import GaussPyDecompose


def fit(file,j,snr=5,ncomps=4,pad=5):
    #
    #  Set the essential parameters
    #  changing these parameters will have the biggest impact on the decomposition results
    #

    #  First smoothing parameter [float]
    alpha1 = 2.58

    #  Second smoothing parameter (only used if 'two_phase_decomposition = True') [float]
    alpha2 = 5.14

    #  Required minimum signal-to-noise ratio for data peak. [float]
    snr = 3.

    #  Required minimum value for significance criterion. [float]
    significance = 5.


    #
    #  Prepare the spectrum for the decomposition
    #

    #  Initialize the 'GaussPyPrepare' class
    prepare = GaussPyPrepare()

    #  Path to the FITS cube.
    prepare.path_to_file = os.path.join(file)

    prepare.snr = snr
    prepare.significance = significance

    #  Probability threshold given in percent for features of consecutive positive 
    #  or negative channels to be counted as more likely to be a noise feature [float]
    prepare.p_limit = 0.02

    #  Number of channels by which an interval (low, upp) gets extended on both sides, 
    #  resulting in (low - pad_channels, upp + pad_channels) [int]
    prepare.pad_channels = 5

    #  Constrict goodness-of-fit calculations to spectral regions estimated 
    #  to contain signal [True/False]
    prepare.signal_mask = True

    #  Required minimum number of spectral channels that the signal ranges should contain [int]
    prepare.min_channels = 100

    #  Mask out ranges in the spectrum; 
    #  specified as a list of tuples [(low1, upp1), ..., (lowN, uppN)]
    prepare.mask_out_ranges = []

    #  Required signal-to-noise ratio for negative data values 
    #  to be counted as noise spikes [float]
    prepare.snr_noise_spike = 5.

    #  position of the spectrum in the FITS data cube
    data_location = (j, 0)  # given in (ypix, xpix)

    #  prepare the single spectrum for the decomposition step
    prepared_spectrum = prepare.return_single_prepared_spectrum(data_location)


    #
    #  Decompose the prepared spectrum
    #

    #  Initialize the 'GaussPyDecompose' class
    decompose = GaussPyDecompose()

    #  Whether to use one or two smoothing parameters for the decomposition [True/False]
    decompose.two_phase_decomposition = True

    decompose.alpha1 = 2.58
    decompose.alpha2 = 5.14

    #  Note the following parameters only take effect if 'improve_fitting' is set to True

    #  Use the improved fitting routine [True/False]
    decompose.improve_fitting = True

    decompose.snr = snr
    decompose.significance = significance

    #  Exclude Gaussian fit components if their mean position is 
    #  outside the channel range. [bool]
    decompose.exclude_means_outside_channel_range = True

    #  Required minimum value for FWHM values of fitted Gaussian components 
    #  specified in fractions of channels. [float]
    decompose.min_fwhm = 1.

    #  Enforced maximum value for FWHM parameter specified in fractions of channels. 
    #  Use with caution! Can lead to artifacts in the fitting. [float]
    decompose.max_fwhm = None

    #  Required minimum signal-to-noise value for fitted components. 
    #  Defaults to 'snr/2' if not specified. [float]
    decompose.snr_fit = None

    #  Required minimum signal-to-noise value for negative data peaks. 
    #  Used in the search for negative residual peaks. 
    #  Defaults to 'snr' if not specified. [float]
    decompose.snr_negative = None

    #  p-value for the null hypothesis that the normalised residual 
    #  resembles a normal distribution. [float]
    decompose.min_pvalue = 0.01

    #  Factor by which the maximum data value is multiplied to get 
    #  a maximum limit for the fitted amplitudes.
    decompose.max_amp_factor = 1.1

    #  Refit negative residual features. [True/False]
    decompose.refit_neg_res_peak = True

    #  Refit broad components. [True/False]
    decompose.refit_broad = True

    #  Refit blended components. [True/False]
    decompose.refit_blended = True

    #  The required minimum separation between two Gaussian components (mean1, fwhm1) 
    #  and (mean2, fwhm2) is determined as separation_factor * min(fwhm1, fwhm2). [float]
    decompose.separation_factor = 0.8493218

    #  factor by which the FWHM value of a fit component has to exceed all other 
    #  (neighboring) fit components to get flagged [float]
    decompose.fwhm_factor = 2.

    #  maximum number of allowed fit components per spectrum. Use with caution. [int]
    decompose.max_ncomps = None

    decompose.single_prepared_spectrum = prepared_spectrum
    decomposed_test = decompose.decompose()
    
    return decomposed_test['amplitudes_fit'][0],decomposed_test['fwhms_fit'][0],decomposed_test['means_fit'][0]