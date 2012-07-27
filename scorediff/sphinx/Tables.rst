tables
**********************

.. automodule:: tables
   
Class: Tables
---------------

.. autoclass:: Tables

----------------------

.. automethod:: Tables.build_clefs

Example1.1
++++++++++++++
::

        >>> from music21 import *
        >>> from tables import *
        >>> table = Tables(corpus.parse('bwv66.6.mxl'))
        >>> clefs = table.build_clefs(1)
        >>> clefs[0]
        <music21.clef.TrebleClef>



--------------

.. automethod:: Tables.build_all_clefs

Example2.1
++++++++++++++
::

        >>> from music21 import *
        >>> from tables import *
        >>> table = Tables(corpus.parse('bwv66.6.mxl'))
        >>> clefs = table.build_all_clefs()
        >>> clefs[2]
        [<music21.clef.BassClef>, <music21.clef.BassClef>, <music21.clef.BassClef>,
        <music21.clef.BassClef>, <music21.clef.BassClef>, <music21.clef.BassClef>,
        <music21.clef.BassClef>, <music21.clef.BassClef>, <music21.clef.BassClef>,
        <music21.clef.BassClef>]
        >>>

------------

.. automethod:: Tables.build_times

-------

.. automethod:: Tables.build_all_times

--------

.. automethod:: Tables.build_keys

---------

.. automethod:: Tables.build_all_keys


---------

.. automethod:: Tables.build

Example3.1
++++++++++++++
::

        >>> from tables import *
        >>> from music21 import *
        >>> table = Tables(corpus.parse('bwv66.6.mxl'))
        >>> index = table.build()
        >>> index['key'][0][0]
        <music21.key.KeySignature of 3 sharps>
        >>>

        
