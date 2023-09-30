from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Enlace a NASA Exoplanet
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Controlador web
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    ## AGREGA CÓDIGO AQUÍ ##
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content, "html.parser")
        temlist=[]
        for trtag in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdtag=trtag.find_all("td")
            for tdtags in tdtag:
                try: 
                    temlist.append(tdtags.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temlist.append("")
        new_planets_data.append(temlist)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Llamar al método
for index, row in planet_df_1.iterrows():

     ## ADGREGA CÓDIGO AQUÍ ##
     print(row["hyperlink"])
     scrape_more_data(row["hyperlink"])

     # Llama a scrape_more_data(<hyperlink>)

     print(f"La extracción de datos del hipervínculo {index+1} se ha completado")

print(new_planets_data[0:10])

# Remover el carácter '\n' de los datos extraídos
scraped_data = []

for row in new_planets_data:
    replaced = []
    ## AGREGAR EL CÓDIGO AQUÍ ##
    for el in row:
        el=el.replace("\n","")
        replaced.append(el)

    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["Brown_dwarft","Constellation", "Rigth_ascencion", "Distance", "Mass", "Radius"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convertir a CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
