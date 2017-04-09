"""
Author: Peng Wu
License: MIT
"""


# Initialize Spark Context: local multi-threads
from pyspark import SparkConf, SparkContext
from blocktools import *
from block import Block

output_folder = './csv:2017-03-12/'
import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def parse(blockchain):
    blocks = []
    ######
    continueParsing = True
    counter_blk = 0
    blockchain.seek(0, 2)
    fSize = blockchain.tell() - 80  # Minus last Block header size for partial file
    blockchain.seek(0, 0)
    while continueParsing:
        block = Block(blockchain)
        continueParsing = block.continueParsing
        if continueParsing:
            #block.toString()
            blocks.append(block.toMemory())
        counter_blk += 1

    print ''
    print 'Reached End of Field'
    print 'Parsed blocks:{}'.format(counter_blk)
    return blocks


def main(argv_filenames, argv_setMaster):
    # Initialize Spark Context: local multi-threads
    conf = SparkConf().setMaster(argv_setMaster).setAppName("parser")
    sc = SparkContext(conf=conf)

    rawfiles = sc.parallelize(argv_filenames)

    # Transformations and/or Actions
    blocks = rawfiles.map(lambda filename: parse(open(filename))).flatMap(lambda x:x)

    # Output file
    with open(output_folder+'inputs_mapping.csv:2017-03-12','w') as f:
        pass
    with open(output_folder+'outputs.csv:2017-03-12','w') as f:
        pass
    with open(output_folder+'transactions.csv:2017-03-12','w') as f:
        pass
    def formatted_print(block):
        """
        print the return of block.toMemery()
        """
        with open(output_folder + 'inputs_mapping.csv:2017-03-12', 'a') as f:
            f.write(block[0])
        with open(output_folder + 'outputs.csv:2017-03-12', 'a') as f:
            f.write(block[1])
        with open(output_folder + 'transactions.csv:2017-03-12', 'a') as f:
            f.write(block[2])
    blocks.foreach(formatted_print)

    with open(output_folder + 'README.md', 'w') as f:
        f.write('\n'.join(argv_filenames))
    # End Program


if __name__ == "__main__":

    import sys
    import time
    # Initialize Timer
    start_time = time.time()

    if len(sys.argv) >= 3:
        if sys.argv[1] == 'local[*]' or sys.argv[1] == 'yarn':
            main(argv_filenames = [sys.argv[i] for i in range(2, len(sys.argv))], argv_setMaster = sys.argv[1])
    else:
        print "\n\tUSAGE:\n\
                spark-submit spark_parser.py local[*] filename1.dat filename2.dat ...\n\
                spark-submit spark_parser.py yarn filename1.dat filename2.dat ...\n\
              "

    print("--- %s seconds ---" % (time.time() - start_time))
