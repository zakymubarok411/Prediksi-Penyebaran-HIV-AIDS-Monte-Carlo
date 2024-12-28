import matplotlib
matplotlib.use('Agg')  # Set backend ke 'Agg' untuk menghindari masalah GUI
import matplotlib.pyplot as plt
from flask import Flask, render_template
import numpy as np
import pandas as pd
import io
import base64

app = Flask(__name__)

# Data awal AIDS di berbagai wilayah
initial_data = {
    'Wilayah': ["Kota Bandung", "Bogor", "Indramayu", "Majalengka", "Kota Bekasi", "Kota Bogor", "Cirebon", "Garut", "Kota Depok", "Bekasi", "Karawang", "Kota Cirebon", "Kota Sukabumi", "Cianjur", "Kota Cimahi", "Subang", "Kuningan", "Sukabumi", "Kota Tasikmalaya", "Purwakarta", "Sumedang", "Bandung", "Tasikmalaya", "Bandung Barat", "Ciamis", "Pangandaran", "Kota Banjar"],
    'Kasus_AIDS': [190, 139, 135, 116, 99, 92, 83, 79, 79, 56, 55, 52, 46, 45, 44, 43, 38, 36, 35, 35, 33, 25, 21, 18, 13, 10, 0]
}

# Parameter simulasi Monte Carlo
n_tahun = 3  # Prediksi 3 tahun ke depan
n_simulasi = 1000  # Jumlah iterasi Monte Carlo
pertumbuhan_min = 0.01  # Pertumbuhan minimum (1%)
pertumbuhan_max = 0.15  # Pertumbuhan maksimum (15%)

@app.route('/')
def index():
    # Data tambahan untuk informasi
    informasi = {
        'judul': 'Prediksi Penyebaran HIV/AIDS di Jawa Barat',
        'deskripsi': 'Simulasi metode Monte Carlo memberikan gambaran bagaimana penyebaran HIV/AIDS di Jawa Barat pada tahun 2023, dan proyeksi untuk 3 tahun ke depan.',
        'kontak': 'Jika Anda membutuhkan informasi lebih lanjut, hubungi kami di email@zakymubarok411.com',
    }

    # Konversi data AIDS ke DataFrame dan lakukan simulasi (seperti sebelumnya)
    data = pd.DataFrame(initial_data)

    # Simulasi Monte Carlo
    np.random.seed(42)
    simulasi_hasil = {}

    for wilayah in data['Wilayah']:
        kasus_awal = data[data['Wilayah'] == wilayah]['Kasus_AIDS'].values[0]
        hasil_simulasi = []

        for _ in range(n_simulasi):
            kasus = kasus_awal
            kasus_tahunan = [kasus]
            for _ in range(n_tahun):
                pertumbuhan = np.random.uniform(pertumbuhan_min, pertumbuhan_max)
                kasus = kasus * (1 + pertumbuhan)
                kasus_tahunan.append(kasus)
            hasil_simulasi.append(kasus_tahunan)
        simulasi_hasil[wilayah] = np.mean(hasil_simulasi, axis=0)

    # Membuat DataFrame hasil simulasi
    hasil_df = pd.DataFrame(simulasi_hasil).T
    hasil_df.columns = ['Tahun_0', 'Tahun_1', 'Tahun_2', 'Tahun_3']
    hasil_df['Persentase_Kenaikan'] = ((hasil_df['Tahun_3'] - hasil_df['Tahun_0']) / hasil_df['Tahun_0']) * 100

    # Grafik prediksi
    fig, ax = plt.subplots(figsize=(12, 8))
    for wilayah in hasil_df.index:
        ax.plot(range(n_tahun + 1), hasil_df.loc[wilayah, ['Tahun_0', 'Tahun_1', 'Tahun_2', 'Tahun_3']], label=wilayah)

    ax.set_title("Prediksi Penyebaran Kasus HIV/AIDS di Jawa Barat", fontsize=16)
    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Jumlah Kasus", fontsize=12)
    ax.grid(True)
    ax.set_xticks(range(n_tahun + 1))
    ax.set_xticklabels(['Tahun 0', 'Tahun 1', 'Tahun 2', 'Tahun 3'])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

    img_buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_str = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return render_template('index.html', informasi=informasi, tabel=hasil_df.to_html(classes='table table-striped'), img_data=img_str)

if __name__ == '__main__':
    app.run(debug=True)
