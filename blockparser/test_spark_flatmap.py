"""
Usage:
spark-submit *.py
"""

# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[2]").setAppName("mapinput")
sc = SparkContext(conf=conf)


rawfiles = sc.parallelize(['../../blk00796.dat'])

def test(filename):
    return [(['a','b'],['c','d'],['e']),(['f','g'],['h'],['i','j']),(['k'],['l'],['m'])]

left = sc.parallelize(['abc', 'asdf'])
right = left.map(test).flatMap(lambda x:x)
for i in right.collect():
    print i

