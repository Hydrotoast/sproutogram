class BeadDescriptor(object):
	def __init__(self, label):
		self.label = label

	@property
	def radius(self):
		return self.__radius
	
	@radius.setter
	def radius(self, val):
		self.__radius == val

	@property
	def center(self):
		return self.__center

	@center.setter
	def center(self, val):
		self.__center = center
		
