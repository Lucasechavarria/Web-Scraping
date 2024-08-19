Este es un proyecto donde intentaremos extraer informacion sobre el mercado de casas premoldeadas para evaluar su evolucion en el tiempo.

Como primer paso creamos un modelo que permita extraer informacion de una pagina web, almacene la informacion extraida (limpieza incluida) y actualice automaticamente la informacion a un archivo de excel con el objetivo de graficar los precios a lo largo del tiempo.

Para poner en marcha el proyecto hay que seguir las instrucciones del archivo con instrucciones para su uso

se realizan las siguientes modificaciones:

Manejo de Errores: Se agregó manejo de excepciones para la solicitud HTTP y la conexión a la base de datos.

Verificación de Elementos HTML: Se verifica si los elementos HTML existen antes de intentar extraer datos.

Limpieza de Datos: Se limpian los datos extraídos (strip() para eliminar espacios).

Logging: Se agregó logging para registrar el flujo del programa y posibles errores.

Validación de Datos: Se valida que el precio sea un valor numérico antes de insertarlo en la base de datos.