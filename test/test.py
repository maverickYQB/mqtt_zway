import socket
s = socket.socket()
address = "192.168.1.136"
port = 1883  # port number is a number, not string
try:
    s.connect((address, port))
    print "Reachable %s:%d" % (address, port)
    # originally, it was
    # except Exception, e:
    # but this syntax is not supported anymore.
except Exception as e:
    print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
finally:
    s.close()