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
	self.index1 = Index(self.score1).build()	
	self.index2 = Index(self.score2).build()
    
    def display(self, msr=0, part=0):
        """Useful for displaying the differences between the two scores visually

        Kwargs:
          msr (int): A measure number to display

	  part (int): A part number to examine.  
          
	  
        """

        self.__verify_part_and_measure__(msr, part)	
	
	partial1 = self.score1.parts[part].getElementsByClass('Measure')[msr]
	partial2 = self.score2.parts[part].getElementsByClass('Measure')[msr]
        partial1.show()
        partial2.show()


    def have_same_accidentals(self, msr=0, part=0):
        """Checks if the two scores both have the same accidentals at the 
	specified measure and for the specified part

	Kwargs:
	  msr (int): the measure number at which to make the comparison
	
	  part (int): the part for which to make the comparison

	Returns:
	  boolean. The result of the comparison::

	   True -- The scores have the same accidentals
	   False -- The scores do not have the same accidentals

	Raises:
	  ScoreException
	
	
	"""

        self.__verify_part_and_measure__(msr, part)
        
	accidentals1 = self.__get_accidentals__(msr,part,1)
	accidentals2 = self.__get_accidentals__(msr,part,2)

	logging.debug("accidentals1: " +str([x.name for x in accidentals1]))
	logging.debug("accidentals2: " +str([x.name for x in accidentals2]))
	return accidentals1 == accidentals2


    def __get_accidentals__(self, msr, part, score_number):
        """A helper function for the have_same_accidentals fuction
	
	Args:
	  msr (int): measure at which the accidentals should be collected

	  part (int): the part number for which the score should be analyzed

	  score_number (int):  A score number so the function knows which score to analyze

	Returns:
	  list:  The collected accidentals


	"""

        if(score_number == 1):

	    measures = self.score1.parts[part].getElementsByClass('Measure')
	    notes = measures[msr].flat.notes

            if(self.index1['key'][part][msr] == 'atonal'):

	        altered = []

	    else:

                altered = [x.name for x in self.index1['key'][part][msr].alteredPitches]
	   	    
        elif(score_number == 2):

            measures = self.score2.parts[part].getElementsByClass('Measure')
            notes = measures[msr].flat.notes

            if(self.index2['key'][part][msr] == 'atonal'):

	        altered = []
            
	    else:
		    
	        altered = [x.name for x in self.index2['key'][part][msr].alteredPitches]
                           
        naturals = set()
        accidentals = []
	
        for index in range(0, len(notes)):

            if(notes[index].isChord):

                for pitch in notes[index].pitches:

                    if(not pitch.accidental is None and not pitch.name in altered):

                        accidentals.append(pitch.accidental)

                        if(pitch.accidental.name == 'natural'):

                            naturals.add(pitch.name)

                    elif(pitch.name in altered and pitch.name[0] in naturals):

                        accidentals.append(pitch.accidental)
                        naturals.discard(pitch.name)
		
            elif(not notes[index].accidental is None and not notes[index].name in altered):

                accidentals.append(notes[index].accidental)

                if(notes[index].accidental.name == 'natural'):

                    naturals.add(notes[index].name)

            elif(notes[index].name in altered and notes[index].name[0] in naturals):

                accidentals.append(notes[index].accidental)
                naturals.discard(notes[index].name)
					
        return accidentals


    def have_same_articulations(self, msr=0, part=0):
        """Checks if the two scores both have the same articulations 
	at the specified measure and for the specified part [#f2]_
	
	Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same articulations
           False -- The scores do not have the same articulations

        Raises:
          ScoreException
       

        """

	self.__verify_part_and_measure__(msr, part)
                
	notes1 = self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes
        notes2 = self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes
	articulations1 = []
	articulations2 = []
        
        for index in range(0, len(notes1)):
            
            articulations1 += notes1[index].articulations

	for index in range(0, len(notes2)):

	    articulations2 += notes2[index].articulations
        	
	logging.debug("articulations1: " +str(articulations1))
	logging.debug("articulations2: "+ str(articulations2))
        return articulations1 == articulations2


    def have_same_clef_markings(self, msr=0, part=0):
        """Checks if the two scores both have the same clef markings 
	at the specified measure and for the specified part

        Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same clef markings
           False -- The scores do not have the same clef markings

        Raises:
          ScoreException


        """

        self.__verify_part_and_measure__(msr, part)

        measures1 = self.score1.parts[part].getElementsByClass('Measure')
	measures2 = self.score2.parts[part].getElementsByClass('Measure')
        clef1 = self.index1['clef'][part][msr]
        clef2 = self.index2['clef'][part][msr]
	        	
	logging.debug("clef1.sign: " + str(clef1.sign))
	logging.debug("clef2.sign: " + str(clef2.sign))
	return clef1.sign == clef2.sign
    


    def have_same_key_signature(self, msr=0, part=0):
        """Checks if the two scores both have the same key signature 
	at the specified measure and for the specified part

        Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same key
           False -- The scores do not have the same key

        Raises:
          ScoreException
       

        """


        self.__verify_part_and_measure__(msr, part)
        measures1 = self.score1.parts[part].getElementsByClass('Measure')
	measures2 = self.score2.parts[part].getElementsByClass('Measure')
	key_signature1 = self.index1['key'][part][msr]
        key_signature2 = self.index2['key'][part][msr]

	if(key_signature1 == 'atonal' and not key_signature2 == 'atonal' or
			key_signature2 == 'atonal' and not key_signature1 == 'atonal'):

	    return False

        if(key_signature1 == 'atonal' and key_signature2 == 'atonal'):

	    return True
        		
	logging.debug("key signature 1.sharps: "+str(key_signature1.sharps))
	logging.debug("key signature 2.sharpts: "+str(key_signature2.sharps))
	return key_signature1.sharps == key_signature2.sharps


    def have_same_ornaments(self, msr=0, part=0):
        """Checks if the two scores both have the same ornaments at the specified measure and for the specified part

        Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same ornaments
           False -- The scores do not have the same ornaments

        Raises:
          ScoreException


        """

	self.__verify_part_and_measure__(msr, part)
        
        notes1 = self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes
        notes2 = self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes
        ornaments1 = []
	ornaments2 = []

        for index in range(0, len(notes1)):
            
            e1 = notes1[index].expressions
                        
            
            for inner_index in range(0, len(e1)):
                
                classes = e1[inner_index].classes
		    
	        for third_index in range(0, len(classes)):

		    if(classes[third_index] in ScoreDiff.ORNAMENTS):
                    
                        ornaments1.append(classes[third_index])
                
	for index in range(0, len(notes2)):

	    e2 = notes2[index].expressions
	    
            for inner_index in range(0, len(e2)):
                
                classes = e2[inner_index].classes

	        for third_index in range(0, len(classes)):
		    
		    if(classes[third_index] in ScoreDiff.ORNAMENTS):
                        
                        ornaments2.append(classes[third_index])
                
        
	logging.debug("ornaments1: "+ str(ornaments1))
	logging.debug("ornaments2: " + str(ornaments2))
	return ornaments1 == ornaments2    


    def have_same_pitches(self, msr=0, part=0):
        """Checks if the two scores both have the same pitches at the specified measure and for the specified part
	
	.. note:: This function will compare pitches in the order that they occur.  
	   To compare without considering order, use have_same_pitches_ignore_order.

        
	Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same pitches
           False -- The scores do not have the same pitches

        Raises:
          ScoreException
       

        """

	self.__verify_part_and_measure__(msr, part)

        pitches1 = self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes.pitches
        pitches2 = self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes.pitches
	
	logging.debug("pitches1: " + str(pitches1))
	logging.debug("pitches2: " + str(pitches2))
        return pitches1 == pitches2


    def have_same_pitches_ignore_order(self, msr=0, part=0):
        """Checks if the two scores both have the same pitches at the specified measure and for the specified part

        .. note:: This function will determine if the same pitches are present without considering the order in which they appear.

        Kwargs:
          msr (int): the measure number at which to make the comparison

	  part (int): the part for which to make the comparison

        Returns:
          boolean.  The result of the comparison::

	    True -- The scores have the same pitches
	    False -- The scores do not have the same pitches

        Raises:
	   ScoreException


	"""

	self.__verify_part_and_measure__(msr, part)

	pitches1 = sorted(self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes.pitches)
        pitches2 = sorted(self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes.pitches)
	logging.debug("pitches1: " + str(pitches1))
	logging.debug("pitches2: " + str(pitches2))
        return pitches1 == pitches2
	

    def have_same_spanners(self, msr=0, part=0):
        """Checks if the two scores both have the same spanner 
	sites at the specified measure and for the specified part [#f1]_
	
	Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same spanners
           False -- The scores do not have the same spanners

        Raises:
          ScoreException
       

        """

	self.__verify_part_and_measure__(msr, part)
        
        notes1 = self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes
        notes2 = self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes

	spanners1=[]
	spanners2=[]

	for index in range(0, len(notes1)):

	    if(notes1[index].isChord):

	        for pitch in notes1[index].pitches:

		    spanners1 += pitch.getSpannerSites()

	    else:

	        spanners1 += notes1[index].getSpannerSites()
	

	for index in range(0, len(notes2)):
		
	    if(notes2[index].isChord):

	        for pitch in notes2[index].pitches:

		    spanners2 += pitch.getSpannerSites()

	    else:

	        spanners2 += notes2[index].getSpannerSites()
	
	logging.debug("spanners1: " + str(spanners1))
	logging.debug("spanners2: " + str(spanners2))
        return spanners1 == spanners2


    def have_same_stem_directions(self, msr=0, part=0):
        """Checks if the two scores both have the same stem 
	directions at the specified measure and for the specified part

        Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same stem directions
           False -- The scores do not have the same stem directions

        Raises:
          ScoreException
       

        """

	self.__verify_part_and_measure__(msr, part)

        notes1 = self.score1.parts[part].getElementsByClass('Measure')[msr].flat.notes
        notes2 = self.score2.parts[part].getElementsByClass('Measure')[msr].flat.notes

        stems1=[]
	stems2=[]
        
	for index in range(0, len(notes1)):

	    if(notes1[index].isChord):

	        temp = set()

		for pitch in notes1[index].pitches:

		    temp.add(notes1[index].getStemDirection(pitch))

		stems1 += list(temp)

						
	    else:

	        stems1+=[notes1[index].stemDirection]
	
        for index in range(0, len(notes2)):
			
	    if(notes2[index].isChord):

	        temp = set()

		for pitch in notes2[index].pitches:

		    temp.add(notes2[index].getStemDirection(pitch))

		stems2 += list(temp)

			
            else:

                stems2 += [notes2[index].stemDirection]
	
	logging.debug("stems1: " + str(stems1))
	logging.debug("stems2: " + str(stems2))
        return stems1 == stems2
      
   	
    def have_same_time_signature(self, msr=0, part=0):
        """Checks if the two scores both have the same time 
	signature at the specified measure and for the specified part

        Kwargs:
          msr (int):  the measure number at which to make the comparison
          
	  part (int): the part for which to make the comparison

        Returns:
          boolean.   The result of the comparison::

           True -- The scores have the same time signature
           False -- The scores do not have the same time signature

        Raises:
          ScoreException
       

        """

	self.__verify_part_and_measure__(msr, part)

        time_signature1 = self.index1['time'][part][msr]        
	time_signature2 = self.index2['time'][part][msr]	
	
	numerator1 = time_signature1.numerator
        numerator2 = time_signature2.numerator
        denominator1 = time_signature1.denominator
        denominator2 = time_signature2.denominator
	
	logging.debug("time signature1: "+str(numerator1) +"/"+str(denominator1))
	logging.debug("time signature2: "+str(numerator2) +"/"+str(denominator2))
        return numerator1 == numerator2 and denominator1 == denominator2 

    def __verify_part_and_measure__(self, msr, part):
        """Checks to make sure the part and measure numbers a user has entered are 
	not outside of the range that exists for either score

        Args:
          part (int): The part number to check

	  msr (int): The measure number to check

        Raises:
          ScoreException


        """

        self.__verify_part__(part)

	if (msr >= len(self.score1.parts[part].getElementsByClass('Measure').elements) or msr < 0):

	    raise MeasureRangeError("measure number "+str(msr) + " does not exist for "+self.name1)
	
	if (msr >= len(self.score2.parts[part].getElementsByClass('Measure').elements) or msr < 0):
		
	    raise MeasureRangeError("measure number "+str(msr) + " does not exist for "+self.name2)


    def __verify_part__(self, part):
        """Checks to make sure the part number a user has entered is not outside the range that exists for either score

	Args:
	  part (int): The part number to check

	Raises:
	  ScoreException


	"""

        if (part >= len(self.score1.parts) or part < 0):

            raise PartRangeError("part number " + str(part) + " does not exist for " + self.name1)

        if (part >= len(self.score2.parts) or part < 0):

            raise PartRangeError("part number " + str(part) + " does not exist for " + self.name2)


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
	"""Function for fetching this object's error message
		
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
	"""Function for fetching this object's error message"

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
	"""Function for fetching this object's error message

	Returns:
	  This object's error message


	"""

        return repr(self.value)



