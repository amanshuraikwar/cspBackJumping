import sys
import demjson
import json
import func

# reading json from input file
with open(str(sys.argv[1])) as json_data:
    data = json.load(json_data)

# getting array of variables
originalVariables = data['variables']

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
print "----- ----- -----------"
print "GRAPH BASED BACKJUMPING"
print "----- ----- -----------"
print ""

# varCons is dict {'X1':[constriant1, constraint2, constraint3...], 
# 'X2':[constriant1, constraint2, constraint3...], ...}
varConsCopy1 = varCons.copy()
ancestors = dict()

# finding ancestors for each variable
for variable in originalVariables:
	curVar = variable['name']
	constraints = varConsCopy1[curVar]
	temp = set()
	for contraint in constraints:
		scope = contraint['scope']
		for var in scope:

			#rejecting variables with ordering index >= curVar
			if ordering.index(var) >= ordering.index(curVar):
				continue
			temp.add(var)
	ancestors[variable['name']] = list(temp)

vi = 0
# solution is a dict {'X1' : 'r', 'X2' : 'g', ...}
solution = dict()
inducedAncestors = ancestors[ordering[vi]]

# looping until we reach end of ordering array or empty domain for first 
# variable in ordering
while True:
	curVar = ordering[vi]

	print "----"
	print "solution at start of loop: ", solution

	print "----"
	print "getting value of variable: ", curVar
	print "vi: ", str(vi)
	print "induced ancestors: ", inducedAncestors

	curVal = func.getValue(curVar, solution, variablesCopy1, 
		varConsCopy1[curVar])

	if curVal == False:
		
		print "----"
		print "no value consistent got for var: ", curVar
		print "domain of var: ", curVar, " is: ", variablesCopy1[curVar]

		variablesCopy1[curVar] = variables[curVar][:]
		print "revivied domain of: ", curVar, " is: ", variablesCopy1[curVar]
		
		print "getting latest ancestor of variable: ", curVar

		latestAncestorIndex = func.getLatestAncestorIndex(curVar, 
			inducedAncestors, ordering)

		print "got latest ancestor index for variable: ", curVar, " is ",
		print latestAncestorIndex

		if latestAncestorIndex == None:
			print "failed"
			break
			

		if latestAncestorIndex == -1:
			print "failed"
			break

		for x in ancestors[curVar]:
			if (x not in inducedAncestors) and (x != curVar):
				inducedAncestors.append(x)

		for i in range(latestAncestorIndex, vi):
			if i != latestAncestorIndex:
				variablesCopy1[ordering[i]] = variables[ordering[i]][:]
				print "reviving domain of: ", ordering[i]
				print " it is: ", variablesCopy1[ordering[i]]
			solution.pop(ordering[i])

		print "backjumping from variable: ", curVar, " to variable: ",
		print ordering[latestAncestorIndex]
		print "now solution is: ", solution
		vi = latestAncestorIndex

	else:
		vi = vi + 1

		solution[curVar] = curVal

		if vi == len(ordering):
			break

		inducedAncestors = ancestors[ordering[vi]]

print "Solution: ", solution