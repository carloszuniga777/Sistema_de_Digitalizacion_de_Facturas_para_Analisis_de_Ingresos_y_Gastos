import os

# Desactiva verificación de red
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"   # Desactiva la verificación de conectividad al inicio 
                                                               # (un chequeo de red que no es necesario para usar el OCR Paddleocr). 
                                                               # El reconocimiento de texto sigue funcionando igual.         

from ocr.extractor          import InvoiceOCRExtractor
from utils.file_manager     import obtener_facturas
from utils.data_transformer import csv_a_dataframe
from utils.logger           import configurar_logger
from ia.processor           import estructurar_texto
from database.repository    import cargar_sql

import asyncio
import logging
import nest_asyncio
nest_asyncio.apply()  # Necesario para ejecutar asyncio en Positron/Jupyter/IPython  | # En Positron: necesario y En VSCode: no hace nada, no rompe nada



# Se inicializa el logger para que pueda imprimir los warning, info y error
# Se llama UNA sola vez al inicio, todos los módulos lo heredan
configurar_logger() 

logger = logging.getLogger(__name__)



async def main():
    
    logger.info("✅ Iniciando procesamiento de extracción de facturas...")
    
    # 1. Inicializa el extractor de pdf e imagenes
    extractor = InvoiceOCRExtractor()              

    # 2. Obtiene las rutas de las facturas 
    ruta_archivos = obtener_facturas()

    if not ruta_archivos:
        logger.warning("⚠️ No se encontraron facturas. Verifica la carpeta.")
        return
        
    # 3. Extrae el contenido de los pdf  
    texto_pdf = extractor.extraer_texto_pdf(ruta_archivos)
     
    # 4. Extrae el contenido de las imagenes
    texto_img = extractor.extraer_texto_imagenes(ruta_archivos)

    # 5. Unifica lista pdf e imagenes en una sola lista
    texto_no_estructurado = texto_pdf + texto_img    

    if not texto_no_estructurado:
        logger.warning("⚠️ No se pudo extraer texto de ninguna factura.")
        return

    # 6. Extructura el contenido en formato cvs 
    texto_estructurado = await estructurar_texto(texto_no_estructurado)


    if not texto_estructurado:
        logger.warning("⚠️ No se pudo estructurar la información, hubo un problema con la IA.")
        return

     # 7. Lo convierte a dataframe
    df = csv_a_dataframe(texto_estructurado)


    if df.empty or df is None:
        logger.warning("⚠️ No se pudo procesar el CSV.")
        return

    # 8. Lo carga a la base de datos
    sql = cargar_sql(df)

    if not sql:
        logger.warning("⚠️ No se pudo procesar la carga en la base de datos.")
        logger.error("❌ El proceso no completó exitosamente.")
        return 


    logger.info("✅ Proceso completado exitosamente.")

    return df, texto_no_estructurado, texto_estructurado


if __name__ == "__main__":
    df, texto_no_estructurado, texto_estructurado = asyncio.run(main())

    if df.empty or df is None:
        logger.error("❌ El proceso no completó exitosamente.")