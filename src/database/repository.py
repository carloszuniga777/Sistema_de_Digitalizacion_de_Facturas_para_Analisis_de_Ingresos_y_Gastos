import sqlite3
from pathlib import Path
from datetime import date
import pandas as pd
import logging

# Configuración de logging en lugar de print
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



SQLITE_DB = Path(__file__).parent / "facturas.db"



# Definición de la tabla 
CREATE_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS tbl_facturas (
        fecha_carga          TEXT,
        fecha_factura        TEXT,
        dia_factura          TEXT,
        mes_factura          TEXT,
        ano_factura          TEXT,
        numero_factura       TEXT,
        proveedor            TEXT,
        rtn_proveedor        TEXT,
        direccion_proveedor  TEXT,
        telefono_proveedor   TEXT,
        pais_proveedor       TEXT,
        nombre_cliente       TEXT,
        rtn_cliente          TEXT,
        concepto             TEXT,
        monto_total          REAL,
        moneda               TEXT,
        monto_total_lempiras REAL,
        tipo_factura         TEXT,
        categoria            TEXT
    )
'''





def cargar_sql(df: pd.DataFrame) -> bool:
    """
    Carga un DataFrame en la tabla tbl_facturas, reemplazando los registros del año actual.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    if df.empty:
        logging.warning("⚠️ El DataFrame está vacío. No hay datos para insertar.")
        return False


    # Validación opcional: que el DataFrame tenga las columnas esperadas
    expected_columns = [
        'fecha_carga', 
        'fecha_factura', 
        'dia_factura', 
        'mes_factura', 
        'ano_factura',
        'numero_factura', 
        'proveedor', 
        'rtn_proveedor', 
        'direccion_proveedor',
        'telefono_proveedor', 
        'pais_proveedor', 
        'nombre_cliente', 
        'rtn_cliente',
        'concepto', 
        'monto_total', 
        'moneda', 
        'monto_total_lempiras', 
        'tipo_factura',
        'categoria'
    ]

    # Valida que las columnas del dataframe sean las correctas 
    if not all(col in df.columns for col in expected_columns):
        logging.error("❌ El DataFrame no contiene todas las columnas requeridas.")
        return False

    # Se obtiene el año actual
    ano_actual = str(date.today().year)

    try:
        with sqlite3.connect(SQLITE_DB, timeout=30) as conn:
            
            # Crear tabla si no existe 
            conn.execute(CREATE_TABLE_SQL)

            # Iniciar transacción con bloqueo IMMEDIATE (previene escrituras concurrentes)
            conn.execute('BEGIN IMMEDIATE')


            # Insertar nuevos datos
            df.to_sql(
                "tbl_facturas",
                conn,
                if_exists="append",
                index=False,
                method="multi"      # Para inserts por lotes (mejor rendimiento con muchos datos)
            )



            # Eliminar facaturas duplicadas dejando la factura mas antigua  
            conn.execute(
                """delete from tbl_facturas 
                   where rowid in (select rowid from ( select rowid, 
                                                              row_number() over (partition by numero_factura order by fecha_carga asc) as r
                                                        from tbl_facturas 
                                                      ) as t
                                    where r > 1 
                                  )    
                """
            )


            # Confirmar transacción
            conn.commit()
            
            logging.info("✅ Datos insertados a la base de datos correctamente para el año %s", ano_actual)
            
            return True

    except sqlite3.OperationalError as e:
        logging.error("❌ Error de base de datos (posible bloqueo o sintaxis): %s", e)
        # No es necesario rollback explícito, el context manager lo hará al salir
        return False
    
    except Exception as e:
        logging.error("❌ Error inesperado: %s", e)
        return False