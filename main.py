import matplotlib.pyplot as plt
import networkx as nx
from netgraph import Graph

QL = [] #starile
Q = 0 #numarul de stari
A = [] #alfabetul
nr = 0 #numarul de muchii/tranzitii
D = {} #functia de tranzitie
qi = 0 #starea intiala
F = [] #starile finale

def citire_DFA(nume):
    global Q, QL, A, nr, D, qi, F
    
    f = open(nume)
    QL = [x for x in f.readline().split()]
    Q = len(QL)
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


def citire_NFA(nume):
    global Q, QL, A, nr, D, qi, F
    
    f = open(nume)
    QL = [x for x in f.readline().split()]
    Q = len(QL)
    A = [x for x in f.readline().split()] 
    nr = int(f.readline())
    
    for i in range(nr):
        qi, a, qf = f.readline().split()
        if qi not in D:
            D[qi] = {a : [qf]}
        elif a not in D[qi]: 
            D[qi][a] = [qf]
        else:
            D[qi][a].append(qf)
    
    qi = f.readline().strip()
    F = [x for x in f.readline().split()]


def desen_DFA():
    global D, QL, qi, F
    #pentru a-mi desena graful nu-mi stochez ideal muchiile
    D1 = {}
    for start in D:
        for lit in D[start]:
            final = D[start][lit] #nodul in care ajungem plecand din start cu litera lit
            if start not in D1:
                D1[start] = {final : [lit]} 
                #facem toate astea fiindca dintr-un nod pot sa ajung intr-un al doilea cu mai multe cifre
            elif final not in D1[start]:
                D1[start][final] = [lit]
            else:
                D1[start][final].append(lit)
    #ne-am creat un nou dictionar de forma:
    #{nod_start : {nod_final : [literele prin care se ajunge de la nod_start la nod_final]}}

    G = nx.DiGraph()
    for start in D1:
        for final in D1[start]:
            G.add_edge(start, final, label = ', '.join([str(x) for x in D1[start][final]]))
    edge_labels = nx.get_edge_attributes(G, 'label')

    pos = nx.planar_layout(G)

    #adaugam culori pt a identifica nodurile speciale
    colors = {}
    for nod in QL:
        if nod in F:
            colors[nod] = '#337bb8'
        elif nod == qi:
            colors[nod] = '#9fc5e5'
        else:
            colors[nod] = '#63a0d4'

    Graph(G, node_layout = pos, edge_layout = 'curved', origin = (-1, -1), scale = (2, 2),
        node_color = colors, node_size = 8, node_labels = True, node_label_fontdict = dict(size = 10),
        edge_labels = edge_labels, edge_label_fontdict = dict(size = 10), edge_label_position = 0.7, arrows = True
    )
    plt.show()


def desen_NFA():
    global D, QL
    #pentru a-mi desena graful nu-mi stochez ideal muchiile
    D1 = {}
    for start in D:
        for lit in D[start]: #acum trebuie sa iau in considerare faptul ca D[start][lit] e o lista
            for final in D[start][lit]:
                if start not in D1:
                    D1[start] = {final : [lit]} 
                    #facem toate astea fiindca dintr-un nod pot sa ajung intr-un al doilea cu mai multe cifre
                elif final not in D1[start]:
                    D1[start][final] = [lit]
                else:
                    D1[start][final].append(lit)
    #ne-am creat un nou dictionar de forma:
    #{nod_start : {nod_final : [literele prin care se ajunge de la nod_start la nod_final]}}

    G = nx.DiGraph()
    for start in D1:
        for final in D1[start]:
            G.add_edge(start, final, label = ', '.join([str(x) for x in D1[start][final]]))
    edge_labels = nx.get_edge_attributes(G, 'label')

    pos = nx.planar_layout(G)
    
    #adaugam culori pt a identifica nodurile speciale
    colors = {}
    for nod in QL:
        if nod in F:
            colors[nod] = '#337bb8'
        elif nod == qi:
            colors[nod] = '#9fc5e5'
        else:
            colors[nod] = '#63a0d4'
    
    Graph(G, node_layout = pos, edge_layout = 'curved', origin = (-1, -1), scale = (2, 2),
        node_color = colors, node_size = 8, node_labels = True, node_label_fontdict = dict(size = 10),
        edge_labels = edge_labels, edge_label_fontdict = dict(size = 10), edge_label_position = 0.7, arrows = True
    )
    plt.show()


def test_DFA(cuv):
    global A, D, qi, F
    respins = 0
    i = 0
    drum = [qi]
    sc = qi #starea curenta
    while i < len(cuv):
        su = D[sc].get(cuv[i], -1) #starea urmatoare
        if su == -1:
            respins = 1
            break
        else:
            sc = su
            drum.append(sc)
            i += 1
    #daca pe parcurs n-am mai gasit tranzitie / nu terminam intr-o stare finala
    if respins == 1 or drum[len(drum) - 1] not in F: 
        return 0, []
    else:
        return 1, drum


def test_NFA(cuv):
    global A, D, qi, F
    drum = [[qi]]

    def verificare(drumuri, i):
        if i < len(cuv):
            drumuri_viitoare = []
            for j in range(len(drumuri)):
                #pt fiecare drum partial pe care il avem luam un vector de viitoare stari prosibile valabile
                if drumuri[j][len(drumuri[j]) - 1] in D:
                    su = D[drumuri[j][len(drumuri[j]) - 1]].get(cuv[i], -1)
                    if su != -1:
                        #avem in su toate starile in care putem ajunge cu cuv[i] din ultima stare a drumului
                        #la care suntem
                        drum_temp = []
                        for k in range(len(su)):
                            drum_temp = drumuri[j].copy()
                            drum_temp.append(su[k])
                            drumuri_viitoare.append(drum_temp)
                            #adaugam noile drumuri 
            return verificare(drumuri_viitoare, i + 1)
        else:
            return drumuri
        
    drum = verificare(drum, 0)

    drumuri_finale = []
    #verificam daca vreunul dintre drumurile obtinute ajung intr-un punct final
    for i in range(len(drum)):
        if drum[i][len(drum[i]) - 1] in F:
            drumuri_finale.append(drum[i])
    
    if len(drumuri_finale) == 0:
        return 0, []
    else:
        return 1, drumuri_finale


teste = [test_NFA, test_DFA]
#citim automatul
cerinta = int(input("Citim un AFD? \n[0/1]: "))
nume = input("Dati numele fisierului ce contine automatul: ")

if cerinta == 1:
    citire_DFA(nume)
    desen_DFA()
else:
    citire_NFA(nume)
    desen_NFA()


#trestam apartenenta cuvintelor la limbaj
k = 1
while k:
    cuv = input("\nDati cuvantul: ")
    apartine, drum = teste[cerinta](cuv)
    
    if apartine:
        print("Cuvant acceptat!") 
        if cerinta == 1:
            print("Drumul parcurs este: ", end = '')
            print(*drum)
        elif cerinta == 0 and len(drum) == 1:
            print("Drumul parcurs este: ", end = '')
            print(*drum[0])
        else:
            print("Drumurile parcurse sunt: ")
            for i in range(len(drum)):
                print(" - ", *drum[i])
    
    else:
        print("Cuvant respins!")

    k = int(input("\nVreti sa mai testati un cuvant? \n[0/1]: "))