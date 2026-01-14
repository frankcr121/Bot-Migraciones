import json
import os
import pathlib
import time
from lib_resources.re_gmail import *

def descargar_img(page, urlImg, nombre_archivo, ruta):
    # Descargar la imagen usando fetch
    imagen_bytes = page.evaluate(f'''
        async () => {{
            const response = await fetch("{urlImg}");
            const buffer = await response.arrayBuffer();
            return Array.from(new Uint8Array(buffer));
        }}
    ''')
    with open(f"{ruta}/{nombre_archivo}.png", "wb") as archivo:
        archivo.write(bytearray(imagen_bytes))

    print(f"{nombre_archivo} descargada correctamente.")

def iniciar_sesion_MIG(page):
    try:
        page.goto('')
        usuario = ''
        contrasena = ''
        page.locator('#txtLogin').click()
        page.keyboard.type(usuario)
        time.sleep(2)
        page.locator('#txtPas').click()
        page.keyboard.type(contrasena)
        page.click('#btnIngresar')
    except Exception as e:
        print('Error al iniciar sesion: ',e)

def consulta_MIG(page, CE, archivo_json, ruta):
    try:
        page.wait_for_selector('#ctl00_ContentPlaceHolder1_lblMenuDinamico > table > tbody > tr:nth-child(1) > td:nth-child(3) > a')
        page.click('#ctl00_ContentPlaceHolder1_lblMenuDinamico > table > tbody > tr:nth-child(1) > td:nth-child(3) > a')
        #OBTENER DATOS PERSONALES
        try:
            page.locator('#ctl00_ContentPlaceHolder1_txtNroBusqueda').fill(CE)
            page.locator('#ctl00_ContentPlaceHolder1_btnBuscar').click()
            page.wait_for_selector('#divCENotarias > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td')
            apellido_paterno = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(1)').inner_text()
            apellido_materno = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(2)').inner_text()
            if apellido_materno == " ":
                apellido_materno = " "
            nombre = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(3)').inner_text()
            genero = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(4)').inner_text()
            fecha_nacimiento = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(5)').inner_text()
            estado_civil = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(6)').inner_text()
            nacionalidad = page.locator('#ctl00_ContentPlaceHolder1_gwPersona > tbody > tr:nth-child(2) > td:nth-child(7)').inner_text()
            datos_persona = {
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "genero": genero,
                "fecha_nacimiento": fecha_nacimiento,
                "estado_civil": estado_civil,
                "nacionalidad": nacionalidad
            }
            os.makedirs(ruta, exist_ok=True)
            with open(archivo_json, 'w', encoding='utf-8') as file:
                json.dump(datos_persona, file, ensure_ascii=False, indent=4)
            
            print('Se guardó los datos en el JSON:', archivo_json)
        except Exception as e:
            to_s = ''
            enviar_email(to_s, "BOT MIGRACIONES", str(e))
            print('Error al guardar los datos del cliente',e)
        
        #DESCARGAR PDF
        try:
            ruta_descargas = os.path.join(os.getcwd(), f"{ruta}")
            with page.expect_download() as download_info:
                page.locator('#ctl00_ContentPlaceHolder1_btnDescargar').click()
            descarga = download_info.value
            nuevo_nombre = f"ficha_{CE}.pdf"
            ruta_archivo = os.path.join(ruta_descargas, nuevo_nombre)
            descarga.save_as(ruta_archivo)
            print(f"PDF descargado correctamente: {ruta_archivo}")
        except Exception as e:
            print("Error al descargar el PDF:", e)
        
        #DESCARGAR IMAGENES
        page.locator('#btnGrabar').click()
        page.wait_for_selector('#popupColor > div > div.PopupCuerpo > div:nth-child(1)')
        try:
            url_foto = page.evaluate('''() => {
            const img = document.querySelector("#ctl00_ContentPlaceHolder1_imgPersonaFoto");
            return new URL(img.getAttribute("src"), window.location.href).href;
            }''')
            # Descargar la imagen usando fetch
            nombre_archivo = 'img_foto'
            descargar_img(page, url_foto, nombre_archivo, ruta)
        except Exception as e:
            print('Error al descargar foto:', e)
        try:
            url_firma = page.evaluate('''() => {
                const img = document.querySelector("#ctl00_ContentPlaceHolder1_imgPersonaFirma");
                return new URL(img.getAttribute("src"), window.location.href).href;
            }''')
            nombre_archivo = 'img_firma'
            descargar_img(page, url_firma, nombre_archivo, ruta)
        except Exception as e:
            print('Error al descargar la firma: ', e)
        try:
            url_huella = page.evaluate('''() => {
                const img = document.querySelector("#ctl00_ContentPlaceHolder1_imgPersonaHuella");
                return new URL(img.getAttribute("src"), window.location.href).href;
            }''')
            nombre_archivo = 'img_huella'
            descargar_img(page, url_huella, nombre_archivo, ruta)
        except Exception as e:
            print('Error al descargar la huella: ', e)
        
    except Exception as e:
        print('Error en Consultar_MIG():', e)