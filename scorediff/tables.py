"""

.. module:: tables
     :synopsis: A module for keeping track of information about clefs, key signatures,
       and time signatures

..   moduleauthor::  Julien Dubeau <jdubeau@dons.usfca.edu>


"""

class Tables:
    """The Tables class builds a variety of tables
    for convenient lookup

    """

    def __init__(self, score):
        """sets this object's score to the score passed in

	Args:
	  score (music21.stream.Score):  A music21 score object to analyze
        
	"""
        	
        self.score = score


    def build_clefs(self, part):
        """Returns a list of clef objects based on all measures in part from score passed to __init__
	        
	Args:
	  part (music21.stream.Part):  A music21 part object to restrict
	  the building to only one part of the score
        
	Returns:
	  list.

        """
	
        temp = list()
	measures = self.score.parts[part].getElementsByClass('Measure')
        
	for index, measure in enumerate(measures):

	    if(measure.clef is not None):

                recent_clef = measure.clef
		temp.append(measure.clef)

            else:

		temp.append(recent_clef)

	return temp


    def build_all_clefs(self):
        """Returns a list of lists of clef objects based on score passed to __init__
	A list of clefs can be accessed for a given part via list[part_index]
        
	Returns:
	  list

	"""

	temp = list(list())

        for i in range(0, len(self.score.parts.elements)):

	    temp.append(self.build_clef(i))

	return temp


    def build_times(self, part):
        """Returns a list of timesignature objects based on all measures in part from score passed to __init__

	Args:
	  part (music21.stream.Part):  A music21 part object to restrict
	  the building to only one part of the score

	Returns:
	  list

	"""

	temp = list()
	measures = self.score.parts[part].getElementsByClass('Measure')

	for index, measure in enumerate(measures):

	    if(measure.timeSignature is not None):

	        recent_time = measure.timeSignature
		temp.append(measure.timeSignature)

	    else:

	        temp.append(recent_time)

	return temp


    def build_all_times(self):
        """Returns a list of lists of timesignature objects based on all
	parts in the score.  Access data for a given part with list[part_index]
        
	Returns:
	  list

	"""

	temp = list(list())
	
	for i in range(0, len(self.score.parts.elements)):

	    temp.append(self.build_times(i))

	return temp


    def build_keys(self, part):
        """Returns a list of keysignature objects based on all measures in part from score passed to __init__
        
	Args:
	  part (music21.stream.Part):  A music21 part object to restrict the building
	  to only part of the score

	Returns:
	  list

	"""

	temp = list()
	measures = self.score.parts[part].getElementsByClass('Measure')
	recent_key = None

	for index, measure in enumerate(measures):

	    if(measure.keySignature is not None):

	        recent_key = measure.keySignature
		temp.append(measure.keySignature)

	    else:

	        temp.append(recent_key)

	return temp


    def build_all_keys(self):
        """Returns a list of lists of keysignature objects based on all
	parts in the score.  Access data for a given part with list[part_index]

	Returns:
	  list

	"""

	temp = list(list())

	for i in range(0, len(self.score.parts.elements)):

	    temp.append(self.build_keys(i))

	return temp


    def build(self):
        """Returns a dictionary of doubly nested lists.  These include all
	of the data that can be obtained from the other methods in this class,
	stored as {'clef':{cleftable}, 'key:{keytable}', 'time:{timetable}'}
	
	Returns:
	  dictionary.  A dictionary of the form described above

	"""

        index = dict(list(list()))

	index.update({'clef':self.build_all_clefs()})
	index.update({'time':self.build_all_times()})
	index.update({'key':self.build_all_keys()})

	return index
