import streamlit as st
import pandas as pd
import os
import configparser
from modelo import ModeloFinanciero

st.set_page_config(page_title="Simulador Financiero Interactivo", layout="wide")

# -------------------------------
# 🌍 Diccionario de traducciones UI
# -------------------------------
TEXTOS_UI = {
    "es": {
        "menu": ["⚙️ Configuración", "📈 Evolución", "🎯 Probabilidad de Retiro", "📊 Resumen por Década"],
        "ajustes_rapidos": "⚙️ Ajustes rápidos",
        "configuracion": "💾 Configuración",
        "parametros_simulacion": "### Parámetros de simulación",
        "titulo_evolucion": "### Evolución Financiera Anual",
        "titulo_probabilidad": "### Probabilidad de Éxito Financiero",
        "titulo_resumen": "### Resumen Financiero por Década",
        "descargar_csv": "📥 Descargar resumen en CSV",
        "config_cargada": "✅ Configuración cargada correctamente.",
        "config_guardada": "✅ Configuración guardada correctamente.",
        # Sliders
        "slider_salario": "Salario anual (€)",
        "slider_retiro": "Edad deseada de retiro",
        "slider_gasto": "Gasto anual (€)",
        "slider_inflacion": "Inflación media (%)",
        "slider_edad_actual": "Edad actual",
        "slider_edad_max": "Edad máxima simulada",
        "slider_ahorro_inicial": "Ahorro inicial (€)",
        "slider_ahorro_deseado": "Ahorro deseado anual (€)",
        "slider_pension": "Pensión anual (€)",
        "slider_alquiler1": "Ingreso por alquiler 1 (€)",
        "slider_alquiler2": "Ingreso por alquiler 2 (€)",
        "slider_prestamo": "Deuda o préstamo inicial (€)",
        "slider_rentabilidad": "Rentabilidad media (%)"
    },
    "en": {
        "menu": ["⚙️ Settings", "📈 Evolution", "🎯 Retirement Probability", "📊 Decade Summary"],
        "ajustes_rapidos": "⚙️ Quick Settings",
        "configuracion": "💾 Configuration",
        "parametros_simulacion": "### Simulation Parameters",
        "titulo_evolucion": "### Annual Financial Evolution",
        "titulo_probabilidad": "### Financial Success Probability",
        "titulo_resumen": "### Financial Summary by Decade",
        "descargar_csv": "📥 Download summary as CSV",
        "config_cargada": "✅ Settings loaded successfully.",
        "config_guardada": "✅ Settings saved successfully.",
        "slider_salario": "Annual salary (€)",
        "slider_retiro": "Desired retirement age",
        "slider_gasto": "Annual expenses (€)",
        "slider_inflacion": "Average inflation (%)",
        "slider_edad_actual": "Current age",
        "slider_edad_max": "Maximum simulated age",
        "slider_ahorro_inicial": "Initial savings (€)",
        "slider_ahorro_deseado": "Desired annual savings (€)",
        "slider_pension": "Annual pension (€)",
        "slider_alquiler1": "Rental income 1 (€)",
        "slider_alquiler2": "Rental income 2 (€)",
        "slider_prestamo": "Initial debt or loan (€)",
        "slider_rentabilidad": "Average return (%)"
    },
    # Añade traducciones equivalentes en "fr", "de", "eu"
}

# -------------------------------
# 📁 Funciones para settings.cfg
# -------------------------------
CFG_FILE = "settings.cfg"

