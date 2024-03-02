import time
import mysql.connector
from datetime import datetime, timedelta

def conectar_bd():
    return mysql.connector.connect(host="localhost", user="root", passwd="", database="aplicaciones_iot")

def consultar_sensores(sensor_id):
    conexion = conectar_bd()
    instruccion = f"SELECT * FROM registros WHERE idSensor = {sensor_id}"
    consulta = conexion.cursor()
    consulta.execute(instruccion)
    resultado = ""
    for (idRegistro, idSensor, valor, fecha, hora) in consulta:
        resultado += "{}\t{}\t{}\t{}\t{}\n".format(idRegistro, idSensor, valor, fecha, hora)
    consulta.close()
    conexion.close()
    return resultado

def insertar_sensores(sensor, valor, fecha, hora):
    conexion = conectar_bd()
    instruccion = "INSERT INTO registros(idSensor, valor, fecha, hora) VALUES (%s, %s, %s, %s)"
    datos = (sensor, valor, fecha, hora)
    consulta = conexion.cursor()
    consulta.execute(instruccion, datos)
    n = consulta.rowcount
    conexion.commit()
    consulta.close()
    return n

def fecha_registro():
    hoy = time.strftime("%Y-%m-%d")
    return hoy

def tiempo_registro():
    ahora = time.strftime("%H:%M:%S")
    return ahora

