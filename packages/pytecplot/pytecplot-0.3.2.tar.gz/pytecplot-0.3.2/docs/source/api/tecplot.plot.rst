.. _plot:

Plotting Style Manipulation
===========================

For axes and axis style and manipulations, see `Axes Settings <tecplot.axes>`.

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot.plot

Scatter Plots
-------------

.. autoclass:: Scatter

    **Attributes**

    .. autosummary::
        :nosignatures:

        variable
        variable_index

.. autoattribute:: Scatter.variable
.. autoattribute:: Scatter.variable_index

Vector Plots
------------

.. autoclass:: Vector2D
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: Vector3D
    :members:
    :inherited-members:
    :member-order: bysource

Field Plots
-----------

..  contents::
    :local:
    :depth: 2

Cartesian2DFieldPlot
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Cartesian2DFieldPlot

    **Attributes**

    .. autosummary::
        :nosignatures:

        active_fieldmaps
        active_fieldmap_indices
        axes
        draw_order
        fieldmaps
        num_fieldmaps
        scatter
        show_contour
        show_edge
        show_lighting_effect
        show_mesh
        show_scatter
        show_shade
        show_streamtraces
        show_translucency
        show_vector
        vector
        view

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        contour
        fieldmap
        fieldmap_index

.. automethod:: Cartesian2DFieldPlot.activate
.. autoattribute:: Cartesian2DFieldPlot.num_fieldmaps
.. automethod:: Cartesian2DFieldPlot.fieldmap
.. automethod:: Cartesian2DFieldPlot.fieldmap_index
.. autoattribute:: Cartesian2DFieldPlot.fieldmaps
.. autoattribute:: Cartesian2DFieldPlot.active_fieldmaps
.. autoattribute:: Cartesian2DFieldPlot.active_fieldmap_indices
.. autoattribute:: Cartesian2DFieldPlot.draw_order
.. autoattribute:: Cartesian2DFieldPlot.show_contour
.. autoattribute:: Cartesian2DFieldPlot.show_edge
.. autoattribute:: Cartesian2DFieldPlot.show_lighting_effect
.. autoattribute:: Cartesian2DFieldPlot.show_mesh
.. autoattribute:: Cartesian2DFieldPlot.show_scatter
.. autoattribute:: Cartesian2DFieldPlot.show_shade
.. autoattribute:: Cartesian2DFieldPlot.show_streamtraces
.. autoattribute:: Cartesian2DFieldPlot.show_translucency
.. autoattribute:: Cartesian2DFieldPlot.show_vector
.. autoattribute:: Cartesian2DFieldPlot.axes
.. automethod:: Cartesian2DFieldPlot.contour
.. autoattribute:: Cartesian2DFieldPlot.scatter
.. autoattribute:: Cartesian2DFieldPlot.vector
.. autoattribute:: Cartesian2DFieldPlot.view

Cartesian3DFieldPlot
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Cartesian3DFieldPlot

    **Attributes**

    .. autosummary::
        :nosignatures:

        active_fieldmaps
        active_fieldmap_indices
        axes
        fieldmaps
        num_fieldmaps
        scatter
        show_contour
        show_edge
        show_lighting_effect
        show_mesh
        show_scatter
        show_shade
        show_streamtraces
        show_translucency
        show_vector
        vector
        view

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        contour
        fieldmap
        fieldmap_index

.. automethod:: Cartesian3DFieldPlot.activate
.. autoattribute:: Cartesian3DFieldPlot.num_fieldmaps
.. automethod:: Cartesian3DFieldPlot.fieldmap
.. automethod:: Cartesian3DFieldPlot.fieldmap_index
.. autoattribute:: Cartesian3DFieldPlot.fieldmaps
.. autoattribute:: Cartesian3DFieldPlot.active_fieldmaps
.. autoattribute:: Cartesian3DFieldPlot.active_fieldmap_indices
.. autoattribute:: Cartesian3DFieldPlot.show_contour
.. autoattribute:: Cartesian3DFieldPlot.show_edge
.. autoattribute:: Cartesian3DFieldPlot.show_lighting_effect
.. autoattribute:: Cartesian3DFieldPlot.show_mesh
.. autoattribute:: Cartesian3DFieldPlot.show_scatter
.. autoattribute:: Cartesian3DFieldPlot.show_shade
.. autoattribute:: Cartesian3DFieldPlot.show_streamtraces
.. autoattribute:: Cartesian3DFieldPlot.show_translucency
.. autoattribute:: Cartesian3DFieldPlot.show_vector
.. autoattribute:: Cartesian3DFieldPlot.axes
.. automethod:: Cartesian3DFieldPlot.contour
.. autoattribute:: Cartesian3DFieldPlot.scatter
.. autoattribute:: Cartesian3DFieldPlot.vector
.. autoattribute:: Cartesian3DFieldPlot.view

