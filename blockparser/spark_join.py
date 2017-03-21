from pyspark import SparkConf, SparkContext
import time

start_time = time.time()

conf = SparkConf().setMaster("local[4]").setAppName("jointest")
sc = SparkContext(conf = conf)

#import csv
#import StringIO
#
#def loadRecord(line):
#    """Parse a CSV line"""
#    input = StringIO.StringIO(line)
#    reader = csv.DictReader(input, fieldnames=["txhash", "nid", "value", "addr"])
#    return reader.next()
#


def parse_outputs(line):
    """
    schema:
        txhash, nid, value, addr
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return ((fields[0], fields[1]), (fields[2], fields[3]))

def parse_inputs(line):
    """
    schema:
        txhash, mid, prev_txhash, nid
    :param line:
    :return (key, value):
    """
    fields = line.split(',')
    return ((fields[2], fields[3]), (fields[0], fields[1]))


outputs = sc.textFile('outputs.csv').map(parse_outputs).partitionBy(1).persist()
inputs = sc.textFile('inputs.csv').map(parse_inputs).partitionBy(1).persist()
for item in inputs.take(5):
    print item


# op: transformation + action
final = inputs.join(outputs).mapValues(lambda value:value[1])
for item in final.take(5):
    print item

# op: transformation
UTXOs = outputs.subtractByKey(inputs)
# can be then reduced on address thus to obtain the total value for an UTXO address



#final.map(lambda x:(x[0][0],x[0][1],x[1][0],x[1][1])).saveAsTextFile("input_final")
def formated_print(pair):
    with open('input_final.csv', 'a') as f:
        f.write('{},{},{},{}\n'.format(pair[0][0], pair[0][1], pair[1][0], pair[1][1]))

final.foreach(formated_print)

print inputs.count()
print 'Check it:',outputs.count(),'=',final.count(),'+',UTXOs.count()

print("--- %s seconds ---" % (time.time() - start_time))
