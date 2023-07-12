class Company:
    def __init__(self):
        self.name = "Quanta"
        self.__money = 1000

    def get_money(self):
        return self.__money
    
    def add_money(self):
        self.__money += 1000
        print(self.__money)
    
    @classmethod
    def build(cls):
        a = cls()
        a.__money += 2000
        return a

class Boss(Company):
    def __init__(self):
        super().__init__()
        self._money = 500
        self._year = 100

    def invest_wrong(self):
        self.__money += 1000

c = Company()
c.name = "Meti"
c._year = 3
print(c.name)
print(c.get_money())
c.add_money()
# print(c.__money)

d = Company.build()
print(d.get_money())

e = Boss()
print(e.get_money())
print(e._Company__money)

print(c.__dict__)
print(e.__dict__)