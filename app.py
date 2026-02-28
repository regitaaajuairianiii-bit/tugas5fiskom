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
import statsmodels.api as sm

st.set_page_config(
    page_title="Dashboard Analisis Data Simulasi Siswa",
    layout="wide"
)

# ===============================
# STYLE COLOURFUL
# ===============================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
    }
    h1 {
        text-align: center;
        font-weight: 700;
        color: #1D4ED8;
    }
    h2 {
        color: #7C3AED;
    }
    h3 {
        color: #DB2777;
    }
    .stMetric {
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
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
    # B. DISTRIBUSI NILAI SISWA
    # ======================================================
    st.header("B. Distribusi Nilai Siswa")

    df["Total_Nilai"] = data.sum(axis=1)

    fig1 = px.histogram(
        df,
        x="Total_Nilai",
        nbins=10,
        color_discrete_sequence=["#F59E0B"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ======================================================
    # C. ANALISIS PER SOAL (DIPINDAHKAN)
    # ======================================================
    st.header("C. Analisis Per Soal")

    total_score = data.sum(axis=1)
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

    st.divider()

    # ======================================================
    # D. TINGKAT KESULITAN SOAL
    # ======================================================
    st.header("D. Tingkat Kesulitan Soal")

    mean_per_soal = data.mean()

    fig2 = px.bar(
        x=mean_per_soal.index,
        y=mean_per_soal.values,
        color=mean_per_soal.values,
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ======================================================
    # E. KORELASI ANTAR SOAL
    # ======================================================
    st.header("E. Korelasi Antar Soal")

    corr = data.corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Spectral",
        zmin=-1,
        zmax=1
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ======================================================
    # F. SEGMENTASI SISWA
    # ======================================================
    st.header("F. Segmentasi Siswa")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    fig4 = px.scatter(
        df,
        x=data.columns[0],
        y=data.columns[1],
        color="Cluster",
        color_continuous_scale="Rainbow"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ======================================================
    # G. REGRESI
    # ======================================================
    st.header("G. Analisis Daya Prediksi (Regresi)")

    if data.shape[1] > 1:
        X = sm.add_constant(data.iloc[:, :-1])
        y = data.iloc[:, -1]

        model = sm.OLS(y, X).fit()
        r2 = round(model.rsquared, 3)

        st.metric("R-Squared Model", r2)

    st.divider()

    # ======================================================
    # H. KESIMPULAN OTOMATIS
    # ======================================================
    st.header("H. Kesimpulan dan Saran")

    rata_global = data.mean().mean()

    if rata_global >= 0.75:
        kesimpulan = "Tes cenderung mudah bagi mayoritas siswa."
    elif rata_global >= 0.5:
        kesimpulan = "Tes berada pada tingkat kesulitan sedang."
    else:
        kesimpulan = "Tes cenderung sulit bagi siswa."

    saran = """
    • Pertahankan soal dengan daya pembeda tinggi  
    • Revisi soal dengan korelasi item-total rendah  
    • Seimbangkan kembali tingkat kesulitan agar distribusi nilai lebih normal  
    • Gunakan hasil clustering untuk strategi remedial dan pengayaan  
    """

    st.success(f"Kesimpulan: {kesimpulan}")
    st.info("Saran Perbaikan:")
    st.write(saran)

else:
    st.warning("Silakan upload file Excel untuk memulai analisis.")
