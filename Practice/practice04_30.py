class Bucket:
    def __init__(self):
        self.quota = 0

    def __repr__(self):
        return f"Bucket({self.quota})"

class Bucket:
    def __init__(self):
        self.max = 100
        self.consumed = 0
    
    @property
    def quota(self):
        return self.max - self.consumed
    
    @quota.setter
    def quota(self, c):


def full(bucket, q):
    bucket.quota += q

def drink(bucket, q):
    if bucket.quota > q:
        bucket.quota -= q

b = Bucket()
print(b)
full(b, 100)
print(b)
drink(b, 90)
print(b)
drink(b ,20)
print(b)