defaults = {
    "edad_actual": 48,
    "edad_max": 100,
    "edad_retiro_deseada": 52,
    "salario_inicial": 25000,
    "ahorro_inicial": 100000,
    "ahorro_deseado": 0,
    "gasto_anual": 24000,
    "pension_anual": 18000,
    "alquiler1": 0,
    "alquiler2": 0,
    "prestamo": 0,
    "inflacion_media": 2.0,
    "rentabilidad_media": 2.5,
    "idioma": "es"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def guardar_settings():
    config = configparser.ConfigParser()
    config["PARAMETROS"] = {k: str(v) for k, v in st.session_state.items() if isinstance(v, (int, float, str))}
    with open(CFG_FILE, "w") as f:
        config.write(f)
    st.session_state._original_settings = {k: st.session_state[k] for k in defaults}

def cargar_settings():
    config = configparser.ConfigParser()
    config.read(CFG_FILE)
    if "PARAMETROS" in config:
        for k, v in config["PARAMETROS"].items():
            try:
                if v.replace(".", "", 1).isdigit():
                    st.session_state[k] = float(v) if "." in v else int(v)
                else:
                    st.session_state[k] = v
            except:
                pass
        st.session_state._original_settings = {k: st.session_state[k] for k in defaults}

if "_original_settings" not in st.session_state:
    if os.path.exists(CFG_FILE):
        cargar_settings()
    else:
        st.session_state._original_settings = defaults.copy()

def settings_modificados():
    for k in defaults:
        if st.session_state.get(k) != st.session_state._original_settings.get(k):
            return True
    return False

# -------------------------------
# 📋 Menú lateral
# -------------------------------
idioma_opciones = {
    "Español": "es",
    "English": "en",
    "Français": "fr",
    "Deutsch": "de",
    "Euskara": "eu"
}
with st.sidebar:
    idioma_seleccionado = st.selectbox("Idioma / Language", list(idioma_opciones.keys()))
    st.session_state.idioma = idioma_opciones[idioma_seleccionado]
    t = TEXTOS_UI.get(st.session_state.idioma, TEXTOS_UI["es"])

    seccion = st.selectbox("Menú", t["menu"], index=0)

    st.markdown(t["ajustes_rapidos"])
    st.session_state.salario_inicial = st.number_input(t["slider_salario"], min_value=10000, max_value=100000, value=st.session_state.salario_inicial, step=1000)
    st.session_state.edad_retiro_deseada = st.number_input(t["slider_retiro"], min_value=st.session_state.edad_actual, max_value=65, value=st.session_state.edad_retiro_deseada)
    st.session_state.gasto_anual = st.number_input(t["slider_gasto"], min_value=5000, max_value=80000, value=st.session_state.gasto_anual, step=1000)
    st.session_state.inflacion_media = st.number_input(t["slider_inflacion"], min_value=0.0, max_value=10.0, value=st.session_state.inflacion_media, step=0.1)

    st.markdown(t["configuracion"])
    cfg_existe = os.path.exists(CFG_FILE)
    modificados = settings_modificados()

    if cfg_existe and not modificados:
        if st.button("📥 Cargar settings.cfg"):
            cargar_settings()
            st.success(t["config_cargada"])
    elif modificados:
        if st.button("💾 Guardar settings.cfg"):
            guardar_settings()
            st.success(t["config_guardada"])
    elif not cfg_existe:
        if st.button("💾 Guardar settings.cfg (inicial)"):
            guardar_settings()
            st.success(t["config_guardada"])

# -------------------------------
# 🧠 Contenido principal
# -------------------------------
params = st.session_state
modelo = ModeloFinanciero(
    salario_inicial=params.salario_inicial,
    patrimonio_inicial=params.ahorro_inicial,
    anio_inicial=2025,
    prestamo_inicial=params.prestamo,
    alquiler1_inicial=params.alquiler1,
    alquiler2_inicial=params.alquiler2
)

if seccion == t["menu"][0]:
    st.markdown(t["parametros_simulacion"])
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.edad_actual = st.slider(t["slider_edad_actual"], 25, 65, st.session_state.edad_actual)
        st.session_state.edad_max = st.slider(t["slider_edad_max"], st.session_state.edad_actual + 10, 100, st.session_state.edad_max)
        st.session_state.ahorro_inicial = st.slider(t["slider_ahorro_inicial"], 0, 1000000, st.session_state.ahorro_inicial, step=5000)
        st.session_state.ahorro_deseado = st.slider(t["slider_ahorro_deseado"], 0, 30000, st.session_state.ahorro_deseado, step=500)

    with c2:
        st.session_state.pension_anual = st.slider(t["slider_pension"], 6000, 40000, st.session_state.pension_anual, step=1000)
        st.session_state.alquiler1 = st.slider(t["slider_alquiler1"], 0, 30000, st.session_state.alquiler1, step=500)
        st.session_state.alquiler2 = st.slider(t["slider_alquiler2"], 0, 30000, st.session_state.alquiler2, step=500)
        st.session_state.prestamo = st.slider(t["slider_prestamo"], 0, 200000, st.session_state.prestamo, step=5000)
        st.session_state.rentabilidad_media = st.slider(t["slider_rentabilidad"], 0.0, 15.0, st.session_state.rentabilidad_media, step=0.1)

elif seccion == t["menu"][1]:
    st.markdown(t["titulo_evolucion"])
    df = modelo.simular_evolucion_patrimonial(
        salario_inicial=params.salario_inicial,
        ahorro_inicial=params.ahorro_inicial,
        gasto_anual=params.gasto_anual,
        ahorro_deseado=params.ahorro_deseado,
        pension_anual=params.pension_anual,
        edad_actual=params.edad_actual,
        edad_max=params.edad_max,
        edad_retiro_deseada=params.edad_retiro_deseada,
        inflacion_media=params.inflacion_media / 100,
        rentabilidad_media=params.rentabilidad_media / 100
    )
    fig = modelo.graficar_evolucion(df, idioma=params.idioma)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

elif seccion == t["menu"][2]:
    st.markdown(t["titulo_probabilidad"])
    edades, probabilidades, edad_optima = modelo.curva_probabilidad_retiro(
        salario_inicial=params.salario_inicial,
        ahorro_inicial=params.ahorro_inicial,
        gasto_anual=params.gasto_anual,
        ahorro_deseado=params.ahorro_deseado,
        pension_anual=params.pension_anual,
        edad_actual=params.edad_actual,
        edad_max=params.edad_max,
        edad_retiro_deseada=params.edad_retiro_deseada,
        inflacion_media=params.inflacion_media / 100,
        rentabilidad_media=params.rentabilidad_media / 100
    )
    fig = modelo.graficar_curva_retiro(edades, probabilidades, edad_optima, idioma=params.idioma)
    st.plotly_chart(fig, use_container_width=True)



elif seccion == t["menu"][3]:
    st.markdown(t["titulo_resumen"])
    df_evolucion = modelo.simular_evolucion_patrimonial(
        salario_inicial=params.salario_inicial,
        ahorro_inicial=params.ahorro_inicial,
        gasto_anual=params.gasto_anual,
        ahorro_deseado=params.ahorro_deseado,
        pension_anual=params.pension_anual,
        edad_actual=params.edad_actual,
        edad_max=params.edad_max,
        edad_retiro_deseada=params.edad_retiro_deseada,
        inflacion_media=params.inflacion_media / 100,
        rentabilidad_media=params.rentabilidad_media / 100
    )
    resumen = modelo.resumen_por_decada(df_evolucion, idioma=params.idioma)
    st.dataframe(resumen.style.format({
        resumen.columns[1]: "{:,.2f} €",
        resumen.columns[2]: "{:,.2f} €",
        resumen.columns[3]: "{:,.2f} €"
    }), use_container_width=True)

    st.download_button(
        t["descargar_csv"],
        resumen.to_csv(index=False),
        file_name="resumen_por_decada.csv"
    )