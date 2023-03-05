import random

alphabet=list(range(26))
random.shuffle(alphabet)

E={}
for i in range(26):
    E[i]=alphabet[i]

plain=input("평문 입력: ")
plain=list(plain)

cyper=""
for i in range(len(plain)):
    if plain[i].isalpha():
        n=ord(plain[i])-ord('a')
        m=chr(E[n]+ord('a'))
    else:
        m=plain[i]    
    cyper+=m

print ("암호문: ",cyper)
D={}
for i in E:
    D[E[i]]=i

decode=""
for i in range(len(cyper)):
    if plain[i].isalpha():
        n=ord(cyper[i])-ord('a')
        m=chr(D[n]+ord('a'))
    else:
        m=cyper[i]
    decode+=m

print("복호문: ",decode)
