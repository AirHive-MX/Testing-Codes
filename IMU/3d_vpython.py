import serial
from vpython import *
import time

PORT = "/dev/ttyACM0"  # Ajusta
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

scene.title = "Visual 3D estilo Betaflight"
scene.width = 800
scene.height = 600
scene.background = color.gray(0.9)

# Construir dron sencillo
body = box(length=2, width=2, height=0.1, color=color.red)
arm1 = cylinder(pos=vector(-1,0,0), axis=vector(2,0,0), radius=0.05, color=color.blue)
arm1.parent = body

def set_orientation(obj, pitch, roll, yaw):
    # Reset a la identidad
    obj.up = vector(0,1,0)
    obj.axis = vector(1,0,0)
    # Rotar en orden (yaw -> pitch -> roll) o el que necesites
    obj.rotate(angle=radians(yaw),   axis=vector(0,0,1))
    obj.rotate(angle=radians(pitch), axis=vector(1,0,0))
    obj.rotate(angle=radians(roll),  axis=vector(0,1,0))

while True:
    rate(30)
    #line = ser.readline().decode().strip()
    if not line:
        continue
    data = line.split(',')
    if len(data) < 3:
        continue
    try:
        pitch = float(data[0])
        roll  = float(data[1])
        yaw   = float(data[2])
        set_orientation(body, pitch, roll, yaw)
    except:
        pass
