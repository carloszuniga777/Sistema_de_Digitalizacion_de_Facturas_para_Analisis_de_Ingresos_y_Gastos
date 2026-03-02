import os
import fitz                     # PyMuPDF
from google import genai        # Geminis
from google.genai import types
from dotenv import load_dotenv  # Carga las variables de entorno
import src.utils.prompts
import asyncio
import pandas as pd
from io import StringIO
import sqlite3
from datetime import date


SQLITE_DB = "database/facturas.db"


# # Cargar variables de entorno desde el archivo .env
# load_dotenv(".env")

# # Obtener la clave de API de OpenAI desde las variables de entorno
# GEMINIS_API_KEY = os.getenv("GOOGLE_GEMINIS_API_KEY")




# def obtener_facturas():
#     facturas = []
#     carpeta_factura = "./facturas"
#     contenido = os.listdir(carpeta_factura)

#     if not contenido:
#          print("La carpeta 'facturas' está vacía. No hay nada que procesar.")
#          return facturas
#     else:         

#         # Recorrer todas las carpetas dentro de la carpeta "facturas"
#         for carpeta in sorted(os.listdir(carpeta_factura)):
#             ruta_carpeta_meses = os.path.join(carpeta_factura + "/", carpeta)

#             # Verificar que sea una carpeta antes de intentar listar
#             if not os.path.isdir(ruta_carpeta_meses):
#                 print(f"⚠️ Ignorando archivo suelto: {ruta_carpeta_meses}")
#                 continue

#             # Recorrer todos los archivos dentro de la carpeta
#             for archivo in os.listdir(ruta_carpeta_meses):
#                 ruta_pdf = os.path.join(ruta_carpeta_meses + "/", archivo)

#                 facturas.append(ruta_pdf)
#                 # print(f"📄 Procesando factura: {ruta_pdf}")

#     return facturas



# def extraer_texto_pdf(rutas):
#     pdf = [] 

#     # 1. Busca todos los pdf
#     rutas_pdf = [ruta for ruta in rutas if ruta.lower().endswith(".pdf")]

#     # 2. Valida que haya archivos pdf, sino los hay se sale
#     if not rutas_pdf:
#        print("No se encontraron archivos PDF para procesar.")
#        return pdf  # Retorna lista vacía          

#     # 3. Itera sobre cada pdf y extrae su contenido    
#     for ruta in rutas_pdf:    
#         doc = fitz.open(ruta)  # Abrir PDF
#         text = "\n".join([page.get_text("text") for page in doc])  # Extraer texto
#         pdf.append(text)

#     return pdf




# def extraer_texto_imagenes(rutas, ocr):
#     content_images = []

#     # 1. Busca todas las imagenes
#     rutas_img = [ruta for ruta in rutas if ruta.endswith(('.png', '.jpg', '.jpeg'))]

#     # 2. Si no encuentra imagenes se sale
#     if not rutas_img:
#         print("No se encontraron archivos PDF para procesar.")
#         return content_images

#     # 3. Procesamos la factura
#     for ruta in rutas_img:
        
#         output = ocr.predict(ruta)         


#     for res in output:
#         res.print()

#         # lineas_texto  = []

#         # # output es un generador/lista de resultados por imagen
#         # for resultado in output:
#         #     if resultado and hasattr(resultado, 'rec_texts'):        # Cada resultado tiene rec_texts (textos) y rec_scores (confianza)
#         #         for texto in resultado.rec_texts:
#         #             if texto:
#         #                 lineas_texto.append(texto)

#         # # Unimos todas las líneas detectadas con un salto de línea
#         # texto_unido = "\n".join(lineas_texto)

#         # # Guardamos el nombre del archivo y su texto
#         # content_images.append({
#         #     "archivo": ruta,
#         #     "texto_crudo": texto_unido
#         # })

#     return content_images




# """
# Envía el texto a OpenAI y obtiene la respuesta estructurada en CSV,
# asegurando que solo devuelva datos válidos o 'error' en caso de problema.
# """

# async def estructurar_texto(texto_no_estructurado_list, tamanio_lote=30):

#     texto_estructurado = []    

#      # Validacion si la lista viene vacia   
#     if not texto_no_estructurado_list: 
#         print('No se encontró ningun contenido para que la IA lo estructure')
#         return texto_estructurado
 

#     client = genai.Client(api_key=GEMINIS_API_KEY)
#     semaforo = asyncio.Semaphore(3)                   # Máximo 3 llamadas simultáneas

#     async def procesar_lote_geminis(lote, indice):
#         async with semaforo:
            
#             # Se concatenan las facturas del lote en un solo string, separadas por una marca
#             # que permitirá al modelo identificar dónde termina una y empieza la siguiente.
#             separador = "\n\n--- FACTURA NUEVA ---\n\n"
#             texto_lote = separador.join(lote)
            
#             try:
#                 # Realizamos la petición a geminis
#                 # Documentacion API: https://ai.google.dev/gemini-api/docs/quickstart?hl=es-419
#                 respuesta = await client.aio.models.generate_content(
#                     model="gemini-3-flash-preview",
#                     contents=prompts.prompt + "\n Este es el texto a parsear:\n" + texto_lote,
#                     config=types.GenerateContentConfig(
#                         system_instruction=prompts.instrucciones_sistema,
#                         temperature=0.1,                                     # Baja temperatura para que sea más preciso y menos creativo
#                     ),
#                 )

#                 # print(f'inidice {indice}')

#                 return respuesta.text
            
#             except asyncio.TimeoutError:
#                 print(f"Lote {indice}: Timeout, la API tardó demasiado.")
#                 return None

