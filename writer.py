from datetime import datetime
import os, html, json

'''

URL                             tag                 modulo          json
/modulo                         modulo                              x       no hace falta ya que es tag
/modulo/funcion                 funcion                             x
/modulo/clase                   clase                               x
/modulo/clase/constructor       constructor                            
/modulo/clase/metodo            metodo
/modulo/clase/atributo          atributo
/modulo/excepcion               excepcion                           x
/modulo/constante               constante                           x

'''

__OUT__ = "/Users/victor/GitHub/w3api-portal/_posts/Python/"
__OUTJSON__ = "/Users/victor/GitHub/w3api-portal/_data/Python/"
__OUTTAGS__ = "/Users/victor/GitHub/w3api-portal/tags/Python/"

def doc_JSON(elemento,nombre_modulo):


    if not nombre_modulo == "base":
        basepath = nombre_modulo

        if not os.path.exists(__OUTJSON__ + basepath[0].upper() + "/" + basepath + "/"):        
            os.makedirs(__OUTJSON__ + basepath[0].upper() + "/" + basepath + "/")

        # Clases como AbstractDocument.AttributeContext se generan en un directorio
        f = open(__OUTJSON__ + basepath[0] + "/" + basepath + "/" + elemento.nombre + ".json","w")
    else:

        if not os.path.exists(__OUTJSON__ + elemento.nombre[0].upper() + "/"):        
            os.makedirs(__OUTJSON__ + elemento.nombre[0].upper() + "/")

        # Clases como AbstractDocument.AttributeContext se generan en un directorio
        f = open(__OUTJSON__ + elemento.nombre[0] + "/" + elemento.nombre + ".json","w")


    data_json = {}
    data_json["description"] = ""
    data_json["code"] = ""
    data_json["ldc"] = []
    s = ""
    for sintaxis in elemento.sintaxis:
        s = s + sintaxis + "\n"
    data_json["sintaxis"] = s

    if hasattr(elemento,"parametros"):
        p = []
        for parametro in elemento.parametros:
            parametro_json = {}
            parametro_json["nombre"] = parametro
            parametro_json["description"] = ""
            
            p.append(parametro_json)
        data_json["parametros"] = p

    if hasattr(elemento,"atributos"):
        a = []
        for atributo in elemento.atributos:
            atributo_json = {}
            atributo_json["nombre"] = atributo.nombre
            atributo_json["description"] = ""
            atributo_json["code"] = ""
            atributo_json["ldc"] = []
            s = ""
            for sintaxis in atributo.sintaxis:
                s = s + sintaxis + "\n"
            atributo_json["sintaxis"] = s
                    
            a.append(atributo_json)
        data_json["atributos"] = a

    if hasattr(elemento,"metodos"):
        m = []
        for metodo in elemento.metodos:
            metodo_json = {}
            metodo_json["nombre"] = metodo.nombre
            metodo_json["description"] = ""
            metodo_json["code"] = ""
            metodo_json["ldc"] = []
            s = ""
            for sintaxis in metodo.sintaxis:
                s = s + sintaxis + "\n"
            metodo_json["sintaxis"] = s

            if hasattr(metodo,"parametros"):
                p = []
                for parametro in metodo.parametros:
                    parametro_json = {}
                    parametro_json["nombre"] = parametro
                    parametro_json["description"] = ""                    
                    p.append(parametro_json)                
                metodo_json["parametros"] = p

            m.append(metodo_json)
        data_json["metodos"] = m

    if hasattr(elemento,"constructores"):
        c = []
        for constructor in elemento.constructores:
            constructor_json = {}
            constructor_json["nombre"] = constructor.nombre
            constructor_json["description"] = ""
            constructor_json["code"] = ""
            constructor_json["ldc"] = []
            s = ""
            for sintaxis in constructor.sintaxis:
                s = s + sintaxis + "\n"
            constructor_json["sintaxis"] = s

            if hasattr(constructor,"parametros"):
                p = []
                for parametro in constructor.parametros:
                    parametro_json = {}
                    parametro_json["nombre"] = parametro
                    parametro_json["description"] = ""                    
                    p.append(parametro_json)                
                constructor_json["parametros"] = p

            c.append(constructor_json)
        data_json["constructores"] = c

    f.write(json.dumps(data_json,indent=4))
    f.close()


