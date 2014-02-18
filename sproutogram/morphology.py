from SimpleCV import *


def hitmiss(src, element):
    """
    Morphological operation for shape detection. The notation for the
    structuring element uses ``1`` for foreground, ``-1`` for background and
    ``0`` for ignore.

    :param src: source image
    :param element: structuring element for the desired shape as a square matrix
    :returns: the hit-or-miss transformation of the source image
    :rtype: Image

    The algorithm can be described as below:

    .. math::

        \mathbf{A} \otimes \mathbf{B} = (\mathbf{A} \ominus \mathbf{B_1})
            \cap (\overline{\mathbf{A}} \ominus \mathbf{B_2})
    """
    k1 = np.array(
        [[(x == 1) for x in row] for row in element],
        dtype=np.uint8)
    k2 = np.array(
        [[(x == -1) for x in row] for row in element],
        dtype=np.uint8)

    e1 = Image(
        cv2.erode(
            src.getGrayNumpyCv2(), 
            k1), cv2image=True)
    e2 = Image(
        cv2.erode(
            src.invert().getGrayNumpyCv2(), 
            k2), cv2image=True)

    dst = Image(
        cv2.bitwise_and(
            e1.getGrayNumpyCv2(), 
            e2.getGrayNumpyCv2(), 
            np.array([])), cv2image=True)
    return dst
