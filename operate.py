from random import randint

import matplotlib.pyplot as plt
import networkx as nx

from k_shortest_paths import k_shortest_paths
from graph_with_value import graph_with_random_value


def draw(graph: nx.Graph):
    r"""画出路网"""
    # 得到点的坐标
    pos = nx.get_node_attributes(graph, 'pos')
    # 两个图，一个标红，一个正常
    graph_red = nx.Graph()
    graph_normal = nx.Graph()
    for edge in graph.edges:
        e1, e2 = edge
        if 'color' in graph[e1][e2]:
            graph_red.add_nodes_from([e1, e2])
            graph_red.add_edge(e1, e2)
        else:
            graph_normal.add_nodes_from([e1, e2])
            graph_normal.add_edge(e1, e2)

    nx.draw(graph_red, pos, edge_color='red')
    nx.draw(graph_normal, pos)
    plt.xlim(118.066, 118.197)
    plt.ylim(24.424, 24.561)
    plt.show()


def random_od_set(graph: nx.Graph, k=5, cnt=10):
    r"""返回若干个od集"""
    node_cnt = len(graph.nodes)
    res = []
    while len(res) < cnt:
        o = randint(0, node_cnt)
        d = randint(0, node_cnt)
        if o == d:
            continue
        if k_shortest_paths(graph, o, d, k):
            res.append((o, d))
    return res
