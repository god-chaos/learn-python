import pytest

from common.ExcelHelper import Excel

class Test_ExcelHelper:

    def test_excel_001(self):
        excel = Excel()
        excel.open(name='./data/people.xlsx')
        print(excel.get_header('Sheet1'))
        print(excel.get_row_data('Sheet1', 10))
        print(excel.set_col_data('Sheet1', 1, [x for x in range(15)]))
        print(excel.get_col_data('Sheet1', 1))
        print(excel.get_cell_data('Sheet1', 1, 1))
        print(excel.get_sheet_data('Sheet1'))