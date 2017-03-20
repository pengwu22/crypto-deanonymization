header = data[offset:offset+BlockHeader.FIXED_HEADER_BYTES]
block_hash = double_sha256(header) 
tx_id = double_sha256(tx[offset_0:offset])
