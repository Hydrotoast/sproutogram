import operator

def alpharange(start='A', end='Z'):
    """
    Alphabetic generator from a given start letter to end letter. An example
    of this sequence is A, B, C, D, ...

    :param start: starting character
    :param end: ending character
    :rtype: character
    """
    start = ord(start)
    end = ord(end)
    for letter_ord in range(start, end + 1):
        yield chr(letter_ord)

def lis(l):
    """
    Retrives the longest increasing subsequence (LIS) from the given list.

    :param l: original list
    :returns: the longest increasing subsequence
    :rtype: list

    **Example**
    
        >>> lis([1, 6, 0, 8])
        [1, 6, 8]
    """
    length = [0] * len(l)
    n = [0] * len(l)
    max_index = max_length = float('-inf')
    for i in range(len(l) - 1, -1, -1):
        for j in range(i, len(l)):
            if l[i] < l[j]:
                if length[i] < length[j] + 1:
                    length[i] = length[j] + 1
                    n[i] = j
                if length[i] > max_length:
                    max_index = i
                    max_length = length[i]

    sub = []
    while length[max_index] != 0:
        sub.append(l[max_index])
        max_index = n[max_index]
    sub.append(l[max_index])
    return sub
