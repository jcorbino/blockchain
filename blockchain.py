from time import time
from hashlib import md5
from datetime import datetime


## Hashing functions:
# Slower, 64 bytes
#sha256 = sha256('content').hexdigest()
# Faster, 32 bytes
#md5 = md5('content').hexdigest()


class Block:
    timestamp = ''
    prev_hash = ''
    content = ''
    nonce = 0
    md5_hash = ''

    def __init__(self, timestamp, prev_hash, content, nonce, md5_hash):
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.content = content
        self.nonce = nonce
        self.md5_hash = md5_hash

    def serialize(self):
        return self.prev_hash+self.content+str(self.nonce)


class Blockchain:
    MAX_NONCE = 999999 # To prevent infinite mining
    prefix = '00000'   # Mining difficulty
    blocks = []

    # Genesis block:
    def __init__(self):
        nonce = 622722 # For 00000
        self.blocks.append(Block(datetime.now(), ''.zfill(32), 'Genesis', nonce,
                           md5((''.zfill(32)+'Genesis'+str(nonce)).encode('utf-8')).hexdigest()))

    def add_block(self, content = ''):
        nonce = 0
        prev_hash = self.blocks[-1].md5_hash

        md5_hash = md5((prev_hash+content+str(nonce)).encode('utf-8')).hexdigest()

        # Mining:
        while md5_hash[0:len(self.prefix)] != self.prefix and nonce < self.MAX_NONCE:
            nonce += 1
            md5_hash = md5((prev_hash+content+str(nonce)).encode('utf-8')).hexdigest()

        if nonce < self.MAX_NONCE:
            self.blocks.append(Block(datetime.now(), prev_hash, content, nonce, md5_hash))
        else:
            print('Unable to mine block #'+str(len(self.blocks)+1))

    def print_chain(self):
        i = 1
        for block in self.blocks:
            print(f'BLOCK #{i} ======================='); i += 1
            print(block.prev_hash)
            print(block.timestamp)
            print(block.content)
            print(block.md5_hash)
            print('================================\n\t\t|\n\t\tV')

    def check_block(self, block_num):
        if block_num > 0:
            block = self.blocks[block_num-1]
            if md5((block.serialize()).encode('utf-8')).hexdigest() == block.md5_hash:
                print(f'Block #{block_num} is valid')
            else:
                print(f'Block #{block_num} is invalid')
        else:
            print('Invalid block number')

    def check_chain(self):
        for i in range(1, len(self.blocks)+1):
            self.check_block(i)


b = Blockchain()

t1 = time()
b.add_block('Johnny')
b.add_block('Noelle')
t2 = time()

b.print_chain()
print(f'Elapsed time: {t2-t1:.2f}s')
b.check_chain()
