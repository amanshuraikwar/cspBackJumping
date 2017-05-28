class CspState:
	
	def __init__(self, variables, curVar, originalDomains, curDomains, deadEndFlag, culpritVar):
		self.variables = variables
		self.curVar = curVar
		self.originalDomains = originalDomains
		self.curDomains = curDomains
		self.deadEndFlag = deadEndFlag
		self.culpritVar = culpritVar

		self.evaluate()

	def evaluate():
		self.evaluatedDomains = dict()
		
		self.pastVals = dict()
		self.futureVals = dict()

		for var in self.variables:
			divIndex = len(self.originalDomains[var]) - len(self.curDomains[var]) - 1
			
			pastValsTemp = []
			futureValsTemp = []

			if var == curVar:
				self.curVal = originalDomains[var][divIndex]
				for i in range(len(originalDomains[var])):
					if i < divIndex:
						pastValsTemp.append(originalDomains[var][i])
					elif i > divIndex:
						futureValsTemp.append(originalDomains[var][i])
			else:
				for i in range(len(originalDomains[var])):
					if(i <= divIndex):
						pastValsTemp.append(originalDomains[var][i])
					else:
						futureValsTemp.append(originalDomains[var][i])

			self.pastVals[var] = pastValsTemp
			self.futureVals[var] = futureValsTemp