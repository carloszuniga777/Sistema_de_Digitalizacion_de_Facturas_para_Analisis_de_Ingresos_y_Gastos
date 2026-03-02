import os

def obtener_facturas():
    facturas = []
    carpeta_factura = "./facturas"
    contenido = os.listdir(carpeta_factura)

    if not contenido:
         print("La carpeta 'facturas' está vacía. No hay nada que procesar.")
         return facturas
    else:         

        # Recorrer todas las carpetas dentro de la carpeta "facturas"
        for carpeta in sorted(os.listdir(carpeta_factura)):
            ruta_carpeta_meses = os.path.join(carpeta_factura + "/", carpeta)

            # Verificar que sea una carpeta antes de intentar listar
            if not os.path.isdir(ruta_carpeta_meses):
                print(f"⚠️ Ignorando archivo suelto: {ruta_carpeta_meses}")
                continue

            # Recorrer todos los archivos dentro de la carpeta
            for archivo in os.listdir(ruta_carpeta_meses):
                ruta_pdf = os.path.join(ruta_carpeta_meses + "/", archivo)

                facturas.append(ruta_pdf)
                # print(f"📄 Procesando factura: {ruta_pdf}")

    return facturas
