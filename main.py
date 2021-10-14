import requests, os
from bs4 import BeautifulSoup
from elementos import ElementoHTML
import writer, json


URLFUNCIONES = "https://docs.python.org/es/3/library/functions.html"

# URLFUNCIONES = "https://docs.python.org/es/3/library/stdtypes.html"

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
    return " ".join(cadena.split())


def limpiar_signatura(cadena):
    return cadena.replace('¶','')

def limpiar_parametro(parametro):
    # Hay parámetros que no vienen en detalle y vienen enteros. Del estilo start=0
    # La idea es quedarse con lo que hay antes del igual
    if "=" in parametro:
        return parametro[:parametro.find("=")]
    else:
        return parametro

def todos_los_elementos():


    page = requests.get(URLFUNCIONES)
    soup = BeautifulSoup(page.content, 'html5lib')

    
    ## Funciones
    funciones = soup.find_all("dl", {"class":"py function"})
    print ("Hay " + str(len(funciones)) + " funciones.")
    
    for funcion in funciones:
        
        sintaxis = funcion.find_all("dt",limit=1)

        for s in sintaxis:
            print (limpiar_signatura(s.text))
            nombre = s.find("code", {"class":"sig-name descname"})        
            print (nombre.text)

            # Chequeamos que tenga parámetros. Están a la misma altura que el nombre.
            parametros = nombre.find_next_siblings("em", {"class":"sig-param"})

            for parametro in parametros:
            
                nombre_parametro = parametro.find("span", {"class":"n"})            
                if nombre_parametro:
                    print(nombre_parametro.text)
                else: 
                    print(limpiar_parametro(parametro.text))

    ## Clases
    clases = soup.find_all("dl", {"class":"py class"})
    print ("Hay " + str(len(clases)) + " clases.")
    
    for clase in clases:
        
        sintaxis = clase.find_all("dt",limit=2)

        print (len(sintaxis))

        for s in sintaxis:
            print (limpiar_signatura(s.text))
            nombre = s.find("code", {"class":"sig-name descname"})        
            print (nombre.text)

            # Chequeamos que tenga parámetros. Están a la misma altura que el nombre.
            parametros = nombre.find_next_siblings("em", {"class":"sig-param"})

            for parametro in parametros:
            
                nombre_parametro = parametro.find("span", {"class":"n"})            
                if nombre_parametro:
                    print(nombre_parametro.text)
                else: 
                    print(limpiar_parametro(parametro.text))    
    



# Inicio del Programa
print ("Analizando la documentación Python")
todos_los_elementos()




