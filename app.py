import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dashboard Edukatif", layout="wide")

st.title("📊 Dashboard Analisis Data Siswa")
st.markdown("Visualisasi data berbasis Excel dengan desain pastel lembut & edukatif")

# ===============================
# LOAD DATA (AMAN UNTUK CLOUD)
# ===============================
try:
    df = pd.read_excel("data_excel.xlsx")
    st.success(f"✅ Data berhasil dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")
except:
    st.error("❌ File data_excel.xlsx tidak ditemukan. Pastikan sudah diupload ke repository.")
    st.stop()

# ===============================
# KPI
# ===============================
st.subheader("📌 Ringkasan Utama")

col1, col2, col3 = st.columns(3)

col1.metric("👥 Jumlah Responden", df.shape[0])
col2.metric("📄 Jumlah Variabel", df.shape[1])
col3.metric("📊 Rata-rata Skor", f"{df.mean(numeric_only=True).mean():.2f}")

st.divider()

# ===============================
# RATA-RATA INDIKATOR
# ===============================
st.subheader("📈 Rata-rata Nilai Setiap Indikator")

mean_values = df.mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8,5))
colors = ["#A8DADC", "#FBC4AB", "#CDB4DB", "#BDE0FE"]

ax.bar(mean_values.index, mean_values.values, color=colors[:len(mean_values)])

ax.set_ylabel("Rata-rata Nilai")
ax.set_title("Visualisasi Rata-rata Indikator")
ax.grid(axis="y", linestyle="--", alpha=0.5)

for i, v in enumerate(mean_values.values):
    ax.text(i, v + 0.05, f"{v:.2f}", ha="center")

st.pyplot(fig)

st.divider()

# ===============================
# DISTRIBUSI
# ===============================
st.subheader("📊 Distribusi Nilai")

selected_col = st.selectbox("Pilih indikator:", mean_values.index)

fig2, ax2 = plt.subplots(figsize=(7,4))
ax2.hist(df[selected_col], bins=10, color="#BDE0FE", edgecolor="black")

ax2.set_title(f"Distribusi {selected_col}")
ax2.set_xlabel("Nilai")
ax2.set_ylabel("Frekuensi")

st.pyplot(fig2)

st.success("🎯 Dashboard siap digunakan!")
