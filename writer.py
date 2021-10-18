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

def doc_JSON(elemento,nombre_modulo):


    if not nombre_modulo == "base":
        basepath = nombre_modulo

        if not os.path.exists(__OUTJSON__ + basepath[0] + "/" + basepath + "/"):        
            os.makedirs(__OUTJSON__ + basepath[0] + "/" + basepath + "/")

        # Clases como AbstractDocument.AttributeContext se generan en un directorio
        f = open(__OUTJSON__ + basepath[0] + "/" + basepath + "/" + elemento.nombre + ".json","w")
    else:

        if not os.path.exists(__OUTJSON__ + elemento.nombre[0] + "/"):        
            os.makedirs(__OUTJSON__ + elemento.nombre[0] + "/")

        # Clases como AbstractDocument.AttributeContext se generan en un directorio
        f = open(__OUTJSON__ + elemento.nombre[0] + "/" + elemento.nombre + ".json","w")


    data_json = {}
    data_json["description"] = ""
    data_json["code"] = ""
    data_json["ldc"] = []

    if hasattr(elemento,"parametros"):
        p = []
        for parametro in elemento.parametros:
            parametro_json = {}
            parametro_json["nombre"] = parametro
            parametro_json["description"] = ""
            
            p.append(parametro_json)
        data_json["parametros"] = p


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

def gen_cabecera_tag(tipo, nombre, titulo):

    c = ["---" + "\n",
                "title: \"" + titulo + " " + nombre + "\"\n",
                "layout: tag\n",
                "permalink: /html/tag/" + nombre + "/\n",
                "date: " + str(datetime.now()) + "\n",
                "key: " + tipo + nombre + "\n",
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

def gen_sintaxis(sintaxis):

    s = ["## Sintaxis\n",
          "~~~python\n"]
    for sin in sintaxis:
         s.append(sin + "\n")
    s.append("~~~\n\n")
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
        c.append("* [" + constructor + "](/Python/" + nombre + "/" + constructor + "/)\n")
    c.append("\n")
    return m

def gen_metodos(metodos,nombre):
    m = ["## Métodos\n"]
    for metodo in metodos:
        m.append("* [" + metodo + "](/Python/" + nombre + "/" + metodo + "/)\n")
    m.append("\n")
    return m

def gen_parametros(parametros):
    p = ["## Parámetros\n"]
    for parametro in parametros:
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
        a.append("* [" + atributo + "](/Python/" + nombre + "/" + atributo + "/)\n")
    a.append("\n")
    return a


def gen_clasepadre(nombre,path):
    cp = ["## Elemento Padre\n",
          "[" + nombre + "](/Python/"+ path.replace(".","/") + "/)\n\n"]

    return cp

def gen_infometodo(clave,tipo,valor):
    bm = ["{% include w3api/datos.html clase=site.data." + clave + "." + tipo + " valor=\"" + valor +"\" %}\n\n"]
    return bm


def doc_constante(constante,nombre_modulo):

    # Recibe el objeto
    # Nombre del módulo
    # El path del fichero "clase" o "modulo/clase" o "modulo/clase/metodo"
    # El tipo que quiere plasmar "modulo","clase","funcion","método","constante","atributo"

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + constante.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + constante.nombre
        jsonsource = "Python." + nombre_modulo[0] + "." + nombre_modulo.replace(".","") + "." + constante.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"        
    
    else:
        basepath = constante.nombre
        clave = "Python."+constante.nombre[0]+ "." + constante.nombre
        jsonsource = "Python." + constante.nombre[0] + "." + constante.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0] + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0] + "/" + basepath + "/")

    f = open(__OUT__ + basepath[0] + "/" + basepath + "/2021-01-01-" + constante.nombre + ".md","w")


    tags = []
    tags.append("constante python")     
    tags.append(nombre_modulo)

    if not nombre_modulo == "base":
        cabecera = gen_cabecera(nombre_modulo + "." + constante.nombre,path,clave, tags)
    else:
        cabecera = gen_cabecera(constante.nombre,path,clave, tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + jsonsource)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis(constante.sintaxis)
    f.writelines(sintaxis)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)

    f.close()

    doc_JSON(constante,nombre_modulo)


def doc_excepcion(excepcion,nombre_modulo):

    # Recibe el objeto
    # Nombre del módulo
    # El path del fichero "clase" o "modulo/clase" o "modulo/clase/metodo"
    # El tipo que quiere plasmar "modulo","clase","funcion","método","constante","atributo"

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + excepcion.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + excepcion.nombre
        jsonsource = "Python." + nombre_modulo[0] + "." + nombre_modulo.replace(".","") + "." + excepcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"        
    
    else:
        basepath = excepcion.nombre
        clave = "Python."+excepcion.nombre[0]+ "." + excepcion.nombre
        jsonsource = "Python." + excepcion.nombre[0] + "." + excepcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0] + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0] + "/" + basepath + "/")

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

    sintaxis = gen_sintaxis(excepcion.sintaxis)
    f.writelines(sintaxis)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)

    f.close()

    doc_JSON(excepcion,nombre_modulo)


def doc_funcion(funcion,nombre_modulo):

    # Recibe el objeto
    # Nombre del módulo
    # El path del fichero "clase" o "modulo/clase" o "modulo/clase/metodo"
    # El tipo que quiere plasmar "modulo","clase","funcion","método","constante","atributo"

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + funcion.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + funcion.nombre
        jsonsource = "Python." + nombre_modulo[0] + "." + nombre_modulo.replace(".","") + "." + funcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        
    
    else:
        basepath = funcion.nombre
        clave = "Python."+funcion.nombre[0]+ "." + funcion.nombre
        jsonsource = "Python." + funcion.nombre[0] + "." + funcion.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0] + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0] + "/" + basepath + "/")

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

    sintaxis = gen_sintaxis(funcion.sintaxis)
    f.writelines(sintaxis)

    if funcion.parametros:
        parametros = gen_parametros_funcion(funcion.parametros,"site.data." + clave)
        f.writelines(parametros)

    ejemplo = gen_ejemplo("site.data." + jsonsource)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + jsonsource)
    f.writelines(ldc)


    f.close()

#    if e.atributos:
#        doc_atributosHTML(e)

#    if e.eventos:
#        doc_eventosHTML(e)

    doc_JSON(funcion,nombre_modulo)


def doc_clase(clase,nombre_modulo):

    if not nombre_modulo == "base":
        basepath = nombre_modulo.replace(".","-") + "/" + clase.nombre
        clave = "Python."+nombre_modulo[0]+ "." + nombre_modulo + "." + clase.nombre
        jsonsource = "Python." + nombre_modulo[0] + "." + nombre_modulo.replace(".","") + "." + clase.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        
    
    else:
        basepath = clase.nombre
        clave = "Python."+clase.nombre[0]+ "." + clase.nombre
        jsonsource = "Python." + clase.nombre[0] + "." + clase.nombre # Las base JSON compuestas se accede sin punto
        path = "/Python/"+basepath + "/"
        

    if not os.path.exists(__OUT__ + basepath[0] + "/" + basepath + "/"):
        os.makedirs(__OUT__ + basepath[0] + "/" + basepath + "/")

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

    sintaxis = gen_sintaxis(clase.sintaxis)
    f.writelines(sintaxis)

    if clase.constructores:
        constructores = gen_constructores(clase.cosntructores,basepath)
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

#    if e.atributos:
#        doc_atributosHTML(e)

#    if e.eventos:
#        doc_eventosHTML(e)

    doc_JSON(clase,nombre_modulo)