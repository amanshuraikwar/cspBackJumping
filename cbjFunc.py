import func

ordering = []

def compare(cons1, cons2):
	scope1 = set(cons1['scope'])
	scope2 = set(cons2['scope'])
	uncommonScope1 = scope1 - scope2
	uncommonScope2 = scope2 - scope1
	latestVar = None
	returnValue = None

	for var in list(uncommonScope1):
		if latestVar == None:
			latestVar = var
			returnValue = 1
		elif ordering.index(var) > ordering.index(latestVar):
			latestVar = var
			returnValue = 1

	for var in list(uncommonScope2):
		if latestVar == None:
			latestVar = var
			returnValue = -1
		elif ordering.index(var) > ordering.index(latestVar):
			latestVar = var
			returnValue = -1

	return returnValue

def sortConstraints(constraints, ordering):
	return sorted(constraints, cmp=compare, reverse=True)

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


def getValueCbj(curVar, ins, domains, constraints, ordering):
	
	domain = domains[curVar]

	print "----"
	print "getValue() for variable: ", curVar
	print "domain of: ",curVar," is: ",domain

	scopesOfConflCons = set()

	if not domain:
		print "EMPTY DOMAIN"
		return False, scopesOfConflCons
	
	vi = 0
	while vi < len(domain):
		consistentFlag = True
		
		print "----"
		print "took first value out of: ", domain, 
		curVal = domain[vi]
		domain.remove(curVal)
		print "and now it is: ", domain
		
		print "checking for this value: ", curVal, " of: ", curVar

		for i in range(ordering.index(curVar)):
			
			consistentFlagTemp, latestConstraint = checkConsistencyCbj(
				curVal, curVar, ins[ordering[i]], ordering[i], constraints,
				ordering)

			if consistentFlagTemp:
				print "value: ", curVal, " CONSISTENT with: ", ordering[i]
			else:
				print "value: ", curVal, " INCONSISTENT with: ", ordering[i]
				consistentFlag = False
				scopesOfConflCons = (
					scopesOfConflCons | set(latestConstraint['scope'])
					) - set([curVar])
				break

		if consistentFlag:
			return curVal, None

	return False, scopesOfConflCons

def checkConsistencyCbj(curVal, curVar, toCheckVal, toCheckVar, constraints,
	ordering):

	for cons in constraints:

		if not ((curVar in cons['scope']) and (toCheckVar in cons['scope'])):
			continue

		print "----"
		print "checking for this constraint: ", cons

		orderedIns = []
		for var in cons['scope']:
			if var == curVar:
				orderedIns.append(curVal)
			elif var == toCheckVar:
				orderedIns.append(toCheckVal)
			else:
				orderedIns.append('*')

		print "ordered instantiation: ",orderedIns
		if not(func.constraintSatisfaction(orderedIns, cons)):
			print "constraint not satisfied between ", curVar, " and ",
			print cons
			return False, cons

	print "all constraints satisfied between ", curVar, " and ", toCheckVar
	return True, None