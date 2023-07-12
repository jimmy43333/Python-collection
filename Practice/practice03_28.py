from collections.abc import Sequence

class MyContainer(Sequence):
    def __init__(self):
        self.result = [1,2,3,4,5]

    def __getitem__(self, index):
        return self.result[index]
    
    def __len__(self):
        return 10
    

obj = MyContainer()
print(len(obj))
print(obj[3])
print(obj.index(1))
print(obj.count(5))