.. _fieldmap:

Fieldmaps
---------

..  contents::
    :local:
    :depth: 2

Cartesian2DFieldmap
^^^^^^^^^^^^^^^^^^^

.. autoclass:: Cartesian2DFieldmap

    **Attributes**

    .. autosummary::
        :nosignatures:

        contour
        edge
        effects
        group
        mesh
        points
        scatter
        shade
        show
        show_iso_surfaces
        show_slices
        show_streamtraces
        surfaces
        vector
        zones

.. autoattribute:: Cartesian2DFieldmap.group
.. autoattribute:: Cartesian2DFieldmap.zones
.. autoattribute:: Cartesian2DFieldmap.show
.. autoattribute:: Cartesian2DFieldmap.points
.. autoattribute:: Cartesian2DFieldmap.surfaces
.. autoattribute:: Cartesian2DFieldmap.contour
.. autoattribute:: Cartesian2DFieldmap.edge
.. autoattribute:: Cartesian2DFieldmap.effects
.. autoattribute:: Cartesian2DFieldmap.mesh
.. autoattribute:: Cartesian2DFieldmap.scatter
.. autoattribute:: Cartesian2DFieldmap.shade
.. autoattribute:: Cartesian2DFieldmap.vector
.. autoattribute:: Cartesian2DFieldmap.show_iso_surfaces
.. autoattribute:: Cartesian2DFieldmap.show_slices
.. autoattribute:: Cartesian2DFieldmap.show_streamtraces

Cartesian3DFieldmap
^^^^^^^^^^^^^^^^^^^

.. autoclass:: Cartesian3DFieldmap

    **Attributes**

    .. autosummary::
        :nosignatures:

        contour
        edge
        effects
        group
        mesh
        points
        scatter
        shade
        show
        show_iso_surfaces
        show_slices
        show_streamtraces
        surfaces
        vector
        zones

.. autoattribute:: Cartesian3DFieldmap.group
.. autoattribute:: Cartesian3DFieldmap.zones
.. autoattribute:: Cartesian3DFieldmap.show
.. autoattribute:: Cartesian3DFieldmap.points
.. autoattribute:: Cartesian3DFieldmap.surfaces
.. autoattribute:: Cartesian3DFieldmap.contour
.. autoattribute:: Cartesian3DFieldmap.edge
.. autoattribute:: Cartesian3DFieldmap.effects
.. autoattribute:: Cartesian3DFieldmap.mesh
.. autoattribute:: Cartesian3DFieldmap.scatter
.. autoattribute:: Cartesian3DFieldmap.shade
.. autoattribute:: Cartesian3DFieldmap.vector
.. autoattribute:: Cartesian3DFieldmap.show_iso_surfaces
.. autoattribute:: Cartesian3DFieldmap.show_slices
.. autoattribute:: Cartesian3DFieldmap.show_streamtraces

FieldmapContour
^^^^^^^^^^^^^^^

.. autoclass:: FieldmapContour

    **Attributes**

    .. autosummary::
        :nosignatures:

        contour_type
        flood_group
        flood_group_index
        lighting_effect
        line_color
        line_group
        line_group_index
        line_pattern
        line_thickness
        pattern_length
        show

.. autoattribute:: FieldmapContour.show
.. autoattribute:: FieldmapContour.contour_type
.. autoattribute:: FieldmapContour.flood_group
.. autoattribute:: FieldmapContour.flood_group_index
.. autoattribute:: FieldmapContour.line_group
.. autoattribute:: FieldmapContour.line_group_index
.. autoattribute:: FieldmapContour.line_color
.. autoattribute:: FieldmapContour.line_thickness
.. autoattribute:: FieldmapContour.line_pattern
.. autoattribute:: FieldmapContour.pattern_length
.. autoattribute:: FieldmapContour.lighting_effect

FieldmapEdge
^^^^^^^^^^^^

.. autoclass:: FieldmapEdge

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        edge_type
        i_border
        j_border
        k_border
        line_thickness
        show

.. autoattribute:: FieldmapEdge.show
.. autoattribute:: FieldmapEdge.edge_type
.. autoattribute:: FieldmapEdge.i_border
.. autoattribute:: FieldmapEdge.j_border
.. autoattribute:: FieldmapEdge.k_border
.. autoattribute:: FieldmapEdge.color
.. autoattribute:: FieldmapEdge.line_thickness

