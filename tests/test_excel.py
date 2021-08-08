import pytest

from common.excel import Excel


class Test_Excel:

    def test_1(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.headers)
        print(xlsx.values)

    def test_2(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.get_col_data('车系'))
        print(xlsx.get_row_data(2))

    def test_3(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.get_col_data('官方价'))
        print(xlsx.get_row_data(2))
        xlsx.set_col_data('官方价', ['0万' for x in range(
            10)]).set_row_data(2, [0, 0, 0, 0, 0])
        print(xlsx.get_col_data('官方价'))
        print(xlsx.get_row_data(2))

    def test_4(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.get_row_data(3))
        xlsx.set_cell_data(3, 2, 'new data').set_cell_data(3, 3, 'haha')
        print(xlsx.get_row_data(3))

    def test_5(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.get_cell_data(3, '官方价'))
        print(xlsx.get_cell_data(3, 2))

    def test_6(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.filter_eq('排名', [1, 2]).values)

        print(xlsx.filter_eq('排名', 1).add(xlsx.filter_eq('排名', 2)).values)

    def test_7(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        print(xlsx.filter_not('排名', 1).filter_not('排名', 2).values)

    def test_8(self):
        xlsx = Excel()
        xlsx.read('./data/2020-suv-top10.xlsx')
        e1 = xlsx.filter_eq('排名', 1)
        e2 = xlsx.filter_eq('排名', 2)
        print(e1.add(e2).values)


if __name__ == '__main__':
    pytest.main(["-qq"], plugins=[Test_Excel()])
