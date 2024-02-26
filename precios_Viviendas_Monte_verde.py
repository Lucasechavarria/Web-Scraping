# Importamos paquetes necesarios
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pyodbc

# Colocamos la pagina de la que vamos a extraer la info
url = "https://viviendasmonteverde.com.ar/"

# Indicamos que navegador vamos a simular 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Realizamos el requests(solicitud a la web)
response = requests.get(url, headers=headers)
#Almacenamos la respuesta en una variable con formato texto
contenido = response.text

# Instanciamos el objeto 
soup = BeautifulSoup(contenido, 'lxml')
casa=[]
precio=[]
fecha = []

# Guardamos las etiquetas y clases por las que vamos a iterar para extraer la info de interes
box = soup.find_all('h2', class_='titulo-cuadrados titulo-sucursales')
box2 = soup.find_all('h4', class_='hero-text texto-sucursales')

# Creamos los bucles que iteraran para guardar en cada iteracion la info en cada variable
for modelo in box:
        casa.append(modelo.text)

for modelo in box2:
        precio.append( modelo.text)
        fecha.append(dt.datetime.now())


# Unimos las listas y las convertimos a DataFrame

casas = list(zip(fecha,casa, precio))
casas2 = pd.DataFrame(casas, columns=['Fecha','Modelo', 'Precio'])



# Establecer la cadena de conexión a SQL, completando SERVER= con el nombre de nuestro servidor sql 
# y en DATABASE= el nombre de la base de datos en la que creamos las tablas
conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-KCPUGDG\FACULTADMARIO;DATABASE=Precios_casas;Trusted_Connection=yes')

# Crear el cursor para operar en SQL
cursor = conexion.cursor()


# Insertar los datos del DataFrame en la tabla de informacion cruda (sin tratar)
for indice, fila in casas2.iterrows():
    cursor.execute(f"INSERT INTO [Precios_casas].[dbo].[Viviendas_Monteverde_crudo] (Fecha, Modelo, Precio) VALUES (?, ?, ?)",
                   fila['Fecha'], fila['Modelo'], fila['Precio'])

# Confirmar los cambios
conexion.commit()

# Ejecutamos el proceso almacenado que ya creamos en SQL (Store Procedure)
cursor.execute('exec PA_COC_VIVIENDAS_MONTEVERDE')


conexion.commit()


# Cerrar la conexión
conexion.close()

