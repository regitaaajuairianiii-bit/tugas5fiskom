# =========================================
# DASHBOARD ANALISIS DATA SIMULASI SISWA
# VERSI AKADEMIS LENGKAP
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

    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]

    skor_min = data.min().min()
    skor_max = data.max().max()

    nilai_maks_teoritis = jumlah_soal * skor_max

    df["Total_Nilai"] = data.sum(axis=1)
    rata_kelas = df["Total_Nilai"].mean()
    median_nilai = df["Total_Nilai"].median()
    nilai_tertinggi = df["Total_Nilai"].max()
    nilai_terendah = df["Total_Nilai"].min()

    # ======================================================
    # A. STATISTIK UMUM
    # ======================================================
    st.header("A. Statistik Umum")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Nilai Tertinggi", round(nilai_tertinggi,2))
    col4.metric("Nilai Terendah", round(nilai_terendah,2))

    st.metric("Rata-rata Total", round(rata_kelas,2))

    st.divider()

    # ======================================================
    # B. DISTRIBUSI SOAL
    # ======================================================
    st.header("B. Distribusi Soal (Rata-rata Skor)")

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
        yaxis=dict(range=[skor_min, max_mean + 0.05])
    )

    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ======================================================
    # C. ANALISIS PER SOAL LENGKAP
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
        px.histogram(data[soal_pilih], color_discrete_sequence=["#A5B4FC"]),
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

    st.plotly_chart(px.line(x=list(K_range), y=inertia, markers=True))
    st.plotly_chart(px.line(x=list(K_range), y=silhouette_scores, markers=True))

    st.divider()

    # ======================================================
    # E. SEGMENTASI SISWA + INTERPRETASI DETAIL
    # ======================================================
    st.header("E. Segmentasi Siswa")

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

    cluster_summary = df.groupby("Cluster")["Total_Nilai"].agg(["count","mean"]).reset_index()
    cluster_summary.columns = ["Cluster","Jumlah Siswa","Rata-rata Nilai"]

    cluster_summary["Persentase (%)"] = round(
        cluster_summary["Jumlah Siswa"]/jumlah_siswa*100,2
    )

    st.dataframe(cluster_summary, use_container_width=True)

    st.subheader("Interpretasi Karakteristik Tiap Cluster")

    for i in cluster_summary["Cluster"]:
        mean_cluster = cluster_summary.loc[cluster_summary["Cluster"]==i,"Rata-rata Nilai"].values[0]
        jumlah_cluster = cluster_summary.loc[cluster_summary["Cluster"]==i,"Jumlah Siswa"].values[0]
        persen_cluster = cluster_summary.loc[cluster_summary["Cluster"]==i,"Persentase (%)"].values[0]

        if mean_cluster > rata_kelas:
            karakter = "memiliki performa di atas rata-rata kelas dan menunjukkan penguasaan materi yang baik."
        elif mean_cluster < rata_kelas:
            karakter = "memiliki performa di bawah rata-rata kelas dan memerlukan pendampingan tambahan."
        else:
            karakter = "memiliki performa yang relatif stabil dan mendekati rata-rata kelas."

        st.write(f"""
Cluster {i} terdiri dari {jumlah_cluster} siswa ({persen_cluster}%).
Kelompok ini {karakter}
""")

    st.divider()

    # ======================================================
    # F. REGRESI
    # ======================================================
    st.header("F. Analisis Regresi")

    if jumlah_soal > 1:
        X = sm.add_constant(data.iloc[:,:-1])
        y = data.iloc[:,-1]
        model = sm.OLS(y,X).fit()
        st.metric("R-Squared", round(model.rsquared,3))

    st.divider()

    # ======================================================
    # G. KESIMPULAN BERBASIS DATA
    # ======================================================
    st.header("G. Kesimpulan Analitis")

    proporsi = rata_kelas / nilai_maks_teoritis
    persen_diatas_rata = (df["Total_Nilai"] > rata_kelas).mean() * 100

    if proporsi >= 0.75:
        kategori = "cenderung mudah"
    elif proporsi >= 0.5:
        kategori = "tingkat kesulitan sedang"
    else:
        kategori = "cenderung sulit"

    st.success(f"""
Rata-rata total siswa adalah {round(rata_kelas,2)} dari maksimum teoritis {nilai_maks_teoritis}.
Proporsi pencapaian terhadap skor maksimum sebesar {round(proporsi*100,2)}%.
Sebanyak {round(persen_diatas_rata,2)}% siswa berada di atas rata-rata kelas.

Distribusi skor per soal menunjukkan kecenderungan nilai berada pada rentang atas.
Berdasarkan indikator tersebut, tes dapat dikategorikan sebagai **{kategori}**.
""")

else:
    st.warning("Upload file Excel untuk memulai analisis.")
