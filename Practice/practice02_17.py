class Two:
    def __init__(self):
        self.number = [111, 222, 333, 444, 555]
    
    def __iter__(self):
        for ele in self.number:
            yield ele

# def one(input_list):
#     for i in input_list:
#         yield int(i)

# number = [1,2,34,5,6,7,8]
# a = one(number)
# for ele in a:
#     print(ele)
# print(list(a))

# def sub(a,b=0,c=0):
#     print(a-b-c)

# sub(10,2)
# sub(10, b=5)
# sub(10, c=4)
# sub(10,2,3)
# sub(10, c=4, b=4)
from datetime import datetime
def log(message, timestamp=None):
    """
    timestamp: when the log message occurred.
    """
    timestamp = datetime.now() if timestamp is None else timestamp
    print(f"{timestamp}  {message}")

log("This is the message!!!")

def safe_version(id, *, user='root', password='root'):
    print(f"({id}) {user}:{password}")

safe_version(1, user="Jimmy", password=1234)
safe_version(2, "Jimmy", 1234)