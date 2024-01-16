import requests, socket
from time import sleep

started = False
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    r = requests.get('http://192.168.1.46:8000/home/connected')

    data = r.json()
    if len(data['up']) == 0:
        if not started:
            sock.connect(('192.168.1.30', 5001))
            sock.sendall(b'start')
            started = True
            print('started')
            requests.get('http://192.168.1.46/surveilance/newround')
        sleep(10)
    else:
        if started:
            sock.connect(('192.168.1.30', 5001))
            sock.sendall(b'finis')
            print('finised')
            started = False
        sleep(10)