# Importamos paquetes necesarios
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pyodbc
import logging

# Configuración del logging
logging.basicConfig(filename='scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Colocamos la página de la que vamos a extraer la información
url = "https://viviendasmonteverde.com.ar/"

# Indicamos que navegador vamos a simular 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Realizamos la solicitud a la web con manejo de errores
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Esto lanzará una excepción si el código de estado HTTP no es 200
    logging.info("Solicitud realizada con éxito.")
except requests.exceptions.RequestException as e:
    logging.error(f"Error al realizar la solicitud: {e}")
    exit()

# Almacenamos la respuesta en una variable con formato texto
contenido = response.text

# Instanciamos el objeto BeautifulSoup
soup = BeautifulSoup(contenido, 'lxml')

# Inicializamos las listas para almacenar los datos
casa = []
precio = []
fecha = []

# Guardamos las etiquetas y clases por las que vamos a iterar para extraer la info de interés
box = soup.find_all('h2', class_='titulo-cuadrados titulo-sucursales')
if not box:
    logging.warning("No se encontraron elementos con la clase especificada para 'casa'.")

box2 = soup.find_all('h4', class_='hero-text texto-sucursales')
if not box2:
    logging.warning("No se encontraron elementos con la clase especificada para 'precio'.")

# Iteramos para guardar en cada iteración la información en cada variable
for modelo, precio_modelo in zip(box, box2):
    casa.append(modelo.text.strip())
    precio.append(precio_modelo.text.strip())
    fecha.append(dt.datetime.now())

# Unimos las listas y las convertimos a DataFrame
casas = list(zip(fecha, casa, precio))
casas2 = pd.DataFrame(casas, columns=['Fecha', 'Modelo', 'Precio'])

# Establecemos la conexión a la base de datos SQL
try:
    with pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-KCPUGDG\FACULTADMARIO;DATABASE=Precios_casas;Trusted_Connection=yes') as conexion:
        cursor = conexion.cursor()
        
        # Insertamos los datos del DataFrame en la tabla de información cruda
        for indice, fila in casas2.iterrows():
            if not fila['Precio'].replace('.', '').isdigit():
                logging.warning(f"Precio inválido detectado: {fila['Precio']}")
                continue
            cursor.execute(f"INSERT INTO [Precios_casas].[dbo].[Viviendas_Monteverde_crudo] (Fecha, Modelo, Precio) VALUES (?, ?, ?)",
                           fila['Fecha'], fila['Modelo'], fila['Precio'])

        # Confirmamos los cambios
        conexion.commit()
        logging.info("Datos insertados en la base de datos con éxito.")
        
        # Ejecutamos el proceso almacenado
        cursor.execute('exec PA_COC_VIVIENDAS_MONTEVERDE')
        conexion.commit()
        logging.info("Proceso almacenado ejecutado con éxito.")
except pyodbc.Error as e:
    logging.error(f"Error en la conexión con la base de datos: {e}")

logging.info("Proceso de scraping completado.")
