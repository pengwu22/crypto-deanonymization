## time /Users/SUIDANNING/spark-2.0.1-bin-hadoop2.7/bin/spark-submit als_kmeans.py ##
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark.mllib.clustering import KMeans, KMeansModel

conf = SparkConf().setAppName("ALS")
sc = SparkContext()

########### prepare data ############
data = sc.textFile("data/addrs_intid.csv")
# data = sc.textFile("test.csv")
data_amount = data.map(lambda l: l.split(","))\
    .map(lambda l: ((int(l[0]),int(l[1])), float(l[2])))\
    .reduceByKey(lambda x,y :x + y)

# data_amount: [((payer_addr, payee_addr), amount)]

##### ALS to extract features #####
ratings_amount = data_amount.map(lambda l: Rating(int(l[0][0]), int(l[0][1]), float(l[1])))
model_amount = ALS.trainImplicit(ratings_amount,rank=4, iterations=5, lambda_=0.01, alpha=1.0, seed =5L)
feature_payer = model_amount.userFeatures().persist()
# feature_payer:[(payer_addr,(d1,d2,d3,d4))]
feature_payee = model_amount.productFeatures().persist()
# feature_payer:[(payee_addr,(d1,d2,d3,d4))]

n_cluster = 27000


##### KMEANS to cluster #####
clusters = KMeans.train(feature_payer.values(), n_cluster, maxIterations=10, initializationMode="random")
labels = clusters.predict(feature_payer.values()).persist()

payers = feature_payer.keys().collect()

node_payee = feature_payee\
    .filter(lambda x: x[0] not in payers)\
    .keys()\
    .zipWithIndex()\
    .map(lambda x: (x[0],x[1]+n_cluster))
# node_payee: [payee_addr, user_id]

node_payer = feature_payer.keys().zip(labels)
# node_payer: [payer_addr, user_id (kmeans_labels)]

node = node_payer.union(node_payee).persist()
# node: [ addr ,user_id]

with open("output/kmeans_node.csv", "w") as f1:
    for i in node.collect():
        f1.write(str(i[0]) + ',' + str(i[1]) + '\n')

edge = data_amount.map(lambda x:(x[0][0],(x[0][1], x[1])))\
    .join(node)\
    .map(lambda x: (x[1][0][0],(x[1][1], x[1][0][1])))\
    .join(node)\
    .map(lambda x: ((x[1][0][0],x[1][1]), x[1][0][1]))\
    .reduceByKey(lambda x,y :x + y)

with open("output/kmeans_edge.csv", "w") as f2:
    for i in edge.collect():
        f2.write(str(i[0][0]) + ',' + str(i[0][1]) + ',' + str(i[1])  + '\n')
