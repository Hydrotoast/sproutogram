def alpharange(start='A', end='Z'):
	start = ord(start)
	end = ord(end)
	for letter_ord in range(start, end + 1):
		yield chr(letter_ord)
