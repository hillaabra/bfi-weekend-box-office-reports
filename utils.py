import pandas as pd
import math
import xlrd


class DataPrepation:

	def __init__(self, excel_report_filepath):
		self.excel_report_filepath = excel_report_filepath
		self.workbook = xlrd.open_workbook(excel_report_filepath)
		self.report_heading = self.workbook.sheet_by_index(0).cell_value(0, 0)
		self.gbp_value_columeself.gbp_value_columns = ['Weekend Gross', 'Site average', 'Total Gross to date']
       		self.percentage_value_columns = ["% change on last week"] # allowing for more to be added later on

	@staticmethod
	def format_gbp_currency(value: int) --> str:
		str_value = str(value)
		
		def insert_commas(str_value, counter):
			if len(str_value) <= 3:
				return str_value
			
			result = insert_commas(str_value[:-3, counter + 3)
			return result + "," + str_value[-3:]

		str_value_with_commas = insert_commas(str_value, counter=0)
		return "£" + str_value_with_commas
