@echo off
echo ====================================
echo  Sistema de Digitalizacion Facturas
echo ====================================

:: ── Verificar si ya está todo instalado ──────────────────────
if exist ".installed" (
    echo El sistema ya esta instalado. Iniciando...
    goto :iniciar
)

:: ── Verificar Python ─────────────────────────────────────────
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no encontrado. Descargando e instalando...
    curl -o "%TEMP%\python_installer.exe" https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%TEMP%\python_installer.exe"
    echo Python instalado correctamente.
) else (
    echo Python ya esta instalado.
)

:: ── Verificar ODBC SQLite ────────────────────────────────────
echo Verificando SQLite ODBC Driver...
reg query "HKLM\SOFTWARE\ODBC\ODBCINST.INI\SQLite3 ODBC Driver" >nul 2>&1
if errorlevel 1 (
    echo SQLite ODBC Driver no encontrado. Descargando e instalando...
    curl -o "%TEMP%\sqliteodbc.exe" http://www.ch-werner.de/sqliteodbc/sqliteodbc_w64.exe
    "%TEMP%\sqliteodbc.exe" /S
    del "%TEMP%\sqliteodbc.exe"
    echo SQLite ODBC Driver instalado correctamente.
) else (
    echo SQLite ODBC Driver ya esta instalado.
)

:: ── Crear entorno virtual ────────────────────────────────────
echo Creando entorno virtual...
if not exist ".venv" (
    python -m venv .venv
    echo Entorno virtual creado.
) else (
    echo Entorno virtual ya existe.
)

:: ── Instalar dependencias ────────────────────────────────────
echo Instalando dependencias...
call .venv\Scripts\activate
pip install -r requirements.txt

:: ── Marcar como instalado ────────────────────────────────────
echo instalado > .installed
echo.
echo ====================================
echo  Instalacion completada exitosamente
echo ====================================

:iniciar
echo Iniciando sistema...
call .venv\Scripts\activate
start "" http://localhost:8501
streamlit run pages\app.py

pause
```

Lo que hace este script:
```
Primera ejecución:
  → Verifica Python    → instala si no existe
  → Verifica ODBC      → instala si no existe  
  → Crea .venv         → solo si no existe
  → Instala librerías  → desde requirements.txt
  → Crea archivo .installed como bandera
  → Inicia la app

Ejecuciones siguientes:
  → Detecta .installed → salta todo
  → Inicia la app directamente


