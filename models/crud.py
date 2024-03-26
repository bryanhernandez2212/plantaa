import mysql.connector
import time

conexion = None
gestion_serial = None

def conectar_bd():
    global conexion
    try:
        conexion = mysql.connector.connect(host="localhost", user="root", passwd="", database="aplicaciones")
        print("Conexión a la base de datos establecida correctamente")
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")

def fecha_registro():
    hoy = time.strftime("%Y-%m-%d")
    return hoy

def tiempo_registro():
    ahora = time.strftime("%H:%M:%S")
    return ahora

def inicializar_serial(ser):
    global gestion_serial
    gestion_serial = ser
    conectar_bd()  # Conecta a la base de datos
    # Otras inicializaciones si es necesario...

def obtener_datos_desde_arduino(sensor_id):
    global gestion_serial
    print("Solicitando datos desde Arduino...")
    if sensor_id == '2':
        gestion_serial.enviar_datos('2')  # Envía el comando '2' para solicitar temperatura desde el Arduino
    elif sensor_id == '3':
        gestion_serial.enviar_datos('3')  # Envía el comando '3' para solicitar luminosidad desde el Arduino
    elif sensor_id == '4':
        gestion_serial.enviar_datos('4')  # Envía el comando '4' para solicitar humedad desde el Arduino
    elif sensor_id == '5':
        gestion_serial.enviar_datos('5')  # Envía el comando '5' para solicitar estado del riego desde el Arduino
    else:
        print("ID de sensor no válido")
        return None
    
    valor = gestion_serial.recibir_datos()
    print("Valor recibido desde Arduino:", valor)
    return valor

def insertar_datos_en_bd(sensor_id, valor):
    global conexion
    cursor = conexion.cursor()
    try:
        fecha = fecha_registro()
        hora = tiempo_registro()
        print("Insertando datos en la base de datos...")
        print(f"Sensor ID: {sensor_id}, Valor: {valor}, Fecha: {fecha}, Hora: {hora}")
        cursor.execute("INSERT INTO registros (idSensor, fecha, hora, valor) VALUES (%s, %s, %s, %s)", (sensor_id, fecha, hora, valor))
        conexion.commit()
        print("Datos insertados correctamente en la base de datos:", valor)  # Mensaje de depuración
    except mysql.connector.Error as error:
        print(f"Error al insertar datos: {error}")
        conexion.rollback()
    finally:
        cursor.close()


def insertar_sensores_auto():
    global gestion_serial, conexion
    if not gestion_serial or not conexion:
        print("Error: La conexión serial o la conexión a la base de datos no están disponibles.")
        return

    print("Iniciando inserción automática de datos en la base de datos...")

    cursor = conexion.cursor()

    # Insertar sensores si aún no existen
    try:
        cursor.execute("INSERT INTO sensores (nombre) VALUES ('Temperatura')")
        cursor.execute("INSERT INTO sensores (nombre) VALUES ('Luminosidad')")
        cursor.execute("INSERT INTO sensores (nombre) VALUES ('Humedad')")
        conexion.commit()
        print("Sensores insertados correctamente")
    except mysql.connector.Error as error:
        print(f"Error al insertar sensores: {error}")
        conexion.rollback()

    # Bucle para insertar registros de sensores automáticamente cada 10 segundos
    try:
        while True:
            print("Esperando respuesta desde Arduino...")
            sensor_id = input("Ingrese el ID del sensor (2: Temperatura, 3: Luminosidad, 4: Humedad, 5: Estado del riego): ")
            valor = obtener_datos_desde_arduino(sensor_id)
            if valor is not None:
                print("Datos recibidos desde Arduino:", valor)
                insertar_datos_en_bd(sensor_id, valor)
            else:
                print("No se recibió respuesta desde Arduino")
            time.sleep(10)  # Esperar 10 segundos antes de la siguiente inserción
    except KeyboardInterrupt:
        print("Inserción automática detenida por el usuario")
    except Exception as e:
        print(f"Error en la inserción automática: {e}")
    finally:
        cursor.close()

