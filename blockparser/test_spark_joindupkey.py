"""
Usage:
~/spark/bin/spark-submit project_csds/blockparser/test_spark_joindupkey.py
"""

# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[4]").setAppName("mapinput")
sc = SparkContext(conf=conf)


left = sc.parallelize([('a',0),('a',0),('a',0),('b',0),('c',0)])
right = sc.parallelize([('a',4),('a',4),('b',8),('b',9)])
print left.keys().collect()
test = left.join(right).collect()


for i in right.groupByKey().collect():
    print i[0], i[1].data