#am descoperit netgraph -- imbunatateste vizualizarea considerabil

import matplotlib.pyplot as plt
import networkx as nx
from netgraph import Graph

G = nx.DiGraph() #empty graph
G.add_edge('A', 'B', label = 'a')
G.add_edge('A', 'C', label = 'b')
G.add_edge('C', 'B', label = 'b')
G.add_edge('B', 'A', label = 'a')
G.add_edge('A', 'A', label = 'b')
edge_labels = nx.get_edge_attributes(G, 'label')

#spring_layout e luat din documentatie
#pozitioneaza nodurile din graf random (pt noi, el se foloseste de fapt de un anumit algoritm)
pos = nx.planar_layout(G)

#node_label_fontdict si edge_label_fotndict se ocupa de stilizarea marginilor
Graph(G, node_layout = pos, edge_layout = 'curved', origin = (-1, -1), scale = (2, 2),
      node_color = '#63a0d4', node_size = 8, node_labels = True, node_label_fontdict = dict(size = 10),
      edge_labels = edge_labels, edge_label_fontdict = dict(size = 10), edge_label_position = 0.3, arrows = True
)
plt.show()