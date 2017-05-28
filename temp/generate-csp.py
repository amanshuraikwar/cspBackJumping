#for command line arguments
import sys

def getNQueensRelation(row1, row2, n):
	relation = []
	for q1i in range(1, n+1):
		for q2i in range(1, n+1):
			if q1i == q2i:
				continue
			elif abs(q1i-q2i) == abs(row1-row2):
				continue
			else:
				relation.append([""+str(q1i)+"", ""+str(q2i)+""])
	return relation

def getNMapColouringRelation(noOfColors):
	relation = []
	for n1i in range(1, noOfColors+1):
		for n2i in range(1, noOfColors+1):
			if n1i != n2i:
				relation.append(["C" + str(n1i), "C" + str(n2i)])
	return relation

cspChoice = int(sys.argv[1])

cspJson = "{\n"

if cspChoice == 0:
	#n-queens
	nameOfProblem =  sys.argv[2]
	noOfQueens = int(sys.argv[3])

	# ordering = raw_input("Ordering (node index separated by space): ")
	# ordering = ordering.split(" ")

	cspJson = cspJson + "\t'name' : '" + nameOfProblem + "',\n\n"
	cspJson = cspJson + "\t'variables' : \n"
	cspJson = cspJson + "\t\t[\n"

	for ni in range(noOfQueens):

		cspJson = cspJson + "\t\t\t{\n"
		cspJson = cspJson + "\t\t\t\t'name' : 'X" + str(ni+1) + "',\n"
		cspJson = cspJson + "\t\t\t\t'domain' : ["

		for di in range(noOfQueens):

			cspJson =  cspJson + "'" + str(di+1) + "'"

			if di != (noOfQueens - 1):

				cspJson = cspJson + ", "

		cspJson = cspJson + "]\n"

		if ni == (noOfQueens - 1):

			cspJson = cspJson + "\t\t\t}\n"

		else:

			cspJson = cspJson + "\t\t\t},\n\n"

	cspJson = cspJson + "\t\t],\n\n"
	cspJson = cspJson + "\t'constraints' : \n"
	cspJson = cspJson + "\t\t[\n"

	for r1i in range(1, noOfQueens+1):
		for r2i in range(r1i+1, noOfQueens+1):
			
			cspJson = cspJson + "\t\t\t{\n"		
			cspJson = cspJson + "\t\t\t\t'scope' : ['X" + str(r1i) +"', 'X" + str(r2i) + "'],\n"
			cspJson = cspJson + "\t\t\t\t'relation' : " + str(getNQueensRelation(r1i, r2i, noOfQueens)) + "\n"

			if (r1i*r2i) == ((noOfQueens-1)*noOfQueens):

				cspJson = cspJson + "\t\t\t}\n"

			else:

				cspJson = cspJson + "\t\t\t},\n\n"

	cspJson = cspJson + "\t\t],\n\n"
	cspJson = cspJson + "\t'ordering' : ["

	for oi in range(noOfQueens):
		
		cspJson = cspJson + "'X" + str(oi+1) + "'"

		if oi != (noOfQueens - 1):

			cspJson = cspJson + ", "

	cspJson = cspJson + "]\n"

elif cspChoice == 1:
	#n-map-colouring
	nameOfProblem =  raw_input("Name of problem: ")
	
	noOfCountries = input("No of countries: ")
	noOfColors = input("No of colors: ")

	ordering = raw_input("Ordering (node index separated by space): ")
	ordering = ordering.split(" ")

	connectedCountries = raw_input("Connected countries\ncountries separated by ',' and pair separated by ';': ")
	connectedCountries = connectedCountries.split(";")

	temp = []
	for ci in range(len(connectedCountries)):
		temp1 = connectedCountries[ci].split(",")
		temp.append([int(temp1[0]), int(temp1[1])])
	connectedCountries = temp[:]

	cspJson = cspJson + "\tname : " + nameOfProblem + ",\n\n"
	cspJson = cspJson + "\tvariables : \n"
	cspJson = cspJson + "\t\t[\n"

	for ni in range(noOfCountries):

		cspJson = cspJson + "\t\t\t{\n"
		cspJson = cspJson + "\t\t\t\tname : X" + str(ni+1) + ",\n"
		cspJson = cspJson + "\t\t\t\tdomain : ["

		for di in range(noOfColors):

			cspJson = cspJson + "C" + str(di+1)

			if di != (noOfColors - 1):

				cspJson = cspJson + ", "

		cspJson = cspJson + "]\n"

		if ni == (noOfCountries - 1):

			cspJson = cspJson + "\t\t\t}\n"

		else:

			cspJson = cspJson + "\t\t\t},\n\n"

	cspJson = cspJson + "\t\t],\n\n"
	cspJson = cspJson + "\tconstraints : \n"
	cspJson = cspJson + "\t\t[\n"

	for ci in range(len(connectedCountries)):
			
		cspJson = cspJson + "\t\t\t{\n"
		cspJson = cspJson + "\t\t\t\tscope : [X" + str(connectedCountries[ci][0]) +", X" + str(connectedCountries[ci][1]) + "],\n"
		cspJson = cspJson + "\t\t\t\trelation : " + str(getNMapColouringRelation(noOfColors)) + "\n"

		if ni == (len(connectedCountries) - 1):

			cspJson = cspJson + "\t\t\t}\n"

		else:

			cspJson = cspJson + "\t\t\t},\n\n"

	cspJson = cspJson + "\t\t],\n\n"
	cspJson = cspJson + "\tordering : ["

	for oi in range(noOfCountries):
		
		cspJson = cspJson + "X" + ordering[oi]

		if oi != (noOfCountries - 1):

			cspJson = cspJson + ", "

	cspJson = cspJson + "]\n"

elif cspChoice == 2:
	#crypto-arithematic
	nameOfProblem =  raw_input("Name of problem: ")

	print "inputs should be fully upper case or fully lower case"
	inputWords = raw_input("Input words to be added (separated by spaces): ")
	inputWords = inputWords.split(" ")
	temp = []
	for wi in range(len(inputWords)):
		temp.append(list(inputWords[wi]))
	inputWords = temp[:]
	sumOfWords = raw_input("Sum of input words: ")
	sumOfWords = list(sumOfWords)

	totalWords = inputWords.append(sumOfWords)

	cspJson = cspJson + "\tname : " + nameOfProblem + ",\n\n"
	cspJson = cspJson + "\tvariables : \n"
	cspJson = cspJson + "\t\t[\n"



	variables = []
	for wi in range(len(totalWords)):
		for ch in totalWords[wi]:
			if ch not in variables:
				variables.append(ch)

	for ni in range(len(variables)):

		cspJson = cspJson + "\t\t\t{\n"
		cspJson = cspJson + "\t\t\t\tname : " + variables[ni] + ",\n"
		cspJson = cspJson + "\t\t\t\tdomain : ["

		for di in range(10):

			cspJson = cspJson + str(di)

			if di != (10 - 1):

				cspJson = cspJson + ", "

		cspJson = cspJson + "]\n"

		if ni == (len(variables) - 1):

			cspJson = cspJson + "\t\t\t}\n"

		else:

			cspJson = cspJson + "\t\t\t},\n\n"

	cspJson = cspJson + "\t\t],\n\n"
	cspJson = cspJson + "\tconstraints : \n"
	cspJson = cspJson + "\t\t[\n"

cspJson = cspJson + "}"
print cspJson