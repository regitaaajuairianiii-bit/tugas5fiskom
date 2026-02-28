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

# ===============================
# STYLE SOFT COLOR
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
**NIM : 06111282429048**  
**Kelas : B / Indralaya**  
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

    df["Total_Nilai"] = data.sum(axis=1)

    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]
    rata_kelas = df["Total_Nilai"].mean()
    median_nilai = df["Total_Nilai"].median()
    nilai_tertinggi = df["Total_Nilai"].max()
    nilai_terendah = df["Total_Nilai"].min()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Rata-rata", round(rata_kelas,2))
    col4.metric("Nilai Tertinggi", round(nilai_tertinggi,2))
    col5.metric("Nilai Terendah", round(nilai_terendah,2))

    st.divider()

    # ======================================================
    # B. DISTRIBUSI SOAL (DINAMIS SESUAI DATA)
    # ======================================================
    st.header("B. Distribusi Soal (Rata-rata Skor per Soal)")

    mean_per_soal = data.mean().reset_index()
    mean_per_soal.columns = ["Soal", "Rata-rata Skor"]

    fig1 = px.bar(
        mean_per_soal,
        x="Soal",
        y="Rata-rata Skor",
        color="Rata-rata Skor",
        color_continuous_scale="Blues"
    )

    max_mean = mean_per_soal["Rata-rata Skor"].max()

    fig1.update_layout(
        yaxis=dict(range=[0, max_mean + 0.05]),
        xaxis_title="Nomor Soal",
        yaxis_title="Rata-rata Skor"
    )

    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    st.plotly_chart(fig1, use_container_width=True)

    st.info("Mean mendekati nilai maksimum → soal mudah | Mendekati 0 → soal sulit")

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
        discrimination = df_temp.head(n)["item"].mean() - df_temp.tail(n)["item"].mean()
        item_total_corr = skor_item.corr(total_score)

        hasil_item.append({
            "Soal": col,
            "Indeks Kesukaran": round(p_value,3),
            "Daya Pembeda": round(discrimination,3),
            "Korelasi Item-Total": round(item_total_corr,3)
        })

    item_df = pd.DataFrame(hasil_item)
    st.dataframe(item_df, use_container_width=True)

    soal_pilih = st.selectbox("Pilih Soal untuk Analisis Detail", data.columns)

    colA, colB = st.columns(2)

    colA.plotly_chart(
        px.histogram(data[soal_pilih],
                     color_discrete_sequence=["#A5B4FC"]),
        use_container_width=True
    )

    colB.plotly_chart(
        px.scatter(x=total_score, y=data[soal_pilih],
                   color_discrete_sequence=["#FBCFE8"]),
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # D. VALIDASI CLUSTER
    # ======================================================
    st.header("D. Validasi Jumlah Cluster")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    inertia = []
    silhouette_scores = []
    K_range = range(2,6)

    for k in K_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        inertia.append(model.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, labels))

    st.plotly_chart(px.line(x=list(K_range), y=inertia, markers=True),
                    use_container_width=True)

    st.plotly_chart(px.line(x=list(K_range), y=silhouette_scores, markers=True),
                    use_container_width=True)

    st.divider()

    # ======================================================
    # E. SEGMENTASI SISWA
    # ======================================================
    st.header("E. Segmentasi Siswa (K-Means + PCA)")

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

    centroids_pca = pca.transform(kmeans.cluster_centers_)

    fig_cluster = px.scatter(
        pca_df,
        x=pca_df.columns[0],
        y=pca_df.columns[1],
        color="Cluster",
        color_discrete_sequence=["#A5B4FC","#FBCFE8","#86EFAC"]
    )

    fig_cluster.add_trace(
        go.Scatter(
            x=centroids_pca[:,0],
            y=centroids_pca[:,1],
            mode="markers",
            marker=dict(symbol="x", size=18, color="black"),
            name="Centroid"
        )
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.divider()

    # ======================================================
    # F. KESIMPULAN
    # ======================================================
    st.header("F. Kesimpulan")

    mean_global = df["Total_Nilai"].mean()

    if rata_kelas >= jumlah_soal * 0.75:
        tingkat = "cenderung mudah"
    elif rata_kelas >= jumlah_soal * 0.5:
        tingkat = "tingkat kesulitan sedang"
    else:
        tingkat = "cenderung sulit"

    st.success(f"""
Rata-rata kelas = {round(rata_kelas,2)}  
Median = {round(median_nilai,2)}  

Distribusi skor per soal menunjukkan variasi tingkat kesukaran.
Berdasarkan rata-rata keseluruhan dan sebaran skor,
tes dapat dikategorikan sebagai **{tingkat}**.
""")

else:
    st.warning("Upload file Excel untuk memulai analisis.")
