Coverage Blind Spots
====================

This software lists all positions in given bam files, that have no or only 
very limited coverage and stores the result in a hdf5 file.

Usage
-----

::

    cbs [-h] [--min-cov MIN_COV] files [files ...] output

If multiple files are given, a position is designated a blind spot, if no file
contains a coverage of at least MIN_COV at this position.

Output
------

The output is a hdf5 file with the following structure. For every chromosome a 
group is created, that contains a dataset called `missing_cov`. The dataset 
contains rows of tuples of 32bit integer, representing the first blind spot and
the first position having enough coverage.

Install
-------

This software requires python3, samtools, hdf5, numpy and h5py. All python 
dependencies can be installed by installing cbs via pip::

    pip install git+https://github.com/christofsteel/cbs.git
