def getLatestAncestorIndex(curVar, inducedAncestors, ordering):

	print "getLatestAncestorIndex() for variable: ", curVar
	print "induced ancestors of variable: ", curVar, " are ",
	print inducedAncestors

	if ordering[0] == curVar:
		return -1

	latestAncestorIndex = None
	curVarIndex = ordering.index(curVar)

	for ancestor in inducedAncestors:
		curAncestorIndex = ordering.index(ancestor)

		if (curVarIndex > curAncestorIndex):
			if latestAncestorIndex == None:
				latestAncestorIndex = curAncestorIndex
			elif (curAncestorIndex > latestAncestorIndex):
				latestAncestorIndex = curAncestorIndex

	return latestAncestorIndex

def getValue(curVar, ins, domains, constraints):
	domain = domains[curVar]

	print "----"
	print "getValue() for variable: ", curVar
	print "domain of: ",curVar," is: ",domain
	if not domain:
		print "EMPTY DOMAIN"
		return False
	
	vi = 0
	while vi < len(domain):
		
		print "----"
		print "took first value out of: ", domain, 
		curVal = domain[vi]
		domain.remove(curVal)
		print "and now it is: ", domain

		print "checking for this value: ", curVal, " of: ", curVar
		
		if checkConsistency(curVal, curVar, ins, constraints):
			print curVal, " turns out to be a CONSISTENT value"
			return curVal
		else:
			print curVal, " is NOT CONSISTENT"
	print "no value consistent for variable: ", curVar
	return False

def checkConsistency(curVal, curVar, ins, constraints):
	for cons in constraints:

		orderedIns = []
		previousVariableExistsFlag = False

		for var in cons['scope']:
			if var == curVar:
				orderedIns.append(curVal)
			elif var in ins:
				orderedIns.append(ins[var])
				previousVariableExistsFlag = True
			else:
				orderedIns.append('*')

		if (not previousVariableExistsFlag):
			return True

		print "----"
		print "checking for this constraint: ",cons
		print "ordered instantiation: ",orderedIns

		if not(constraintSatisfaction(orderedIns, cons)):
			print "constraint not satisfied"
			return False

	print "all constraints satisfied"
	return True

def constraintSatisfaction(ins, constraint):
	relation = constraint['relation']
	for reli in relation:
		print "checking if these are equal: ", reli, " ", ins
		if checkEqual(reli, ins):
			return True
	return False

def checkEqual(original, ins):
	if len(original) != len(ins):
		print "these are not equal"
		return False

	for i in range(len(original)):
		if ins[i] == '*':
			continue
		elif ins[i] != original[i]:
			print "these are NOT EQUAL"
			return False

	print "these are EQUAL"
	return True