## Genera los ficheros desde una clase
def gen_cabecera(nombre,path,clave,tags):

    c = ["---" + "\n",
                "title: " + nombre + "\n",
                "permalink: " + path + "\n",
                "date: 2021-01-01\n",
                "key: " + clave + "\n",
                "category: python" + "\n",
                "tags: " + str(tags) + "\n",
                "sidebar: " + "\n",
                "  nav: python" + "\n",
                "---" + "\n\n"]
    return c

def gen_cabecera_tag(lenguaje, tipo_elemento, nombre):

    c = ["---" + "\n",
                "title: \"" + tipo_elemento + " " + nombre + "\"\n",
                "layout: tag\n",
                "permalink: /" + lenguaje + "/tag/" + nombre.replace(".","-") + "/\n",
                "date: " + str(datetime.now()) + "\n",
                "key: " + lenguaje + "." + nombre + "\n",
                "sidebar: " + "\n",
                "  nav: python" + "\n",
                "aside: " + "\n",
                "  toc: true" + "\n",
                "pagination: " + "\n",
                "  enabled: true" + "\n",
                "  tag: \"" + nombre + "\"\n",
                "  permalink: /:num/" + "\n",
                "---" + "\n\n"]
    return c

def gen_sintaxis(base):

    s = ["## Sintaxis\n",
          "~~~python\n",
          "{{ " + base + ".sintaxis }}",
          "~~~\n\n"]
    return s

def gen_ldc(clave):
    ldc = ["## Artículos\n",
           "<ul>\n",
            "{%- for _ldc in " + clave + ".ldc -%}\n",
            "   <li>\n",
                "       <a href=\"{{_ldc['url'] }}\">{{ _ldc['nombre'] }}</a>\n",
            "   </li>\n",
            "{%- endfor -%}\n",
          "</ul>\n"]
    return ldc

def gen_ejemplo(base):

    e = ["## Ejemplo\n"
         "~~~python\n",
         "{{ " + base + ".code}}\n",
         "~~~\n\n",
         ]
    return e

def gen_descripcion(base):
    d = ["## Descripción\n",
         "{{" + base + ".description }}\n\n"
         ]
    return d

def gen_constructores(constructores,nombre):
    c = ["## Constructores\n"]
    for constructor in constructores:
        c.append("* [" + constructor.nombre + "](/Python/" + nombre + "/" + constructor.nombre + "/)\n")
    c.append("\n")
    return c

def gen_metodos(metodos,nombre):
    m = ["## Métodos\n"]
    for metodo in metodos:
        m.append("* [" + metodo.nombre + "](/Python/" + nombre + "/" + metodo.nombre + "/)\n")
    m.append("\n")
    return m

def gen_parametros(parametros):
    p = ["## Parámetros\n"]
    for parametro in parametros:
        
        # Hay parámetros que son asteriscos
        if parametro=="*":
            parametro = "\*"

        p.append("* **" + html.escape(parametro) + "**,  ")
        p.append("{% include w3api/param_description.html metodo=_dato parametro=\"" + parametro + "\" %}\n")
    p.append("\n")
    return p    

def gen_parametros_funcion(parametros,clave):
    p = ["## Parámetros\n"]
    for parametro in parametros:
        p.append("* **" + html.escape(parametro) + "**,  ")
        p.append("{% include w3api/function_param_description.html propiedad=" + clave + " valor=\"" + parametro + "\" %}\n")
    p.append("\n")
    return p    
            
def gen_atributos(atributos,nombre):
    a = ["## Atributos\n"]
    for atributo in atributos:
        a.append("* [" + atributo.nombre + "](/Python/" + nombre + "/" + atributo.nombre + "/)\n")
    a.append("\n")
    return a

