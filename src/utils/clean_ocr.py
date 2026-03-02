import re

def limpiar_texto_ocr(texto: str) -> str:
    
    # Corrige RTN mal leído por OCR. Ej: BTN: → RTN:
    texto = re.sub(r'\b[A-Z0-9]TN:', 'RTN:', texto)
    
    # Corrige número de factura con letras mezcladas (007-00l-0l → 007-001-01)
    texto = re.sub(r'\b(\d{3}-\d{2})[lI](-\d{2})[lI]', r'\g<1>1\g<2>1', texto)
    
    return texto