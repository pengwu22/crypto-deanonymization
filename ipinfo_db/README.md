API used:

1	get the latest mainchain block height:
			https://blockchain.info/latestblock
	
2	get the block index info by height:
			https://blockchain.info/block-height/$block-height?format=json
			
3	get the block ip info by index:
			https://blockchain.info/block-index/$block-index?format=json


The ip addresses are vacant or invalid for the first or last hundred blocks, so in the test file, we pick 15 blocks from the middle.