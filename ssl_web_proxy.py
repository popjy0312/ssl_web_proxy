#-*- coding: utf-8 -*-

import os
import SocketServer

def initCertSetting():
	if not os.path.exists('root'):
		os.system('_make_root.bat popjy')
		print 'please install root CA'
		print '인증서 저장소: 신뢰할 수 있는 루트 인증 기관'
		os.system('root\\root.crt')
	os.system('_init_site.bat')

class TCPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		print self.request.recv(1024)

class TCPServer(SocketServer.ThreadingTCPServer):
	def __init__(self, addr):
		SocketServer.ThreadingTCPServer.__init__(self, addr, TCPHandler)
		self.allow_reuse_address = True
	def start(self):
		self.serve_forever()

if __name__ == '__main__':
	initCertSetting()

	server = TCPServer(('127.0.0.1', 4433))
	server.start()