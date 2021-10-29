import requests, os
from bs4 import BeautifulSoup
from elementos import Modulo,Clase,Funcion,Excepcion,Atributo,Metodo,Constante,Constructor
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


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    else:
        return obj.__dict__
    raise TypeError

def obtener_constantes(cadena):

    cadena1 = cadena[:cadena.index("...")-1]
    inicio_cadena1 = cadena1[:cadena1.index("_")+1]
    numero_cadena1 = int(cadena1[cadena1.index("_")+1:])

    cadena2 = cadena[cadena.index("...")+4:]
    inicio_cadena2 = cadena2[:cadena2.index("_")+1]
    numero_cadena2 = int(cadena2[cadena2.index("_")+1:])

    lista = []

    for x in range(numero_cadena1,numero_cadena2+1):
        lista.append(inicio_cadena1 + str(x))

    return lista


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
        dAtributo.add_sintaxis (limpiar(sintaxis.text))
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

def existe_metodo(dClase,dMetodo):

    encontrado = False
    x=0

    while ((not encontrado) and (x<len(dClase.metodos))):
        
        if (dClase.metodos[x].nombre == dMetodo.nombre):
            # Hemos encontrado el método
            
            '''
            y=0
            encontradoSintaxis = False            

            while ((not encontradoSintaxis) and (y<len(dClase.metodos[x].sintaxis))):           

                for sintaxis in dMetodo.sintaxis:
                    if (dClase.metodos[x].sintaxis[y] == sintaxis):
                        encontradoSintaxis = True
                        encontrado = True                    
                else:
                    y = y+1
            
            if (not encontrado):
                x = x+1
            '''
            encontrado = True
        else:
            x = x+1

    if encontrado:
        return x
    else:
        return -1   

def analiza_modulo(dModulo,URL):

    page = requests.get(URL)
    base = BeautifulSoup(page.content, 'html5lib')

    # Buscamos el id del DIV o SPAN con el contenido
    if "#" in URL:
        nombre_capa = URL[URL.index("#")+1:]  

        soup = base.find("div",{"id":nombre_capa})
        if not soup:
            soup = base.find("span",{"id":nombre_capa})
    else:
        soup = base
    
    ## Funciones
    print ("----------FUNCIONES----------")
    funciones = soup.find_all("dl", {"class":"py function"})    
    
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

            dFuncion.add_sintaxis(limpiar(s.text))
            for parametro in parametros:
                dFuncion.add_parametro(parametro)

        dModulo.add_funcion(dFuncion)            

    ## Clases
    print ("----------CLASES----------")
    clases = soup.find_all("dl", {"class":"py class"})    
    
    for clase in clases:        
        
        # Buscamos la primera sintaxis    
        sintaxis = clase.find("dt")
        nombre = sintaxis.find("code", {"class":"sig-name descname"})                
        parametros = obtener_parametros(nombre)
        metodos = obtener_metodos(clase)

        dClase = Clase()
        dClase.nombre =  nombre.text
        
        dConstructor = Constructor()
        dConstructor.nombre = nombre.text
        dConstructor.add_sintaxis(limpiar(sintaxis.text))
        for parametro in parametros:
            dConstructor.add_parametro(parametro)

        for metodo in metodos:
            posicion = existe_metodo(dClase,metodo)
            if (posicion<0):   
                # no existe el método
                dClase.add_metodo(metodo)
            else:
                # existe, metemos sintaxis y parámetros
                for sintaxis in metodo.sintaxis:
                    dClase.metodos[posicion].add_sintaxis(sintaxis)
                for parametro in metodos.parametros:
                    dClase.metodos[posicion].add_parametro(parametro)

        

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
                posicion = existe_metodo(dClase,metodo)
                if (posicion<0):   
                    # no existe el método
                    dClase.add_metodo(metodo)
                else:
                    # existe, metemos sintaxis y parámetros
                    for sintaxis in metodo.sintaxis:
                        dClase.metodos[posicion].add_sintaxis(sintaxis)
                    for parametro in metodo.parametros:
                        dClase.metodos[posicion].add_parametro(parametro)

        
        dClase.add_constructor(dConstructor)

        atributos = obtener_atributos(clase)
        for atributo in atributos:
            dClase.add_atributo(atributo)

        # Hay que ver si actualizamos sobre una clase que existe o sobre una nueva
        posicion = existe_clase(dModulo,dClase.nombre)
        if (posicion >= 0):            
            # Copiamos toda la dClase a la existente
            for constructor in dClase.constructores:                
                dModulo.clases[posicion].add_constructor(constructor)
            for metodo in dClase.metodos:

                posicion_metodo = existe_metodo(dModulo.clases[posicion],metodo)
                if (posicion_metodo<0):   
                    # no existe el método
                    dModulo.clases[posicion].add_metodo(metodo)
                else:
                    # existe, metemos sintaxis y parámetros
                    for sintaxis in metodo.sintaxis:
                        dModulo.clases[posicion].metodos[posicion_metodo].add_sintaxis(sintaxis)
                    for parametro in metodo.parametros:
                        dModulo.clases[posicion].metodos[posicion_metodo].add_parametro(parametro)

                    


            for atributo in dClase.atributos:
                dModulo.clases[posicion].add_atributo(atributo)               
        else:        
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
                dMetodo.add_sintaxis(limpiar(s.text))
                for parametro in parametros:
                    dMetodo.add_parametro(parametro)                

                # Hay que ver si actualizamos sobre una clase que existe o sobre una nueva
                posicion = existe_clase(dModulo,clase.text[:-1])
     
                if (posicion >= 0):    
                    # Existe la Clase            

                    posicion_metodo = existe_metodo(dModulo.clases[posicion],dMetodo)
                    if (posicion_metodo<0):   
                        # no existe el método                        
                        dModulo.clases[posicion].add_metodo(dMetodo)
                    else:
                        # existe, metemos sintaxis y parámetros                    
                        for sintaxis in dMetodo.sintaxis:
                            dModulo.clases[posicion].metodos[posicion_metodo].add_sintaxis(sintaxis)
                        for parametro in dMetodo.parametros:
                            dModulo.clases[posicion].metodos[posicion_metodo].add_parametro(parametro)

                else:
                    # No Existe la Clase

                    dClase = Clase()
                    dClase.nombre = clase.text[:-1]
                    dClase.add_metodo(dMetodo)
                    dModulo.add_clase(dClase)                

               

    # Hay atributos que no están debajo de la clase
    # Hay que mirar su clase base, sino ignorarlos ya que están en clase y ya se han añadido
    print ("----------ATRIBUTOS----------")
    atributos = soup.find_all("dl", {"class":"py attribute"})
    for atributo in atributos:
        sintaxis = atributo.find("dt")
        clase = sintaxis.find("code",{"class":"sig-prename descclassname"})
        if clase:
            nombre = sintaxis.find("code", {"class":"sig-name descname"})                    

            dAtributo = Atributo()
            dAtributo.nombre = nombre.text
            dAtributo.add_sintaxis(limpiar(sintaxis.text))

            posicion = existe_clase(dModulo,clase.text[:-1])
            if (posicion >= 0):

                dModulo.clases[posicion].add_atributo(dAtributo)
            else:
                dClase = Clase()
                dClase.nombre = clase.text[:-1]
                dClase.add_atributo(dAtributo)
                dModulo.add_clase(dClase)
 

    # Constantes
    print ("----------CONSTANTES----------")
    constantes = soup.find_all("dl", {"class":"py data"})
    for constante in constantes:
        sintaxis = constante.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})

        if "..." in nombre.text:
            constantes = obtener_constantes(nombre.text)
            for constante in constantes:
                dConstante = Constante()
                dConstante.nombre = constante
                dConstante.add_sintaxis(limpiar(sintaxis.text))
                dModulo.add_constante(dConstante)
        else:
            dConstante = Constante()
            dConstante.nombre = nombre.text.replace("*","")
            dConstante.add_sintaxis(limpiar(sintaxis.text))
            
            dModulo.add_constante(dConstante)

    # Excepciones
    print ("----------EXCEPCIONES---------")
    excepciones = soup.find_all("dl", {"class":"py exception"})
    for excepcion in excepciones:
        sintaxis = excepcion.find("dt")        
        nombre = sintaxis.find("code", {"class":"sig-name descname"})  

        dExcepcion = Excepcion()
        dExcepcion.nombre = nombre.text
        dExcepcion.add_sintaxis(limpiar(sintaxis.text))
        
        dModulo.add_execpcion(dExcepcion)

    return dModulo

