from cryptography.fernet import Fernet

key = Fernet.generate_key() 
# 암호 키 생성: 송신자와 수신자가 공유할 것!
f = Fernet(key)
# 생성된 키를 이용하여 Fernet 개체 생성

readfile=open('data.txt','rb')
data=readfile.read()
readfile.close()

writefile=open('encrypted.txt','wb')

token = f.encrypt(data)
# # byte 타입으로 입력된 평문을 암호화
writefile.write(token)
# # 암호문을 출력
    
writefile=open('encrypted.txt','rb')
d=f.decrypt(writefile.read())
print(d)
writefile.close()