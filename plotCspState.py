import Tkinter as tk
import cspState

import random
import time

class CspStateDrawer:
	
	def nextButtonOnClick(self):
		if self.currentStateIndex != (self.totalSates - 1):
			self.currentStateIndex = self.currentStateIndex + 1
			self.draw(self.cspStates[self.currentStateIndex])
			self.master.update()

	def previousButtonOnClick(self):
		if self.currentStateIndex != 0:
			self.currentStateIndex = self.currentStateIndex - 1
			self.draw(self.cspStates[self.currentStateIndex])
			self.master.update()

	def __init__(self, canvas_width, canvas_height, states):
		self.master = tk.Tk()
		self.canvasWidth = 1000
		self.canvasHeight = 800
		self.w = tk.Canvas(self.master, 
		    	width=self.canvasWidth,
		    	height=self.canvasHeight)
		self.cspStates = states
		self.totalSates = len(states)

		nextButton = tk.Button(self.master, text="Next", command = self.nextButtonOnClick)
		previousButton = tk.Button(self.master, text="Previous", command = self.previousButtonOnClick)

		self.w.pack()
		nextButton.pack()
		previousButton.pack()

		self.currentStateIndex = 0
		self.draw(self.cspStates[self.currentStateIndex])

		# self.master.update_idletasks()
		# self.master.update()
		self.master.mainloop()

	def draw(self, state):
		self.w.delete("all")
		self.w.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill="#ffffff")

		varNo = len(state.variables)
		diameterCircle = 50
		space = 50
		circleWidth = 3
		pastValuesColor = "#212121"
		currentValueColor = "#03A9F4"
		futureValueColor = "#607D8B"
		culpritVariableColor = "#F44336"
		normalVariableColor = "#212121"
		mostRecentCurrentValueColor = "#4CAF50"

		start = 0

		#printing variables
		for i in range(len(state.variables)):
			curVar = state.variables[i]
			
			tempTextColor = normalVariableColor

			if state.deadEndFlag:
				if curVar == state.culpritVar:
					tempTextColor = culpritVariableColor

			self.w.create_oval(space, i*diameterCircle+(i+1)*space, space+diameterCircle,
				(i+1)*diameterCircle+(i+1)*space, width=circleWidth, outline=tempTextColor)

			self.w.create_text(space+25, i*diameterCircle+(i+1)*space+25, fill=tempTextColor,
				font="Times 15 bold",text=curVar)

			temp = 1
			for val in state.pastVals[curVar]:
				
				self.w.create_text(space+(diameterCircle+space)*temp+25,
					i*diameterCircle+(i+1)*space+25, fill=pastValuesColor, font="Times 15 bold",
					text=val)

				temp = temp + 1

			if curVar == state.curVar:
				
				tempColor = mostRecentCurrentValueColor
				if state.deadEndFlag:
					tempColor = culpritVariableColor

				self.w.create_text(space+(diameterCircle+space)*temp+25,
					i*diameterCircle+(i+1)*space+25, fill=tempColor,
					font="Times 15 bold", text=state.curVals[curVar])

				self.w.create_oval(space+(diameterCircle+space)*temp+10,
					i*diameterCircle+(i+1)*space+10,
					 space+(diameterCircle+space)*temp + diameterCircle - 10,
					i*diameterCircle+(i+1)*space + diameterCircle - 10,
					width=2, outline=tempColor)

				temp = temp + 1
			else:
				if i < state.variables.index(state.curVar):
					self.w.create_text(space+(diameterCircle+space)*temp+25,
						i*diameterCircle+(i+1)*space+25, fill=currentValueColor,
						font="Times 15 bold", text=state.curVals[curVar])
					temp = temp + 1

			for val in state.futureVals[curVar]:
				self.w.create_text(space+(diameterCircle+space)*temp+25,
					i*diameterCircle+(i+1)*space+25, fill=futureValueColor,
					font="Times 15 bold",text=val)
				temp = temp + 1

# drawer = cspStateDrawer(500, 500, [cspState.CspState(['X1', 'X2'], 'X2', {'X1': ['r', 'g', 'b'], 'X2': ['r', 'g', 'b']},
# 			{'X1': ['b'], 'X2': ['b']}, True, 'X1'), cspState.CspState(['X1', 'X2'], 'X1', {'X1': ['r', 'g', 'b'], 'X2': ['r', 'g', 'b']},
# 			{'X1': ['b'], 'X2': ['b']}, True, 'X1')])