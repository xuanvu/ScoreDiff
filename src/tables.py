"""

.. module:: tables
     :synopsis: A module for keeping track of information about clefs, key signatures,
       and time signatures

..   moduleauthor::  Julien Dubeau <jdubeau@dons.usfca.edu>


"""

class Index:
    """The Index class builds a variety of dictionaries
    for convenient lookup

    """

    def __init__(self, score):
        """sets this object's score to the score passed in

	Args:
	  score (music21.stream.Score):  A music21 score object to analyze
        
	"""
        	
        self.score = score


    def build_clef(self, part):
        """Returns a dictionary of (measure, clef) pairs based on score passed to __init__
	        
	Args:
	  part (music21.stream.Part):  A music21 part object to restrict
	  the building to only one part of the score
        
	Returns:
	  dictionary.

        """
	
        temp = dict()
	measures = self.score.parts[part].getElementsByClass('Measure')
        
	for index, measure in enumerate(measures):

	    if(measure.clef is not None):

                recent_clef = measure.clef
		temp.update({index:measure.clef})

	    else:

		temp.update({index:recent_clef})

	return temp


    def build_all_clefs(self):
        """Returns a dictionary of dictionaries of (measure, clef) pairs based on score passed to __init__
        
	Returns:
	  dictionary

	"""

	temp = dict()

        for i in range(0, len(self.score.parts.elements)):

	    temp.update({i:self.build_clef(i)})

	return temp


    def build_times(self, part):
        """Returns a dictionary of (measure, timesignature) pairs based on score passed to __init__

	Args:
	  part (music21.stream.Part):  A music21 part object to restrict
	  the building to only one part of the score

	Returns:
	  dictionary

	"""

	temp = dict()
	measures = self.score.parts[part].getElementsByClass('Measure')

	for index, measure in enumerate(measures):

	    if(measure.timeSignature is not None):

	        recent_time = measure.timeSignature
		temp.update({index:measure.timeSignature})

	    else:

	        temp.update({index:recent_time})

	return temp


    def build_all_times(self):
        """Returns a dictionary of dictionaries of (measure, timesignature) pairs based on all
	parts in the score
        
	Returns:
	  dictionary

	"""

	temp = dict()
	
	for i in range(0, len(self.score.parts.elements)):

	    temp.update({i:self.build_times(i)})

	return temp


    def build_keys(self, part):
        """Returns a dictionary of (measure, keysignature) pairs based on score passed to __init__
        
	Args:
	  part (music21.stream.Part):  A music21 part object to restrict the building
	  to only part of the score

	Returns:
	  dictionary

	"""

	temp = dict()
	measures = self.score.parts[part].getElementsByClass('Measure')
	recent_key = 'atonal'
	for index, measure in enumerate(measures):

	    if(measure.keySignature is not None):

	        recent_key = measure.keySignature
		temp.update({index:measure.keySignature})

	    else:

	        temp.update({index:recent_key})

	return temp


    def build_all_keys(self):
        """Returns a dictionary of dictionaries of (measure, keysignature) pairs based on all
	parts in the score

	Returns:
	  dictionary

	"""

	temp = dict()

	for i in range(0, len(self.score.parts.elements)):

	    temp.update({i:self.build_keys(i)})

	return temp


    def build(self):
        """Returns a dictionary of dictionaries of dictionaries.  These include all
	of the data that can be obtained from the other methods in this class,
	stored as {'clef':{clefmap}, 'key:{keymap}', 'time:{timemap}'}
	
	Returns:
	  dictionary.  A dictionary of the form described above

	"""

        index = dict(dict(dict()))

	index.update({'clef':self.build_all_clefs()})
	index.update({'time':self.build_all_times()})
	index.update({'key':self.build_all_keys()})

	return index
