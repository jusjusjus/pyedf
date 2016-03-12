#! /usr/bin/python


import state as st
import numpy as np
import re



class score(object):

	commentSymbol = '#'	# used for comments in state.annot
	annotSeparator = '_'	# used as separators in state.annot
	lineSeparator = ','	# used as separators in the line
	states_dict = dict()
	interpreter = dict()
	statetypes = 0

	def __init__(self, score_file=None, states=None, verbose=0):

		self.add_state('epoch', score.interpret_epoch)
		self.add_state('segment', score.interpret_segment)
		self.add_state('event', score.interpret_event)

		self.verbose = verbose
		self.declare()

		if score_file:
			states = self.load(score_file)
			if self.verbose > 0: print "score: score file '%s' found." % (score_file)
			if self.verbose == 2: print states
		else:
			if self.verbose: print "# score: no score file given."

		if not states == None:
			states = np.sort(states)
			self.clean_states(states)
			self.interpret_states()


	def add_state(self, annotator, function):
		self.interpreter[annotator] = function
		self.states_dict[annotator] = self.statetypes
		self.statetypes += 1


	def declare(self):

		self.states = []	# contains all recognizable states
		self.trash  = []	# contains states that could not be evaluated
		self.epochs = dict()	# contains 'epoch' states
		self.segments = dict()	# contains 'segments' states
		self.events = []	# contains events, no duration


	def isComment(self, line, separator):

		if line[0] == self.commentSymbol:	# if line starts with the commentSymbol, it is a comment:
			return None			# ... don't process it.
		else: return line.split(separator)	# else: split the line at separators.


	def load(self, score_file_name):

		score_file, states = open(score_file_name, 'r'), []

		for line in score_file:

			try:
				x = self.isComment(line, self.lineSeparator)
				if x == None: continue
	
				if x[1] == '':		x[1] = '-1'
				if x[2][-1] == '\n':	x[2] = x[2][:-1]
	
				states.append( st.state(start=x[0], duration=x[1], annot=x[2]) )

			except:
				if self.verbose > 0: print "# line not readable:", line


		score_file.close()

		return states


	def save(self, score_file_name):

		print "# opening", score_file_name, "to write ..."
		score_file = open(score_file_name, 'w')
		string = '# start, duration, annotation\n'+self.__str__()
		score_file.write(string)
		score_file.close()


	def clean_states(self, states):

		if not states == None:
			self.states, self.trash = [], []
	
		for state in states:

			annot = state.annot.split(self.annotSeparator)

			if type(self).states_dict.has_key(annot[0]):
				self.states.append(state)

			else:
				self.trash.append(state)


	def interpret_segment(self, state, annot):

		epoch_id = annot[1]					# identify of the Epoch/this particular trial

		if not self.segments.has_key(epoch_id):
			self.segments[epoch_id] = []
	
		self.segments[epoch_id].append(state)			# state contains start and duration
		

	def interpret_epoch(self, state, annot):

		epoch_id = annot[1]					# identify of the Epoch/this particular trial
		self.epochs[epoch_id] = state			 	# stores state and administration group


	def interpret_event(self, state, annot):

		event_descriptor = annot[1:]					# identify of the Epoch/this particular trial
		self.events.append([state, event_descriptor])			 	# stores event time and event description


	def interpret_state(self, state):

		annot = self.isComment(state.annot, self.annotSeparator)	# splits the state if its not a comment.  Else: returns None
		if not annot == None: # it's not a comment?  continue

			recognized = False
			for key in self.interpreter:#.keys():

				if re.search(key, state.annot):
					self.interpreter[key](self, state, annot)
					recognized = True
					break

	
			if not recognized:
				print "# edf.score: could not process", state


	def interpret_states(self):

		for state in self.states:
			self.interpret_state(state)


	def append(self, new_state=None, start=None, duration=None, annot=None):

		if new_state == None:
			new_state = st.state(start=start, duration=duration, annot=annot)

		self.states.append(new_state)
		self.interpret_state(new_state)



	def __str__(self):

		return '\n'.join([str(state) for state in self.states])



	def select_by_function(self, function, **kwargs):

		selection = []
		for state in self.states:
			
			if function(state, **kwargs):
				selection.append(state)

		score_select = object.__new__(type(self))
		score_select.__init__(states=selection)
		return score_select
	


	def intersect(self, other_score):

		section = []
		for state in self.states:
	
			for other in other_score.states:

				sect_j = state.intersect(other, annot=state.annot)

				if not sect_j == None:
					section.append(sect_j)
	
		return type(self)(states=section)







