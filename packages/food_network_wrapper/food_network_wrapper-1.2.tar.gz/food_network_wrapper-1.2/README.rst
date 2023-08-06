food\_network\_wrapper
======================

|Build Status| |Coverage Status| |PyPI| |Python Versions|

Search your favorite recipes from `Food
Network <http://foodnetwork.com>`__ and then scrape their contents.

Installation
------------

::

    pip install food_network_wrapper

Usage
-----

import methods

::

    from food_network_wrapper import recipe_search, get_n_recipes, scrape_recipe

Search recipes

::

    rthumbnails = recipe_search("pad thai")

Returns up to 10 ``RThumbnail`` objects in a list

To get more recipes you have to increment the ``page`` parameter

::

    rthumbnails = recipe_search("pad thai", page=2)

Or you can use the shortcut method

::

    rthumbnails = get_n_recipes("pad thai", n=31) 

Scrape a recipe

::

    recipe = scrape_recipe("http://www.foodnetwork.com/recipes/food-network-kitchens/grape-jelly-breakfast-tarts-recipe.html")

Use search and scrape together

::

    rthumbnails = get_n_recipes("pad thai", n=31) 
    recipes = []
    for i in rthumbnails:
       recipe = scrape_recipe(i.url) 
       recipes.append(recipe)

For more examples check out
```demo.py`` <https://github.com/benawad/food_network_wrapper/blob/master/demo.py>`__

.. |Build Status| image:: https://travis-ci.org/benawad/food_network_wrapper.svg?branch=master
   :target: https://travis-ci.org/benawad/food_network_wrapper
.. |Coverage Status| image:: https://coveralls.io/repos/github/benawad/food_network_wrapper/badge.svg?branch=master
   :target: https://coveralls.io/github/benawad/food_network_wrapper?branch=master
.. |PyPI| image:: https://img.shields.io/pypi/v/food_network_wrapper.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/food_network_wrapper
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/Django.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/food_network_wrapper
