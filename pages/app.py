import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import subprocess
import sys


# ──────────────────── Configuración de página ────────────────────────

st.set_page_config(
    page_title="Sistema de Facturas",
    page_icon="🧾",
    layout="wide"
)



# ──────────────────── Estilos CSS ───────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 50%, #f5f0ff 100%);
        font-family: 'DM Sans', sans-serif;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #9333ea 0%, #a855f7 50%, #9333ea 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.25);
    }
    .main-header h1 {
        color: #ffffff;
        font-family: 'DM Sans', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .main-header p {
        color: #f3e8ff;
        font-size: 0.9rem;
        margin: 6px 0 0 0;
        font-weight: 300;
    }
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }        



    /* Métricas */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(99, 102, 241, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1a1f3a;
        font-family: 'DM Mono', monospace;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }
    
    /* Grid de métricas responsive */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        margin-bottom: 8px;
    }        


    /* Sección tabla */
    .table-section {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        border: 1px solid rgba(99, 102, 241, 0.08);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }

    /* Tabla */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stDataEditor"] {
        border-radius: 10px;
    }
     
            

    /*------Botones-----*/        
            
    /* Botón guardar */
    .stButton > button {
        background: #0d6efd !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 28px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: none !important;
        transition: background 0.2s ease !important;
        width: auto !important;        /* ← ya no ocupa todo el ancho */
        white-space: nowrap !important; /* ← evita que el texto se parta */
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    .stButton > button:hover {
        background: #0b5ed7 !important;
        box-shadow: none !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
            
    /*Estilo boton de confirmacion de la modal*/
    [data-testid="stDialog"] .stButton button[kind="primary"] {
        background: #157347 !important;
        color: #ffffff !important;
    }

    /*Estilo boton de cancelar de la modal*/
    [data-testid="stDialog"] .stButton button[kind="secondary"] {
        background: #ffc107 !important;
        color: #000000 !important;
        border: none !important;
    }       
     
     /*Estilo boton procesar*/       
    .btn-procesar {
        background: white !important;
        color: #9333ea !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        transition: background 0.2s !important;
    }
    .btn-procesar:hover {
        background: #f3e8ff !important;
    }         



    /* Success */
    .stSuccess {
        border-radius: 10px !important;
        border-left: 4px solid #22c55e !important;
    }
             

    /* Ocultar elementos por defecto de streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Scrollbar bonito */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
    ::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #6366f1; }
            

    /* ──────────────────── RESPONSIVE ──────────────────────── */

    /* Monitor grande (>1400px) */
    @media (min-width: 1400px) {
        .main-header h1 { font-size: 2rem; }
        .metric-value   { font-size: 1.8rem; }
    }

    /* Laptop (1024px - 1400px) → ya funciona bien, ajustes menores */
    @media (max-width: 1400px) {
        .main-header { padding: 24px 28px; }
        .metric-value { font-size: 1.4rem; }
    }

    /* Tablet (768px - 1024px) */
    @media (max-width: 1024px) {
        .main-header { padding: 20px 22px; }
        .main-header h1 { font-size: 1.4rem; }
        .main-header p  { font-size: 0.82rem; }
        .metric-card    { padding: 16px 14px; }
        .metric-value   { font-size: 1.2rem; }
        .metric-label   { font-size: 0.68rem; }
        .table-section  { padding: 18px 14px; }
    }

    /* Tablet pequeña (600px - 768px) */
    @media (max-width: 768px) {
        .main-header { padding: 16px 18px; border-radius: 12px; }
        .main-header h1 { font-size: 1.6rem; }
        .main-header p  { font-size: 1.1rem; }
        .metric-card    { padding: 14px 10px; border-radius: 10px; }
        .metric-value   { font-size: 1.1rem; }
        .metric-label   { font-size: 0.65rem; letter-spacing: 0.4px; }
        .table-section  { padding: 14px 10px; border-radius: 12px; }
        .section-title  { font-size: 0.78rem; }

        /* Botón más compacto */
        .stButton > button {
            padding: 10px 20px !important;
            font-size: 0.82rem !important;
            border-radius: 8px !important;
        }
    }

    /* Celular (< 600px) */
    @media (max-width: 600px) {
        .main-header { padding: 14px 16px; border-radius: 10px; }
        .main-header h1 { font-size: 1.2rem; letter-spacing: 0px; }
        .main-header p  { font-size: 0.9rem; margin-top: 4px; }
        .metric-card    { padding: 12px 8px; border-radius: 8px; }
        .metric-value   { font-size: 0.95rem; }
        .metric-label   { font-size: 0.6rem; letter-spacing: 0.2px; }
        .table-section  { padding: 12px 8px; border-radius: 10px; }

        /* Botón full width en celular */
        .stButton > button {
            padding: 10px 16px !important;
            font-size: 0.8rem !important;
            border-radius: 8px !important;
            width: 100% !important;
        }
    }
            
    /* ---------- Métricas ----------- */
    
    /* Laptop (max 1200px) → 3 arriba, 2 abajo ocupando todo */
    @media (max-width: 1200px) {
        .metrics-grid {
            grid-template-columns: repeat(6, 1fr);
        }
        .metrics-grid .metric-card:nth-child(1) { grid-column: span 2; }
        .metrics-grid .metric-card:nth-child(2) { grid-column: span 2; }
        .metrics-grid .metric-card:nth-child(3) { grid-column: span 2; }
        .metrics-grid .metric-card:nth-child(4) { grid-column: span 3; } /* mitad */
        .metrics-grid .metric-card:nth-child(5) { grid-column: span 3; } /* mitad */
    }

    /* Tablet (max 768px) → 2 columnas, última ocupa todo */
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .metrics-grid .metric-card:nth-child(1) { grid-column: span 1; }
        .metrics-grid .metric-card:nth-child(2) { grid-column: span 1; }
        .metrics-grid .metric-card:nth-child(3) { grid-column: span 1; }
        .metrics-grid .metric-card:nth-child(4) { grid-column: span 1; }
        .metrics-grid .metric-card:nth-child(5) { grid-column: span 2; } /* ocupa todo */
    }

    /* Celular (max 480px) → 1 columna, todas verticales */
    @media (max-width: 480px) {
        .main-header h1 { text-align: center !important; }
        .main-header p  { text-align: center !important; }    
        .metrics-grid {
            grid-template-columns: 1fr;
            gap: 8px;
        }
        .metrics-grid .metric-card:nth-child(n) { grid-column: span 1; }
        .metric-card  { padding: 14px 10px; }
        .metric-value { font-size: 1rem; }
        .metric-label { font-size: 0.62rem; }
    }
  
   /*Header y boton procesar*/
   @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            align-items: stretc;
        }
        .btn-procesar {
            width: 100%;
            text-align: center !important;
            box-sizing: border-box !important;
        }
    }

    
    }                        
            
