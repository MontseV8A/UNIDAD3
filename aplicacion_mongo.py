import bcrypt
import random
from crudmysql import MySQL
from con_bd import variables
from caja import Password
from mongodb import PyMongo
from variables_mongo import variables_m
def cargar_estudiantes():
    obj_MySQL = MySQL(variables)
    obj_PyMongo = PyMongo(variables_m)
    #consultas
    sql_estudiante = "select * from estudiantes;"
    sql_kardex = "select * from kardex;"
    sql_usuario = "select * from usuarios;"
    obj_MySQL.conectar_mysql()
    lista_estudiantes=obj_MySQL.consulta_sql(sql_estudiante)
    lista_kardex = obj_MySQL.consulta_sql(sql_kardex)
    lista_usuarios=obj_MySQL.consulta_sql(sql_usuario)
    obj_MySQL.desconectar_mysql()
    #insertar datos en mongo
    obj_PyMongo.conectar_mongodb()
    for est in lista_estudiantes:
        e={}
        e['control']=est[0]
        e['nombre']=est[1]
        obj_PyMongo.insertar('estudiantes', e)
    for mat in lista_kardex:
        k = {}
        k['control'] = mat[1]
        k['materia'] = mat[2]
        k['calificacion'] = float(mat[3])
        obj_PyMongo.insertar('kardex', k)
    for us in lista_usuarios:
        u={}
        u['idUsuario']=us[0]
        u['control']=us[1]
        u['clave']=us[2]
        u['clave_cifrada']=us[3]
        obj_PyMongo.insertar('usuarios', u)
    obj_PyMongo.desconectar_mongodb()



def insertar_estudiante():
    obj_PyMongo = PyMongo(variables_m)
    print(" == INSERTAR ESTUDIANTES ==")
    ctrl = input("Dame el numero de control: ")
    nombre = input("Dame el nombre del estudiante: ")
    clave = input("Dame la clave de acceso: ")
    obj_usuario = Password(longitud=len(clave), contrasena=clave)
    json_estudiante = {'control': ctrl, 'nombre': nombre} #f"INSERT INTO estudiantes values('{ctrl}','{nombre}');"
    json_usuario = {'idUsuario': 100, 'control': ctrl, 'clave': clave, 'clave_cifrada': obj_usuario.contrasena_cifrada.decode()}#f'INSERT INTO usuarios(control,clave,clave_cifrada) values("{ctrl}","{clave}","{obj_usuario.contrasena_cifrada.decode()}");'
    # print(sql_usuario)
    obj_PyMongo.conectar_mongodb()
    obj_PyMongo.insertar('estudiantes',json_estudiante)
    obj_PyMongo.insertar('usuarios',json_usuario)
    obj_PyMongo.desconectar_mongodb()
    print("Datos insertados correctamente")

def actualizar_calificacion():
    obj_PyMongo = PyMongo(variables_m)
    print(" == ACTUALIZAR PROMEDIO ==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a actualizar: ")
    filtro_buscar_materia = {"control": ctrl, "materia": materia}
    obj_PyMongo.conectar_mongodb()
    respuesta = obj_PyMongo.consulta_mongodb('kardex', filtro_buscar_materia)
    if respuesta:
        promedio = float(input("Dame el nuevo promedio: "))
        json_actualiza_prom = {"$set": {"calificacion": promedio}}
        obj_PyMongo.actualizar_mongo('kardex',filtro_buscar_materia,json_actualiza_prom)
        print("Promedio ha sido actualizado")
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia: {materia} NO EXISTE")
    obj_PyMongo.desconectar_mongodb()

def eliminar_estudiante():
    obj_PyMongo = PyMongo(variables_m)
    print(" == Eliminar estudiante ==")
    ctrl = input("Dame el numero de control: ")
    filtro_buscar_estudiante = {"control": ctrl}
    obj_PyMongo.conectar_mongodb()
    respuesta = obj_PyMongo.consulta_mongodb('estudiante', filtro_buscar_estudiante)
    print(respuesta)
    if respuesta:
        print(respuesta)
        obj_PyMongo.eliminar_mongo('estudiantes',filtro_buscar_estudiante)
        print(f"El estudiante con el número de control {ctrl} ha sido ELIMINADO")
    else:
        print(f"El estudiante con numero de control {ctrl}  NO EXISTE")
    obj_PyMongo.desconectar_mongodb()


def consultar_materias():
    objPyMongo = PyMongo(variables_m)
    print("CONSULTA MATERIAS DEL ESTUDIANTE")
    ctrl = input("Dame el número de control: ")
    filtro = {'control': ctrl}
    atributos_estudiante = {"_id":0, "nombre":1}
    atributos_kardex={"_id":0,"materia":1,"calificacion":1}
    #sql_materias = f"select E.nombre, K.materia, K.calificacion from estudiantes E, kardex K where E.control = K.control and E.control= '{ctrl}';"
    objPyMongo.conectar_mongodb()
    resp1=objPyMongo.consulta_mongodb('estudiantes', filtro, atributos_estudiante)
    resp2=objPyMongo.consulta_mongodb('kardex', filtro, atributos_kardex)
    #print("respuesta1", resp1)
    #print("respuesta 2 ", resp2)
    objPyMongo.desconectar_mongodb()
    # resp = obj_MySQL.consulta_sql(sql_materias)
    if resp1["status"] and resp2["status"]:
        print("estudiante: ", resp1["resultado"][0]["nombre"])
        for mat in resp2["resultado"]:
            print(f"Materia:{mat['materia'],mat['calificacion']}")

def consulta_general():
    obj_PyMongo = PyMongo(variables_m)
    print("CONSULTA GENERAL")
    atributos_estudiante = {"_id": 0, "control": 1}
    atributos_kardex = {"_id": 0, "materia": 1, "calificacion": 1}
    # sql_materias = f"select E.nombre, K.materia, K.calificacion from estudiantes E, kardex K where E.control = K.control and E.control= '{ctrl}';"
    obj_PyMongo.conectar_mongodb()
    resp1 = obj_PyMongo.consulta_general('estudiantes')
    resp2 = obj_PyMongo.consulta_general('kardex')
    obj_PyMongo.desconectar_mongodb()

    if resp1["status"] and resp2["status"]:
        for est in resp1["resultado"]:
            promedio=0
            cont=0
            for mat in resp2["resultado"]:
                if est['control'] == mat['control']:
                    #print(f"Calificacion:{ mat['calificacion']}")
                    promedio+=mat['calificacion']
                    cont+=1
            #print(promedio)
            #print(cont)
            print(f"control:{est['control']}, {est['nombre']} calificacion")
        print(promedio/cont)

                #print(f"Estudiante: {est['control']}")promedio = (acumulado + promedio) / cont        #print(f"Materia:{mat['materia'], mat['calificacion']}")
                #
def menu():
    while(True):
        print("-----Menú Principal-----")
        print("1. Insertar estudiante")
        print("2. Actualizar calificación")
        print("3. Consultar materias por estudiante")
        print("4. Consulta general de estudiantes")
        print('5. Eliminar un estudiante')
        print("6. Salir")
        print("Selecciona una opción: ")
        try:
            opcion=int(input(""))
        except Exception as error :
            print("Error", error)
            break
        else:
            if opcion == 1:
                insertar_estudiante()
            elif opcion ==2:
                actualizar_calificacion()
            elif opcion ==3:
                consultar_materias()
            elif opcion ==4:
                consulta_general()
            elif opcion ==5:
                eliminar_estudiante()
            elif opcion ==6:
                break
            else:
                print("Opción incorrecta")
menu()


#cargar_estudiantes()