import os
import sys
import time
from Serial.serial import GestionSerial
from models import crud  # Importa el módulo crud

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



def obtener_valor_sensor(sensor):
    gestion_serial.enviar_datos(sensor)
    valor = gestion_serial.recibir_datos()
    return valor

def procesar_opcion(entrada):
    if entrada == '1':
        mostrar_lista_plantas()
        planta_seleccionada = input("Selecciona la planta (a, b, c): ")
        print(f"Seleccionaste la planta {planta_seleccionada}")

    elif entrada == '2':
        print("Solicitando temperatura...")
        valor = obtener_valor_sensor(entrada)
        if valor:
            print(f"Valor de temperatura: {valor} %")
            # Si deseas insertar la temperatura en la base de datos, aquí puedes hacerlo
            # insertar_datos_en_bd(float(valor), None, None)
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '3':
        print("Solicitando luminosidad...")
        valor = obtener_valor_sensor(entrada)
        if valor:
            print(f"Valor de luminosidad: {valor}")
            # Si deseas insertar la luminosidad en la base de datos, aquí puedes hacerlo
            # insertar_datos_en_bd(None, None, float(valor))
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '4':
        print("Solicitando humedad...")
        valor = obtener_valor_sensor(entrada)
        if valor:
            print(f"Valor de humedad: {valor} %")
            # Si deseas insertar la humedad en la base de datos, aquí puedes hacerlo
            # insertar_datos_en_bd(None, float(valor), None)
        else:
            print("No se recibió respuesta desde Arduino")

    elif entrada == '5':
        print("Solicitando estado del riego...")
        valor = obtener_valor_sensor(entrada)
        if valor:
            print(f"Estado del riego: {valor}")
            # Si deseas insertar el estado del riego en la base de datos, aquí puedes hacerlo
            # insertar_datos_en_bd(None, None, None, valor)
        else:
            print("No se recibió respuesta desde Arduino")

    else:
        print("Opción no válida...")

def cerrar_arduino():
    gestion_serial.cerrar_conexion()

def menu_sensores():
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
        procesar_opcion(entrada)
        print(" ")
        print(menu)
        entrada = input("Captura una opcion: ")

    print("Saliendo del programa...")
    cerrar_arduino()

if __name__ == "__main__":
    print("Iniciando el menú de sensores...")
    menu_sensores()
