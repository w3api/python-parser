class Modulo:

    nombre = ""
    funciones = []
    clases = []
    constantes = []
    excepciones = []

    def __init__(self):
        self.nombre = ""
        self.funciones = []
        self.clases = []
        self.constantes = []
        self.excepciones = []

    def nombre(self,nombre):
        self.nombre = nombre

    def add_funcion(self,funcion):
        self.funciones.append(funcion)

    def add_clase(self,clase):
        self.clases.append(clase)

    def add_constante(self,constante):
        self.constantes.append(constante)

    def add_execpcion(self,excepcion):
        self.excepciones.append(excepcion)

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Funciones: ")
        for funcion in self.funciones:
            print(">> " + str(funcion))
        print("Clases: ")
        for clase in self.clases:
            print(">> " + str(clase))
        print("Constantes: ")
        for constante in self.constantes:
            print(">> " + str(constante))
        print("Excecpiones: ")
        for excepcion in self.excepcpiones:
            print(">> " + str(excepcion))

class Funcion:

    nombre = ""
    sintaxis = []
    parametros = []

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []
        self.parametros = []

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def add_parametro(self,parametro):
        self.parametros.append(parametro)

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Sintaxis: ")
        for s in self.sintraxis:
            print(">> " + s)
        print("Parametros: ")
        for parametro in self.parametros:
            print(">> " + parametro)

class Clase:

    nombre = ""
    metodos = []
    atributos = []

    def __init__(self):
        self.nombre = ""
        self.metodos = []
        self.atributos = []        

    def nombre(self,nombre):
        self.nombre = nombre

    def add_metodo(self,metodo):
        self.metodos.append(metodo)

    def add_atributos(self,atributo):
        self.atributos.append(atributo)

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Metodos: ")
        for metodo in self.metodos:
            print(">> " + str(metodo))
        print("Atributos: ")
        for atributo in self.atributos:
            print(">> " + str(atributo))


class Metodo:

    nombre = ""
    sintaxis = []
    parametros = []

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []
        self.parametros = []

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def add_parametro(self,parametro):
        self.parametros.append(parametro)

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Sintaxis: ")
        for s in self.sintraxis:
            print(">> " + s)
        print("Parametros: ")
        for parametro in self.parametros:
            print(">> " + parametro)

class Atributo:

    nombre = ""
    sintaxis = ""
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = ""

    def nombre(self,nombre):
        self.nombre = nombre
    
    def sintaxis(self,sintaxis):
        self.sintaxis = sintaxis

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Sintaxis: " + self.sintaxis)

class Constante:

    nombre = ""
    sintaxis = ""
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = ""

    def nombre(self,nombre):
        self.nombre = nombre
    
    def sintaxis(self,sintaxis):
        self.sintaxis = sintaxis

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Sintaxis: " + self.sintaxis)

class Excepciones:

    nombre = ""
    sintaxis = ""
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = ""

    def nombre(self,nombre):
        self.nombre = nombre
    
    def sintaxis(self,sintaxis):
        self.sintaxis = sintaxis

    def toString(self):
        print("Nombre: " + self.nombre)
        print("Sintaxis: " + self.sintaxis)
