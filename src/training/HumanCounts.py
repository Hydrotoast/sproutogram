class SproutCounts(object):
	def __init__(self, maxCounts, focusCounts):
		self.maxCounts = maxCounts
		self.focusCounts = focusCounts

data = {}
data.update({'Ang1 250 ng_ml 1 Day 7': SproutCounts(14, 8)})
data.update({'1k 3 Day 7': SproutCounts(23, 14)})
data.update({'1k 2 Day 7': SproutCounts(15, 11)})
data.update({'10k 5 Day 7': SproutCounts(20, 10)})
data.update({'10k 1 Day 7': SproutCounts(16, 7)})
data.update({'Control 5 Day 7': SproutCounts(17, 7)})
data.update({'Control 4 Day 7': SproutCounts(17, 8)})
data.update({'Control 2 Day 7': SproutCounts(18, 12)})
data.update({'Control 1 Day 7': SproutCounts(17, 10)})
data.update({'20k 5 Day 7': SproutCounts(24, 9)})
data.update({'20k 3 Day 7': SproutCounts(12, 6)})
data.update({'20k 2 Day 7': SproutCounts(23, 15)})
data.update({'20k 1 Day 7': SproutCounts(17, 10)})
data.update({'Ang1 100ng_ml 5 Day 7': SproutCounts(13, 9)})
data.update({'Ang1 100ng_ml 3 Day 7': SproutCounts(12, 7)})
