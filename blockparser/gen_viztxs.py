
"""
f70ec1d478becd0bde6793d671d9ce19c1bb455de1f6b90a8736d3d2a864bf84,1489208515,2017-03-12-00-42-45,1,2
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


####
import csv
import requests
import pycountry

tx_api = "https://blockchain.info/rawtx/"
ip_api = "https://ipinfo.io/{}/json"

output_txnode = open('csv/viz_txnode.csv', 'w')
#output_txedge = open('csv/viz_txedge.csv', 'w')

txnode_writer = csv.writer(output_txnode)
#txedge_writer = csv.writer(output_txedge)


def add_info(row):
    tx = requests.get(tx_api + row[0]).json()
    tx_geo = requests.get(ip_api.format(tx['relayed_by'])).json()
    try: # Membership test of a key AKA key exists
        row.append(tx_geo['loc'])
        row.append(tx_geo['city'])
        row.append(tx_geo['region'])
        row.append(pycountry.countries.get(alpha_2=tx_geo['country']).name)
    except KeyError:
        row.append('')
        row.append('')
        row.append('')
        row.append('')

    return ','.join(row)+'\n'


with open('csv/transactions.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print reader.line_num
        output_txnode.write(add_info(row))

output_txnode.close()
#output_txedge.close()


