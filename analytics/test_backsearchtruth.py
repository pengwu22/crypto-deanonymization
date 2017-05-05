import csv, sys


def strID_to_intID(strID):
    MAXINT = 2 ** 31
    #return int(hashlib.sha256(strID).hexdigest(), base=16) % MAXINT
    return hash(strID) % MAXINT

addrFolder = "../../csv-2013-10-25/"
addrs = set([])
with open(addrFolder + "addrs.csv") as f:
    reader = csv.reader(f)
    for l in reader:
        addrs.add(l[0])
        addrs.add(l[1])


ids = map(strID_to_intID, addrs)
addr2id = dict(zip(addrs,ids))
id2addr = dict(zip(ids,addrs))


# I tell you user, you tell me all the address it has
from collections import defaultdict
user2addr = defaultdict(list)

userFolder = "../../danning/joint_total_"
with open(userFolder + "node.csv") as f:
    reader = csv.reader(f)
    for l in reader:
        user = l[1]
        addr = id2addr[int(l[0])]
        user2addr[user].append(addr)


userID = 312
with open(userFolder + "tempaddrlist.txt", 'w') as f:
    for addr in user2addr[str(userID)]:
        f.write('{}\n'.format(addr))



#####
addrlist = user2addr[str(userID)]
import requests

def backtrack():
    for addr in addrlist:
        print addr
        response = requests.get("https://blockchain.info/address/{}?format=json".format(addr))
        profile = response.json()
        if int(profile["final_balance"]) != 0:
            print addr, profile['n_tx'], int(profile["total_received"]), int(profile["total_sent"]), int(profile["final_balance"])


print 'A smart address:'
print "121Rz8UsHF3xzF8EX6Tt7KzB2Un1dVGc8Z 6027 74408527656 74346293301 62234355"
