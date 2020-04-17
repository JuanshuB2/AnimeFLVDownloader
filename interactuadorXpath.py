from time import sleep

def seleccionar_segunda_opcion(downloader, n_opcion):
    #clickamos la segunda opcion
    opc_2 = downloader.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/ul/li[2]/a')
    opc_2.click()

def seleccionar_opcionFembed(downloader):
    contenedor_opciones = downloader.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/ul')
    opciones = contenedor_opciones.find_elements_by_xpath('li')

    for opcion in opciones:
        titulo_opcion = opcion.get_attribute("title")
        if(titulo_opcion == 'Fembed'):
            opcion.find_element_by_xpath('a').click()
    

def getVideo_Fembed(downloader):
    #cambiamos el contexto, al reproductor de video (es una web incrustada)
    iframe_video = downloader.driver.find_element_by_xpath('//*[@id="video_box"]/iframe')
    downloader.driver.switch_to_frame(iframe_video)
    #le damos al play
    botonPlay = downloader.driver.find_element_by_xpath('/html/body/div[2]/div')
    botonPlay.click()

    sleep(0.5)
    downloader.close_all_tabs(1)

    #Espera para la carga del video
    sleep(20)

    iframe_video2 = downloader.driver.find_element_by_xpath('//*[@id="video_box"]/iframe')
    downloader.driver.switch_to_frame(iframe_video2)
    capitulo = downloader.driver.find_element_by_xpath('//*[@id="vstr"]/div[2]/div[3]/video')

    return capitulo

def getVideo_general(downloader):
    print("funcion por implementar")

#Devuelve la url y el nombre
def reproducirvideo(downloader, link_capitulo):
    #vamos a la web
    downloader.driver.get(link_capitulo)
    #espera para la carga
    sleep(7)
    #cerramos el popup de inicio
    downloader.close_all_tabs(1)
    sleep(0.5)

    seleccionar_opcionFembed(downloader)

    #Guardamos el nombre del capitulo
    nombre_capitulo = downloader.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/div[1]/h1').text

    #Espera carga reproductor
    sleep(7)

    capitulo = getVideo_Fembed(downloader)

    #Guarreria para que cierre la puta tab 
    #self.abrirnuevaTab()
    #tabs = self.driver.window_handles
    #self.driver.switch_to.window(tabs[0])
    #self.driver.close()
    #tabs = self.driver.window_handles
    #self.driver.switch_to.window(tabs[0])

    return capitulo.get_property('src'), nombre_capitulo

#Devuelve la url y el nombre
def reproducirvideo_elegible(downloader, link_capitulo):
    #Guardamos el nombre del capitulo
    nombre_capitulo = downloader.driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/div[1]/h1').text

    #Espera carga reproductor
    raw_input("Elige la opcion y presiona una tecla")

    capitulo = downloader.getVideo_Fembed()

    #Guarreria para que cierre la puta tab 
    #self.abrirnuevaTab()
    #tabs = self.driver.window_handles
    #self.driver.switch_to.window(tabs[0])
    #self.driver.close()
    #tabs = self.driver.window_handles
    #self.driver.switch_to.window(tabs[0])

    return capitulo.get_property('src'), nombre_capitulo