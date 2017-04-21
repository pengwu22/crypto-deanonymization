import csv, random

# with open("user_edge_sampled.csv",'w') as w:
#     writer = csv.writer(w)
#     with open("../blockparser/csv/user_edge.csv",'r') as r:
#         reader = csv.reader(r)
#         for i, row in enumerate(reader):
#             if random.uniform(0, 1) < 0.2:
#                 writer.writerow(row)


folder = "../../csv-2017-03-12/"
with open(folder+"addrs_sampled.csv",'w') as w:
    writer = csv.writer(w)
    with open(folder+"addrs.csv",'r') as r:
        reader = csv.reader(r)
        for i, row in enumerate(reader):
            if random.uniform(0, 1) < 0.005:
                writer.writerow(row)