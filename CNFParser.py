"""
初始化:
>>>graph = graph_with_random_value()
>>>cnf_parser = CNFParser(graph, od_set=[(4, 5)])
或
>>>cnf_parser = CNFParser(graph)
>>>cnf_parser.get_od_set([(4, 5)])
处理:
>>>cnf_parser.parse_od_set() # 分析OD集
>>>cnf_parser.get_cnf_list() # 得到cnf格式列表
保存为文件:
>>>cnf_parser.save_to('out/test.cnf')
查看分析结果:
>>>cnf_parser.max_sat_description()
"""
import os

import networkx as nx

from graph_with_value import graph_with_random_value
from k_shortest_paths import k_shortest_paths

MAX_VALUE = 10000


def _fmt(node1, node2):
    return str(node1) + '->' + str(node2)


def _save_road(roads: dict, get_road_id: dict, road_cnt: int, node1, node2):
    idx = road_cnt + 1
    roads[idx] = [node1, node2]
    get_road_id[_fmt(node1, node2)] = idx
    get_road_id[_fmt(node2, node1)] = idx


def _save_path(paths, path_cnt, fmt_path):
    paths[path_cnt + 1] = fmt_path


def _with_value(lst, value: 'int > 0'=MAX_VALUE):
    return [value, lst]


def _have_road(path, road):
    node1, node2 = road
    return (_fmt(node1, node2) in path) or (_fmt(node2, node1) in path)


class CNFParser:

    def __init__(self, graph: nx.Graph, od_set=None):
        self.graph = graph
        if od_set is None:
            self.od_set = list()
        else:
            self.od_set = od_set
        # 路段保存
        self.roads = dict() # {id: [node1, node2]}
        self.get_road_id = dict()
        self._road_cnt = 0
        # 路径保存
        self.paths = dict()
        self.od_path = list()
        self._path_cnt = 0
        # cnf样式: [ [ value, [.|.|.] ] ...]
        self.cnf_list = list()

    def get_od_set(self, od_set: list):
        r"""得到od集"""
        self.od_set = od_set

    def _to_dict(self, paths):
        # path: [n1, n2, ..., ni]
        # 首先添加每个od集的paths
        add_paths = list(range(self._path_cnt + 1, self._path_cnt + len(paths) + 1))
        self.od_path.append(add_paths)
        # print(add_paths)
        for path in paths:
            fmt_path = []
            for n1, n2 in zip(path, path[1:]):
                if _fmt(n1, n2) not in self.get_road_id:
                    # 保存两点, 即一条边
                    _save_road(self.roads, self.get_road_id, self._road_cnt, n1, n2)
                    # 路段加1
                    self._road_cnt += 1
                fmt_path.append(_fmt(n1, n2))
            _save_path(self.paths, self._path_cnt, fmt_path)
            # 路径加1
            self._path_cnt += 1

    def parse_od_set(self, get_paths_func=k_shortest_paths, k=5, alpha=0.2):
        factor = k
        for o, d in self.od_set:
            paths = get_paths_func(self.graph, o, d, factor)
            self._to_dict(paths)

    def _parse_paths(self, paths: list):
        # path_cnt = len(paths)
        self.cnf_list.append(_with_value([x for x in paths]))
        for i in paths:
            for j in paths:
                if i != j:
                    self.cnf_list.append(_with_value([-i, -j]))

    def _parse_roads(self):
        for road in self.roads.values():
            node1, node2 = road
            # 求当前路段id
            road_id = self.get_road_id[_fmt(node1, node2)] + self._path_cnt
            have_this_road_paths = []
            for idx, path in self.paths.items():
                if _have_road(path, road):
                    have_this_road_paths.append(idx)
                    # path->当前路段
                    self.cnf_list.append(_with_value([-idx, road_id]))
            have_this_road_paths.append(-road_id)
            self.cnf_list.append(_with_value(have_this_road_paths))

    def _add_assume(self):
        r"""添加全部边的id，假设它们都可以经过，则将多解问题转化为无解问题"""
        for road in self.roads.values():
            node1, node2 = road
            road_id = self.get_road_id[_fmt(node1, node2)] + self._path_cnt
            self.cnf_list.append(_with_value([road_id],
                                             value=self.graph[node1][node2]['value']))

    def get_cnf_list(self):
        for paths in self.od_path:
            self._parse_paths(paths)
        self._parse_roads()
        self._add_assume()

    def save_to(self, file):
        r"""看后缀写入文件"""
        if file[-4:] == '.cnf':
            fmt = 'cnf'
        else:
            fmt = 'wcnf'
        with open(file, 'w') as f:
            if fmt == 'wcnf':
                f.write('c\nc comments Weighted Max-SAT\nc\n')
            f.write(f'p {fmt} {self._road_cnt + self._path_cnt} {len(self.cnf_list)}\n')
            for cl in self.cnf_list:
                value, factors = cl
                if fmt == 'wcnf':
                    f.write(f'{value} ')
                for factor in factors:
                    f.write(f'{factor} ')
                f.write('0\n')

    def _value(self, path_id):
        r"""获得此边的值"""
        path = self.paths[path_id]
        value = 0
        for road in path:
            road_id = self.get_road_id[road]
            node1, node2 = self.roads[road_id]
            value += self.graph[node1][node2]['value']
        return value

    def max_sat(self):
        r"""TODO:
        :return [max_value, [path-id list]]
        """
        if os.getcwd() == 'D:\\road-network':
            os.chdir('sat4j')
        message = os.popen('java -jar sat4j-maxsat.jar ../out/result.wcnf').readlines()[-3]
        message = message.split(' ')
        path_result = [int(x) for x in message[1:self._path_cnt+1]]
        value = sum([self._value(x) for x in path_result if x > 0])
        return [value, [x for x in path_result if x > 0], [x for x in path_result if x < 0]]

    def max_sat_description(self):
        r"""描述结果"""
        ms = self.max_sat()
        return '值={}, 经过的路径编号:{!r}, 不经过的路径编号:{!r}'.format(ms[0], ms[1], ms[2])

    def max_sat_result_show(self, draw_graph=False):
        r"""TODO: 可提供画图，将经过的边标红
        """
        ms = self.max_sat()
        print('值={}, 经过的路径编号:{!r}, 不经过的路径编号:{!r}'.format(ms[0], ms[1], ms[2]))
        pass


if __name__ == '__main__':
    # (4, 5), (100, 120), (90, 400), (50, 70)
    cnf_parser = CNFParser(graph_with_random_value(),
                           od_set=[(4, 5), (100, 120), (90, 400), (50, 70)])
    cnf_parser.parse_od_set()
    cnf_parser.get_cnf_list()

    # test
    # print(cnf_parser.od_path)
    # print('-Paths:')
    # for path_id, path in cnf_parser.paths.items():
    #     print(f'{path_id}: {path}')
    # for i in cnf_parser.cnf_list:
    #     print(i[1])

    print(f'Total {len(cnf_parser.paths)} paths.')
    cnf_parser.save_to('out/result.wcnf')
    print('Generate cnf file done!\n')

    print('Parse result:')
    print(cnf_parser.max_sat_description())
    # print(os.getcwd())
    # os.chdir('sat4j')
    # result = os.popen('java -jar sat4j-maxsat.jar ../out/result.wcnf').readlines()
    # for line in result:
    #     print(line)
