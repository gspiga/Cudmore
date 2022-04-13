### Introduction 
Welcome! This repository is made up of multiple projects that I take on as a Student Assistant at the Cudmore/Santana Lab at the UC Davis Health Department 
of Physiology and Memebrane Biology. So far, you will find projects and explorations pertaining to electrophysiology. Below I will provide a short summary of what can be
found in each project folder. 

### Sinusoidal Regression
In the *SinusoidalRegress* you can find a notebook explaining how to build a Sinusoidal Regression model for sinusoidal data. To do so, you take a fourier transform of the sample distribution and some initial educated guesses on the parameters of a sin wave formula such as amplitude and offset. After, you can then convert it into a formula in numpy which will be fit to your data to model your sinusoidal data. 

### Non-Parametric Comparing Differences in Mean and Variance
In *VarAnalysis*, we explore data provided from the lab of the spike response of mice heart cells with control and a [Thapsigargin](https://en.wikipedia.org/wiki/Thapsigargin) groups. Here, we go beyond the question of are the mean and variance *signficantly* different from each other. We ask "Is the difference between these summaary statistics a linear shift or a multiplicative shift?" Since there is no known statistical test for finding this, we find a method to approximate. We use properties of scaling and linear shifts for mean and variance with the support of bootstrapping to solve this problem

### Estimating the Distribution for Small N
Using the data from the previous, *DistributionEstimation* looks at the data from all the repeated trials of the experiments and explores the distribution of each spike's peak value. We observe the density plot for each spike, and ask how is this data distributed. Two immediate problems arise when looking at a histogram: our $n$ for each file is small, anywhere from from 4-15, and the hyperparameter bind width on the histograms has no one size fits all, so we struggle more to visualize the distribution with high confidence. We first approach it by perfomring a Gaussian Kernel Density Estimation on each file. However, due to the second problem stated, this does not provide the clearest answer, so we turn again to non-parametric methods, specifically the Shapiro-Wilk and Kolomgrov-Smirnov tests. 

### Technical
Almost all visuals are made possible by the amazing plotly library. For calculation, we use mainly numpy, pandas, and scipy. 

https://cudmorelab.github.io/
