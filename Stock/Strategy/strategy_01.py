import os
import sys
import time
import copy
import datetime
import pandas as pd
from strategy import Strategy

# class Strategy_01(Strategy):
# 	def __init__(self, name):
# 		super().__init__(name)

# 	def judge_entry_point(self):
# 		return True

# 	def judge_stop_profit(self):
# 		if self.first_flag:
# 			self.first_flag = False
# 			self.today_open = self.current["Open"]
# 			if self.current["Open"] > self.in_price:
# 				self.out_price = self.current["Open"]
# 				return True
# 			else:
# 				if self.current["Open"] - 10 < self.in_price:
# 					self.out_price = self.current["Open"]
# 					return True
# 			return False
# 		else:
# 			sell_point = self.today_open + 20
# 			if self.current["Low"] <= sell_point <= self.current["High"]:
# 				self.out_price = sell_point
#     				return True
# 			sell_point = self.today_open - 10
# 			if self.current["Low"] <= sell_point <= self.current["High"]:
# 				self.out_price = sell_point
# 				return True
# 			return False

# 	def get_yesterday_info(self, file_path):
# 		data = pd.read_csv(file_path)
# 		row = data.tail(1)
# 		self.in_price = row["Close"].values[0]
# 		self.result["Buy_Date"] = row["Date"].values[0]
# 		self.result["Buy_Time"] = row["Time"].values[0]
# 		self.result["Buy_Open"] = row["Open"].values[0]
# 		self.result["Buy_Close"] = row["Close"].values[0]
# 		self.result["Buy_High"] = row["High"].values[0]
# 		self.result["Buy_Low"] = row["Low"].values[0]
# 		self.result["* Buy"] = self.in_price
# 		self.buy_flag = True
# 		self.not_trade = False

class Car:
    def __init__(self):
        print("Car...")

    def run(self):
        print("I'm Run")
		
    	
if __name__ == '__main__':
	#long_short = "L"
	#obj = Strategy_01(f"Strategy01_{long_short}")
	#obj.set_type(long_short)
	#obj.run_strategy(2011, 2020)

    b = ["a","b","c","a","d"]
    f = "/Users/TGsung/Desktop/Program/Stock/Result/Strategy01_L_2011.csv"
    df = pd.read_csv(f)
    print(type(df))
    # print(df)    
    df = pd.DataFrame(index=b)

    a = [10,20,30,40,50]

    for ele in zip(a,b):
        if ele[1] == "a":
            ele[0] += 10
        print(ele)

    print("+++++++++++++++++++++")
    for ele in a:
        ele += 2

    c = {"a":10, "b":20, "c":30}

    e = c["a"]
    print(type(c))
    for key,value in c.items():
        if key == "a":
            value += 10
        print(key)
        print(value)