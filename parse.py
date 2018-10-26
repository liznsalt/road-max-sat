from k_shortest_paths import k_shortest_paths
from graph_with_value import graph_with_random_value
# import json


def parse_paths(paths):
    r"""
    TODO 因为每一个path都由许多路段组成，所以path不是最小项，须将下式化为合取范式
    TODO (path1 | path2 | ... | path?) & (path1 -> ~path2) & ... & (path?-1 -> path?)
    tip: path1 -> ~path2 <=> ~path1 | ~path2
    求(path1 | path2 | ... | path?) & (path1 -> ~path2) & ... & (path?-1 -> path?)的合取范式
    :param paths: List[List[int]]
    :return: List[List[int]]
    """
    pass


def to_dict(paths):
    r"""
    生成 road_id -> path  :   cnf.json
    :param paths: List[List[int]]
    :return: dict{int: string}
    """
    res = {i: '->'.join([str(node) for node in path])
           for i, path in enumerate(paths)}
    return res


def to_cnf(all_paths, section_count):
    r"""
    生成 .cnf 格式文件， 之后传给SatSolve可得出结果
    传入多组paths，每组paths有若干条path，每条path为(o->a1, a1->a2, ..., a.->d)
    :param all_paths: List[List[List[int]]]
    :param section_count: int
    :return: None
    """
    with open('out/result.cnf', 'w') as f:
        f.write(f'p cnf {section_count} {None}\n')
        for paths in all_paths:
            pass


if __name__ == '__main__':
    graph = graph_with_random_value()
    paths = k_shortest_paths(graph, 4, 5, 5)
    p = to_dict(paths)
    print(p)
