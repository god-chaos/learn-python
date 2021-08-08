import copy

import pytest

from common.JsonHelper import get_one_json_node, get_json_node, set_one_json_node, set_json_node
from common.exec_time import exec_time


class TestJsonGet:
    js = {'a': 10, 'b': 20, 'c': {'e': 10, 'f': 'string'}, 'c1': {'e': {'f1': 30}, 'f': 'string'},
          'c2': {'e': 10, 'f': 'string'}, 'z': [{'z1': 10}, {'z1': 20}]}

    def test_get1(self):
        print('test')
        assert 10 == get_one_json_node(self.js, 'a')
        assert 10 == get_one_json_node(self.js, 'e')

    def test_get2(self):
        assert None == get_one_json_node(self.js, 'c.e')

    def test_get3(self):
        assert 10 == get_json_node(self.js, 'a')
        assert 10 == get_json_node(self.js, 'e')
        assert 10 == get_json_node(self.js, 'c.e')

    def test_get4(self):
        assert 10 == get_json_node(self.js, 'z.z1')


class TestJsonSet:
    js = {'a': 10, 'b': 20, 'c': {'e': 10, 'f': 'string'}, 'c1': {'e': {'f1': 30}, 'f': 'string'},
          'c2': {'e': 10, 'f': 'string'}, 'z': [{'z1': 10}, {'z1': 20}]}

    @exec_time
    def test_set1(self):
        js = copy.deepcopy(self.js)
        set_one_json_node(js, 'a', 20)
        set_one_json_node(js, 'e', 30)
        assert 20 == get_one_json_node(js, 'a')
        assert 30 == get_one_json_node(js, 'e')

    def test_set2(self):
        js = copy.deepcopy(self.js)
        set_one_json_node(js, 'c.e', 20)
        assert None == get_one_json_node(self.js, 'c.e')

    def test_set3(self):
        js = copy.deepcopy(self.js)
        set_json_node(js, 'a', 20)
        set_json_node(js, 'e', 30)
        assert 20 == get_json_node(js, 'a')
        assert 30 == get_json_node(js, 'e')
        set_json_node(js, 'c.e', 40)
        assert 40 == get_json_node(js, 'c.e')

    def test_set4(self):
        js = copy.deepcopy(self.js)
        set_json_node(js, 'z.z1', 100)
        assert 100 == get_json_node(js, 'z.z1')


if __name__ == '__main__':
    pytest.main(["-qq"], plugins=[TestJsonGet()])
    pytest.main(["-qq"], plugins=[TestJsonSet()])
