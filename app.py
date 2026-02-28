# =========================================
# EDU ANALYTICS DASHBOARD - PRESENTATION VERSION
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

st.set_page_config(page_title="Edu Analytics Dashboard", layout="wide")

# ===============================
# STYLE
# ===============================
st.markdown("""
    <style>
    .main {background-color: #F8FAFC;}
    h1, h2, h3 {color: #1E3A8A;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Edu Analytics - Dashboard Analisis Soal")
st.markdown("Dashboard analisis kualitas butir soal untuk kebutuhan evaluasi pembelajaran")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)
    data = df.select_dtypes(include=np.number)

    if data.shape[1] == 0:
        st.error("File tidak memiliki kolom numerik.")
        st.stop()

    # ======================================================
    # A. STATISTIK UMUM
    # ======================================================
    st.header("A. Statistik Umum")

    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]
    rata_kelas = round(data.mean().mean(), 2)
    nilai_tertinggi = data.max().max()
    nilai_terendah = data.min().min()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Rata-rata", rata_kelas)
    col4.metric("Nilai Tertinggi", nilai_tertinggi)
    col5.metric("Nilai Terendah", nilai_terendah)

    st.info("""
    Statistik umum memberikan gambaran performa kelas secara keseluruhan.
    Digunakan untuk melihat kualitas hasil tes secara global.
    """)

    st.divider()

    # ======================================================
    # B. DISTRIBUSI NILAI SISWA
    # ======================================================
    st.header("B. Distribusi Nilai Siswa")

    df["Total_Nilai"] = data.sum(axis=1)

    fig1 = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        color_discrete_sequence=["#1E3A8A"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Tujuan Analisis:**
    - Melihat apakah nilai menyebar normal  
    - Mengidentifikasi dominasi nilai rendah/tinggi  
    - Menilai apakah tes terlalu mudah atau sulit  
    """)

    st.divider()

    # ======================================================
    # C. TINGKAT KESULITAN SOAL
    # ======================================================
    st.header("C. Tingkat Kesulitan Soal")

    mean_per_soal = data.mean()

    fig2 = px.bar(
        x=mean_per_soal.index,
        y=mean_per_soal.values,
        title="Rata-rata Skor per Soal"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Interpretasi:**
    - Mean mendekati 1 → Soal mudah  
    - Mean mendekati 0 → Soal sulit  
    """)

    st.divider()

    # ======================================================
    # D. KORELASI ANTAR SOAL
    # ======================================================
    st.header("D. Korelasi Antar Soal")

    corr = data.corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Tujuan:**
    - Melihat apakah soal mengukur kompetensi yang sama  
    - Mendeteksi soal redundan  
    - Menguji konsistensi antar butir  
    """)

    st.divider()

    # ======================================================
    # E. SEGMENTASI SISWA
    # ======================================================
    st.header("E. Segmentasi Siswa (Clustering)")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    fig4 = px.scatter(
        df,
        x=data.columns[0],
        y=data.columns[1],
        color="Cluster",
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    **Tujuan:**
    - Mengelompokkan siswa kemampuan tinggi, sedang, rendah  
    - Dasar strategi remedial dan pengayaan  
    """)

    st.divider()

    # ======================================================
    # F. ANALISIS DAYA PREDIKSI (REGRESI)
    # ======================================================
    st.header("F. Analisis Daya Prediksi (Regresi)")

    if data.shape[1] > 1:
        X = sm.add_constant(data.iloc[:, :-1])
        y = data.iloc[:, -1]

        model = sm.OLS(y, X).fit()
        r2 = round(model.rsquared, 3)

        st.metric("R-Squared Model", r2)

        st.markdown("""
        **Tujuan:**
        - Mengidentifikasi soal yang representatif  
        - Menilai validitas internal tes  
        - R² mendekati 1 → hubungan kuat antar soal  
        """)

    else:
        st.warning("Jumlah soal minimal 2 untuk analisis regresi.")

else:
    st.warning("Silakan upload file Excel untuk memulai analisis.")
