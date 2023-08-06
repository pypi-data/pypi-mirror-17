Data Access and Manipulation
============================

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot.data

.. py:currentmodule:: tecplot.data

Loading Data
------------

.. autofunction:: load_tecplot
.. autofunction:: load_cgns
.. autofunction:: load_fluent
.. autofunction:: load_plot3d

Saving Data
-----------

.. autofunction:: save_tecplot_binary
.. autofunction:: save_tecplot_ascii

.. py:currentmodule:: tecplot.data.query

Data Queries
------------

.. autofunction:: probe_at_position

.. py:currentmodule:: tecplot.data.operate

Data Operations
---------------

.. autoclass:: Range

.. autofunction:: execute_equation

.. py:currentmodule:: tecplot.data

Dataset
-------

.. autoclass:: Dataset

    **Attributes**

    .. autosummary::
        :nosignatures:

        num_variables
        num_zones
        title

    **Methods**

    .. autosummary::
        :nosignatures:

        add_ordered_zone
        add_fe_zone
        add_poly_zone
        add_variable
        add_zone
        copy_zones
        delete_variables
        delete_zones
        variable
        variables
        zone
        zones

    **Special Methods**

    .. autosummary::
        :nosignatures:

        __str__
        __repr__
        __eq__

.. autoattribute:: Dataset.title
.. autoattribute:: Dataset.num_variables
.. autoattribute:: Dataset.num_zones
.. automethod:: Dataset.variable
.. automethod:: Dataset.variables
.. automethod:: Dataset.zone
.. automethod:: Dataset.zones
.. automethod:: Dataset.copy_zones
.. automethod:: Dataset.add_ordered_zone
.. automethod:: Dataset.add_fe_zone
.. automethod:: Dataset.add_poly_zone
.. automethod:: Dataset.add_variable
.. automethod:: Dataset.add_zone
.. automethod:: Dataset.delete_variables
.. automethod:: Dataset.delete_zones
.. automethod:: Dataset.__str__
.. automethod:: Dataset.__repr__
.. automethod:: Dataset.__eq__

Variable
--------

.. autoclass:: Variable

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        num_zones

    **Methods**

    .. autosummary::
        :nosignatures:

        zone
        zones

    **Special Methods**

    .. autosummary::
        :nosignatures:

        __str__
        __repr__
        __eq__

.. autoattribute:: Variable.index
.. autoattribute:: Variable.name
.. autoattribute:: Variable.num_zones
.. automethod:: Variable.zone
.. automethod:: Variable.zones
.. automethod:: Variable.__str__
.. automethod:: Variable.__repr__
.. automethod:: Variable.__eq__

Zone
----

.. autoclass:: Zone

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        num_points
        shape
        num_variables

    **Methods**

    .. autosummary::
        :nosignatures:

        variable
        variables
        copy

    **Special Methods**

    .. autosummary::
        :nosignatures:

        __str__
        __repr__
        __eq__

.. autoattribute:: Zone.index
.. autoattribute:: Zone.name
.. autoattribute:: Zone.num_points
.. autoattribute:: Zone.shape
.. autoattribute:: Zone.num_variables
.. automethod:: Zone.variable
.. automethod:: Zone.variables
.. automethod:: Zone.copy
.. automethod:: Zone.__str__
.. automethod:: Zone.__repr__
.. automethod:: Zone.__eq__

Array
-----

.. autoclass:: Array
    :members:
