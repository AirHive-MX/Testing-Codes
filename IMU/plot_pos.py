import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuración del puerto serie
port = "/dev/ttyACM0"  # Cambia esto por el puerto de tu Arduino
baudrate = 9600
ser = serial.Serial(port, baudrate)

# Inicializar listas para los datos
pos_x, pos_y, pos_z = [], [], []
roll_data, pitch_data, yaw_data = [], [], []

def update(frame):
    global pos_x, pos_y, pos_z, roll_data, pitch_data, yaw_data
    if ser.in_waiting:
        try:
            # Leer datos del puerto serie
            line = ser.readline().decode("utf-8").strip()

            # Dividir los valores recibidos por Arduino
            if "Position" in line and "Orientation" in line:
                # Separar la línea en partes
                pos_part, orient_part = line.split("Orientation")

                # Procesar posición
                pos_values = pos_part.replace("Position (m):", "").strip().split()
                x = float(pos_values[0].split("=")[1])
                y = float(pos_values[1].split("=")[1])
                z = float(pos_values[2].split("=")[1])
                pos_x.append(x)
                pos_y.append(y)
                pos_z.append(z)

                # Procesar orientación
                orient_values = orient_part.replace("(°):", "").strip().split()
                roll = float(orient_values[0].split("=")[1])
                pitch = float(orient_values[1].split("=")[1])
                yaw = float(orient_values[2].split("=")[1])
                roll_data.append(roll)
                pitch_data.append(pitch)
                yaw_data.append(yaw)

                # Limitar el tamaño de las listas
                if len(pos_x) > 100:
                    pos_x.pop(0)
                    pos_y.pop(0)
                    pos_z.pop(0)
                    roll_data.pop(0)
                    pitch_data.pop(0)
                    yaw_data.pop(0)

                # Actualizar gráficos
                ax1.clear()
                ax1.plot(pos_x, pos_y, label="Position X-Y")
                ax1.plot(pos_x, pos_z, label="Position X-Z")
                ax1.set_title("Position (X, Y, Z)")
                ax1.set_xlabel("X (m)")
                ax1.set_ylabel("Y/Z (m)")
                ax1.legend()

                ax2.clear()
                ax2.plot(roll_data, label="Roll")
                ax2.plot(pitch_data, label="Pitch")
                ax2.plot(yaw_data, label="Yaw")
                ax2.set_title("Orientation (Roll, Pitch, Yaw)")
                ax2.set_xlabel("Time")
                ax2.set_ylabel("Angle (°)")
                ax2.legend()

        except Exception as e:
            print(f"Error parsing data: {e}")

# Configuración de las gráficas
fig, (ax1, ax2) = plt.subplots(2, 1)
ani = animation.FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()
