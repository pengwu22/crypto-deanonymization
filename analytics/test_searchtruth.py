fileFolder = "../../csv-2013-10-25/"

import csv, sys
addrs = set([])
with open(fileFolder + "addrs.csv") as f:
    reader = csv.reader(f)
    for l in reader:
        addrs.add(l[0])
        addrs.add(l[1])


def search(addr):
    if addr in addrs:
        return 'YES'
    else:
        return 'NO'

print search("1GhvfPjPHdPARM1cNiBJk49e7Ayueiznyw")


####

def select_dict():
    for addr in addrs:
        if "1Bet" in addr:
            yield addr

def strID_to_intID(strID):
    MAXINT = 2 ** 31
    #return int(hashlib.sha256(strID).hexdigest(), base=16) % MAXINT
    return hash(strID) % MAXINT

for addr in select_dict():
    pass
    print addr, " | ", strID_to_intID(addr)





