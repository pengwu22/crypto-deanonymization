
"""
f70ec1d478becd0bde6793d671d9ce19c1bb455de1f6b90a8736d3d2a864bf84,1489208515,2017-03-12-00-42-45,1,2
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyspark import SparkConf, SparkContext

####
import requests
#import pycountry
#from blocktools import blktime2datetime

tx_api = "https://blockchain.info/rawtx/"
ip_api = "https://ipinfo.io/{}/json"


conf = SparkConf().setMaster('yarn').setAppName("parser")
sc = SparkContext(conf=conf)

prerow = sc.textFile('csv:2017-03-12/transactions.csv:2017-03-12').map(lambda line:line.split(','))


def add_info(row):
    tx = requests.get(tx_api + row[0]).json()
    #row[2] = ' '.join(blktime2datetime(int(tx['time'])).split('T'))
    tx_geo = requests.get(ip_api.format(tx['relayed_by'])).json()
    try: # Membership test of a key AKA key exists
        row.append(tx_geo['loc'])
        row.append(tx_geo['city'])
        row.append(tx_geo['region'])
	row.append(tx_geo['country'])
        #row.append(pycountry.countries.get(alpha_2=tx_geo['country']).name)
    except KeyError:
        row.append('')
        row.append('')
        row.append('')
        row.append('')

    return ','.join(row)

row = prerow.map(add_info)

row.saveAsTextFile('csv:2017-03-12/output')



