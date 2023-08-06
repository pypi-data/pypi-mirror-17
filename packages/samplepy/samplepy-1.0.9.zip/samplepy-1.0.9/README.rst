==============
samplepy 1.0.9
==============

**samplepy** implements three sampling methods for univariate distributions. The package includes:

- Importance sampling: **samplepy.Importance**
- Rejection sampling: **samplepy.Rejection**
- Metropolis-Hastings sampling: **samplepy.MH**

Examples:
=========

.. code:: python

 from samplepy import Rejection
 import matplotlib.pyplot as plt
 import numpy as np

 """
 Rejection sampling example from 2 different functions
 """
 # define a unimodal function to sample under
 f = lambda x: 2.0*np.exp(-2.0*x)
 rej = Rejection(f, [0.01, 3.0])  # instantiate Rejection sampling with f and interval
 sample = rej.sample(10000, 1)    # create a sample of 10K points

 x = np.arange(0.01, 3.0, (3.0-0.01)/10000)
 fx = f(x)

 figure, axis = plt.subplots()
 axis.hist(sample, normed=1, bins=40)
 axis2 = axis.twinx()
 axis2.plot(x, fx, 'g', label="f(x)=2.0*exp(-2*x)")
 plt.legend(loc=1)
 plt.show()

More examples and package documentation can be found at <https://github.com/elena-sharova/samplepy/blob/master/README.rst>

Installation
===============

::

    pip install samplepy
