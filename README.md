# 🎯 KPSS Ortaöğretim — 10 Günlük Hızlandırılmış Kamp (15–25 Ekim 2026)

**25 Ekim 2026 Pazar** günü yapılacak KPSS Ortaöğretim sınavına hazırlanan, temeli zayıf
(meslek lisesi çıkışlı) bir öğrenci için tasarlanmış, **tamamen Türkçe** ve **tek ekrandan**
yönetilen bir çalışma kampı.

Kamp takvimi: **15 Ekim – 24 Ekim 2026** (10 gün) → **Sınav: 25 Ekim 2026**.

Her gün **5 ders (Tarih, Coğrafya, Vatandaşlık, Türkçe, Güncel Bilgiler)** sırayla işlenir;
gün sonunda **deneme sınavı** çözülür; sonuçlara göre ertesi günün içeriği **otomatik
genişletilir** (zayıf konudan ek sorular + anlatım tekrarı; hata sürerse 500 soruya kadar
yoğunlaştırılmış tekrar).

---

## 🚀 Projeyi Çalıştırma

Gereksinimler: **Python 3.9+** ve `pip`.

```bash
# 1) Bu klasöre girin
cd Kpss-Orta-retim

# 2) Sanal ortam oluşturun (önerilir)
python3 -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4) Sunucuyu başlatın
python app.py
```

Ardından tarayıcınızda **<http://localhost:5000>** adresini açın. Hepsi bu kadar!

> Veri kontrolü isterseniz: `python araclar/veri_kontrol.py`
> Denemeleri yeniden üretmek için: `python araclar/deneme_uret.py`

---

## 📚 İçerik

| Ders | Konu anlatımı (10 gün × modül) | Soru bankası |
|---|---|---|
| Tarih | ✅ | 140 soru |
| Coğrafya | ✅ | 85 soru |
| Vatandaşlık | ✅ | 62 soru |
| Türkçe | ✅ | 61 soru |
| Güncel Bilgiler | ✅ | 63 soru |
| **Toplam** | **50 ders modülü** | **411 soru + 10 deneme** |

- **Her gün, 5 dersin tamamı** sırayla işlenir (tek ders günü yoktur).
- Her ders günü: **önce sade anlatım** (günlük hayat diliyle), sonra **20 soruluk çalışma seti**.
- **Günün sonunda deneme:** 1–4. günler 15 soruluk mini deneme (12 dk),
  **5. ve 10. günler 50 soruluk geniş deneme** (40 dk). Gerçek KPSS'de 120 soru / 130 dk
  olduğundan süreler orantılı ölçeklenmiştir.
- Sorular **geçmiş KPSS sorularından yeniden düzenlenmiş** ya da **KPSS formatında**
  özgün sorulardır; her sorunun `kaynak` alanında bu bilgi yer alır.
- Her sorunun **iki farklı çözüm yöntemi** vardır (biri hikâye/şaka/benzerlik, diğeri
  kural/teknik) — hata yapılan konu tekrar edildiğinde anlatım **farklı yöntemle** sunulur.

## 🧠 Uyarlanabilir Sistem ("Yanlış nereden geliyorsa oradan")

1. **Gün içi:** Yanlış cevapladığınız her sorudan sonra **2 benzer soru** eklenir
   (aynı kök, farklı kelimeler), ardından konu kısa tekrarla pekiştirilir.
2. **Deneme sonrası:** Deneme sonucundaki zayıf etiketler tespit edilir; ertesi günün
   20 soruluk setinin **%60'ı yeni konu, %40'ı zayıf konudan** oluşturulur.
3. **Hata Atölyesi:** Hata defterindeki her konu için tekrar seti açılır. Aynı konuda
   hatalar sürerse sistem **yoğunlaştırılmış tekrar** başlatır ve günlük **500 soruluk
   üst sınır** dolana kadar (sadece sınavda çıkan konulardan) soru yağdırır.
4. **Benzer soru mantığı:** Her sorunun `kok` (soru kökü) ve `etiketler` alanları vardır;
   pekiştirme soruları aynı kökten seçilir — "aynı sorunun tekrarı" hissi yaratır.

## 🖥️ Uygulama Bölümleri

| Bölüm | Ne yapar |
|---|---|
| **Bugünün Paneli** | Günün planı (saat saat), ders kartları, görev tikleri, zayıf konular |
| **10 Günlük Takvim** | 15–24 Ekim tam program; her günün teması ve deneme bağlantısı |
| **Günün Dersi** | Ders modülü: giriş, sade anlatım, 2 yöntem, sık hatalar, cebe kart, ağız tekrarı |
| **Soru Çözümü** | Günlük set / hata seti / konu seti; şık anında renklenir, çözüm 2 yöntemle |
| **Denemeler** | Süreli deneme; soru ızgarası, net (D − Y/4) hesapları |
| **Hata Defteri** | Yanlışlar; "tekrar" butonu ile benzer soru seti |
| **İstatistik** | Doğruluk, ders/konu performansı, 500 soru ilerlemesi, deneme geçmişi |
| **Ayarlar** | İlerlemeyi dışa/içe aktarma, sıfırlama |

İlerlemeniz **otomatik kaydedilir** (tarayıcı + sunucudaki `data/ilerleme/` klasörü).

## 📁 Proje Yapısı

```
Kpss-Orta-retim/
├── app.py                  # Flask sunucu + veri API'si (/api/...)
├── requirements.txt
├── data/
│   ├── program.json        # 10 günlük kamp planı, sınav bilgileri
│   ├── denemeler.json      # 10 denemenin içerik listesi (üretilmiş)
│   ├── dersler/*.md        # 50 ders modülü (sade anlatım, yöntemler, kartlar)
│   ├── sorular/*.jsonl     # 411 soru (kök, 5 şık, 2 çözüm, etiketler)
│   └── ilerleme/           # kayıtlı ilerleme (çalışma zamanı)
├── static/                 # Arayüz (HTML/CSS/JS — tek sayfa uygulama)
└── araclar/
    ├── veri_kontrol.py     # bütünlük testi (id benzersizliği, alan kontrolü)
    └── deneme_uret.py      # denemeleri soru bankasından üretir (tohum: 20261025)
```

## 🎨 Tasarım

- Koyu kenar çubuğu + açık çalışma alanı, ders başına renk kodlu kartlar
  (Tarih 🟠, Coğrafya 🟢, Vatandaşlık 🔵, Türkçe 🟣, Güncel 🟡).
- Cep telefonu uyumlu (mobil menü), yazdırma dostu görünüm, yumuşak animasyonlar.
- Sınav temasına özel hero: geri sayım, net rozetleri, motivasyon cümlesi.

---
*Başarılar! 25 Ekim'de görüşürüz. 🗓️*