</style>
""", 
unsafe_allow_html=True)


# ──────────────────── Ruta del archivo main.py ─────────────────────────────────

MAIN_PY = Path(__file__).parent.parent / "src" / "main.py"              # Archivo principal: main
ROOT_DIR = Path(__file__).parent.parent                                 # ← raíz del proyecto

# ────────────────────── Header ──────────────────────────────

st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div>
                <h1>🧾 Sistema de Digitalización de Facturas</h1>
                <p>Visualiza, edita y gestiona todas las facturas procesadas</p>
            </div>
            <a href="?procesar=1" target="_self">
                <button class="btn-procesar">🚀 Procesar Facturas</button>
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)


#-- Logica del boton procesar facturas: ejecuta el script de python 

#  Detectar si se hizo clic
if st.query_params.get("procesar") == "1":
    st.query_params.clear()
    with st.spinner("⏳ Procesando facturas..."):
        resultado = subprocess.run(
            [sys.executable, str(MAIN_PY)],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR)                       # ← ejecuta desde la raíz
        )
    if resultado.returncode == 0:
        st.success("✅ Facturas procesadas correctamente")
        st.rerun()
    else:
        st.error(f"❌ Error:\n{resultado.stderr}")




# ──────────────────── Ruta de la Base de datos ─────────────────────────────────

SQLITE_DB = Path(__file__).parent.parent / "src" / "database" / "facturas.db"


# ──────────────────── Estados del Modal ──────────────────────────────────────── 
# Al inicio del archivo, inicializa el estado

# Estado mensaje de guardado exitoso
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False


# Estado del modal abrir/cerrar modal
if "abrir_dialog" not in st.session_state:
    st.session_state.abrir_dialog = False



# ─────────────── Dialog (debe definirse ANTES de usarse) ────────

@st.dialog("⚠️ ¿Guardar cambios?")
def abrir_modal(df):
    st.markdown("Esta acción sobreescribirá los datos en la base de datos.")
    st.markdown("<br>", unsafe_allow_html=True)


    #-------------Botones----------------    
    
    col_cancel, col_confirm = st.columns(2, gap="small")

    # Boton cancelar
    with col_cancel:
        if st.button("❌ Cancelar", use_container_width=True, type="secondary"):
            st.rerun()

    # Boton confirmar
    with col_confirm:
        if st.button("✅ Confirmar", use_container_width=True, type="primary"):
            guardarCambios(df)
            st.session_state.guardado_exitoso = True
            st.rerun()



def guardarCambios(df):
    df_guardar = df.copy()                                                                     # Crea una copia de dataframe de la tabla
    
    fechas = df_guardar["fecha_factura"]
    
     # Actualizar campos derivados de la fecha
    df_guardar["fecha_factura"] = fechas.dt.strftime("%Y-%m-%d %H:%M:%S")
    df_guardar["dia_factura"]   = fechas.dt.day.astype(str)
    df_guardar["mes_factura"]   = fechas.dt.month.astype(str)
    df_guardar["ano_factura"]   = fechas.dt.year.astype(str)

    with sqlite3.connect(SQLITE_DB) as conn:
        df_guardar.to_sql("tbl_facturas", conn, if_exists="replace", index=False)




#============================================================
#               INICIO DEL PROGRAMA 
#============================================================

# ─────────────── Conexion con la base de datos  ───────────────
with sqlite3.connect(SQLITE_DB) as conn:
    df = pd.read_sql("SELECT * FROM tbl_facturas", conn)
    
    
    
    # ---------------- Métricas ------------------

    total_facturas  = len(df)
    ingresos_total  = df.query("tipo_factura == 'Ingresos'")["monto_total_lempiras"].sum() if "monto_total_lempiras" in df.columns else 0
    gastos_total    = df.query("tipo_factura == 'Gastos'")["monto_total_lempiras"].sum() if "monto_total_lempiras" in df.columns else 0
    cantidad_gastos    = len(df[df["tipo_factura"] == "Gastos"]) if "tipo_factura" in df.columns else 0
    cantidad_ingresos  = len(df[df["tipo_factura"] == "Ingresos"]) if "tipo_factura" in df.columns else 0

    metricas = [
        (str(total_facturas),            "Total Facturas"),
        (f"L. {ingresos_total:,.0f}",    "Ingresos Total"),
        (f"L. {gastos_total:,.0f}",      "Gastos Total"),
        (str(cantidad_gastos),           "Gastos"),
        (str(cantidad_ingresos),         "Ingresos"),
    ]



    st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_facturas}</div>
                <div class="metric-label">Total Facturas</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">L. {ingresos_total:,.0f}</div>
                <div class="metric-label">Ingresos Total</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">L. {gastos_total:,.0f}</div>
                <div class="metric-label">Gastos Total</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{cantidad_gastos}</div>
                <div class="metric-label">Gastos</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{cantidad_ingresos}</div>
                <div class="metric-label">Ingresos</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


     


    # ------------------- Tabla editable y filtros ---------------------

    st.markdown('<div class="section-title">📋 Facturas Procesadas</div>', unsafe_allow_html=True)

    # Convertir fecha_factura a datetime para mostrar el calendario
    df["fecha_factura"] = pd.to_datetime(df["fecha_factura"], format="%Y-%m-%d %H:%M:%S", errors="coerce")



    # --- Filtros de la tabla ---
    _, col_f1, col_f2, col_f3, _ = st.columns([1, 1, 1, 2, 1], gap="small")

    with col_f1:
        anos_disponibles = sorted(df["ano_factura"].dropna().unique().tolist(), reverse=True)
        ano_seleccionado = st.selectbox("📅 Año", options=["Todos"] + anos_disponibles)

    with col_f2:
        tipo_seleccionado = st.selectbox("🏷️ Tipo", options=["Todos", "Gastos", "Ingresos"])

    with col_f3:
        busqueda = st.text_input("🔍 Buscar", placeholder="Buscar en tabla...")    


    # --- Aplicar filtros ---
    df_filtrado = df.copy()
     
     # Filtro ano
    if ano_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["ano_factura"] == ano_seleccionado]

    # filtro tipo de factura
    if tipo_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo_factura"] == tipo_seleccionado]

    # filtro busqueda    
    if busqueda:
        mask = df_filtrado.apply(
            lambda col: col.astype(str).str.contains(busqueda, case=False, na=False)
        ).any(axis=1)

        df_filtrado = df_filtrado[mask]
    

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)



    # ------ Tabla ----------
    df_editado = st.data_editor(
        df_filtrado,
        use_container_width=True,      # ← ocupa todo el ancho
        hide_index=True,
        num_rows="dynamic",
        
        column_order=[
            "fecha_factura",
            "numero_factura",
            "proveedor",
            "rtn_proveedor",
            "nombre_cliente",
            "concepto",
            "monto_total",
            "moneda",
            "monto_total_lempiras",
            "tipo_factura",
            "categoria",
        ],

        column_config={
            "fecha_factura":        st.column_config.DateColumn("Fecha Factura", width="medium"),
            "numero_factura":       st.column_config.TextColumn("N° Factura",    width="medium"),
            "proveedor":            st.column_config.TextColumn("Proveedor",     width="large"),
            "rtn_proveedor":        st.column_config.TextColumn("RTN Proveedor", width="medium"),
            "nombre_cliente":       st.column_config.TextColumn("Cliente",       width="large"),
            "concepto":             st.column_config.TextColumn("Concepto",      width="large"),
            "monto_total":          st.column_config.NumberColumn("Monto",       format="%.2f"),
            "moneda":               st.column_config.SelectboxColumn("Moneda",        options=["lempiras", "dólares", "euros"],  width="small"),
            "monto_total_lempiras": st.column_config.NumberColumn("Monto (L)",   format="L. %.2f"),
            "tipo_factura":         st.column_config.SelectboxColumn("Tipo",     options=["Gastos", "Ingresos"], width="small"),
            "categoria":            st.column_config.SelectboxColumn("Categoría",     options=["supermercado", "ferreteria", "farmacia", "tecnologia", "servicios_profesionales", "salud", "restaurante_alimentos", "agropecuario", "muebles_decoracion", "papeleria_oficina", "servicios_basicos", "combustible_transporte", "software_suscripciones", "reparaciones_mantenimiento",  "otros"], width="medium"),
        }
    )

    st.markdown('</div>', unsafe_allow_html=True)



    # ------- Botón guardar -----------
    _, col_btn, _ = st.columns([2, 1, 2])
    
    with col_btn:
        if st.button("💾 Guardar cambios"):
            abrir_modal(df_editado)            # Abre la modal
             
    
# ------ Mensaje de éxito ----------
if st.session_state.get("guardado_exitoso", False):
    st.success("✅ Cambios guardados correctamente")
    st.session_state.guardado_exitoso = False



