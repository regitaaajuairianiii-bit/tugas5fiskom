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
import statsmodels.api as sm

st.set_page_config(
    page_title="Dashboard Analisis Data Simulasi Siswa",
    layout="wide"
)

# ===============================
# STYLE SOFT ACADEMIC
# ===============================
st.markdown("""
    <style>
    .main {background-color: #F8FAFC;}
    h1 {text-align:center; color:#334155;}
    h2 {color:#475569;}
    .stMetric {
        background-color:#FFFFFF;
        padding:15px;
        border-radius:12px;
        box-shadow:0px 3px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 DASHBOARD ANALISIS DATA SIMULASI SISWA")

st.markdown("""
### 👤 Identitas Mahasiswa  
**Nama : Regita Juairiani**  
**NIM : __________________**  
**Kelas : __________________**  
**Mata Kuliah : Fisika Komputasi**
""")

st.markdown("---")

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

    st.divider()

    # ======================================================
    # B. DISTRIBUSI NILAI
    # ======================================================
    st.header("B. Distribusi Nilai Siswa")

    df["Total_Nilai"] = data.sum(axis=1)

    fig1 = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        color_discrete_sequence=["#94A3B8"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ======================================================
    # C. ANALISIS PER SOAL
    # ======================================================
    st.header("C. Analisis Per Soal")

    total_score = df["Total_Nilai"]
    hasil_item = []

    for col in data.columns:
        skor_item = data[col]
        p_value = skor_item.mean()

        df_temp = pd.DataFrame({
            "item": skor_item,
            "total": total_score
        }).sort_values("total", ascending=False)

        n = int(len(df_temp) * 0.27)

        kelompok_atas = df_temp.head(n)["item"].mean()
        kelompok_bawah = df_temp.tail(n)["item"].mean()

        discrimination = kelompok_atas - kelompok_bawah
        item_total_corr = skor_item.corr(total_score)

        hasil_item.append({
            "Soal": col,
            "Indeks Kesukaran": round(p_value, 3),
            "Daya Pembeda": round(discrimination, 3),
            "Korelasi Item-Total": round(item_total_corr, 3)
        })

    item_df = pd.DataFrame(hasil_item)
    st.dataframe(item_df, use_container_width=True)

    soal_pilih = st.selectbox("🎯 Pilih Soal untuk Analisis Detail", data.columns)

    colA, colB = st.columns(2)

    fig_dist = px.histogram(
        data[soal_pilih],
        nbins=5,
        color_discrete_sequence=["#A5B4FC"]
    )
    colA.plotly_chart(fig_dist, use_container_width=True)

    fig_scatter = px.scatter(
        x=total_score,
        y=data[soal_pilih],
        color_discrete_sequence=["#FBCFE8"]
    )
    colB.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # ======================================================
    # D. KORELASI
    # ======================================================
    st.header("D. Korelasi Antar Soal")

    corr = data.corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Blues")
    st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()

    # ======================================================
    # E. SEGMENTASI SISWA (FINAL UPGRADE)
    # ======================================================
    st.header("E. Segmentasi Siswa")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    explained_var = pca.explained_variance_ratio_

    pca_df = pd.DataFrame(
        components,
        columns=[
            f"PC1 ({round(explained_var[0]*100,2)}%)",
            f"PC2 ({round(explained_var[1]*100,2)}%)"
        ]
    )

    pca_df["Cluster"] = df["Cluster"].astype(str)

    centroids_pca = pca.transform(kmeans.cluster_centers_)
    centroid_df = pd.DataFrame(centroids_pca, columns=pca_df.columns[:2])

    fig_cluster = px.scatter(
        pca_df,
        x=pca_df.columns[0],
        y=pca_df.columns[1],
        color="Cluster",
        color_discrete_sequence=["#A5B4FC", "#FBCFE8", "#86EFAC"]
    )

    fig_cluster.add_trace(
        go.Scatter(
            x=centroid_df.iloc[:,0],
            y=centroid_df.iloc[:,1],
            mode="markers",
            marker=dict(symbol="x", size=18, color="black"),
            name="Centroid"
        )
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    # ======================================================
    # KARAKTERISTIK CLUSTER
    # ======================================================
    st.subheader("Makna dan Karakteristik Tiap Cluster")

    cluster_summary = df.groupby("Cluster")["Total_Nilai"].agg(["count","mean"]).reset_index()
    cluster_summary.columns = ["Cluster","Jumlah Siswa","Rata-rata Total Nilai"]

    mean_global = df["Total_Nilai"].mean()
    std_global = df["Total_Nilai"].std()

    def kategori_cluster(x):
        if x >= mean_global + 0.3*std_global:
            return "Siswa Berprestasi"
        elif x <= mean_global - 0.3*std_global:
            return "Perlu Pendampingan"
        else:
            return "Siswa Stabil"

    cluster_summary["Keterangan"] = cluster_summary["Rata-rata Total Nilai"].apply(kategori_cluster)
    cluster_summary["Persentase (%)"] = round(
        cluster_summary["Jumlah Siswa"]/jumlah_siswa*100,2
    )

    st.dataframe(cluster_summary, use_container_width=True)

    fig_pie = px.pie(
        cluster_summary,
        names="Cluster",
        values="Jumlah Siswa",
        color_discrete_sequence=["#A5B4FC","#FBCFE8","#86EFAC"]
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # ======================================================
    # F. REGRESI
    # ======================================================
    st.header("F. Analisis Regresi")

    if data.shape[1] > 1:
        X = sm.add_constant(data.iloc[:, :-1])
        y = data.iloc[:, -1]
        model = sm.OLS(y, X).fit()
        st.metric("R-Squared Model", round(model.rsquared,3))

    st.divider()

    # ======================================================
    # G. KESIMPULAN
    # ======================================================
    st.header("G. Kesimpulan dan Saran")

    if rata_kelas >= 0.75:
        kesimpulan = "Tes cenderung mudah."
    elif rata_kelas >= 0.5:
        kesimpulan = "Tes tingkat kesulitan sedang."
    else:
        kesimpulan = "Tes cenderung sulit."

    st.success(f"Kesimpulan: {kesimpulan}")

    st.info("""
Saran:
- Pertahankan soal dengan daya pembeda tinggi
- Revisi soal dengan korelasi rendah
- Gunakan hasil clustering untuk strategi diferensiasi pembelajaran
""")

else:
    st.warning("Silakan upload file Excel untuk memulai analisis.")
