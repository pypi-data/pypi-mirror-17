.. |Build Status| image:: https://travis-ci.org/IndianEngineeringDesignForum/geomi.svg?branch=master
   :target: https://travis-ci.org/IndianEngineeringDesignForum/geomi
.. |Coverage Status| image:: https://codecov.io/github/IndianEngineeringDesignForum/geomi/branch/master/graph/badge.svg
   :target: https://codecov.io/github/IndianEngineeringDesignForum/geomi
.. |Version Status| image:: https://badge.fury.io/py/geomi.svg
   :target: http://badge.fury.io/py/geomi


Geomi
=====

|Build Status| |Coverage Status| |Version Status| 

Planar, solid and higher dimensional geometry.

LICENSE
-------

MIT. See `License File <https://github.com/IndianEngineeringDesignForum/geomi/blob/master/LICENSE>`__.

Install
-------

``geomi`` is on the Python Package Index (PyPI):

::

    pip install geomi

or

::

    easy_install geomi

Structure
---------

``geomi`` is implemented in these parts:

|literal planar|_: points, lines, curves, shapes, polygons ...

|literal solid|_: 3D geometry including cubes, cones, spheres, Platonic solids ...

|literal ndim|_: higher dimensional geometries ...

|literal utils.algos|_: algorithms that can applied on geometric entities ...

|literal utils.plotter|_: plot geometries for visualization ...

.. |literal planar| replace:: ``planar``
.. _literal planar: https://github.com/IndianEngineeringDesignForum/geomi/tree/master/src/geomi/planar

.. |literal solid| replace:: ``solid``
.. _literal solid: https://github.com/IndianEngineeringDesignForum/geomi/tree/master/src/geomi/solid

.. |literal ndim| replace:: ``ndim``
.. _literal ndim: https://github.com/IndianEngineeringDesignForum/geomi/tree/master/src/geomi/ndim

.. |literal utils.algos| replace:: ``utils.algos``
.. _literal utils.algos: https://github.com/IndianEngineeringDesignForum/geomi/tree/master/src/geomi/utils/algos

.. |literal utils.plotter| replace:: ``utils.plotter``
.. _literal utils.plotter: https://github.com/IndianEngineeringDesignForum/geomi/tree/master/src/geomi/utils/plotter


Dependencies
------------

``geomi`` supports Python 2.7+ and Python 3.5+ with a common codebase.
It is pure Python and requires no dependencies beyond the standard
library.



