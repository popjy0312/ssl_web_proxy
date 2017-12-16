import SocketServer
import os


if ___name__ == '__main__':
	if not os.path.isfile('root'):
		os.system('_make_root.bat popjy')
		print 'install root/root.crt file'
		print 'then retry this program'
	os.system('_make_root.bat popjy')
	os.system('_init_site.bat')
