import json, pandas as pd
from vale import predict

def veriyi_cek(): # ÇEKİLEN VERİLER --> ENLEM, BOYLAM, İRTİFA, DİKİLME, YÖNELME, YATIŞ VE HIZ
    veriler = []

    with open("telemetri_log.txt", "r") as dosya:
        for satir in dosya:
            if satir.strip():  # boş satır varsa atla
                try:
                    veri = json.loads(satir)
                    veriler.append(veri)
                except json.JSONDecodeError as e:
                    print(f"Hata: {e} - Satır: {satir}")

    istenen_alanlar = ['iha_enlem', 'iha_boylam', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis', 'iha_hiz']

    filtrelenmis_veriler = []

    for veri in veriler:
        yeni_veri = {key: veri[key] for key in istenen_alanlar}
        
        

        filtrelenmis_veriler.append(yeni_veri)
        
    return pd.DataFrame(filtrelenmis_veriler)

df = veriyi_cek()

time = 0.5 # KAÇ SANİYE SONRAKİ KONUMU TAHMİN ETMEK İSTERSEK ONU YAZIYORUZ

df_tahmin = df.apply( # HER VERİDEN BİR SONRAKİ KONUM TAHMİNİ İŞLEMİ
    lambda row: pd.Series(predict(
        row['iha_enlem'],
        row['iha_boylam'],
        row['iha_irtifa'],
        row['iha_dikilme'],
        row['iha_yonelme'],
        row['iha_yatis'],
        row['iha_hiz'],
        zaman=time
    )),
    axis=1
)

# Tahmin sütunlarını adlandır
df_tahmin.columns = ['yeni_enlem', 'yeni_boylam', 'yeni_irtifa']

fark_df = pd.DataFrame() # GERÇEK İLE TAHMİN ARASINDAKİ FARKI KAYDEDİYORUZ

fark_df['enlem_farki'] = (df['iha_enlem'] - df_tahmin['yeni_enlem']).abs()
fark_df['boylam_farki'] = (df['iha_boylam'] - df_tahmin['yeni_boylam']).abs()
fark_df['irtifa_farki'] = (df['iha_irtifa'] - df_tahmin['yeni_irtifa']).abs()

# Sonuçlara bakalım
print(fark_df.describe())
print(fark_df.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

# Gerçek veriler
plt.scatter(df['iha_boylam'], df['iha_enlem'], color='blue', label='Gerçek Konum', alpha=0.6)

# Tahmin verileri
plt.scatter(df_tahmin['yeni_boylam'], df_tahmin['yeni_enlem'], color='red', label='Tahmin Edilen Konum', alpha=0.6)

plt.xlabel('Boylam')
plt.ylabel('Enlem')
plt.title('İHA Gerçek ve Tahmin Edilen Konumları')
plt.legend()
plt.grid(True)
plt.show()
