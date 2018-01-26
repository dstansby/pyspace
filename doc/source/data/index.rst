.. _heliopy-data:

Data import (:mod:`heliopy.data`)
---------------------------------

.. currentmodule:: heliopy.data

Methods for automatically importing data to python. Each spacecraft has its
own sub-module:

.. toctree::
   :maxdepth: 1

   ace
   artemis
   cassini
   cluster
   helios
   imp
   messenger
   mms
   ulysses
   wind

There is also a module for downloading SPICE kernels:

.. toctree::

   spice

and helper methods that much of the data import uses are also available in the
helper module:

.. toctree::
   :maxdepth: 1

   helper
