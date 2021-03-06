#!/usr/bin/python

"""
Authors:while True:
            # STREAM
            line = self.serial.read(512)
    Domenico Scotece
    Michele Solimando

Description:

"""
#   1 Intercept Client close socket (EOF or Read/Write Error)
#   2 Write on file
#   3 Send buffered data

import sys
import socket
from MessageProtocol import MessageProtocol


def main(argv):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Option to immediately reuse the socket if it is in TIME_WAIT status, due to a previous execution.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8282))
    server_socket.listen(1)

    while True:
        # accept connections
        print 'Wait for connection'
        (socketClient, address) = server_socket.accept()
        try:
            print 'Client ADDRESS: ', address
            # receive start message
            data = socketClient.recv(MessageProtocol.MSG_START.__len__())

            # DEBUG
            print data

            if data == MessageProtocol.MSG_START:
                print 'Start sending data to client'
                # send ack connection
                socketClient.sendall(MessageProtocol.MSG_OK)

                #DEBUG
                #Open test file
                try:
                    f = open('position.txt', 'r')
                except IOError as e:
                    print 'IOError ', e.strerror

                while True:
                    #STREAM
                    line=f.read(1024)
                    if len(line)==0:
                        socketClient.close()
                        break
                    socketClient.sendall(line)

            else:
                print >> sys.stderr, 'Protocol Error!! Exit'
                socketClient.close()
                # Exit with error code
                sys.exit(1)

        except (KeyboardInterrupt, SystemExit):
            print >> sys.stderr, 'KeyboardInterrupt or SystemExit Received. Exit.'
            socketClient.close()

        finally:
            # close connection
            print 'Client ', address, 'Disconnected.'
            socketClient.close()

if __name__ == "__main__":
    main(sys.argv[1:])
