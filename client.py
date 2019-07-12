from multiprocessing import Process, Queue
import socket, sys
import pyaudio


def record(socket):
    '''capture stream from the microphone'''
    
    p = pyaudio.PyAudio()
    chunk = 256

    # initialize the input stream (input = True)
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100, 
        input=True,    
        frames_per_buffer=chunk)

    print("***** start recording")
    while True:

        # take data from the microphone
        data = stream.read(chunk) 
        
        if data:

            # send on socket
            socket.send(data)
        else:
            socket.close()
            break


def put(q, socket):
    '''adds data to Queue'''

    while True:
        response = sock.recv(256)
        if response:
            q.put(response)
        else:
            break


def play(q):
    '''sends data to play'''

    p = pyaudio.PyAudio()
    chunk = 4096

    # initialize the output stream (output = True)
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        output=True,        
        frames_per_buffer=chunk)

    while True:
        data = q.get()
        if data:
            # write the data in stream.
            stream.write(data)
        else:
            break


if __name__ == '__main__':
    try:
        host = str(sys.argv[1])
    except IndexError:
        host = 'localhost'
    try:    
        port = int(sys.argv[2])
    except IndexError:
        port = 9090
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))    
    except ConnectionRefusedError:
        print('error connecting to server')
    else:
        print('Connected to server. Host: {} Port: {}'.format(host, port))

        q = Queue()
        
        record = Process(target=record, args=(sock,))
        play = Process(target=play, args=(q,))
        put = Process(target=put, args=(q, sock,))
        
        record.start()
        play.start()
        put.start()