import os
import sys
import time
from models.crud import insertar_sensores, fecha_registro, tiempo_registro
from Serial.serial import GestionSerial

directorio_actual = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(directorio_actual, '..'))
sys.path.append(root_dir)

gestion_serial = GestionSerial('COM3', 9600)
time.sleep(2)

def mostrar_lista_plantas():
    sub_menu_plantas = '''
    ======= [Menu Plantas]==============================
    || a - Cactus                                       ||
    || b - Tulipanes                                    ||
    || c - Violetas africanas (Saintpaulia)             ||
    ====================================================
    '''
    print(sub_menu_plantas)

def obtener_valor_sensor(sensor):
    gestion_serial.enviar_datos(sensor)
    valor = gestion_serial.recibir_datos()
    return valor

def procesar_opcion(entrada):
    if entrada == '1':
        mostrar_lista_plantas()
        planta_seleccionada = input("Selecciona la planta (a, b, c): ")
        print(f"Seleccionaste la planta {planta_seleccionada}")
        
    elif entrada in ['2', '3', '4']:
        valor = obtener_valor_sensor(entrada)
        print(f"{valor}")
        if insertar_sensores(entrada, valor, fecha_registro(), tiempo_registro()) > 0:
            print("Se insertó el registro exitosamente...")
        else:
            print("ERROR al insertar el registro") 

    elif entrada == '5':
        valor = obtener_valor_sensor(entrada)
        print(f"Estado de la bomba: {valor}")

    else:
        print("Opción no válida...")

def cerrar_arduino():
    gestion_serial.cerrar_conexion()
