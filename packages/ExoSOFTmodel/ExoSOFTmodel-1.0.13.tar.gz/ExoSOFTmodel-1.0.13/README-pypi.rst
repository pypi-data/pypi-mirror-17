ExoSOFTmodel
============

An astronomical model for calculating the predicted astrometry and radial velocity due to a companion.

Examples are provided, including ones showing how to use ExoSOFTmodel with the popular emcee, and another for very simple initial testing.


Installation Notes
==================

The easiest way to install it is:
 
 $pip install ExoSOFTmodel
 
Re-compiling Cython tools
-------------------------

Should you need to modify any of the tools within '(cytools.pyx)<https://github.com/kylemede/ExoSOFTmodel/blob/master/ExoSOFTmodel/cytools.pyx>'_
 you need to have cython installed.  Then compile the code within its directory using:
 
 $python setup.py build_ext --inplace

License
-------

Copyright 2016 Kyle Mede and contributors.

ExoSOFTmodel is free software made available under the GNU GPLv3 license. 
For details see the license.txt file.