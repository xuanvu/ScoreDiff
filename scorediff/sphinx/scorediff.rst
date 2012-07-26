scorediff
************************

.. automodule:: scorediff


Class: ScoreDiff
-------------------------

.. autoclass:: ScoreDiff
  
---------

.. automethod:: ScoreDiff.display

Example1.1
+++++++++++++++++++
::
        
        >>> from scorediff import *
        >>> diff = ScoreDiff('bwv66.6.mxl', 'beethoven_appassionata.mxl')
        >>> diff.display(3,1,5,0)
                
.. note::  
        This will display the 4th measure of the 2nd part of score1
        and the 6th measure of the first part of score2.  As usual,
        counting begins at zero, hence the reason 3 gives the 4th measure.
         

Example1.2
++++++++++++++
::

        >>> from scorediff import *
        >>> diff = ScoreDiff('bwv66.6.mxl', 'beethoven_appassionata.mxl')
        >>> diff.display(0,0,6000,0)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "scorediff.py", line 74, in display
        self.__verify_part_and_measure__(msr1, part1, msr2, part2)      
        File "scorediff.py", line 652, in __verify_part_and_measure__
        raise MeasureRangeError("measure number "+str(msr2) + " does not exist for "+self.name2)
        scorediff.MeasureRangeError: 'measure number 6000 does not exist for beethoven_appassionata.mxl'

-------

.. automethod:: ScoreDiff.have_same_accidentals

Example2.1
+++++++++++++
::

        >>> from scorediff import *
        >>> diff = ScoreDiff('bwv66.6.mxl', 'beethoven_appassionta.mxl')
        >>> diff.have_same_accidentals()
        True
        >>>

Example2.2
+++++++++++++
::

        >>> from scorediff import *
        >>> diff = ScoreDiff('bwv66.6.mxl', 'beethoven_appassionata.mxl')
        >>> for i in range(0, 10):
        ...     print diff.have_same_accidentals()
        ... 
        True
        True
        True
        True
        True
        True
        True
        True
        True
        True
        >>> 

Example2.3
++++++++++++
::

        >>> from scorediff import *
        >>> diff = ScoreDiff('bwv66.6.mxl', 'beethoven_appassionata.mxl')
        >>> for i in range(0, 10):
        ...     print diff.have_same_accidentals(i,0,i)
        ...
        True
        True
        True
        False
        True
        False
        False
        True
        True
        False
        >>>

-----

.. automethod:: ScoreDiff.have_same_articulations



-------

.. automethod:: ScoreDiff.have_same_clef_markings


-------

.. automethod:: ScoreDiff.have_same_key_signature

Example3.1
+++++++++++
Suppose a musicxml file contains the following snippet::

        </part-list>
        <part id="P1">
          <measure number="0">
            <attributes>
              <divisions>1080</divisions>
              
              <time>
                <beats>4</beats>
                <beat-type>4</beat-type>
              </time>
              <clef>
                <sign>G</sign>
                <line>2</line>
                </clef>
                </attributes>


If it seems like something is missing here, it's because
a key signature was intentionally omitted.  The have_same_key_signature
method will treat this measure as an atonal passage.  Two atonal passages
will be said to have the same key signature.


-------

.. automethod:: ScoreDiff.have_same_ornaments

-------

.. automethod:: ScoreDiff.have_same_pitches

-------

.. automethod:: ScoreDiff.have_same_pitches_ignore_order

-------

.. automethod:: ScoreDiff.have_same_spanners

-------

.. automethod:: ScoreDiff.have_same_stem_directions

-------

.. automethod:: ScoreDiff.have_same_time_signature
      
Class: RangeError
------------------------
.. autoclass:: RangeError
   :members:

Class: MeasureRangeError
------------------------
.. autoclass:: MeasureRangeError
   :members:

Class: PartRangeError
------------------------
.. autoclass:: PartRangeError
   :members:





.. rubric:: Footnotes

.. [#f1] http://mit.edu/music21/doc/html/moduleSpanner.html

.. [#f2] http://mit.edu/music21/doc/html/moduleArticulations.html?highlight=articulation#music21.articulations
