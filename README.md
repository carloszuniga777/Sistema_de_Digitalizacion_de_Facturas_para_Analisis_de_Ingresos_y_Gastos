# 🧾 Sistema de Digitalización de Facturas

> Sistema automatizado para la extracción, estructuración y análisis de facturas mediante OCR e Inteligencia Artificial.

---

## 📌 Introducción

Es un sistema **ETL** (Extract, Transform, Load) y visualizacion de datos desarrollado en Python que automatiza la digitalización de facturas a partir de imágenes y documentos PDF. Utiliza **PaddleOCR** y **PyMuPDF** para la extracción de texto, Inteligencia Artificial  **Google Gemini** para estructurar e interpretar la información, y **SQLite** como base de datos local. Los datos procesados se visualizan a través de una interfaz web construida con **Streamlit** y un dashboard analítico en **Power BI**.

El sistema soporta facturas escaneadas, fotografiadas y archivos PDF, y permite al usuario revisar, corregir, exportar y analizar la información de sus ingresos y gastos desde una sola plataforma.

---

## 🧩 Problemática y Origen

Este proyecto nació de una necesidad real: mi hermana trabaja de manera independiente junto a su esposo y cada año debe declarar impuestos, lo que implica recopilar y registrar manualmente todas las facturas de compras, gastos e ingresos acumuladas durante el año.

El proceso le tomaba una cantidad considerable de tiempo, ya que debía transcribir uno a uno los datos de decenas de documentos físicos y digitales hacia una hoja de Excel. Un trabajo tedioso, propenso a errores y difícil de escalar a medida que el volumen de documentos crecía.

A partir de esa situación surgió la idea de crear un sistema capaz de leer automáticamente esos documentos y extraer la información relevante de cada factura, eliminando la necesidad de hacerlo de forma manual y permitiéndole enfocarse en el análisis y no en la captura de datos.

---

## ✅ Resultado

Gracias a este sistema, el proceso de digitalización de facturas pasó de ser una tarea manual de horas a un proceso automatizado de minutos. El sistema es capaz de:

- Leer y extraer información de facturas en imagen o PDF sin intervención manual
- Clasificar automáticamente cada factura por categoría, tipo (gasto o ingreso), proveedor, monto y fecha
- Permitir revisiones y correcciones desde una interfaz amigable antes de guardar
- Generar un resumen visual de ingresos y gastos por mes, proveedor y categoría
- Exportar los datos procesados a Excel listo para declaración de impuestos

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| **Python** | Lenguaje principal del sistema |
| **PaddleOCR** | Extracción de texto desde imágenes (facturas fotografiadas o escaneadas) |
| **PyMuPDF** | Extracción de texto desde archivos PDF |
| **Gemini API** | Estructuración e interpretación de la información extraída mediante IA |
| **SQLite** | Almacenamiento local de las facturas procesadas |
| **Streamlit** | Interfaz web para procesamiento, revisión y visualización |
| **Pandas** | Manipulación y transformación de datos |
| **Plotly** | Gráficos interactivos dentro del dashboard de Streamlit |
| **Power BI** | Dashboard analítico avanzado conectado a la base de datos |


---

## ⚙️ Funcionamiento

```
facturas/
  └── imagen.jpg / documento.pdf
         │
         ▼
   PaddleOCR / PyMuPDF
   (extracción de texto)
         │
         ▼
   Gemini API
   (estructuración: proveedor, monto, fecha, categoría...)
         │
         ▼
   SQLite
   (almacenamiento)
         │
         ▼
   Streamlit / Power BI
   (visualización y análisis)
```

1. El usuario coloca las facturas (imágenes o PDFs) en la carpeta `facturas/`
2. Desde la interfaz web, presiona **"Procesar Facturas"**
3. El sistema extrae y estructura la información automáticamente
4. El usuario revisa y corrige los datos en la tabla editable
5. Guarda los cambios en la base de datos
6. Visualiza el resumen en el Dashboard o en Power BI

---

## 📖 Guía de Usuario

### Primera vez (PC nueva)

1. Descarga o clona este repositorio: 
`https://github.com/carloszuniga777/Sistema_de_Digitalizacion_de_Facturas_para_Analisis_de_Ingresos_y_Gastos.git`
2. Ejecuta el archivo **`Sistema Digitalizacion Facturas.bat`** haciendo doble clic
3. El script instalará automáticamente Python y las dependencias necesarias.
4. Al finalizar, se abrirá el navegador con el sistema listo para usar

> ⚠️ Se requiere conexión a internet en la primera ejecución para descargar Python y las dependencias.

### Ejecuciones siguientes

Solo ejecuta nuevamente **`Sistema Digitalizacion Facturas.bat`**. El sistema detecta que ya está instalado y abre la aplicación directamente.

### Pantalla de Facturas

- Primero coloca tus facturas (imágenes JPG/PNG o archivos PDF) en la carpeta `facturas/`
- Presiona **"🚀 Procesar Facturas"** para iniciar la extracción automática (puede tomar varios minutos)
- Revisa los datos en la tabla editable y realiza correcciones si es necesario
- Presiona **"💾 Guardar cambios"** y confirma para guardar en la base de datos

