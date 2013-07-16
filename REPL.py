from SimpleCV import *
import Preprocess

class REPL(object):
	"""Read-Eval-Print-Loop for interacting with the BVSproutExtractor."""
	def __init__(self):
		self.display = Display()

	def run(self, img):
		done = False
		while not done:
			line = raw_input('Enter Parameters (cannyMin,cannyMax,dilateCount): ')
			reload(Preprocess)
			if line == 'done':
				break
			data = line.split(',')
			if len(data) == 3:
				data = map(int, data)
				cannyMin, cannyMax, dilationCount = data
				frame = Preprocess.approach(img, cannyMin, cannyMax, dilationCount)
			else:
				frame = Preprocess.approach(img)
			self.display = frame.show()
			frame.save('data/output/result.jpg')
		self.display.quit()
