import serial
import time

class GestionSerial:
    def __init__(self, port, baudrate):
        self.serial_connection = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def enviar_datos(self, comando):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(f'{comando}:'.encode('ascii'))
                time.sleep(1)
            except Exception as e:
                print(f"Error al enviar datos: {e}")
        else:
            print("La conexión serial no está abierta")

    def recibir_datos(self):
        if self.serial_connection and self.serial_connection.is_open:
            respuesta = self.serial_connection.readline().decode('utf-8').strip()
            return respuesta
        else:
            return None
        # if self.serial_connection.in_waiting > 0:
        #     try:
        #         respuesta = self.serial_connection.readline().decode('utf-8').strip()
        #         return respuesta
        #     except Exception as e:
        #         print(f"Error al recibir datos: {e}")
        # else:
        #     return None

    def cerrar_conexion(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Conexión serial cerrada")
