from selenium import webdriver
from time import sleep
import urllib
import sys
import threading
from tqdm import tqdm
from descargarFichero import descargarFicheroconBarra
import os

threads = []

class AnimeDownloader():
    def __init__(self):
        opcion_muteo = webdriver.ChromeOptions()
        opcion_muteo.add_argument("--mute-audio")
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver.exe', chrome_options=opcion_muteo)
        
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

    def seleccionar_opcion(self, link_capitulo, n_opcion):
        #vamos a la web
        self.driver.get(link_capitulo)
        #espera para la carga
        sleep(7)
        #cerramos el popup de inicio
        self.close_all_tabs(1)
        sleep(0.5)
        #clickamos la segunda opcion
        opc_2 = self.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/ul/li[2]/a')
        opc_2.click()

    def getVideo_Fembed(self):
        #cambiamos el contexto, al reproductor de video (es una web incrustada)
        iframe_video = self.driver.find_element_by_xpath('//*[@id="video_box"]/iframe')
        self.driver.switch_to_frame(iframe_video)
        #le damos al play
        botonPlay = self.driver.find_element_by_xpath('/html/body/div[2]/div')
        botonPlay.click()

        sleep(0.5)
        self.close_all_tabs(1)

        #Espera para la carga del video
        sleep(20)

        iframe_video2 = self.driver.find_element_by_xpath('//*[@id="video_box"]/iframe')
        self.driver.switch_to_frame(iframe_video2)
        capitulo = self.driver.find_element_by_xpath('//*[@id="vstr"]/div[2]/div[3]/video')

        return capitulo

    #Devuelve la url y el nombre
    def reproducirvideo(self, link_capitulo):
        self.seleccionar_opcion(link_capitulo, 0)

        #Guardamos el nombre del capitulo
        nombre_capitulo = self.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/div[1]/h1').text

        #Espera carga reproductor
        sleep(7)

        capitulo = self.getVideo_Fembed()

        #Guarreria para que cierre la puta tab 
        #self.abrirnuevaTab()
        #tabs = self.driver.window_handles
        #self.driver.switch_to.window(tabs[0])
        #self.driver.close()
        #tabs = self.driver.window_handles
        #self.driver.switch_to.window(tabs[0])

        return capitulo.get_property('src'), nombre_capitulo

    #Devuelve la url y el nombre
    def reproducirvideo_elegible(self, link_capitulo):
        self.seleccionar_opcion(link_capitulo, 0)

        #Guardamos el nombre del capitulo
        nombre_capitulo = self.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/div[1]/h1').text

        #Espera carga reproductor
        raw_input("Elige Fembed y presiona una tecla")

        capitulo = self.getVideo_Fembed()

        #Guarreria para que cierre la puta tab 
        #self.abrirnuevaTab()
        #tabs = self.driver.window_handles
        #self.driver.switch_to.window(tabs[0])
        #self.driver.close()
        #tabs = self.driver.window_handles
        #self.driver.switch_to.window(tabs[0])

        return capitulo.get_property('src'), nombre_capitulo

    #numero hebra es la posicion dondre saldra la barra de descarga, que corresponde con la hebra
    def descargar_capitulo(self, link_capitulo, numero_hebra, ruta = ''):
        
        video_url, nombrecapitulo = self.reproducirvideo(link_capitulo)

        print(nombrecapitulo)

        #creamos la hebra para que ponga a descargar y pueda seguir con el resto
        hebra = threading.Thread(target=descargarFicheroconBarra, args=(video_url, ruta+nombrecapitulo+'.mp4', numero_hebra))
        hebra.start()
        #anadimos la hebra a la lista para poder controlarla desde fuera
        threads.append(hebra)

    #pausa antes de elegir el reproductor
    #numero hebra es la posicion dondre saldra la barra de descarga, que corresponde con la hebra
    def descargar_capitulo_con_eleccion(self, link_capitulo, numero_hebra, ruta = ''):
        
        video_url, nombrecapitulo = self.reproducirvideo_elegible(link_capitulo)

        print(nombrecapitulo)

        #creamos la hebra para que ponga a descargar y pueda seguir con el resto
        hebra = threading.Thread(target=descargarFicheroconBarra, args=(video_url, ruta+nombrecapitulo+'.mp4', numero_hebra))
        hebra.start()
        #anadimos la hebra a la lista para poder controlarla desde fuera
        threads.append(hebra)

    def descargar_serie(self, link_serie):
        existsCarpeta('Animes descargados/')

        self.driver.get(link_serie)
        #espera para la carga
        sleep(7)
        #cerramos el popup de inicio
        self.close_all_tabs(1)
        sleep(0.5)

        titulo_serie = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/h2').text
        nombre_carpeta_serie = 'Animes descargados/'+titulo_serie+'/'
        existsCarpeta(nombre_carpeta_serie)

        elemento_lista_capitulos = self.driver.find_element_by_xpath('//*[@id="episodeList"]')
        elementos_capitulo = elemento_lista_capitulos.find_elements_by_xpath('li/a')

        lista_capitulos = list()
        for ecapitulo in elementos_capitulo:
            link_capitulo = ecapitulo.get_property('href')
            lista_capitulos.append(link_capitulo)

        for capitulo in lista_capitulos:
            print("Descargando: " + capitulo)
            #self.descargar_capitulo(capitulo, lista_capitulos.index(capitulo), nombre_carpeta_serie)
            self.descargar_capitulo_con_eleccion(capitulo, lista_capitulos.index(capitulo), nombre_carpeta_serie)


def existsCarpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)