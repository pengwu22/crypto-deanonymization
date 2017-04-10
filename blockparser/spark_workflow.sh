#!/bin/sh
files="../../blk00000.dat ../../blk00001.dat"
echo "###### Spark Parsing Workflow Starts... ######"
spark-submit spark_parser.py local[*] $files &&
echo "\n###### Step 1 Done ######\n" &&
spark-submit spark_mapinput.py local[*] &&
echo "\n###### Step 2 Done ######\n" &&
spark-submit spark_mapaddr.py local[*] &&
echo "\n###### Parsed Files: ######\n"$files



