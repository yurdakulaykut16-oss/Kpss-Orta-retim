# KPSS Ortaöğretim — Hızlandırılmış Kamp

**Sınav: 25 Ekim 2026 (Pazar) — Saat 10:15** · Senin için özel 10 günlük hızlandırılmış kamp (**15–24 Ekim 2026**).
Python/Flask + vanilla JS — kurulumu tek komut.

> ✅ İlk 2 günde **tüm konular** bitirilir (Konu Maratonu). Sonrasında **yanlışlarına göre** konular sana **farklı
> anlatımla** tekrar anlatılır ve o konudan **yeni sorular** gelir. Her konuda **ustalana kadar** çalışırsın.
> Her gün yüzlerce soruluk havuzdan **durumuna uygun** sorular çıkar; **aynı soru iki kez gelmez**.

---

## Hızlı Kurulum

```bash
pip install -r requirements.txt
python app.py
```

Tarayıcıda aç: **http://localhost:5000**

---

## 10 Günlük Kamp (15–24 Ekim 2026)

| Gün | Tarih | Tema |
|-----|-------|------|
| 1. gün | 15 Ekim Perşembe | **Konu Maratonu I** — 5 derste TÜM konular (hızlı tur + 10'luk testler) |
| 2. gün | 16 Ekim Cuma | **Konu Maratonu II** — tur tamamlama + konu testleri (ustalana kadar) |
| 3–8. gün | 17–22 Ekim | **Ustalık Günleri** — hatalardan ustalığa; zayıf konu tekrarı + test |
| 9. gün | 23 Ekim Perşembe | Genel Tekrar — zayıf konu atağı |
| 10. gün | 24 Ekim Cuma | **Final Provası** — 50 soruluk büyük deneme |

Her gün **sırayla** 5 ders: **Tarih → Coğrafya → Vatandaşlık → Türkçe → Güncel**. Gün, denemeyle biter.

> 📌 **Hafta sonu ek programı (hafta içi iş/okul olmayınca):** Günde 500 soruya kadar çıkan maraton günleri.
> 1. turla 500 soru maratonu (4 saat) — 5. gün ile 10. gün arası hafta sonları ideal.

---

## Sistem Nasıl Çalışıyor?

### 1. Konu Maratonu (ilk 2 gün) — tüm konular
- **55 konu** (sadece KPSS'de çıkmış konular) — her konuda:
  - **Hızlı tur** (özet) → **Farklı anlatım** (hikâyeyle) → **Sınav tuzağı** → **Nasıl sorulur**
  - Hemen altında **o konudan 10 soruluk test**
- 50 derin **konu modülü** (10 günlük dersler) de hazır; istersen detaylı okursun.

### 2. 10'luk Testler + Otomatik Kontrol
- Öğrendiğin her konudan **10'ar soruluk testler** çözersin.
- **Her 10 soruda otomatik kontrol** yapılır:
  - ✅/❌ sonucun ve netin
  - ❌ **Yanlışların çözümleri** (2 farklı yöntemle)
  - 🎭 **Yanlış konuların FARKLI anlatımı** (hikâye + tuzak kartları)
  - 🔁 O konulara uygun **yeni 10 soru** (tekrar çöz)
- Yanlış yaparsan benzer 2 soru pekiştirme olarak kuyruğa girer.

### 3. Ustalık Sistemi
- Her konunun ustalığı takip edilir: **son 10 soruda 8+ doğru = Usta** (rozet yeşile döner).
- Usta olmadığın konular öncelikli gelir; ustalaştığın konular geri planda kalır.
- Günde **500 soruya kadar** çıkabilirsin — havuz her gün yüzlerce soru sunar ama **durumuna göre** karşına çıkar.

### 4. Aynı Soru Tekrar Gelmez
- Bir soruyu **bugün** çözdüysen o gün tekrar gelmez (anti-tekrar).
- **Hiç görmediğin** sorular öncelikli gelir; eskiden çözdüklerin zamanla geri döner.
- Yanlış yaptıkların **ustalana kadar** tekrar; doğru bildiklerin arka plana düşer.

### 5. Denemeler
- 10 deneme (**DEN-01…DEN-10**), her gün 1 tanesi o günün rehberine bağlı: 5. ve 10. gün
  **50 soruluk büyük prova**, diğer günler 15 soruluk mini.
- Denemeler her dersi dengeli dağıtır, şıklar karışık gelir (sınav gibi).
- Süre geri sayar; bitirince **net + ders analizi + tüm çözümler**.

---

## Kapsam (Sınav Mufredatı — geçmiş KPSS konuları)

| Ders | Kapsam | Soru bankası |
|------|--------|--------------|
| **Tarih** | İlk Türk Devletleri → Osmanlı → Milli Mücadele → Devrimler → Çağdaş Tarih | 274 |
| **Coğrafya** | Harita–iklim → yer şekilleri → nüfus–ekonomi → bölgeler–afetler–çevre | 162 |
| **Vatandaşlık** | Hukuk → Anayasa → haklar → TBMM–yürütme–yargı → insan hakları → seçimler | 122 |
| **Türkçe** | Sözcükte/cümlede anlam → paragraf → **sözel mantık** → dil bilgisi | 129 |
| **Güncel** | Türkiye yönetimi → ekonomi → kurumlar → son olaylar | 111 |

> 📚 **Toplam: 798 soru** — her biri 2 farklı çözüm yöntemiyle. Havuz her gün yüzlerce soru sunar,
> karşıya durumuna göre 10'luk setler halinde gelir. Her 10 soruda otomatik kontrol + telafi döngüsü.
>
> ⚠️ **Geçmiş KPSS çıkmış sorular için PDF bekleniyor.** Şu anki banka ÖSYM mantığına uygun üretildi
> ve tümü geçmiş sınav konularından. PDF'lerini bu repo'ya koyarsan (veya linkini verirsen) gerçek
> çıkmış soruları `kaynak` alanıyla "2018-KPSS" gibi etiketleyip ekleriz.

**Konu seçimi kuralı:** *Sadece geçmiş KPSS sınavlarında çıkmış konular.* Hiç sorulmamış devletler
(Avarlar, Akhunlar, Avrupa Hunları, Hazarlar, Bulgarlar, Karluklar, Kırgızlar…) konu olarak anlatılmaz;
yalnızca "karıştırma şıkkı" olarak kullanılabilir.

---

## Deneme Sonuçları Ertesi Günü Şekillendirir

Gün sonu denemesi bitince **yanlış/boş bıraktığın konular** otomatik olarak "odak listene" yazılır:

- Ertesi günün rehberinde **"🎯 Dünkü Denemeden Gelen Odakların"** paneli çıkar.
- Maraton ve testlerde bu konulardan gelen sorular **öncelikli** gelir.
- **Odak Testi** (10 soru) ile zayıf konularını doğrudan çalışabilirsin.
- Bir konudan doğru çözdükçe o konu listeden silinir — ta ustalaşana kadar.

## Sayfalar

- **🏠 Bugünün Rehberi** — 1. gün…10. gün numaralı, her gün için 3 adım: konu turu → 10'luk testler → deneme
- **📖 Konu Anlatımları** — 55 konunun hızlı turu + farklı anlatımı + 50 derin modül
- **✏️ Test Çöz** — Günün Maratonu / Konu Testi (10) / Yanlış Telafisi / Hata Atölyesi — hepsi 10'luk
- **📝 Denemeler** — 10 deneme + çözüm analizi
- **🎯 Hata Defteri** — zayıf konular + yanlış sorular + saldırı butonları
- **📊 İstatistik** — ustalık, günlük 500 sayaç, net takibi
- **⚙️ Ayarlar** — yedekle / geri yükle / sıfırla

---

## Gerçek Çıkmış KPSS Soruları (2014–2024)

ÖSYM'nin resmî soru kitapçıklarından birebir aktarılmış **350 gerçek çıkmış soru** bankada
kaynak etiketleriyle durur — her sorunun kartında ve çözümünde **kaynak yılı** görünür:

| Yıl | Soru | Not |
|-----|------|-----|
| 2014-KPSS | 84 | Tam kitapçık; ÖSYM'nin **cevap anahtarlı** %10 kitapçığıyla doğrulandı |
| 2016-KPSS | 86 | ÖSYM'nin kitapçık içi **resmî cevap anahtarıyla** doğrulandı |
| 2018-KPSS | 86 | Tam kitapçık; %10'luk kitapçık **resmî cevaplarıyla** doğrulandı |
| 2020-KPSS | 85 | Tam kitapçık; %10'luk kitapçık **resmî cevaplarıyla** doğrulandı |
| 2024-KPSS | 9 | ÖSYM'nin %10'luk Temel Soru Kitapçığı'ndaki tam metinli sorular + resmî cevaplar |

- Test Çöz sayfasında **🎯 Gerçek Çıkmış KPSS Soruları** paneli: yıla göre (2014…2024) ya da karışık test.
- Günlük denemeler çıkmış sorulara öncelik verir (deneme başına ~%80 gerçek çıkmış).
- `/api/sorular/<ders>?cikmis=1` uç noktası yalnızca yıl etiketli çıkmışları döndürür.
- Bütün yıl etiketli cevaplar ÖSYM'nin resmî cevap anahtarlarıyla karşılaştırılıp doğrulanmıştır.

## Veri & Araçlar

- `data/sorular/*.jsonl` — soru bankası (id, konu, zorluk, **kaynak**, 2 çözüm, etiketler)
- `data/konu_yeniden.json` — 55 konu için farklı anlatım kartları (özet + hikâye + tuzak + kalıp)
- `data/dersler/*.md` — günlük konu modülleri
- `data/program.json` — 10 günlük plan
- `data/denemeler.json` — 10 deneme
- `data/ilerleme/` — ilerleme kaydı (otomatik yedek)
- `araclar/soru_genislet.py` — yeni soru ekleme (TSV → JSONL)
- `araclar/deneme_uret.py` — denemeleri yeniden üret
- `araclar/veri_kontrol.py` — banka bütünlük kontrolü (`python3 araclar/veri_kontrol.py`)

Yeni soru eklemek için `data/kaynaklar/*.tsv` dosyasına `id|gun|konu|zorluk|kaynak|kok|sik1..sik5|dogru|cozum1|cozum2|etiketler` yazıp `python3 araclar/soru_genislet.py` çalıştır.

---

*Başarılar! İlk 2 günde konuları bitir, sonra yanlışlarından ustalığa — her gün 500 soruya kadar, aynı soru tekrar etmeden.* 🚀
