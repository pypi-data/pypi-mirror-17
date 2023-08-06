Session and Top-Level Functionality
===================================

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot

|Tecplot Engine|
----------------

    .. autosummary::
        .. Don't include :nosignatures: so that stop, acquire, and release will display as functions.

        tecplot.session.stop
        tecplot.session.acquire_license
        tecplot.session.release_license

Session
-------

.. automodule:: tecplot.session

    .. autosummary::
        .. See note for Tecplot Engine above.

        tecplot_install_directory
        tecplot_examples_directory

.. autofunction:: tecplot.session.tecplot_install_directory
.. autofunction:: tecplot.session.stop
.. autofunction:: tecplot.session.acquire_license
.. autofunction:: tecplot.session.release_license


    This directory is generally platform-dependent and will contain
    configuration files and the examples directory:

    .. code-block:: python
        :emphasize-lines: 4

        >>> import os
        >>> import tecplot

        >>> installdir = tecplot.session.tecplot_install_directory()
        >>> infile = os.path.join(installdir,'examples','3D','spaceship.lpk')
        >>> outfile = 'spaceship.png'
        >>> tecplot.load_layout(infile)
        >>> tecplot.export_image(outfile)

    .. figure:: /_static/images/spaceship.png
        :width: 300px
        :figwidth: 300px

.. autofunction:: tecplot.session.tecplot_examples_directory

    This directory is generally platform-dependent and by default contains
    the various examples shipped with |Tecplot 360 EX|:

    .. code-block:: python
        :emphasize-lines: 4

        >>> import os
        >>> import tecplot

        >>> exdir = tecplot.session.tecplot_examples_directory()
        >>> infile = os.path.join(exdir,'3D','JetSurface.lay')
        >>> outfile = 'jet_surface.png'
        >>> tecplot.load_layout(infile)
        >>> tecplot.export_image(outfile)

    .. figure:: /_static/images/jet_surface.png
        :width: 300px
        :figwidth: 300px

Miscellaneous
-------------

.. autoclass:: tecplot.tecutil.Index
.. autoclass:: tecplot.tecutil.IndexRange
.. autofunction:: tecplot.export_image
