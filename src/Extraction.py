from math import *

from SimpleCV import *

from SetForest import *
from SproutSegmentation import *
from Morphology import *

class NoBeadException(Exception):
    pass

class ExtractorBase(object):
    def __init__(self, img):
        self.img = img

    def preprocess(self):
        """Preprocesses a target image before feature extraction is
        performed."""
        pass

    def extract(self):
        """
        Extracts a homogenous list of a single feature from a target image. The
        template first applies preprocessing steps and follows with feature
        extraction.

        Returns:
            A homogenous list of a single feature.
        """
        pass

class BeadExtractor(ExtractorBase):
    """
    Extracts bead features from a target image using a circular hough
    transformation to find the center and radius of the bead.
    """
    def __init__(self, img):
        super(BeadExtractor, self).__init__(img)

    def extractCircles(self, canny=164, thresh=128, distance=512):
        """
        Extracts circle features from the target image using the circular
        hough transform. Use this instead of the default
        ``image.findCircles()`` algorithm because a maximum radius is
        supplied here.

        :param canny: upper threshold passed to the canny edge detector
        :param thresh: accumulator threshold for detecting circles
        :param distance: the minimum distance between two bead origins
        :returns: a list of circle features from the target image
        :rtype: [Circle]

        Relative Parameters
        -------------------

        It is recommended that the `distance` parameter is at least as long
        as the average bead diameter because it is physically impossible
        for beads to overlap. Furthermore, we recommend that the parameter
        is doubled due to space occupied by sprouts.
        """
        storage = cv.CreateMat(self.img.width, 1, cv.CV_32FC3)
        if(distance < 0 ):
            distance = 1 + max(self.img.width, self.img.height)/50
        cv.HoughCircles(
            self.img._getGrayscaleBitmap(),
            storage,
            cv.CV_HOUGH_GRADIENT,
            2,
            distance,
            canny,
            thresh,
            min_radius=48,
            max_radius=min(self.img.width//10, self.img.height//10))
        if storage.rows == 0:
            return None
        circs = np.asarray(storage)
        sz = circs.shape
        circleFS = FeatureSet()
        for i in range(sz[0]):
            circleFS.append(Circle(
                self.img,
                int(circs[i][0][0]),
                int(circs[i][0][1]),
                int(circs[i][0][2])))
        return circleFS

    def extract(self):
        circles = self.extractCircles()
        if not circles:
            raise NoBeadException()
        beads = FeatureSet(Bead(self.img, circle) for circle in circles)
        return beads

class SproutExtractor(ExtractorBase):
    """
    Extracts sprout features form a target image using segmentation
    strategies and computational geometry. Sprout features extracted
    from the image must belong to a specified bead.
    """
    def __init__(self, img, beads, segmentStrat = SproutSegmenter()):
        self.beads = beads
        super(SproutExtractor, self).__init__(img)

        # Strategies
        self.segmentStrat = segmentStrat

    def maskBeads(self, img):
        """Mask the beads."""
        maskedImg = img
        for bead in self.beads:
            goldenRatio = 1.614
            circleMask = Image(self.img.size())
            circleMask.dl().circle(
                (bead.x, bead.y),
                bead.radius() * goldenRatio,
                filled = True,
                color = Color.WHITE)
            circleMask = circleMask.applyLayers()
            maskedImg = maskedImg - circleMask
            maskedImg = maskedImg.applyLayers()
        return maskedImg

    def preprocess(self):
        cannyMin, cannyMax = (100, 240)
        dilateCount = 8
        imgEdges = self.img.edges(cannyMin, cannyMax)
        imgEdges = self.maskBeads(imgEdges)

        imgEdges = imgEdges.morphClose()
        blobs = imgEdges.findBlobs()
        for blob in blobs:
            if len(blob.mContourAppx) > 2:
                blob.drawAppx(color=Color.WHITE, width=-1)
            blob.drawHoles(color=Color.WHITE, width=-1)
        imgEdges = imgEdges.applyLayers()

        imgEdges = imgEdges.morphClose()
        # imgEdges = imgEdges.convolve(kernel=[
        # 	[1,0,1],
        # 	[0,0,1],
        # 	[1,1,0]])
        # imgEdges = imgEdges.convolve(kernel=[
        # 	[0,1,1],
        # 	[1,0,0],
        # 	[1,0,1]])

        skeleton = imgEdges.dilate(dilateCount).skeletonize(3)
        # isolatedPoints = hitmiss(
        # 	skeleton,
        # 	[[-1,-1,-1,-1,-1,-1,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,0,0,1,0,0,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,0,0,0,0,0,-1],
        # 	[-1,-1,-1,-1,-1,-1,-1]])
        # skeleton = skeleton - isolatedPoints

        self.img = skeleton

    def extract(self):
        self.preprocess()
        self.segmentStrat.injectImg(self.img)
        self.segmentStrat.injectBeads(self.beads)
        sprouts = self.segmentStrat.segment()
        return FeatureSet(sprouts)

class HLSGExtractor(ExtractorBase):
    """
    Extracts High-Level Sprout Geometry (HLSG) features from a target image.
    These features include a heterogenous composition of lower-level features:
    a bead and sprouts.
    """
    def __init__(self, img):
        super(HLSGExtractor, self).__init__(img)

    def preprocess(self):
        pass

    def maskBeads(self, beads):
        """Mask the beads."""
        maskedImg = self.img
        for bead in beads:
            goldenRatio = 1.614
            circleMask = Image(self.img.size())
            circleMask.dl().circle(
                (bead.x, bead.y),
                bead.radius() * goldenRatio,
                filled = True,
                color = Color.WHITE)
            circleMask = circleMask.applyLayers()
            maskedImg = maskedImg - circleMask
            maskedImg = maskedImg.applyLayers()
        return maskedImg

    def mapSproutsToBeads(self, sprouts, beads):
        """
        Generates a list of HLSGs by mapping sprouts to their associated beads.

        :returns: a list of HLSGs by mapping sprouts to their associated beads.
        :rtype: [HLSG]
        """
        hlsgs = []
        hlsgsMapper = {}

        # Initialize mapper
        for bead in beads:
            hlsgsMapper[bead] = []

        # Map sprouts
        for sprout in sprouts:
            closestBead = None
            closestDist = float('inf')
            for bead in beads:
                dist = spsd.euclidean((bead.x, bead.y), sprout[0].start)
                if dist < closestDist:
                    closestDist = dist
                    closestBead = bead
            hlsgsMapper[closestBead].append(sprout)

        # Generate HLSGs
        for bead, sprouts in hlsgsMapper.items():
            hlsgs.append(HLSG(self.img, bead, sprouts))

        return hlsgs

    def extract(self):
        # Extract beads
        try:
            beadExtractor = BeadExtractor(self.img)
            beads = beadExtractor.extract()

            # Extract sprouts
            maskedImg = self.maskBeads(beads)
            sproutExtractor = SproutExtractor(maskedImg, beads)
            sprouts = sproutExtractor.extract()
            hlsgs = self.mapSproutsToBeads(sprouts, beads)

            return FeatureSet(hlsgs)
        except NoBeadException as e:
            return []
