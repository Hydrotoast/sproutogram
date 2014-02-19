from ..sprout_segmentation import *
from ..morphology import *


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

    def extract_circles(self, canny=164, thresh=128, distance=512):
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
        if distance < 0:
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
        circle_fs = FeatureSet()
        for i in range(sz[0]):
            circle_fs.append(Circle(
                self.img,
                int(circs[i][0][0]),
                int(circs[i][0][1]),
                int(circs[i][0][2])))
        return circle_fs

    def extract(self):
        circles = self.extract_circles()
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
    def __init__(self, img, beads, segment_strat=SproutSegmenter()):
        self.beads = beads
        super(SproutExtractor, self).__init__(img)

        # Strategies
        self.segment_strat = segment_strat

    def mask_beads(self, img):
        """Mask the beads."""
        masked_img = img
        for bead in self.beads:
            golden_ratio = 1.614
            circle_mask = Image(self.img.size())
            circle_mask.dl().circle(
                (bead.x, bead.y),
                bead.radius() * golden_ratio,
                filled=True,
                color=Color.WHITE)
            circle_mask = circle_mask.applyLayers()
            masked_img = masked_img - circle_mask
            masked_img = masked_img.applyLayers()
        return masked_img

    def preprocess(self):
        canny_min, canny_max = (100, 240)
        dilate_count = 8
        img_edges = self.img.edges(canny_min, canny_max)
        img_edges = self.mask_beads(img_edges)

        img_edges = img_edges.morphClose()
        blobs = img_edges.findBlobs()
        for blob in blobs:
            if len(blob.mContourAppx) > 2:
                blob.drawAppx(color=Color.WHITE, width=-1)
            blob.drawHoles(color=Color.WHITE, width=-1)
        img_edges = img_edges.applyLayers()

        img_edges = img_edges.morphClose()
        # imgEdges = imgEdges.convolve(kernel=[
        #   [1,0,1],
        #   [0,0,1],
        #   [1,1,0]])
        # imgEdges = imgEdges.convolve(kernel=[
        #   [0,1,1],
        #   [1,0,0],
        #   [1,0,1]])

        skeleton = img_edges.dilate(dilate_count).skeletonize(3)
        # isolatedPoints = hitmiss(
        #   skeleton,
        #   [[-1,-1,-1,-1,-1,-1,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,0,0,1,0,0,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,0,0,0,0,0,-1],
        #   [-1,-1,-1,-1,-1,-1,-1]])
        # skeleton = skeleton - isolatedPoints

        self.img = skeleton

    def extract(self):
        self.preprocess()
        self.segment_strat.inject_img(self.img)
        self.segment_strat.inject_beads(self.beads)
        sprouts = self.segment_strat.segment()
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

    def mask_beads(self, beads):
        """Mask the beads."""
        masked_img = self.img
        for bead in beads:
            golden_ratio = 1.614
            circle_mask = Image(self.img.size())
            circle_mask.dl().circle(
                (bead.x, bead.y),
                bead.radius() * golden_ratio,
                filled=True,
                color=Color.WHITE)
            circle_mask = circle_mask.applyLayers()
            masked_img = masked_img - circle_mask
            masked_img = masked_img.applyLayers()
        return masked_img

    def map_sprouts_to_beads(self, sprouts, beads):
        """
        Generates a list of HLSGs by mapping sprouts to their associated beads.

        :returns: a list of HLSGs by mapping sprouts to their associated beads.
        :rtype: [HLSG]
        """
        hlsgs = []
        hlsgs_mapper = {}

        # Initialize mapper
        for bead in beads:
            hlsgs_mapper[bead] = []

        # Map sprouts
        for sprout in sprouts:
            closest_bead = None
            closest_dist = float('inf')
            for bead in beads:
                dist = spsd.euclidean((bead.x, bead.y), sprout[0].origin)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_bead = bead
            hlsgs_mapper[closest_bead].append(sprout)

        # Generate HLSGs
        for bead, sprouts in hlsgs_mapper.items():
            hlsgs.append(HLSG(self.img, bead, sprouts))

        return hlsgs

    def extract(self):
        # Extract beads
        try:
            bead_extractor = BeadExtractor(self.img)
            beads = bead_extractor.extract()

            # Extract sprouts
            maked_img = self.mask_beads(beads)
            sprout_extractor = SproutExtractor(maked_img, beads)
            sprouts = sprout_extractor.extract()
            hlsgs = self.map_sprouts_to_beads(sprouts, beads)

            return FeatureSet(hlsgs)
        except NoBeadException:
            return []
