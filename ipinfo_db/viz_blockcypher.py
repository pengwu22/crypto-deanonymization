
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from datetime import datetime
import time


format_datetime_0 = "%Y-%m-%dT%H:%M:%S"
format_datetime_1 = "%Y-%m-%dT%H:%M:%S.%fZ"
token = "?token="+"3265d85a8d2745b5acd5edc08f12e28f"
block_hash = "0000000000000000021f82e525faffe09a014f96c8ce3a09f2d8ed8f8118e673"




def get_geoinfo(ip):
    pass



tx_start = 0
pre_tx_start = "?txstart="
tx_ids = [0]
while len(tx_ids) > 0:
    block = requests.get("https://api.blockcypher.com/v1/btc/main/blocks/" + block_hash + pre_tx_start + str(tx_start) + token).json()
    tx_url = block["tx_url"]
    tx_ids = block["txids"]

    for tx_hash in tx_ids:
        time.sleep(0.5)
        #tx_hash = "ad4a2ba16175b7dce1c61acbe097d3800ca0affaa377c56cc587d6c4746a5684"
        tx = requests.get(tx_url+tx_hash+token).json()
        tx_dt = datetime.strptime(tx["received"].split('Z')[0].split('.')[0], format_datetime_0)
        #tx_date, tx_time = tx_dt.strftime("%Y-%m-%d %H:%M:%S").split()
        tx_datetime = tx_dt.strftime("%Y-%m-%d %H:%M:%S")

        print "##"
        print tx_hash

        tx_ip = tx["relayed_by"]


        tx_geo  = requests.get("https://ipinfo.io/" + str(tx_ip).split(":")[0] + "/json").json()
        #[u'loc', u'city', u'country', u'region']#


        with open("viz_txs.csv:2017-03-12","a") as f:
            f.write("{},{},{},{},{},{},{},{},{}\n".format(tx_datetime, tx_geo['loc'], tx_geo['city'], tx_geo['region'], tx_geo['country'], tx['total'], tx['vin_sz'], tx['vout_sz'], tx_hash))


    tx_start += 20



