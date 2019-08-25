import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Edge():
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

def show_graph(edges):
    G=nx.Graph()

    for edge in edges:
        G.add_edge(edge.frm, edge.to)
    pos = nx.random_layout(G)
    d = dict(G.degree)
    size = []
    for node in G.nodes():
        size.append(d[node]*10)
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), with_labels=False, node_color='red', node_size=size)
    nx.draw_networkx_edges(G, pos, edge_color='orange')

    labels = {}
    threshold = kLargest(d, k=5)
    for node in G.nodes():
        if d[node] > threshold:
            labels[node] = node
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=16, font_color='black')
    plt.show()

def kLargest(my_dict, k):
    sorted_x = sorted(my_dict.items(), key=lambda kv: kv[1], reverse=True)
    if len(sorted_x) > 0:
        if len(sorted_x) > k:
            return sorted_x[k][1]
        else:
            return sorted_x[len(sorted_x) - 1][1]
    else:
        return 0

def show_line_chart(x, y, xlabel, ylabel, file):
    figure = plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim=(min(y), max(y))
    plt.plot(x, y, marker='o', markerfacecolor='red', markersize=12, color='orange', linewidth=4)
    plt.show()
    figure.savefig(file)

def show_smell_distribution(smell_count, filename):
    figure = plt.figure()
    matplotlib.rc('font', weight='bold')

    # Values of each group
    bars1 = smell_count.ambigious_interface
    bars2 = smell_count.cyclic_dependency
    bars3 = smell_count.dense_structure
    bars4 = smell_count.god_component
    bars5 = smell_count.feature_concentration
    bars6 = smell_count.scattered_functionality
    bars7 = smell_count.unstable_dependency

    bars1_2 = np.add(bars1, bars2).tolist()
    bars1_3 = np.add(bars1_2, bars3).tolist()
    bars1_4 = np.add(bars1_3, bars4).tolist()
    bars1_5 = np.add(bars1_4, bars5).tolist()
    bars1_6 = np.add(bars1_5, bars6).tolist()

    # The position of the bars on the x-axis
    r = np.arange(len(bars1))

    versions = []
    for i in range (1, len(bars1) + 1):
        versions.append('V' + str(i))

    barWidth = 1
    b1 = plt.bar(r, bars1, color='#cd6155', edgecolor='#7b241c', width=barWidth * 0.8 )
    b2 = plt.bar(r, bars2, bottom=bars1, color='#707b7c', edgecolor='#212f3c', width=barWidth * 0.8)
    b3 = plt.bar(r, bars3, bottom=bars1_2, color='#bb8fce', edgecolor='#884ea0', width=barWidth * 0.8)
    b4 = plt.bar(r, bars4, bottom=bars1_3, color='#5499c7', edgecolor='#1f618d', width=barWidth * 0.8)
    b5 = plt.bar(r, bars5, bottom=bars1_4, color='#48c9b0', edgecolor='#17a589', width=barWidth * 0.8)
    b6 = plt.bar(r, bars6, bottom=bars1_5, color='#f1c40f', edgecolor='#f39c12', width=barWidth * 0.8)
    b7 = plt.bar(r, bars7, bottom=bars1_6, color='#ec7063', edgecolor='#cb4335', width=barWidth * 0.8)

    # Custom X axis
    plt.xticks(r, versions, fontweight='bold')
    plt.xlabel("Versions")
    plt.ylabel("No of architecture smells")

    plt.legend((b1[0], b2[0], b3[0], b4[0], b5[0], b6[0], b7[0]),
               ('Ambigious interface', 'Cyclic dependency', 'Dense structure', 'God component',
                'Feature concentration', 'Scattered functionality', 'Unstable dependency'))

    plt.show()
    figure.savefig(filename)


def show_component_structure(cause, filename):
    fig = plt.figure()
    edge_strings = cause.split(';')
    edges = []
    for edge_string in edge_strings:
        from_to_string = edge_string.split(' to: ')
        from_string = from_to_string[0]
        to_string = from_to_string[1]
        frm = from_string.replace('from:', '').strip()
        to = to_string.strip()
        edge = Edge(frm, to)
        edges.append(edge)
    show_graph(edges)
    fig.savefig(filename)