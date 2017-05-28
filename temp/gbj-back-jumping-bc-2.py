import sys
import demjson
import json

def checkEqual(original, ins):
	if len(original) != len(ins):
		print "these are not equal"
		return False

	for i in range(len(original)):
		if ins[i] == '*':
			continue
		elif ins[i] != original[i]:
			print "these are not equal"
			return False

	print "these are equal"
	return True

def constraintSatisfaction(ins, constraint):
	relation = constraint['relation']
	for insI in relation:
		print "checking if this is equal: ",insI," ",ins
		if checkEqual(insI, ins):
			return True
	return False

def checkConsistency(curVal, curVar, ins, constraints):
	for cons in constraints:
		print "checking for this constraint: ",cons
		orderedIns = []
		for var in cons['scope']:
			if var == curVar:
				orderedIns.append(curVal)
			elif var in ins:
				orderedIns.append(ins[var])
			else:
				orderedIns.append('*')
		print "ordered instantiation: ",orderedIns
		if not(constraintSatisfaction(orderedIns, cons)):
			print "constraint not satisfied"
			return False
	print "all constraints satisfied"
	return True

def getValue(curVar, ins, domains, constraints):
	domain = domains[curVar]
	print "domain of: ",curVar," is: ",domain
	if not domain:
		return False
	
	vi = 0
	while vi < len(domain):
		print "1 loop domain of: ",curVar," is: ",domain
		curVal = domain[vi]
		domain.remove(curVal)
		print "2 loop domain of: ",curVar," is: ",domain
		print "checking for this value: ", curVal, " of: ", curVar
		if checkConsistency(curVal, curVar, ins, constraints):
			print "got consistent value: ",curVal
			return curVal
	print "no value consistent"
	return False

def checkConsistencyGbj(curVal, curVar, toCheckVal, toCheckVar, constraints, ordering):
	for cons in constraints:
		
		if (curVar not in cons['scope']) and (toCheckVar not in cons['scope']):
			continue

		print "checking for this constraint: ",cons
		orderedIns = []
		for var in cons['scope']:
			if var == curVar:
				orderedIns.append(curVal)
			elif var == toCheckVar:
				orderedIns.append(toCheckVal)
			else:
				orderedIns.append('*')
		print "ordered instantiation: ",orderedIns
		if not(constraintSatisfaction(orderedIns, cons)):
			print "constraint not satisfied between ", curVar, " and ", toCheckVar
			return False
	print "all constraints satisfied between ", curVar, " and ", toCheckVar
	return True

def getValueGbj(curVar, ins, domains, constraints, ordering, latesti):
	tempLatesti = latesti

	domain = domains[curVar]

	print "called getValueGbj for variable: ", curVar
	print "domain of: ",curVar," is: ",domain

	if not domain:
		print "empty domain for variable: ", curVar
		return False, tempLatesti
	
	vi = 0
	while vi < len(domain):
		consistentFlag = True
		print "before taking value from domain of: ",curVar," is: ",domain
		curVal = domain[vi]
		domain.remove(curVal)
		print "after taking value from domain of: ",curVar," is: ",domain
		print "checking for this value: ", curVal, " of: ", curVar
		
		for i in range(ordering.index(curVar)):
			if i > tempLatesti:
				tempLatesti = i
			if checkConsistencyGbj(curVal, curVar, ins[ordering[i]], ordering[i], constraints, ordering):
				print "value: ", curVal, " consistent with: ", ordering[i]
			else:
				print "value: ", curVal, " inconsistent with: ", ordering[i]
				consistentFlag = False
				break

		if consistentFlag:
			return curVal, (ordering.index(curVar) - 1)

	return False, tempLatesti

with open(str(sys.argv[1])) as json_data:
    data = json.load(json_data)

variables = data['variables']
temp = dict()
temp1 = dict()
for var in variables:
	temp[var['name']] = var['domain'][:]
	temp1[var['name']] = var['domain'][:]
variables = temp
variablesCopy1 = temp1

constraints = data['constraints']
varCons = dict()
for cons in constraints:
	scope = cons['scope']
	for var in scope:
		if var in varCons:
			varCons[var].append(cons.copy())
		else:
			varCons[var] = [cons.copy()]

ordering = data['ordering']

print "Solving: ", data['name']

print ""
print "[1] Gashnig's Backjumping"
print "[2] Graph Based Backjumping"
print "[3] Conflict-Directed Backjumping"
print ""

algoChoice = input("Your choice: ")

if algoChoice == 1:
	print ""
	print "--------- -----------"
	print "GASHNIG'S BACKJUMPING"
	print "--------- -----------"
	print ""

	#variablesCopy1 = variables.copy()
	varConsCopy1 = varCons.copy()

	latesti = dict()
	for var in variablesCopy1:
		latesti[var] = -1

	# print variablesCopy1
	# print varConsCopy1

	vi = 0
	solution = dict()
	while True:

		curVar = ordering[vi]

		print "solution at start of loop: ", solution
		print "getting value of variable: ", curVar

		curVal, gotLatesti = getValueGbj(curVar, solution, variablesCopy1, varConsCopy1[ordering[vi]], ordering, latesti[curVar])
		latesti[curVar] = gotLatesti

		print "new latesti of variable: ", curVar, " is: ", latesti[curVar]

		if curVal == False:
			print "domain: ", variablesCopy1[ordering[vi]], " of variable: ", curVar, "must be empty"
			

			#solution.pop(ordering[vi-1])

			if(latesti[curVar] == -1):
				print "failed"
				break

			for ti in range(latesti[curVar], vi+1):
				
				if ti != latesti[curVar]:
					print "reviving domain of variable: ", ordering[ti]
					variablesCopy1[ordering[ti]] = variables[ordering[ti]][:]
					print "revivied domain of: ", ordering[ti], " is: ", variablesCopy1[ordering[ti]]

				if ti != vi:
					solution.pop(ordering[ti])

			vi = latesti[curVar]
		
			print "backjumping"
			continue

		solution[curVar] = curVal
		
		vi = vi + 1

		print "solution at the end of loop: ", solution

		if vi == len(ordering):
			break

	print "Solution: ", solution