#-*- coding: utf-8 -*-

import os
import ssl
from socket import socket, AF_INET, SOCK_STREAM
import SocketServer
import threading
from time import sleep

lock = threading.Lock()
lock_sites = dict()

def initCertSetting():
	if not os.path.exists('root'):
		os.system('_make_root.bat popjy')
		print 'please install root CA'
		print '인증서 저장소: 신뢰할 수 있는 루트 인증 기관'
		os.system('root\\root.crt')
	os.system('_init_site.bat')

class TCPHandler(SocketServer.StreamRequestHandler):
	def getHost(self, data):
		assert 'CONNECT' in data

		addr = data[data.find('CONNECT ') + len('CONNECT '):data.find('HTTP')]
		host,port = addr.split(':')
		print 'host is ' + host
		port = int(port)
		return host, port

	def recv_http_header(self, sock):
		buf = ''
		while True:
			data = sock.recv(1)
			buf += data
			if not data or buf[-4:] == '\r\n\r\n':
				break
		return buf

	def forward_n(self, srcSock, dstSock, n):
		buf = ''
		for i in range(n):
			data = srcSock.recv(1)
			if i < 512:
				buf += data
			dstSock.send(data)
		print buf

	def parseContenLen(self, header):
		header = header.split('\r\n')
		for data in header:
			if 'Content-Length' in data:
				return int(data[data.find('Content-Length: ')+len('Content-Length: '):])

	def handle(self):
		data = self.request.recv(2048)
		host, port = self.getHost(data)
		self.request.send('HTTP/1.1 200 Connection established\r\n\r\n')

		cert_file = host + '.pem'
		if not os.path.exists(cert_file):
			with lock:
				if host not in lock_sites:
					lock_sites[host] = threading.Lock()

			with lock_sites[host]:
				if not os.path.exists(cert_file):
					os.system('_make_site.bat ' + host)

		cliSock = ssl.wrap_socket(self.request, certfile=cert_file, server_side=True)

		_request = self.recv_http_header(cliSock)
		
		serverSock = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
		serverSock.connect((host,port))
		print 'create socket host: ' + host + ' port: ' + str(port)

		serverSock.send(_request + '\r\n\r\n')

		sleep(1)

		header = self.recv_http_header(serverSock)

		print '#############header#############'
		print header

		contentLen = self.parseContenLen(header)

		print 'content length is %d' % contentLen

		if contentLen:
			self.forward_n(serverSock, cliSock, contentLen)
		else:
			cliSock.send(header)

class ThreadTCPServer(SocketServer.ThreadingTCPServer):
	def __init__(self, addr):
		SocketServer.ThreadingTCPServer.__init__(self, addr, TCPHandler)
		self.allow_reuse_address = True
	def start(self):
		self.serve_forever()

if __name__ == '__main__':
	initCertSetting()
	print "init done"
	server = ThreadTCPServer(('127.0.0.1', 4433))
	server.start()