# =========================================
# DASHBOARD ANALISIS SOAL SIMULASI
# =========================================

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import plotly.io as pio

pio.templates.default = "plotly_white"

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("data_simulasi_50_siswa_20_soal.xlsx")
data = df.select_dtypes(include=np.number)

# =========================
# STATISTIK UMUM
# =========================
jumlah_siswa = len(df)
jumlah_soal = data.shape[1]
rata_keseluruhan = round(data.mean().mean(), 2)

print("Jumlah Siswa :", jumlah_siswa)
print("Jumlah Soal  :", jumlah_soal)
print("Rata-rata    :", rata_keseluruhan)

# =========================
# 1. HISTOGRAM NILAI TOTAL
# =========================
df["Total_Nilai"] = data.sum(axis=1)

fig1 = px.histogram(
    df,
    x="Total_Nilai",
    nbins=10,
    title="Distribusi Total Nilai Siswa"
)
fig1.show()

# =========================
# 2. RATA-RATA PER SOAL
# =========================
mean_per_soal = data.mean().sort_values()

fig2 = px.bar(
    x=mean_per_soal.index,
    y=mean_per_soal.values,
    title="Tingkat Kesulitan Soal (Rata-rata Skor)"
)
fig2.update_layout(
    xaxis_title="Soal",
    yaxis_title="Rata-rata Skor"
)
fig2.show()

# =========================
# 3. HEATMAP KORELASI
# =========================
corr = data.corr()

fig3 = px.imshow(
    corr,
    text_auto=True,
    title="Korelasi Antar Soal",
    zmin=-1,
    zmax=1
)
fig3.show()

# =========================
# 4. CLUSTERING SISWA
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

fig4 = px.scatter(
    df,
    x=data.columns[0],
    y=data.columns[1],
    color="Cluster",
    title="Segmentasi Siswa"
)
fig4.show()

# =========================
# 5. REGRESI (VALIDITAS INTERNAL)
# =========================
X = sm.add_constant(data.iloc[:, :-1])
y = data.iloc[:, -1]

model = sm.OLS(y, X).fit()

print("\nR-Squared Model :", round(model.rsquared, 3))
