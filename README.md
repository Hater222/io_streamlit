# io_streamlit
# Sesión 3 · Protocolos IoT (Streamlit App)

Aplicación interactiva para comparar **WiFi, Zigbee, LoRaWAN y NB-IoT** en términos de consumo, latencia, cobertura y duración de batería. Desarrollada en **Streamlit**, se despliega directamente en la nube sin necesidad de instalación local.

---

## 🚀 Objetivo

Explorar el comportamiento de distintos protocolos IoT bajo diferentes condiciones de uso:

* Ajustar parámetros (sensores, mensajes, payload, batería, overhead).
* Visualizar gráficas comparativas de consumo, latencia, cobertura y duración de batería.
* Exportar resultados en formato CSV.
* Evaluar casos de uso típicos (hogar conectado, parking urbano, riego agrícola).

---

## ⚙️ Instalación y ejecución local

```bash
# Clonar el repositorio
git clone https://github.com/Hater222/iot-streamlit.git
cd iot-streamlit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

---

## 🌐 Despliegue en Streamlit Cloud

1. Accede a [Streamlit Community Cloud](https://streamlit.io/cloud).
2. Conéctalo con tu cuenta de GitHub.
3. Selecciona este repositorio.
4. Define `app.py` como archivo principal.
5. Haz clic en **Deploy** y comparte el enlace con tu equipo.

---

## 🧪 Cómo usar la app

1. Ajusta los parámetros desde la barra lateral (nº de sensores, mensajes/día, payload, batería, etc.).
2. Observa en tiempo real cómo cambian las métricas y gráficas.
3. Exporta los resultados en CSV con un clic.
4. En el panel **Caso aplicado**, redacta una breve justificación sobre el protocolo más adecuado para tu escenario.

---


---

## 📌 Nota

El modelo es **simplificado y didáctico**, no sustituye un diseño industrial de red IoT. Sirve para experimentar con los compromisos entre **consumo energético, latencia, cobertura y vida útil de batería** en distintos protocolos.
