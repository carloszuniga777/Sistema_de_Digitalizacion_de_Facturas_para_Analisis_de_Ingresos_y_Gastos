from src.utils.clean_ocr import limpiar_texto_ocr
import fitz       # PyMuPDF


def extraer_texto_pdf(rutas):
    pdf = [] 

    # 1. Busca todos los pdf
    rutas_pdf = [ruta for ruta in rutas if ruta.lower().endswith(".pdf")]

    # 2. Valida que haya archivos pdf, sino los hay se sale
    if not rutas_pdf:
       print("No se encontraron archivos PDF para procesar.")
       return pdf  # Retorna lista vacía          

    # 3. Itera sobre cada pdf y extrae su contenido    
    for ruta in rutas_pdf:    
        doc = fitz.open(ruta)  # Abrir PDF
        text = "\n".join([page.get_text("text") for page in doc])  # Extraer texto
        pdf.append(text)

    return pdf



def extraer_texto_imagenes(rutas, ocr):
    content_images = []

    # 1. Busca todas las imagenes
    rutas_img = [ruta for ruta in rutas if ruta.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # 2. Si no encuentra imagenes se sale
    if not rutas_img:
        print("No se encontraron archivos de imagen para procesar.")
        return content_images

    # 3. Procesamos cada imagen
    for ruta in rutas_img:

        results = ocr.predict(ruta)
        lineas_texto = []

        for result in results:
            if result is None:
                continue
            
            texts  = result.get("rec_texts", [])
            scores = result.get("rec_scores", [])

            print(f'texts: {texts}, score: {scores}')

            for text, score in zip(texts, scores):
                if text.strip() and float(score) >= 0.5:
                    lineas_texto.append(text.strip())

        texto_unido = "\n".join(lineas_texto)
        texto_unido = limpiar_texto_ocr(texto_unido)
        content_images.append(texto_unido)
        
    return content_images