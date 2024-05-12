import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver

def extrae_comentarios_meneo (meneo, pagina_comentarios):
    ''' 
        Función para la extración de todos los comentarios de una noticia (meneo)
    '''
    comentarios = []   

    try:
        ol_comentarios = meneo.find("ol", class_="comments-list")
        lista_comentarios = ol_comentarios.find_all("li")
        url  = "https://old.meneame.net" + meneo.find("a", class_="comments")["href"].strip()
        fechas = meneo.find("div", class_="news-submitted").find_all("span", class_="ts")
        fecha_envio = fechas[0]["data-ts"].strip()
        fecha_publicacion = fechas[1]["data-ts"].strip()
    except:
        return comentarios
    
    for comentario in lista_comentarios:
        datos_comentario = {}
        datos_comentario["URL"] = url
        datos_comentario["fecha_envio"] = fecha_envio
        datos_comentario["fecha_publicacion"] = fecha_publicacion
        datos_comentario["pag_comentario"] = pagina_comentarios
        
        try:
            datos_comentario["num_comentario"] = comentario.find("a", class_="comment-order").text.strip("#")
        except:
            datos_comentario["num_comentario"] = np.nan

        try:
            datos_comentario["usuario"] = comentario.find("a", class_="username").text.strip()
        except:
            datos_comentario["usuario"] = np.nan

        try:
            datos_comentario["fecha"] = comentario.find("span", class_="comment-date")["data-ts"].strip()
        except:
            datos_comentario["fecha"] = np.nan

        try:
            datos_comentario["texto"] = comentario.find("div", class_="comment-text").text.replace("\n", " ").strip()
        except:
            datos_comentario["texto"] = np.nan

        try:
            datos_comentario["votos"] = comentario.find(title="Votos").text.strip()
        except:
            datos_comentario["votos"] = np.nan

        try:
            datos_comentario["karma"] = comentario.find(title="Karma").text.strip("K ")
        except:
            datos_comentario["karma"] = np.nan

        comentarios.append(datos_comentario)

    return comentarios