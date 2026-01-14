import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def persona_KP(page, numero):
    try:
        fecha_actual = datetime.today()
        fecha_actual = fecha_actual + relativedelta(years=1)
        fecha_actual = fecha_actual.strftime('%d/%m/%Y')
        page.wait_for_selector('#MENUHORIZONTAL_MPAGE')
        page.goto(f"")
        frame = page.frame_locator("#gxp0_ifrm")
        frame.locator('#PERFICFCHVENC').fill(fecha_actual)  
        with page.expect_file_chooser() as fc_info:  
            frame.locator("#PERFICREN").click()  
            file_chooser = fc_info.value
            file_chooser.set_files(f"./documentos/{numero}/ficha_{numero}.pdf")  
            time.sleep(1)
            frame.locator('#BUTTON1').click() 
        time.sleep(1)
        page.locator('#BUTTON1').click
        page.reload()
        com_fech = page.locator('#span_W0324PERFICFCHREG_0001').inner_text()
        # if com_fech == fecha_actual:
        #     print('Se subieron los documentos')
        #     return True
        # else:
        #     print('No se subieron los documentos')
        #     return False
        print(f"Se subio la ficha {numero}")
        return True
    except Exception as e:
        print(f"Error al subir la ficha {numero}: ",e)
        return False

def iniciar_sesion_KP(page):
    try:
        page.goto('')
        time.sleep(1)
        usuario = ''
        contrasena = '' 
        page.wait_for_selector('#user')
        #page.locator('#user').press_sequentially(usuario, delay = 100)
        page.click('#user')
        page.keyboard.type(usuario, delay = 100)
        #page.locator('#user').fill(usuario)
        page.wait_for_selector('#password')
        #page.locator('#password').press_sequentially(contrasena, delay = 100)
        page.click('#password')
        page.keyboard.type(contrasena, delay=100)
        page.click('#login')
    except Exception as e:
        print(e)