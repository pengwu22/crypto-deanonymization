## time /Users/SUIDANNING/spark-2.0.1-bin-hadoop2.7/bin/spark-submit network_reconstruction.py ##
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("network_reconstruction")
sc = SparkContext(conf = conf)
# sc = SparkContext()

########### load data #############
addrs = sc.textFile("addrs_intid.csv").map(lambda l: l.split(",")).map(lambda x: (int(x[0]),int(x[1]), float(x[2])))
# addrs: [payer_addr, payee_addr, amount, tx_hash]

node = sc.textFile("joint_serial_partial_node.csv").map(lambda l: l.split(",")).map(lambda x: (int(x[0]),int(x[1])))
# node: [ addr_hash, user_id]

n_user = node.values().max()
users = node.keys().collect()


# add missing nodes with
missing_payer = addrs.map(lambda x:x[1])
total_node = addrs.map(lambda x:x[0])\
    .union(missing_payer)\
    .distinct()\
    .filter(lambda x: x not in users)\
    .zipWithIndex()\
    .map(lambda x: (x[0],x[1]+n_user+1))\
    .union(node)

with open("joint_serial_total_node.csv", "w") as f1:
    for i in total_node.collect():
        f1.write(str(i[0]) + ',' + str(i[1]) + '\n')


# replace edges with full user_ids

total_edge = addrs.map(lambda x:(x[0],(x[1], x[2])))\
    .join(total_node)\
    .map(lambda x: (x[1][0][0],(x[1][1], x[1][0][1])))\
    .join(total_node)\
    .map(lambda x: ((x[1][0][0],x[1][1]), x[1][0][1]))\
    .reduceByKey(lambda x,y :x + y)


with open("joint_serial_total_edge.csv", "w") as f2:
    for i in total_edge.collect():
        f2.write(str(i[0][0]) + ',' + str(i[0][1]) + ',' + str(i[1])  + '\n')
