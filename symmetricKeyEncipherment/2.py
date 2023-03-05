def vigenere(key,plain):
    result=""
    for i in range(len(plain)):
        c=(ord(plain[i])-ord('A')+key[i%6])%26
        result+=chr(c+ord('A'))
    
    return result

def decryptVigenere(key,cyper):
    result=""
    for i in range(len(cyper)):
        c=ord(cyper[i])-ord('A')
        p=(c-key[i%6]+26)%26
        result+=chr(p+ord('A'))
    return result

def autokeyCiper(key,plain):
    result=""
    for i in range(len(plain)):
        p=ord(plain[i])-ord('A')
        c=(p+key)%26
        result+=chr(c+ord('A'))
        key=p
    return result

def decryptAutokeyCiper(key,cyper):
    result=""
    for i in range(len(cyper)):
        c=ord(cyper[i])-ord('A')
        p=(c-key+26)%26
        result+=chr(p+ord('A'))
        key=p
    return result

def getKeyList(keyString):
    keyString=keyString.upper().replace(" ","")
    key={}
    for i in range(len(keyString)):
        key[i]=ord(keyString[i])-ord('A')
    return key


plain=input("평문 입력: ")
plain=plain.upper().replace(" ","")

keyString=input("Vigenere 암호: ")
vkey=getKeyList(keyString)

cyper=vigenere(vkey,plain)
print("암호문: ",cyper)
print("평문: ",decryptVigenere(vkey,cyper))

akey=int(input("자동 키 암호: "))

cyper=autokeyCiper(akey,plain)
print("암호문: ",cyper)
print("평문: ",decryptAutokeyCiper(akey,cyper))






