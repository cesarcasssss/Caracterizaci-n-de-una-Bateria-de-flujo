"""

  SISTEMA DE CARACTERIZACIÓN DE BATERÍA DE FLUJO
  programador:Cesar Castro Soto ultima version: 1.2 16/06/26

"""

import streamlit as st
import pandas as pd
import os
from datetime import date


# CONFIGURACIÓN GENERAL DE LA PÁGINA

st.set_page_config(
    page_title="Caracterización de Batería de Flujo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ESTILOS CSS PERSONALIZADOS

st.markdown("""
<style>
    /* Importar fuentes distintivas */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* Variables de color — paleta científica oscura con acento ámbar */
    :root 
    {
        --bg-dark:      #0d1117;
        --bg-card:      #161b22;
        --bg-input:     #1c2330;
        --border:       #30363d;
        --accent:       #e6ac2c;
        --accent-light: #f5c842;
        --accent-glow:  rgba(230,172,44,0.15);
        --text-primary: #e6edf3;
        --text-muted:   #8b949e;
        --success:      #3fb950;
        --info:         #58a6ff;
    }

    /* Fondo principal */
    .stApp 
    {
        background-color: var(--bg-dark);
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] 
    {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * 
    {
        color: var(--text-primary) !important;
    }

    /* Tarjetas de sección */
    .card 
    {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
    }

    /* Encabezado principal */
    .main-header 
    {
        font-family: 'Space Mono', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--accent);
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .main-sub 
    {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }

    /* Línea separadora decorativa */
    .divider 
    {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0;
    }

    /* Etiquetas de sección */
    .section-label 
    {
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.8rem;
    }

    /* Métricas personalizadas */
    .metric-box 
    {
        background: var(--accent-glow);
        border: 1px solid var(--accent);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        text-align: center;
    }
    .metric-label 
    {
        font-size: 0.72rem;
        color: var(--text-muted);
        letter-spacing: 1px;
        text-transform: uppercase;
        font-family: 'Space Mono', monospace;
    }
    .metric-value 
    {
        font-family: 'Space Mono', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--accent-light);
    }
    .metric-unit 
    {
        font-size: 0.75rem;
        color: var(--text-muted);
    }

    /* Botón principal */
    .stButton > button 
    {
        background: linear-gradient(135deg, var(--accent), #c89420) !important;
        color: #0d1117 !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton > button:hover 
    {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(230,172,44,0.4) !important;
    }

    /* Tabla de datos */
    .stDataFrame 
    {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    /* Inputs */
    .stNumberInput input, .stTextInput input 
    {
        background-color: var(--bg-input) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }

    /* Alerts */
    .stSuccess 
    {
        background-color: rgba(63,185,80,0.12) !important;
        border-color: var(--success) !important;
    }
    .stInfo 
    {
        background-color: rgba(88,166,255,0.1) !important;
    }

    /* Badge de estado */
    .status-badge 
    {
        display: inline-block;
        background: rgba(63,185,80,0.15);
        color: var(--success);
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid var(--success);
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* Ocultar el menú hamburguesa de Streamlit (opcional) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTE — RUTA DEL ARCHIVO CSV 
# ─────────────────────────────────────────────────────────────────────────────
ARCHIVO_CSV = "registro_bateria_avanzado.csv"


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────


def cargar_datos_existentes() -> pd.DataFrame:
    """
    Carga el historial de mediciones desde el CSV local.
    Si el archivo no existe, devuelve un DataFrame vacío con las columnas correctas.
    """
    columnas = [
      #--------------------------------------------------------------------------------
      #proximas mejoras: viscocidD, PH, EFICIENCIA, etc
      #------------------------------------------------------------------------------
        "Operador", "Laboratorio", "Fecha", "Área (m²)", "RPM", "Par Redox",
        "OCP Inicial (V)", "SCC Inicial (A)",
        "Resistencia (Ω)", "Voltaje (V)", "Corriente (A)",
        "Potencia (W)", "Densidad de Corriente (A/m²)", "Densidad de Potencia (W/m²)",
        "Temperatura (°C)", "pH", "Concentración (mol/L)",
        "Eficiencia Coulómbica (%)", "Eficiencia Energética (%)",
        "Tiempo (s)", "Capacidad (mAh)", "Energía (Wh)",
        "Viscosidad (mPa·s)", "Conductividad (mS/cm)",
    ]
    if os.path.exists(ARCHIVO_CSV):
        try:
            df = pd.read_csv(ARCHIVO_CSV)
            # Asegurar que las columnas existan aunque el CSV esté parcialmente formateado
            for col in columnas:
                if col not in df.columns:
                    df[col] = None
            return df
        except Exception as e:
            st.warning(f"⚠️ No se pudo leer el CSV existente: {e}. Se iniciará uno nuevo.")
    return pd.DataFrame(columns=columnas)


def calcular_parametros(voltaje: float, corriente: float, area: float) -> dict:
    """
    Aplica las ecuaciones de caracterización eléctrica.

    Args:
        voltaje:   Voltaje medido en Voltios (V).
        corriente: Corriente medida en Amperios (A).
        area:      Área activa de la celda en m².

    Returns:
        Diccionario con Potencia, Densidad de Corriente y Densidad de Potencia.
    """
    potencia            = voltaje * corriente            # P = V × I  [W]
    densidad_corriente  = corriente / area       # J = I / A²  [A/m²]
    densidad_potencia   = potencia / area                # Pd = P / A  [W/m²]
    return {
        "Potencia (W)":                round(potencia, 6),
        "Densidad de Corriente (A/m²)": round(densidad_corriente, 6),
        "Densidad de Potencia (W/m²)": round(densidad_potencia, 6),
    }


def guardar_datos(df: pd.DataFrame) -> None:
    """Persiste el DataFrame completo en el archivo CSV local."""
    df.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8-sig")


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICAS 
# ─────────────────────────────────────────────────────────────────────────────

def generar_graficas(df: pd.DataFrame) -> None:
    """
    Genera las gráficas de análisis de la batería de flujo:
      - Curva de polarización (Voltaje vs. Densidad de Corriente)
      - Curva de potencia    (Densidad de Potencia vs. Densidad de Corriente)
      - Potencia vs. Resistencia
    """
    if df.empty:
        st.info("📊 Registra al menos una medición para visualizar las gráficas.")
        return

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Ordenar por densidad de corriente para curvas suaves
    df_plot = df.copy().sort_values("Densidad de Corriente (A/m²)").reset_index(drop=True)

    colores = {
        "voltaje":   "#e6ac2c",
        "potencia":  "#58a6ff",
        "resistencia": "#3fb950",
    }

    config_layout = dict(
        paper_bgcolor="#161b22",
        plot_bgcolor="#0d1117",
        font=dict(family="DM Sans, sans-serif", color="#e6edf3", size=12),
        margin=dict(l=50, r=30, t=50, b=50),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
        xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", linecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d", linecolor="#30363d"),
    )

    tab1, tab2, tab3 = st.tabs([
        "Curva de polarización",
        " Densidad de potencia",
        " Potencia vs. Resistencia",
    ])

    # ── Tab 1: Curva de polarización ─────────────────────────────────────────
    with tab1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df_plot["Densidad de Corriente (A/m²)"],
            y=df_plot["Voltaje (V)"],
            mode="lines+markers",
            name="Voltaje",
            line=dict(color=colores["voltaje"], width=2.5),
            marker=dict(size=7, color=colores["voltaje"],
                        line=dict(color="#0d1117", width=1.5)),
        ))
        fig1.update_layout(
            title="Curva de Polarización",
            xaxis_title="Densidad de Corriente (A/m²)",
            yaxis_title="Voltaje (V)",
            **config_layout,
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.download_button(
            "⬇️ Descargar gráfica (HTML)",
            data=fig1.to_html(full_html=True, include_plotlyjs="cdn"),
            file_name="curva_polarizacion.html",
            mime="text/html",
        )

    # ── Tab 2: Densidad de potencia ──────────────────────────────────────────
    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_plot["Densidad de Corriente (A/m²)"],
            y=df_plot["Densidad de Potencia (W/m²)"],
            mode="lines+markers",
            name="Den. Potencia",
            line=dict(color=colores["potencia"], width=2.5),
            marker=dict(size=7, color=colores["potencia"],
                        line=dict(color="#0d1117", width=1.5)),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)",
        ))
        fig2.update_layout(
            title="Curva de Densidad de Potencia",
            xaxis_title="Densidad de Corriente (A/m²)",
            yaxis_title="Densidad de Potencia (W/m²)",
            **config_layout,
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.download_button(
            "⬇️ Descargar gráfica (HTML)",
            data=fig2.to_html(full_html=True, include_plotlyjs="cdn"),
            file_name="densidad_potencia.html",
            mime="text/html",
        )

    # ── Tab 3: Potencia vs. Resistencia ──────────────────────────────────────
    with tab3:
        df_res = df.copy().sort_values("Resistencia (Ω)").reset_index(drop=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_res["Resistencia (Ω)"].astype(str) + " Ω",
            y=df_res["Potencia (W)"],
            name="Potencia",
            marker=dict(
                color=df_res["Potencia (W)"],
                colorscale=[[0, "#1c2330"], [1, colores["resistencia"]]],
                line=dict(color="#30363d", width=1),
            ),
        ))
        fig3.update_layout(
            title="Potencia por Resistencia",
            xaxis_title="Resistencia (Ω)",
            yaxis_title="Potencia (W)",
            **config_layout,
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.download_button(
            "⬇️ Descargar gráfica (HTML)",
            data=fig3.to_html(full_html=True, include_plotlyjs="cdn"),
            file_name="potencia_vs_resistencia.html",
            mime="text/html",
        )


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ─────────────────────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = cargar_datos_existentes()

if "ultima_muestra" not in st.session_state:
    st.session_state.ultima_muestra = None



#  BARRA LATERAL  

with st.sidebar:

    # ── 1. LOGOTIPO DEL INSTITUTO ─────────────────────────────────────────────
    st.markdown('<p class="section-label">Programador: Cesar Castro version 1.2</p>', unsafe_allow_html=True)
    try:
        st.image("logo_instituto.png", use_container_width=True)
    except FileNotFoundError:
        st.info("📷 Espacio reservado para el Logotipo del Instituto\n\n*(Guardar como `logo_instituto.png`)*")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── 2. DATOS DE ACCESO / CONFIGURACIÓN INICIAL ────────────────────────────
    st.markdown('<p class="section-label">Configuración del experimento</p>', unsafe_allow_html=True)

    operador = st.text_input(
        " Nombre del operador",
        placeholder="Ej: Dra. Ziomara",
        help="Nombre completo del técnico que realiza el experimento."
    )

    laboratorio = st.text_input(
        " Laboratorio / Departamento / Instituto",
        placeholder="Ej: Lab. de Electroquímica — UNAM",
    )

    fecha_experimento = st.date_input(
        "📅 Fecha del experimento",
        value=date.today(),
    )

    area_celda = st.number_input(
        "📐 Área activa de la celda (m²)",
        min_value=0.0001,
        value=0.001,
        step=None,
        format="%.6f",
        help="Área geométrica activa de la celda en metros cuadrados. Se usará como constante en todos los cálculos."
    )

    rpm = st.number_input(
        "🔄 RPM (revoluciones por minuto)",
        min_value=0.0,
        value=0.0,
        step=None,
        format="%.2f",
        help="Velocidad de la bomba o agitador en RPM."
    )

    par_redox = st.text_input(
        " Par redox",
        placeholder="Ej: Fe²⁺/Fe³⁺, V²⁺/V³⁺",
        help="Par redox del electrolito utilizado en el experimento."
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Condiciones iniciales</p>', unsafe_allow_html=True)

    ocp_inicial = st.number_input(
        " OCP Inicial (V)",
        min_value=0.0,
        value=0.0,
        step=None,
        format="%.4f",
        help="Potencial de circuito abierto (Open Circuit Potential) medido al inicio del experimento."
    )

    scc_inicial = st.number_input(
        " SCC Inicial (A)",
        min_value=0.0,
        value=0.0,
        step=None,
        format="%.4f",
        help="Corriente de cortocircuito (Short Circuit Current) medida al inicio del experimento."
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Indicador de registros guardados ─────────────────────────────────────
    n_registros = len(st.session_state.df)
    st.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-label">Registros totales</div>'
        f'<div class="metric-value">{n_registros}</div>'
        f'<div class="metric-unit">mediciones acumuladas</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Descarga del CSV ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.df.empty:
        csv_bytes = st.session_state.df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="⬇️  Descargar CSV",
            data=csv_bytes,
            file_name=ARCHIVO_CSV,
            mime="text/csv",
            help="Descarga todos los registros como archivo CSV.",
        )


# ─────────────────────────────────────────────────────────────────────────────
# ══════════════════════  ÁREA PRINCIPAL  ══════════════════════
# ─────────────────────────────────────────────────────────────────────────────

# ── Encabezado ───────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown('<p class="main-header">⚡ Caracterización de Batería de Flujo</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-sub">Sistema de registro y procesamiento de datos eléctricos por resistencia</p>',
        unsafe_allow_html=True
    )
with col_badge:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="status-badge">● En línea</span>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN A — RESUMEN DE CONFIGURACIÓN ACTIVA
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("📋  Configuración activa del experimento", expanded=False):
    if operador and laboratorio:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Operador",    operador)
        c2.metric("Laboratorio", laboratorio)
        c3.metric("Fecha",       str(fecha_experimento))
        c4.metric("Área celda",  f"{area_celda:.6f} m²")
        c5.metric("RPM",         f"{rpm:.2f}")
        c6.metric("Par redox",   par_redox if par_redox else "—")
    else:
        st.warning("⚠️ Completa el **Nombre del operador** y el **Laboratorio** en la barra lateral antes de registrar muestras.")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN B — TABLA DE 10 FILAS PARA CAPTURA MANUAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-label">🔬 Captura de datos técnicos — 10 mediciones</p>', unsafe_allow_html=True)
st.caption("Escribe directamente en las celdas con el teclado. Llena las filas que necesites (no es obligatorio llenar las 10). Cuando termines presiona **Registrar y guardar**.")

# Tabla con 10 filas vacías y todas las columnas de caracterización
df_plantilla = pd.DataFrame({
    "Resistencia (Ω)":          [None] * 20,
    "Voltaje (V)":              [None] * 20,
    "Corriente (A)":            [None] * 20,
    #"Temperatura (°C)":         [None] * 10,
    #"pH":                       [None] * 10,
    #"Concentración (mol/L)":    [None] * 10,
    #"Eficiencia Coulómbica (%)": [None] * 10,
    #"Eficiencia Energética (%)": [None] * 10,
    #"Tiempo (s)":               [None] * 10,
    #"Capacidad (mAh)":          [None] * 10,
    #"Energía (Wh)":             [None] * 10,
    #"Viscosidad (mPa·s)":       [None] * 10,
    #"Conductividad (mS/cm)":    [None] * 10,
})

df_capturado = st.data_editor(
    df_plantilla,
    num_rows="fixed",
    use_container_width=True,
    column_config={
        "Resistencia (Ω)":           st.column_config.NumberColumn("Resistencia (Ω)",          format="%.4f"),
        "Voltaje (V)":               st.column_config.NumberColumn("Voltaje (V)",               format="%.4f"),
        "Corriente (A)":             st.column_config.NumberColumn("Corriente (A)",             format="%.4f"),
        #"Temperatura (°C)":          st.column_config.NumberColumn("Temperatura (°C)",          format="%.2f"),
        #"pH":                        st.column_config.NumberColumn("pH",                        format="%.2f"),
        #"Concentración (mol/L)":     st.column_config.NumberColumn("Concentración (mol/L)",     format="%.4f"),
        #"Eficiencia Coulómbica (%)": st.column_config.NumberColumn("Eficiencia Coulómbica (%)", format="%.2f"),
        #"Eficiencia Energética (%)": st.column_config.NumberColumn("Eficiencia Energética (%)", format="%.2f"),
        #"Tiempo (s)":                st.column_config.NumberColumn("Tiempo (s)",                format="%.2f"),
        #"Capacidad (mAh)":           st.column_config.NumberColumn("Capacidad (mAh)",           format="%.4f"),
        #"Energía (Wh)":              st.column_config.NumberColumn("Energía (Wh)",              format="%.6f"),
        #"Viscosidad (mPa·s)":        st.column_config.NumberColumn("Viscosidad (mPa·s)",        format="%.4f"),
        #"Conductividad (mS/cm)":     st.column_config.NumberColumn("Conductividad (mS/cm)",     format="%.4f"),
    },
    key="tabla_10_filas",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Botón de registro ────────────────────────────────────────────────────────
btn_registrar = st.button("⚡  Registrar y guardar", type="primary")

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LÓGICA DE REGISTRO AL PRESIONAR EL BOTÓN
# ─────────────────────────────────────────────────────────────────────────────
if btn_registrar:
    # Validación de campos obligatorios
    errores = []
    if not operador.strip():
        errores.append("• Nombre del operador (barra lateral)")
    if not laboratorio.strip():
        errores.append("• Laboratorio / Departamento (barra lateral)")
    if area_celda <= 0:
        errores.append("• Área de la celda debe ser mayor a 0")

    if errores:
        st.error("❌ **Completa los siguientes campos obligatorios antes de registrar:**\n\n" + "\n".join(errores))
    else:
        # Filtrar solo las filas que tienen al menos un valor capturado
        df_valido = df_capturado.dropna(how="all")

        if df_valido.empty:
            st.warning("⚠️ No hay datos en la tabla. Escribe al menos una fila antes de guardar.")
        else:
            filas_nuevas = []
            for _, fila in df_valido.iterrows():
                resistencia = float(fila["Resistencia (Ω)"] or 0)
                voltaje     = float(fila["Voltaje (V)"]     or 0)
                corriente   = float(fila["Corriente (A)"]   or 0)

                # Cálculos automáticos por cada fila
                resultados = calcular_parametros(voltaje, corriente, area_celda)

                filas_nuevas.append({
                    "Operador":                      operador.strip(),
                    "Laboratorio":                   laboratorio.strip(),
                    "Fecha":                         str(fecha_experimento),
                    "Área (m²)":                     area_celda,
                    "RPM":                           round(rpm, 2),
                    "Par Redox":                     par_redox.strip() if par_redox else "",
                    "OCP Inicial (V)":               round(ocp_inicial, 4),
                    "SCC Inicial (A)":               round(scc_inicial, 4),
                    "Resistencia (Ω)":               round(resistencia, 4),
                    "Voltaje (V)":                   round(voltaje, 4),
                    "Corriente (A)":                 round(corriente, 4),
                    "Potencia (W)":                  resultados["Potencia (W)"],
                    "Densidad de Corriente (A/m²)":  resultados["Densidad de Corriente (A/m²)"],
                    "Densidad de Potencia (W/m²)":   resultados["Densidad de Potencia (W/m²)"],
                    #"Temperatura (°C)":              fila.get("Temperatura (°C)"),
                    #"pH":                            fila.get("pH"),
                    #"Concentración (mol/L)":         fila.get("Concentración (mol/L)"),
                    #"Eficiencia Coulómbica (%)":     fila.get("Eficiencia Coulómbica (%)"),
                    #"Eficiencia Energética (%)":     fila.get("Eficiencia Energética (%)"),
                    #"Tiempo (s)":                    fila.get("Tiempo (s)"),
                    #"Capacidad (mAh)":               fila.get("Capacidad (mAh)"),
                    #"Energía (Wh)":                  fila.get("Energía (Wh)"),
                    #"Viscosidad (mPa·s)":            fila.get("Viscosidad (mPa·s)"),
                    #"Conductividad (mS/cm)":         fila.get("Conductividad (mS/cm)"),
                })

            # Agregar todas las filas al historial
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame(filas_nuevas)],
                ignore_index=True
            )

            # Persistir en CSV
            guardar_datos(st.session_state.df)

            st.success(
                f"✅ **{len(filas_nuevas)} muestra(s) registrada(s) correctamente.** "
                f"Total acumulado: {len(st.session_state.df)} medición(es)."
            )
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN C — TABLA DE DATOS HISTÓRICOS EN TIEMPO REAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label" style="margin-top:1.5rem;">📊 Historial de mediciones</p>', unsafe_allow_html=True)

if st.session_state.df.empty:
    st.info("📋 Aún no hay datos registrados. Ingresa los parámetros y presiona **Registrar Muestra**.")
else:
    # Mostrar tabla con formato
    st.dataframe(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
    )

    # Estadísticas rápidas
    with st.expander("📈  Estadísticas rápidas del conjunto de datos"):
        cols_numericas = [
            "Resistencia (Ω)", "Voltaje (V)", "Corriente (A)",
            "Potencia (W)", "Densidad de Corriente (A/m²)", "Densidad de Potencia (W/m²)"
        ]
        df_num = st.session_state.df[cols_numericas].describe().round(6)
        st.dataframe(df_num, use_container_width=True)

    # Botón para limpiar sesión (mantiene el CSV como respaldo)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Limpiar vista (mantiene el CSV guardado)"):
        st.session_state.df = pd.DataFrame(columns=st.session_state.df.columns)
        st.session_state.ultima_muestra = None
        st.info("Vista limpiada. Los datos siguen guardados en el archivo CSV local.")
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN D — MÓDULO DE GRÁFICAS (RESERVADO)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">📉 Visualización de datos</p>', unsafe_allow_html=True)

generar_graficas(st.session_state.df)


# ─────────────────────────────────────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; font-family:\'Space Mono\',monospace; '
    'font-size:0.7rem; color:#444d56; letter-spacing:1px;">'
    'SISTEMA DE CARACTERIZACIÓN ELECTROQUÍMICA · BATERÍA DE FLUJO · '
    f'ARCHIVO LOCAL: {ARCHIVO_CSV}'
    '</p>',
    unsafe_allow_html=True
)
