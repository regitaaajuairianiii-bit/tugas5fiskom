# =========================================
# DASHBOARD ANALISIS DATA SIMULASI SISWA
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import statsmodels.api as sm

st.set_page_config(
    page_title="Dashboard Analisis Data Simulasi Siswa",
    layout="wide"
)

st.title("📊 DASHBOARD ANALISIS DATA SIMULASI SISWA")

st.markdown("""
### 👤 Identitas Mahasiswa  
**Nama : Regita Juairiani**  
**NIM : 06111282429048**  
**Kelas : B / Indralaya**  
**Mata Kuliah : Fisika Komputasi**
""")

st.markdown("---")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Ambil hanya kolom numerik
    data = df.select_dtypes(include=np.number)

    if data.shape[1] == 0:
        st.error("File tidak memiliki kolom numerik.")
        st.stop()

    # ======================================================
    # DETEKSI SKALA DATA ASLI
    # ======================================================
    skor_min = data.min().min()
    skor_max = data.max().max()

    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]

    nilai_maks_teoritis = jumlah_soal * skor_max
    nilai_min_teoritis = jumlah_soal * skor_min

    df["Total_Nilai"] = data.sum(axis=1)

    rata_kelas = df["Total_Nilai"].mean()
    median_nilai = df["Total_Nilai"].median()
    nilai_tertinggi = df["Total_Nilai"].max()
    nilai_terendah = df["Total_Nilai"].min()

    # ======================================================
    # A. STATISTIK UMUM
    # ======================================================
    st.header("A. Statistik Umum")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Skor Maks per Soal", skor_max)

    col4, col5, col6 = st.columns(3)
    col4.metric("Rata-rata Total", round(rata_kelas,2))
    col5.metric("Nilai Tertinggi", round(nilai_tertinggi,2))
    col6.metric("Nilai Terendah", round(nilai_terendah,2))

    st.info(f"""
Nilai maksimum teoritis = {nilai_maks_teoritis}  
Nilai minimum teoritis = {nilai_min_teoritis}
""")

    st.divider()

    # ======================================================
    # B. DISTRIBUSI SOAL (RATA-RATA ASLI)
    # ======================================================
    st.header("B. Distribusi Soal")

    mean_per_soal = data.mean().reset_index()
    mean_per_soal.columns = ["Soal", "Rata-rata Skor"]

    max_mean = mean_per_soal["Rata-rata Skor"].max()

    fig1 = px.bar(
        mean_per_soal,
        x="Soal",
        y="Rata-rata Skor",
        color="Rata-rata Skor",
        color_continuous_scale="Blues"
    )

    fig1.update_layout(
        yaxis=dict(range=[skor_min, max_mean + 0.05]),
        xaxis_title="Nomor Soal",
        yaxis_title="Rata-rata Skor"
    )

    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ======================================================
    # C. CLUSTERING SISWA (DATA ASLI)
    # ======================================================
    st.header("C. Segmentasi Siswa")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    explained_var = pca.explained_variance_ratio_

    pca_df = pd.DataFrame(
        components,
        columns=[f"PC1 ({round(explained_var[0]*100,2)}%)",
                 f"PC2 ({round(explained_var[1]*100,2)}%)"]
    )
    pca_df["Cluster"] = df["Cluster"].astype(str)

    fig_cluster = px.scatter(
        pca_df,
        x=pca_df.columns[0],
        y=pca_df.columns[1],
        color="Cluster"
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.divider()

    # ======================================================
    # D. REGRESI
    # ======================================================
    st.header("D. Analisis Regresi")

    if jumlah_soal > 1:
        X = sm.add_constant(data.iloc[:,:-1])
        y = data.iloc[:,-1]
        model = sm.OLS(y,X).fit()
        st.metric("R-Squared", round(model.rsquared,3))

    st.divider()

    # ======================================================
    # E. KESIMPULAN OTOMATIS
    # ======================================================
    st.header("E. Kesimpulan")

    proporsi = rata_kelas / nilai_maks_teoritis

    if proporsi >= 0.75:
        kategori = "Tes cenderung mudah"
    elif proporsi >= 0.5:
        kategori = "Tes tingkat kesulitan sedang"
    else:
        kategori = "Tes cenderung sulit"

    st.success(f"""
Rata-rata total siswa adalah {round(rata_kelas,2)} dari maksimum teoritis {nilai_maks_teoritis}.  

Proporsi pencapaian = {round(proporsi*100,2)}%  

Kesimpulan: **{kategori}**
""")

else:
    st.warning("Upload file Excel untuk memulai analisis.")
