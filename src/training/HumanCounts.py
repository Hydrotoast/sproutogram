class HumanData(object):
	def __init__(self, maxCounts, focusCounts, branchingCount):
		self.maxCounts = maxCounts
		self.focusCounts = focusCounts
		self.branchingCount = branchingCount

data = {}
data.update({'Ang1 250 ng_ml 1 Day 7': HumanData(14, 8, 2)})
data.update({'1k 3 Day 7': HumanData(23, 14, 3)})
data.update({'1k 2 Day 7': HumanData(15, 11, 4)})
data.update({'10k 5 Day 7': HumanData(20, 10, 4)})
data.update({'10k 1 Day 7': HumanData(16, 7, 0)})
data.update({'Control 5 Day 7': HumanData(17, 7, 2)})
data.update({'Control 4 Day 7': HumanData(17, 8, 3)})
data.update({'Control 2 Day 7': HumanData(18, 12, 7)})
data.update({'Control 1 Day 7': HumanData(17, 10, 2)})
data.update({'20k 5 Day 7': HumanData(24, 9, 4)})
data.update({'20k 3 Day 7': HumanData(12, 6, 11)})
data.update({'20k 2 Day 7': HumanData(23, 15, 3)})
data.update({'20k 1 Day 7': HumanData(17, 10, 0)})
data.update({'Ang1 100ng_ml 5 Day 7': HumanData(13, 9, 3)})
data.update({'Ang1 100ng_ml 3 Day 7': HumanData(12, 7, 1)})
