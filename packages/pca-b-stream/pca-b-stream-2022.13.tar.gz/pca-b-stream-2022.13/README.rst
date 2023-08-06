..
   Copyright CNRS/Inria/UCA
   Contributor(s): Eric Debreuve (since 2021)

   eric.debreuve@cnrs.fr

   This software is governed by the CeCILL  license under French law and
   abiding by the rules of distribution of free software.  You can  use,
   modify and/ or redistribute the software under the terms of the CeCILL
   license as circulated by CEA, CNRS and INRIA at the following URL
   "http://www.cecill.info".

   As a counterpart to the access to the source code and  rights to copy,
   modify and redistribute granted by the license, users are provided only
   with a limited warranty  and the software's author,  the holder of the
   economic rights,  and the successive licensors  have only  limited
   liability.

   In this respect, the user's attention is drawn to the risks associated
   with loading,  using,  modifying and/or developing or reproducing the
   software by the user in light of its specific status of free software,
   that may mean  that it is complicated to manipulate,  and  that  also
   therefore means  that it is reserved for developers  and  experienced
   professionals having in-depth computer knowledge. Users are therefore
   encouraged to load and test the software's suitability as regards their
   requirements in conditions enabling the security of their systems and/or
   data to be ensured and,  more generally, to use and operate it in the
   same conditions as regards security.

   The fact that you are presently reading this means that you have had
   knowledge of the CeCILL license and that you accept its terms.

.. |PROJECT_NAME|      replace:: PCA-B-Stream
.. |SHORT_DESCRIPTION| replace:: Byte Stream Representation of Piecewise-constant Array

.. |PYPI_NAME_LITERAL| replace:: ``pca-b-stream``
.. |PYPI_PROJECT_URL|  replace:: https://pypi.org/project/pca-b-stream/
.. _PYPI_PROJECT_URL:  https://pypi.org/project/pca-b-stream/



===================================
|PROJECT_NAME|: |SHORT_DESCRIPTION|
===================================



Installation
============

A Web app of |PROJECT_NAME| is available on `PythonAnywhere <https://ericdbv.eu.pythonanywhere.com>`_.

This project is published
on the `Python Package Index (PyPI) <https://pypi.org/>`_
at: |PYPI_PROJECT_URL|_.
It should be installable from Python distribution platforms or Integrated Development Environments (IDEs).
Otherwise, it can be installed from a command console:

- For all users, after acquiring administrative rights:
    - First installation: ``pip install`` |PYPI_NAME_LITERAL|
    - Installation update: ``pip install --upgrade`` |PYPI_NAME_LITERAL|
- For the current user (no administrative rights required):
    - First installation: ``pip install --user`` |PYPI_NAME_LITERAL|
    - Installation update: ``pip install --user --upgrade`` |PYPI_NAME_LITERAL|



Brief Description
=================

In a Few Words
--------------

The ``PCA-B-Stream`` project allows to generate a printable `byte stream <https://docs.python.org/3/library/stdtypes.html#bytes-objects>`_ representation of a piecewise-constant `Numpy array <https://numpy.org/devdocs/reference/generated/numpy.ndarray.html>`_ and to re-create the array from the byte stream, similarly to what is available as part of the `COCO API <https://github.com/cocodataset/cocoapi>`_.



Illustration
------------

In Python:

.. code-block:: python

    >>> import pca_b_stream as pcas
    >>> import numpy as nmpy
    >>> # --- Array creation
    >>> array = nmpy.zeros((10, 10), dtype=nmpy.uint8)
    >>> array[1, 1] = 1
    >>> # --- Array -> Byte stream -> Array
    >>> stream = pcas.PCA2BStream(array)
    >>> decoding = pcas.BStream2PCA(stream)
    >>> # --- Check and print
    >>> assert nmpy.array_equal(decoding, array)
    >>> print(stream)
    b'FnmHoFain+3jtU'

From command line:

.. code-block:: sh

    pca2bstream some_image_file           # Prints the corresponding byte stream
    bstream2pca a_byte_stream a_filename  # Creates an image from the byte stream and stores it



.. _sct_motivations:

Motivations
===========

The motivations for developing an alternative to existing solutions are:

- Arrays can be of any dimension (i.e., not just 2-dimensional)
- Their `dtype <https://numpy.org/devdocs/reference/generated/numpy.dtype.html>`_ can be of boolean, integer, or float
- They can contain more than 2 distinct values (i.e., non-binary arrays) as long as the values are integers (potentially stored in a floating-point format though)
- The byte stream representation is self-contained; In particular, there is no need to keep track of the array shape externally
- The byte stream representation contains everything needed to re-create the array *exactly* as it was instantiated (``dtype``, endianness, C or Fortran ordering); See `note <note_on_exact_>`_ though


.. _note_on_exact:

.. note::
    The statement "re-create the array *exactly* as it was instantiated" is over-confident. First this has not been fully tested by, for example, re-creating an array on a another machine with a native endianness different from the one it was originally instantiated on. Second, more work might be required to ensure that enumeration ordering is correctly dealt with.



Documentation
=============

Functions
---------

