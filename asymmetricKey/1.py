from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa # hazmat layer 이용
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def AESencrypt(msg):
    key= Fernet.generate_key()
    f = Fernet(key)
    if type(msg) is not bytes:
        msg=msg.encode('utf-8')
    enc_msg=f.encrypt(msg)
    return key,enc_msg

def RSAencrypt(msg):
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
        )
    
    if type(msg) is not bytes:
        msg=msg.encode('utf-8')

    encrypted = public_key.encrypt(
        msg,
        padding.OAEP( # OAEP: Optimal Asymmetric Encryption Padding
        mgf=padding.MGF1(algorithm=hashes.SHA256()), # 짧은 메시지 공격에 대비. 패딩을 추가
        algorithm=hashes.SHA256(),
        label=None
    ) )

    return encrypted

def AESdecrypt(enc_msg,aesKey):
    f=Fernet(aesKey)
    msg=f.decrypt(enc_msg)
    return msg

def RSAdecrypt(enc_msg):
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
        )    
    msg = private_key.decrypt(
    enc_msg,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    return msg
        

msg=input("평문 입력: ")
aes_key, enc_msg=AESencrypt(msg)
enc_key=RSAencrypt(aes_key)
aes_key=RSAdecrypt(enc_key)
msg=AESdecrypt(enc_msg,aes_key)
msg=msg.decode('utf-8')
print('복호화 결과: ',msg)
