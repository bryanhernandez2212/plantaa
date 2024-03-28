from controllers.controlador import menu_sensores
from models.crud import insertar_sensores_auto

if __name__ == "__main__":
    print("Iniciando el menú de sensores...")
    menu_sensores()
    # print("Insertando automáticamente registros en la base de datos...")
    # insertar_sensores_auto()