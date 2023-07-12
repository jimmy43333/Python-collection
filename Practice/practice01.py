# A = {"red": [5], "green": ["40"], "blue": []}

# key_list = ['red', 'green', 'blue', 'opacity']
# for ele in key_list:
#     print(A.get(ele))
# # 1
# print("\n-- 1 ------")
# for ele in key_list:
#     r = int((A.get(ele) or [0])[0])
#     print(f"{ele}: {r}")

# # 2 
# print("\n-- 2 ------")
# for ele in key_list:
#     t = A.get(ele)
#     r = int(t[0]) if t else 0
#     print(f"{ele}: {r}")

# # 3 
# print("\n-- 3 ------")
# def check_helper(dictionary, key, default=0):
#     t = dictionary.get(key)
#     if t:
#         r = int(t[0])
#     else:
#         r = default
#     return r

# for ele in key_list:
#     print(f"{ele}: {check_helper(A, ele)}")

# l = [1,2,3,4,5,6,7,8,9]
# print(l[2:5])
# print(l[-3:-1])
# print(l[3:-3])
# print(l[:4])
# print(l[5:])
# print(l[:-2])
# print(l[-3:])
# print(l[:20])
# print(l[8:-7])

# print("\n-------------")
# l2 = l[:]
# l3 = l
# l2[2:5] = ['A','B','C']
# l3[6:8] = ['D','E','F']
# print(l)
# print(l2)
# print(l3) 

# print("---------------")
# a = [1,2,3,4,5,6]
# b = [x ** 2 for x in a if x % 2 == 0]
# c = map(lambda x: x**2, a)
# d = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
# a_d = {"A": "Apple", "B":"Ball", "C": "Cat", "D":"Dog"}
# b_d = { obj:chr for chr, obj in a_d.items() }
# c_d = {len(obj) for obj in a_d.values()}
# print(b)
# print(b_d)
# print(c_d)

# g = (x for x in range(100))
# g2 = (x*2 for x in g)

# count = 0
# while count < 10:
#     print(f"G1: {next(g)}")
#     print(f"G2: {next(g2)}")
#     count += 1

# items_dict = {"A": "Apple", "B":"Ball", "C": "Cat", "D":"Dog"}
# items_list = items_dict.values()
# for i, obj in enumerate(items_dict):
#     print(f"{i} > {obj}")
# for i, obj in enumerate(items_list, 2):
#     print(f"{i} > {obj}")

# items_len = [ len(x) for x in items_list ]
# for i,j,k in zip(items_dict, items_list, items_len):
#     print(f"{i} > {j}: {k}")

# a = [1,2,3,4,5]
# b = ["A", "B", "C"]
# c = ["J", "K", "L", "M"]
# for i, j, k in zip(a, b, c):
#     print(f"{i} {j} {k}")
import json
def divide_json(file):
    handle = open(file, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = ( 10/int(x) for x in op.values())
        for ele in op.keys():
            v = next(value)
            op[ele] = v
    except ValueError as e:
        print(e)
    except ZeroDivisionError as e:
        print(e)
    else:
        print("Else")
    finally:
        print("Finally")
        handle.close()

a = [1, 2, 3, 4, 5, 6]
b = [ x*2 for x in a ]
c = [ x ** 2 for x in a if x % 2 == 0 ] 
d = map(lambda x: x**2, a)
e = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))

f = {"A": "Apple", "B":"Ball", "C": "Cat", "D":"Dog"}
g = { obj:chr for chr, obj in f.items() }
h = { len(obj) for obj in f.values() }

nf = lambda x,y: x+y
o = nf(1, 3)



items_dict = {"A": "Apple", "B":"Ball", "C": "Cat", "D":"Dog"}
items_list = items_dict.values()
for i, obj in enumerate(items_dict):
    print(f"{i} > {obj}")
for i, obj in enumerate(items_list, 2):
    print(f"{i} > {obj}")

print("--"*10)

items_dict = {"A": "Apple", "B":"Ball", "C": "Cat", "D":"Dog"}
items_list = items_dict.values()
items_len = [ len(x) for x in items_list ]
for i,j,k in zip(items_dict, items_list, items_len):
    print(f"{i} > {j}: {k}")
