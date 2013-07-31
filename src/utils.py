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
