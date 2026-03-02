
import sqlite3
from pathlib import Path
from datetime import date


# ✅ Robusto - siempre apunta al mismo lugar sin importar desde dónde ejecutas
SQLITE_DB = Path(__file__).parent / "facturas.db"


def cargar_sql(df):
    
     # Validacion si dataframe viene vacio
    if df.empty:
        print("Advertencia: El DataFrame está vacío. No hay datos para insertar.")
        return 

    try:
        with sqlite3.connect(SQLITE_DB, timeout=30) as conn:
            
            conn.execute('BEGIN EXCLUSIVE')
    
            # Creacion de tabla
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tbl_facturas(
                    fecha_carga          text,
                    fecha_factura        text,
                    dia_factura          text,
                    mes_factura          text,
                    ano_factura          text,
                    numero_factura       text, 
                    proveedor            text, 
                    rtn_proveedor        text, 
                    direccion_proveedor  text, 
                    telefono_proveedor   text, 
                    pais_proveedor       text, 
                    nombre_cliente       text, 
                    rtn_cliente          text, 
                    concepto             text, 
                    monto_total          real, 
                    moneda               text, 
                    monto_total_lempiras real,
                    tipo_factura         text
                )   
            ''')
            print("Tabla creada correctamente")



            # Borrar facturas del año actual
            ano_actual = date.today().year
            conn.execute(
                "DELETE FROM tbl_facturas WHERE strftime('%Y', fecha_factura) = ?",
                (str(ano_actual),)
            )

            # Insertar datos
            df.to_sql(
                 "tbl_facturas",                                # Nombre de tabla
                 conn,                                          # Conexion a la base de datos
                 if_exists="append",                            # Si existe inserta
                 index=False                                    # No incluir el indice del dataframe
             )

            print("Datos insertados correctamente")
            print("Proceso de extracción y estructuración de facturas completado exitosamente.")
            print("Datos guardados en la base de datos 'facturas.db'.")
            
            conn.commit()    
   
    except Exception as e: 
        print(f"Error en la creacion e insercion de datos en SQLITE: {str(e)}")
