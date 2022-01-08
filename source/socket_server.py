import socket
import pygal
import json

HOST = '0.0.0.0'
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

x = []
y = []
z = []
c = []
data = ""
            
def stringProcess(data,x,y,z,c):
    while '}' in data :
        s = data[:data.find('}')+1]
        data = data[data.find('}')+1:]
        s = json.loads(s)
        x.append(s["x"])
        y.append(s["y"])
        z.append(s["z"])
        c.append(s["s"])
    if len(data) != 0:
        return data
    else:
        return ""

print("Server starting at: %s : %s" % (HOST, PORT))

while True:
    conn, addr = s.accept()
    print("Connected by : ", addr)
    while len(c) == 0 or c[-1] <= 200 :
        if(len(c) != 0 ) :
            print(c[-1])
        data += conn.recv(1024).decode('utf-8')
        print(data)
        if '}' in data :
            data = stringProcess(data,x,y,z,c)
    print("Closing connection\n")
    conn.close()
    break

line_chart = pygal.Line()
line_chart.title = 'Acceleration data in 300 seconds'
line_chart.x_labels = map(str, range(0, 200))
line_chart.add('x', x)
line_chart.add('y', y)
line_chart.add('z', z)
line_chart.render_to_file('chart.svg')