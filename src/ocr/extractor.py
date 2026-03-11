import fitz                                              # PyMuPDF
from utils.clean_ocr import limpiar_texto_ocr
from paddleocr import PaddleOCR
import logging                                           # Imprime print() en produccion 



logger = logging.getLogger(__name__)  # ← __name__ toma el nombre del módulo automáticamente


"""
Módulo de extracción de texto desde imágenes y PDFs de facturas.
"""

class InvoiceOCRExtractor:
    """
    Extractor de texto para facturas con fallback automático a modelo avanzado.
    
    Usa modelo mobile (rápido) por defecto. Si la confianza promedio
    de una imagen es baja, reintenta automáticamente con modelo server (más preciso).
    
    Ejemplo:
        extractor = InvoiceOCRExtractor()
        textos = extractor.extraer_texto_imagenes(rutas)
    """

    UMBRAL_CONFIANZA = 0.70  # Por debajo de esto se reprocesa con modelo avanzado

    # ──────────────────────── Constructor ──────────────────────────────────────────

    # Inicializacion
    def __init__(self):
        self._ocr_basico   = self._crear_ocr_basico()              # Inicializar el OCR PaddleOCR con modelo bajo
        self._ocr_avanzado =  None                                 # ← no carga hasta que se necesite


    # ──────────────────────── Métodos públicos ────────────────────────────────────

    # 1. Metodo para extraer documentos PDF
    def extraer_texto_pdf(self, rutas: list[str]) -> list[str]:
        
        """Extrae texto de archivos PDF usando PyMuPDF."""

        # 1. Busca las rutas que contengan archivos pdf 
        rutas_pdf = [r for r in rutas if r.lower().endswith(".pdf")]

        # 2. Si no encuentra PDF sale
        if not rutas_pdf:
            logger.warning("⚠️ No se encontraron archivos PDF que procesar.")
            return []         
        

        resultado = []

        # 3. Itera sobre cada ruta pdf y extrae su contenido 
        for ruta in rutas_pdf:
            doc  = fitz.open(ruta)                                              # Extrae su contenido
            text = "\n".join([page.get_text("text") for page in doc])           # Itera para extraer su contenido 
            resultado.append(text)                                              # Almacena


        logger.info('✅ Extracción de PDF finalizó exitosamente')

        return resultado





    # 2. Metodo para extraer Imagenes
    def extraer_texto_imagenes(self, rutas: list[str]) -> list[str]:
        """
        Extrae texto de imágenes con fallback automático a modelo avanzado
        cuando la confianza promedio es menor al umbral definido.
        """
        
        # 1. Busca las rutas que contendan archivos imagenes
        rutas_img = [r for r in rutas if r.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # 2. Si no encuentra imagenes sale
        if not rutas_img:
            logger.warning("⚠️ No se encontraron archivos de imagen que procesar.")
            return []
        
        resultado = []

        # 3. Itera sobre cada imagen y extrae su contenido
        for ruta in rutas_img:
            texto = self._procesar_imagen(ruta)          # Extrae su contenido
            resultado.append(texto)                      # Almacena
        

        logger.info('✅ Extracción de imagenes finalizó correctamente')

        return resultado

     
    # ──────────────────── Métodos privados ───────────────────────────────────────────────


    # 3. Inicializa el OCR avanzado
    def _obtener_ocr_avanzado(self) -> PaddleOCR:
      """Carga el modelo avanzado solo la primera vez que se necesita."""
      
      if self._ocr_avanzado is None:
          self._ocr_avanzado = self._crear_ocr_avanzado()
      
      return self._ocr_avanzado


     # 4. Extrae el contenido de las imagenes 
    def _procesar_imagen(self, ruta: str) -> str:
        """Procesa una imagen, con reintento automático si la confianza es baja."""
        
        results = self._ocr_basico.predict(ruta)                                     # Extrae su toda la informacion y contenido de la imagenes (Sucio)
        lineas, scores = self._extraer_lineas_y_scores(results)                      # Extrae el contenido de las imagenes en una lista y una lista de puntaje score(0 a 1) que indica el nivel de confianza, ese puntaje indica si el modelo entendio o no el contenido que extrajo, dandole un puntaje 


        # Calcula un promedio de confianza que indica si el modelo entendio todo el contenido de la imagen, 
        # Si su promedio es mas bajo que el umbral de confianza, se procesa con un modelo OCR mas avanzado
      
        promedio = sum(scores) / len(scores) if scores else 0

        if promedio < self.UMBRAL_CONFIANZA:
           # logger.warning(f"⚠️ Baja confianza ({promedio:.2f}), reprocesando con modelo avanzado: {ruta}")

            # Se reprocesa la imagen con el modelo server que es mas avazando  
            results = self._obtener_ocr_avanzado().predict(ruta)                   # ← carga aquí si se necesita: Patrón se llama lazy initialization, inicializar solo cuando se necesita.     
         
            lineas, _ = self._extraer_lineas_y_scores(results)                # Extrae el contenido de las imagenes en una lista y una lista de puntaje score(0 a 1) que indica el nivel de confianza, ese puntaje indica si el modelo entendio o no el contenido que extrajo, dandole un puntaje 

          
        texto = "\n".join(lineas)                                             # Unifica todo el contenido extraido en una sola linea 
        return limpiar_texto_ocr(texto)                                       # Realiza correcciones en el texto por si el OCR mal interpreto algun caracter raro


    

    # 4. Metodo obtener el contenido de las imagenes:
    #    Procesa la informacion extraida de la imagen para obtener su contenido y darle una puntuacion a cada elemento extraido, esta puntuncion es el nivel de confianza que indica
    #    si el modelo entenido el elemento extraido de la imagen dandole una puntuacion de 0-1
    
    def _extraer_lineas_y_scores(self, results: list) -> tuple[list[str], list[float]]:
        """Convierte los resultados raw de PaddleOCR en listas de texto y scores."""
      
        lineas  = []
        scores  = []

        # Valida que el elemento de la lista no lleve None    
        for result in results:
            if result is None:
                continue

            texts  = result.get("rec_texts", [])              # Obtiene el texto de la imagen
            scores = result.get("rec_scores", [])             # Obtiene la puntuacion del elemento 


            # logger.warning(f'texts: {texts}, score: {scores}')

            for text, score in zip(texts, scores):

                # Filtra el contenido, si su nivel de confianza es mayor a 0.5 lo toma en consideracion, sino lo descarta
                if text.strip() and float(score) >= 0.3:
                    lineas.append(text.strip())
                    scores.append(float(score))

        return lineas, scores


    # ──────────────────── Métodos Estaticos ───────────────────────────────────────────────
    
    # 5. Inicializacion del modelo basico OCR de PaddleOCR
    @staticmethod
    def _crear_ocr_basico() -> PaddleOCR:
        """Modelo mobile: rápido, suficiente para imágenes limpias."""
        
        return PaddleOCR(
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
            lang="es",
        )

    # 6. Inicializacion del modelo avanzado OCR de PaddleOCR
    @staticmethod
    def _crear_ocr_avanzado() -> PaddleOCR:
        """Modelo server: más lento, mejor para imágenes difíciles."""

        return PaddleOCR(
            text_detection_model_name="PP-OCRv5_server_det",
            text_recognition_model_name="PP-OCRv5_server_rec",
            use_doc_orientation_classify=True,                # ← activa para fotos inclinadas
            use_doc_unwarping=True,                           # ← corrige perspectiva en fotos
            use_textline_orientation=True,                    # ← ayuda con texto inclinado
            text_det_thresh=0.2,                              # ← más sensible
            text_det_box_thresh=0.4,                          # ← acepta cajas menos seguras
            text_det_unclip_ratio=2.5,                        # ← más dilatación
            enable_mkldnn=False,
            lang="es",
        )
    



