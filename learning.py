#am invatat care e faza cu networkx -- nu e chiar ce trebuie pana la urma

import networkx as nx 
import matplotlib.pyplot as plt

G = nx.DiGraph() #empty graph
#adaugam margini intre perechile din lista de tupluri
G.add_weighted_edges_from([('A', 'B', 'a'), ('A', 'C', 'b'), ('C', 'B', 'a'), ('B', 'A', 'b')])
labels = nx.get_edge_attributes(G, 'weight') #weight-ul nostru va fi de fapt litera 

#spring_layout e luat din documentatie
#pozitioneaza nodurile din graf random (pt noi, el se foloseste de fapt de un anumit algoritm)
pos = nx.planar_layout(G)

#desenam elementele
nx.draw_networkx_nodes(G, pos, node_size = 500, node_color = '#63a0d4') #pretty blue color =)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist = G.edges(), edge_color = 'black', connectionstyle = 'arc3, rad=0.1')
nx.draw_networkx_edge_labels(G, pos, edge_labels = labels, font_size = 50)
plt.show()