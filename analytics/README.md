# Methods

## Serial Joint Control
<img src="https://github.com/pw2393/project_csds/blob/master/analytics/serial-joint-control.jpeg">

## Kmeans Clustering

# Flow Chart
<img src="https://github.com/pw2393/project_csds/blob/master/analytics/files_usage.jpeg">


# Graph Statistics

The original data (transactions verified on Oct 25, 2013) has 68584 distinct string addresses involved, after the hash function, 68542 int addresses remained.

After spliting multiple inputs and outputs, there are 265,479 transaction records in data.


graph type | node | edge | shrinkage rate | leaf node | isolated node |
----------------|---------------|-----------|-----------|------------|----------------|
original | 68582 | 265479 | 100% | 13509 | 1 |
serial control | 67313 | 208253 | 98.15% | 13728 | 82 |
joint control | 46210 | 71492 | 67.37% | 19995 | 1 |
serial&joint control | 44950 | 70660 |65.54% | 19511 | 82 |
cf + k-means | 35939 | 126679 | 52.40% | 7384 | 47 |


* node: in original network, a node is an address; in clustered network, a node is a user
* edge: transaction between two entities
* shrinkage rate: (# of users in current network)/(# of original addresses)
* leaf node: degree in + degree out == 1
* isolated node: only has loop edge with itself / 0 neighbor
