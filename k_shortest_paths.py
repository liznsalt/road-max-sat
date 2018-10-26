import networkx as nx

from graph_with_value import graph_with_random_value


def k_shortest_paths(G, o, d, k):
    r"""返回o到d的前k短路径，不存在的返回空列表"""
    try:
        paths = nx.shortest_simple_paths(G, o, d)
        res = []
        i = 0
        for path in paths:
            res.append(path)
            i += 1
            if i >= k:
                break
        return res
    except nx.exception.NetworkXNoPath:
        print(f'No this path between node {o} and node {d}')
        return []


if __name__ == '__main__':
    G = graph_with_random_value()
    print('Graph -')
    for i, path in enumerate(k_shortest_paths(G, 50, 70, 10)):
        print(f'{i}: {path}: {len(path)-1}')
