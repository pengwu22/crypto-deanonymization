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


#####
import requests

print len(addrs)
f = open(addrFolder + "addrs_info.txt", 'w')
for i, addr in enumerate(addrs):
    response = requests.get("https://blockchain.info/address/{}?format=json".format(addr))
    profile = response.json()
    if int(profile['n_tx']) > 500 and int(profile["final_balance"]) != 0:
        print "{}%".format(i * 100.0/len(addrs))
        print addr, profile['n_tx'], int(profile["total_received"]), int(profile["total_sent"]), int(profile["final_balance"])
        f.write("{},{},{},{},{}\n".format(addr, profile['n_tx'], int(profile["total_received"]), int(profile["total_sent"]), int(profile["final_balance"])))


f.close()