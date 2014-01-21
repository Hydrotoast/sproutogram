from SimpleCV import *

from Extraction import *

import os

class REPL(object):
    """Read-Eval-Print-Loop for interacting with the BVSproutExtractor."""
    def __init__(self):
        self.display = Display()

    def run(self, img, filename):
        self.img = img

        done = False
        while not done:
            line = raw_input('>> ')

            # Reload preprocessor before obtaining frame
            reload(Preprocess)
            frame = self.parseLine(line)

            # Break if no frame returned
            if not frame:
                break

            # Display and save the frame
            self.display = frame.show()
            frame.save(os.path.join('../data/output', filename))

        self.display.quit()

    def parseLine(self, line):
        """Returns a frame for the given parameters."""
        if line == 'done':
            return False
        extractor = HLSGExtractor(self.img)
        hlsgs = extractor.extract()
        frame = hlsgs
        return frame
