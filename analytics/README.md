# Flow Chart
<img src="https://github.com/pw2393/project_csds/blob/master/analytics/files_usage.jpeg">


# Graph Statistics

The original data (transactions verified on Oct 25, 2013) has 68584 distinct string addresses involved, after the hash function, 68542 int addresses remained.

After spliting multiple inputs and outputs, there are 265,479 transaction records in data.


clustering type | nodes (users) | edges (transactions) | leaf nodes | isolated nodes |
----------------|---------------|----------------------|------------|----------------|
serial control | 67313 | 208253 | 13728 | 82 |
joint control | 46210 | 71492 | 19995 | 1 |
serial&joint control | 44950 | 70660 |19511 | 82 |
cf + k-means | 35939 | 126679 | 7384 | 47 |


* leaf nodes: degree in + degree out == 1
* isolated nodes: only has loop edge with itself / 0 neighbor
