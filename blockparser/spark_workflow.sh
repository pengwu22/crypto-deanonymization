#!/bin/sh
files="../../blk00121.dat"
echo "###### Spark Parsing Workflow Starts... ######"
spark-submit spark_parser.py local[*] $files &&
echo "\n###### Step 1 Done ######\n" &&
spark-submit spark_mapinput.py local[*] &&
echo "\n###### Step 2 Done ######\n" &&
#spark-submit spark_mapaddr.py local[*] &&
echo "\n###### Parsed Files: ######\n"$files
#spark-submit ../analytics/two_assumption_clustering.py
