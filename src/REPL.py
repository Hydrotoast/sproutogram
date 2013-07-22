from SimpleCV import *
import Preprocess

class REPL(object):
	"""Read-Eval-Print-Loop for interacting with the BVSproutExtractor."""
	def __init__(self):
		self.display = Display()

	def run(self, img):
		self.img = img

		done = False
		while not done:
			line = raw_input('Enter Parameters (cannyMin,cannyMax,dilateCount): ')

			# Reload preprocessor before obtaining frame
			reload(Preprocess)
			frame = self.parseLine(line)

			# Break if no frame returned
			if not frame:
				break

			# Display and save the frame
			self.display = frame.show()
			frame.save('data/output/result.jpg')
		self.display.quit()

	def parseLine(self, line):
		"""Returns a frame for the given parameters"""
		if line == 'done':
			return False
		data = line.split(',')
		if len(data) == 3:
			data = map(int, data)
			cannyMin, cannyMax, dilationCount = data
			frame = Preprocess.approach(self.img, cannyMin, cannyMax, dilationCount)
		else:
			frame = Preprocess.approach(self.img)
		return frame