def analizar_modulo(URL):
    # Analiza y genera el JSON de un solo módulo
    dModulo = Modulo()
    dModulo = analiza_modulo(dModulo,URL)
    f = open("data-one.json","w")
    f.write(json.dumps(dModulo,default=set_default,indent=4))
    f.close()

# Inicio del Programa
print ("Analizando la documentación Python")
documentacion = []

URLFUNCIONES = "https://docs.python.org/es/3/library/functions.html"
URLTIPOS = "https://docs.python.org/es/3/library/stdtypes.html"
URLEXCEPCIONES = "https://docs.python.org/es/3/library/exceptions.html"
URLMODULOS = "https://docs.python.org/es/3/py-modindex.html"
URLMODULOSBASE = "https://docs.python.org/es/3/"


# 1. Funciones Base
print ("Analizando el módulo Base")
dModulo = Modulo()
dModulo.nombre = "base"
dModulo = analiza_modulo(dModulo,URLFUNCIONES)


# 2. Tipos Base
# Reutilizamos el mismo módulo que la base
print ("Analizando el módulo Tipos Base")
dModulo = analiza_modulo(dModulo,URLTIPOS)

# 3. Excepciones Base
# Reutilizamos el mismo módulo que la base
print ("Analizando el módulo Excepciones")
dModulo = analiza_modulo(dModulo,URLEXCEPCIONES)

documentacion.append(dModulo)


# 4. Módulos
page = requests.get(URLMODULOS)
soup = BeautifulSoup(page.content, 'html5lib')

tabla = soup.find("table", {"class":"indextable modindextable"})
modulos = tabla.find_all("a")

for modulo in modulos:
    print ("Analizando el módulo " + modulo.text)
    dModulo = Modulo()
    dModulo.nombre = modulo.text    
    dModulo = analiza_modulo(dModulo,URLMODULOSBASE + modulo.get("href"))    
    documentacion.append(dModulo)

''' -- PRUEBA UN MODULO
dModulo = Modulo()
dModulo.nombre = "socket"
print ("Analizando el módulo Excepciones")
dModulo = analiza_modulo(dModulo,"https://docs.python.org/es/3/library/socket.html")
documentacion.append(dModulo)
'''

# Generamos el JSON
f = open("data.json","w")
f.write(json.dumps(documentacion,default=set_default,indent=4))
f.close()

# Cargamos el JSON para ir más rápdio
#with open('data.json') as f:
#    documentacion = json.load(f)


for modulo in documentacion:

    writer.doc_modulo(modulo)

    for funcion in modulo.funciones:
        writer.doc_funcion(funcion,modulo.nombre)
    for clase in modulo.clases:
        writer.doc_clase(clase,modulo.nombre)
    for excecpion in modulo.excepciones:
        writer.doc_excepcion(excecpion,modulo.nombre) 
    for constante in modulo.constantes:
        writer.doc_constante(constante,modulo.nombre) 


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





