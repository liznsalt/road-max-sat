import json

import matplotlib.pyplot as plt
import networkx as nx


def get_point_data():
    r"""得到点的信息"""
    with open('out/nodes.json', 'r') as f:
        res = json.load(f)
    return res


def get_graph():
    pos = get_point_data()
    G = nx.Graph()
    with open('out/roads.txt', 'r') as f:
        for line in f:
            data = line.split()
            if data[0] == 'e':
                _, e1, e2 = data
                G.add_node(e1, pos=pos[e1])
                G.add_node(e2, pos=pos[e2])
                G.add_edge(e1, e2)
                G.add_edge(e2, e1)
    return G


def draw(G):
    r"""画出厦门市的路网"""
    pos = get_point_data()
    nx.draw(G, pos=pos)
    plt.xlim(118.066, 118.197)
    plt.ylim(24.424, 24.561)
    plt.show()
    # plt.savefig('out/graph.png', dpi=300)


def get_final_graph():
    r"""去掉多余点并且做出映射后的图"""
    G = get_graph()
    pos = get_point_data()
    final_G = nx.Graph()
    # 映射: 原id -> 排序后的id
    g = {Id: i for i, Id in enumerate(sorted(G.nodes, key=int))}
    for edge in G.edges:
        e1, e2 = edge
        final_G.add_node(g[e1], pos=pos[e1])
        final_G.add_node(g[e2], pos=pos[e2])
        final_G.add_edge(g[e1], g[e2])
        final_G.add_edge(g[e2], g[e1])
    return final_G


if __name__ == '__main__':
    draw(get_graph())
    print('Draw done!')
