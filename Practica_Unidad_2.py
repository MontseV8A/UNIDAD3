import json
import bcrypt
import random

def regresa_conjunto_estudiantes():
    estudiantes = set()
    lista_estudiante = ()
    try:
        with open("estudiantes.prn") as arch_estudiantes:
            for linea in arch_estudiantes:
                control = linea[0:8]
                nombre = linea[8:-1]
                estudiantes.add((control,nombre))
        # Cerrar el archivo
        arch_estudiantes.close()
        return estudiantes
    except:
        print("Error al abrir el archivo")


def regresa_conjunto_promedios():
    promedios_materias = set()
    try:
        with open("kardex.txt") as kardex:
            for linea in kardex:
                control = linea.split("|")[0]
                materia = linea.split("|")[1]
                promedio = linea.split("|")[2][:-1]  # el -1 para no incluir el último caracter
                promedios_materias.add((control,materia,promedio))
        # Cerrar el archivo
        kardex.close()
    except:
        print("ERROR AL ABRIR EL ARCHIVO")
        kardex.close()
    return promedios_materias

def regresa_datos(ctrl):
    estudiantes = regresa_conjunto_estudiantes()
    promedios = regresa_conjunto_promedios()
    datos = dict() # Creamos el diccionario
    lista_materias = []
    nombre = ""
    promedio = 0.0
    for alu in estudiantes:
        if ctrl == alu[0]:
            nombre = alu[1]
            promedio_acumulado = 0 # Para acumular los promedios
            numero_materias = 0 # Para contar el número de materias.
            for mat in promedios:
                if ctrl == mat[0]:
                    materia = {}
                    materia["Nombre"] = mat[1]
                    materia["Promedio"] = int(mat[2])
                    lista_materias.append(materia)
                    promedio_acumulado += int(mat[2])
                    numero_materias += 1
                    promedio = promedio_acumulado / numero_materias
                else:
                    for mat in promedios:
                        if ctrl=='':
                            materia={}
                            materia["Nombre"] = mat[1]
                            materia["Promedio"]=int(mat[2])
                            lista_materias.append(materia)
                            promedio_acumulado+=int(mat[2])
                            numero_materias+=1
                            promedio=promedio_acumulado/numero_materias

# Ya se puede formar el JSON
    datos["Nombre"] = nombre
    datos["Materias"] = lista_materias

    return json.dumps(datos) # regresar el JSON

print(regresa_datos('18420100'))





