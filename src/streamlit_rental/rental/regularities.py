

_REGULARITIES = [{'type': "水电煤气", 'item': "水费", "unit": '单元价', 'frequency': "每月", 'price': 6},
                 {'type': "水电煤气", 'item': "电费", "unit": '单元价', 'frequency': "每月", 'price': 1},
                 {'type': "水电煤气", 'item': "气费", "unit": '单元价', 'frequency': "每月", 'price': 0},
                 {'type': "水电煤气", 'item': "网费", "unit": '单元价', 'frequency': "每月", 'price': 0},

                 {'type': "管理", 'item': "物业管理费", "unit": '次', 'frequency': "每月", 'price': 25},
                 {'type': "管理", 'item': "垃圾费", "unit": '次', 'frequency': "每月", 'price': 0},
                 {'type': "租金", 'item': "租金", "unit": '次', 'frequency': "每月", 'price': 1000},

                 {'type': "押金", 'item': "押金", "unit": '次', 'frequency': "合同开始日", 'price': 1000}]


COL_TRANSLATION = {"type": "类型", "item": "收费项", "unit": "收费单位", "frequency": "频次", "price": "价格"}


class RegularityParser(object):

    def __init__(self, regularities=None):
        if not regularities:
            self._regularities = [_dict.copy() for _dict in _REGULARITIES]
        else:
            self._regularities = []

    def all(self):
        return self._regularities

    def filter_type(self, types):
        filtered_list = []

        for regularity in self._regularities:
            if regularity['type'] in types:
                filtered_list.append(regularity)

        return filtered_list

