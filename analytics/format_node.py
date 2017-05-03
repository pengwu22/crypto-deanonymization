
import sys
import csv


print("sys.maxint = {}".format(sys.maxint))
print("The program use 2^31 as the MAXINT.")
MAXINT = 2**31

import hashlib
def strID_to_intID(strID):
    #return int(hashlib.sha256(strID).hexdigest(), base=16) % MAXINT
    return hash(strID) % MAXINT


inputFileFolder = "/Users/SUIDANNING/Desktop/2017SPRING/CSDS/project/may3/output/"

######
output = open(inputFileFolder + "serial_total_node_intid.csv", 'w')
writer = csv.writer(output)
with open(inputFileFolder + "serial_total_node.csv") as f:
    old = []
    new = []
    reader = csv.reader(f)
    for row in reader:
        from_addr = strID_to_intID(row[0])

        old.append(row[0])
        new.append(from_addr)

        #print [from_addr, to_addr, value, tx_hash]
        writer.writerow([from_addr, row[1]])
output.close()
print(len(set(old)), len(set(new)))
print("# addrs.csv Done")
