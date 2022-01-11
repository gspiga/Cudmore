"""
Author: Robert Cudmore
Date: 20211221

Purpose: Load a csv, massage it, and plot.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import seaborn as sns


def plotOneFile(df, filename : str):
	"""
	Plot each file in a figure with subplots corresponding to sweep

	Args:
		df (dataframe): Pandas dataframe with columns ['filename', 'sweeps', peakPhase']
		filename (str): Name of file to plot.

	Notes:
		This is bad form as I am mixing code for plotting and analysis.
	"""

	dfFile = df[ df['filename']==filename ]  # grab specified filename
	sweeps = dfFile['sweep'].unique()  # get list of sweeps [0, 1, 2, ...]

	numSubplot = len(sweeps)
	fig, axs = plt.subplots(numSubplot, 1, sharex=True, figsize=(8, 6))
	fig.suptitle(filename)

	for idx,sweep in enumerate(sweeps):
		dfSweep = dfFile[dfFile['sweep'] == sweep]  # grab one sweep from one file
		peakPhase = dfSweep['peakPhase']  # grab the raw data

		#trying to add something here to maybe make a psuedo time variable for x axis, Ill use the index
		ourIndex = list(range(0, len(peakPhase)))

		# selecting appropriate bins is important
		# lots of different algorithms, not sure which one is best
		# see: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
		bins = 'auto'

		# plot the histogram and grab its data
		#counts, bins, bars = axs[idx].hist(peakPhase, bins=bins)

		#
		# TODO: Do a sine fit of x=bins and y=counts
		#
		# Lets tackle this sine fit

		#Bins and counts arent the same length, so it did not work
		axs[idx].scatter(ourIndex, peakPhase)
		res = fit_sin(ourIndex, peakPhase)
		print(
			"Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res)
		#print(type(ourIndex))
		# Going about plotting the sine curve
		x = np.asarray(ourIndex)

		y = res['amp']*np.sin(res['omega']*x + res['phase']) + res['offset']
		axs[idx].plot(ourIndex, y, 'b')

		axs[idx].set_ylabel('Count')
		axs[idx].set_xlabel('Phase')  # This is phase within a sin wave (we don't know the frequency)

def run(path : str):
	"""
	Each 'filename' is a different recording
		Within each recording we have a number of different sweeps ('sweep')
			Within each sweep are 'peakPhase' values to analyze/fit

	Args:
		path (str): Full path to csv file for analysis.
	"""

	# load the file
	df = pd.read_csv(path)

	# check the format of loaded csv
	print(f'this is what our loaded file looks like, it has {len(df)} rows.')
	print(df.head())

	# print some stats
	aggList = ['count', 'median', 'mean', 'std', 'min', 'max']
	dfTmp = df.groupby(['filename', 'sweep']).agg(aggList)
	print('')
	print("and here it is grouped by ['filename', 'sweep'] ...")
	print(dfTmp)

	# plot each file in a figure with subplots corresponding to sweep
	filenames = df['filename'].unique()
	for filename in filenames:
		plotOneFile(df, filename)

		#
	plt.show()


def fit_sin(tt, yy):
	# declaring response and explanatory variables as numpy arrays
	tt = np.array(tt)  # xdata
	yy = np.array(yy)  # ydata
	# np.fft computes the  one-dimensional discrete Fourier Transform
	# np.fft.fftfreq returns Discrete Fourier Transform sample frequencies
	ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
	Fyy = abs(np.fft.fft(yy))

	# Preliminary guesses of the parameters of sine function (this will not fit well)
	guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])  # excluding the zero frequency "peak", which is related to offset
	guess_amp = np.std(
		yy) * 2. ** 0.5  # this uses the standard deviation rather than the root mean square, might want to investigate which is better
	guess_offset = np.mean(yy)  # guessing the constant C with the mean of the data
	guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

	def sinfunc(t, A, w, p, c):  return A * np.sin(
		w * t + p) + c  # this one-liner returns the format for the sin equation

	# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
	# Scipy.optimize takes multiple parameters to fit non-linear data, p0 is an optional variable for guess of parameters
	# optimize returns 2 objects: popt is optimal values for paramters where SQUARED RESIDUALS are minimized
	# pcov is a 2-D array that is the estimated covariance of popt

	popt, pcov = scipy.optimize.curve_fit(f=sinfunc, xdata=tt, ydata=yy, p0=guess)
	A, w, p, c = popt  # takes the optimized variables
	f = w / (2. * np.pi)  # still need to understand why omega is divided by 2pi, radian conversion?
	fitfunc = lambda t: A * np.sin(w * t + p) + c  # lambda function to build sin expression
	return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1. / f, "fitfunc": fitfunc,
			"maxcov": np.max(pcov), "rawres": (guess, popt, pcov)}


if __name__ == '__main__':
	#
	# change this to location of your csv file
	#
	#path = '/home/cudmore/Sites/SanPy/colin/gianni-master.csv'
	path = "C:/Users/Gianni/Desktop/Github/Cudmore/SinusoidalRegress/gianni-master-20220104.csv"
	run(path)


