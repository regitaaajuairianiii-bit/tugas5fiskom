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

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Analisis Data Simulasi Siswa",
    layout="wide"
)

# ===============================
# HEADER
# ===============================
st.title("📊 DASHBOARD ANALISIS DATA SIMULASI SISWA")
st.markdown("**Nama : Regita Juairiani**")
st.markdown("**NIM  : 06111282429048**")
st.markdown("**Kelas : B / Indralaya**")
st.markdown("**Mata Kuliah : Fisika Komputasi**")
st.divider()

# ===============================
# UPLOAD FILE
# ===============================
uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)
    data = df.select_dtypes(include=np.number)

    # ===============================
    # HITUNG TOTAL NILAI
    # ===============================
    df["Total_Nilai"] = data.sum(axis=1)

    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]
    rata_kelas = df["Total_Nilai"].mean()
    nilai_tertinggi = df["Total_Nilai"].max()
    nilai_terendah = df["Total_Nilai"].min()

    # ===============================
    # A. STATISTIK UMUM
    # ===============================
    st.header("A. Statistik Umum")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Nilai Tertinggi", round(nilai_tertinggi,2))
    col4.metric("Nilai Terendah", round(nilai_terendah,2))

    st.metric("Rata-rata Total", round(rata_kelas,2))
    st.divider()

    # ===============================
    # B. DISTRIBUSI NILAI
    # ===============================
    st.header("B. Distribusi Nilai Siswa")

    fig_hist = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        color_discrete_sequence=["#6C8EBF"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    # ===============================
    # C. DISTRIBUSI SOAL (RATA-RATA)
    # ===============================
    st.header("C. Distribusi Soal (Rata-rata Skor per Soal)")

    mean_per_soal = data.mean()

    fig_bar = px.bar(
        x=mean_per_soal.index,
        y=mean_per_soal.values,
        labels={"x": "Nomor Soal", "y": "Rata-rata Skor"},
        color=mean_per_soal.values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # ===============================
    # D. ANALISIS PER SOAL INTERAKTIF
    # ===============================
    st.header("D. Analisis Per Soal")

    pilihan_soal = st.selectbox("Pilih Nomor Soal", data.columns)

    fig_item = px.histogram(
        df,
        x=pilihan_soal,
        nbins=5,
        color_discrete_sequence=["#A8DADC"]
    )
    st.plotly_chart(fig_item, use_container_width=True)

    st.divider()

    # ===============================
    # E. SEGMENTASI SISWA
    # ===============================
    st.header("E. Segmentasi Siswa (K-Means + PCA)")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    # Elbow Method
    inertia = []
    for k in range(1,6):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertia.append(km.inertia_)

    fig_elbow = px.line(
        x=range(1,6),
        y=inertia,
        markers=True,
        labels={"x": "Jumlah Cluster", "y": "Inertia"},
        title="Elbow Method"
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

    # Clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster = kmeans.fit_predict(X_scaled)
    df["Cluster"] = cluster

    silhouette = silhouette_score(X_scaled, cluster)
    st.write(f"Silhouette Score: {round(silhouette,3)}")

    # PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)

    df["PC1"] = pca_result[:,0]
    df["PC2"] = pca_result[:,1]

    explained_var = pca.explained_variance_ratio_

    fig_cluster = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color="Cluster",
        title=f"PCA Projection (PC1={round(explained_var[0]*100,1)}%, PC2={round(explained_var[1]*100,1)}%)",
        color_discrete_sequence=["#8ECAE6","#219EBC","#023047"]
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

    # Distribusi Cluster
    cluster_count = df["Cluster"].value_counts().sort_index()
    fig_pie = px.pie(
        values=cluster_count.values,
        names=[f"Cluster {i}" for i in cluster_count.index],
        color_discrete_sequence=["#8ECAE6","#219EBC","#023047"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Interpretasi Cluster
    st.subheader("Makna dan Karakteristik Tiap Cluster")

    cluster_mean = df.groupby("Cluster")["Total_Nilai"].mean()

    interpretasi = []
    for i in cluster_mean.index:
        if cluster_mean[i] > rata_kelas:
            ket = "Kelompok siswa dengan performa tinggi"
        elif cluster_mean[i] < rata_kelas:
            ket = "Kelompok siswa dengan performa rendah"
        else:
            ket = "Kelompok siswa dengan performa sedang"
        interpretasi.append([i, round(cluster_mean[i],2), ket])

    interpretasi_df = pd.DataFrame(
        interpretasi,
        columns=["Cluster","Rata-rata Nilai","Keterangan"]
    )

    st.dataframe(interpretasi_df, use_container_width=True)

    st.divider()

    # ===============================
    # F. KESIMPULAN ANALITIS
    # ===============================
    st.header("F. Kesimpulan Analitis")

    persen_diatas_rata = (df["Total_Nilai"] > rata_kelas).mean() * 100

    if persen_diatas_rata > 65:
        kategori_tes = "Tes tergolong mudah"
    elif persen_diatas_rata < 35:
        kategori_tes = "Tes tergolong sulit"
    else:
        kategori_tes = "Tes tergolong sedang"

    st.success(f"""
Rata-rata nilai siswa adalah {round(rata_kelas,2)}.
Nilai tertinggi adalah {round(nilai_tertinggi,2)} dan nilai terendah {round(nilai_terendah,2)}.

Sebanyak {round(persen_diatas_rata,2)}% siswa memperoleh nilai di atas rata-rata kelas.

Berdasarkan distribusi nilai aktual, {kategori_tes}.
""")

else:
    st.warning("Silakan upload file Excel untuk memulai analisis.")