FieldmapEffects
^^^^^^^^^^^^^^^

.. autoclass:: FieldmapEffects

    **Attributes**

    .. autosummary::
        :nosignatures:

        clip_planes
        value_blanking

.. autoattribute:: FieldmapEffects.value_blanking
.. autoattribute:: FieldmapEffects.clip_planes

.. autoclass:: FieldmapEffects3D

    **Attributes**

    .. autosummary::
        :nosignatures:

        clip_planes
        lighting_effect
        surface_translucency
        value_blanking

.. autoattribute:: FieldmapEffects3D.lighting_effect
.. autoattribute:: FieldmapEffects3D.surface_translucency
.. autoattribute:: FieldmapEffects3D.value_blanking
.. autoattribute:: FieldmapEffects3D.clip_planes

FieldmapMesh
^^^^^^^^^^^^

.. autoclass:: FieldmapMesh

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        line_thickness
        line_pattern
        mesh_type
        pattern_length
        show

.. autoattribute:: FieldmapMesh.show
.. autoattribute:: FieldmapMesh.mesh_type
.. autoattribute:: FieldmapMesh.color
.. autoattribute:: FieldmapMesh.line_thickness
.. autoattribute:: FieldmapMesh.line_pattern
.. autoattribute:: FieldmapMesh.pattern_length

FieldmapPoints
^^^^^^^^^^^^^^

.. autoclass:: FieldmapPoints

    **Attributes**

    .. autosummary::
        :nosignatures:

        points_to_plot
        step

.. autoattribute:: FieldmapPoints.points_to_plot
.. autoattribute:: FieldmapPoints.step

FieldmapScatter
^^^^^^^^^^^^^^^

.. autoclass:: FieldmapScatter

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        fill_color
        line_thickness
        show
        size
        size_by_variable
        symbol_type

    **Methods**

    .. autosummary::
        :nosignatures:

        symbol

.. autoattribute:: FieldmapScatter.show
.. autoattribute:: FieldmapScatter.symbol_type
.. automethod:: FieldmapScatter.symbol
.. autoattribute:: FieldmapScatter.color
.. autoattribute:: FieldmapScatter.fill_color
.. autoattribute:: FieldmapScatter.size
.. autoattribute:: FieldmapScatter.size_by_variable
.. autoattribute:: FieldmapScatter.line_thickness

.. autoclass:: GeometryScatterSymbol

    **Attributes**

    .. autosummary::
        :nosignatures:

        shape

.. autoattribute:: GeometryScatterSymbol.shape

.. autoclass:: TextScatterSymbol

    **Attributes**

    .. autosummary::
        :nosignatures:

        text
        typeface

.. autoattribute:: TextScatterSymbol.text
.. autoattribute:: TextScatterSymbol.typeface

FieldmapShade
^^^^^^^^^^^^^

.. autoclass:: FieldmapShade

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        show

.. autoattribute:: FieldmapShade.show
.. autoattribute:: FieldmapShade.color

.. autoclass:: FieldmapShade3D

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        lighting_effect
        show

.. autoattribute:: FieldmapShade3D.show
.. autoattribute:: FieldmapShade3D.color
.. autoattribute:: FieldmapShade3D.lighting_effect

FieldmapSurfaces
^^^^^^^^^^^^^^^^

.. autoclass:: FieldmapSurfaces

    **Attributes**

    .. autosummary::
        :nosignatures:

        i_range
        j_range
        k_range
        surfaces_to_plot

.. autoattribute:: FieldmapSurfaces.surfaces_to_plot
.. autoattribute:: FieldmapSurfaces.i_range
.. autoattribute:: FieldmapSurfaces.j_range
.. autoattribute:: FieldmapSurfaces.k_range

FieldmapVector
^^^^^^^^^^^^^^

.. autoclass:: FieldmapVector

    **Attributes**

    .. autosummary::
        :nosignatures:

        arrowhead_style
        color
        line_pattern
        line_thickness
        pattern_length
        show
        tangent_only
        vector_type

.. autoattribute:: FieldmapVector.show
.. autoattribute:: FieldmapVector.vector_type
.. autoattribute:: FieldmapVector.tangent_only
.. autoattribute:: FieldmapVector.color
.. autoattribute:: FieldmapVector.arrowhead_style
.. autoattribute:: FieldmapVector.line_thickness
.. autoattribute:: FieldmapVector.line_pattern
.. autoattribute:: FieldmapVector.pattern_length

