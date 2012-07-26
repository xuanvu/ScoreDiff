tables
**********************

.. automodule:: tables
   
Class: Tables
---------------

.. autoclass:: Tables

----------------------

.. automethod:: Tables.build_clef

Example1.1
++++++++++++++
::

        >>> from music21 import *
        >>> from tables import *
        >>> table = Tables(corpus.parse('bwv66.6.mxl'))
        >>> clefs = table.build_clefs(1)
        >>> clefs[0]
        <music21.clef.TrebleClef>


