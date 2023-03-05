3.py 에러 기록

##cryptography.exceptions.InvalidSignature: Signature did not match digest. 에러

파일 입출력 과정에서 file.read가 아니라 file.readlines 혹은 readline을 사용하면 생성되는 에러인듯하다.
byte 형태로 저장된 파일을 문자열 형태로 받아오는 함수를 사용해서 생긴 에러로 보임.
파일을 wb,rb로 열어서 file.read, file.write 함수를 사용하면 해결되는 에러