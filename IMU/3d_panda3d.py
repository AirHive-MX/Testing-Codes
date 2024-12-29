from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Filename
import serial
import sys

# Configuración del puerto serie
SERIAL_PORT = "/dev/ttyACM0"  # Cambia según tu sistema
BAUD_RATE = 9600

# Configura la ventana y el motor de renderizado
loadPrcFileData("", "window-title Drone Viewer")  # Título de la ventana
loadPrcFileData("", "win-size 800 600")          # Tamaño de la ventana

class DroneViewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Configura el puerto serie
        try:
            self.serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print("Conexión al puerto serie establecida.")
        except Exception as e:
            print(f"Error al conectar con el puerto serie: {e}")
            sys.exit(1)

        # Carga el modelo del dron
        model_path = Filename.from_os_specific("./drone_final/drone_final.obj")
        self.drone = self.loader.loadModel(model_path)
        self.drone.reparentTo(self.render)       # Conecta el modelo a la escena
        self.drone.setScale(0.1, 0.1, 0.1)      # Ajusta la escala del modelo
        self.drone.setPos(0, 5, 0)              # Coloca el modelo en la escena

        # Orientación inicial del dron
        self.initial_orientation = (180, 90, 0)  # (H, P, R) iniciales
        self.drone.setHpr(*self.initial_orientation)

        # Configura la cámara
        self.camera.setPos(0, 0, 0)             # Posición de la cámara
        self.camera.lookAt(self.drone)          # Haz que la cámara mire al dron

        # Iluminación
        self.setup_lighting()

        # Variables para almacenar rotaciones del IMU
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        # Tarea para actualizar las rotaciones del dron
        self.taskMgr.add(self.update_drone_orientation, "UpdateDroneOrientation")

    def setup_lighting(self):
        """Configura una luz básica en la escena"""
        from panda3d.core import PointLight, AmbientLight

        # Luz ambiental
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.6, 0.6, 0.6, 1))  # Luz suave
        ambient_node = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_node)

        # Luz puntual
        point_light = PointLight("point_light")
        point_light.setColor((1, 1, 1, 1))  # Luz blanca
        point_node = self.render.attachNewNode(point_light)
        point_node.setPos(10, -10, 20)  # Coloca la luz
        self.render.setLight(point_node)

    def update_drone_orientation(self, task):
        """Lee los valores del IMU desde el puerto serie y actualiza la orientación del dron."""
        if self.serial_connection.in_waiting > 0:
            try:
                # Leer línea del puerto serie
                line = self.serial_connection.readline().decode(errors='replace').strip()

                # Verificar que la línea tenga los datos esperados
                if "Roll=" in line and "Pitch=" in line and "Yaw=" in line:
                    data = line.split("|")
                    self.roll = float(data[0].split("=")[1])
                    self.pitch = float(data[1].split("=")[1])
                    self.yaw = float(data[2].split("=")[1])

                    # Reasignar ejes para que coincidan con Panda3D
                    # El mapeo depende de cómo se orienta tu IMU y modelo
                    adjusted_h = self.initial_orientation[0] + self.yaw     # Yaw → Heading
                    adjusted_p = self.initial_orientation[1] + self.roll   # Roll → Pitch
                    adjusted_r = self.initial_orientation[2] + self.pitch  # Pitch → Roll (invertido)

                    # Aplicar las rotaciones al modelo
                    self.drone.setHpr(adjusted_h, adjusted_p, adjusted_r)

                    # Imprimir valores de orientación para depuración
                    print(f"Roll: {self.roll:.2f}°, Pitch: {self.pitch:.2f}°, Yaw: {self.yaw:.2f}°")
                else:
                    print(f"Línea no válida: {line}")

            except Exception as e:
                print(f"Error al procesar los datos del IMU: {e}")

        return task.cont

# Ejecuta la aplicación
app = DroneViewer()
app.run()
