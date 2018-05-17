import random

def showbits(n):
    return "{0:b}".format(n)

def findnum(n):
    rn = random.randrange(0,n)
    return (rn, showbits(rn))

def oddbits(s):
    return s[::2]

def evenbits(s):
    return s[1::2]

def parity(bits): # expecting string of '01'
    num = filter(lambda x:x == '1', bits) # get the 1 bits
    return len(num) % 2

def paritybits(num):
    n = showbits(num)
    ebits = evenbits(n)
    obits = oddbits(n)
    enum = parity(ebits)
    onum = parity(obits)
    return (enum, onum)

# (content, parity of even bits, parity of odd bits, nonce)
genesis_block = (42,0,0,0)
chain = genesis_block
# next block contains
# 1. content you want to add
# 2,3 hash of previous block (even bits parity and odd bits parity)
# 4 nonce, that makes the entire contents match the magicical proof of work - https://en.bitcoin.it/wiki/Nonce

def check_difficult(content, hash1, hash2, nonce): # start out with even bits even parity
    if (paritybits(content + hash1 + hash2 + nonce)[0] == 0):
        return True
    print "nonce bits are {}".format(showbits(nonce))
    print "{}: Even bits {}; parity bit {}; needed {}".format(nonce,evenbits(showbits(nonce)),paritybits(content + hash1 + hash2 + nonce), "0,?")
    return False

def check_more_difficult(content, hash1, hash2, nonce):
    if (paritybits(content + hash1 + hash2 + nonce) == (0,0)):
        return True
    print "nonce bits are {}".format(showbits(nonce))
    print "{}: Even bits {}; Odd bits {}; parity bit {}; needed {}".format(nonce,evenbits(showbits(nonce)),oddbits(showbits(nonce)),paritybits(content + hash1 + hash2 + nonce), "0,0")
    return False
# second_block = sum(genesis_block) + sum(72,nonce)

# in the beginning, magic_difficulty is that even bits have even parity
# when difficulty increases, even and odd bits must have even parity
chain = [genesis_block]

def maybe_content(chain,content,nonce_guess):
    last_block = chain[-1]
    last_hash = last_block[1:3]
    hash1,hash2 = paritybits(content + last_hash[0] + last_hash[1] + nonce_guess)
    if (check_difficult(content, hash1, hash2, nonce_guess)):
        print "It worked!"
        chain.append((content, hash1, hash2, nonce_guess))
        return chain

def maybe_hard_content(chain,content,nonce_guess):
    last_block = chain[-1]
    last_hash = last_block[1:3]
    hash1,hash2 = paritybits(content + last_hash[0] + last_hash[1] + nonce_guess)
    if (check_more_difficult(content, hash1, hash2, nonce_guess)):
        print "It worked!"
        chain.append((content, hash1, hash2, nonce_guess))
        return chain

def do_it_for_me(chain,content):
    last_block = chain[-1]
    last_hash = last_block[1:3]
    nonce_guess = random.randrange(0,255)
    hash1,hash2 = paritybits(content + nonce_guess)
    while (not check_difficult(content, hash1, hash2, nonce_guess)):
        nonce_guess = random.randrange(0,255)
    hash1,hash2 = paritybits(content + nonce_guess)
    chain.append((content, hash1, hash2, nonce_guess))
    return chain
