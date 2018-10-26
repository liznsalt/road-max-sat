import json

import osmium as osm
import networkx as nx


class OSMHandler(osm.SimpleHandler):

    def __init__(self):
        super(OSMHandler, self).__init__()
        self.G = nx.Graph()

    def node(self, n):
        lon, lat = str(n.location).split('/')
        self.G.add_node(n.id, pos=(lon, lat))

    def way(self, w):
        for i, n in enumerate(w.nodes):
            if i != len(w.nodes) - 1:
                a, b = n.ref, w.nodes[i+1].ref
                self.G.add_edge(a, b)
                self.G.add_edge(b, a)

    # 暂时不处理relation
    def relation(self, r):
        pass


def write_to_file(osmhandler):
    # 映射: 原id -> 排序后的id
    g = {Id: i for i, Id in enumerate(sorted(osmhandler.G.nodes, key=int))}

    # 存储点的坐标 nodes.json
    with open('out/nodes.json', 'w') as f:
        nodes = {i: osmhandler.G.nodes[Id]['pos']
                 for i, Id in enumerate(sorted(osmhandler.G.nodes, key=int))}
        json.dump(nodes, f, ensure_ascii=False,
                  indent=4, separators=(',', ': '))

    # 保存为DIMACS格式 roads.txt
    with open('out/roads.txt', 'w', encoding='utf-8') as f:
        f.write('c XiaMen graph\n')
        f.write(f'p edge {len(osmhandler.G.nodes)} {len(osmhandler.G.edges)}\n')
        # 记录各边
        for edge in osmhandler.G.edges:
            e1, e2 = edge
            f.write(f'e {g[e1]} {g[e2]}\n')


def main():
    osmhandler = OSMHandler()
    osmhandler.apply_file('data/map.osm')
    write_to_file(osmhandler)


if __name__ == '__main__':
    main()
    print('Generate XiaMen Graph done!')
