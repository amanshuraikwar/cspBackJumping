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

	# print variablesCopy1
	# print varConsCopy1

	vi = 0
	solution = dict()
	while True:

		print "solution before: ", solution
		print "getting value of: ", ordering[vi]

		curVal = getValue(ordering[vi], solution, variablesCopy1, varConsCopy1[ordering[vi]])
		if curVal == False:
			print "domain: ", variablesCopy1[ordering[vi]], " of: ", ordering[vi], "must be empty"
			print "reviving domain"
			variablesCopy1[ordering[vi]] = variables[ordering[vi]][:]
			print "revivied domain of: ", ordering[vi], " is: ", variablesCopy1[ordering[vi]]
			solution.pop(ordering[vi-1])
			vi = vi - 1
			if(vi == -1):
				print "failed"
				break
			print "backtracking"
			continue

		solution[ordering[vi]] = curVal
		#variablesCopy1[ordering[vi]].remove(curVal)
		vi = vi + 1

		print "solution after: ", solution

		if vi == len(ordering):
			break

	print "Solution: ", solution
