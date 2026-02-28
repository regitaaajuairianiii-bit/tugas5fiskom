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
    # B. DISTRIBUSI SOAL (RATA-RATA SKOR PER SOAL)
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

    fig1.update_layout(
        yaxis=dict(range=[0,1]),
        xaxis_title="Nomor Soal",
        yaxis_title="Rata-rata Skor"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.info("Mean mendekati 1 → soal mudah | Mendekati 0 → soal sulit")

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

    st.plotly_chart(px.line(x=list(K_range), y=inertia, markers=True,
                            title="Elbow Method"),
                    use_container_width=True)

    st.plotly_chart(px.line(x=list(K_range), y=silhouette_scores, markers=True,
                            title="Silhouette Score"),
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

    # Ringkasan Cluster
    cluster_summary = df.groupby("Cluster")["Total_Nilai"].agg(["count","mean"]).reset_index()
    cluster_summary.columns = ["Cluster","Jumlah Siswa","Rata-rata Nilai"]

    mean_global = df["Total_Nilai"].mean()
    std_global = df["Total_Nilai"].std()

    def kategori(x):
        if x >= mean_global + 0.3*std_global:
            return "Siswa Berprestasi"
        elif x <= mean_global - 0.3*std_global:
            return "Perlu Pendampingan"
        else:
            return "Siswa Stabil"

    cluster_summary["Keterangan"] = cluster_summary["Rata-rata Nilai"].apply(kategori)
    cluster_summary["Persentase (%)"] = round(
        cluster_summary["Jumlah Siswa"]/jumlah_siswa*100,2
    )

    st.dataframe(cluster_summary, use_container_width=True)

    st.divider()

    # ======================================================
    # F. REGRESI
    # ======================================================
    st.header("F. Analisis Regresi")

    if data.shape[1] > 1:
        X = sm.add_constant(data.iloc[:,:-1])
        y = data.iloc[:,-1]
        model = sm.OLS(y,X).fit()
        st.metric("R-Squared Model", round(model.rsquared,3))

    st.divider()

    # ======================================================
    # G. KESIMPULAN
    # ======================================================
    st.header("G. Kesimpulan")

    proporsi_tinggi = round(
        (df["Total_Nilai"] > mean_global).mean()*100,2
    )

    if rata_kelas >= data.shape[1]*0.75:
        tingkat = "cenderung mudah"
    elif rata_kelas >= data.shape[1]*0.5:
        tingkat = "tingkat kesulitan sedang"
    else:
        tingkat = "cenderung sulit"

    st.success(f"""
Rata-rata kelas = {round(rata_kelas,2)}  
Median = {round(median_nilai,2)}  
{proporsi_tinggi}% siswa berada di atas rata-rata.  

Berdasarkan distribusi skor per soal dan performa keseluruhan,
tes dapat dikategorikan sebagai **{tingkat}**.
""")

else:
    st.warning("Upload file Excel untuk memulai analisis.")
