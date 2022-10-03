'''
Tema: Clases y Objetos en Python
Fecha: 29 de septiembre del 2022
Autor: Leonardo Martínez González
'''
import mysql.connector

'''
Crear una clase de nombre MySQL que tenga las siguientes propiedades:
    MYSQL_HOST
    MYSQL_USER
    MYSQL_PASSWORD
    MYSQL_DATABASE
    MYSQL_CONNECTION
    MYSQL_CURSOR
    
y los siguientes métodos:
    constructor (host="localhost",user="root", pwd="", bd="opensource") que recibe parámetros
    con valores por defecto
    
    conectar_mysql(). se conecta a la Base de datos, 
    
    desconectar_mysql(). Cerrar la conexion a la Base de Datos
    
    consulta_sql(sql). Recibe la consulta SQL que ejecutará, desde este método se conectará a la
    Base de Datos y terminando de ejecutar la consulta se deconectará de la BD.

Utilizando la clase MySQL, cargue los datos a la Base de datos de:
    Estudiantes.txt
    Kardex.txt 

Genere las constraseñas a los estudiantes en una tabla llamada Usuarios, utilice la clase Password.

Para ello, cree la Base de Datos y las tablas: Estudiantes, Usuarios y Kardex con los campos que tienen
los archivos mencionados, considere integridad referencial.
Realice el CRUD a la tabla Kardex

Realice algo SIMILAR para MongoDB, considere solo consultas de una tabla.

para instalar mysql: pip install mysql-conector-python
para instalar pymongo: pip install pymongo
'''

class MySQL:
    def __init__(self, host="localhost", user="root",pws="", bd="opensource"):
        self.MYSQL_HOST = host
        self.MYSQL_USER = user
        self.MYSQL_PASSWORD = pws
        self.MYSQL_DATABASE = bd
        self.MYSQL_CONNECTION = None
        self.MYSQL_CURSOR = None

    def conectar_mysql(self):
        if self.MYSQL_CONNECTION == None:
            try:
                self.MYSQL_CONNECTION = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER,
                password = self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE)
            except Exception as error:
                print("Error",error)
    def desconectar_mysql(self):
        if self.MYSQL_CONNECTION is None:
            self.MYSQL_CONNECTION.close()

    def consulta_sql(self, sql):
        self.conectar_mysql()
        try:
            self.MYSQL_CURSOR.execute(sql)
        except mysql.connector.errors.ProgrammingError as e:
            print("Error en la consulta ", e)
        except Exception as error:
            print("ERROR: ", error)
        else:
            for reg in self.MYSQL_CURSOR:
                print(reg)
                self.MYSQL_CURSOR.close()
                self.desconectar_mysql()

objMySQL= MySQL()
objMySQL.consulta_sql("Select * from Productos")