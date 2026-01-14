import requests, json

def insertar_migracion(datos, ce, server):
    url = f"{server}api/migraciones/insertar-migraciones"  
    documento = "CE"
    tipo_persona = 'N'
    nombre = datos["nombre"]
    apellido_paterno = datos["apellido_paterno"]
    apellido_materno = datos["apellido_materno"]
    genero = datos["genero"]
    fecha_nacimiento = datos["fecha_nacimiento"]
    estado_civil = datos["estado_civil"]
    nacionalidad = datos["nacionalidad"]
    data = {
        "documento": documento,
        "numero": ce,
        "tipo_persona": tipo_persona,
        "nombre": nombre,
        "apellido_paterno": apellido_paterno,
        "apellido_materno" : apellido_materno,
        "genero": genero,
        "fecha_nacimiento": fecha_nacimiento,
        "estado_civil": estado_civil,
        "nacionalidad": nacionalidad
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Registro agregado exitosamente:", response.json())
    elif response.status_code == 400:
        print("Error de autenticación o datos inválidos:", response.json())
    else:
        print("Error:", response.status_code, response.json())

def actualizar_migracion(datos, ce, server):
    url = f"{server}api/migraciones/actualizar-migracion"  
    nombre = datos["nombre"]
    apellido_paterno = datos["apellido_paterno"]
    apellido_materno = datos["apellido_materno"]
    genero = datos["genero"]
    fecha_nacimiento = datos["fecha_nacimiento"]
    estado_civil = datos["estado_civil"]
    nacionalidad = datos["nacionalidad"]
    data = {
        "numero": ce,
        "nombre": nombre,
        "apellido_paterno": apellido_paterno,
        "apellido_materno" : apellido_materno,
        "genero": genero,
        "fecha_nacimiento": fecha_nacimiento,
        "estado_civil": estado_civil,
        "nacionalidad": nacionalidad
    }

    response = requests.put(url, json=data)

    if response.status_code == 200:
        print("Registro actualizado exitosamente:", response.json())
    elif response.status_code == 400:
        print("Error de autenticación o datos inválidos:", response.json())
    else:
        print("Error:", response.status_code, response.json())
