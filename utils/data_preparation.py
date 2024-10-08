import pandas as pd
import math

class DataPreparation:

	def __init__(self):
		self.gbp_value_columns = ['Weekend Gross', 'Site average', 'Total Gross to date']
		self.percentage_value_columns = ["% change on last week"] # allowing for more to be added later on

	@staticmethod
	def format_gbp_currency(value: int) -> str:
		str_value = str(round(value))

		def insert_commas(str_value, counter):
			if len(str_value) <= 3:
				return str_value

			result = insert_commas(str_value[:-3], counter + 3)
			return result + "," + str_value[-3:]

		str_value_with_commas = insert_commas(str_value, counter=0)
		return "£" + str_value_with_commas

	def restore_string_formatting_to_gbp_values(self, df: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
		for column_name in column_names:
			df[column_name] = df[column_name].apply(self.format_gbp_currency)
		return df

	@staticmethod
	def convert_decimal_to_percentage_str(value: float) -> str:
		if math.isnan(value) == False:
			str_value = str(round(value * 100)) + "%"
			return str_value
		else:
			return value

	def restore_string_formatting_to_percentage_values(self, df: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
		for column_name in column_names:
			df[column_name] = df[column_name].apply(lambda x: self.convert_decimal_to_percentage_str(x))
		return df

	def restore_original_formatting(self, df_table: pd.DataFrame) -> pd.DataFrame:
		df_reformatted = self.restore_string_formatting_to_gbp_values(df_table, self.gbp_value_columns)
		df_reformatted = self.restore_string_formatting_to_percentage_values(df_reformatted, self.percentage_value_columns)
		df_reformatted.fillna("-", inplace=True)
		return df_reformatted