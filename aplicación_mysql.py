'''
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
import bcrypt
import random
from crudmysql import MySQL
from caja import Password
from con_bd import variables
def regresa_conjunto_estudiantes():
    estudiantes = set()
    with open("estudiantes.prn") as arch_estudiantes:
        for linea in arch_estudiantes:
            control = linea[0:8]
            nombre = linea[8:-1]
            estudiantes.add((control,nombre))
    # Cerrar el archivo
    arch_estudiantes.close()
    return estudiantes

def regresa_conjunto_promedios():
    promedios_materias = set()
    with open("kardex.txt") as kardex:
        for linea in kardex:
            control = linea.split("|")[0]
            materia = linea.split("|")[1]
            promedio = linea.split("|")[2][:-1]  # el -1 para no incluir el último caracter
            promedios_materias.add((control,materia,promedio))
    # Cerrar el archivo
    kardex.close()
    return promedios_materias
def cargar_materias():
    objKardex=MySQL(variables)
    lista_materias=regresa_conjunto_promedios()
    for ctrl,nom,cal in lista_materias:
        sql=f"INSERT INTO kardex(control,materia,calificacion) values('{ctrl}','{nom}','{cal}');"
        print(sql)
        objKardex.consulta_sql(sql)
#cargar_materias()
def cargar_datos():
    objEstudiante = MySQL(variables)
    lista_estudiantes = regresa_conjunto_estudiantes()
    for ctrl,nom in lista_estudiantes:
        sql=f"INSERT INTO estudiantes values('{ctrl}','{nom}');"
        print(sql)
        objEstudiante.consulta_sql(sql)

   # print(lista_estudiantes)
#cargar_datos()
def regresa_usuarios():
    lista_usuarios = set()
    with open("usuarios.txt") as usuarios:
        for us in usuarios:
            control = us.split("|")[0]
            contrasena = us.split("|")[1]
            contrasena_cifrada = us.split("|")[2][:-1]  # el -1 para no incluir el último caracter
            lista_usuarios.add((control, contrasena,contrasena_cifrada))

    # Cerrar el archivo
    usuarios.close()
    return lista_usuarios
#print(regresa_usuarios())
def cargar_usuarios():
    objUsuarios = MySQL(variables)
    lista_usuarios=regresa_usuarios()
    for ctrl,clve,ccve in lista_usuarios:
        sql=f"INSERT INTO usuarios (control,clave,clave_cifrada) values('{ctrl}','{clve}','{ccve}');"
        print(sql)
        objUsuarios.consulta_sql(sql)
#cargar_usuarios()


def generar_letra_mayuscula():  # Regresa una Letra desde la A .. Z
    return chr(random.randint(65,90))

def generar_letra_minuscula():  # Regresa una letra minuscula desde la a ...  z
    return chr(random.randint(97,122))

def generar_numeros():  # Regresa un numero aleatorio entre 0 .... 9
    return chr(random.randint(48,57))

def generar_caracter_especial():  # Regresa un caracter especial
    lista_caracteres = ['@', '#', '$','%','&','_','?','!']
    return lista_caracteres[random.randint(0,7)]

def generar_contrasena():
    clave = ""
    for i in range(0,10):
        numero = random.randint(1,5)
        if numero == 1:
            clave = clave + generar_letra_mayuscula()
        elif numero == 2:
            clave = clave + generar_letra_minuscula()
        elif numero == 3:
            clave = clave + generar_caracter_especial()
        elif numero >= 4 and numero <= 5:
            clave = clave + generar_numeros()
    # Regresar la contraseña
    return clave

#print(generar_contrasena())

# Cifrar las contraseñas con bcrypt
def cifrar_contrasena(contrasena):
    sal = bcrypt.gensalt() # Default tiene de 12
    contrasena_cifrada = bcrypt.hashpw(contrasena.encode('utf-8'), sal)
    return contrasena_cifrada

# clave = generar_contrasena()
# print(clave,cifrar_contrasena(clave))

#print(bcrypt.checkpw("_@3S8&@3TK".encode('utf-8'),"$2b$12$2CJJaULDzRi51zw2K8e3yeT5zLWz0tOrNE0e5f2nk3q5RzX6Rl6YG".encode('utf-8')))

# Generar el archivo de usuarios:
def generar_archivo_usuarios():
    #Obtener la lista de estudiantes
    estudiantes = regresa_conjunto_estudiantes()
    usuarios = open("usuarios.txt", "w")
    contador = 1
    for est in estudiantes:
        c,n = est
        clave = generar_contrasena()
        clave_cifrada = cifrar_contrasena(clave)
        registro = c + "|" + clave + "|" + str(clave_cifrada, 'utf-8') + "\n"
        usuarios.write(registro)
        contador += 1
        print(contador)
    print("Archivo generado")


#generar_archivo_usuarios()

def verificar_contraseña(us, psw):
    res={}
    if us!=" ":
        archivo=open("usuarios.txt", 'r')
        usu=archivo.read().split("\n")

        for al in usu:
            info=al.split("|")
            if len(info)>0:
                if info[0] == us:
                    pswn=psw.encode('utf-8')
                    pswe=info[3].encode('utf-8')
                    iguales=bcrypt.checkpw(pswn,pswe)
                    if iguales == True:
                        res={"Bandera" : True, "Usuario" :  info[1],"Mensaje" : "Datos correctos bienvenido"}
                    else:
                        res={"Bandera" : False, "Mensaje": "Datos incorrectos para el usuario", "Usuario": info[1]}

                    break
    if len(res)==0:
        res={"Bandera": False, "Usuario: ": "", "Mensaje" : "Usuario inexistente"}
    print(res)

#verificar_contraseña("18420451","@g$W3Io6uv")

def insertar_estudiante():
    obj_MySQL = MySQL(variables)
    print(" == INSERTAR ESTUDIANTES ==")
    ctrl = input("Dame el numero de control: ")
    nombre = input("Dame el nombre del estudiante: ")
    clave = input("Dame la clave de acceso: ")
    obj_usuario = Password(longitud=len(clave), contrasena=clave)
    sql_estudiante = f"INSERT INTO estudiantes values('{ctrl}','{nombre}');"
    sql_usuario = f'INSERT INTO usuarios(control,clave,clave_cifrada) values("{ctrl}","{clave}","{obj_usuario.contrasena_cifrada.decode()}");'
    # print(sql_usuario)
    obj_MySQL.conectar_mysql()
    obj_MySQL.consulta_sql(sql_estudiante)
    obj_MySQL.consulta_sql(sql_usuario)
    obj_MySQL.desconectar_mysql()
    print("Datos insertados correctamente")

def actualizar_calificacion():
    obj_MySQL = MySQL(bd="itj_estudiantes")
    print(" == ACTUALIZAR PROMEDIO ==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a actualizar: ")
    sql_buscar_materia = f"SELECT 1 FROM kardex" \
                         f" WHERE control='{ctrl}' AND materia='{materia.strip()}';"
    print(sql_buscar_materia)
    obj_MySQL.conectar_mysql()
    respuesta = obj_MySQL.consulta_sql(sql_buscar_materia)
    obj_MySQL.desconectar_mysql()
    if respuesta:
        promedio = float(input("Dame el nuevo promedio: "))
        sql_actualiza_prom = f"UPDATE kardex set calificacion={promedio} " \
                             f"WHERE control='{ctrl}' and materia='{materia.strip()}';"
        obj_MySQL.conectar_mysql()
        obj_MySQL.consulta_sql(sql_actualiza_prom)
        obj_MySQL.desconectar_mysql()
        print("Promedia ha sido actualizado")
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia: {materia} NO EXISTE")


# def insertar_estudiante():
#     obj_MySQL=MySQL(bd="itj_estudiantes")
#     print("INSERTAR ESTUDIANTES")
#     ctrl= input("Ingresa el número de control : ")
#     nombre= input("Ingresa el nombre del estudiante: ")
#     clave=input("Ingresa una clave: ")
#     obj_usuario = Password(longitud=len(clave),contrasena=clave)
#     sql_estudiante = f"INSERT INTO estudiantes values('{ctrl}', '{nombre}');"
#     sql_usuarios=f'INSERT INTO usuarios (control, clave,clave_cifrada) values("{ctrl}","{clave}", "{obj_usuario.contrasena_cifrada.decode()}");'
#     obj_MySQL.consulta_sql(sql_estudiante)
#     obj_MySQL.consulta_sql(sql_usuarios)
#     print("datos insertados correctamente")


def actualiza_calificacion():
    obj_MySQL = MySQL(bd="itj_estudiantes")
    print("ACTUALIZA CALIFICACIÓN")
    ctrl = input("Ingresa el número de control : ")
    materia = input("Ingresa el nombre de la materia: ")
    sql_buscar_materia= f"SELECT 1 FROM kardex WHERE control = '{ctrl}' AND materia='{materia.strip()}'"
    respuesta=obj_MySQL.consulta_sql(sql_buscar_materia)
    if respuesta:
        promedio=float(input("Dame el nuevo promedio: "))
        sql_actualiza_promedio= f"UPDATE kardex set calificacion = {promedio} WHERE control='{ctrl}' and materia ='{materia}';"
        obj_MySQL.consulta_sql(sql_actualiza_promedio)
        print("Promedio actualizado...")
    else:
        print(f"El estudiante con número de control {ctrl} o la materia {materia} no existe")
    #sql_materia=f"UPDATE kardex set calificacion ={100} WHERE control='18420100' and materia ='Contabilidad Financiera';"

def consultar_materias():
    obj_MySQL = MySQL(bd="itj_estudiantes")
    print("CONSULTA MATERIAS DEL ESTUDIANTE")
    ctrl = input("Dame el número de control: ")
    sql_materias=f"select E.nombre, K.materia, K.calificacion from estudiantes E, kardex K where E.control = K.control and E.control= '{ctrl}';"
    resp=obj_MySQL.consulta_sql(sql_materias)
    if resp:
        print("estudiante: ", resp[0][0])
        for mat in resp:
            print("Materia: ",mat[1],"|","Calificación: ",mat[2])

def consulta_general():
    obj_MySQL = MySQL(variables)
    sql_general="select E.control, E.nombre, format(avg(K.calificacion),1) as Promedio from estudiantes E, kardex K where E.control = K.control group by K.control;"
    resp=obj_MySQL.consulta_sql(sql_general)
    print("CONTROL: |", "MATERIA: |", "PROMEDIO: |")
    for est in resp:
        print(est[0],est[1],est[2])


def eliminar_estudiante():
    obj_MySQL=MySQL(bd="itj_estudiantes")
    ctrl=input("Ingresa el numero de control a eliminar: ")
    sql_eliminar1=f"delete from kardex where control = '{ctrl}';"
    sql_eliminar2=f"delete from usuarios where control='{ctrl}';"
    sql_eliminar3=f"delete from estudiantes where control='{ctrl}';"
    obj_MySQL.consulta_sql(sql_eliminar1)
    obj_MySQL.consulta_sql(sql_eliminar2)
    obj_MySQL.consulta_sql(sql_eliminar3)
    print(f"El estudiante con numero de control {ctrl} ha sido eliminado")
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
                actualiza_calificacion()
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

