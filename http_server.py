import logging
import sys
import threading
import SocketServer
# time package
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


HOST = '127.0.0.1'
PORT = 2201

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

html_body = """
<!DOCTYPE html>
<html>
<head>
	<title>names</title>
</head>
<body>
	<p>Name 1, PERM 1</p>
	<p>Name 2, PERM 2</p>
</body>
</html>
"""

now = datetime.now()
stamp = mktime(now.timetuple())
line = "\r\n"
header_501 = "HTTP 1.1 501 Not Implemented" + line + "Content-Type: text/html" + line + \
    "Content-Length: " + line + "Date:" + format_date_time(stamp) + line + line 
header_404 = "HTTP/1.1 404 Not Found" + line + "Content-Type: text/html" + line + \
    "Content-Length: " + line + "Date:" + format_date_time(stamp) + line + line
     
class StupidServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            print "handling"
            data = self.request.recv(1024)
            print data
            # get request
            command = data.split(' ')[0]
            response = {
                "GET": self.get,
                "HEAD": self.head,
                "POST": self.post,
                "PUT": self.put,
                "DELETE": self.delete,
                "TRACE": self.trace,
                "CONNECT": self.connect}
            response[command](data)
        except KeyboardInterrupt:
			print "KeyboardInterrupt"

    def head(self, data):
        if data.split(' ')[1] == '/names':
            self.names(data, 'head')
        elif data.split(' ')[1].split('/')[1] == 'sort':
            self.sort(data, 'head')
        else:
            self.request.send(header_404)
        
    def get(self, data):
        if data.split(' ')[1] == '/names':
            self.names(data, 'get')
        elif data.split(' ')[1].split('/')[1] == 'sort':
            self.sort(data, 'get')
        else:
            self.request.send(header_404)
    
            #line + "Content-length: {a}".format(a=len(html_body))+ \
    def names(self, data, cri):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        a = str(len(html_body))
        line = "\r\n"
        # edit header
        header = "HTTP/1.1 200 OK" + line + "Content-Type: text/html" + \
            line + "Date:" + format_date_time(stamp) + \
            line + "Content-length:" + a + line + line
        # if request is get, return header and body; if request is head, return header
        content = header + html_body + line + line if cri == 'get' else header
        self.request.send(content)

    def sort(self, data, cri):
        # get sort data
        sort_data = data.split(' ')[1].split('/')[2:]
        # convert them to integer
        con_data = [int(i) for i in sort_data]
        # sorting and convert them back to string
        sorted_data = ""
        for i in range(len(sorted(con_data))):
            sorted_data = sorted_data + " " + str(sorted(con_data)[i])
        # edit header
        a = str(len(sorted_data))
        header = "HTTP/1.1 200 OK" + line + "Content-Type: text/html" + \
            line + "Date:" + format_date_time(stamp) + \
            line + "Content-length:" + a + line + line
        # if request is get, return header and body; if request is head, return header
        content = header + sorted_data + line + line if cri == 'get' else header
        self.request.send(content)
 
    def post(self, data):
        self.request.send(header_501)   

    def put(self, data):
        self.request.send(header_501)   

    def delete(self, data):
        self.request.send(header_501)   
   
    def trace(self, data):
        self.request.send(header_501)   
  
    def connect(self, data):
        self.request.send(header_501)   
   

class ThreadedStupidServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	# Ctrl-C will cleanly kill all spawned threads
	daemon_threads = True
	# much faster rebinding
	allow_reuse_address = True

if __name__ == '__main__':
	server = ThreadedStupidServer((HOST, PORT), StupidServerHandler)
	# terminate with Ctrl-C
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)
