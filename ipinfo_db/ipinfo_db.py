def update_data():
    import requests
    import json
    import os.path as path

    r_latest = requests.get('https://blockchain.info/latestblock')
    latest_height = r_latest.json()[u'height']

    if not path.isfile('ipinfo_db.csv'):
        fd = open('ipinfo_db.csv', 'w')
        fd.write("block_hash" + "," + "relayed_ip" + "," + "tx_count" + "," + "block_index" + "\n")
        fd.close()

    fd = open('ipinfo_db.csv', 'r+')
    line = len(fd.readlines())
    new_block_index = []    
    for i in range(line, latest_height + 1):
        r = requests.get("https://blockchain.info/block-height/"+ str(i) +"?format=json")
        new_block_index = r.json()[u'blocks'][0][u'block_index']
        r = requests.get("https://blockchain.info/block-index/" + str(new_block_index) + "?format=json")
        a = r.json()
        hash_nb = a[u'hash']
        if a.has_key(u'relayed_by'):
            relayed_ip = str(a[u'relayed_by'])
        else:
            relayed_ip = 'NA'
        tx_count = str(a[u'n_tx'])
        block_index = str(a[u'block_index'])
        fd.seek(0, 2)
        fd.write( hash_nb + "," + relayed_ip + "," + tx_count + "," + block_index + "\n")

    fd.close()
    
update_data()

def cnt_tx_per_ip():
    import csv
    with open('ipinfo_db.csv', 'rb') as fd:
        reader = csv.reader(fd)
        your_list = list(reader)

    valid_ip = []
    tx_n = []
    flag = 0
    for i in range(1, len(your_list)):
        if your_list[i][1] != 'NA' and your_list[i][1] != '0.0.0.0':
            if len(valid_ip) == 0:
                valid_ip.append(your_list[i][1])
                tx_n.append(your_list[i][2])
            else:
                for j in range(0, len(valid_ip)):
                    if your_list[i][1] == valid_ip[j]:
                        tx_n[j] = int(tx_n[j]) + int(your_list[i][2])
                        flag = 1
                        break
                if flag == 0:
                    valid_ip.append(your_list[i][1])
                    tx_n.append(your_list[i][2])

    for i in range(0, len(valid_ip)):
        print valid_ip[i], tx_n[i]

cnt_tx_per_ip()

