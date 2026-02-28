import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Dashboard Edukatif",
    layout="wide"
)

st.title("📊 Dashboard Analisis Data Siswa")
st.markdown("Visualisasi data berbasis Excel dengan desain **pastel lembut & edukatif**")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_excel("data_excel.xlsx")

st.success(f"✅ Data berhasil dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")

# ===============================
# KPI UTAMA
# ===============================
st.subheader("📌 Ringkasan Utama")

col1, col2, col3 = st.columns(3)

col1.metric(
    label="👥 Jumlah Responden",
    value=df.shape[0]
)

col2.metric(
    label="📄 Jumlah Variabel",
    value=df.shape[1]
)

col3.metric(
    label="📊 Rata-rata Skor",
    value=f"{df.mean(numeric_only=True).mean():.2f}"
)

st.divider()

# ===============================
# GRAFIK RATA-RATA PER VARIABEL
# ===============================
st.subheader("📈 Rata-rata Nilai Setiap Indikator")

mean_values = df.mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8,5))
ax.bar(
    mean_values.index,
    mean_values.values,
    color=["#A8DADC", "#FBC4AB", "#CDB4DB", "#BDE0FE"]
)

ax.set_ylabel("Rata-rata Nilai")
ax.set_title("Visualisasi Rata-rata Indikator")
ax.grid(axis="y", linestyle="--", alpha=0.5)

for i, v in enumerate(mean_values.values):
    ax.text(i, v + 0.05, f"{v:.2f}", ha="center")

st.pyplot(fig)

st.info("📘 Grafik ini menunjukkan indikator mana yang sudah baik dan mana yang perlu ditingkatkan")

st.divider()

# ===============================
# DISTRIBUSI DATA
# ===============================
st.subheader("📊 Distribusi Nilai")

selected_col = st.selectbox(
    "Pilih indikator untuk dianalisis:",
    mean_values.index
)

fig2, ax2 = plt.subplots(figsize=(7,4))
ax2.hist(
    df[selected_col],
    bins=10,
    color="#BDE0FE",
    edgecolor="black"
)

ax2.set_title(f"Distribusi Nilai {selected_col}")
ax2.set_xlabel("Nilai")
ax2.set_ylabel("Frekuensi")

st.pyplot(fig2)

st.success("🎯 Dashboard siap digunakan untuk presentasi & analisis!")