Line Plots
----------

..  contents::
    :local:
    :depth: 2

PolarLinePlot
^^^^^^^^^^^^^

.. autoclass:: PolarLinePlot

    **Attributes**

    .. autosummary::
        :nosignatures:

        active_linemaps
        active_linemap_indices
        axes
        legend
        linemaps
        num_linemaps
        show_lines
        show_symbols
        view

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        add_linemap
        delete_linemaps
        linemap

.. automethod:: PolarLinePlot.activate
.. autoattribute:: PolarLinePlot.num_linemaps
.. automethod:: PolarLinePlot.linemap
.. autoattribute:: PolarLinePlot.linemaps
.. autoattribute:: PolarLinePlot.active_linemaps
.. autoattribute:: PolarLinePlot.active_linemap_indices
.. automethod:: PolarLinePlot.add_linemap
.. automethod:: PolarLinePlot.delete_linemaps
.. autoattribute:: PolarLinePlot.show_lines
.. autoattribute:: PolarLinePlot.show_symbols
.. autoattribute:: PolarLinePlot.axes
.. autoattribute:: PolarLinePlot.legend
.. autoattribute:: PolarLinePlot.view

XYLinePlot
^^^^^^^^^^

.. autoclass:: XYLinePlot

    **Attributes**

    .. autosummary::
        :nosignatures:

        active_linemaps
        active_linemap_indices
        axes
        legend
        linemaps
        num_linemaps
        show_bars
        show_error_bars
        show_lines
        show_symbols
        view

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        add_linemap
        delete_linemaps
        linemap

.. automethod:: XYLinePlot.activate
.. autoattribute:: XYLinePlot.num_linemaps
.. automethod:: XYLinePlot.linemap
.. autoattribute:: XYLinePlot.linemaps
.. autoattribute:: XYLinePlot.active_linemaps
.. autoattribute:: XYLinePlot.active_linemap_indices
.. automethod:: XYLinePlot.add_linemap
.. automethod:: XYLinePlot.delete_linemaps
.. autoattribute:: XYLinePlot.show_bars
.. autoattribute:: XYLinePlot.show_error_bars
.. autoattribute:: XYLinePlot.show_lines
.. autoattribute:: XYLinePlot.show_symbols
.. autoattribute:: XYLinePlot.axes
.. autoattribute:: XYLinePlot.legend
.. autoattribute:: XYLinePlot.view

.. _linemap:

Linemaps
--------

..  contents::
    :local:
    :depth: 2

PolarLinemap
^^^^^^^^^^^^

.. autoclass:: PolarLinemap
    :members:
    :inherited-members:
    :member-order: bysource

XYLinemap
^^^^^^^^^

.. autoclass:: XYLinemap

    **Attributes**

    .. autosummary::
        :nosignatures:

        bars
        curve
        error_bars
        function_dependency
        index
        indices
        line
        name
        show
        sort_by
        symbols
        x_axis
        x_axis_index
        x_variable
        x_variable_index
        y_axis
        y_axis_index
        y_variable
        y_variable_index
        zone

.. autoattribute:: XYLinemap.index
.. autoattribute:: XYLinemap.name
.. autoattribute:: XYLinemap.show
.. autoattribute:: XYLinemap.zone
.. autoattribute:: XYLinemap.sort_by
.. autoattribute:: XYLinemap.curve
.. autoattribute:: XYLinemap.indices
.. autoattribute:: XYLinemap.line
.. autoattribute:: XYLinemap.symbols
.. autoattribute:: XYLinemap.bars
.. autoattribute:: XYLinemap.error_bars
.. autoattribute:: XYLinemap.function_dependency
.. autoattribute:: XYLinemap.x_axis
.. autoattribute:: XYLinemap.x_axis_index
.. autoattribute:: XYLinemap.x_variable
.. autoattribute:: XYLinemap.x_variable_index
.. autoattribute:: XYLinemap.y_axis
.. autoattribute:: XYLinemap.y_axis_index
.. autoattribute:: XYLinemap.y_variable
.. autoattribute:: XYLinemap.y_variable_index

LinemapLine
^^^^^^^^^^^

.. autoclass:: LinemapLine

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        line_pattern
        line_thickness
        pattern_length
        show

.. autoattribute:: LinemapLine.show
.. autoattribute:: LinemapLine.color
.. autoattribute:: LinemapLine.line_thickness
.. autoattribute:: LinemapLine.line_pattern
.. autoattribute:: LinemapLine.pattern_length

