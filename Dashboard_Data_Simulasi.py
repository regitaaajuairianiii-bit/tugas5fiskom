# =========================================
# DASHBOARD ANALISIS SOAL - STREAMLIT
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title="Dashboard Analisis Soal",
    layout="wide"
)

st.title("📊 Dashboard Analisis Soal Simulasi")
st.markdown("Analisis kualitas butir soal dan performa siswa")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    data = df.select_dtypes(include=np.number)

    # =========================
    # STATISTIK UMUM
    # =========================
    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]
    rata_keseluruhan = round(data.mean().mean(), 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Rata-rata Nilai", rata_keseluruhan)

    st.divider()

    # =========================
    # DISTRIBUSI NILAI TOTAL
    # =========================
    st.subheader("📈 Distribusi Nilai Total Siswa")

    df["Total_Nilai"] = data.sum(axis=1)

    fig1 = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        title="Distribusi Total Nilai"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Insight otomatis
    st.info("Distribusi ini menunjukkan apakah tes cenderung mudah, sedang, atau sulit.")

    st.divider()

    # =========================
    # RATA-RATA PER SOAL
    # =========================
    st.subheader("📊 Tingkat Kesulitan Soal")

    mean_per_soal = data.mean().sort_values()

    fig2 = px.bar(
        x=mean_per_soal.index,
        y=mean_per_soal.values,
        title="Rata-rata Skor per Soal"
    )
    fig2.update_layout(
        xaxis_title="Soal",
        yaxis_title="Rata-rata Skor"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.success("Semakin rendah rata-rata, semakin sulit soal tersebut.")

    st.divider()

    # =========================
    # HEATMAP KORELASI
    # =========================
    st.subheader("🔥 Korelasi Antar Soal")

    corr = data.corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        title="Heatmap Korelasi"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info("Korelasi tinggi menunjukkan soal mengukur kompetensi yang sama.")

    st.divider()

    # =========================
    # CLUSTERING SISWA
    # =========================
    st.subheader("👥 Segmentasi Siswa")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    fig4 = px.scatter(
        df,
        x=data.columns[0],
        y=data.columns[1],
        color="Cluster",
        title="Clustering Siswa Berdasarkan Pola Jawaban"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.success("Cluster membantu mengidentifikasi kelompok siswa: rendah, sedang, dan tinggi.")

else:
    st.warning("Silakan upload file Excel terlebih dahulu.")
