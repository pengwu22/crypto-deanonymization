# Spark Bitcoin Parser

Bitcoin transaction data stored in `blkXXXXX.dat` files in every full node of the network.
As more people participate in Bitcoin transactions, the data grows exponentially.
Scalable analysis is called for.

This project is a Bitcoin transaction data Parser, based on Python and Spark's Python API – PySpark.


## Files

Filename | Description | First Author | Modified by
------ | ------ | ------ | ------
base58.py | module: necessary encoder for public address | Gavin Andresen | Peng Wu
blocktools.py | module: tools for reading binary data from block files | Alex Gorale | Peng Wu
block.py | module: classes for Blocks, Transactions | Alex Gorale | Peng Wu
spark_parser.py | parser: step 1| Peng Wu |
spark_mapinput.py | parser: step 2 | Peng Wu |
spark_mapaddrs.py | parser: step 3 | Peng Wu |


## Usage: Data Pipeline

### Step 1
```
spark-submit spark_parser.py blk00001.dat blk00002.dat ...
```
Input:
blkXXXXX.dat: Bitcoin raw binary blockchain data file

Output:
inputs_mapping.csv:
outputs.csv:
transaction.csv:

```
spark-submit spark_mapinput.py local[*]
spark-submit sprk_mapaddr.py local[*]
```

### Step 2
```
spark-submit spark_mapinput.py
```

Input:
inputs_mapping.csv:
outputs.csv:

Outputs:
inputs.csv

### Step 3
```
spark-submit spark_mapinput.py
```

Input:
inputs.csv
outputs.csv

Outputs:
addrs.csv

## License

MIT

