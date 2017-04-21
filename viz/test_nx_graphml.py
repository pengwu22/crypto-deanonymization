import networkx as nx
G = nx.DiGraph()
import csv
with open('../../csv-2017-03-09/user_edge.csv') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        sender = row[0]
        recipients = row[1]
        G.add_edge(sender, recipients, weight=float(row[2]) * 10e-8)

        if i == 8000:
            break


nx.write_graphml(G, 'user_edge.xml')
