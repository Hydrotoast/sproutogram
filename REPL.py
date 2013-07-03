from SimpleCV import *
from Preprocess import *

class REPL(object):
"""Read-Eval-Print-Loop for interacting with the BVSproutExtractor."""
	def __init__(self):
		self.display = Display()

	def run(self, img):
		done = False
		while not done:
			line = raw_input('Enter Parameters (cannyMin,cannyMax,dilateCount): ')
			if line == 'done':
				break
			cannyMin, cannyMax, dilationCount = map(int, line.split(','))
			frame = approach1(img, cannyMin, cannyMax, dilationCount)
			self.display = frame.show()
		self.display.quit()
