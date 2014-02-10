from SimpleCV import Line


class RadialSegment(Line):
    def __init__(self, img, origin, head, blob=None):
        self.origin = origin
        self.head = head

        self.blob = blob
        super(RadialSegment, self).__init__(img, (origin, head))