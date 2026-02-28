# =========================================
# DASHBOARD ANALISIS SOAL - PREMIUM VERSION
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Edu Analytics Dashboard",
    layout="wide"
)

# ===============================
# CUSTOM THEME
# ===============================
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Edu Analytics - Dashboard Analisis Soal")
st.markdown("Analisis kualitas butir soal berbasis data simulasi")

# ===============================
# FILE UPLOAD
# ===============================
uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)
    data = df.select_dtypes(include=np.number)

    # ===============================
    # STATISTIK UMUM
    # ===============================
    jumlah_siswa = len(df)
    jumlah_soal = data.shape[1]
    rata_kelas = round(data.mean().mean(), 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("Jumlah Siswa", jumlah_siswa)
    col2.metric("Jumlah Soal", jumlah_soal)
    col3.metric("Rata-rata Kelas", rata_kelas)

    st.divider()

    # ===============================
    # DISTRIBUSI NILAI TOTAL
    # ===============================
    st.subheader("📈 Distribusi Nilai Total")

    df["Total_Nilai"] = data.sum(axis=1)

    fig1 = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        color_discrete_sequence=["#1E3A8A"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ===============================
    # INDEKS KESUKARAN
    # ===============================
    st.subheader("📊 Analisis Indeks Kesukaran Soal")

    mean_per_soal = data.mean()

    def kategori_kesukaran(x):
        if x >= 0.80:
            return "Sangat Mudah"
        elif x >= 0.60:
            return "Mudah"
        elif x >= 0.40:
            return "Sedang"
        elif x >= 0.20:
            return "Sulit"
        else:
            return "Sangat Sulit"

    indeks_df = pd.DataFrame({
        "Soal": mean_per_soal.index,
        "Indeks Kesukaran": mean_per_soal.values,
        "Kategori": mean_per_soal.apply(kategori_kesukaran).values
    }).sort_values("Indeks Kesukaran")

    fig2 = px.bar(
        indeks_df,
        x="Soal",
        y="Indeks Kesukaran",
        color="Kategori",
        color_discrete_map={
            "Sangat Mudah": "#16A34A",
            "Mudah": "#22C55E",
            "Sedang": "#EAB308",
            "Sulit": "#F97316",
            "Sangat Sulit": "#DC2626"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(indeks_df, use_container_width=True)

    st.info("Indeks kesukaran = proporsi siswa yang menjawab benar.")

    st.divider()

    # ===============================
    # RADAR CHART KOMPETENSI
    # ===============================
    st.subheader("🕸 Radar Chart Kompetensi")

    rata_per_soal = data.mean()

    fig3 = go.Figure()

    fig3.add_trace(go.Scatterpolar(
        r=rata_per_soal.values,
        theta=rata_per_soal.index,
        fill='toself',
        line=dict(color="#1E3A8A")
    ))

    fig3.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.success("Radar chart menunjukkan kekuatan dan kelemahan kompetensi pada tiap soal.")

    st.divider()

    # ===============================
    # CLUSTERING SISWA
    # ===============================
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
        color_continuous_scale="viridis"
    )

    st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Silakan upload file Excel untuk memulai analisis.")
