import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

RTN_PRINCIPAL = os.getenv("RTN_PRINCIPAL")
NOMBRE_PRINCIPAL = os.getenv("NOMBRE_PRINCIPAL")


instrucciones_sistema = (
    "Eres un experto en extracción de datos de facturas. "
    "Devuelve solo el CSV sin explicaciones ni mensajes adicionales. "
    "Si no puedes extraer datos, devuelve exactamente la palabra 'error' sin comillas."
)


prompt = """
Eres un sistema especializado en extracción estructurada de facturas nacionales e internacionales.

Recibirás texto plano extraído de una o varias facturas. Debes analizar el contenido y devolver un CSV limpio usando punto y coma (;) como separador de campos.

Tu objetivo es extraer exclusivamente los datos solicitados sin inventar, inferir o completar información que no esté explícitamente presente.

Si el texto contiene múltiples facturas, debes generar una línea por cada factura detectada.

Si no puedes identificar claramente al menos fecha_factura, proveedor e importe en una factura, responde exactamente: error

No agregues explicaciones ni comentarios.


📌 Reglas estrictas de extracción y normalización:

1. fecha_factura

    ✅ Prioriza en este orden:

        1. Fecha de emisión
        2. Fecha de factura
        3. Fecha de pedido

    ✅ Ignora fecha de vencimiento.

    ✅ Convierte siempre al formato: dd/mm/aaaa.

    ✅ Si el formato original es ambiguo (ej: 01/02/24), asume formato día/mes/año.


2. proveedor
    ✅ Extrae únicamente el nombre legal o comercial del emisor.
    ✅ Devuelve el nombre en formato capitalizado:
        1. Primera letra de cada palabra en mayúscula
        2. Resto en minúscula
        3. Ejemplo:
            “MARIA GONZALEZ S.A.” → Maria Gonzalez S.A.
            “empresa comercial del norte” → Empresa Comercial Del Norte

    ✅ No incluyas dirección ni información adicional.
    ✅ Elimina signos de puntuación.
    ✅ Extrae el RTN, la direccion, telefono y pais del proveedor si estos los contiene.
    ✅ No extraiga texto adicional.
    ✅ Mantén letras y números.

3. concepto
    ✅ Haz un resumen compacto de los productos o servicios de la factura.
    ✅ Agrupa productos similares o iguales en uno solo con su cantidad total.
    ✅ Abrevia las descripciones eliminando palabras innecesarias, conservando lo esencial: marca, modelo, medida o característica clave.
    ✅ Concatena cada item resumido separado por pipe (|).
    ✅ Formato: producto1 xN | producto2 xN
    ✅ Ejemplos:
        "Arroz premium 50 lb | Frijoles rojos 25 lb | Sal refinada 25 lb" → Arroz 50lb | Frijoles 25lb | Sal 25lb
        "1306000051 Impresora Multifuncional Epson L3250 1x (x3 veces)" → Epson L3250 x3
        "Amoxicilina 500mg caja x100 cap | Ibuprofeno 400mg caja x100 tab" → Amoxicilina 500mg x1 | Ibuprofeno 400mg x1
    ✅ No incluyas precios, subtotales ni códigos de producto.
    ✅ Elimina saltos de línea y comillas.
    ✅ Si algún texto contiene pipe (|), reemplázalo por coma (,).

4. Monto Total
    ✅ Extrae exclusivamente el TOTAL FINAL A PAGAR.
    ✅ No uses subtotal ni impuestos individuales.
    ✅ Si hay varias cifras, elige la que esté asociada a:
        1. “Total”
        2. “Importe total”
        3. “Amount due”
        4. “Grand total”
        5. “Total Neto Recibido”
        6. “Gran total”
        7. “Total Final”
    ✅ Convierte al formato español:

    ✅ Usa punto como separador decimal.
    ✅ Usa el coma como separadores de miles.

    Ejemplo:
        1234,56 → 1,234.56
        1234.56 → 1,234.56
        1000000 → 1,000,000

    Si no existe total explícito pero puede calcularse claramente, calcúlalo.

    Si no es posible determinar el total con claridad, responde error.   

5. moneda
    ✅ Determina la moneda siguiendo este orden lógico:
        1. Si aparece EUR o € → euros
        2. Si aparece USD o $ y el país no es Honduras → dólares 
        3. Si aparece LPS o L y el contexto es Honduras → lempiras
        4. Si aparece solo “$”:
        5. Si el proveedor o cliente está en Honduras → lempiras
        6. Si el documento está en inglés y el proveedor no es de Honduras → dólares  
        7. Si el documento está en español y el proveedor es de Honduras → lempiras 
        7. Si no es determinable con razonable certeza → otros
        8. No inventes moneda.

6. Formato del nombre del cliente
    ✅ Devuelve el nombre en formato capitalizado:
        1. Primera letra de cada palabra en mayúscula
        2. Resto en minúscula

    ✅ Ejemplo:
        “MARIA GONZÁLEZ S.A.” → Maria González S.A.
        “empresa comercial del norte” → Empresa Comercial Del Norte

    ✅ No incluyas dirección ni información adicional.


7. RTN del cliente

    ✅ Extrae el RTN únicamente si está explícitamente identificado como RTN del cliente.

    ✅ No asumas que un número es RTN si no está claramente etiquetado.

    ✅ No confundas con el RTN del proveedor.

    ✅ Si no aparece o no puede determinarse con claridad, deja el campo vacío.

8. Tipo Factura:
    ✅ Clasifica cada factura aplicando estrictamente las siguientes reglas en este orden:
        
        Regla 1 — Ingresos

            Clasifica como "Ingresos" únicamente si se cumplen simultáneamente estas dos condiciones:

                1. El texto del documento contiene explícitamente la frase:

                    - “Recibo por honorarios profesionales”

                2. El RTN asociado al documento, identificado junto al CAI o como RTN del emisor, es exactamente:

                    - {RTN_PRINCIPAL}

            Ambas condiciones deben cumplirse al mismo tiempo.
            Si falta una de ellas, no clasifiques como Ingresos.     


        Regla 2 — Gastos

            Clasifica como "Gastos" cuando:

            - El proveedor NO corresponde a {NOMBRE_PRINCIPAL}
                Y
            - El RTN del proveedor NO es {RTN_PRINCIPAL}


        Regla 3 — Prioridad

            - Primero evalúa si cumple condiciones de Ingresos.

            - Si no cumple, evalúa condiciones de Gastos.

            - Si ninguna condición puede determinarse con claridad, clasifica como "Gastos".

            - No inventes clasificaciones.   

9. numero_factura

    ✅ Extrae el número de factura si aparece en el documento.

    ✅ Debe cumplir un formato similar a:

                000-001-01-00017044

    ✅ Es decir:

        - Tres bloques numéricos separados por guiones.

        - Estructura esperada: 3 dígitos - 3 dígitos - 2 dígitos - 8 dígitos.

    ✅ Expresión estructural de referencia:

        Formato válido:  XXX-XXX-XX-XXXXXXXX

    ✅ No extraigas:

        - CAI
        - RTN
        - Número de pedido
        - Número de orden de compra
        - Número de autorización

    ✅ Si existen varios números similares:

        - Prioriza el que esté identificado como:

            - "Factura No"
            - "Número de factura"
            - "Factura"
            - "N° XXX-XXX-XX-XXXXXXXX (Seguido del numero de factura N° XXX-XXX-XX-XXXXXXXX, ejemplo: N° 000-001-01-00017044)"
            - "No. Factura"
            - Devuélvelo respetando el formato XXX-XXX-XX-XXXXXXXX
            - Si no se encuentra un número con ese patrón, deja el campo vacío.


10. categoria

    ✅ Clasifica el gasto en una categoría basándote en el proveedor Y los productos comprados.
    ✅ Usa el proveedor como primera señal de clasificación. Si el proveedor es reconocible, clasifica directamente.
    ✅ Si el proveedor no es suficiente, analiza los productos para determinar la categoría.
    ✅ Devuelve la categoría en español, en minúsculas y sin acentos.

    📌 Categorías disponibles y criterios:

        supermercado
            - Proveedores: Walmart, La Colonia, El Rey, Supermercados, etc.
            - Productos: alimentos, bebidas, artículos de limpieza, productos del hogar

        ferreteria
            - Proveedores: Ferretería, Homex, EPA, etc.
            - Productos: cemento, varillas, pintura, tornillos, tuberías, herramientas, madera

        farmacia
            - Proveedores: Farmacia, Droguería, etc.
            - Productos: medicamentos, vitaminas, insumos médicos, jeringas, guantes

        tecnologia
            - Proveedores: Office Depot, Dell, HP, Apple, Samsung, tiendas de tecnología
            - Productos: computadoras, monitores, impresoras, cables, accesorios tecnológicos

        servicios_profesionales
            - Proveedores: contadores, abogados, consultores, honorarios profesionales
            - Productos/servicios: consultoría, asesoría, honorarios, servicios legales

        salud
            - Proveedores: clínicas, hospitales, laboratorios, dentistas, médicos
            - Productos/servicios: consultas, procedimientos médicos, exámenes

        restaurante_alimentos
            - Proveedores: restaurantes, panaderías, reposterías, cafeterías
            - Productos: pan, pasteles, comida preparada, repostería

        agropecuario
            - Proveedores: agropecuarias, veterinarias
            - Productos: semillas, fertilizantes, herbicidas, fumigadoras, insumos agrícolas

        muebles_decoracion
            - Proveedores: mueblerías, decoraciones, tiendas de muebles
            - Productos: muebles, sillas, mesas, closets, decoración del hogar

        papeleria_oficina
            - Proveedores: librerías, papelerías, Office Depot
            - Productos: papel, lapiceros, cuadernos, calculadoras, mochilas, folders

        servicios_basicos
            - Proveedores: ENEE, SANAA, Hondutel, empresas de telecomunicaciones
            - Productos/servicios: electricidad, agua, internet, telefonía

        combustible_transporte
            - Proveedores: gasolineras, talleres, empresas de transporte
            - Productos/servicios: gasolina, diesel, mantenimiento vehicular, transporte

        software_suscripciones
            - Proveedores: Amazon, Google, Microsoft, Adobe, Netflix, servicios digitales
            - Productos/servicios: suscripciones, licencias, servicios en la nube

        reparaciones_mantenimiento
            - Proveedores: talleres, técnicos, servicios de reparación
            - Productos/servicios: reparaciones de equipos, mantenimiento, instalaciones

        otros
            - Cuando no sea posible determinar la categoría con razonable certeza.
            - No inventes categorías fuera de esta lista.


📌 Formato de salida obligatorio

✅ Siempre incluye exactamente esta cabecera como primera línea (sin repetirla):

    fecha_factura;numero_factura;proveedor;rtn_proveedor;direccion_proveedor;telefono_proveedor;pais_proveedor;nombre_cliente;rtn_cliente;concepto;monto_total;moneda;tipo_factura;categoria

✅ Después, genera una línea por cada factura detectada, sin líneas vacías.

✅ No agregues texto adicional antes o después del CSV.



📌 Ejemplo de salida válida

fecha_factura;numero_factura;proveedor;rtn_proveedor;direccion_proveedor;telefono_proveedor;pais_proveedor;nombre_cliente;rtn_cliente;concepto;monto_total;moneda;tipo_factura;categoria
15/01/2024;000-001-01-00017044;Ana;080119750004;;;Honduras;Empresa Comercial Del Norte;;Servicios contables x1;8,500.00;lempiras;Ingresos;servicios_profesionales
20/01/2024;000-002-01-00004567;Supermercado La Colonia;08011999000001;;;Honduras;Jorge Trochez;;Arroz 50lb x1 | Frijoles 25lb x1 | Aceite 1L x1;1,250.50;lempiras;Gastos;supermercado
05/02/2024;;Amazon Services Europe Sarl;;;;Irlanda;Jorge Trochez;;Suscripcion software x1;19.99;euros;Gastos;software_suscripciones

📌 **Instrucciones finales**:
- Devuelve solo el CSV limpio, sin repeticiones de encabezado ni líneas vacías.
- **Si no puedes extraer datos, responde exactamente con `"error"` sin comillas**.
"""


