"""

.. module:: scorediff
    :synopsis: A module for comparing two musicxml files and displaying the differences

..  moduleauthor:: Julien Dubeau <jdubeau@dons.usfca.edu>


"""

import music21.environment
from music21.corpus import base
import logging
logging.basicConfig(filename='debug.log', level = logging.DEBUG)
#To enable debug output, comment out the following line
logging.disable(logging.DEBUG)
from tables import *


class ScoreDiff:
    """The ScoreDiff class uses the music21 toolkit to parse and analyze two scores passed
    to the initialization function, so that the user can detect and display certain differences.


    """


    #This ornaments list is used as a reference when comparing ornaments    
    ORNAMENTS = set(['Appoggiatura', 'GeneralAppoggiatura', 'GeneralMordent', 'HalfStepAppoggiatura',
                 'HalfSetpInvertedAppoggiatura', 'HalfStepInvertedMordent', 'HalfStepMordent', 'HalfStepTrill',
                 'InvertedAppoggiatura', 'InvertedMordent', 'InvertedTurn', 'Mordent', 'Schleifer', 'Shake',
                 'Tremolo', 'Trill', 'Turn', 'WholeStepAppoggiatura', 'WholeStepInvertedAppoggiatura',
                 'WholeStepInvertedMordent', 'WholeStepMordent', 'WholeStepTrill'])


    def __init__(self, score1, score2, localCorpusPath = '.'):
        """Initializes a ScoreDiff object.
    
        Args:
         score1 (str):  The pathname of a score to parse
         
	 score2 (str):  The pathname of a score to parse and compare to score1

        Kwargs:
         localCorpusPath (str)  A path to a corpus if your files are located elsewhere


	"""        

        music21.environment.set('localCorpusPath', localCorpusPath)
        self.score1 = base.parse(score1)
       	self.score2 = base.parse(score2)
        self.name1 = score1
        self.name2 = score2
	self.index1 = Tables(self.score1).build()	
	self.index2 = Tables(self.score2).build()
    
    def display(self, msr1=0, part1=0, msr2=0, part2=0):
        """Useful for displaying the differences between the two scores visually

        Kwargs:
          msr1 and msr2 (int): measure numbers to display

	  part1 and part2 (int): part numbers to display 

	Raises:
	  PartRangeError: If user passes in a part that is out of range for either score

	  MeasureRangeError: If user passes in a measure that is out of range for either score
          
	  
        """

        self.__verify_part_and_measure(msr1, part1, msr2, part2)	
	
	partial1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1]
	partial2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2]
        partial1.show()
        partial2.show()


    def have_same_accidentals(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same accidentals at the 
	specified measures and for the specified parts

	.. note:: This method will ignore a cautionary sharp or flat on a pitch
	   that is already altered in the same way in the key signature.

	Kwargs:
	  msr1 and msr2 (int): The measures to compare	
	  
	  part1 and part2 (int): The parts to compare

	Returns:
	  boolean. The result of the comparison::

	   True -- The scores have the same accidentals
	   False -- The scores do not have the same accidentals

	Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score


	"""

        self.__verify_part_and_measure(msr1, part1, msr2, part2)
        
	accidentals1 = self.__get_accidentals(1,msr1,part1)
	accidentals2 = self.__get_accidentals(2,msr2,part2)

	logging.debug("accidentals1: " +str([x.name for x in accidentals1]))
	logging.debug("accidentals2: " +str([x.name for x in accidentals2]))
	return accidentals1 == accidentals2


    def __get_accidentals(self, score_number, msr=0, part=0):
        """A helper method for the have_same_accidentals method
	
	Args:
	  msr (int): measure at which the accidentals should be collected

	  part (int): the part number for which the score should be analyzed

	  score_number (int):  A score number so the method knows which score to analyze

	Returns:
	  list:  The collected accidentals


	"""

        if(score_number == 1):

	    measures = self.score1.parts[part].getElementsByClass('Measure')
	    notes = measures[msr].flat.notes

            if(self.index1['key'][part][msr] is None):

	        altered = []

	    else:

                altered = [x.name for x in self.index1['key'][part][msr].alteredPitches]
	   	    
        elif(score_number == 2):

            measures = self.score2.parts[part].getElementsByClass('Measure')
            notes = measures[msr].flat.notes

            if(self.index2['key'][part][msr] is None):

	        altered = []
            
	    else:
		    
	        altered = [x.name for x in self.index2['key'][part][msr].alteredPitches]
                           
        naturals = set()
        accidentals = []
	
        for note in notes:

            if(note.isChord):

                for pitch in note.pitches:

                    if(not pitch.accidental is None and not pitch.name in altered):

                        accidentals.append(pitch.accidental)

                        if(pitch.accidental.name == 'natural'):

                            naturals.add(pitch.name)

                    elif(pitch.name in altered and pitch.name[0] in naturals):

                        accidentals.append(pitch.accidental)
                        naturals.discard(pitch.name)
		
            elif(not note.accidental is None and not note.name in altered):

                accidentals.append(note.accidental)

                if(note.accidental.name == 'natural'):

                    naturals.add(note.name)

            elif(note.name in altered and note.name[0] in naturals):

                accidentals.append(note.accidental)
                naturals.discard(note.name)
					
        return accidentals


    def have_same_articulations(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same articulations 
	at the specified measures and for the specified parts [#f2]_
	
	Kwargs:
          msr1 and msr2 (int):  The measures to compare

	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same articulations
           False -- The scores do not have the same articulations

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score

       

        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)
                
	notes1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes
        notes2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes
	articulations1 = []
	articulations2 = []
        
        for note in notes1:
            
            articulations1 += note.articulations

	for note in notes2:

	    articulations2 += note.articulations
        	
	logging.debug("articulations1: " +str(articulations1))
	logging.debug("articulations2: "+ str(articulations2))
        return articulations1 == articulations2


    def have_same_clef_markings(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same clef markings 
	at the specified measures and for the specified parts

	.. note:: The current version does not support mid-measure clef
	   changes.  This is something that will be addressed in future
	   versions.

        Kwargs:
          msr1 and msr2 (int):  The measures to compare

	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same clef markings
           False -- The scores do not have the same clef markings

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score



        """

        self.__verify_part_and_measure(msr1, part1, msr2, part2)

        clef1 = self.index1['clef'][part1][msr1]
        clef2 = self.index2['clef'][part2][msr2]
	        	
	logging.debug("clef1.sign: " + str(clef1.sign))
	logging.debug("clef2.sign: " + str(clef2.sign))
	return clef1.sign == clef2.sign
    


    def have_same_key_signature(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same key signature 
	at the specified measures and for the specified parts

	.. note:: The exception raised in the case of a measure with no
	   key signature is done to alert the user in case someone has
	   inadvertently omitted a key signature from a measure, not to
	   suggest that an atonal piece is "wrong".

        Kwargs:
          msr1 and msr2 (int): The measures to compare

	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same key
           False -- The scores do not have the same key

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score

	  AtonalPassageException: If there is no recorded key signature for msr1 or msr2

       

        """


        self.__verify_part_and_measure(msr1, part1, msr2, part2)
       	key_signature1 = self.index1['key'][part1][msr1]
        key_signature2 = self.index2['key'][part2][msr2]

	if(key_signature1 is None  and key_signature2 is not None or
			key_signature2 is None and key_signature1 is not None):
            
	    raise AtonalPassageException("One or more measures does not have a key signature")

        if(key_signature1 is None and key_signature2 is None):

	    raise AtonalPassageException("Neither measure has a key signature")
        		
	logging.debug("key signature1.sharps: "+str(key_signature1.sharps))
	logging.debug("key signature2.sharps: "+str(key_signature2.sharps))
	return key_signature1.sharps == key_signature2.sharps


    def have_same_ornaments(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same ornaments at the specified measures and for the specified parts

        Kwargs:
          msr1 and msr2 (int):  The measures to compare
          
	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same ornaments
           False -- The scores do not have the same ornaments

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score



        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)
        
        notes1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes
        notes2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes
        ornaments1 = []
	ornaments2 = []

        for note in notes1:
            
            expressions = note.expressions
                                    
            for expression in expressions:
                
                classes = expression.classes
		    
	        for cls in classes:

		    if(cls in ScoreDiff.ORNAMENTS):
                    
                        ornaments1.append(cls)
                
	for note in notes2:

	    expressions = note.expressions
	    
            for expression in expressions:
                
                classes = expression.classes

	        for cls in classes:
		    
		    if(cls in ScoreDiff.ORNAMENTS):
                        
                        ornaments2.append(cls)
                        
	logging.debug("ornaments1: "+ str(ornaments1))
	logging.debug("ornaments2: " + str(ornaments2))
	return ornaments1 == ornaments2    


    def have_same_pitches(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same pitches at the specified measures and for the specified parts
	
	.. note:: This method will compare pitches in the order that they occur.  
	   To compare without considering order, use have_same_pitches_ignore_order.

        
	Kwargs:
          msr1 and msr2 (int):  The measures to compare
          
	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same pitches
           False -- The scores do not have the same pitches

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score
       

        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)

        pitches1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes.pitches
        pitches2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes.pitches
	
	logging.debug("pitches1: " + str(pitches1))
	logging.debug("pitches2: " + str(pitches2))
        return pitches1 == pitches2


    def have_same_pitches_ignore_order(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same pitches at the specified measures and for the specified parts

        .. note:: This method will determine if the same pitches are present without considering the order in which they appear.

        Kwargs:
          msr1 and msr2 (int): The measures to compare

	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.  The result of the comparison::

	    True -- The scores have the same pitches
	    False -- The scores do not have the same pitches

        Raises:
	   PartRangeError: If user passes in a part that is out of range for either score
	   
	   MeasureRangeError: If user passes in a measure that is out of range for either score



	"""

	self.__verify_part_and_measure(msr1, part1, msr2, part2)

	pitches1 = sorted(self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes.pitches)
        pitches2 = sorted(self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes.pitches)
	logging.debug("pitches1: " + str(pitches1))
	logging.debug("pitches2: " + str(pitches2))
        return pitches1 == pitches2
	

    def have_same_spanners(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same spanner 
	sites at the specified measures and for the specified parts [#f1]_
	
	Kwargs:
          msr1 and msr2 (int):  The measures to compare
          
	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same spanners
           False -- The scores do not have the same spanners

        Raises:
	   PartRangeError: If user passes in a part that is out of range for either score
	   
	   MeasureRangeError: If user passes in a measure that is out of range for either score

       

        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)
        
        notes1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes
        notes2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes

	spanners1=[]
	spanners2=[]

	for note in notes1:

	    if(note.isChord):

	        for pitch in note.pitches:

		    spanners1 += pitch.getSpannerSites()

	    else:

	        spanners1 += note.getSpannerSites()
	

	for note in notes2:
		
	    if(note.isChord):

	        for pitch in note.pitches:

		    spanners2 += pitch.getSpannerSites()

	    else:

	        spanners2 += note.getSpannerSites()
	
	logging.debug("spanners1: " + str(spanners1))
	logging.debug("spanners2: " + str(spanners2))
        return spanners1 == spanners2


    def have_same_stem_directions(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same stem 
	directions at the specified measures and for the specified parts

	.. note:: This method will consider a chord with multiple upward
	   pointing stems as one upward pointing stem.  This is done to facilitate
	   the comparison of a passage with chords to simpler passages.  The method
	   will, however, pick up on a stem direction within a chord that is different 
	   from the other stem directions in the chord.

        Kwargs:
          msr1 and msr2 (int):  The measures to compare
          
	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same stem directions
           False -- The scores do not have the same stem directions

        Raises:
	  PartRangeError: If user passes in a part that is out of range for either score
	  
	  MeasureRangeError: If user passes in a measure that is out of range for either score

       

        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)

        notes1 = self.score1.parts[part1].getElementsByClass('Measure')[msr1].flat.notes
        notes2 = self.score2.parts[part2].getElementsByClass('Measure')[msr2].flat.notes

        stems1=[]
	stems2=[]
        
	for note in notes1:

	    if(note.isChord):

	        temp = set()

		for pitch in note.pitches:

		    temp.add(note.getStemDirection(pitch))

		stems1 += temp

						
	    else:

	        stems1+=[note.stemDirection]
	
        for note in notes2:
			
	    if(note.isChord):

	        temp = set()

		for pitch in note.pitches:

		    temp.add(note.getStemDirection(pitch))

		stems2 += temp

			
            else:

                stems2 += [note.stemDirection]
	
	logging.debug("stems1: " + str(stems1))
	logging.debug("stems2: " + str(stems2))
        return stems1 == stems2
      
   	
    def have_same_time_signature(self, msr1=0, part1=0, msr2=0, part2=0):
        """Checks if the two scores both have the same time 
	signature at the specified measures and for the specified parts

        Kwargs:
          msr1 and msr2 (int):  The measures to compare
          
	  part1 and part2 (int): The parts to compare

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same time signature
           False -- The scores do not have the same time signature

        Raises:
	   PartRangeError: If user passes in a part that is out of range for either score
	   
	   MeasureRangeError: If user passes in a measure that is out of range for either score

       

        """

	self.__verify_part_and_measure(msr1, part1, msr2, part2)

        time_signature1 = self.index1['time'][part1][msr1]        
	time_signature2 = self.index2['time'][part2][msr2]	
	
	numerator1 = time_signature1.numerator
        numerator2 = time_signature2.numerator
        denominator1 = time_signature1.denominator
        denominator2 = time_signature2.denominator
	
	logging.debug("time signature1: "+str(numerator1) +"/"+str(denominator1))
	logging.debug("time signature2: "+str(numerator2) +"/"+str(denominator2))
        return numerator1 == numerator2 and denominator1 == denominator2 

    def __verify_part_and_measure(self, msr1, part1, msr2, part2):
        """Checks to make sure the part and measure numbers a user has entered are 
	not outside of the range that exists for either score

        Args:
          part1 and part2 (int): The part number to check for score1 and score2, respectively

	  msr1 and msr2 (int): The measure number to check for score1 and score2, respectively

        Raises:
	   PartRangeError: If user passes in a part that is out of range for either score
	   
	   MeasureRangeError: If user passes in a measure that is out of range for either score



        """

        self.__verify_part(part1, part2)


	if (msr1 >= len(self.score1.parts[part1].getElementsByClass('Measure').elements) or msr1 < 0):

	    raise MeasureRangeError("measure number "+str(msr1) + " does not exist for "+self.name1)
	
	if (msr2 >= len(self.score2.parts[part2].getElementsByClass('Measure').elements) or msr2 < 0):
		
	    raise MeasureRangeError("measure number "+str(msr2) + " does not exist for "+self.name2)


    def __verify_part(self, part1, part2):
        """Checks to make sure the part number a user has entered is not outside the range that exists for either score

	Args:
	  part1 and part2 (int): The part number to check for score1 and score2, respectively

	Raises:
	  PartRangeError: If user passes in a part that is out of range for either score


	"""

        if (part1 >= len(self.score1.parts) or part1 < 0):

            raise PartRangeError("part number " + str(part1) + " does not exist for " + self.name1)

        if (part2 >= len(self.score2.parts) or part2 < 0):

            raise PartRangeError("part number " + str(part2) + " does not exist for " + self.name2)


class RangeError(Exception):
    """Class for handling range erros while using the ScoreDiff tool


    """

    def __init__(self , value):
        """Initializes the RangeError object

	Args:
	  value (str): An error message


	"""

        self.value = value


    def __str__(self):
	"""method for fetching this object's error message
		
	Returns:
	  This object's error message


	"""

        return repr(self.value)


class MeasureRangeError(RangeError):
    """Exception raised when user enters a measure number that is out of range


    """
  
  
    def __init__(self, value):
	"""Initializes the MeasureRangeError object

	Args:
          value (str): An error message


	"""

	self.value = value


    def __str__(self):
	"""method for fetching this object's error message"

	Returns:
          This object's error message


	"""

        return repr(self.value)


class PartRangeError(RangeError):
    """Exception raised when user enters a part number that is out of range
	

    """
   
   
    def __init__(self, value):
	"""Initializes the PartRangeError object

	Args:
          value (str): An error message


	"""

        self.value = value


    def __str__(self):
	"""method for fetching this object's error message

	Returns:
	  This object's error message


	"""

        return repr(self.value)

class PassageException(Exception):
    """Class for handling unusual passages in a score

    """

    def __init__(self, value):
        """Initializes the PassageException object

	Args:
	  value(str): An error message


	"""

	self.value = value

    def __str__(self):
        """method for fetching this object's error message

	Returns:
	  This object's error message


        """

	return repr(self.value)

class AtonalPassageException(PassageException):
    """Exception raised when an atonal passage is found

    """

    def __init_(self, value):
        """Initializes the AtonalPassageException object

	Args:
	  value(str): An error message


        """

	self.value = value

    def __str__(self):
        """method for fetching this object's error message

	Returns:
	  This object's error message


        """

	return repr(self.value)