LinemapCurve
^^^^^^^^^^^^

.. autoclass:: LinemapCurve

    **Attributes**

    .. autosummary::
        :nosignatures:

        curve_type
        fit_range
        num_points
        polynomial_order
        spline_derivative_at_ends
        weight_variable
        weight_variable_index

.. autoattribute:: LinemapCurve.curve_type
.. autoattribute:: LinemapCurve.fit_range
.. autoattribute:: LinemapCurve.num_points
.. autoattribute:: LinemapCurve.polynomial_order
.. autoattribute:: LinemapCurve.spline_derivative_at_ends
.. autoattribute:: LinemapCurve.weight_variable
.. autoattribute:: LinemapCurve.weight_variable_index

LinemapBars
^^^^^^^^^^^

.. autoclass:: LinemapBars

    **Attributes**

    .. autosummary::
        :nosignatures:

        fill_color
        line_color
        line_thickness
        show
        size

.. autoattribute:: LinemapBars.show
.. autoattribute:: LinemapBars.size
.. autoattribute:: LinemapBars.fill_color
.. autoattribute:: LinemapBars.line_color
.. autoattribute:: LinemapBars.line_thickness

LinemapErrorBars
^^^^^^^^^^^^^^^^

.. autoclass:: LinemapErrorBars

    **Attributes**

    .. autosummary::
        :nosignatures:

        bar_type
        color
        endcap_size
        line_thickness
        show
        step
        step_mode
        variable
        variable_index

.. autoattribute:: LinemapErrorBars.show
.. autoattribute:: LinemapErrorBars.bar_type
.. autoattribute:: LinemapErrorBars.variable
.. autoattribute:: LinemapErrorBars.variable_index
.. autoattribute:: LinemapErrorBars.color
.. autoattribute:: LinemapErrorBars.line_thickness
.. autoattribute:: LinemapErrorBars.endcap_size
.. autoattribute:: LinemapErrorBars.step
.. autoattribute:: LinemapErrorBars.step_mode

LinemapIndices
^^^^^^^^^^^^^^

.. autoclass:: LinemapIndices

    **Attributes**

    .. autosummary::
        :nosignatures:

        i_range
        j_range
        k_range
        varying_index

.. autoattribute:: LinemapIndices.varying_index
.. autoattribute:: LinemapIndices.i_range
.. autoattribute:: LinemapIndices.j_range
.. autoattribute:: LinemapIndices.k_range

LinemapSymbols
^^^^^^^^^^^^^^

.. autoclass:: LinemapSymbols

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        fill_color
        line_thickness
        show
        size
        step
        step_mode
        symbol_type

    **Methods**

    .. autosummary::
        :nosignatures:

        symbol

.. autoattribute:: LinemapSymbols.show
.. autoattribute:: LinemapSymbols.symbol_type
.. automethod:: LinemapSymbols.symbol
.. autoattribute:: LinemapSymbols.step
.. autoattribute:: LinemapSymbols.step_mode
.. autoattribute:: LinemapSymbols.color
.. autoattribute:: LinemapSymbols.fill_color
.. autoattribute:: LinemapSymbols.size
.. autoattribute:: LinemapSymbols.line_thickness

.. autoclass:: GeometrySymbol

    **Attributes**

    .. autosummary::
        :nosignatures:

        shape

.. autoattribute:: GeometrySymbol.shape

.. autoclass:: TextSymbol

    **Attributes**

    .. autosummary::
        :nosignatures:

        text
        typeface

.. autoattribute:: TextSymbol.text
.. autoattribute:: TextSymbol.typeface

Sketch Plots
------------

SketchPlot
^^^^^^^^^^

.. autoclass:: SketchPlot
    :members:
    :inherited-members:
    :member-order: bysource

View
----

Viewports
^^^^^^^^^

.. autoclass:: ReadOnlyViewport
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: Viewport
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: Cartesian2DViewport
    :members:
    :inherited-members:
    :member-order: bysource

Cartesian2DView
^^^^^^^^^^^^^^^

.. autoclass:: Cartesian2DView
    :members:
    :inherited-members:
    :member-order: bysource

Cartesian3DView
^^^^^^^^^^^^^^^

.. autoclass:: Cartesian3DView
    :members:
    :inherited-members:
    :member-order: bysource

LineView
^^^^^^^^

.. autoclass:: LineView
    :members:
    :inherited-members:
    :member-order: bysource

PolarView
^^^^^^^^^

.. autoclass:: PolarView
    :members:
    :inherited-members:
    :member-order: bysource
