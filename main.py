import requests, os
from bs4 import BeautifulSoup
from elementos import Modulo,Clase,Funcion,Excepcion,Atributo,Metodo,Constante
import writer, json


URLFUNCIONES = "https://docs.python.org/es/3/library/functions.html"
URLTIPOS = "https://docs.python.org/es/3/library/stdtypes.html"
URLEXCEPCIONES = "https://docs.python.org/es/3/library/exceptions.html"
URLMODULOS = "https://docs.python.org/es/3/py-modindex.html"
URLMODULOSBASE = "https://docs.python.org/es/3/"

# Ejemplo de Módulo
# URLFUNCIONES = "https://docs.python.org/es/3/library/time.html"
# URLFUNCIONES =  "https://docs.python.org/es/3/library/sqlite3.html"
# URLFUNCIONES = "https://docs.python.org/es/3/library/email.errors.html"

######
#  dl con class "py function" son las funciones
#       class "sig-name descname" es el nombre de la funcion. pueden ser varios nombres
#       class "sig-param", es el parámetro.
#           El parámetro se puede dividir en (NO SIEMPRE APARECE)
#               span class="o" atributos opcionales como *
#               span class="n" es el nombre del parámetro
#               span class="default_value" es el valor por defecto


#   dl con class "py class" son clases
#       hay clases con varios "sig-name descname" que parecen ser varios constructores
#       una clase puede tener dentro class="py method". Están anidados


def limpiar(cadena):
    return " ".join(cadena.replace('¶','').split())

def limpiar_parametro(parametro):
    # Hay parámetros que no vienen en detalle y vienen enteros. Del estilo start=0
    # La idea es quedarse con lo que hay antes del igual
    if "=" in parametro:
        return parametro[:parametro.find("=")]
    else:
        return parametro


def obtener_parametros(nombre):
    # Chequeamos que tenga parámetros. Están a la misma altura que el nombre.
    parametros = nombre.find_next_siblings("em", {"class":"sig-param"})
    lista = []

    for parametro in parametros:
    
        nombre_parametro = parametro.find("span", {"class":"n"})            
        if nombre_parametro:
            lista.append(nombre_parametro.text)
        else: 
            lista.append(limpiar_parametro(parametro.text))

    return lista


def obtener_metodos(clase):

    metodos = clase.find_all("dl", {"class":"py method"})
    lista = []

    for metodo in metodos:
        sintaxis = metodo.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})

        dMetodo = Metodo()
        dMetodo.nombre = nombre.text
        dMetodo.add_sintaxis(limpiar(sintaxis.text))
        for parametro in obtener_parametros(nombre):
            dMetodo.add_parametro(parametro)

        lista.append(dMetodo)

    return lista
 
    
        
def obtener_atributos(clase):

    atributos = clase.find_all("dl", {"class":"py attribute"})
    lista = []

    for atributo in atributos:
        sintaxis = atributo.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        
        dAtributo = Atributo()
        dAtributo.nombre = nombre.text
        dAtributo.sintaxis = limpiar(sintaxis.text)
        lista.append(dAtributo)

    return lista


def existe_clase(modulo,nombre_clase):
    
    encontrado = False
    x=0
    
    while ((not encontrado) and (x<len(modulo.clases))):
        if modulo.clases[x].nombre == nombre_clase:
            encontrado = True
        else:
            x = x+1

    if encontrado:
        return x
    else:
        return -1
        

