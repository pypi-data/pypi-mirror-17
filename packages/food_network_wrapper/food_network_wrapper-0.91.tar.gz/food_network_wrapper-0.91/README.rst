food\_network\_wrapper
======================

|Build Status| |Coverage Status| |PyPI version| |PyPI|

Search your favorite recipes from `Food
Network <http://foodnetwork.com>`__ and then scrape the recipes
contents.

Installation
------------

::

    pip install food_network_wrapper

Usage
-----

Search recipes

::

    rthumbnails = recipe_search("pad thai")

Returns up to 10 ``RThumbnail`` objects in a list

To get more recipes you have to increment the ``page`` parameter

::

    rthumbnails = recipe_search("pad thai", page=2)

.. |Build Status| image:: https://travis-ci.org/benawad/food_network_wrapper.svg?branch=master
   :target: https://travis-ci.org/benawad/food_network_wrapper
.. |Coverage Status| image:: https://coveralls.io/repos/github/benawad/food_network_wrapper/badge.svg?branch=master
   :target: https://coveralls.io/github/benawad/food_network_wrapper?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/food_network_wrapper.svg
   :target: https://badge.fury.io/py/food_network_wrapper
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/Django.svg?maxAge=2592000
   :target: https://badge.fury.io/py/food_network_wrapper
