# -*- coding: utf-8 -*-
"""

This code can visualize the micro structures and patterns 
of the bitcoin transactions. Given a hash (transaction id),
the code plots the transaction tree by tracing its parents
and sons of the given node of transaction.

Explicit Dependency:
    * PIP packages: pandas, networkx, matplotlib

Implicit Dependency:
    * PIP packages: pydot, pydotplus
    * Application: graphviz (as a brew package in MAC OS)

Input CSV File Format Without Header line:
    * transactions.csv: hash (str), value (int),
                        timestamp (%Y-%m-%dT%H:%M:%S),
                        vin_size (int), vout_size (int)
    * viz_txedge.csv:   from_hash (str), value (int)
                        to_hash (str), timestamp
                            

Usage:
    1. Satisfy all above dependencies
    2. Below in the MODIFIABLE PART:
        @target: the hash of the target transaction node
        @levels_down: how many downside tree levels wanted
        @levels_up: how many upside tree levels wanted
        @input_file_folder
    3. Put the CSV files in the input file folder
    4. # python tx_structure.py
    5. Wait the program to plot!


Author: Peng Wu
License: MIT

"""

import math

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


############## MODIFIABLE PART #############
target = '85e78d04ab8f94bc7e59dd9ad188bc426698842ce5ec50e1a0d19e386b8677ec'
levels_down = 1
levels_up = 1
input_file_folder = "../../csv-2013-10-25/"
##############################################


txnodes = pd.read_csv(input_file_folder+"transactions.csv",
                      names=['hash', 'value', 'timestamp', 'vin_size', 'vout_size'])
txnodes.timestamp = pd.to_datetime(txnodes.timestamp, format='%Y-%m-%dT%H:%M:%S')


txedges = pd.read_csv(input_file_folder+"viz_txedge.csv",
                      names=['from_hash', 'value', 'to_hash', 'timestamp'])
txedges.timestamp = pd.to_datetime(txedges.timestamp, format='%Y-%m-%dT%H:%M:%S')


G = nx.from_pandas_dataframe(txedges, 'from_hash', 'to_hash', edge_attr=['value', 'timestamp'],
                             create_using=nx.DiGraph())


nodes_childs = []
level = [target]
for depth in range(levels_down):
    level = sum([G.neighbors(n) for n in level], [])
    nodes_childs += level


rG = G.reverse()
nodes_parents = []
level = [target]
for depth in range(levels_up):
    level = sum([rG.neighbors(n) for n in level], [])
    nodes_childs += level


subnodes = [target] + nodes_parents + nodes_childs
H = G.subgraph(subnodes)


nodesize = [txnodes.loc[txnodes['hash'] == n]['value'].values[0] for n in subnodes]
nodesize = [int((math.log(i)/10) ** 6) for i in nodesize]
nodecolor = ['b'] + ['r'] * (len(subnodes) - 1)


edgelabels = {}
for u, v in H.edges():
    edgelabels[(u, v)] = H[u][v]['timestamp']


######
# pip-dependencies: pydot, pydotplus
# brew-dependencies: graphviz
nx.drawing.nx_pydot.write_dot(H, 'test.dot')
pos = nx.drawing.nx_pydot.graphviz_layout(H, prog='dot')
######


nx.draw_networkx(H, pos, with_labels=False, nodelist=subnodes, node_size=nodesize, node_color=nodecolor, alpha=0.7, width=1)
nx.draw_networkx_edge_labels(H, pos, edge_labels=edgelabels, font_size=3)
plt.axis('off')
plt.show()
