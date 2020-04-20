from selenium import webdriver
from time import sleep
import urllib
import sys
import threading
from tqdm import tqdm
from descargarFichero import descargarFicheroconBarra
from interactuadorXpath import *
import os
import traceback

threads = []

carpetaDescargas = 'Animes descargados/'


class AnimeDownloader():
    def __init__(self):
        opcion_muteo = webdriver.ChromeOptions()
        opcion_muteo.add_argument("--mute-audio")
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=opcion_muteo)
        
    #tabs_vivas, cuantas tabs quieres dejar vivas desde el inicio
    def close_all_tabs(self, tabs_vivas):
            while (len(self.driver.window_handles) > tabs_vivas):
                self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
                self.driver.close()
                self.driver.switch_to.window(window_name=self.driver.window_handles[0])

    def change_tab(self, n_tab):
        if(len(self.driver.window_handles) > n_tab):
            self.driver.switch_to.window(window_name=self.driver.window_handles[n_tab])

    def abrirnuevaTab(self):
        self.driver.execute_script("window.open('', 'new window')")
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])

    def limpiarPantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    #numero hebra es la posicion dondre saldra la barra de descarga, que corresponde con la hebra
    def descargar_capitulo(self, link_capitulo, numero_hebra, ruta = ''):
        
        video_url, nombrecapitulo = reproducirvideo(self, link_capitulo)

        #Para que salgan bien las barras al meter un nuevo episodio
        self.limpiarPantalla()

        print(nombrecapitulo)

        #creamos la hebra para que ponga a descargar y pueda seguir con el resto
        hebra = threading.Thread(target=descargarFicheroconBarra, args=(video_url, ruta, nombrecapitulo+'.mp4', numero_hebra))
        #Definimos la hebra como Daemon para que muera junto con la main
        hebra.setDaemon(True)
        hebra.start() 
        threads.append(hebra)

    #pausa antes de elegir el reproductor
    #numero hebra es la posicion dondre saldra la barra de descarga, que corresponde con la hebra
    def descargar_capitulo_con_eleccion(self, link_capitulo, numero_hebra, ruta = ''):
        
        video_url, nombrecapitulo = reproducirvideo_elegible(self, link_capitulo)

        print(nombrecapitulo)

        #creamos la hebra para que ponga a descargar y pueda seguir con el resto
        hebra = threading.Thread(target=descargarFicheroconBarra, args=(video_url, ruta+nombrecapitulo+'.mp4', numero_hebra))
        hebra.start()
        #anadimos la hebra a la lista para poder controlarla desde fuera
        threads.append(hebra)

    def descargar_serie(self, link_serie):
        existsCarpeta(carpetaDescargas)

        self.driver.get(link_serie)
        #espera para la carga
        sleep(7)
        #cerramos el popup de inicio
        self.close_all_tabs(1)
        sleep(0.5)
        #Guardamos el nombre de la serie
        
        titulo_serie = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/h2').text
        nombre_carpeta_serie = carpetaDescargas+titulo_serie+'/'
        existsCarpeta(nombre_carpeta_serie)
        #Guardamos todos los elementos de capitulo
        elemento_lista_capitulos = self.driver.find_element_by_xpath('//*[@id="episodeList"]')
        elementos_capitulo = elemento_lista_capitulos.find_elements_by_xpath('li/a')

        lista_capitulos = list()
        for ecapitulo in elementos_capitulo:
            link_capitulo = ecapitulo.get_property('href')
            lista_capitulos.append(link_capitulo)

        for capitulo in lista_capitulos:
            print("Descargando: " + capitulo)
            
            self.descargar_capitulo(capitulo, lista_capitulos.index(capitulo), nombre_carpeta_serie)
            #self.descargar_capitulo_con_eleccion(capitulo, lista_capitulos.index(capitulo)+1, nombre_carpeta_serie)

def existsCarpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)


if( len(sys.argv) >= 2 and sys.argv[1] == "-d" ):
    print("Modo dinamico")
    bot = AnimeDownloader()
else:

    link_serie = None
    if( len(sys.argv) == 1 ):
        print("Introduce el link de la serie a descargar: ")
        link_serie = raw_input()
    else:
        link_serie = sys.argv[1]

    ad = AnimeDownloader()

    existsCarpeta(carpetaDescargas)

    try:
        ad.descargar_serie(link_serie)

        ad.driver.quit()
    except Exception as e:
        with open(carpetaDescargas + 'BUG_LOG.txt', 'a+') as f:
            f.write("ERROR EN LA SERIE: " + link_serie )
            f.write(str(e))
            f.write(traceback.format_exc())

    for thread in threads:
        thread.join()
    
    