def gen_clasepadre(nombre,path):
    cp = ["## Clase Padre\n",
          "[" + nombre + "](/Python/"+ path.replace(".","/") + "/)\n\n"]

    return cp

def gen_infometodo(clave,tipo,valor):
    bm = ["{% include w3api/datos.html clase=site.data." + clave + "." + tipo + " valor=\"" + valor +"\" %}\n\n"]
    return bm

def gen_elemento(elementos,nombre,path):
    e = ["## " + nombre + "\n"]
    for elemento in elementos:
        e.append("* [" + elemento.nombre + "](" + path + "/" + elemento.nombre + "/)\n")
    e.append("\n")
    return e

def doc_constante(constante,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + constante.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + constante.nombre
        jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + constante.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"        
    
    else:
        basepath = constante.nombre
        clave = "Python."+constante.nombre[0]+ "." + constante.nombre
        jsonsource = "Python." + constante.nombre[0].upper() + "." + constante.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + constante.nombre + ".md","w")


    tags = []
    tags.append("constante python")     
    tags.append(nombre_modulo)

    if not nombre_modulo == "base":
        cabecera = gen_cabecera(nombre_modulo + "." + constante.nombre,path,clave,tags)
    else:
        cabecera = gen_cabecera(constante.nombre,path,clave,tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis("site.data." + jsonsource)
    f.writelines(sintaxis)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)

    f.close()

    doc_JSON(constante,nombre_modulo)


def doc_excepcion(excepcion,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + excepcion.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + excepcion.nombre
        jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + excepcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"        
    
    else:
        basepath = excepcion.nombre
        clave = "Python."+excepcion.nombre[0]+ "." + excepcion.nombre
        jsonsource = "Python." + excepcion.nombre[0].upper() + "." + excepcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + excepcion.nombre + ".md","w")

    tags = []
    tags.append("excepcion python")     
    tags.append(nombre_modulo)

    if not nombre_modulo == "base":
        cabecera = gen_cabecera(nombre_modulo + "." + excepcion.nombre,path,clave, tags)
    else:
        cabecera = gen_cabecera(excepcion.nombre,path,clave, tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis("site.data." + jsonsource)
    f.writelines(sintaxis)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)

    f.close()

    doc_JSON(excepcion,nombre_modulo)


def doc_funcion(funcion,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + funcion.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + funcion.nombre
        jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + funcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        
    
    else:
        basepath = funcion.nombre
        clave = "Python."+funcion.nombre[0]+ "." + funcion.nombre
        jsonsource = "Python." + funcion.nombre[0].upper() + "." + funcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + funcion.nombre + ".md","w")

    
    tags = []
    tags.append("funcion python")     
    tags.append(nombre_modulo)


    if not nombre_modulo == "base":
        cabecera = gen_cabecera(nombre_modulo + "." + funcion.nombre,path,clave, tags)
    else:
        cabecera = gen_cabecera(funcion.nombre,path,clave, tags)
    f.writelines(cabecera)

    #info_elemento = gen_infometodo(jsonsource,"metodos",basepath)
    #f.writelines(info_elemento)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis("site.data." + jsonsource)
    f.writelines(sintaxis)

    if funcion.parametros:
        parametros = gen_parametros_funcion(funcion.parametros,"site.data." + clave)
        f.writelines(parametros)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)


    f.close()

    doc_JSON(funcion,nombre_modulo)


