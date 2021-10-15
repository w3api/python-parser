import requests, os
from bs4 import BeautifulSoup
from elementos import ElementoHTML
import writer, json


#URLFUNCIONES = "https://docs.python.org/es/3/library/functions.html"
# URLFUNCIONES = "https://docs.python.org/es/3/library/stdtypes.html"

URLMODULOS = "https://docs.python.org/es/3/py-modindex.html"
URLMODULOSBASE = "https://docs.python.org/es/3/"

# Ejemplo de Módulo
# URLFUNCIONES = "https://docs.python.org/es/3/library/time.html"
URLFUNCIONES =  "https://docs.python.org/es/3/library/sqlite3.html"
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

    for parametro in parametros:
    
        nombre_parametro = parametro.find("span", {"class":"n"})            
        if nombre_parametro:
            print(nombre_parametro.text)
        else: 
            print(limpiar_parametro(parametro.text))

def obtener_metodos(clase):

    metodos = clase.find_all("dl", {"class":"py method"})
    for metodo in metodos:
        sintaxis = metodo.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print ("Método: " + nombre.text)
        print ("Sintaxis: " + limpiar(sintaxis.text))
        obtener_parametros(nombre)


def obtener_atributos(clase):

    atributos = clase.find_all("dl", {"class":"py attribute"})
    for atributo in atributos:
        sintaxis = atributo.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print ("Atributo: " + nombre.text)
        print ("Sintaxis: " + limpiar(sintaxis.text))
        

def todos_los_elementos():

    page = requests.get(URLFUNCIONES)
    soup = BeautifulSoup(page.content, 'html5lib')

    
    ## Funciones
    print ("----------FUNCIONES----------")
    funciones = soup.find_all("dl", {"class":"py function"})
    print ("Hay " + str(len(funciones)) + " funciones.")
    
    for funcion in funciones:
        
        # Buscamos la primera sintaxis
        sintaxis = funcion.find("dt")
        print (limpiar(sintaxis.text))
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print (nombre.text)
        obtener_parametros(nombre)

        # Buscamos si hay más sintaxis
        mas_sintaxis = sintaxis.find_next_siblings("dt")
        for s in mas_sintaxis:        
            print (limpiar(s.text))    
            nombre = s.find("code", {"class":"sig-name descname"})        
            print (nombre.text)
            obtener_parametros(nombre)            

    ## Clases
    print ("----------CLASES----------")
    clases = soup.find_all("dl", {"class":"py class"})
    print ("Hay " + str(len(clases)) + " clases.")
    
    for clase in clases:
        
        # Buscamos la primera sintaxis    
        sintaxis = clase.find("dt")
        nombre = sintaxis.find("code", {"class":"sig-name descname"})        
        print ("Clase: " + nombre.text)
        print ("Signatura: " + limpiar(sintaxis.text))
        obtener_parametros(nombre)
        obtener_metodos(clase)
        

        # Comprobamos si hay dt al mismo nivel con más signatura
        mas_sintaxis = sintaxis.find_next_siblings("dt")
        for s in mas_sintaxis:            
            nombre = s.find("code", {"class":"sig-name descname"})        
            print ("Clase: " + nombre.text)
            print ("Signatura: " + limpiar(s.text))
            obtener_parametros(nombre)
            obtener_metodos(clase)            
        
        obtener_atributos(clase)
    
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
                print ("Clase: "+ clase.text)
                nombre = s.find("code", {"class":"sig-name descname"})        
                print ("Método: " + nombre.text)
                print ("Sintaxis: " + limpiar(s.text))
                obtener_parametros(nombre)

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


# Inicio del Programa
print ("Analizando la documentación Python")
todos_los_elementos()



'''
# Recorrer los módulos
page = requests.get(URLMODULOS)
soup = BeautifulSoup(page.content, 'html5lib')

tabla = soup.find("table", {"class":"indextable modindextable"})
modulos = tabla.find_all("a")

lista = []

for modulo in modulos:
    print (modulo.text)
    lista = lista_funciones(URLMODULOSBASE + modulo.get("href"),lista)
    #print (len(lista))


lista = sorted(lista)
for e in lista:
    print (e)
'''
