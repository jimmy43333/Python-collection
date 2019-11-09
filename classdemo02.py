class Square():
	kid = 0
	def __init__(self,l):
		self.hl = l
		Square.kid += 1
	def getrc(self):
		return self.hl;
	def setrc(self,l):
		self.hl = l
	def geta(self):
		return self.hl * self.hl
	
	slen = property(getrc,setrc)
	area = property(geta)
	
	@classmethod     # use @classmethod to say it is a class method 
	def kids(cls):
		print("Generate ",cls.kid," kids")
	@staticmethod
	def helping():
		print("It is a function of the square.Input the length of square")

class Triangle(Square):
	def geta(self):
		return (self.hl * self.hl) / 2
	tarea = property(geta)
	
	@staticmethod
	def helping():
		print("It is a function of the triangle.Input the length of triangle")

image = Square(4)
trian = Triangle(6)
print(image.slen)
image.slen = 8
print(image.area)
print(trian.area)
print(trian.tarea)
image2 = Square(5)
image3 = Square(6)
Triangle.helping()
Square.kids()
Square.helping()
print(image.kid)
