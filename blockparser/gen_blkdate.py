"""
Filename: gen_blkdate.py
Purpose: Generate date of blocks

Authors:
    * Peng Wu

License: MIT
"""


import sys
from blocktools import *
from block import Block


def parse_dates(blockchain):
    print 'print Parsing Block Chain'
    continueParsing = True
    counter = 0
    blockchain.seek(0, 2)
    fSize = blockchain.tell() - 80  # Minus last Block header size for partial file
    blockchain.seek(0, 0)
    while continueParsing:
        block = Block(blockchain)
        continueParsing = block.continueParsing
        if continueParsing:
            # print '#',str(block.blockHeader.time)
            #print "{},{},{}".format(blktime2datetime(str(block.blockHeader.time)), 'blk'+blockchain.name.split('blk')[-1], blockchain.tell())
            yield (blktime2datetime(str(block.blockHeader.time)), 'blk'+blockchain.name.split('blk')[-1], blockchain.tell())
        counter += 1

    print ''
    print 'Reached End of Field'
    print 'Parsed {} blocks'.format(counter)


def main():
    if len(sys.argv) < 2:
        print 'Usage: gen_blkdate.py folderpath'
    else:
        output_file = open('blkdate.csv','w')
        import os
        from datetime import datetime, date
        datetime_format = '%Y-%m-%dT%H:%M:%S'
        curdate = date(2000,1,1)

        folder_path = sys.argv[1]
        files = [filename for filename in os.listdir(folder_path) if filename.startswith('blk')]

        for file_path in files:
            with open(folder_path+file_path, 'rb') as blockchain:
                for blockinfo in parse_dates(blockchain):
                    blockdate = datetime.strptime(blockinfo[0], datetime_format).date()
                    if blockdate > curdate:
                        curdate = blockdate
                        #print '!!!!'
                        #print blockinfo
                        #print os.path.getsize(folder_path+file_path)
                        print('{},{},{},{}'.format(blockinfo[0],
                                                               blockinfo[1],
                                                               blockinfo[2],
                                                               os.path.getsize(folder_path + file_path)))
                        output_file.write('{},{},{},{}\n'.format(blockinfo[0].split('T')[0],
                                                               blockinfo[1],
                                                               blockinfo[2],
                                                               os.path.getsize(folder_path + file_path)))
        output_file.close()


if __name__ == '__main__':
    main()
