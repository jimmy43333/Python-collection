import os
import sys
import time
import copy
import datetime
import pandas as pd
from strategy import Strategy

class Strategy_04(Strategy):
	def __init__(self, name):
		super().__init__(name)

	def judge_entry_point(self):
		if self.first_flag:
			self.first_flag = False
			self.today_open = self.current["Open"]
			self.today_lowest = self.current["Low"]
			if self.today_open < self.yesterday_close:
				self.in_price = self.today_open
				self.not_trade = False
				return True
		return False

	def judge_stop_profit(self):
		if self.current["Low"] < self.in_price + 15 < self.current["High"]:
			self.out_price = self.in_price + 15
			return True
		if self.current["Low"] < self.today_lowest + 15 < self.current["High"]:
			self.out_price = self.today_lowest + 15
			return True
		if self.current["Low"] < self.today_lowest:
			self.today_lowest = self.current["Low"]
		return False
	
	def get_yesterday_info(self, file_path):
		data = pd.read_csv(file_path)
		row = data.tail(1)
		self.yesterday_close = row["Close"].values[0]


if __name__ == '__main__':
	long_short = "S"
	obj = Strategy_04(f"Strategy04_{long_short}")
	obj.set_type(long_short)
	obj.run_strategy(2011, 2020)