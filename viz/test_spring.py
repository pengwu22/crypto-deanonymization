import csv
import networkx as nx
import matplotlib.pyplot as plt


G= nx.Graph()

with open('../../csv-2013-10-25/user_edge.csv') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        sender = row[0]
        recipients = row[1]
        G.add_edge(sender, recipients, weight=float(row[2])*10e-8)

        if i == 2000:
            break

pos = nx.spring_layout(G, dim=2)
nx.draw(G, pos=pos, node_size=10, node_color='b', width=0.5)
plt.show()