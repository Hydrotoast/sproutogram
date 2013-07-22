class SproutDescriptor(object):
	def __init__(self, label):
		self.label = label

	@property
	def length(self):
		return self.__length

	@length.setter
	def length(self, val):
		return self.__length

	@property
	def width(self):
		return self.__width

	@width.setter
	def width(self, val):
		self.__width = val
