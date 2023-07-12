from pprint import pprint
class Family(object):
    def __init__(self):
        self.money = 100

class Dad(Family):
    def __init__(self):
        super().__init__()
        self.money += 10

class Mom(Family):
    def __init__(self):
        super().__init__()
        self.money *= 10

class Son(Dad, Mom):
    def __init__(self):
        super().__init__()
        self.money += 5
        print(self.money)

class Daughter(Mom, Dad):
    def __init__(self):
        super().__init__()
        self.money += 5
        print(self.money)

child1 = Son()
child2 = Daughter()
pprint(Son.mro())
pprint(Daughter.mro())