### Pantalla de Dashboard

- Filtra por tipo de factura (Gastos / Ingresos) y por año
- Visualiza el resumen de montos por mes, top proveedores y categorías
- Descarga los datos del año seleccionado en formato Excel con el botón **"⬇️ Descargar"**

---
## Instalación y configuración de Power BI (Opcional)

Power BI Desktop es la herramienta de Microsoft para visualización y análisis de datos. 
Es completamente gratuita y permite conectarse a múltiples fuentes de datos incluyendo SQLite.

**Descarga e instalación:**

1. Ve a [powerbi.microsoft.com](https://powerbi.microsoft.com/es-es/desktop/)
2. Haz clic en **"Descargar gratis"**
3. Ejecuta el instalador y sigue el asistente con las opciones por defecto
4. Al abrir Power BI por primera vez te pedirá iniciar sesión con una cuenta Microsoft (opcional para uso local)

> 💡 Power BI Desktop es gratuito para uso local. Solo se requiere licencia de pago para publicar reportes en la nube (Power BI Service).


### Conexión con SQLite mediante ODBC

ODBC es el puente que permite a Power BI leer la información almacenada en la base de datos SQLite del sistema. Sin este paso, Power BI no puede acceder al archivo `.db`.

> Guía paso a paso para conectar una base de datos SQLite a Power BI Desktop utilizando un driver ODBC de 64 bits.

**¿Por qué usar ODBC?**

ODBC (Open Database Connectivity) es el método recomendado para conectar SQLite a Power BI en entornos de producción porque:

- No depende de lenguajes adicionales como Python.
- Permite actualizaciones automáticas de datos desde el archivo `.db`.
- Se configura **una sola vez** en Windows y queda disponible permanentemente.
- Es compatible con Power BI Gateway para actualizaciones en la nube.

<br>

#### Paso 1 — Instalar el driver ODBC para SQLite

<br>

**¿Para qué sirve?**  
Power BI no incluye soporte nativo para SQLite. Este paso instala el "puente" (driver) que le permite a Windows comunicarse con archivos `.db`.

**Fuentes de descarga confiables:**

| Fuente | URL | Notas |
|--------|-----|-------|
| Autor original (Christian Werner) | http://www.ch-werner.de/sqliteodbc/ | Gratuito y open source. Usa HTTP, descarga en red de confianza |
| GitHub (código fuente verificable) | https://github.com/softace/sqliteodbc | Recomendado por transparencia |


**¿Qué archivo descargar?**

```
sqliteodbc_w64.exe   ←  para sistemas Windows de 64 bits
```

> 💡 El driver es desarrollado por Christian Werner y es ampliamente utilizado 
> en entornos profesionales para conectar SQLite con herramientas como Power BI y Excel.

**Instalación:**

1. Ejecuta el archivo `sqliteodbc_w64.exe`.
2. Sigue el asistente y acepta las opciones por defecto.
3. El driver quedará registrado automáticamente en Windows.

> 💡 Esta instalación se realiza **una sola vez**. No es necesario repetirla a menos que reinstales Windows o cambies de computadora.

<br>

#### Paso 2 — Crear un DSN en el Administrador ODBC de Windows

<br>


**¿Para qué sirve?**  
Un DSN (Data Source Name) es un nombre de referencia que le dice a Windows dónde está tu archivo `.db` y con qué driver abrirlo. Power BI usará este nombre para conectarse. Solo debes crearlo una vez.

**Instrucciones:**

1. Presiona `Windows + S` y busca: `ODBC`
2. Abre **"Orígenes de datos ODBC (64 bits)"** ← importante que sea la versión de 64 bits.
3. Ve a la pestaña **"DSN de sistema"** (disponible para todos los usuarios del equipo).
4. Haz clic en **"Agregar..."**.
5. Selecciona **SQLite3 ODBC Driver** de la lista y haz clic en Finalizar.
6. Completa los campos:
   - **Data Source Name:** Un nombre descriptivo sin espacios, por ejemplo: `MiBaseSQLite`
   - **Database Name:** Haz clic en **Browse** y navega hasta tu archivo `.db`
7. Haz clic en **OK**.

> 💡 Si en el futuro mueves o renombras tu archivo `.db`, vuelve aquí y actualiza la ruta en el campo **Database Name**. En cualquier otro caso, no necesitas repetir este paso.

<br>

#### Paso 3 — Conectar Power BI al origen de datos ODBC

<br>

**¿Para qué sirve?**  
Se le indica a Power BI qué origen de datos usar para importar las tablas de tu base de datos SQLite.

**Instrucciones:**

1. Abre **Power BI Desktop**.
2. Haz clic en **"Obtener datos"**.
3. Busca **ODBC** y selecciónalo. Haz clic en Conectar.
4. En el menú desplegable, elige el DSN que creaste (por ejemplo: `MiBaseSQLite`).
5. Haz clic en **Conectar**.


<br>

#### Paso 4 — Ingresar credenciales (usuario ficticio)

<br>

**¿Para qué sirve?**  
El protocolo ODBC solicita usuario y contraseña de forma estándar, incluso para bases de datos que no usan autenticación. SQLite no tiene sistema de usuarios, por lo que Power BI ignorará los valores ingresados — pero requiere que el campo no esté vacío.

**Qué ingresar:**

| Campo | Valor |
|-------|-------|
| Usuario | Cualquier texto, por ejemplo: `admin` |
| Contraseña | Dejar en blanco |

1. Escribe `admin` (o cualquier palabra) en el campo **Usuario**.
2. Deja el campo **Contraseña** en blanco.
3. Haz clic en **Conectar**.

> 💡 SQLite es un archivo de base de datos local y no implementa autenticación. El valor ingresado es completamente ignorado por el sistema.



<br>

#### Paso 5 — Seleccionar tablas y cargar los datos

<br>

**¿Para qué sirve?**  
Power BI muestra todas las tablas disponibles en tu base de datos. Aquí eliges cuáles importar al modelo de datos para construir reportes y visualizaciones.

**Instrucciones:**

1. Aparecerá el **Navegador** con la lista de tablas de tu base de datos.
2. Marca el checkbox de cada tabla que deseas importar.
3. Si necesitas transformar los datos antes de cargarlos, haz clic en **Transformar datos** para abrir Power Query.
4. Si los datos están listos, haz clic en **Cargar**.

> 💡 Puedes seleccionar varias tablas a la vez. Power BI las importará como tablas separadas en el modelo de datos, desde donde podrás crear relaciones entre ellas.

<br>

#### Resumen de frecuencia

<br>

| # | Paso | ¿Cada cuánto? | Excepción |
|---|------|---------------|-----------|
| 1 | Instalar driver ODBC | Una sola vez | Reinstalación de Windows o cambio de PC |
| 2 | Crear DSN en Windows | Una sola vez | Si mueves o renombras el archivo `.db` |
| 3 | Conectar en Power BI | Una vez por reporte | Nuevo reporte o nueva computadora |
| 4 | Ingresar usuario ficticio | Una vez por conexión | No aplica |
| 5 | Seleccionar tablas y cargar | Una vez (o al agregar tablas nuevas) | Nuevas tablas en la base de datos |


<br>

*Una vez completados los 5 pasos, Power BI estará conectado a tu base de datos SQLite y los datos se actualizarán automáticamente cada vez que abras el reporte.*

---
## 📁 Estructura de Carpetas

```
Sistema_Digitalización_Facturas/
│
├── facturas/                   # Carpeta donde se colocan las facturas a procesar
├── logs/                       # Registros de ejecución del sistema
├── pages/
│   ├── 1_🧾_Facturas.py        # Pantalla de procesamiento y edición
│   └── 2_📊_Dashboard.py       # Pantalla de análisis y descarga
├── powerbi/                     
│    ├── media                   # imagenes
│    └── Dashboard.pbix          # Archivo de Power BI
├── src/
│   ├── database/
│   │   ├── facturas.db         # Base de datos SQLite
│   │   └── repository.py       # Interacción con la base de datos
│   ├── ia/
│   │   └── processor.py        # Estructuración con Gemini
│   ├── ocr/
│   │   └── extractor.py        # Extracción PDF e imagenes con el OCR principal
│   │  
│   └── utils/
│       ├── data_transformer.py # Transformación de datos de formato csv a dataframe
│       ├── file_manager.py     # Manejo de archivos y carpetas
│       ├── logger.py           # Configuracion del logger para imprimir 
│       ├── prompts.py          # Instrucciones de Geminis 
│       └── clean_ocr.py        # Limpieza de datos del OCR principal
│ 
│ 
│ 
│ 
│ 
├── .env                                  # Variables de entorno 
├── Inicio.py                             # Punto de entrada de Streamlit
├── styles.py                             # Estilos globales de la interfaz
├── main.py                               # Orquestador principal del proceso
├── requirements.txt                      # Lista de dependencias necesarias
├── Sistema Digitalizacion Facturas.bat   # Ejecutable
├── LICENSE                               # Licencias
├── .gitignore                
└── README.md                             # Instrucciones de uso                    
```

---

## 🔧 Instalación Manual (usuarios avanzados)

Si prefieres instalar manualmente sin usar el `.bat`:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/Sistema_Digitalizacion_Facturas.git
cd Sistema_Digitalizacion_Facturas

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Modifica el archivo .env_template: Del nombre del archivo borra _template para que quede como .env 
# Agrega tu API Key de Gemini:

#     GEMINI_API_KEY=tu_api_key_aqui
#     RTN_PRINCIPAL = "Tu_RTN_aqui"
#     NOMBRE_PRINCIPAL = "Tu_Nombre_aqui" 


# 5. Ejecutar la aplicación
streamlit run Inicio.py
```

---



## 📄 Licencia

Este proyecto está bajo la licencia **Apache 2.0**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

*Desarrollado por Carlos Zuniga — Portfolio de Data Analytics*