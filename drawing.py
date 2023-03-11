import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

Q = 0 #numarul de stari
A = [] #alfabetul
nr = 0 #numarul de muchii/tranzitii
D = {} #functia de tranzitie
qi = 0 #starea intiala
F = [] #starile finale

def citire_DFA(nume):
    global Q, A, nr, D, qi, F
    
    f = open(nume)
    Q = int(f.readline()) 
    A = [x for x in f.readline().split()] 
    nr = int(f.readline())
    
    for i in range(nr):
        qi, a, qf = f.readline().split()
        if qi not in D:
            D[qi] = {a : qf}
        else: 
            D[qi][a] = qf
    
    qi = f.readline().strip()
    F = [x for x in f.readline().split()]

#citim automatul
cerinta = int(input("Citim un AFD? \n[0/1]: "))
nume = input("Dati numele fisierului ce contine automatul: ")

if cerinta == 1:
    citire_DFA(nume)

G = nx.DiGraph()

nodes = np.arange(0, Q).tolist()

G.add_nodes_from(nodes)

for i in D:
    for a in D[i]:
        G.add_edges_from([(i, D[i][a])])

pos = {}
x = 10
y = 10
for i in range(Q):
    pos[i] = (x, y)
    y += 10

labels = {}
for i in range(Q):
    labels[i] = "q" + str(i)

nx.draw_networkx(G, pos = pos, labels = labels, arrows = True, node_shape = "s", node_color = "white")
plt.show()