import pymysql
import time
from lib_resources.co_kpcloud import *
from lib_resources.co_migraciones import *
from api.api_insertar import *

def verificar_estado_migracion(ver_kpce, ce):
    try:
        ruta_json = f"documentos/{ce}/{ce}.json"
        with open(ruta_json, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)
        ruta_config = "config/config.json"
        with open(ruta_config, "r") as archivo:
            datos_config = json.load(archivo)
        server = datos_config["server"]
        if ver_kpce == True:
            print('Actualizar migraciones...')
            actualizar_migracion(datos, ce, server)
            return True
        else:
            print('Insertar migraciones...')
            insertar_migracion(datos, ce, server)
            return True
    except Exception as e:
        print("Error en el proceso verificar_estado_migracion(): ", e)
        return False

def verificar_logeo(page):
    try:
        try:
            texto = page.locator('#ctl00_ContentPlaceHolder1_lblMenuDinamico > table > tbody > tr:nth-child(1) > td:nth-child(3) > a')
            if str(texto) == 'NOTARÍAS - CONSULTA DE CARNÉ EXTRANJERÍA':
                print('Se inicio sesion con exito')
                return True
        except:
            texto = page.locator('#form1 > div.centrar > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > h3').inner_text()
            if str(texto) == 'MÓDULO DE ACCESO A SERVICIOS EN LÍNEA':
                return False     
    except Exception as e:
        print('Error en verificar_logeo: ',e)
        
def verificar_ce(ce, database):
    try:
        consulta = database.consultaCE(ce)
        if not consulta:
            return False
        elif consulta[0][0] == ce:  
            return True
        else:
            return False
    except Exception as e:
        print('Erro al verificar_ce: ', e)

def buscar_KpCloud(page, numero):
    try:
        iniciar_sesion_KP(page)
        persona_KP(page, numero) 
    except Exception as e:
        print(e)

def buscar_Migraciones(page, ces, database):
    print("Ejecutando bot de migraciones...")
    try:
        for arreglo in ces:
            ce = arreglo[0]
            iniciar_sesion_MIG(page)
            ver_logeo = verificar_logeo(page)
            #ver_logeo = True
            if ver_logeo == False:
                print('No se pudo iniciar sesion')
                time.sleep(5)
                buscar_Migraciones(page) 
            ruta = f"documentos/{ce}"   
            archivo_json = f'{ruta}/{ce}.json'  
            if os.path.exists(archivo_json):
                print("Ya existen los datos del cliente.") 
            else:
                #print('a')
                consulta_MIG(page, ce, archivo_json, ruta)
            ver_kpce = verificar_ce(ce, database)
            validacion = verificar_estado_migracion(ver_kpce, ce)
            buscar_KpCloud(page, ce)
            return validacion
    except Exception as e:
        print('Error en buscar_migraciones: ', e)
        return False
