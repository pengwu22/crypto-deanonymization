from blocktools import *

class BlockHeader:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.previousHash = hash32(blockchain)
		self.merkleHash = hash32(blockchain)
		self.time = uint4(blockchain)
		self.bits = uint4(blockchain)
		self.nonce = uint4(blockchain)
	def toString(self):
		print "Version:\t %d" % self.version
		print "Previous Hash\t %s" % hashStr(self.previousHash)
		print "Merkle Root\t %s" % hashStr(self.merkleHash)
		print "Time\t\t %s" % str(self.time)
		print "Difficulty\t %8x" % self.bits
		print "Nonce\t\t %s" % self.nonce

class Block:
	def __init__(self, blockchain):
		self.continueParsing = True
		self.magicNum = 0
		self.blocksize = 0
		self.blockheader = ''
		self.txCount = 0
		self.Txs = []

		if self.hasLength(blockchain, 8):	
			self.magicNum = uint4(blockchain)
			self.blocksize = uint4(blockchain)
		else:
			self.continueParsing = False
			return
		
		if self.hasLength(blockchain, self.blocksize):
			self.setHeader(blockchain)
			self.txCount = varint(blockchain)
			self.Txs = []

			for i in range(0, self.txCount):
				tx = Tx(blockchain)
				self.Txs.append(tx)
		else:
			self.continueParsing = False
						

	def continueParsing(self):
		return self.continueParsing

	def getBlocksize(self):
		return self.blocksize

	def hasLength(self, blockchain, size):
		curPos = blockchain.tell()
		blockchain.seek(0, 2)
		
		fileSize = blockchain.tell()
		blockchain.seek(curPos)

		tempBlockSize = fileSize - curPos
		print tempBlockSize
		if tempBlockSize < size:
			return False
		return True


	def setHeader(self, blockchain):
		self.blockHeader = BlockHeader(blockchain)

	def toString(self):
		print ""
		print "Magic No: \t%8x" % self.magicNum
		print "Blocksize: \t", self.blocksize
		print ""
		print "#"*10 + " Block Header " + "#"*10
		self.blockHeader.toString()
		print 
		print "##### Tx Count: %d" % self.txCount
		for t in self.Txs:
			t.toString()
from hashlib import sha256
def double_sha256(x):
	return sha256(sha256(x).digest()).digest()

class Tx:
	def __init__(self, blockchain):
		#####
		self.pos_start = blockchain.tell()
		###
		self.version = uint4(blockchain)
		self.inCount = varint(blockchain)
		self.inputs = []
		for i in range(0, self.inCount):
			input = txInput(blockchain)
			self.inputs.append(input)
		self.outCount = varint(blockchain)
		self.outputs = []
		if self.outCount > 0:
			for i in range(0, self.outCount):
				output = txOutput(blockchain)
				self.outputs.append(output)	
		self.lockTime = uint4(blockchain)

		####### self-defined
		self.pos_end = blockchain.tell()
		blockchain.seek(self.pos_start)
		self.txHash = double_sha256(blockchain.read(self.pos_end-self.pos_start))
		
		
	def toString(self):
		print ""
		print "="*10 + " New Transaction " + "="*10
		print "Tx Version:\t %d" % self.version
		print "Inputs:\t\t %d" % self.inCount
		for i in self.inputs:
			i.toString()

		print "Outputs:\t %d" % self.outCount
		for o in self.outputs:
			o.toString()
		print "Lock Time:\t %d" % self.lockTime

		### self-defined output
		print "\t %s" %hashStr(self.txHash[::-1])
		def toFile(inputs, outputs):
			pass#TODO
		toFile(self.inputs, self.outputs)
					

class txInput:
	def __init__(self, blockchain):
		self.prevhash = hash32(blockchain)
		self.txOutId = uint4(blockchain)
		self.scriptLen = varint(blockchain)
		self.scriptSig = blockchain.read(self.scriptLen)
		self.seqNo = uint4(blockchain)

	def toString(self):
		print "Previous Hash:\t %s" % hashStr(self.prevhash)
		print "Tx Out Index:\t %8x" % self.txOutId
		print "Script Length:\t %d" % self.scriptLen
		print "Script Sig:\t %s" % hashStr(self.scriptSig)
		print "Sequence:\t %8x" % self.seqNo

import binascii
import hashlib
def hex_pk_script(pk_script):
	#return bytes(pk_script).encode('hex')
	return binascii.hexlify(pk_script)
	#return binascii.b2a_uu(pk_script)

def pk2int(pk_script):
	hash_obj = hashlib.sha256(pk_script)
	hex_dig = hash_obj.hexdigest()
	#print int(hex_dig)
	return int(hex_dig, 16) % 2147483647

class txOutput:
	def __init__(self, blockchain):	
		self.value = uint8(blockchain)
		self.scriptLen = varint(blockchain)
		self.pubkey = blockchain.read(self.scriptLen)

	def toString(self):
		print "Value:\t\t %d" % self.value
		print "Script Len:\t %d" % self.scriptLen
		print "Pubkey:\t\t %s" % hashStr(self.pubkey)
		print "\t\t %s" % hex_pk_script(self.pubkey)
		print "How long? \t %d" % len(self.pubkey)
