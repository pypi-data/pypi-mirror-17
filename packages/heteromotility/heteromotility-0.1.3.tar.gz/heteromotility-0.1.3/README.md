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

Both methods of package installation will add an alias 'heteromotility' to your PATH environment variable.

As with all research software, we recommend installing Heteromotility inside of a virtual environment.

    $ virtualenv heteromotility_env/
    $ source heteromotility_env/bin/activate
    $ pip install heteromotility

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

Heteromotility is invoked as a script from your terminal of choice. For the following examples, it is assumed that the alias **heteromotility** has been added to your PATH environment variable, per the installation methods above.  
Commands will differ slightly if you are invoking the script directly. i.e.) **heteromotility** will be **/path/to/heteromotility.py**.

The general method to calculate motility statistics is:

*Internal Tracking Algorithm*

    $ heteromotility path_to_input_csvs/ output_path/

*External Tracking Algorithm*

    $ heteromotility . output_path/ --exttrack path/to/object_paths.pickle

Both methods will output a CSV named "motility_statistics.csv" in the specified output directory, formatted with features as columns and samples as rows.  
The optional argument **--output_suffix** can be used to add a suffix to the output csv.

    $ heteromotility path_to_input_csvs/ ./
    $ ls
    motility_statistics.csv
    $ heteromotility path_to_input_csvs/ ./ --output_suffix TEST_SUFFIX
    $ ls
    motility_statistics.csv motility_statistics_TEST_SUFFIX.csv

## Demo

As a demonstration, simulated cell paths are provided for multiple models of motion in the **demo/** directory. These paths are saved as Python pickle objects.

To calculate Heteromotility features for a simulated path, simply run the following. (**Note:** Assumes **heteromotility** is present as an alias, as described above.)

    $ heteromotility ./ demo/sim_XYZ/ --exttrack demo/sim_XYZ/sim_XYZ.pickle

## Split Motility Path Calculation

Heteromotility supports splitting an object's path into multiple subpaths and calculating features for each subpath. This is useful to investigate changes in an object's motility over time. This feature is triggered with the **--detailedbalance** command line flag, followed by an integer specifying the minimum number of path steps to consider. Heteromotility will calculate features for every subpath of the minimum length, and every possible length up to 1/2 the total length of the supplied path.  
**Note:** Subpaths have a minimum length of 18 steps, as multiple Heteromotility features rely upon regression analyses that are confounded by exceedingly small path lengths.

This feature is executed like so:

    $ heteromotility /path/to/csvs /output/path/ --detailedbalance 20

where the integer 20 can be replaced by your desired minimum path length.

The resulting output files will be named 'motility_statistics_split_LENGTH.csv' where LENGTH is the subpath size for those features. Importantly, the 'cell_ids' column will now contain additional information. In addition to the unique cell identifier, 'cell_ids' will contain a dash following the identifier with subpath number, indexed beginning at 0. The format appears:

    cell_ids ...
    ObjectIdentifier-SubpathNumber ...
    ...

For instance, for a path with total length N = 80, minimum length tau = 20, the 'cell_ids' column would appear as follows:

    cell_ids ...
    obj0-0 ...
    obj0-1 ...
    obj0-2 ...
    obj0-3 ...
    obj1-1 ...
    obj1-2 ...
    ...

Where 'obj0-0' is the first subpath (length = 20) of 'obj0', 'obj0-1' is the second subpath of 'obj0', and so forth.

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
