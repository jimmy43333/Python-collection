import string
# self.counting = { x: 0 for x in string.ascii_lowercase}
# print(self.counting)

class Extra_Bonus:
    def __init__(self):
        self.counting = 0

    def __call__(self, input_member):
        self.counting += 1
        input_member.add_money(5000)

    def add(self):
        print("Find !!")
        self.counting += 1
    
    def get(self):
        print(f"Member Counting: {self.counting}\n")
        return self.counting

class Member:
    def __init__(self, user, money=0):
        self.user = user
        self.bank = money
    
    def add_money(self, income):
        self.bank += income
    
    def get_info(self):
        print(f"{self.user}: {self.bank}")
 
def check_member(input_member, handle):
    for ele in input_member:
        ele.add_money(5000)
        if "A" in ele.user:
            handle(ele)

n = ["Ashelly", "Ben", "Cris", "Dicky", "Eric", "Amy", "Amenda"]
members = [ Member(x) for x in n ]
obj = Extra_Bonus()
check_member(members, obj)
obj.get()
for ele in members:
    ele.get_info()
