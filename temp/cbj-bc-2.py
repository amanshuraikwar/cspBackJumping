import sys
import demjson
import json
import cbjFunc as func

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
func.ordering = ordering

print "Solving: ", data['name']

print ""
print "-------- ----------- -----------"
print "CONFLICT DIRECTECTED BACKJUMPING"
print "-------- ----------- -----------"
print ""

# varCons is dict {'X1':[constriant1, constraint2, constraint3...], 
# 'X2':[constriant1, constraint2, constraint3...], ...}
varConsCopy1 = varCons.copy()

for variable in ordering:
	print "original ", varConsCopy1[variable]
	varConsCopy1[variable] = func.sortConstraints(varConsCopy1[variable],
		ordering)
	print "sorted ", varConsCopy1[variable]

vi = 0
# solution is a dict {'X1' : 'r', 'X2' : 'g', ...}
solution = dict()
jumpBackSet = set()

# looping until we reach end of ordering array or empty domain for first 
# variable in ordering
while True:
	curVar = ordering[vi]

	print "----"
	print "solution at start of loop: ", solution

	print "----"
	print "getting value of variable: ", curVar
	print "vi: ", str(vi)
	print "jump back set: ", jumpBackSet

	curVal, jumpBackSetTemp = func.getValueCbj(curVar, solution,
		variablesCopy1, varConsCopy1[curVar], ordering)

	print "got jump back set: ", jumpBackSetTemp

	if curVal == False:

		print "----"
		print "no value consistent got for var: ", curVar
		print "domain of var: ", curVar, " is: ", variablesCopy1[curVar]

		jumpBackSet = jumpBackSet | jumpBackSetTemp

		if len(jumpBackSet) == 0:
			print "failed"
			break

		latestAncestorIndex = func.getLatestAncestorIndex(curVar,
			list(jumpBackSet), ordering)

		print "got latest ancestor index for variable: ", curVar, " is ", 
		print latestAncestorIndex

		for i in range(latestAncestorIndex, vi+1):
			
			if i != latestAncestorIndex:
				variablesCopy1[ordering[i]] = variables[ordering[i]][:]
				print "reviving domain of: ", ordering[i]
				print " it is: ", variablesCopy1[ordering[i]]

			if i != (vi):
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

		jumpBackSet = set()

print "Solution: ", solution