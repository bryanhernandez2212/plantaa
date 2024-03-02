import serial, time

class GestionSerial:
    def __init__(self, port, baudrate):
        self.serial_connection = serial.Serial(port, baudrate)
        time.sleep(2)

    def abrir_conexion(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Conexión serial establecida en {self.port}")
        except serial.SerialException as e:
            print(f"Error al abrir la conexión serial: {e}")

    def cerrar_conexion(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Conexión serial cerrada")

    @staticmethod
    def enviar_datos(self, comando):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(f'{comando}:'.encode('utf-8'))
                time.sleep(1)  # Esperar para asegurar que la respuesta se haya recibido completamente
                respuesta = self.serial_connection.readline().decode('utf-8').strip()
                print(f"Respuesta Arduino: {respuesta}")
            except UnicodeEncodeError:
                print("Error al codificar datos")
            except UnicodeDecodeError:
                print("Error al decodificar datos")
        else:
            print("La conexión serial no está abierta")
    @staticmethod
    def recibir_datos(self):
        with self.serial_connection:
            while True:
                if self.serial_connection.in_waiting > 0:
                    respuesta = self.serial_connection.readline().decode('utf-8').strip()
                    self.serial_connection.flushInput()
                    time.sleep(0.1)
                    return respuesta