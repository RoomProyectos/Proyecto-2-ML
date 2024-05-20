import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver

def extrae_datos_meneos (lista_meneos):
    ''' 
        Función para la extración de todas las noticias (meneos) de la web meneame.net
    '''
    datos = []
    
    for meneo in lista_meneos:
        dicc_aux = {}
      
        ###################################    Titular    ####################################################################
        try:
            dicc_aux["Titular"] = meneo.find("h2").text.replace("\n", " ").strip()
        except:
            dicc_aux["Titular"] = np.nan
        
        ###################################    Medio    ######################################################################
        try:
            dicc_aux["Medio"] = meneo.find("span", class_="showmytitle").text.strip()
        except:            
            dicc_aux["Medio"] = "meneame.net"

        ###################################    URL    ######################################################################
        try:
            dicc_aux["URL"] = "https://old.meneame.net" + meneo.find("a", class_="comments")["href"].strip()
        except:            
            dicc_aux["URL"] = np.nan

        ###################################    Fechas    ######################################################################    
        try:
            fechas = meneo.find("div", class_="news-submitted").find_all("span", class_="ts")
            dicc_aux["Enviado"] = fechas[0]["data-ts"].strip()
            dicc_aux["Publicado"] = fechas[1]["data-ts"].strip()
        except:
            dicc_aux["Enviado"] = np.nan
            dicc_aux["Publicado"] = np.nan

        ###################################    Meneos    ######################################################################
        try:
            dicc_aux["Meneos"] = meneo.find("div", class_="votes").find("a").text.strip()
        except:
            dicc_aux["Meneos"] = np.nan

        ###################################    Click    ######################################################################
        try:
            dicc_aux["Clicks"] = meneo.find("div", class_="clics").find("span").text.strip()
        except:        
            dicc_aux["Clicks"] = np.nan

        ###################################    Positivos    ###################################################################
        try:
            dicc_aux["Positivos"] = meneo.find("span", class_="positive-vote-number").text.strip()
        except:
            dicc_aux["Positivos"] = np.nan

        ###################################    Votos Anónimos    ##############################################################
        try:
            dicc_aux["Anonimos"] = meneo.find("span", class_="anonymous-vote-number").text.strip()
        except:
            dicc_aux["Anonimos"] = np.nan

        ###################################    Votos Negativos    ##############################################################
        try:
            dicc_aux["Negativos"] = meneo.find("span", class_="negative-vote-number").text.strip()
        except:
            dicc_aux["Negativos"] = np.nan

        ###################################    Número comentarios    ###########################################################
        try:
            dicc_aux["Comentarios"] = meneo.find("a", class_="comments")["data-comments-number"].strip()
        except:
            dicc_aux["Comentarios"] = np.nan

        ###################################    Karma    ########################################################################
        try:
            dicc_aux["Karma"] = meneo.find("span", class_="karma-number").text.strip()
        except:
            dicc_aux["Karma"] = np.nan

        datos.append(dicc_aux)       

    return datos

URL_BASE = "https://old.meneame.net/"

lista_aux = []
contador_paginas = 0
contador_errores = {"Errores" : 0, "Paginas_Error" : []}

browser = webdriver.Chrome()
browser.get(f"{URL_BASE}")

# Se obtiene el número total de páginas de noticias y se calcula la página de inicio para el año elegido
total_paginas = int(BeautifulSoup(browser.page_source, "html.parser").find("div", class_="pages").find_all("a")[-2].text)
pagina = 1

try:
    while pagina <= total_paginas:          
        try:
            # Se solicita al navegador la apertura de la URL de la página
            if pagina >= 2: 
                browser.get(f"{URL_BASE}?page={pagina}")

            # Se obtiene el BeautifulSoup a partir del código fuente de la página
            Soup_pagina_meneos = BeautifulSoup(browser.page_source, "html.parser")

            # Se extrae el listado de noticias
            lista_meneos = Soup_pagina_meneos.find_all("div", class_="news-summary")

            # Se analiza el listado con la función de extracción
            resultado = extrae_datos_meneos(lista_meneos)
            
            # Se añaden los resultados de la extracción a una lista
            lista_aux.extend(resultado)

            # Se aumenta el contador de páginas
            pagina += 1
            contador_paginas += 1
            
            print(f" Escaneando página {contador_paginas}  ", end="\r")
        except:            
            contador_errores["Errores"] += 1
            contador_errores["Paginas_Error"].append(pagina)
except:
    print("Ocurrido un error inesperado... ¿Estaba cargada la función?")

print("\n")
print("-"*34)
print(f" Total paginas procesadas: {contador_paginas}")
print(f" Total noticias importadas: {len(lista_aux)}")
print(f" Total de errores: {contador_errores['Errores']}")
print("-"*34)

browser.close()

df = pd.DataFrame(lista_aux)
df.to_csv('../Data/MeneosCompleto.csv', sep=';', encoding='utf-8', index=False)