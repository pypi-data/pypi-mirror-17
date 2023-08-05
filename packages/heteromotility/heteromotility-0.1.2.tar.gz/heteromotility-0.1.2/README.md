![Heteromotility logo](logo.png)

## Introduction

Heteromotility is a tool for analyzing cell motility in a quantitative manner. Heteromotility takes timelapse imaging data as input and calculates 70+ 'motility features' that can be used to generate a 'motility fingerprint' for a given cell. The tool includes a cell tracking algorithm, but can also be used to analyze cell trajectories derived from another software source. By analyzing more features of cell motility than most common cell tracking methods, Heteromotility may be able to identify novel heterogenous motility phenotypes.

Heteromotility is developed by [Jacob Kimmel](http://jacobkimmel.github.io/) in the [Brack](http://www.bracklab.com/) and [Marshall](http://biochemistry2.ucsf.edu/labs/marshall/) Labs at the [University of California, San Francisco](http://www.ucsf.edu/).

## Installation

Heteromotility can be installed from the Python Package Index with **pip**

    $ pip install heteromotility

or

Simply clone this repository and run **setup.py** in the standard manner.  

    $ git clone https://github.com/jacobkimmel/heteromotility
    $ cd heteromotility
    $ python setup.py install
    $ heteromotility -h
    usage: Calculate motility features from cell locations or cell paths
    [-h] [--seg SEG] [--exttrack EXTTRACK] input_dir output_dir
    ...

Both methods of package installation will add an alias 'heteromotility' to your PATH environment variable

## Motility Features

Feature Name | Notation | Description
-------------|----------|--------------
Total Distance | total_distance | total distance traveled
Net Distance | net_distance | net distance traveled
Minimum Speed | min_speed | minimum overall speed
Maximum Speed | max_speed | maximum speed
Average Speed | avg_speed | average overall speed
Time Spent Moving [1,10] | time_moving | proportion of time in motion, variable time intervals considered [1,10] frames
Average Moving Speed [1,10] | avg_moving_speed | average speed during movement, variable time intervals considered [1,10] frames
Linearity | linearity | Pearson's *r*<sup>2</sup> of regression through all cell positions
Spearman's rho<sup>2</sup> | spearmanrsq | Spearman's rho<sup>2</sup> through all cell positions
Progressivity | progressivity | (net distance traveled / total distance traveled)
Mean Square Displacement Coefficient | msd_alpha | coefficient of log(tau) in a plot of log(tau) vs log(MSD)
Random Walk Linearity Comparison | rw_linearity | (cell path linearity - simulated random walk linearity)
Random Walk Net Distance Comparison | rw_net_distance | (cell path net distance - simulated random walk net distance)
Random Walk Kurtosis Comparison [1,10] | diff_kurtosis | (cell displacement kurtosis - random walk kurtosis) for variable time intervals
Hurst Exponent (Rescaled-Range) | hurst_RS | Hurst exponent estimation using Mandelbrot's rescaled range methods
Autocorrelation [1,10] | autocorr | Autocorrelation of the displacement distribution for variable time lags
Non-Gaussian coefficient | nongauss | Non-Gaussian coefficient (alpha_2) of the displacement distribution
Proportion of Right Turns [time_lag, estimation_interval] | p_turn | proportion of turns an object makes to the left, calculated for multiple time lags and direction estimation intervals
Minimum Turn Magnitude | min_theta | minimum turn angle in radians, for various time lags and direction estimation intervals
Maximum Turn Magnitude | max_theta | maximum turn angle in radians, for various time lags and direction estimation intervals
Average Turn Magnitude | mean_theta | mean turn angle in radians, for various time lags and direction estimation intervals

# Usage

Heteromotility is invoked as a script from your terminal of choice. For the following examples, it is assumed that the alias **heteromotility** has been added to your PATH environment variable, per the pip package installation method above.  
Syntax and command structure if you are invoking the script directly, as in the cloned repository "installation" method above.

The general method to calculate motility statistics is:

*Internal Tracking Algorithm*

    $ heteromotility path_to_input_csvs/ output_path/

*External Tracking Algorithm*

    $ heteromotility . output_path/ --exttrack path/to/object_paths.pickle

Both methods will output a CSV named "motility_statistics.csv" in the specified output directory, formatted with features as columns and samples as rows.

## Demo

As a demonstration, simulated cell paths are provided for multiple models of motion in the **demo/** directory. These paths are saved as Python pickle objects.

To calculate Heteromotility features for the simulated paths, simply run the following. (**Note:** Assumes **heteromotility** is present as an alias, as described above.)

    $ for path in demo/*.pickle; do heteromotility ./ demo/ --exttrack ${path}; done

## Input Data Format

### Internal Tracking Algorithm

If you'd like to use Heteromotility's internal tracking algorithm, provide a set of CSVs with object positions as input.  
For each time point in your series, a single CSV should provide the XY coordinate of each object (i.e. centroid coordianates). All CSV names should include the string 'centroids', have the file extension '.csv', and should be named so that time points are in order when you sort alphanumerically.  

*Example Input Directories*

    input_dir/
      experiment_t01_centroids.csv
      experiment_t02_centroids.csv
      experiment_t03_centroids.csv
      ...

    input_dir/
      t01_thing_centroids.csv
      t02_thing_centroids.csv
      t03_thing_centroids.csv
      ...

    input_dir/
        T01centroids.csv
        T02centroids.csv
        T03centroids.csv

### External Tracking Algorithm

If you'd like to use an external tracking algorithm, Heteromotility accepts a pickled Python dictionary of object paths as an input. The dictionary should be keyed by a unique object identifier (i.e. numbers, names), with each key corresponding to a sequential list of XY-point tuples.

    object_paths = {
                    obj1 : [(x1,y1), (x2,y2), (x3,y3)...],
                    obj2 : [(x1,y1), (x2,y2), (x3,y3)...],
                    ...
                    }

To export this dictionary as a pickle, use the standard Python pickle library.

    > import pickle
    > with file('output_name.pickle', 'wb') as of:
    >   pickle.dump(object_paths, of)

Making this dictionary will require different data massaging for every possible output format from your tracking algorithm of choice, so a general method can't be provided. If the idea of "massaging data" in Python is a little daunting -- please feel free to email me for a bit of help!
