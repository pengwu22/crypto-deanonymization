## /Users/SUIDANNING/spark-2.0.1-bin-hadoop2.7/bin/spark-submit two_assumption_clustering.py ##

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("two_assumption")
sc = SparkContext(conf = conf)

## load data and parse
## type transform
rdd_addr = sc.textFile("addrs.csv")\
            .map(lambda line: line.split(','))\
            .map(lambda x: (x[3], (x[0], x[1], float(x[2]))))
            ## key: hash , value: input_addr, output_addr, amount

rdd_tx = sc.textFile("transactions.csv")\
            .map(lambda line: line.split(','))\
            .map(lambda x: (x[0], (float(x[1]), int(x[3]), int(x[4]))))
            ## key: hash, value: amount, m, n

## serial-control
def serial_control(rdd_tx, rdd_addr):
    serial_tx_hash = rdd_tx\
                    .filter(lambda x: x[1][1]==x[1][2]==1)\
                    .mapValues(lambda value: value[0])

    addr_pair = rdd_addr\
                .join(serial_tx_hash)\
                .values()\
                .map(lambda x: set([x[0][0],x[0][1]]))

    return addr_pair
    # return an rdd contains sets: [set([addr_id, addr_id]),...,set([addr_id, addr_id])]



## joint-control
def joint_control(rdd_addr):

    joint_user = rdd_addr\
                .map(lambda x: (x[0],x[1][0]))\
                .groupByKey()\
                .values()\
                .map(lambda x: set(x.data))\
                .filter(lambda x: len(x)>1)

    return joint_user
    # return an rdd contains sets: [set([addr_id, addr_id]),...,set([addr_id, addr_id])]

user_merged = serial_control(rdd_tx, rdd_addr)\
            .union(joint_control(rdd_addr))\
            .collect() #.persist()

## union the intersected sets into a big set
#def user_set_union(user_merged):

user_n = len(user_merged)

visited = [0] * user_n # init all state as existing
# visited state:
# 0: not visited set
# 1: visited, fully checked sets
# 2: visited, deleted set

for i in range(user_n): # the first set i
    if visited[i] == 0: # if this set i hasn't been visited

        for j in range(i + 1, user_n): # all other following sets j
            if visited[j] == 0: # if this set j hasn't been visited
                if (user_merged[i] & user_merged[j]): # if there are intersected
                    user_merged[i] = user_merged[i] | user_merged[j] # union set j's elements into the first set i
                    visited[j] = 2 # delete this set j
                #else: if there are not intersected then continue the loop
            #else: if the set j is deleted or  then go on to the next set j+1

        # inner loop finished, meaning that the set i's comparison is fully checked, no other sets have common elements with it, then mark it as 1
        visited[i] = 1
    #else: the set i is deleted, we don't need to do anything, just go on with the loop.

# we only need those expanded sets whose state is marked as 1
user_list = []
for i in range(user_n):
    if (visited[i] == 1):
        user_list.append(list(user_merged[i]))

# store it into an rdd
user_list_rdd = sc\
            .parallelize(user_list)\
            .zipWithUniqueId()\
            .map(lambda x: (x[1],x[0]))\
            .flatMapValues(lambda x: x)\
            .map(lambda x: (x[1], x[0]))

user_dict = user_list_rdd.collect()
dict_user = {}
for (key, val) in user_dict:
    dict_user[key] = val

print dict_user

dict_edge = {}

for record in rdd_addr.values().toLocalIterator():
    if record[0] in dict_user:
        if record[1] in dict_user and dict_user[record[0]] != dict_user[record[1]]:
            dict_edge[(dict_user[record[0]], dict_user[record[1]])] = record[2]

print dict_edge




#reuser_flatten.countByValue()


#for line in user_merged.collect():
 #   print line
