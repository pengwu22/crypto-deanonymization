"""
Usage:
~/spark/bin/spark-submit project_csds/blockparser/spark_mapinput.py
"""

# Initialize Timer
import time

start_time = time.time()

# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[4]").setAppName("mapinput")
sc = SparkContext(conf=conf)


# Loading files
def parse_outputs(line):
    """
    schema:
        txhash, nid, value, addr
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return (fields[0], fields[1]), (fields[2], fields[3])


def parse_inputsmapping(line):
    """
    schema:
        txhash, mid, prev_txhash, nid
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return (fields[2], fields[3]), (fields[0], fields[1])


outputs = sc.textFile('outputs.csv').map(parse_outputs).partitionBy(2).persist()
inputs = sc.textFile('inputs_mapping.csv').map(parse_inputsmapping).partitionBy(2).persist()

# Transformations and/or Actions

# op: transformation + action
final = inputs.join(outputs).values()

# op: transformation
UTXOs = outputs.subtractByKey(inputs)
# can be then reduced on address thus to obtain the total value for an UTXO address


# final.map(lambda x:(x[0][0],x[0][1],x[1][0],x[1][1])).saveAsTextFile("input_final")
with open('inputs.csv', 'w') as f:
    pass


def formatted_print(keyValue):
    with open('inputs.csv', 'a') as f:
        f.write('{},{},{},{}\n'.format(keyValue[0][0], keyValue[0][1], keyValue[1][0], keyValue[1][1]))


final.foreach(formatted_print)

print inputs.count()
print 'Check it:', outputs.count(), '=', final.count(), '+', UTXOs.count()
print("--- %s seconds ---" % (time.time() - start_time))
