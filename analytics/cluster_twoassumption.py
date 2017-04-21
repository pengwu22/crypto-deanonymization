## /Users/SUIDANNING/spark-2.0.1-bin-hadoop2.7/bin/spark-submit two_assumption_clustering.py ##

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[*]").setAppName("two_assumption")
sc = SparkContext(conf = conf)

########################
# load data and parse
########################
filefolder = "../blockparser/csv/"

## datatype transform
rdd_addr = sc.textFile(filefolder+"addrs.csv")\
            .map(lambda line: line.split(','))\
            .map(lambda x: (x[3], (x[0], x[1], float(x[2]))))
            ## key: hash , value: input_addr, output_addr, amount

rdd_tx = sc.textFile(filefolder+"transactions.csv")\
            .map(lambda line: line.split(','))\
            .map(lambda x: (x[0], (float(x[1]), int(x[3]), int(x[4]))))
            ## key: hash, value: amount, m, n

#############################
# serial-control assumption
#############################

## In this part, we extract those addresses which are 1-1 in transactions

def serial_control(rdd_tx, rdd_addr):
    serial_tx_hash = rdd_tx\
                    .filter(lambda x: x[1][1]==1 and x[1][2]==1)\
                    .mapValues(lambda value: value[0])

    addr_pair = rdd_addr\
                .join(serial_tx_hash)\
                .values()\
                .map(lambda x: set([x[0][0],x[0][1]]))

    return addr_pair
    # return an rdd contains sets: [set([addr_id, addr_id]),...,set([addr_id, addr_id])]

## Addresses in a same set are from same user

#############################
## joint-control assumption
#############################

## In this part, we extract those addresses are together serving as one input in a transaction

def joint_control(rdd_addr):

    joint_user = rdd_addr\
                .map(lambda x: (x[0],x[1][0]))\
                .groupByKey()\
                .values()\
                .map(lambda x: set(x.data))\
                .filter(lambda x: len(x)>1)

    return joint_user
    # return an rdd contains sets: [set([addr_id, addr_id]),...,set([addr_id, addr_id])]

## Addresses in a same set are from same user

######################
# 2 assumptions merge
######################

## In this part, we union the results above by their intersection.
## We come up with the final user-dict here

user_merged = serial_control(rdd_tx, rdd_addr)\
            .union(joint_control(rdd_addr))\
            .collect() #.persist()

## union the intersected sets into a big set

############################################## python object begins ###################################
###################
# user set merge
###################

user_n = len(user_merged)

visited = [0] * user_n # init all sets' states as 'not visited'
# visited state:
# 0: not visited set
# 1: visited, fully checked sets
# 2: visited, deleted set

for i in range(user_n): # the first set i
    if visited[i] == 0: # if this set i hasn't been visited, then visit

        for j in range(i + 1, user_n): # all other following sets j
            if visited[j] == 0: # if this set j hasn't been visited, then visit
                if (user_merged[i] & user_merged[j]): # if there are intersected, then union them

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
        user_list.append(list(user_merged[i])) # here in the list are all the user clusters

############################################### python object ends ####################################

##############################
# generate the user_dict table
##############################

# store it into an rdd
user_list_rdd = sc\
            .parallelize(user_list)\
            .zipWithUniqueId()\
            .map(lambda x: (x[1], x[0]))\
            .flatMapValues(lambda x: x)\
            .map(lambda x: (x[1], x[0]))
# zip with unique id: [([address1, address2, ...], unique id),...]
# map key: unique user id , value: address list
# flatmap : turn address list in value into one address
# change key and value,  key: address, value: user id

# results are now in user_list_rdd.collect()
# format: list [address, id]
# one address and the user's id it belongs to

############################################## python object begins #####################################
# convert the list into dictionary for faster query later
dict_user = user_list_rdd.collectAsMap()

# format: dict {key: address, value: user id}

#############################
# generate the user_tx graph
#############################
from collections import defaultdict
dict_edge = defaultdict(float)

# go through every record in addr table
for record in rdd_addr.values().toLocalIterator():
    try:
        dict_edge[(dict_user[record[0]], dict_user[record[1]])] += record[2]
    except KeyError:
        pass
# if we found that there is a transaction record is between different users in our user dictionary, then we add this tx amount into the edge between these two users.

# format: {key: (user id1, user id2), value: transaction amount}
# directed graph, nodes are the user ids, edges are the transactions with value.
############################################## python object ends ########################################
# write into csv:2017-03-12


with open(filefolder+'user_node.csv', 'w') as f1:
    for key in dict_user.keys():
        f1.write(str(key) + ',' + str(dict_user[key]) + '\n')


with open(filefolder+'user_edge.csv', 'w') as f2:
    for key in dict_edge.keys():
        f2.write(str(key[0])+ ',' + str(key[1]) + ',' + str(dict_edge[key]) + '\n')
