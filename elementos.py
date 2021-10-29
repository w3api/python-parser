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

    def __str__(self):

        cadena =  "Nombre: " + self.nombre + "\n"
        cadena +=  "Funciones: \n"
        for funcion in self.funciones:
            cadena += "\t" + str(funcion) + "\n"
        cadena += "Clases: \n"
        for clase in self.clases:
            cadena += "\t" + str(clase) + "\n"
        cadena += "Constantes: \n"
        for constante in self.constantes:
            cadena += "\t" + str(constante) + "\n"
        cadena += "Excecpiones: \n"
        for excepcion in self.excepciones:
            cadena += "\t" + str(excepcion) + "\n"
        return cadena

class Funcion:

    nombre = ""
    sintaxis = []
    parametros = set()

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []
        self.parametros = set()

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def add_parametro(self,parametro):
        self.parametros.add(parametro)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: \n"
        for s in self.sintaxis:
            cadena += "\t" + s + "\n"
        cadena += "Parametros: \n"
        for parametro in self.parametros:
            cadena += "\t" + parametro + "\n"
        return cadena

class Clase:

    nombre = ""
    constructores = []
    metodos = []
    atributos = []

    def __init__(self):
        self.nombre = ""
        self.constructores = []
        self.metodos = []
        self.atributos = []        

    def nombre(self,nombre):
        self.nombre = nombre

    def add_constructor(self,constructor):
        if (len(self.constructores) == 0):
            self.constructores.append(constructor)
        else:
            for sintaxis in constructor.sintaxis:
                self.constructores[0].add_sintaxis(sintaxis)
            for parametro in constructor.parametros:
                self.constructores[0].add_parametro(parametro)
            

    def add_metodo(self,metodo):
        self.metodos.append(metodo)

    def add_atributo(self,atributo):
        self.atributos.append(atributo)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Constructores: \n"
        for constructor in self.constructores:
            cadena += "\t " + str(constructor) + "\n"
        cadena += "Metodos: \n"
        for metodo in self.metodos:
            cadena += "\t " + str(metodo) + "\n"
        cadena += "Atributos: \n"
        for atributo in self.atributos:
            cadena += "\t" + str(atributo) + "\n"
        return cadena

class Metodo:

    nombre = ""
    sintaxis = set()
    parametros = set()

    def __init__(self):
        self.nombre = ""
        self.sintaxis = set()
        self.parametros = set()

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.add(sintaxis)

    def add_parametro(self,parametro):
        self.parametros.add(parametro)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: \n"
        for s in self.sintaxis:
            cadena += "\t" + s + "\n"
        cadena += "Parametros: \n"
        for parametro in self.parametros:
            cadena += "\t" + parametro + "\n"
        return cadena


class Constructor:

    nombre = ""
    sintaxis = set()
    parametros = set()

    def __init__(self):
        self.nombre = ""
        self.sintaxis = set()
        self.parametros = set()

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.add(sintaxis)

    def add_parametro(self,parametro):
        self.parametros.add(parametro)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: \n"
        for s in self.sintaxis:
            cadena += "\t" + s + "\n"
        cadena += "Parametros: \n"
        for parametro in self.parametros:
            cadena += "\t" + parametro + "\n"
        return cadena



class Atributo:

    nombre = ""
    sintaxis = []
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def __str__(self):        
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: " + self.sintaxis + "\n"
        return cadena

class Constante:

    nombre = ""
    sintaxis = ""
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: " + self.sintaxis + "\n"
        return cadena
    
class Excepcion:

    nombre = ""
    sintaxis = ""
    
    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre
    
    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def __str__(self):
        cadena = "Nombre: " + self.nombre + "\n"
        cadena += "Sintaxis: " + self.sintaxis + "\n"
        return cadena