def analiza_modulo(nombre_modulo,URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')

    dModulo = Modulo()
    dModulo.nombre = nombre_modulo
    
    ## Funciones
    print ("----------FUNCIONES----------")
    funciones = soup.find_all("dl", {"class":"py function"})
    print ("Hay " + str(len(funciones)) + " funciones.")
    
    for funcion in funciones:

        # Buscamos la primera sintaxis
        sintaxis = funcion.find("dt")
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        parametros = obtener_parametros(nombre)

        dFuncion = Funcion()
        dFuncion.nombre = nombre.text
        dFuncion.add_sintaxis(limpiar(sintaxis.text))

        for parametro in parametros:
            dFuncion.add_parametro(parametro)

        # Buscamos si hay más sintaxis
        mas_sintaxis = sintaxis.find_next_siblings("dt")
        for s in mas_sintaxis:                    
            nombre = s.find("code", {"class":"sig-name descname"})                    
            parametros = obtener_parametros(nombre)            

            for parametro in parametros:
                dFuncion.add_parametro(parametro)

        dModulo.add_funcion(dFuncion)            

    ## Clases
    print ("----------CLASES----------")
    clases = soup.find_all("dl", {"class":"py class"})
    print ("Hay " + str(len(clases)) + " clases.")
    
    for clase in clases:        
        
        # Buscamos la primera sintaxis    
        sintaxis = clase.find("dt")
        nombre = sintaxis.find("code", {"class":"sig-name descname"})                
        parametros = obtener_parametros(nombre)
        metodos = obtener_metodos(clase)

        dClase = Clase()
        dClase.nombre =  nombre.text
        
        dConstructor = Metodo()
        dConstructor.nombre = nombre.text
        dConstructor.add_sintaxis(limpiar(sintaxis.text))
        for parametro in parametros:
            dConstructor.add_parametro(parametro)

        for metodo in metodos:
            dClase.add_metodo(metodo)
        

        # Comprobamos si hay dt al mismo nivel con más signatura
        mas_sintaxis = sintaxis.find_next_siblings("dt")
        for s in mas_sintaxis:            
            nombre = s.find("code", {"class":"sig-name descname"})        
            parametros = obtener_parametros(nombre)
            metodos = obtener_metodos(clase)         
 
            dConstructor.add_sintaxis(limpiar(s.text))
            for parametro in parametros:
                dConstructor.add_parametro(parametro)

            for metodo in metodos:
                dClase.add_metodo(metodo)
        

        dClase.add_constructor(dConstructor)

        atributos = obtener_atributos(clase)
        for atributo in atributos:
            dClase.add_atributos(atributo)


        for clase in dModulo.clases:
            print (clase.nombre)
        print ("--")


        dModulo.add_clase(dClase)
    
    # Métodos no asociados directamente a la clase, aunque son de una clase
    # Hay métodos que son de clases que no se han definido aquí. Hay que mirar su clase base, sino ignorarlos
    print ("----------METODOS----------")
    
    metodos = soup.find_all("dl", {"class":"py method"})

    for metodo in metodos:

        # Hay métodos con varias sintaxis
        sintaxis = metodo.find_all("dt")
        
        for s in sintaxis:
            # Solo los que son de una clase
            clase = s.find("code",{"class":"sig-prename descclassname"})
            if clase:                
                nombre = s.find("code", {"class":"sig-name descname"})        
                parametros = obtener_parametros(nombre)

                dMetodo = Metodo()
                dMetodo.nombre = nombre.text
                dMetodo.sintaxis = limpiar(s.text)
                for parametro in parametros:
                    dMetodo.add_parametro(parametro)

                # Hay que ver si actualizamos sobre una clase que existe o sobre una nueva
                posicion = existe_clase(dModulo,clase.text[:-1])
                if (posicion > 0):
                    print ("existe clase " + str(posicion))
                    dModulo.clases[posicion].add_metodo(dMetodo)                    
                else:
                    dClase = Clase()
                    dClase.nombre = clase.text[:-1]
                    dClase.add_metodo(dMetodo)
                    dModulo.add_clase(dClase)
                    print ("no existe la clase " + str(posicion))


    # Hay atributos que no están debajo de la clase
    # Hay que mirar su clase base, sino ignorarlos ya que están en clase y ya se han añadido
    print ("----------ATRIBUTOS----------")
    atributos = soup.find_all("dl", {"class":"py attribute"})
    for atributo in atributos:
        sintaxis = atributo.find("dt")
        clase = sintaxis.find("code",{"class":"sig-prename descclassname"})
        if clase:
            print ("Clase: "+ clase.text)
            nombre = sintaxis.find("code", {"class":"sig-name descname"})        
            print ("Atributo: " + nombre.text)
            print ("Sintaxis: " + limpiar(sintaxis.text))

    # Constantes
    print ("----------CONSTANTES----------")
    constantes = soup.find_all("dl", {"class":"py data"})
    for constante in constantes:
        sintaxis = constante.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print ("Constante: " + nombre.text)
        print ("Sintaxis: " + limpiar(sintaxis.text))

    # Excepciones
    print ("----------EXCEPCIONES---------")
    excepciones = soup.find_all("dl", {"class":"py exception"})
    for excepcion in excepciones:
        sintaxis = excepcion.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print ("Excepcion: " + nombre.text)
        print ("Sintaxis: " + limpiar(sintaxis.text))

    return dModulo


# Inicio del Programa
print ("Analizando la documentación Python")
documentacion = []

# 1. Funciones Base
print ("1. Funciones Base")
documentacion.append(analiza_modulo("base","https://docs.python.org/es/3/library/stdtypes.html"))

# 2. Tipos Base


# 3. Excepciones Base


# 4. Módulos
page = requests.get(URLMODULOS)
soup = BeautifulSoup(page.content, 'html5lib')

tabla = soup.find("table", {"class":"indextable modindextable"})
modulos = tabla.find_all("a")

#for modulo in modulos:
    #print (modulo.text)
    #lista = lista_funciones(URLMODULOSBASE + modulo.get("href"),lista)
   

# Imprimimos todo
#for modulo in documentacion:
#    print (str(modulo))




'''
def lista_funciones(URL,lista):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')


    nombre_capa = URL[URL.index("#")+1:]
    #print (nombre_capa)
    
    capa = soup.find("div",{"id":nombre_capa})
    if not capa:
        capa = soup.find("span",{"id":nombre_capa})

    funciones = capa.find_all("dl", {"class":"py function"})
    
    for funcion in funciones:    
        # Buscamos la primera sintaxis
        sintaxis = funcion.find("dt")
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        

        if any(dictionary for dictionary in lista if dictionary["nombre"] == nombre.text):
            print ("COINCIDE " + nombre.text)
            print (next(dictionary for dictionary in lista if dictionary["nombre"] == nombre.text))
        else:
            e = {
                "nombre": nombre.text,
                "modulo": nombre_capa
            }
            # print(e)
            lista.append(e)

    return lista
'''





