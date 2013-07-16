from SimpleCV import *
from REPL import REPL

def main():
	repl = REPL()
	img = Image('data/samples/mono.jpg')
	img = img.resize(w=510)
	repl.run(img)

if __name__ == '__main__':
	main()
