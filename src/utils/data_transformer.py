import pandas as pd
from io import StringIO
import logging                   # Imprime print() en produccion 

logger = logging.getLogger(__name__)  # ← __name__ toma el nombre del módulo automáticamente




"""Convierte el texto CSV en un DataFrame de pandas, asegurando que 'importe' sea numérico."""

def csv_a_dataframe(list_csv: list[str])-> pd.DataFrame | None:

    if not list_csv:
        logger.warning("⚠️ No se encontró ningún contenido para convertir a dataframe.")
        return None

    # Definir los tipos de datos para cada columna
    dtype_cols = {
        "fecha_factura": str,
        "proveedor": str,
        "rtn_proveedor": str,
        "direccion_proveedor": str,
        "telefono_proveedor":str,
        "pais_proveedor":str,
        "nombre_cliente":str,
        "rtn_cliente": str,
        "concepto": str,
        "monto_total": str,  # Se leerá primero como str para poder limpiar comas
        "moneda": str,
        "tipo_factura": str,
        "categoria": str
    }
    
    

    try:
        # Recorre cada elemento y crea una lista de dataframe
        lista_df = [pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols) 
                    for csv in list_csv]  

        df = pd.concat(lista_df, ignore_index=True)
    
    except Exception as e:
        logger.error(f"❌ Error leyendo el CSV: {e}")
        return None
    
    try:
        # Convertir 'importe' a float, asegurando que los valores con coma se conviertan correctamente
        df["monto_total"] = (
            df["monto_total"]
            .str.replace(",", "", regex=False)
            .astype(float)
        )
    except Exception as e:
        logger.error(f"❌ Error convirtiendo monto_total a número: {e}")
        return None


    
    try:
        # Convertir las monedas a lempiras
        # Ultima actualizacion montos: 28-febrero-2026
        
        df['monto_total_lempiras'] = 0.0           # inicializar
        df.loc[df["moneda"] == "dolares", "monto_total_lempiras"] = df.loc[df["moneda"] == "dolares", "monto_total"] * 26.5057
        df.loc[df["moneda"] == "euros", "monto_total_lempiras"] = df.loc[df["moneda"] == "euros", "monto_total"] * 29.6864
        df.loc[df["moneda"] == "lempiras", "monto_total_lempiras"] = df.loc[df["moneda"] == "lempiras", "monto_total"]
        
        df["fecha_carga"] = pd.Timestamp.now()

        # Extrayendo ano, mes, dia
        df["fecha_factura"] = pd.to_datetime(df["fecha_factura"], format="%d/%m/%Y")   # Convirtiendo a datetime
        
        df['dia_factura'] = df['fecha_factura'].dt.day
        df['mes_factura'] = df["fecha_factura"].dt.month
        df['ano_factura'] = df['fecha_factura'].dt.year

    except Exception as e:
        logger.error(f"❌ Error procesando columnas: {e}")
        return None
    
    
    logger.info("✅ Conversión a dataframe finalizó")
    
    return df

   

