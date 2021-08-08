from jsonpath_rw import parse as parserw
import jsonpath
from jsonpath_ng import parse

from common.exec_time import exec_time


def get_one_json_node(data: dict, field: str):
    if isinstance(data, list):
        for it in data:
            ret = get_one_json_node(it, field)
            if ret is not None:
                return ret

    if not isinstance(data, dict):
        return None
    if field in data.keys():
        return data[field]

    for it in data.keys():
        ret = get_one_json_node(data[it], field)
        if ret:
            return ret
    return None


@exec_time
def get_json_node(data: dict, field: str):
    node_path = field.split(".")
    node = data
    find = False
    for it in node_path:
        node = get_one_json_node(node, it)
        if not node:
            return None
        else:
            find = True

    if find:
        return node
    else:
        return None


def set_one_json_node(data: dict, field: str, value):
    if isinstance(data, list):
        for it in data:
            ret = set_one_json_node(it, field, value)
            if ret is not None:
                return ret

    if not isinstance(data, dict):
        return None
    if field in data.keys():
        data[field] = value
        return data

    for it in data.keys():
        ret = set_one_json_node(data[it], field, value)
        if ret:
            return ret
    return None


@exec_time
def set_json_node(data: dict, field: str, value):
    pos = field.find('.')
    if pos != -1:
        parent = field[0:pos]
        node = get_json_node(data, parent)
        if node is None:
            return None
        else:
            return set_one_json_node(node, field[pos + 1:], value)
    else:
        return set_one_json_node(data, field, value)


class JsonHelper:
    def __init__(self, buffer: dict):
        self.__dict__['_buffer'] = buffer

    @exec_time
    def get(self, field: str):
        if not field.startswith('$..'):
            condition = '$..' + field
        else:
            condition = field
        ret = []
        for match in parse(condition).find(self.__dict__['_buffer']):
            ret.append(match.value)

        if not ret:
            raise Exception("field:{} is not exist".format(field))
        else:
            return ret[0]

    @exec_time
    def set(self, field: str, value):
        if not field.startswith('$..'):
            condition = '$..' + field
        else:
            condition = field

        parse(condition).update(self.__dict__['_buffer'], value)
        return self

    def __getitem__(self, field):
        return self.get(field)

    def __setitem__(self, field, value):
        return self.set(field, value)

    def __getattr__(self, field):
        if field in self.__dir__() or field == '_buffer':
            return super().__getattr__(field)

        return self.get(field)

    def __setattr__(self, field: str, value):
        if field in self.__dir__() or field == '_buffer':
            super().__setattr__(field, value)
            return
        else:
            self.set(field, value)


@exec_time
def op_dict(data, field):
    data[field] = 20
    return data


@exec_time
def test_jsonpath(data, field):
    return jsonpath.jsonpath(data, field)


@exec_time
def test_jsonpathrw(data, field):
    jsonpath_expr = parserw(field)
    return jsonpath_expr.find(data)


class __JsonHelper:
    def __init__(self, buffer: dict):
        self.__dict__['_buffer'] = buffer

    def get(self, field: str):
        ret = self.__get_json_node(self.__dict__['_buffer'], field)

        if not ret:
            raise Exception("field:{} is not exist".format(field))
        else:
            return ret[0]

    def set(self, field: str, value):
        ret = self.__set_json_node(self.__dict__['_buffer'], field, value)
        if ret is None:
            raise Exception("field:{} is not exist".format(field))
        return self

    def __get_one_json_node(self, data: dict, field: str):
        if isinstance(data, list):
            for it in data:
                ret = self.__get_one_json_node(it, field)
                if ret is not None:
                    return ret

        if not isinstance(data, dict):
            return None
        if field in data.keys():
            return data[field]

        for it in data.keys():
            ret = self.__get_one_json_node(data[it], field)
            if ret:
                return ret
        return None

    def __get_json_node(self, data: dict, field: str):
        node_path = field.split(".")
        node = data
        find = False
        for it in node_path:
            node = self.__get_one_json_node(node, it)
            if not node:
                return None
            else:
                find = True

        if find:
            return node
        else:
            return None

    def __set_one_json_node(self, data: dict, field: str, value):
        if isinstance(data, list):
            for it in data:
                ret = self.__set_one_json_node(it, field, value)
                if ret is not None:
                    return ret

        if not isinstance(data, dict):
            return None
        if field in data.keys():
            data[field] = value
            return data

        for it in data.keys():
            ret = self.__set_one_json_node(data[it], field, value)
            if ret:
                return ret
        return None

    @exec_time
    def __set_json_node(self, data: dict, field: str, value):
        pos = field.find('.')
        if pos != -1:
            parent = field[0:pos]
            node = self.__get_json_node(data, parent)
            if node is None:
                return None
            else:
                return self.__set_one_json_node(node, field[pos + 1:], value)
        else:
            return self.__set_one_json_node(data, field, value)
