import pymysql

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='',  
            user='', 
            password='',  
            port='',  
            db='',  
        )

        self.cursor = self.connection.cursor()
        print("Conexión a base de datos exitosa.")

    def db_close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexión a base de datos cerrada.")
        
    def consultar_migraciones(self):
        sql = """select MigNum, MigEst from tmmig10
                where MigEst = '1'"""
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            return info
        except Exception as e:
            print(f"Error al ejecutar el Procedimiento consultar_migraciones en BD: ", str(e))
            return False
    
    def consulta_datos(self, numero):
        sql = f"""select MigNom, MigApp, MigApm, MigGen, MigFechNac, MigEstCiv, MigNacio from tmmig10 where MigNum = {numero}"""
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            return info
        except Exception as e:
            print(f"Error al ejecutar el Procedimiento consultaCE en BD: ", str(e))
            return False

    def consultaCE(self, numero):
        sql = f"""select MigNum from tmmig10
                where MigNum = '{numero}'"""
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            return info
        except Exception as e:
            print(f"Error al ejecutar el Procedimiento consultaCE en BD: ", str(e))
            return False

    def ListarCE(self):
        sql = """select MigCe from tmmig10"""
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            return info
        except Exception as e:
            print(f"Error al ejecutar el Procedimiento ListarCE en BD: ", str(e))
            return False
