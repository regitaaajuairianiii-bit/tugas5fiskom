{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMNKtXrT5a0/4hxRGgwJrnq",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/regitaaajuairianiii-bit/tugas5fiskom/blob/main/Dashboard_Data_Simulasi.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 373
        },
        "id": "0RSEM-ad7bsd",
        "outputId": "51045d88-ffbe-497d-e2ac-2e7c7561c7d0"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "FileNotFoundError",
          "evalue": "[Errno 2] No such file or directory: 'data_simulasi_50_siswa_20_soal.xlsx'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-200/667639090.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     17\u001b[0m \u001b[0;31m# LOAD DATA\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     18\u001b[0m \u001b[0;31m# =========================\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 19\u001b[0;31m \u001b[0mdf\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread_excel\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"data_simulasi_50_siswa_20_soal.xlsx\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     20\u001b[0m \u001b[0mdata\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mselect_dtypes\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0minclude\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mnp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mnumber\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     21\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/excel/_base.py\u001b[0m in \u001b[0;36mread_excel\u001b[0;34m(io, sheet_name, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skiprows, nrows, na_values, keep_default_na, na_filter, verbose, parse_dates, date_parser, date_format, thousands, decimal, comment, skipfooter, storage_options, dtype_backend, engine_kwargs)\u001b[0m\n\u001b[1;32m    493\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0misinstance\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mExcelFile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    494\u001b[0m         \u001b[0mshould_close\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 495\u001b[0;31m         io = ExcelFile(\n\u001b[0m\u001b[1;32m    496\u001b[0m             \u001b[0mio\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    497\u001b[0m             \u001b[0mstorage_options\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstorage_options\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/excel/_base.py\u001b[0m in \u001b[0;36m__init__\u001b[0;34m(self, path_or_buffer, engine, storage_options, engine_kwargs)\u001b[0m\n\u001b[1;32m   1548\u001b[0m                 \u001b[0mext\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"xls\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1549\u001b[0m             \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1550\u001b[0;31m                 ext = inspect_excel_format(\n\u001b[0m\u001b[1;32m   1551\u001b[0m                     \u001b[0mcontent_or_path\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mpath_or_buffer\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstorage_options\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstorage_options\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1552\u001b[0m                 )\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/excel/_base.py\u001b[0m in \u001b[0;36minspect_excel_format\u001b[0;34m(content_or_path, storage_options)\u001b[0m\n\u001b[1;32m   1400\u001b[0m         \u001b[0mcontent_or_path\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mBytesIO\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcontent_or_path\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1401\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1402\u001b[0;31m     with get_handle(\n\u001b[0m\u001b[1;32m   1403\u001b[0m         \u001b[0mcontent_or_path\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"rb\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstorage_options\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstorage_options\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mis_text\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mFalse\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1404\u001b[0m     ) as handle:\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pandas/io/common.py\u001b[0m in \u001b[0;36mget_handle\u001b[0;34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[0m\n\u001b[1;32m    880\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    881\u001b[0m             \u001b[0;31m# Binary mode\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 882\u001b[0;31m             \u001b[0mhandle\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mhandle\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mioargs\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmode\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    883\u001b[0m         \u001b[0mhandles\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mhandle\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    884\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: 'data_simulasi_50_siswa_20_soal.xlsx'"
          ]
        }
      ],
      "source": [
        "# =========================================\n",
        "# DASHBOARD ANALISIS SOAL SIMULASI\n",
        "# =========================================\n",
        "\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import plotly.express as px\n",
        "import plotly.graph_objects as go\n",
        "from sklearn.cluster import KMeans\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "import statsmodels.api as sm\n",
        "import plotly.io as pio\n",
        "\n",
        "pio.templates.default = \"plotly_white\"\n",
        "\n",
        "# =========================\n",
        "# LOAD DATA\n",
        "# =========================\n",
        "df = pd.read_excel(\"data_simulasi_50_siswa_20_soal.xlsx\")\n",
        "data = df.select_dtypes(include=np.number)\n",
        "\n",
        "# =========================\n",
        "# STATISTIK UMUM\n",
        "# =========================\n",
        "jumlah_siswa = len(df)\n",
        "jumlah_soal = data.shape[1]\n",
        "rata_keseluruhan = round(data.mean().mean(), 2)\n",
        "\n",
        "print(\"Jumlah Siswa :\", jumlah_siswa)\n",
        "print(\"Jumlah Soal  :\", jumlah_soal)\n",
        "print(\"Rata-rata    :\", rata_keseluruhan)\n",
        "\n",
        "# =========================\n",
        "# 1. HISTOGRAM NILAI TOTAL\n",
        "# =========================\n",
        "df[\"Total_Nilai\"] = data.sum(axis=1)\n",
        "\n",
        "fig1 = px.histogram(\n",
        "    df,\n",
        "    x=\"Total_Nilai\",\n",
        "    nbins=10,\n",
        "    title=\"Distribusi Total Nilai Siswa\"\n",
        ")\n",
        "fig1.show()\n",
        "\n",
        "# =========================\n",
        "# 2. RATA-RATA PER SOAL\n",
        "# =========================\n",
        "mean_per_soal = data.mean().sort_values()\n",
        "\n",
        "fig2 = px.bar(\n",
        "    x=mean_per_soal.index,\n",
        "    y=mean_per_soal.values,\n",
        "    title=\"Tingkat Kesulitan Soal (Rata-rata Skor)\"\n",
        ")\n",
        "fig2.update_layout(\n",
        "    xaxis_title=\"Soal\",\n",
        "    yaxis_title=\"Rata-rata Skor\"\n",
        ")\n",
        "fig2.show()\n",
        "\n",
        "# =========================\n",
        "# 3. HEATMAP KORELASI\n",
        "# =========================\n",
        "corr = data.corr()\n",
        "\n",
        "fig3 = px.imshow(\n",
        "    corr,\n",
        "    text_auto=True,\n",
        "    title=\"Korelasi Antar Soal\",\n",
        "    zmin=-1,\n",
        "    zmax=1\n",
        ")\n",
        "fig3.show()\n",
        "\n",
        "# =========================\n",
        "# 4. CLUSTERING SISWA\n",
        "# =========================\n",
        "scaler = StandardScaler()\n",
        "X_scaled = scaler.fit_transform(data)\n",
        "\n",
        "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
        "df[\"Cluster\"] = kmeans.fit_predict(X_scaled)\n",
        "\n",
        "fig4 = px.scatter(\n",
        "    df,\n",
        "    x=data.columns[0],\n",
        "    y=data.columns[1],\n",
        "    color=\"Cluster\",\n",
        "    title=\"Segmentasi Siswa\"\n",
        ")\n",
        "fig4.show()\n",
        "\n",
        "# =========================\n",
        "# 5. REGRESI (VALIDITAS INTERNAL)\n",
        "# =========================\n",
        "X = sm.add_constant(data.iloc[:, :-1])\n",
        "y = data.iloc[:, -1]\n",
        "\n",
        "model = sm.OLS(y, X).fit()\n",
        "\n",
        "print(\"\\nR-Squared Model :\", round(model.rsquared, 3))"
      ]
    }
  ]
}