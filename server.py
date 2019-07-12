import select
from time import time
import socket 
import sys 

host = 'localhost'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen() 
input = [server,] 

while True: 
    try:
        inputready, outputready, exceptready = select.select(input,[],[])
    except:
        break 

    for s in inputready: 

        if s == server: 
            client, address = server.accept() 
            input.append(client) 
            print ('new client added {}'.format(str(address)))

        else: 
            try:
                #start_recv = time()
                data = s.recv(256)
                #vr_recv = time() - start_recv
                if data:
                    #start_send = time()
                    s.send(data)
                    #vr_send = time() - start_send
                    #ping = time() - start_recv
                    #print('  get: {0:.3f}ms ({1:.7f}sec) || send: {2:.3f}ms ({3:.7f}sec) PING: {4:.5f}'.format(vr_recv*1000, vr_recv, vr_send*1000, vr_send, ping), end='\r', flush=True) 

                else:  
                    #print()
                    s.close() 
                    input.remove(s) 
                    continue
            except ConnectionResetError:
                #print()
                continue

server.close()