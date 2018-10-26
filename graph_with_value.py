import random

from xiamen_graph import get_final_graph


def write_to_file(G):
    r"""保存为 roads_with_value.txt"""
    with open('out/roads_with_value.txt', 'w', encoding='utf-8') as f:
        f.write(f'{len(G.nodes)}\n\n')
        for edge in G.edges:
            e1, e2 = edge
            f.write('{} {} {}'.format(e2, e1, G[e2][e1]['value']) + '\n')
            f.write('{} {} {}'.format(e1, e2, G[e1][e2]['value']) + '\n')


def graph_with_random_value():
    G = get_final_graph()
    for edge in G.edges:
        e1, e2 = edge
        G[e1][e2]['value'] = random.randint(1, 10)
    write_to_file(G)
    return G


def graph_with_real_value():
    pass


if __name__ == '__main__':
    graph_with_random_value()
    print('Generate random value done!')
