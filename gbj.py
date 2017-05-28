import sys
import json
import gbjFunc as func
import cspState as cs
import plotCspState as pcs

# reading json from input file
with open(str(sys.argv[1])) as json_data:
    data = json.load(json_data)

# getting array of variables
originalVariables = data['variables']

# forming a dict of {variable : domain, ...}
variables = data['variables']
temp = dict()
temp1 = dict()
for var in variables:
	temp[var['name']] = var['domain'][:]
	temp1[var['name']] = var['domain'][:]
variables = temp
variablesCopy1 = temp1

# forming a dictionary of {variable : [constraints], ...}
constraints = data['constraints']
varCons = dict()
for cons in constraints:
	scope = cons['scope']
	for var in scope:
		if var in varCons:
			varCons[var].append(cons.copy())
		else:
			varCons[var] = [cons.copy()]

# ordering of variables
ordering = data['ordering']
func.ordering = ordering

print "Solving: ", data['name']

print ""
print "--------- ---- -------"
print "GASHNIG'S BACK JUMPING"
print "--------- ---- -------"
print ""

varConsCopy1 = varCons.copy()

# initialising latest i
latesti = dict()
for var in variablesCopy1:
	latesti[var] = -1

vi = 0
# solution is a dict {'X1' : 'r', 'X2' : 'g', ...}
solution = dict()

cspStates = []

failFlag = False
# looping until we reach end of ordering array or empty domain for first 
# variable in ordering

while True:
	curVar = ordering[vi]

	print "----"
	print "solution at start of loop: ", solution

	print "----"
	print "getting value of variable: ", curVar
	print "vi: ", str(vi)
	print "latesti: ", latesti[curVar]

	curVal, gotLatesti = func.getValueGbj(curVar, solution, variablesCopy1,
		varConsCopy1[ordering[vi]], ordering, latesti[curVar])
	latesti[curVar] = gotLatesti

	print "got latesti: ", latesti[curVar]

	print "new latesti of variable: ", curVar, " is: ", latesti[curVar]

	if curVal == False:

		print "----"
		print "no value consistent got for var: ", curVar
		print "domain of var: ", curVar, " is: ", variablesCopy1[curVar]
		
		if latesti[curVar] == -1:
			print "failed"
			failFlag = True
			break

		cspStates.append(cs.CspState(ordering, curVar,
			variables, variablesCopy1, True, ordering[latesti[curVar]]))

		for ti in range(latesti[curVar], vi+1):
			
			if ti != latesti[curVar]:
				variablesCopy1[ordering[ti]] = variables[ordering[ti]][:]
				
				print "reviving domain of: ", ordering[ti]
				print " it is: ", variablesCopy1[ordering[ti]]

			if ti != vi:
				solution.pop(ordering[ti])

		vi = latesti[curVar]

		print "backjumping from variable: ", curVar, " to variable: ", 
		print ordering[vi]
		print "now solution is: ", solution

	else:

		solution[curVar] = curVal
		
		vi = vi + 1

		cspStates.append(cs.CspState(ordering, curVar,
			variables, variablesCopy1, False, ''))

		if vi == len(ordering):
			break

if not failFlag:
	print "Solution: ", solution

gui = pcs.CspStateDrawer(800, 800, cspStates)
	