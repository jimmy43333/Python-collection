class Person():
	def __init__(self, name, gender, age):
		self.name = name
		self.gender = gender
		self.age = age
	def grow(self):
		self.age += 1

class Doctor(Person) :
	def __init__(self, name, gender, age):
		self.name = "Dr" + name
		self.gender = gender
		self.age = age

class Police(Person):
	def __init__(self, name, gender, age):
		super().__init__(name, gender, age)
	def claim(self):
		print("Im Police")
t = Person("Amy","M",21)
p = Police("jimmy","M",20)
d = Doctor("jeff","M",19)
print("doctor age :" + str(d.age))
d.grow()
print("doctor age : " + str(d.age))
print(p.gender)
p.claim()

