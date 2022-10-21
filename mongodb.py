#Clase para conectarnos a mongo db
'''import pymongo
from variables_mongo import  variables
from con_bd import variables as varsmysql
from crudmysql import MySQL

class PyMongo():
    def __init__(self, variables): #host='localhost', db='opensource',port=27017,timeout=1000,user="",password=""
        self.MONGO_DATABASE = variables["db"]
        self.MONGO_URI ='mongodb://'+ variables["host"] + ':'+ str(variables["port"])
        self.MONGO_CLIENT= None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT=variables["timeout"]
    
    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT =pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
            
        except Exception as error:
            print("ERROR ", error)
        else:
            print("Conexion al servidor de mongo_db realizada")
        #finally:
            #if MONGO_CLIENT:
               # MONGO_CLIENT.close()
    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
                self.MONGO_CLIENT.close()
                
    def consulta_mongodb(self,tabla):
        self.MONGO_RESPUESTA =self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find({})
        if self.MONGO_RESPUESTA:
            for reg in self.MONGO_RESPUESTA:
                print(reg)

    def insertar_estudiante(self,est):
        self.MONGO_RESPUESTA =self.MONGO_CLIENT['itj_estudiantes']['estudiantes'].insert_one(est)
        if self.MONGO_RESPUESTA:
           return True
        else:
            return False

def cargar_estudiantes_mongo():
    obj_MySQL = MySQL(varsmysql)
    obj_Mongo=PyMongo(variables)
    sql = "Select * from estudiantes;"
    obj_MySQL.conectar_mysql()
    lista_estudiantes = obj_MySQL.consulta_sql(sql)
    obj_MySQL.desconectar_mysql()
    obj_Mongo.conectar_mongodb()
    for est in lista_estudiantes:
        e={
            "control":est[0],
            "nombre":est[1]
        }
        obj_Mongo.insertar_estudiante(e)
    obj_Mongo.desconectar_mongodb()

cargar_estudiantes_mongo()
alumno={
    "control": 200,
    "nombre": "Montserrat Valdovinos Ochoa"
}

# obj_Mongo = PyMongo(variables)
# obj_Mongo.conectar_mongodb()
# obj_Mongo.insertar_estudiante(alumno)
# obj_Mongo.desconectar_mongodb()
'''

# Clase para conectarnos a MongoDB

import pymongo
from variables_mongo import variables_m
from con_bd import variables as varsmysql
from crudmysql import MySQL


class PyMongo:
    def __init__(self, variables):  # host='localhost', db='opensource', port=27017, timeout=1000, user='', password=''
        self.MONGO_DATABASE = variables["db"]
        self.MONGO_URI = 'mongodb://' + variables["host"] + ':' + str(variables["port"])
        self.MONGO_CLIENT = None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT = variables["timeout"]

    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
        except Exception as error:
            print("ERROR", error)
        else:
            pass
            #print("Conexión al servidor de MongoDB realizada: ", )
        # finally:

    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def consulta_mongodb(self, tabla, filtro, atributos={"_id": 0}):
        response = {"status":False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find(filtro,atributos)
        if self.MONGO_RESPUESTA:
            response["status"]=True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
            return response
        else:
            return None
    # Insertar datos en la coleccion de estudiantes

    def consulta_general(self,tabla):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find({})
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
            return response
        else:
            return None
    def insertar(self, tabla, doc):

        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(doc)
        if self.MONGO_RESPUESTA:
            return True
        else:
            return None

    def actualizar_mongo(self,tabla, filtro, nuevos_valores):
        response= {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_many(filtro, nuevos_valores)
        if self.MONGO_RESPUESTA:
            response["status"]= True
            #return self.MONGO_RESPUESTA
       # else:
            #return None
        return response

    def eliminar_mongo(self,tabla, filtro):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_many(filtro)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            return self.MONGO_RESPUESTA
        return response

def cargar_estudiantes():
    obj_MySQL = MySQL(varsmysql)
    obj_Mongo = PyMongo(variables_m)
    sql = "SELECT * FROM estudiantes;"
    obj_MySQL.conectar_mysql()
    lista_estudiantes = obj_MySQL.consulta_sql(sql)
    obj_MySQL.desconectar_mysql()
    obj_Mongo.conectar_mongodb()
    for est in lista_estudiantes:
        e = {
            "control": est[0],
            "nombre": est[1]
        }
        print(e)
        obj_Mongo.insertar('estudiantes', e)
    obj_Mongo.desconectar_mongodb()


#cargar_estudiantes()

# alumno = {
#     'control': 200,
#     'nombre': 'Piter Pan'
# }

# obj_Mongo = PyMongo(variables)
# obj_Mongo.conectar_mongodb()
# obj_Mongo.insertar_estudiante(alumno)
# obj_Mongo.desconectar_mongodb()

