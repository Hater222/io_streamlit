# app.py — Sesión 3 IoT (single-file, web-only)
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dataclasses import dataclass


st.set_page_config(page_title="Sesión 3 · Protocolos IoT", page_icon="📡", layout="wide")
st.title("📡 Sesión 3 · Comparativa de Protocolos IoT (WiFi, Zigbee, LoRaWAN, NB-IoT)")
st.caption("Grado en Ingeniería Informática · Blockchain y IoT · Práctica 100% web")


# ---------- Modelo en un archivo ----------
@dataclass
class ProtocolParams:
name: str
bitrate_bps: float
tx_current_mA: float
rx_current_mA: float
idle_current_mA: float
range_m: float
overhead_bytes: int
base_latency_ms: float
duty_cycle_limit: float
notes: str = ""


def default_protocols():
return [
ProtocolParams("WiFi", 10e6, 180.0, 50.0, 5.0, 30, 80, 50, 1.0, "alto throughput"),
ProtocolParams("Zigbee", 250e3, 35.0, 19.0, 0.3, 100, 25, 100, 1.0, "malla, bajo consumo"),
ProtocolParams("LoRaWAN", 5e3, 45.0, 12.0, 0.01, 15000,20, 800, 0.01, "largo alcance, bajo bitrate"),
ProtocolParams("NB-IoT", 26e3, 220.0, 30.0, 0.05, 10000,30, 200, 1.0, "cobertura celular"),
]


def scenario(n_sensors:int, msgs_per_day:int, payload_bytes:int, rx_ratio:float):
return dict(n_sensors=n_sensors, msgs_per_day=msgs_per_day,
payload_bytes=payload_bytes, rx_ratio=rx_ratio)


def estimate(proto: ProtocolParams, sc: dict, battery_mAh: float, header_factor: float=1.0):
msgs = sc["msgs_per_day"]; payload = sc["payload_bytes"]; rx_ratio = sc["rx_ratio"]
bytes_total = payload + int(proto.overhead_bytes * header_factor)
bits_total = bytes_total * 8
# tiempo de transmisión por mensaje (s)
tx_time_s = bits_total / proto.bitrate_bps
# tiempo de recepción estimado por mensaje (s)
rx_time_s = tx_time_s * rx_ratio
# si existe limitación por duty-cycle, ajustar (simulación simplificada)
if proto.duty_cycle_limit < 1.0:
# empujamos el TX time efectivo para respetar duty-cycle (modelo didáctico)
tx_time_s = tx_time_s / proto.duty_cycle_limit
tx_total_h = (tx_time_s * msgs) / 3600.0
rx_total_h = (rx_time_s * msgs) / 3600.0
active_h = tx_total_h + rx_total_h
idle_h = max(0.0, 24.0 - active_h)
tx_mAh = proto.tx_current_mA * tx_total_h
rx_mAh = proto.rx_current_mA * rx_total_h
idle_mAh = proto.idle_current_mA * idle_h
daily_mAh_per_sensor = tx_mAh + rx_mAh + idle_mAh
latency_ms = proto.base_latency_ms + (tx_time_s * 1000.0)
days_battery = battery_mAh / daily_mAh_per_sensor if daily_mAh_per_sensor > 0 else float('inf')
return {
"protocol": proto.name,
"consumo_mAh_dia": daily_mAh_per_sensor,
"latencia_ms": latency_ms,
"cobertura_m": proto.range_m,
"dias_bateria": days_battery,
"notas": proto.notes
}


def evaluate_all(protocols, sc, battery_mAh, header_factor):
rows = [estimate(p, sc, battery_mAh, header_factor) for p in protocols]
df = pd.DataFrame(rows)
return df.sort_values(by="consumo_mAh_dia").reset_index(drop=True)


# ---------- UI ----------
st.caption("Modelo docente y simplificado. Ajusta parámetros para explorar compromisos reales.")
