import os
import sys
import time
import serial
from models.crud import insertar_sensores, fecha_registro, tiempo_registro
from Serial.serial import GestionSerial
from controllers.controlador import mostrar_lista_plantas, procesar_opcion, cerrar_arduino, obtener_valor_sensor

directorio_actual = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(directorio_actual, '..'))
sys.path.append(root_dir)


def menu_sensores():
    menu = '''======= [Menu sensores]=======
    || 1 - Seleccionar planta      ||
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
    menu_sensores()
