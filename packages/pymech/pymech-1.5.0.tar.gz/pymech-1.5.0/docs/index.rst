.. _documentation-index:

pymech documentation
====================

This is the documentation for pymech_, a Python suite of routines for Nek5000_ and SIMSON_.


+--------------+------------------------------------------------------+
| Authors      |  |author| (:ref:`see here <thanks.md#credits>`)      |
+--------------+------------------------------------------------------+
| Version      |  |version|                                           |
+--------------+------------------------------------------------------+

Pymech can be used for reading, editing and writing Nek5000_ and SIMSON_ meshes
and output files. For a detailed tutorial refer to :ref:`usage
<Usage.myst.md#usage>`.

The data structure is defined by the :py:class:`pymech.core.HexaData` class.
The functions for manipulating Nek5000_ files are in :ref:`neksuite`, while the
functions for SIMSON_ are, of course, in :ref:`simsonsuite`.

.. _installation:

Installation
------------

Pymech requires Python version |py_min_version| and above. For most purposes, we recommend
creating a `virtual environment`_ and then running::

   pip install pymech

Optional dependencies can be installed as follows::

   pip install "pymech[full]"

.. note::

   Specifying ``[full]`` would also install optional dependencies, namely:

   .. literalinclude:: ../setup.cfg
      :start-at: full =
      :end-before: docs =

.. _virtual environment: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments

Install using conda / mamba
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In certain cases, typically:

- in an OS where at least Python version |py_min_version| is unavailable, or
- to install ``mayavi`` to make use of :mod:`pymech.vtksuite`, or
- to use PyPy_ instead of CPython,

a simple ``pip install pymech`` may not cut it.  Then, it is recommended to use conda_ (or
mamba_) to set up the Python environment first. To install Pymech with a Python
interpreter of your choice:

.. tab:: PyPy

   ::

      conda create -n my-env -c conda-forge pypy pip xarray
      conda activate my-env
      pypy -m pip install pymech

.. tab:: CPython

   ::

      conda create -n my-env -c conda-forge python pip
      conda activate my-env
      python -m pip install pymech

.. _PyPy: https://www.pypy.org/
.. _conda: https://docs.conda.io/projects/conda/en/latest/user-guide/index.html
.. _mamba: https://mamba.readthedocs.io/en/latest/installation.html

----------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   core.rst
   neksuite.rst
   simsonsuite.rst
   vtksuite.rst
   dataset.rst
   meshtools.rst
   usage.myst.md

.. toctree::
   :maxdepth: 1
   :caption: Reference

   deprecations.rst
   dev.md
   asv_bench/README.md
   changelog.md
   contributing.md
   thanks.md
   Source code on GitHub <https://github.com/eX-Mech/pymech>

.. Indices and tables

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


.. External links:

.. _pymech: https://github.com/eX-Mech/pymech
.. _SIMSON: https://github.com/KTH-Nek5000/SIMSON
.. _Nek5000: https://nek5000.mcs.anl.gov/
