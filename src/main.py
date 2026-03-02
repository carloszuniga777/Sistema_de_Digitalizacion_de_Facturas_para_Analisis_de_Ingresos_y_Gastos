import os

# Desactiva verificación de red
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"   # Desactiva la verificación de conectividad al inicio 
                                                               # (un chequeo de red que no es necesario para usar el OCR Paddleocr). 
                                                               # El reconocimiento de texto sigue funcionando igual.         

from paddleocr import PaddleOCR
from src.utils.file_manager     import obtener_facturas
from src.utils.data_transformer import csv_a_dataframe
from src.ocr.extractor          import extraer_texto_pdf, extraer_texto_imagenes
from src.ia.processor           import estructurar_texto
from src.database.repository    import cargar_sql
import asyncio
import nest_asyncio
nest_asyncio.apply()  # Necesario para ejecutar asyncio en Positron/Jupyter/IPython


# Inicializacion: Solo carga detección y reconocimiento de texto. 
ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",
    text_recognition_model_name="PP-OCRv5_server_rec",
    # text_detection_model_name="PP-OCRv5_mobile_det",
    # text_recognition_model_name="PP-OCRv5_mobile_rec",
    use_doc_orientation_classify=False,   # ← activa para fotos inclinadas
    use_doc_unwarping=False,              # ← corrige perspectiva en fotos
    use_textline_orientation=False,       # Detecta orientación de líneas de texto
    enable_mkldnn=False,                  # prevents MKLDNN/PIR crash
    lang="es",
)


async def main():
    

    ruta_archivos = obtener_facturas()
        
    texto_pdf = extraer_texto_pdf(ruta_archivos)
     
    texto_img = extraer_texto_imagenes(ruta_archivos, ocr)

    texto_no_extructurado = texto_pdf + texto_img    

    texto_estructurado = await estructurar_texto(texto_no_extructurado)

    df = csv_a_dataframe(texto_estructurado)

    cargar_sql(df)

    return df, texto_no_extructurado, texto_estructurado

if __name__ == "__main__":
    df, texto_no_extructurado, texto_estructurado = asyncio.run(main())