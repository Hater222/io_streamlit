import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Configuración inicial
# -----------------------
st.set_page_config(
    page_title="Comparativa Protocolos IoT",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Comparativa de Protocolos IoT")
st.markdown("Explora **WiFi, Zigbee, LoRaWAN y NB-IoT** según consumo, latencia, cobertura y duración de batería.")

# -----------------------
# Parámetros del usuario
# -----------------------
st.sidebar.header("⚙️ Parámetros de simulación")
n_sensores = st.sidebar.slider("Número de sensores", 1, 500, 50)
mensajes_dia = st.sidebar.slider("Mensajes por sensor al día", 1, 500, 50)
payload = st.sidebar.slider("Tamaño del payload (bytes)", 1, 512, 50)
bateria = st.sidebar.slider("Capacidad de la batería (mAh)", 100, 10000, 2000)
overhead = st.sidebar.slider("Overhead (%)", 1, 50, 10)

# -----------------------
# Funciones de cálculo (cacheadas)
# -----------------------
@st.cache_data
def calcular_metricas(n_sensores, mensajes_dia, payload, bateria, overhead):
    # Valores base (aproximados y didácticos, no industriales)
    protocolos = {
        "WiFi": {"consumo": 15, "latencia": 50, "cobertura": 50},
        "Zigbee": {"consumo": 5, "latencia": 30, "cobertura": 100},
        "LoRaWAN": {"consumo": 1, "latencia": 1000, "cobertura": 10000},
        "NB-IoT": {"consumo": 2, "latencia": 150, "cobertura": 1000},
    }

    resultados = []
    for proto, vals in protocolos.items():
        # Consumo estimado por mensaje
        consumo_mensaje = (payload * (1 + overhead/100)) * vals["consumo"] / 1000
        consumo_dia = consumo_mensaje * mensajes_dia * n_sensores
        # Duración de la batería en días
        duracion_bateria = bateria * 1000 / consumo_dia if consumo_dia > 0 else 0

        resultados.append({
            "Protocolo": proto,
            "Consumo diario (mAh)": round(consumo_dia, 2),
            "Latencia (ms)": vals["latencia"],
            "Cobertura (m)": vals["cobertura"],
            "Duración batería (días)": round(duracion_bateria, 2)
        })

    return pd.DataFrame(resultados)

df = calcular_metricas(n_sensores, mensajes_dia, payload, bateria, overhead)

# -----------------------
# Visualización
# -----------------------
st.subheader("📊 Resultados comparativos")
st.dataframe(df, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df, x="Protocolo", y="Consumo diario (mAh)", color="Protocolo",
                  title="Consumo energético diario")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df, x="Protocolo", y="Latencia (ms)", color="Protocolo",
                  title="Latencia de transmisión")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.bar(df, x="Protocolo", y="Cobertura (m)", color="Protocolo",
                  title="Cobertura estimada")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(df, x="Protocolo", y="Duración batería (días)", color="Protocolo",
                  title="Duración estimada de la batería")
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------
# Exportación
# -----------------------
st.subheader("💾 Exportar resultados")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Descargar CSV",
    data=csv,
    file_name="resultados_protocolos.csv",
    mime="text/csv"
)

# -----------------------
# Justificación del caso aplicado
# -----------------------
st.subheader("📝 Justificación del caso aplicado")
st.markdown("Redacta aquí tu defensa sobre el protocolo más adecuado según tu escenario (hogar, ciudad, agricultura...).")
texto = st.text_area("Escribe tu justificación aquí")

if st.button("Guardar justificación"):
    with open("justificacion.md", "w", encoding="utf-8") as f:
        f.write(texto)
    st.success("Justificación guardada en **justificacion.md**")
