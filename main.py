import time
import json
from playwright.sync_api import sync_playwright
from lib_resources.co_principal import *
from lib_resources.re_gmail import *
from lib_resources.co_migraciones import *
from lib_resources.co_json import *
from lib_resources.co_conexion import DataBase

database = DataBase()

def main():
    while True:
        with sync_playwright() as p:
            encendido = leer_json()  
            if encendido == 0:
                print("No hay datos por procesar...")
            else:
                database = DataBase()
                ces = database.consultar_migraciones()  
                rutaDir = "C:/tmp/bot-migraciones"
                browser = p.chromium.launch_persistent_context(rutaDir, headless=False)  
                page = browser.new_page()
                migra = buscar_Migraciones(page, ces, database)
                browser.close()
                database.db_close()
                apagar_bot()
        time.sleep(10)

if __name__ == "__main__":
    main()
