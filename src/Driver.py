from SimpleCV import *

from REPL import REPL
from Extraction import *

class Driver(object):
	def extractMonoBead(self, img):
		extractor = HLSGExtractor(img)
		hlsgs = extractor.extract()
		for hlsg in hlsgs:
			print hlsg

	def runExtractions(self):
		monoBead = Image('../data/samples/mono.jpg')
		monoBead = monoBead.resize(w=800)
		self.extractMonoBead(monoBead)

def main():
	repl = REPL()
	img = Image('../data/samples/mono.jpg')
	img = img.resize(w=800)
	repl.run(img)

if __name__ == '__main__':
	driver = Driver()
	driver.runExtractions()