#             except Exception as e:
#                 print(f"Error en lote {indice}: {e}")
#                 return None  

    
#     # Se crean TODAS las corrutinas primero (sin await), luego se resuelven juntas
#     response = [ 
#                 procesar_lote_geminis(texto_no_estructurado_list[i:i + tamanio_lote], i)
#                for i in range(0, len(texto_no_estructurado_list), tamanio_lote) 
#              ]


#     # Se ejecutan todas las corrutinas de los lotes concurrentemente,
#     # respetando el límite de 3 llamadas simultáneas impuesto por el semáforo.
#     # Los resultados se recogen en el mismo orden de los lotes.
#     contenido = await asyncio.gather(*response)


#     # Imprime los lotes que fallaron: 
#     lotes_fallidos = [i for i, r in enumerate(contenido) if r is None]
    
#     if lotes_fallidos:
#         print(f"Advertencia: {len(lotes_fallidos)} lotes fallaron: {lotes_fallidos}")


#     texto_estructurado =  [r for r in contenido if r is not None]  # Solo devuelve los elementos que no tuvieron error es decir, no son "None"

#     return texto_estructurado
           


# """Convierte el texto CSV en un DataFrame de pandas, asegurando que 'importe' sea numérico."""

# def csv_a_dataframe(list_csv):

#     if not list_csv:
#         print("No se encontró ningún contenido para convertir a dataframe.")
#         return []

#     # Definir los tipos de datos para cada columna
#     dtype_cols = {
#         "fecha_factura": str,
#         "proveedor": str,
#         "rtn_proveedor": str,
#         "direccion_proveedor": str,
#         "telefono_proveedor":str,
#         "pais_proveedor":str,
#         "nombre_cliente":str,
#         "rtn_cliente": str,
#         "concepto": str,
#         "monto_total": str,  # Se leerá primero como str para poder limpiar comas
#         "moneda": str,
#         "tipo_factura": str
#     }
    
#     # Recorre cada elemento y crea una lista de dataframe
#     lista_df = [pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols) 
#                 for csv in list_csv]  

#     df = pd.concat(lista_df, ignore_index=True)

 
#     # Convertir 'importe' a float, asegurando que los valores con coma se conviertan correctamente
#     df["monto_total"] = (
#         df["monto_total"]
#         .str.replace(",", "", regex=False)
#         .astype(float)
#     )


#     # Convertir las monedas a lempiras
#     # Ultima actualizacion montos: 28-febrero-2026
    
#     df['monto_total_lempiras'] = 0.0           # inicializar
#     df.loc[df["moneda"] == "dolares", "monto_total_lempiras"] = df.loc[df["moneda"] == "dolares", "monto_total"] * 26.5057
#     df.loc[df["moneda"] == "euros", "monto_total_lempiras"] = df.loc[df["moneda"] == "euros", "monto_total"] * 29.6864
#     df.loc[df["moneda"] == "lempiras", "monto_total_lempiras"] = df.loc[df["moneda"] == "lempiras", "monto_total"]
    
#     df["fecha_carga"] = pd.Timestamp.now()

#     # Extrayendo ano, mes, dia
#     df["fecha_factura"] = pd.to_datetime(df["fecha_factura"], format="%d/%m/%Y")   # Convirtiendo a datetime
    
#     df['dia_factura'] = df['fecha_factura'].dt.day
#     df['mes_factura'] = df["fecha_factura"].dt.month
#     df['ano_factura'] = df['fecha_factura'].dt.year

#     return df



# def cargar_sql(df):
    
#      # Validacion si dataframe viene vacio
#     if df.empty:
#         print("Advertencia: El DataFrame está vacío. No hay datos para insertar.")
#         return 

#     try:
#         with sqlite3.connect(SQLITE_DB, timeout=30) as conn:
            
#             conn.execute('BEGIN EXCLUSIVE')
    
#             # Creacion de tabla
#             conn.execute('''
#                 CREATE TABLE IF NOT EXISTS tbl_facturas(
#                     fecha_carga          text,
#                     fecha_factura        text,
#                     dia_factura          text,
#                     mes_factura          text,
#                     ano_factura          text,
#                     numero_factura       text, 
#                     proveedor            text, 
#                     rtn_proveedor        text, 
#                     direccion_proveedor  text, 
#                     telefono_proveedor   text, 
#                     pais_proveedor       text, 
#                     nombre_cliente       text, 
#                     rtn_cliente          text, 
#                     concepto             text, 
#                     monto_total          real, 
#                     moneda               text, 
#                     monto_total_lempiras real,
#                     tipo_factura         text
#                 )   
#             ''')
#             print("Tabla creada correctamente")



#             # Borrar facturas del año actual
#             ano_actual = date.today().year
#             conn.execute(
#                 "DELETE FROM tbl_facturas WHERE strftime('%Y', fecha_factura) = ?",
#                 (str(ano_actual),)
#             )

#             # Insertar datos
#             df.to_sql(
#                  "tbl_facturas",                                # Nombre de tabla
#                  conn,                                          # Conexion a la base de datos
#                  if_exists="append",                            # Si existe inserta
#                  index=False                                    # No incluir el indice del dataframe
#              )

#             print("Datos insertados correctamente")
#             print("Proceso de extracción y estructuración de facturas completado exitosamente.")
#             print("Datos guardados en la base de datos 'facturas.db'.")
            
#             conn.commit()    
   
#     except Exception as e: 
#         print(f"Error en la creacion e insercion de datos en SQLITE: {str(e)}")


    