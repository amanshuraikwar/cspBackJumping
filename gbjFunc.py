import func

def getValueGbj(curVar, ins, domains, constraints, ordering, latesti):
	tempLatesti = latesti

	domain = domains[curVar]

	print "----"
	print "getValue() for variable: ", curVar
	print "domain of: ",curVar," is: ",domain

	print "called getValueGbj for variable: ", curVar
	print "domain of: ",curVar," is: ",domain

	if not domain:
		print "EMPTY DOMAIN"
		return False, tempLatesti
	
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
			if i > tempLatesti:
				tempLatesti = i
			if checkConsistencyGbj(curVal, curVar, ins[ordering[i]],
				ordering[i], constraints, ordering):
				print "value: ", curVal, " CONSISTENT with: ", ordering[i]
			else:
				print "value: ", curVal, " INCONSISTENT with: ", ordering[i]
				consistentFlag = False
				break

		if consistentFlag:
			return curVal, (ordering.index(curVar) - 1)

	return False, tempLatesti

def checkConsistencyGbj(curVal, curVar, toCheckVal, toCheckVar, constraints,
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
			print toCheckVar
			return False
			
	print "all constraints satisfied between ", curVar, " and ", toCheckVar
	return True