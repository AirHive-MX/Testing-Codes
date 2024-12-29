import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configura el puerto serie
port = "/dev/ttyACM0"  # Cambia según tu configuración
baudrate = 9600
ser = serial.Serial(port, baudrate)

# Inicializar datos
accel_x, accel_y, accel_z = [], [], []
gyro_x, gyro_y, gyro_z = [], [], []

def update(frame):
    global accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    if ser.in_waiting:
        try:
            data = ser.readline().decode("utf-8").strip().split(",")
            ax, ay, az, gx, gy, gz = map(float, data)

            # Actualizar listas
            accel_x.append(ax)
            accel_y.append(ay)
            accel_z.append(az)
            gyro_x.append(gx)
            gyro_y.append(gy)
            gyro_z.append(gz)

            # Mantener longitud fija
            if len(accel_x) > 100:
                accel_x.pop(0)
                accel_y.pop(0)
                accel_z.pop(0)
                gyro_x.pop(0)
                gyro_y.pop(0)
                gyro_z.pop(0)

            # Limpiar y volver a graficar
            ax1.clear()
            ax1.plot(accel_x, label="Accel X")
            ax1.plot(accel_y, label="Accel Y")
            ax1.plot(accel_z, label="Accel Z")
            ax1.legend()

            ax2.clear()
            ax2.plot(gyro_x, label="Gyro X")
            ax2.plot(gyro_y, label="Gyro Y")
            ax2.plot(gyro_z, label="Gyro Z")
            ax2.legend()

        except Exception as e:
            print(f"Error parsing data: {e}")

# Configurar gráfica
fig, (ax1, ax2) = plt.subplots(2, 1)
ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
