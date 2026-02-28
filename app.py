import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Edukatif", layout="wide")

st.title("📊 Dashboard Analisis Data")
st.markdown("Dashboard interaktif berbasis Excel")

# Load data
df = pd.read_excel(list(st.session_state.uploaded_file.keys())[0])

st.success(f"✅ Data dimuat: {df.shape[0]} baris")

# KPI
col1, col2 = st.columns(2)
col1.metric("Jumlah Data", df.shape[0])
col2.metric("Rata-rata", f"{df.mean(numeric_only=True).mean():.2f}")

st.divider()

# Grafik rata-rata
mean_values = df.mean(numeric_only=True)

fig, ax = plt.subplots()
ax.bar(mean_values.index, mean_values.values)
ax.set_title("Rata-rata per Variabel")

st.pyplot(fig)
