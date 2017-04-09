import csv
import networkx as nx

G= nx.Graph()

with open('../../user_tx_graph.csv:2017-03-12') as f:
    reader = csv.reader(f)

    for row in reader:
        sender = row[0]
        recipients = row[1]
        G.add_edge(sender, recipients, weight=float(row[2])*10e-8)

nx.write_gexf(G, 'user_tx.gexf')
