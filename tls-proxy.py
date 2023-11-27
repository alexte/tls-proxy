#!/usr/bin/env python3

import argparse
import select
import socket
import ssl

BUFFER_SIZE = 1024000

def server_connection(dst):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    ip, port = dst.split(':')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,int(port)))
    ssock=ctx.wrap_socket(sock)
    return ssock


def tls_proxy(srv_port, dst):
    sockets = []

    ip, port = dst.split(':')

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    srv.bind(("0.0.0.0",int(srv_port)))
    srv.listen(3)

    print ("listening connection on port "+srv_port)

    sockets.append(srv);

    while True:
        print(f"waiting for {len(sockets)} sockets")
        socks,_,_=select.select(sockets,[],[]);

        for sock in socks:
            if sock==srv:
                print("new client")
                client,_=srv.accept()
                print(f"new connection")
                sockets.append(client)
                server=server_connection(dst)
                sockets.append(server)
            else:
                buf=sock.recv(BUFFER_SIZE)
                id=sockets.index(sock)
                if id%2==1: 
                    if len(buf) == 0:
                        sockets[id].close()
                        sockets[id+1].close()
                        del sockets[id]
                        del sockets[id]
                    else:
                        sockets[id+1].sendall(buf)
                else: 
                    if len(buf) == 0:
                        sockets[id-1].close()
                        sockets[id].close()
                        del sockets[id-1]
                        del sockets[id-1]
                    else:
                        sockets[id-1].sendall(buf)


def main():
    parser = argparse.ArgumentParser(description='TLS TCP  proxy.')

    parser.add_argument('-p', '--port', required=True, help='Listening Port')
    parser.add_argument('-d', '--dst', required=True, help='Destination IP and port, 192.168.1.1:443')

    args = parser.parse_args()

    tls_proxy(args.port, args.dst)


if __name__ == '__main__':
    main()


