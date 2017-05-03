
import sys
import csv


print("sys.maxint = {}".format(sys.maxint))
print("The program use 2^31 as the MAXINT.")
MAXINT = 2**31

import hashlib
def strID_to_intID(strID):
    #return int(hashlib.sha256(strID).hexdigest(), base=16) % MAXINT
    return hash(strID) % MAXINT


inputFileFolder = "../blockparser/csv/"

######

output = open(inputFileFolder + "addrs_intid.csv", 'w')
writer = csv.writer(output)
with open(inputFileFolder + "addrs.csv") as f:
    old = []
    new = []
    reader = csv.reader(f)
    for row in reader:
        from_addr = strID_to_intID(row[0])
        to_addr = strID_to_intID(row[1])
        value = float(row[2])
        tx_hash = strID_to_intID(row[3])

        old.append(row[0])
        new.append(from_addr)

        #print [from_addr, to_addr, value, tx_hash]
        writer.writerow([from_addr, to_addr, value, tx_hash])
output.close()
print(len(set(old)), len(set(new)))
print("# addrs.csv Done")

######

output = open(inputFileFolder + "transactions_intid.csv", 'w')
writer = csv.writer(output)
with open(inputFileFolder + "transactions.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        tx_hash = strID_to_intID(row[0])
        row[0] = tx_hash
        writer.writerow(row)
output.close()
print("# transactions.csv Done")

