"""
Compute Cronbach's alpha statistic

* Fork of cronbach_alpha from pingouin
* Avoids some later dependencies (such as newer scipy)
* Credit to pingouin for all the initial code

Features
--------

* Works on pandas.DataFrame objects
* Supports pairwise deletion for missing values
* Computes confidence intervals

Examples
--------

.. code-block:: python

  >>> from cronbach import alpha
  >>> alpha(df)
  (0.9503375120540019, array([0.79 , 0.992]))

License
-------

* Free software: GPL-3.0

Documentation
-------------

* https://cronbach.readthedocs.io/
"""

__author__ = """Brendan Strejcek"""
__email__ = 'brendan@datagazing.com'
__version__ = '0.6.0'

from .cronbach import alpha # noqa F401
