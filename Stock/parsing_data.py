import os
import sys
import time
import datetime
import pandas as pd

class Read_CSV:
	def __init__(self):
		xlsx_file = '20010101-20101231.xlsx'
		df = pd.read_excel(xlsx_file, head=None)
		for each_date in self.get_range_date():
			year = each_date.split("-")[0]
			tmp = df.loc[df["Date"] == each_date]
			print(tmp)
			if not tmp.empty:
				tmp.to_csv(f'Data/{year}/{each_date}.csv', index=False)

	def get_range_date(self):
		start_time = datetime.date(2001,1,1)
		end_time = datetime.date(2010,12,31)
		day_range = []
		for i in range((end_time - start_time).days+1):
			day = start_time + datetime.timedelta(days=i)
			day_range.append(str(day))
		return day_range

	def newfunction(self):
		try:
			x = 1
		except Exception as e:
			print(e)

	def newfunction2(self):
		try:
			for adj = ['red', 'big', 'tasty']
			fruits = ['apple', 'banana', 'cherry']
			for x in adj:
			  for y in fruits:
				print(x, y)
		  print(x)
		except:
		  print('Something went wrong')
		finally:
		  print('The try except is finished')
		     
	def newfunction3(self):
		pass

	def newfunction(self):
     try:
         x = 1
         y = 2
     except Exception as e:
         print()
	
	def 

if __name__ == '__main__':
    A = Read_CSV()