"""

.. module:: tables
     :synopsis: A module for keeping track of information about clefs, key signatures,
       and time signatures

..   moduleauthor::  Julien Dubeau <jdubeau@dons.usfca.edu>


"""

class ClefTable:
    """The ClefTable class builds a dictionary of (measure, clef) pairs
    for convenient lookup

    """

    def __init__(self, score):
        """Initializes an empty ClefTable

	Args:
	  score (music21.stream.Score):  A music21 score object to analyze
        
	"""
        	
        self.score = score

    def build(self, part):
        """Returns a dictionary of (measure, clef) pairs based on score passed to __init__
        
        Args:
	  part (music21.stream.Part):  A music21 part object to restrict
	  the building to only one part of the score

	"""
	
        tuples = []
	measures = self.score.parts[part].getElementsByClass('Measure')
	size = len(measures.elements)
        
	for index, measure in enumerate(measures):

	    if(measure.clef is not None):

                recent_clef = measure.clef
		tuples.append((index, measure.clef))

	    else:

	        tuples.append((index, recent_clef))

	return dict(tuples)

    def build_all_parts(self):
        """Returns a dictionary of (part, (measure, clef)) pairs based on score passed to __init__

	"""

	tuples = []

        for i in range(0, len(self.score.parts.elements)):

	    tuples.append((i, (self.build(i))))

	return dict(tuples)


	    
