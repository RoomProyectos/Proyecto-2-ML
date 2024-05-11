import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver

def extrae_comentarios_meneo (meneo):
    ''' 
        Función para la extración de todos los comentarios de una noticia (meneo)
    '''
    comentarios = []
    continuar = False

    ol_comentarios = meneo.find("ol", class_="comments-list")
    lista_comentarios = ol_comentarios.find_all("li")

    try:
        continuar = meneo.find("div", class_="pages_")["data-total-pages"]        
    except:
        continuar = False

    for comentario in lista_comentarios:
        datos_comentario = {}
        try:
            datos_comentario["num_comentario"] = comentario.find("a", class_="comment-order").text.strip("#")
        except:
            np.nan()
        try:
            datos_comentario["usuario"] = comentario.find("a", class_="username").text.strip()
        except:
            np.nan()
        try:
            datos_comentario["fecha"] = comentario.find("span", class_="comment-date")["data-ts"].strip()
        except:
            np.nan()
        try:
            datos_comentario["texto"] = comentario.find("div", class_="comment-text").text.strip()
        except:
            np.nan()
        try:
            datos_comentario["votos"] = comentario.find(title="Votos").text.strip()
        except:
            np.nan()
        try:
            datos_comentario["karma"] = comentario.find("span", class_="votes-counter").text.strip("K ")
        except:
            np.nan()

        comentarios.append(datos_comentario)

    return [comentarios, continuar]