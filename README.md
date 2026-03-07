# Sistema de Digitalizacion de Facturas para Analisis de Ingresos y Gastos
Sistema automatizado de digitalización y análisis de facturas desarrollado en Python.  Extrae texto de imágenes y PDFs mediante PyMuPDF y PaddleOCR, estructura la información usando  la API de Gemini y almacena los datos en SQLite y se visualiza en Power Bi para análisis de los ingresos y los gastos. Soporta facturas escaneadas, fotografiadas y documentos PDF



# Conexión SQLite → Power BI mediante ODBC

> Guía paso a paso para conectar una base de datos SQLite a Power BI Desktop utilizando un driver ODBC de 64 bits.

---

## ¿Por qué usar ODBC?

ODBC (Open Database Connectivity) es el método recomendado para conectar SQLite a Power BI en entornos de producción porque:

- No depende de lenguajes adicionales como Python.
- Permite actualizaciones automáticas de datos desde el archivo `.db`.
- Se configura **una sola vez** en Windows y queda disponible permanentemente.
- Es compatible con Power BI Gateway para actualizaciones en la nube.

---

## Paso 1 — Instalar el driver ODBC para SQLite

**¿Para qué sirve?**  
Power BI no incluye soporte nativo para SQLite. Este paso instala el "puente" (driver) que le permite a Windows comunicarse con archivos `.db`.

**Fuentes de descarga confiables:**

| Fuente | URL | Notas |
|--------|-----|-------|
| Autor original (Christian Werner) | http://www.ch-werner.de/sqliteodbc/ | Gratuito y open source. Usa HTTP, descarga en red de confianza |
| GitHub (código fuente verificable) | https://github.com/softace/sqliteodbc | Recomendado por transparencia |
| Devart (opción comercial) | https://www.devart.com/odbc/sqlite/ | HTTPS, versión de prueba gratuita |

**¿Qué archivo descargar?**

```
sqliteodbc_w64.exe   ←  para sistemas Windows de 64 bits
```

> ⚠️ **Seguridad:** Si descargaste desde ch-werner.de, verifica el archivo en [virustotal.com](https://virustotal.com) antes de ejecutarlo.

**Instalación:**

1. Ejecuta el archivo `sqliteodbc_w64.exe`.
2. Sigue el asistente y acepta las opciones por defecto.
3. El driver quedará registrado automáticamente en Windows.

> 💡 Esta instalación se realiza **una sola vez**. No es necesario repetirla a menos que reinstales Windows o cambies de computadora.

---

## Paso 2 — Crear un DSN en el Administrador ODBC de Windows

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

---

## Paso 3 — Conectar Power BI al origen de datos ODBC

**¿Para qué sirve?**  
Se le indica a Power BI qué origen de datos usar para importar las tablas de tu base de datos SQLite.

**Instrucciones:**

1. Abre **Power BI Desktop**.
2. Haz clic en **"Obtener datos"**.
3. Busca **ODBC** y selecciónalo. Haz clic en Conectar.
4. En el menú desplegable, elige el DSN que creaste (por ejemplo: `MiBaseSQLite`).
5. Haz clic en **Conectar**.

---

## Paso 4 — Ingresar credenciales (usuario ficticio)

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

---

## Paso 5 — Seleccionar tablas y cargar los datos

**¿Para qué sirve?**  
Power BI muestra todas las tablas disponibles en tu base de datos. Aquí eliges cuáles importar al modelo de datos para construir reportes y visualizaciones.

**Instrucciones:**

1. Aparecerá el **Navegador** con la lista de tablas de tu base de datos.
2. Marca el checkbox de cada tabla que deseas importar.
3. Si necesitas transformar los datos antes de cargarlos, haz clic en **Transformar datos** para abrir Power Query.
4. Si los datos están listos, haz clic en **Cargar**.

> 💡 Puedes seleccionar varias tablas a la vez. Power BI las importará como tablas separadas en el modelo de datos, desde donde podrás crear relaciones entre ellas.

---

## Resumen de frecuencia

| # | Paso | ¿Cada cuánto? | Excepción |
|---|------|---------------|-----------|
| 1 | Instalar driver ODBC | Una sola vez | Reinstalación de Windows o cambio de PC |
| 2 | Crear DSN en Windows | Una sola vez | Si mueves o renombras el archivo `.db` |
| 3 | Conectar en Power BI | Una vez por reporte | Nuevo reporte o nueva computadora |
| 4 | Ingresar usuario ficticio | Una vez por conexión | No aplica |
| 5 | Seleccionar tablas y cargar | Una vez (o al agregar tablas nuevas) | Nuevas tablas en la base de datos |

---

*Una vez completados los 5 pasos, Power BI estará conectado a tu base de datos SQLite y los datos se actualizarán automáticamente cada vez que abras el reporte.*