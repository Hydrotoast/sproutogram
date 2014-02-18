from geometry import *
from set_forest import *
from features import *


class SproutSegmenter(object):
    def __init__(self):
        self.img = None
        self.beads = None

    def inject_img(self, img):
        self.img = img

    def inject_beads(self, beads):
        self.beads = beads

    def find_closest_bead(self, blob):
        """
        Finds the bead of closest to the given blob in terms of Euclidean
        distance.

        :param blob: blob to find the closest bead for
        :returns: closest bead
        :rtype: Bead
        """
        closest_bead = None
        closest_dist = float('inf')
        for bead in self.beads:
            dist = spsd.euclidean((bead.x, bead.y), blob.centroid())
            if dist < closest_dist:
                closest_dist = dist
                closest_bead = bead
        return closest_bead

    def generate_connections(self, blob_segments, distance_threshold=20):
        """
        Generates hypothetical connections between blob segments if they are
        within a thresholded neighborhood of each other.

        :returns: A list of generated, hypothetical connections.
        :rtype: [(Blob, Blob)]
        """
        connections = []
        for segment_outer in blob_segments:
            for segment_inner in blob_segments:
                # Do not connect segments to each other
                if segment_outer == segment_inner:
                    continue
                distance = spsd.euclidean(segment_outer.head, segment_inner.origin)
                if distance < distance_threshold:
                    connections.append((segment_outer, segment_inner))
        return connections

    def generate_blob_segments(self, blobs):
        """
        Generates a list of linear approximations for blobs. That is, blobs are
        modeled as geometric rays defined radially outward.

        :returns: A list of generated rays defined radially outward.
        :rtype: [RadialSegment]
        """
        blob_segments = []
        if blobs:
            # Acquire blob segments
            for blob in blobs:
                bead = self.find_closest_bead(blob)
                sorted_contour = sorted(
                    blob.contour(),
                    key=lambda x: spsd.euclidean(x, (bead.x, bead.y)))
                start = sorted_contour[0]
                end = sorted_contour[-1]

                radial_segment = RadialSegment(self.img, start, end, blob)
                blob_segments.append(radial_segment)
        return blob_segments

    def generate_sprout_segments(self, blob_segments, connections):
        """
        Generates the sprout segments as lists of blobs.

        :returns: A list of sprout segments.
        :rtype: [Sprout]
        """
        set_forest = SetForest(blob_segments)
        for connection in connections:
            set_forest.union(
                set_forest.find(connection[0]),
                set_forest.find(connection[1]))

        seen = set()
        blob_map = {}
        for segment in blob_segments:
            parent = set_forest.find(segment)
            if parent not in seen:
                blob_map.update({parent: list(set([parent, segment]))})
                seen.add(parent)
            else:
                blob_map[parent].append(segment)

        sprouts = []
        for segments in blob_map.values():
            if len(segments) == 1 and segments[0].area() < 40:
                continue
            sprouts.append(Sprout(segments))

        # --DEBUG
        # FeatureSet(blobSegments).draw(color=Color.BLUE, width=2)
        return sprouts

    def segment(self):
        blobs = self.img.findBlobs(minsize=1)

        # --DEBUG
        # blobs.draw(color=Color.RED, width=4)

        if not blobs:
            return []

        blob_segments = self.generate_blob_segments(blobs)

        if not blob_segments:
            return []

        connections = self.generate_connections(blob_segments)
        sprouts = self.generate_sprout_segments(blob_segments, connections)

        return sprouts
