"""
Usage:
~/spark/bin/spark-submit project_csds/blockparser/test_spark_joindupkey.py
"""

# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[4]").setAppName("mapinput")
sc = SparkContext(conf=conf)


left = sc.parallelize([('a',1),('a',2),('a',3),('b',1)])
right = sc.parallelize([('a',4),('a',5),('b',8),('b',9)])
print left.keys().collect()
test = left.join(right).collect()
for i in test:
    print i

