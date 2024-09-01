import pandas as pd
import math
import re
import xlrd


class ExcelParser:
    def __init__(self, excel_report_filepath):
      try:
        self.workbook = xlrd.open_workbook(excel_report_filepath)
      except NotImplementedError:
         print("This program is coded to run on xls files, not xlsx. Try downgrading the input file to xls first.")
      self.excel_sheet = self.workbook.sheet_by_index(0)
      self.report_heading = self.excel_sheet.cell_value(0, 0)
      self.top_15_df = self._read_top_15_table_to_df()
      self.column_names = self.top_15_df.columns
      self.total_top_15_weekend_gross = self._get_top_15_weekend_gross()
      self.total_top_15_gross_to_date = self._get_top_15_total_gross_to_date()
      self._check_for_change_in_footnotes_below_top_15_table() # to check layout is as expected before continuing to read second table
      self.end_boundary_of_other_uk_films_table = self._find_end_of_other_uk_films_table()
      self.end_boundary_of_other_new_releases_table = self._find_end_of_other_new_releases_table()
      self.other_uk_films_df = self._read_other_uk_films_table_to_df()
      self.other_new_releases_df = self._read_other_new_releases_table_to_df()
      self.start_boundary_of_comments_on_top_15_section = self._find_start_boundary_of_comments_on_top_15()
      self.start_boundary_of_notes_on_top_15_section = self._find_start_boundary_of_notes_for_top_15_section()
      self.list_of_comments_on_top_15_result = self._read_comments_on_top_15_to_list()
      self.start_boundary_of_openers_next_week_table = self._find_start_of_openers_next_week_table()
      self.list_of_notes_on_top_15_table = self._read_notes_for_top_15_table_to_list()
      self.openers_next_week_df = self._read_openers_next_week_table_to_df()

    def _read_top_15_table_to_df(self):
      df_top15 = pd.read_excel(self.workbook, header=1, nrows=15)
      return df_top15

    def _get_top_15_weekend_gross(self) -> float:
      cell_d_18 = self.excel_sheet.cell_value(17, 3)
      if cell_d_18 == "":
         raise ValueError("Expected cell D18 to contain the weekend gross total figure but it was empty.\
               \nCheck xls document layout as coordinates may have changed.")
      else:
         return cell_d_18

    def _get_top_15_total_gross_to_date(self) -> float:
      cell_j_18 = self.excel_sheet.cell_value(17, 9)
      if cell_j_18 == "":
         raise ValueError("Expected cell D18 to contain the weekend gross total figure but it was empty.\
               \nCheck xls document layout as coordinates may have changed.")
      else:
         return cell_j_18

    def _check_for_empty_row(self, row_index) -> bool:
       row = self.excel_sheet.row_values(row_index)
       return all(cell == "" or cell is None for cell in row)

    def _check_for_change_in_footnotes_below_top_15_table(self):
        cell_b_19 = self.excel_sheet.cell_value(18, 1)
        if not re.match(r"Note: 'Weekend gross' figures will include Previews.+", cell_b_19):
          raise ValueError("The footnote regarding weekend gross figures including previews was expected in cell B19.\n\
                Examine layout of Excel sheet to see changes.")
        elif self._check_for_empty_row(19) == False:
          raise ValueError("More notes than expected are under the Top 15 Table.\
                Examine layout of Excel sheet to decide how to handle extra content.")
        else:
           print("Ready to read Other UK Films Table.")

    def _find_end_of_other_uk_films_table(self) -> int:
        if "Other UK films" not in self.excel_sheet.row_values(20):
           raise ValueError("Program is written to expect 'Other UK films' header in row 20 (Excel Row 21).")
        else:
           for row_index in range(21, self.excel_sheet.nrows):
              if self._check_for_empty_row(row_index):
                 return row_index

    def _read_other_uk_films_table_to_df(self) -> pd.DataFrame:
        index_of_empty_row_after_table = self.end_boundary_of_other_uk_films_table
        num_rows = index_of_empty_row_after_table - 21
        df_other_uk_films = pd.read_excel(self.workbook, skiprows=21, nrows=num_rows, header=None, names=self.column_names)
        return df_other_uk_films

    def _find_end_of_other_new_releases_table(self) -> int:
       expected_row_ind_of_table_header = self.end_boundary_of_other_uk_films_table + 1

         # Checking for "Other new releases" table header in the next two rows after end of Other UK films table
       if "Other new releases" not in self.excel_sheet.row_values(expected_row_ind_of_table_header):
           raise ValueError("Program is written to expect 'Other new releases' header two rows after 'Other UK Films' table ends.\
                            String value not found in this row. Check document layout.")
       else:
           for row_index in range(expected_row_ind_of_table_header + 1, self.excel_sheet.nrows):
              if self._check_for_empty_row(row_index):
                 return row_index

    def _read_other_new_releases_table_to_df(self) -> pd.DataFrame:
        index_of_empty_row_after_new_releases_table = self.end_boundary_of_other_new_releases_table
        index_of_starting_row_of_new_releases_table = self.end_boundary_of_other_uk_films_table + 2 # this approach would have to be altered if the layout were to ever vary
        num_rows = index_of_empty_row_after_new_releases_table - index_of_starting_row_of_new_releases_table
        df_other_new_releases = pd.read_excel(self.workbook, skiprows=index_of_starting_row_of_new_releases_table, nrows=num_rows, header=None, names=self.column_names)
        return df_other_new_releases

    def _find_start_boundary_of_comments_on_top_15(self) -> int:
       for row_index in range(self.end_boundary_of_other_new_releases_table, self.excel_sheet.nrows):
         row = self.excel_sheet.row_values(row_index)
         if "Comments on this week's top 15 results" in row:
            return row_index + 1
       raise ValueError("Expected to find header 'Comments on this week's top 15 results' in workbook sheet after\
                       end of Other New Releases table. String not found in search of rows. Check document layout.")

    def _find_start_boundary_of_notes_for_top_15_section(self) -> int:
       for row_index in range(self.start_boundary_of_comments_on_top_15_section, self.excel_sheet.nrows):
         row = self.excel_sheet.row_values(row_index)
         if "Notes for Top 15 table:" in row:
            return row_index
       raise ValueError("Expected to find header 'Notes for Top 15 table:' in workbook sheet after\
                       end of 'Comments on this week's top 15 results' section. String not found in search of rows. \
                        Check document layout.")

    def _read_comments_on_top_15_to_list(self) -> list:
       row_index_section_start = self.start_boundary_of_comments_on_top_15_section
       row_index_section_end = self.start_boundary_of_notes_on_top_15_section
       comments_list = []
       for row_index in range(row_index_section_start, row_index_section_end):
          if self._check_for_empty_row(row_index) == False:
             comments_list.append(self.excel_sheet.cell_value(row_index, 1)) # expects the value to be in column B
       return comments_list

    def _find_start_of_openers_next_week_table(self) -> int:
       for row_index in range(self.start_boundary_of_notes_on_top_15_section, self.excel_sheet.nrows):
         row = self.excel_sheet.row_values(row_index)
         if "Openers next week:" in row:
            return row_index
       raise ValueError("Expected to find header 'Openers next week:' in workbook sheet after\
                       end of 'Notes for Top 15 table' section. String not found in search of rows. \
                        Check document layout.")

    def _read_notes_for_top_15_table_to_list(self) -> list:
       row_index_section_start = self.start_boundary_of_notes_on_top_15_section
       row_index_section_end = self.start_boundary_of_openers_next_week_table
       notes_list = []
       for row_index in range(row_index_section_start + 1, row_index_section_end):
          if self._check_for_empty_row(row_index) == False:
             notes_list.append(self.excel_sheet.cell_value(row_index, 1)) # expects the value to be in column B
       return notes_list

    def _read_openers_next_week_table_to_df(self) -> pd.DataFrame:
        num_rows = self.excel_sheet.nrows - self.start_boundary_of_openers_next_week_table
        df_openers_next_week = pd.read_excel(self.workbook, skiprows=self.start_boundary_of_openers_next_week_table + 1, \
                                             nrows=num_rows, header=None, \
                                             usecols=[1, 2, 4])
        df_openers_next_week.columns = ["Film", "Country of Origin", "Distributor"]
        return df_openers_next_week

    @staticmethod
    def filter_for_UK_films(df_top_15: pd.DataFrame) -> pd.DataFrame:
        """
            Returns dataframe of UK films in the top 15 for merging with the UK films dataset.
        """
        mask = df_top_15["Country of Origin"].apply(lambda x: "UK" in x.split("/"))
        return df_top_15[mask]

    @staticmethod
    def filter_for_new_releases(df_top_15: pd.DataFrame) -> pd.DataFrame:
        mask = df_top_15["Weeks on release"] == 1
        return df_top_15[mask]

if __name__ == "__main__":
   #testing
   excel_parser = ExcelParser("bfi-weekend-box-office-report-2024-08-16-18.xls")
   # print("Total Weekend Gross: ", excel_parser.total_top_15_weekend_gross)
   # print("Total Gross to date: ", excel_parser.total_top_15_gross_to_date)
   # print("Other UK Films df: ", excel_parser.other_uk_films_df)
   print(excel_parser.openers_next_week_df)