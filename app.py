import streamlit as st
import pandas as pd
import os
import configparser
from modelo import ModeloFinanciero

st.set_page_config(page_title="Simulador Financiero Interactivo", layout="wide")

# -------------------------------
# 📁 Funciones para settings.cfg
# -------------------------------
CFG_FILE = "settings.cfg"

def guardar_settings():
    config = configparser.ConfigParser()
    config["PARAMETROS"] = {k: str(v) for k, v in st.session_state.items() if isinstance(v, (int, float))}
    with open(CFG_FILE, "w") as f:
        config.write(f)
    st.session_state._original_settings = {k: st.session_state[k] for k in defaults}

def cargar_settings():
    config = configparser.ConfigParser()
    config.read(CFG_FILE)
    if "PARAMETROS" in config:
        for k, v in config["PARAMETROS"].items():
            try:
                st.session_state[k] = float(v) if "." in v else int(v)
            except:
                pass
        st.session_state._original_settings = {k: st.session_state[k] for k in defaults}

# -------------------------------
# 🔧 Inicializar valores por defecto
# -------------------------------
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
    "rentabilidad_media": 2.5
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Cargar settings si existe el archivo
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
with st.sidebar:
    seccion = st.selectbox(
        "Menú",
        ["⚙️ Configuración", "📈 Evolución", "🎯 Probabilidad de Retiro", "📊 Resumen por Década"],
        index=0
    )

    st.markdown("### ⚙️ Ajustes rápidos")
    st.session_state.salario_inicial = st.number_input("Salario anual (€)", min_value=10000, max_value=100000, value=st.session_state.salario_inicial, step=1000)
    st.session_state.edad_retiro_deseada = st.number_input("Edad deseada de retiro", min_value=st.session_state.edad_actual, max_value=65, value=st.session_state.edad_retiro_deseada)
    st.session_state.gasto_anual = st.number_input("Gasto anual (€)", min_value=5000, max_value=80000, value=st.session_state.gasto_anual, step=1000)
    st.session_state.inflacion_media = st.number_input("Inflación media (%)", min_value=0.0, max_value=10.0, value=st.session_state.inflacion_media, step=0.1)

    # 💾 Configuración inteligente
    st.markdown("### 💾 Configuración")
    cfg_existe = os.path.exists(CFG_FILE)
    modificados = settings_modificados()

    if cfg_existe and not modificados:
        if st.button("📥 Cargar settings.cfg"):
            cargar_settings()
            st.success("✅ Configuración cargada correctamente.")
    elif modificados:
        if st.button("💾 Guardar settings.cfg"):
            guardar_settings()
            st.success("✅ Configuración guardada correctamente.")
    elif not cfg_existe:
        if st.button("💾 Guardar settings.cfg (inicial)"):
            guardar_settings()
            st.success("✅ Configuración guardada correctamente.")

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

if seccion == "⚙️ Configuración":
    st.markdown("### Parámetros de simulación")

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.edad_actual = st.slider("Edad actual", 25, 65, st.session_state.edad_actual)
        st.session_state.edad_max = st.slider("Edad máxima simulada", st.session_state.edad_actual + 10, 100, st.session_state.edad_max)
        st.session_state.ahorro_inicial = st.slider("Ahorro inicial (€)", 0, 1000000, st.session_state.ahorro_inicial, step=5000)
        st.session_state.ahorro_deseado = st.slider("Ahorro deseado anual (€)", 0, 30000, st.session_state.ahorro_deseado, step=500)

    with c2:
        st.session_state.pension_anual = st.slider("Pensión anual (€)", 6000, 40000, st.session_state.pension_anual, step=1000)
        st.session_state.alquiler1 = st.slider("Ingreso por alquiler 1 (€)", 0, 30000, st.session_state.alquiler1, step=500)
        st.session_state.alquiler2 = st.slider("Ingreso por alquiler 2 (€)", 0, 30000, st.session_state.alquiler2, step=500)
        st.session_state.prestamo = st.slider("Deuda o préstamo inicial (€)", 0, 200000, st.session_state.prestamo, step=5000)
        st.session_state.rentabilidad_media = st.slider("Rentabilidad media (%)", 0.0, 15.0, st.session_state.rentabilidad_media, step=0.1)

elif seccion == "📈 Evolución":
    st.markdown("### Evolución Financiera Anual")

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
    fig = modelo.graficar_evolucion(df, titulo=None)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

elif seccion == "🎯 Probabilidad de Retiro":
    st.markdown("### Probabilidad de Éxito Financiero")
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
    df_prob = pd.DataFrame({"Edad": edades, "Probabilidad de éxito": probabilidades})
    st.line_chart(df_prob.set_index("Edad"))

    st.info(f"📌 Edad deseada de retiro: {params.edad_retiro_deseada} años")
    if edad_optima:
        st.success(f"🎯 Edad óptima estimada de retiro: {edad_optima} años")
    else:
        st.warning(f"⚠️ No se alcanza el umbral de éxito financiero antes de los {params.edad_max} años.")

elif seccion == "📊 Resumen por Década":
    st.markdown("### Resumen Financiero por Década")
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
    resumen = modelo.resumen_por_decada(df_evolucion)
    st.dataframe(resumen.style.format({
        "Promedio Ingresos": "{:,.2f} €",
        "Promedio Gastos": "{:,.2f} €",
        "Patrimonio Final": "{:,.2f} €"
    }), use_container_width=True)

    st.download_button(
        "📥 Descargar resumen en CSV",
        resumen.to_csv(index=False),
        file_name="resumen_por_decada.csv"
    )