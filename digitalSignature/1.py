import os
import random
import time
import hashlib

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

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
e1 = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def sign(M,d):
    r=random.randint(2,q-2)
    
    #개인키 d *곡선 상의 한점 e1 구하기
    e2=doubleAndAdd(e1,r)
    s1=e2[0]%q
    #S2 = (h(M) + d × S1) × r의역원 mod q
    m = hashlib.sha256()
    m.update(M.encode('utf-8'))
    hm=int(m.hexdigest(),16)
    s2=(hm+d*s1)*extendedEuclidian(q,r)%q
  
    return s1,s2

def verify(M,s1,s2,e2):
    # A = h(M) × S2−1 mod q, B = S1× S2−1 mod q
    m = hashlib.sha256()
    m.update(M.encode('utf-8'))
    hm=int(m.hexdigest(),16)
    s2inv=extendedEuclidian(q,s2)
    A=hm*s2inv%q
    B=S1*s2inv%q
    dot1=doubleAndAdd(e1,A)
    dot2=doubleAndAdd(e2,B)
    T=add(dot1[0],dot1[1],dot2[0],dot2[1])
    print("\tA =", hex(A))
    print("\tB =", hex(B))
    if(T[0]%q==S1%q):
        return True
    else:
        return False
    
    

if __name__ == "__main__":
    #d = generate_private_key() # 2주차 과제에서 작성한 함수
    d=3
    e2 = generate_public_key(d) # 2주차 과제에서 작성한 함수

    M = input("메시지? ")
    S1, S2 = sign(M, d)
    print("1. Sign:")
    print("\tS1 =", hex(S1))
    print("\tS2 =", hex(S2))

    print("2. 정확한 서명을 입력할 경우:")
    if verify(M, S1, S2, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")

    print("3. 잘못된 서명을 입력할 경우:")
    if verify(M, S1-1, S2-1, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")