The ``pca_b_stream`` module defines the following functions:

- ``PCA2BStream``
    - Generates the byte stream representation of an array; Does not check the array validity (see ``PCAIsValid``)
    - Input: a `Numpy ndarray <https://numpy.org/devdocs/reference/generated/numpy.ndarray.html>`_
    - Output: an object of type `bytes <https://docs.python.org/3/library/stdtypes.html#bytes-objects>`_
- ``BStream2PCA``
    - Re-creates the array from its bytes stream representation; Does not check the stream format validity
    - Input/Output: input and output of ``PCA2BStream`` swapped
- ``PCAIsValid``
    - Checks whether an array is a valid input for stream representation generation; It is meant to be used before calling ``PCA2BStream``
    - Input: a `Numpy ndarray <https://numpy.org/devdocs/reference/generated/numpy.ndarray.html>`_
    - Output: a tuple ``(validity, issue)`` where ``validity`` is a boolean and ``issue`` is None if ``validity`` is True, or a string describing why the array is considered invalid otherwise.
    - Additional information about what are valid piecewise-constant arrays here is provided in the section `"Motivations" <sct_motivations_>`_.
- ``BStreamDetails``
    - Extract details from a byte stream representation; See section `"Byte Stream Format" <byte_stream_format_>`_
    - Inputs:
        - a byte stream generated by ``PCA2BStream``
        - details: a string where each character corresponds to a detail to extract, or "+" to extract all of the available details; Default: "+"; Available details are:
            - m=maximum value in array (also number of sub-streams)
            - c=compression indicators (string of zeros and ones, one per sub-stream)
            - e=endianness
            - t=dtype type code
            - T=dtype name
            - o=enumeration order
            - v=first value (0 for 0 or False, 1 for non-zero or True)
            - d=array dimension
            - l=array lengths per dimension
        - should_print: a boolean to instruct whether the extracted details should be printed to console; Defaults: True
        - should_return: a boolean to instruct whether the extracted details should be returned (see Outputs); Defaults: False
    - Output: either one of:
        - None if should_return is False
        - a dictionary of all of the available details if the ``details`` parameter is "+"
        - a tuple of the requested details in the same order as in the ``details`` parameter



Command Line Scripts
--------------------

The ``PCA-B-Stream`` project defines two command line scripts: ``pca2bstream`` and ``bstream2pca``. The former takes a path to an image file as argument, and prints the corresponding byte stream (without the "b" string type prefix). The latter takes a character string and a filename as arguments, in that order, and creates an image file with this name that corresponds to the string interpreted as a byte stream. The file must not already exist.



.. _byte_stream_format:

Byte Stream Format
------------------

A byte stream is a sequence of `base85-encoded (sub-)streams <https://docs.python.org/3/library/base64.html#base64.b85encode>`_ joined with newlines characters b'\n'.

For a boolean array or an array containing only 0's (zeros) and 1's (ones), there is only one such encoded stream. Once decoded, it has the following format (in lexicographical order; all characters are in ``bytes`` format):

- 0 or 1: indicates whether the remaining of the stream is in uncompressed or `ZLIB compressed <https://docs.python.org/3/library/zlib.html#zlib.compress>`_ format; See `note on compression <note_on_compression_>`_; The remaining of the description applies to the stream in uncompressed format
- 3 characters "{E}{T}{O}":
    - E: endianness among "|", "<" and ">"
    - T: ``dtype`` character code among: "?" + numpy.typecodes["AllInteger"] + numpy.typecodes["Float"]
    - O: enumeration order among "C" (C-ordering) and "F" (Fortran-ordering)
- 0 or 1: whether the first value in the array is zero (or False) or one (or True)
- characters resulting from the `unsingned LEB128 encoding <https://en.wikipedia.org/wiki/LEB128#Unsigned_LEB128>`_ of some integers using the `leb128 project <https://github.com/mohanson/leb128>`_; These integers are:
    - one integer for the dimension of the array (1 for vectors, 2 for matrices, 3 for volumes...)
    - one integer per dimension giving the length of the array in that dimension
    - integers of the `run-length representation <https://en.wikipedia.org/wiki/Run-length_encoding>`_ of the array read in its proper enumeration order

For arrays containing 3 distinct integer values or more (or if the maximum value is higher than 1 regardless of the number of distinct values), there is one encoded stream per value between 1 and the maximum value in the array. The first encoded stream format is identical to the binary case above. The format of the remaining streams is a version of the above format where information already known has been removed: the 3 characters "{E}{T}{O}", the integers of the array dimension, and the length per dimension.


.. _note_on_compression:

.. note::
    For small arrays, compressing the byte stream actually produces a longer stream.



Acknowledgments
===============

The project is developed with `PyCharm Community <https://www.jetbrains.com/pycharm/>`_.

The development relies on several open-source packages
(see ``install_requires`` in ``setup.py``, if present; otherwise ``import`` statements should be searched for).

The code is formatted by `Black <https://github.com/psf/black/>`_, *The Uncompromising Code Formatter*.

The imports are ordered by `isort <https://github.com/timothycrosley/isort/>`_... *your imports, so you don't have to*.
