"""
Usage:
~/spark/bin/spark-submit project_csds/blockparser/spark_parser.py
"""

from pyspark import SparkConf, SparkContext
from blocktools import *
from block import Block

def parse(blockchain):
    blocks = []
    ######
    continueParsing = True
    counter = 0
    blockchain.seek(0, 2)
    fSize = blockchain.tell() - 80  # Minus last Block header size for partial file
    blockchain.seek(0, 0)
    while continueParsing:
        block = Block(blockchain)
        continueParsing = block.continueParsing
        if continueParsing:
            #block.toString()
            blocks.append(block.toMemory())
        counter += 1

    print ''
    print 'Reached End of Field'
    print 'Parsed %s blocks', counter
    return blocks

def formatted_print(block):
    """
    print the return of block.toMemery()
    """
    with open('../../inputs_mapping.csv','a') as f:
        f.write(block[0])
    with open('../../outputs.csv','a') as f:
        f.write(block[1])
    with open('../../transactions.csv','a') as f:
        f.write(block[2])


def main():
    import time
    # Initialize Timer
    start_time = time.time()

    # Initialize Spark Context: local multi-threads
    conf = SparkConf().setMaster("local[2]").setAppName("parser")
    sc = SparkContext(conf=conf)

    # Load files
    #if len(sys.argv) < 2:
        #print 'Usage: $SPARK_PATH/spark-submit spark_parser.py filename1 filename2 ...'
    #else:

    rawfiles = sc.parallelize(['../../blk00{}.dat'.format(d) for d in [800]])

    # Transformations and/or Actions
    blocks = rawfiles.map(lambda filename: parse(open(filename))).flatMap(lambda x:x)

    # Output file
    with open('../../inputs_mapping.csv','w') as f:
        pass
    with open('../../outputs.csv','w') as f:
        pass
    with open('../../transactions.csv','w') as f:
        pass
    blocks.foreach(formatted_print)

    # End Program
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()