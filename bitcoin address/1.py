from Crypto.Hash import RIPEMD160
import base58
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
    if e2[1]%2==0:
        pk="02"+hex(e2[0])[2:]
    else:
        pk="03"+hex(e2[0])[2:]
    #print(pk)
    
    m = hashlib.sha256()
    m.update(bytes.fromhex(pk))
    hashm=m.hexdigest()
    #print(hashm)
    
    h = RIPEMD160.new()
    h.update(bytes.fromhex(hashm))
    result="00"+h.hexdigest()
    return result
    
def getAddress(pvHash):
    m = hashlib.sha256()
    m.update(bytes.fromhex(pvHash))
    hashm=m.hexdigest()
    #print(hashm)

    m = hashlib.sha256()
    m.update(bytes.fromhex(hashm))
    hashm=m.hexdigest()
    #print(pvHash+hashm[0:8])
    code_string=pvHash+hashm[0:8]

    encoded_string = base58.b58encode(bytearray.fromhex( code_string ))
    return encoded_string

    

if __name__ == "__main__":
    d=input("개인키 입력? ")
    e2 = generate_public_key(int(d,16)) # 2주차 과제에서 작성한 함수
    pkHash=getPublicHash(e2)
    print("공개 Hash: ",pkHash)
    address=getAddress(pkHash)
    print("주소 :",address.decode('utf-8'))