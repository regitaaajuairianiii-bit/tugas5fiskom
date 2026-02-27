# =====================================================
# DASHBOARD ANALISIS SOAL - GOOGLE COLAB VERSION
# =====================================================

# Install library (jika belum ada)
!pip install plotly openpyxl scikit-learn --quiet

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from google.colab import files
import io

# ============================
# UPLOAD FILE
# ============================
print("Silakan upload file Excel Anda")
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
df = pd.read_excel(io.BytesIO(uploaded[file_name]))

data = df.select_dtypes(include=np.number)

print("\n===== STATISTIK UMUM =====")
print("Jumlah Siswa :", len(df))
print("Jumlah Soal  :", data.shape[1])
print("Rata-rata Kelas :", round(data.mean().mean(),2))

# ============================
# DISTRIBUSI NILAI TOTAL
# ============================
df["Total_Nilai"] = data.sum(axis=1)

fig1 = px.histogram(
    df,
    x="Total_Nilai",
    nbins=10,
    title="Distribusi Total Nilai Siswa",
    color_discrete_sequence=["#1E3A8A"]
)

fig1.update_layout(template="plotly_white")
fig1.show()

# ============================
# ANALISIS INDEKS KESUKARAN
# ============================
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

print("\n===== INDEKS KESUKARAN =====")
display(indeks_df)

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
    },
    title="Tingkat Kesukaran Soal"
)

fig2.update_layout(template="plotly_white")
fig2.show()

# ============================
# RADAR CHART KOMPETENSI
# ============================
fig3 = go.Figure()

fig3.add_trace(go.Scatterpolar(
    r=mean_per_soal.values,
    theta=mean_per_soal.index,
    fill='toself',
    line=dict(color="#1E3A8A")
))

fig3.update_layout(
    title="Radar Chart Kompetensi",
    polar=dict(radialaxis=dict(visible=True, range=[0,1])),
    showlegend=False,
    template="plotly_white"
)

fig3.show()

# ============================
# CLUSTERING SISWA
# ============================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

fig4 = px.scatter(
    df,
    x=data.columns[0],
    y=data.columns[1],
    color="Cluster",
    title="Segmentasi Siswa",
    color_continuous_scale="viridis"
)

fig4.update_layout(template="plotly_white")
fig4.show()

print("\n===== INTERPRETASI =====")
print("• Histogram → Melihat distribusi kemampuan siswa")
print("• Indeks Kesukaran → Mengidentifikasi soal mudah/sulit")
print("• Radar Chart → Visualisasi kekuatan & kelemahan kompetensi")
print("• Clustering → Segmentasi siswa (rendah, sedang, tinggi)")
