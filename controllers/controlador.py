import os
import sys
import time
from Serial.serial import GestionSerial
from models import crud  # Importa el módulo crud
import threading
import queue

directorio_actual = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(directorio_actual, '..'))
sys.path.append(root_dir)

gestion_serial = GestionSerial('COM9', 9600)  # Ajusta el puerto y la velocidad según tu configuración
time.sleep(2)

crud.inicializar_serial(gestion_serial)  # Inicializa la conexión serial en el módulo 'crud'

def mostrar_lista_plantas():
    sub_menu_plantas = '''
    ======= [Menu Plantas]==============================
    || a - Cactus                                       ||
    || b - Tulipanes                                    ||
    || c - Violetas africanas (Saintpaulia)             ||
    ====================================================
    '''
    print(sub_menu_plantas)

# Resto del código permanece sin cambios...

def hilo_escucha_para_arduino(q, stop_event):
    data = ""
    while not stop_event.is_set():
        valor = gestion_serial.recibir_datos()
        if valor:
            partes = valor.split(":")
            data_inicio = partes[0]
            # verificar los datos enviados desde arduino
            if data_inicio.isdigit():
                crud.insertar_datos_en_bd(data_inicio, partes[1])
            if data_inicio == "tr":
                id_sensor = partes[1]
                if len(partes) > 2:
                    # datos enviados despues de una consulta en el menu
                    valor_sensor = partes[2]
                    crud.insertar_datos_en_bd(id_sensor, valor_sensor)
                    if id_sensor == "2":
                        data = f"Temperatura: {valor_sensor}"
                    elif id_sensor == "3":
                        data = f"Luminosida: {valor_sensor}"
                    elif id_sensor == "4":
                        data = f"Humedad: {valor_sensor}"
                if id_sensor == "2":
                    data = f"Temperatura sigue igual "
                elif id_sensor == "3":
                    data = f"Luminosida sigue igual "
                elif id_sensor == "4":
                    data = f"Humedad sigue igual "
                q.put(data)
            if data_inicio == "bom":
                estado = partes[1]
                if estado == "1":
                    data = "Estado del riego: Encendido "
                else:
                    data = "Estado del riego:Apagado"
                q.put(data)
        else:
            q.put(None)
                    


def obtener_valor_sensor(sensor):
    gestion_serial.enviar_datos(sensor)
    # valor = gestion_serial.recibir_datos()
    # return valor

def procesar_opcion(entrada, queue):
    if entrada == '1':
        mostrar_lista_plantas()
        planta_seleccionada = input("Selecciona la planta (a, b, c): ")
        print(f"Seleccionaste la planta {planta_seleccionada}")

    elif entrada == '2':
        print("Solicitando temperatura...")
        obtener_valor_sensor(entrada)
        data = queue.get()
        if data:
            print(data)
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '3':
        print("Solicitando luminosidad...")
        obtener_valor_sensor(entrada)
        data = queue.get()
        if data:
            print(data)
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '4':
        print("Solicitando humedad...")
        obtener_valor_sensor(entrada)
        data = queue.get()
        if data:
            print(data)
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '5':
        print("Solicitando estado del riego...")
        obtener_valor_sensor(entrada)
        data = queue.get()
        if data:
            print(data)
        else:
            print("No se recibió respuesta desde Arduino")
    else:
        print("Opción no válida...")

def cerrar_arduino():
    gestion_serial.cerrar_conexion()

def menu_sensores():
    q = queue.Queue()  # Creamos una cola
    stop_event = threading.Event()
    # Creamos y ejecutamos el hilo secundario
    t = threading.Thread(target=hilo_escucha_para_arduino, args=(q,stop_event))
    t.start()
    
    mostrar_lista_plantas()

    while True:
        planta_seleccionada = input("Selecciona la planta (a, b, c): ")
        if planta_seleccionada in ['a', 'b', 'c']:
            print(f"Seleccionaste la planta {planta_seleccionada}")
            break
        else:
            print("Planta no válida. Por favor, selecciona una opción válida.")

    menu = '''======= [Menu sensores]=======
    || 2 - Mostrar temperatura     ||
    || 3 - Mostrar luminosidad     ||
    || 4 - Mostrar humedad         ||
    || 5 - Estado del riego        ||
    || s - Salir del programa      ||
    =================================='''

    print(menu)
    entrada = input("Captura una opcion: ")

    while entrada != 's':
        procesar_opcion(entrada, q)
        print(" ")
        print(menu)
        entrada = input("Captura una opcion: ")
    stop_event.set()  # Indicamos al hilo secundario que debe detenerse
    t.join()  # Esperamos a que el hilo secundario termine
    print("Saliendo del programa...")
    cerrar_arduino()
    

if __name__ == "__main__":
    print("Iniciando el menú de sensores...")
    menu_sensores()