def doc_clase(clase,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + clase.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + clase.nombre
        jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + clase.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        
    
    else:
        basepath = clase.nombre
        clave = "Python."+clase.nombre[0]+ "." + clase.nombre
        jsonsource = "Python." + clase.nombre[0].upper() + "." + clase.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + ".md","w")

    
    tags = []
    tags.append("clase python")     
    tags.append(nombre_modulo)


    if not nombre_modulo == "base":
        cabecera = gen_cabecera(nombre_modulo + "." + clase.nombre,path,clave, tags)
    else:
        cabecera = gen_cabecera(clase.nombre,path,clave, tags)
    f.writelines(cabecera)

    info_elemento = gen_infometodo(jsonsource,"metodos",basepath)
    f.writelines(info_elemento)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis("site.data." + jsonsource)
    f.writelines(sintaxis)

    if clase.constructores:
        constructores = gen_constructores(clase.constructores,basepath)
        f.writelines(constructores)

    if clase.metodos:
        metodos = gen_metodos(clase.metodos,basepath)
        f.writelines(metodos)

    if clase.atributos:
        atributos = gen_atributos(clase.atributos,basepath)
        f.writelines(atributos)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)


    f.close()

    if clase.constructores:
        doc_constructor(clase,nombre_modulo)
        
    if clase.metodos:
        doc_metodo(clase,nombre_modulo)

    if clase.atributos:
        doc_atributo(clase,nombre_modulo)

    doc_JSON(clase,nombre_modulo)

def doc_atributo(clase,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + clase.nombre    
    else:
        basepath = clase.nombre

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")


    for atributo in clase.atributos:

        if not nombre_modulo == "base":            
            clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + clase.nombre + "." + atributo.nombre
            jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + clase.nombre # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + atributo.nombre + "/"  
        
        else:            
            clave = "Python."+clase.nombre[0]+ "." + clase.nombre + "." + atributo.nombre
            jsonsource = "Python." + clase.nombre[0].upper() + "." + clase.nombre # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + atributo.nombre + "/"

        f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + atributo.nombre + ".md","w")

        tags = []
        tags.append("atributo python")     
        tags.append(nombre_modulo)

        if not nombre_modulo == "base":
            cabecera = gen_cabecera(nombre_modulo + "." + clase.nombre + "." + atributo.nombre,path,clave, tags)
        else:
            cabecera = gen_cabecera(clase.nombre + "." + atributo.nombre,path,clave, tags)
        f.writelines(cabecera)

        info_metodo = gen_infometodo(jsonsource,"atributos",atributo.nombre)
        f.writelines(info_metodo)

        descripcion = gen_descripcion("_dato")
        f.writelines(descripcion)

        sintaxis = gen_sintaxis("_dato")
        f.writelines(sintaxis)

        clase_padre = gen_clasepadre(clase.nombre,basepath)
        f.writelines(clase_padre)

        ejemplo = gen_ejemplo("_dato")
        f.writelines(ejemplo)

        ldc = gen_ldc("_dato")
        f.writelines(ldc)

        f.close()

def doc_metodo(clase,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + clase.nombre 
    else:
        basepath = clase.nombre
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")


    for metodo in clase.metodos:

        if not nombre_modulo == "base":            
            clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + clase.nombre + "." + metodo.nombre
            jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + clase.nombre  # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + metodo.nombre + "/"  
        
        else:            
            clave = "Python."+clase.nombre[0]+ "." + clase.nombre + "." + metodo.nombre
            jsonsource = "Python." + clase.nombre[0].upper() + "." + clase.nombre  # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + metodo.nombre + "/"

        f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + metodo.nombre + ".md","w")

        tags = []
        tags.append("metodo python")     
        tags.append(nombre_modulo)

        if not nombre_modulo == "base":
            cabecera = gen_cabecera(nombre_modulo + "." + clase.nombre + "." + metodo.nombre,path,clave, tags)
        else:
            cabecera = gen_cabecera(clase.nombre + "." + metodo.nombre,path,clave, tags)
        f.writelines(cabecera)

        info_metodo = gen_infometodo(jsonsource,"metodos",metodo.nombre)
        f.writelines(info_metodo)

        descripcion = gen_descripcion("_dato")
        f.writelines(descripcion)

        sintaxis = gen_sintaxis("_dato")
        f.writelines(sintaxis)

        if metodo.parametros:
            parametros = gen_parametros_funcion(metodo.parametros,"site.data." + clave)
            f.writelines(parametros)

        clase_padre = gen_clasepadre(clase.nombre,basepath)
        f.writelines(clase_padre)

        ejemplo = gen_ejemplo("_dato")
        f.writelines(ejemplo)

        ldc = gen_ldc("_dato")
        f.writelines(ldc)

        f.close()

