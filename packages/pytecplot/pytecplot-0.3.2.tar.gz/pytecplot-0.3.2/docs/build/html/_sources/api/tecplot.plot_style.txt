Plot Style
==========

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot.plot

Contours
--------

ContourGroup
^^^^^^^^^^^^

.. autoclass:: ContourGroup

    **Attributes**

    .. autosummary::
        :nosignatures:

        color_cutoff
        colormap_filter
        colormap_name
        default_num_levels
        labels
        levels
        lines
        variable
        variable_index

.. autoattribute:: ContourGroup.color_cutoff
.. autoattribute:: ContourGroup.colormap_filter
.. autoattribute:: ContourGroup.colormap_name
.. autoattribute:: ContourGroup.default_num_levels
.. autoattribute:: ContourGroup.labels
.. autoattribute:: ContourGroup.levels
.. autoattribute:: ContourGroup.lines
.. autoattribute:: ContourGroup.variable
.. autoattribute:: ContourGroup.variable_index

ContourColorCutoff
^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColorCutoff

    **Attributes**

    .. autosummary::
        :nosignatures:

        inverted
        max
        min

.. autoattribute:: ContourColorCutoff.min
.. autoattribute:: ContourColorCutoff.max
.. autoattribute:: ContourColorCutoff.inverted

ContourColormapFilter
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapFilter

    **Attributes**

    .. autosummary::
        :nosignatures:

        distribution
        fast_continuous_flood
        num_cycles
        reversed
        show_overrides
        zebra_shade

    **Methods**

    .. autosummary::

        override

.. autoattribute:: ContourColormapFilter.show_overrides
.. autoattribute:: ContourColormapFilter.distribution
.. autoattribute:: ContourColormapFilter.fast_continuous_flood
.. autoattribute:: ContourColormapFilter.num_cycles
.. autoattribute:: ContourColormapFilter.reversed
.. autoattribute:: ContourColormapFilter.zebra_shade
.. automethod:: ContourColormapFilter.override

ContourColormapOverride
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapOverride

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        end_level
        show
        start_level

.. autoattribute:: ContourColormapOverride.show
.. autoattribute:: ContourColormapOverride.color
.. autoattribute:: ContourColormapOverride.start_level
.. autoattribute:: ContourColormapOverride.end_level

ContourColormapZebraShade
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapZebraShade

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        show

.. autoattribute:: ContourColormapZebraShade.show
.. autoattribute:: ContourColormapZebraShade.color

ContourLabels
^^^^^^^^^^^^^

.. autoclass:: ContourLabels

    **Attributes**

    .. autosummary::
        :nosignatures:

        auto_generate
        auto_align
        background_color
        color
        label_by_level
        margin
        show
        spacing
        step

.. autoattribute:: ContourLabels.show
.. autoattribute:: ContourLabels.label_by_level
.. autoattribute:: ContourLabels.auto_generate
.. autoattribute:: ContourLabels.auto_align
.. autoattribute:: ContourLabels.step
.. autoattribute:: ContourLabels.spacing
.. autoattribute:: ContourLabels.margin
.. autoattribute:: ContourLabels.color
.. autoattribute:: ContourLabels.background_color

ContourLevels
^^^^^^^^^^^^^

.. autoclass:: ContourLevels

    **Methods**

    .. autosummary::

        add
        delete_nearest
        delete_range
        reset
        reset_levels
        reset_to_nice

.. automethod:: ContourLevels.reset
.. automethod:: ContourLevels.reset_levels
.. automethod:: ContourLevels.reset_to_nice
.. automethod:: ContourLevels.add
.. automethod:: ContourLevels.delete_nearest
.. automethod:: ContourLevels.delete_range

ContourLines
^^^^^^^^^^^^

.. autoclass:: ContourLines

    **Attributes**

    .. autosummary::
        :nosignatures:

        mode
        pattern_length
        step

.. autoattribute:: ContourLines.mode
.. autoattribute:: ContourLines.step
.. autoattribute:: ContourLines.pattern_length

Streamtraces
------------

Streamtrace
^^^^^^^^^^^

.. autoclass:: Streamtrace
    :members:

StreamtraceRibbon
^^^^^^^^^^^^^^^^^

.. autoclass:: StreamtraceRibbon
    :members:
