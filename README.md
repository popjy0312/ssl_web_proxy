# ssl_web_proxy

2015410223 정주영
사이버국방학과 이경문교수님 과제
OS : Windows

## 상세

구글링을 통하여 SSL Client, SSL Server 프로그래밍을 익힌다. OpenSSL을 사용하거나 OpenSSL을 wrapping한 라이브러리를 이용해도 된다.
proxy 주소는 "127.0.0.1:4433"으로 한다.
웹 클라이언트로부터 HTTPS Request를 받기 이전에 CONNECT method(plain text)를 parsing하여 접속하고자 하는 Host를 알아 낸다.
SSL Server는 알아낸 Host를 기반으로 사이트 인증서를 실시간으로 생성하여 SSL handshaking certificate에 이용한다.
이전 site_unblock 과제와 마찬가지로 proxying을 수행한다.