def doc_constructor(clase,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + clase.nombre 
    else:
        basepath = clase.nombre
        

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")


    for metodo in clase.constructores:

        if not nombre_modulo == "base":            
            clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + clase.nombre + "." + metodo.nombre
            jsonsource = "Python." + nombre_modulo[0].upper() + "." + nombre_modulo.replace(".","") + "." + clase.nombre  # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + metodo.nombre + "/"  
        
        else:            
            clave = "Python."+clase.nombre[0]+ "." + clase.nombre + "." + metodo.nombre
            jsonsource = "Python." + clase.nombre[0].upper() + "." + clase.nombre  # Las base JSON compuestas se accede sin punto
            path = "/Python/"+basepath + "/" + metodo.nombre + "/"

        f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + metodo.nombre + ".md","w")

        tags = []
        tags.append("constructor python")     
        tags.append(nombre_modulo)

        if not nombre_modulo == "base":
            cabecera = gen_cabecera(nombre_modulo + "." + clase.nombre + "." + metodo.nombre,path,clave, tags)
        else:
            cabecera = gen_cabecera(clase.nombre + "." + metodo.nombre,path,clave, tags)
        f.writelines(cabecera)

        info_metodo = gen_infometodo(jsonsource,"constructores",metodo.nombre)
        f.writelines(info_metodo)

        descripcion = gen_descripcion("_dato")
        f.writelines(descripcion)

        sintaxis = gen_sintaxis("_dato")
        f.writelines(sintaxis)

        if metodo.parametros:
            parametros = gen_parametros_funcion(metodo.parametros,"site.data." + clave)
            f.writelines(parametros)

        clase_padre = gen_clasepadre(clase.nombre,basepath)
        f.writelines(clase_padre)

        ejemplo = gen_ejemplo("_dato")
        f.writelines(ejemplo)

        ldc = gen_ldc("_dato")
        f.writelines(ldc)

        f.close()
    

def doc_modulo(modulo):


    if not modulo.nombre == "base":        
        path = "/Python/" + modulo.nombre.replace(".","-")  
    else:    
        path = "/Python" 

    basepath = modulo.nombre.replace(".","-")
    clave = "Python."+modulo.nombre[0]+ "." + modulo.nombre 
    jsonsource = "Python." + modulo.nombre[0].upper() + "." + modulo.nombre.replace(".","") # Las base JSON compuestas se accede sin punto
              

    if not os.path.exists(__OUT__ + basepath[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0].upper() + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + modulo.nombre + ".md","w")

    tags = []
    tags.append("modulo python")     

    cabecera = gen_cabecera(modulo.nombre,"/Python/"+basepath,clave, tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    if modulo.funciones:
        funciones = gen_elemento(modulo.funciones,"Funciones",path)
        f.writelines(funciones)
    
    if modulo.clases:
        clases = gen_elemento(modulo.clases,"Clases",path)
        f.writelines(clases)
 
    if modulo.excepciones:
        excepciones = gen_elemento(modulo.excepciones,"Excepciones",path)
        f.writelines(excepciones)
 
    if modulo.constantes:
        constantes = gen_elemento(modulo.constantes,"Constantes",path)
        f.writelines(constantes)
 
    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)


    f.close()

    #doc_JSON(clase,nombre_modulo)


def doc_listado_modulos(nombre_modulo):

    if not os.path.exists(__OUTTAGS__ + "modulos/"):
        os.makedirs(__OUTTAGS__ + "modulos/")

    f = open(__OUTTAGS__ + "modulos/"+ nombre_modulo + ".md","w")

    cabecera = gen_cabecera_tag("Python","Módulo",nombre_modulo)
    f.writelines(cabecera)

    contenido = ["<h2>Modulos</h2>\n",
                "Todos los elementos del modulo <strong>" + nombre_modulo + "</strong>\n"]
    f.writelines(contenido)

    f.close()
