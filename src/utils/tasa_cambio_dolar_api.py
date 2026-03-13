import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import logging  


load_dotenv()                           # Carga las variables de entorno
logger = logging.getLogger(__name__)    # Configuracion de logger 

# API
BCH_API_KEY = os.getenv("BCH_API_KEY")
BCH_URL     = "https://bchapi-am.azure-api.net/api/v1/indicadores/97/cifras?reciente=1&formato=json"


# Ubicacion del archivo de cache de tasa de cambio
CACHE_FILE = Path(__file__).parent.parent / "cache" / "tasa_cambio_cache.json"



def obtener_tasa_cambio_dolar() -> float | None:
    try:
        # Peticion    
        response = requests.get(
            BCH_URL,
            headers={"clave": BCH_API_KEY},
            timeout=10
        )
        
     
        response.raise_for_status()             # Lanza una excepción automáticamente si el servidor devuelve un código de error HTTP como 400, 401, 403, 404, 500
        data = response.json()
        tasa = float(data[0]["Valor"])
        
        # Guardar en caché en formato json
        CACHE_FILE.write_text(json.dumps({"tasa": tasa}))

        logger.info(f"✅ Tasa de cambio obtenida del BCH: L. {tasa}")
        
        return tasa
    
    except Exception as e:
        logger.warning(f"⚠️ API no disponible: {e}")
        
        # Si la API dio error 
        if CACHE_FILE.exists():
            tasa_cache = json.loads(CACHE_FILE.read_text())["tasa"]
            logger.warning(f"⚠️ Usando tasa en caché: L. {tasa_cache}")
            return tasa_cache

        logger.error("❌ No hay caché disponible, no se pudo obtener la tasa")
        return None


# Borrar esto
# if __name__ == "__main__":
#    tasa = obtener_tasa_cambio()
#     print(tasa)