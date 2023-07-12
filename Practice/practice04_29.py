class Score:
    def __init__(self):
        self.weight = 1
        self.grade = 0
        self.total = 0
    
    @property
    def grade(self):
        return self._grade
    
    @grade.setter
    def grade(self, g):
        self._grade = g
        self.total = self.weight * g

class Math_Score(Score):
    def __init__(self):
        super().__init__()
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, w):
        if w < 0:
            self._weight = 0
        else:
            self._weight = w

class English_Score(Score):
    def __init__(self):
        super().__init__()
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, w):
        if hasattr(self, '_weight'):
            raise AttributeError("Can not set weight!!")
        self._weight = w

s = Score()
s.weight = 5
print(s.total)
s.grade = 90
print(s.total)

m = Math_Score()
print(m.weight)
m.weight = -5
print(m.weight)

e = English_Score()
e.weight = 5