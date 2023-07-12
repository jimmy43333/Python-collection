import os
import sys
import math
import re
import string

def apple_tree():
	a = "1,2,3,4,5"
	b = [int(x) for x in a.split(",")]
	print(b)
	result = 0
	sum = 0
	max = 0
	index = 0
	while index+1 < len(b):
		if index == 0:
			sum = b[index] + b[index+1]
		else:
			sum = b[index-1] + b[index] + b[index+1]
		if sum > max:
			result = index
			max = sum
		index += 1
	print(result)

def bubble_sort():
	book = [2, 10, 35, 8, 5]
	length = len(book）
	temp = 0
	for i in range(length):
		for j in range(length - i - 1):
			if book[j] > book[j+1]:
				temp = book[j]
				book[j] = book[j+1]
				book[j+1] = temp
	print(book)
		
def draw_square():
	r = 3
	for i in range(r):
		if i == 0 or i == r-1:
			print("*"*r)
		else:
			print("*" + " "*(r-2) +"*")

def mod_number():
	n = 8
	count = n % 2
	while n > 0 :
		n = n // 2
		count += 1
	print(count)

def solve():
	result = 0
	a = 1
	b = 2
	c = 3
	judge = b*b - 4 * a * c
	if a == 0 and b == 0 and c == 0:
		result == -1
	else:
		if judge < 0:
			result = 0
		elif judge == 0:
			result = 1
		else:
			result = 2

def line():
	w = 5
	h = 3
	if w % 2 == 1:
		line1 = "+-" * (w//2) + "+"
		line2 = "-+" * (w//2) + "-"
	else:
		line1 = "+-" * (w//2)
		line2 = line1

	for i in range(h):
		if i % 2 == 0:
			print(line1)
		else:
			print(line2)

def number_sum(num):
	total = 0
	for p in str(num):
		total += int(p)
	return total

def number_math(num):
	total = 0
	while num != 0:
		total += num % 10
		num = num // 10
	return total

def number_sort():
	number_int = [123, 55, 6]
	number_str = ["123", "55", "6"]
	for i in number_int:
		print(number_math(i))
	for i in number_str:
		print(number_sum(i))

def test():
	a = 1
	if a is True:
		print(a)
	a = True
	if a is True:
		print(a)
	b = 0
	if b is False:
		print(b)
	b = False
	if b is False:
		print(b)

def pig_check_input(length):
	while True:
		input_list = input().strip().split(" ")
		if len(input_list) == length:
			return [int(a) for a in input_list]
		else:
			print(f"Invalid Input, need to be {length} numbers")

def pig_temperature():
	coordinate = []
	input_data = pig_check_input(4)
	x = input_data[0]
	y = input_data[1]
	r = input_data[2]
	d = input_data[3]
	mother = []
	piggy = 0
	piggy_around_mom = 0
	for i in range(y+1):
		input_data = pig_check_input(x+1)
		for j in range(x+1):
			if input_data[j] == 0:
				mother.append([j, i])
			else:
				piggy += input_data[j]
		coordinate.append(input_data)
	print(len(mother), piggy)
	result = 1
	for ele in mother:
		for i in range(y+1):
			for j in range(x+1):
				if (i - ele[0]) ** 2 + (j - ele[1]) ** 2 <= r ** 2:
					piggy_around_mom +=  coordinate[i][j]
		if (piggy_around_mom/piggy) * 100 > d:
			result = 0
		piggy_around_mom = 0
	print(result)

def pig_food():
	standard = pig_check_input(3)
	a = pig_check_input(3)
	b = pig_check_input(3)
	u = 0
	v = 0
	minimum_pay = 0
	for total in range(standard[0]+1):
		for i in range(total + 1):
			if a[0] * i + b[0] * (total - i) >= standard[1] \
		    	and a[1] * i + b[1] * (total - i) >= standard[2]:
				pay = a[2] * i + b[2] * (total - i)
				if minimum_pay == 0 or pay < minimum_pay:
					minimum_pay = pay
					u = i
					v = total - i
				elif pay == minimum_pay:
					if total > ( u + v ) or (total == (u + v) and i < u):
						u = i
						v = total - i
	print(str(u) + "," + str(v))
	print(minimum_pay)

def chicken_egg():
	input_data = pig_check_input(4)
	produce_egg = input_data[0]
	x0 = input_data[1]
	T = input_data[2]
	L = input_data[3]
	all_egg = 0
	for i in range(1, T+1):
		x = x0
		for j in range(1, i+1):
			x -= (1 + 0.5 * (j))
		if x < L:
			x = L
		all_egg += math.ceil(float(produce_egg * x * 0.01))
	print(all_egg)

# punct = set()
# for ele in line:
# 	if ele in string.punctuation:
# 		punct.add(ele)

def catch_thief():
	punct = [".", ",", ":", ";"]
	special = "藏身地"
	output = "" 
	while True:
		string_input = input().strip()
		if string_input == "END":
			break
		for ele in punct:
			string_input = re.sub(r"[%s]+" % ele, f"{ele} ", string_input)
		string_input = string_input.replace(special, f"\\{special}\\")
		output += (string_input + "\n")
	print(output)

def main(args=None):
	# apple_tree()
	# bubble_sort()
	# draw_square()
	# mod_number()
	# line()
	# number_sum()
	# number_sort()
	# pig_temperature()
	# pig_food()
	# chicken_egg()
	catch_thief()

if __name__ == '__main__':
    main()
