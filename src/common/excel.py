from typing import List, Union

import pandas as pd
from pandas.core.frame import DataFrame


class Excel:
    """
    excel和csv操作类型
    """

    def __init__(self, df: pd.DataFrame = None):
        """
        构造函数
        @param: df ([DataFrame], optional): pandas.DataFrame类型
        """
        self.df = df

    @property
    def headers(self):
        """
        表头属性

        @return: [list]: [返回表头]
        """
        return list(self.df.columns)

    @property
    def values(self):
        """
        表数据获取

        @return: [numpy.ndarray]: [返回表数据]
        """
        return self.df.values

    @property
    def row_count(self):
        """
        获取行数

        @return: [int]: [返回记录数]
        """
        return len(self.df.values)

    @property
    def col_count(self):
        """
        获取列数

        @return: [int]: [返回列数]
        """
        return len(self.headers)

    def read(self, file_name: str, sheet_name: str = "Sheet1", sep: str = ',', encoding='utf-8'):
        """
        读取excel或者csv文件

        @param: file_name (str): [文件名]
        @param: sheet_name (str, optional): [sheet名称]. Defaults to "Sheet1".
        @param: sep (str, optional): [分隔符，只有对csv文件有效]. 默认值','.
        @param: encoding (str, optional): [csv文件的编解码]. 默认值'utf-8'.
        @raise: Exception: [文件不支持]
        """
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            self.df = pd.read_excel(io=file_name, sheet_name=sheet_name)
        elif file_name.endswith('.csv'):
            self.df = pd.read_csv(io=file_name, sep=sep, encoding=encoding)
        else:
            raise Exception(
                f'just support csv and xlsx type file: {file_name}')

    def write(self, file_name: str, sheet_name: str = "Sheet1", sep: str = ',', encoding='utf-8'):
        """
        写入excel或者csv文件

        @param: file_name (str): [文件名]
        @param: sheet_name (str, optional): [sheet名称]. 默认值"Sheet1".
        @param: sep (str, optional): [分隔符，只有对csv文件有效]. 默认值','.
        @param: encoding (str, optional): [编解码]. 默认值'utf-8'.
        @raise: Exception: [文件类型不支持]
        """
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            self.df.to_excel(io=file_name, sheet_name=sheet_name)
        elif file_name.endswith('.csv', sep=sep, encoding=encoding):
            self.df.to_csv(file_name)
        else:
            raise Exception(
                f'just support csv and xlsx type file: {file_name}')

    def get_col_data(self, col_name: str):
        """
        获取列数据

        @param: col_name (str): [列名]

        @return: [list]: [列数据]
        """
        return self.df[col_name].to_list()

    def get_row_data(self, row_index: int):
        """
        获取行数据

        @param: row_index (int): [行号]

        @return: [list]: [一行数据]
        """
        ret = list()
        for it in self.df.iloc[row_index]:
            ret.append(it)
        return ret

    def set_col_data(self, col_name: str, col_data: list):
        """
        设置列数据

        @param: col_name (str): [类名]
        @param: col_data (list): [列数据]
        @return: [Excel]: [返回Excel对象]
        """
        # 这里要确保col_data的长度与行数相当，可以增加检查
        for index, data in enumerate(col_data):
            self.df[col_name][index] = data
        return self

    def set_row_data(self, row_index: int, row_data: list):
        """
        设置一行数据

        @param: row_index (int): [行号]
        @param: row_data (list): [行数据]
        @return: [Excel]: [返回Excel对象]
        """
        # 这里要使用Series类型（跟dict类似），row_data长度要与列个数相等
        new_row = pd.Series(row_data, self.headers)
        self.df.iloc[row_index] = new_row
        return self

    def get_cell_data(self, row_index: int, col: Union[int, str]):
        """
        获取单元格数据

        @param: row_index ([int]): [行号]
        @param: col (Union[int, str]): [列号，或者列名称]
        @return: [any]: [数据]
        """
        if type(col) is int:
            return self.df.iloc[row_index][col]
        else:
            return self.df.at[row_index, col]

    def set_cell_data(self, row_index: int, col: Union[int, str], cell_data):
        """
        设置单元格数据

        @param: row_index ([int]): [行号]
        @param: col (Union[int, str]): [列号，或者列名称]
        @param: cell_data ([type]): [单元格数据]
        @return: [Excel]: [返回Excel对象]
        """
        # df的set_value方法好像改成_set_value，_开头标识私有，我们还是使用at方法
        if type(col) is int:
            self.df.at[row_index, self.headers[col]] = cell_data
        else:
            self.df.at[row_index, col] = cell_data

        return self

    def set_data(self, data: dict):
        """
        设置数据

        @param: data 数据
        @return: [Excel]: [返回Excel对象]
        """
        df = DataFrame(data)
        self.df = df
        return self

    def filter_eq(self, col_name, col_data: Union[any, list]):
        """
        按照列值，按照相等过滤

        @param: col_name ([str]): [列名]]
        @param: col_data (Union[any, list]): [数据，或者数据]
        @return: [Excel]: [返回Excel类型]
        """
        if type(col_data) is not list:
            df = self.df[self.df[col_name] == col_data]
            return Excel(df)

        df_list = list()
        for it in col_data:
            df = self.df[self.df[col_name] == it]
            df_list.append(df)

        # 需要忽略index
        df_result = pd.concat(df_list, ignore_index=True)
        return Excel(df_result)

    def filter_not(self, col_name, col_data: any):
        """
        按照列值，进行!=条件过滤

        @param: col_name ([str]): [列名]
        @param: col_data ([any]): [值]
        @return: [Excel]: [Excel对象]
        """
        df = self.df[self.df[col_name] != col_data]
        return Excel(df)

    def filter_lt(self, col_name, col_data, eq=False):
        """
        按照列值，<或者<=过滤

        @param: col_name ([str]): [列名]
        @param: col_data ([any]): [值]
        @param: eq (bool, optional): [=标志]. 默认值是False.
        @return: [Excel]: [Excel对象]
        """
        if eq:
            df = self.df[self.df[col_name] <= col_data]
        else:
            df = self.df[self.df[col_name] < col_data]
        return Excel(df)

    def filter_gt(self, col_name, col_data, eq=False):
        """
        按照列值，>或者>=过滤

        @param: col_name ([str]): [列名]
        @param: col_data ([any]): [值]
        @param: eq (bool, optional): [=标志]. 默认值是False.
        @return: [Excel]: [Excel对象]
        """
        if eq:
            df = self.df[self.df[col_name] >= col_data]
        else:
            df = self.df[self.df[col_name] > col_data]
        return Excel(df)

    def filter_in(self, col_name: str, col_data: Union[str, List[str]]):
        """
        按照列值，通过包含条件过滤

        @param: col_name (str): [列名]
        @param: col_data (Union[str, List[str]]): [值，值list]]
        @return: [Excel]: [Excel对象]
        """
        if type(col_data) is not list:
            return Excel(self.df[self.df[col_name].str.contains(col_data, na=False, case=False)])

        con = ''
        for it in col_data:
            con = con + it + "|"
        con = con[:-1]
        return Excel(self.df[self.df[col_name].str.contains(con, na=False, case=False)])

    def filter_notin(self, col_name: str, col_data: Union[str, List[str]]):
        """
        按照列值，通过不包含条件过滤

        @param: col_name (str): [列名]
        @param: col_data (Union[str, List[str]]): [值，值list]]
        @return: [Excel]: [Excel对象]
        """
        if type(col_data) is not list:
            return Excel(self.df[~self.df[col_name].str.contains(col_data, na=False, case=False)])

        con = ''
        for it in col_data:
            con = con + it + "|"
        con = con[:-1]
        return Excel(self.df[~self.df[col_name].str.contains(con, na=False, case=False)])

    def add(self, right: 'Excel'):
        """
        同一个表的，两个数据进行相加

        @param right: [Excel对象]
        @return: [Excel]: [返回Excel对象]
        """
        df_list = [self.df, right.df]
        # 需要忽略index
        df_result = pd.concat(df_list, ignore_index=True)
        return Excel(df_result)

    def sub(self, right: 'Excel'):
        """
        同一个表的，两个数据进行相减

        @param: right (Excel): [Excel对象]
        @return: [Excel]: [返回Excel对象]
        """
        df = pd.concat(self.df, right.df, right.df).drop_duplicates(keep=False)
        return Excel(df)

    def intersection(self, right: 'Excel'):
        """
        同一个表的，两个数据进行交集

        @param: right (Excel): [Excel对象]
        @return: [Excel]: [返回Excel对象]
        """
        df = pd.merge(self.df, right.df, how='inner')
        return Excel(df)

    def union(self, right: 'Excel'):
        """
        同一个表的，两个数据进行并集

        @param: right (Excel): [Excel对象]
        @return: [Excel]: [返回Excel对象]
        """
        df = pd.merge(self.df, right.df, how='outer')
        return Excel(df)

    def subset(self, row_begin, row_end, col_begin, col_end):
        """
        获取表的子集

        @param: row_begin ([type]): [开始行号]
        @param: row_end ([type]): [结束行号]
        @param: col_begin ([type]): [开始列]
        @param: col_end ([type]): [结束列]
        @return: [Excel]: [返回Excel对象]
        """
        df = self.df.iloc[row_begin:row_end, col_begin:col_end]
        return Excel(df)
