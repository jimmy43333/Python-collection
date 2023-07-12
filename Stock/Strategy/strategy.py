import os
import sys
import time
import copy
import datetime
import pandas as pd

class Strategy:
	def __init__(self, name):
		self.s_name = name
		self.s_type = "L"
		self.buy_numbers = 1
		self.in_price = 0
		self.out_price = 0
		self.current = {}
		self.current["Date"] = None
		self.current["Time"] = None
		self.current["Open"] = None
		self.current["Close"] = None
		self.current["High"] = None
		self.current["Low"] = None
		self.current["Volume"] = None
		result_list = ["Buy_Date", "Buy_Time", "Buy_Open", "Buy_Close", "Buy_High", "Buy_Low",
					   "Sell_Date", "Sell_Time", "Sell_Open", "Sell_Close", "Sell_High", "Sell_Low",
					   "Flag", "* Buy", "* Sell", "* Profit"]
		self.output_data = pd.DataFrame(columns=result_list)
		self.result = {}
		self.params_init()

	def params_init(self):
		self.buy_flag = False
		self.not_trade = True
		self.first_flag = True
		self.today_open = None
		self.yesterday_close = None
		self.today_lowest = None
		self.today_highest = None
		self.bounce_back = None
	
	def set_type(self, input_type):
		self.s_type = input_type

	def print_result(self, file_name):
		print(self.output_data)
		self.output_data.to_csv(file_name, index=False)
		self.output_data.drop(self.output_data.index, inplace=True)

	def get_range_date(self, year):
		start_time = datetime.date(year,1,2)
		end_time = datetime.date(year,12,31)
		day_range = []
		for i in range((end_time - start_time).days+1):
			day = start_time + datetime.timedelta(days=i)
			day_range.append(str(day))
		return day_range

	def get_empty(self):
		for ele, value in self.result.items():
			self.result[ele] = "None"
		self.result["Buy_Date"] = self.current["Date"]
		self.output_data = self.output_data.append(self.result, ignore_index=True)

	def get_buy_info(self):
		self.result["Buy_Date"] = self.current["Date"]
		self.result["Buy_Time"] = self.current["Time"]
		self.result["Buy_Open"] = self.current["Open"]
		self.result["Buy_Close"] = self.current["Close"]
		self.result["Buy_High"] = self.current["High"]
		self.result["Buy_Low"] = self.current["Low"]
		self.result["* Buy"] = self.in_price * self.buy_numbers
		self.buy_flag = True

	def get_sell_info(self, flag):
		self.result["Sell_Date"] = self.current["Date"]
		self.result["Sell_Time"] = self.current["Time"]
		self.result["Sell_Open"] = self.current["Open"]
		self.result["Sell_Close"] = self.current["Close"]
		self.result["Sell_High"] = self.current["High"]
		self.result["Sell_Low"] = self.current["Low"]
		self.result["* Sell"] = self.out_price
		if self.s_type == "L":
			calculate_earn = self.out_price - self.in_price
		else:
			calculate_earn = self.in_price - self.out_price
		self.result["* Profit"] = calculate_earn * self.buy_numbers
		self.result["Flag"] = flag
		self.output_data = self.output_data.append(self.result, ignore_index=True)
		self.buy_flag = False

	def run_strategy(self, start_year, end_year):
		for i in range(start_year, end_year):
			print(i)
			run_period = self.get_range_date(i)
			yesterday = None
			for i in run_period:
				year = i.split("-")[0]
				file_path = f"../Data/{year}/{i}.csv"
				if os.path.isfile(file_path):
					if yesterday:
						self.get_yesterday_info(yesterday)
						self.run(i)
					yesterday = file_path
			output_file = f"../Result/{self.s_name}_{year}.csv"
			self.print_result(output_file)

	def run(self, date):
		year = date.split("-")[0]
		file_path = f"../Data/{year}/{date}.csv"
		data = pd.read_csv(file_path)
		for index, row in data.iterrows():
			self.update_data(row)
			if self.buy_flag:
				if self.judge_stop_profit():
					self.get_sell_info("middle")
					break
			else:
				if self.judge_entry_point():
					self.get_buy_info()
					self.not_trade = False
		if self.buy_flag:
			self.out_price = self.current["Close"]
			self.get_sell_info("end")
		if self.not_trade:
			self.get_empty()
		self.params_init()

	def update_data(self, row):
		try:
			for key, values in self.current.items():
				self.current[key] = row[key]
		except Exception as e:
			print(f"Update Exception : {e}")

	def judge_entry_point(self):
		return False

	def judge_stop_profit(self):
		return False

	def get_yesterday_info(self, file_path):
		data = pd.read_csv(file_path)
		row = data.tail(1)
		self.yesterday_close = row["Close"].values[0]
	

if __name__ == '__main__':
	obj = Strategy()
	

		