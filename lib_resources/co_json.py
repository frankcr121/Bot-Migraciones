import json 

def apagar_bot():
    valor = 0
    data = {"encendido": valor}
    with open('encender.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print("Bot Apagado")
        
def leer_json():
    ruta_json = f"encender.json"
    with open(ruta_json, "r") as archivo:
        datos = json.load(archivo)
    encendido = datos["encendido"]
    return encendido