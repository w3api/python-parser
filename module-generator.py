# Genera las páginas de los módulos

import requests
from bs4 import BeautifulSoup
import writer

# Inicio del Programa
print ("Generando documentación de lo módulos Python")
documentacion = []

URLMODULOS = "https://docs.python.org/es/3/py-modindex.html"

# Recorremos la página de los módulos y generamos las
page = requests.get(URLMODULOS)
soup = BeautifulSoup(page.content, 'html5lib')

tabla = soup.find("table", {"class":"indextable modindextable"})
modulos = tabla.find_all("a")

for modulo in modulos:
    print ("Generando el módulo " + modulo.text)
    writer.doc_listado_modulos(modulo.text)



