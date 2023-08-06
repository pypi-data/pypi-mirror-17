Layouts
=======

..  contents::
    :local:
    :depth: 2

Layouts
-------

.. automodule:: tecplot.layout

.. py:currentmodule:: tecplot

.. autosummary::
    :nosignatures:

    active_frame
    active_page
    add_page
    export_image
    new_layout
    load_layout
    page
    pages
    save_layout

.. autofunction:: new_layout
.. autofunction:: load_layout
.. autofunction:: save_layout

.. autofunction:: add_page
.. autofunction:: active_page
.. autofunction:: page
.. autofunction:: pages

.. autofunction:: active_frame

.. py:currentmodule:: tecplot.layout

Frame
-----

.. autoclass:: Frame

    **Attributes**

    .. autosummary::
        :nosignatures:

        active # is_active() ?
        background_color
        border_thickness
        dataset
        header_background_color
        height
        name
        page
        plot_type
        show_border
        show_header
        size_pos_units
        transparent
        width

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        active_zones
        add_text
        create_dataset
        move_to_bottom
        move_to_top
        plot

    **Special Methods**

    .. autosummary::
        :nosignatures:

        __str__
        __repr__
        __eq__

.. autoattribute:: Frame.name
.. autoattribute:: Frame.active
.. automethod:: Frame.activate
.. automethod:: Frame.move_to_bottom
.. automethod:: Frame.move_to_top
.. autoattribute:: Frame.page
    :annotation:

Data and Zones
^^^^^^^^^^^^^^

.. autoattribute:: Frame.dataset
.. automethod:: Frame.create_dataset
.. automethod:: Frame.active_zones

Plot, Annotations and Style
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoattribute:: Frame.plot_type
.. automethod:: Frame.plot
.. automethod:: Frame.add_text
.. autoattribute:: Frame.height
.. autoattribute:: Frame.width
.. autoattribute:: Frame.size_pos_units
.. autoattribute:: Frame.show_header
.. autoattribute:: Frame.header_background_color
.. autoattribute:: Frame.transparent
.. autoattribute:: Frame.background_color
.. autoattribute:: Frame.show_border
.. autoattribute:: Frame.border_thickness

Special Methods
^^^^^^^^^^^^^^^

.. automethod:: Frame.__str__
.. automethod:: Frame.__repr__
.. automethod:: Frame.__eq__

Page
----

.. autoclass:: Page

    **Attributes**

    .. autosummary::
        :nosignatures:

        active
        name
        paper

    **Methods**

    .. autosummary::
        :nosignatures:

        activate
        active_frame
        add_frame
        frame
        frames

    **Special Methods**

    .. autosummary::
        :nosignatures:

        __str__
        __repr__
        __eq__
        __contains__
        __getitem__
        __iter__

.. autoattribute:: Page.name
.. autoattribute:: Page.active
.. automethod:: Page.activate
.. autoattribute:: Page.paper

Accessing and Creating Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Page.active_frame
.. automethod:: Page.frame
.. automethod:: Page.frames
.. automethod:: Page.add_frame

Special Methods
^^^^^^^^^^^^^^^

.. automethod:: Page.__str__
.. automethod:: Page.__repr__
.. automethod:: Page.__eq__
.. automethod:: Page.__contains__
.. automethod:: Page.__getitem__
.. automethod:: Page.__iter__

Paper
-----

.. autoclass:: Paper

    **Attributes**

    .. autosummary::
        :nosignatures:

        dimensions

.. autoattribute:: Paper.dimensions
