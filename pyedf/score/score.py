#! /usr/bin/python


import state as st
import numpy as np
import os
import re



class score(object):

	commentSymbol = '#'	# used for comments in state.annot
	lineSeparator = ','	# used as separators in the line
	states_dict = dict()

	def __init__(self, score_file=None, states=None, verbose=0):

		self.verbose = verbose
		self.states = []

		if score_file:

			if os.path.exists(score_file) == False:
				print "Score file %s does not exist." % (score_file)
				exit(0)

			self.states = self.load(score_file)
			if self.verbose > 0: print "score: score file '%s' found." % (score_file)
			if self.verbose == 2: print "score: the states", self.states

		else:
			if self.verbose: print "# score: no score file given."

		if np.iterable(states) :
			self.states = np.sort(states)
			self.interpret_states()


	def interpret_states(self):
		pass


	def isComment(self, line):

		line.strip(' ')

		if line[0] == self.commentSymbol:	# if line starts with the commentSymbol, it is a comment ..
			return True			# 					.. don't process it.

		else:
			return False	# else: split the line at separators.


	def load(self, score_file_name):

		score_file = open(score_file_name, 'r') 
		states = []

		for line in score_file:

			try:
				if self.isComment(line):
					continue

				x = line.split(self.lineSeparator)
				start = x[0].strip(' ')
				duration = x[1].strip(' ')
				annot = x[2].strip('\n').strip('\r').strip(' ')

				if duration == '':
					duration = '-1'
	
				states.append( st.state(start=start, duration=duration, annot=annot) )

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


	def append(self, new_state=None, start=None, duration=None, annot=None):

		if new_state == None:
			new_state = st.state(start=start, duration=duration, annot=annot)

		self.states.append(new_state)


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




if __name__ == "__main__":

	score_filename = '../../example/sample.csv'

	testscore = score(score_file=score_filename)

	print testscore
	



