PyTecplot
=========

.. warning::
    Please keep in mind that |PyTecplot| is still in a pre-release "alpha"
    state. It should be considered a "work-in-progress" library and is
    subject to dramatic changes. That being said, if you find anything
    particularly helpful or annoying, we would greatly appreciate your
    `feedback <support@tecplot.com>`_.

The pytecplot library is a high level API that connects your Python script
to the power of the |Tecplot 360 EX| visualization engine. It offers line
plotting, 2D and 3D surface plots in a variety of formats, and 3D volumetric
visualization. Familiarity with |Tecplot 360 EX| and the |Tecplot 360 EX|
macro language is helpful, but not required.

.. note::
    |PyTecplot| supports 64-bit Python versions 2.7 and 3.4+. |PyTecplot|
    does not support 32 bit Python. Please refer to INSTALL.rst for
    installation instructions and environment setup. For the best
    experience, developers are encouraged to use the **latest version of
    Python**.

Quick Start
-----------

Please refer to the INSTALL.rst file for installation instructions and
environment setup. The short of it is something like this::

    pip install pytecplot

Linux and OSX users will have to set ``LD_LIBRARY_PATH`` or
``DYLD_LIBRARY_PATH`` to the directory containing the |Tecplot 360 EX|
executable. For OSX, this will be something like::

    /Applications/Tecplot 360 EX/Tecplot 360 EX.app/Contents/MacOS

Getting Help and Finding Documentation
--------------------------------------

Examples can be found in the ``examples`` directory and the primary
documentation (in HTML format) can found under the ``docs`` directory::

    docs/builds/html/index.html

It is generated directly from the source code under ``pytecplot/tecplot``.
In addition, all imported objects and methods that are part of the public
API have doc strings which can be accessed with python's native ``help()``
function.
