import os
import random
from Crypto.Hash import RIPEMD160
import base58
import time
import hashlib
import sys
import os
import random
import time
import hashlib
import sys

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

def extendedEuclidian (n,b):
    r1=n
    r2=b
    t1=0
    t2=1
    while (r2>0):
        q=r1//r2
        r=r1-q*r2
        r1=r2; r2=r
        t=t1-q*t2
        t1=t2;t2=t
    if(r1==1):
        return t1%n
        

def double(x,y):
    ramda=((3*(x**2))*extendedEuclidian(p,2*y))%p
    #print("ramda is " ,ramda)
    nx=(ramda**2-2*x)%p
#   print("hetttt",x,nx,y)
    ny=(ramda*(x-nx)-y)%p
    return nx,ny

def add(x,y,x1,y1):
    if(x1-x<0):
        a,b=x1,y1
        x1,y1=x,y
        x,y=a,b
    ramda=((y1-y)*extendedEuclidian(p,x1-x))%p
    nx=(ramda**2-x1-x)%p
    ny=(ramda*(x1-nx)-y1)%p
    return nx,ny

def generate_private_key():
    a=os.urandom(1000000)
    b=str(random.random())
    c=str(time.time())

    m = hashlib.sha256()
    m.update(a)
    m.update(b.encode('utf-8'))
    m.update(c.encode('utf-8'))
    #print(m.digest_size)
    randNum=m.hexdigest()
    
    return int(randNum,16)

def generate_public_key(k):
    G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    return doubleAndAdd(G,k)


def doubleAndAdd(G,k):
    x1=G[0]
    y1=G[1]
    x=G[0]
    y=G[1]
    for bit in bin(k)[3:]:
        if (bit=='1'):
            x,y=double(x,y)
            x,y=add(x,y,x1,y1)
        else:
            x,y=double(x,y)
    return x,y

def getPublicHash(e2):
    x=hex(e2[0])[2:]
    while len(x)<64:
        x="0"+x
    if e2[1]%2==0:
        pk="02"+x
    else:
        pk="03"+x
    #print(x)
    
    m = hashlib.sha256()
    m.update(bytes.fromhex(x))
    hashm=m.hexdigest()
    #print(hashm)
    
    h = RIPEMD160.new()
    h.update(bytes.fromhex(hashm))
    #print(h.hexdigest())
    result="00"+h.hexdigest()
    
    m = hashlib.sha256()
    m.update(bytes.fromhex(result))
    hashm=m.hexdigest()
    #print(hashm)

    m = hashlib.sha256()
    m.update(bytes.fromhex(hashm))
    hashm=m.hexdigest()
    #print(result+hashm[0:8])
    code_string=result+hashm[0:8]

    encoded_string = base58.b58encode(bytearray.fromhex( code_string ))
    return encoded_string
    
def getDesiredKey(str):
    while True:
        pvK= generate_private_key()
        e2 = generate_public_key(pvK)
        pkHash=getPublicHash(e2)
        pkHash=pkHash.decode('utf-8')
        if str in pkHash:
            return hex(pvK),pkHash

if __name__ == "__main__":
    desiredStr=input("희망하는 주소의 문자열?")
    pvK,addrK=getDesiredKey(desiredStr)
    print("개인키 = ",pvK[2:])
    print("주소 = ",addrK)
    