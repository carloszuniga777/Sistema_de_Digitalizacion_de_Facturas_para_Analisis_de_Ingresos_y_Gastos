import pandas as pd
from io import StringIO



"""Convierte el texto CSV en un DataFrame de pandas, asegurando que 'importe' sea numérico."""

def csv_a_dataframe(list_csv):

    if not list_csv:
        print("No se encontró ningún contenido para convertir a dataframe.")
        return []

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
        "tipo_factura": str
    }
    
    # Recorre cada elemento y crea una lista de dataframe
    lista_df = [pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols) 
                for csv in list_csv]  

    df = pd.concat(lista_df, ignore_index=True)

 
    # Convertir 'importe' a float, asegurando que los valores con coma se conviertan correctamente
    df["monto_total"] = (
        df["monto_total"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )


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

    return df
