import os
import random
import time
import hashlib
import sys

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

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

def add(x,y):
    gx=G[0]
    gy=G[1]
    if(gx-x<0):
        a,b=gx,gy
        gx,gy=x,y
        x,y=a,b
    ramda=((gy-y)*extendedEuclidian(p,gx-x))%p
    nx=(ramda**2-gx-x)%p
    ny=(ramda*(gx-nx)-gy)%p
    return nx,ny

def getPublic(k):
    gx=G[0]
    gy=G[1]
    x=G[0]
    y=G[1]
    #print(bin(k)[2:])
    for bit in bin(k)[3:]:
        if (bit=='1'):
            x,y=double(x,y)
            x,y=add(x,y)
        else:
            x,y=double(x,y)
    return x,y

def getRand():
    a=os.urandom(1000000)
    b=str(random.random())
    c=str(time.time())

    m = hashlib.sha256()
    m.update(a)
    m.update(b.encode('utf-8'))
    m.update(c.encode('utf-8'))
    #print(m.digest_size)
    randNum=m.hexdigest()
    return randNum

#Y2 = (X3 + 7) % p

randNum=int(getRand(),16)

while(p<=num):
    randNum=int(getRand(),16)
    
print(getPublic(randNum))