class CspState:
	
	def __init__(self, variables, curVar, originalDomains, curDomains, deadEndFlag, culpritVar):
		self.variables = variables
		self.curVar = curVar
		self.originalDomains = originalDomains
		self.curDomains = curDomains
		self.deadEndFlag = deadEndFlag
		self.culpritVar = culpritVar

		self.evaluate()

	def evaluate(self):
		self.evaluatedDomains = dict()
		
		self.pastVals = dict()
		self.futureVals = dict()
		self.curVals = dict()

		for var in self.variables:
			divIndex = len(self.originalDomains[var]) - len(self.curDomains[var]) - 1
			
			pastValsTemp = []
			futureValsTemp = []

			# if var == self.curVar:
			if True:
				self.curVals[var] = self.originalDomains[var][divIndex]
				for i in range(len(self.originalDomains[var])):
					if i < divIndex:
						pastValsTemp.append(self.originalDomains[var][i])
					elif i > divIndex:
						futureValsTemp.append(self.originalDomains[var][i])
			else:
				for i in range(len(self.originalDomains[var])):
					if(i <= divIndex):
						pastValsTemp.append(self.originalDomains[var][i])
					else:
						futureValsTemp.append(self.originalDomains[var][i])

			self.pastVals[var] = pastValsTemp
			self.futureVals[var] = futureValsTemp