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

Otomatik kontrol (jsdom smoke — 40 test):

```bash
python3 araclar/refresh_fixtures.py               # sunucu açıkken
(cd /tmp/kpss_test && npm i jsdom >/dev/null)
NODE_PATH=/tmp/kpss_test/node_modules node araclar/smoke_test.js
```

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

> 📌 **Günlük soru hedefi (yeni):** Her derse günlük **minimum 500 soru** (toplam 2.500) — hepsi **10'ar soruluk testler** hâlinde.
> Akış: önce **konu testleri** (müfredat sırasıyla, tüm konular bitene kadar) → konular bitince **karışık testler** (tüm konulardan).
> Her dersin kendi sayacı var: **#/akis/tarih** gibi bir sayfadan o günün akışını takip edebilirsin; sonucunda "Günlük Akışa Dön" düğmesi seni sıradaki teste götürür.

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
- Her derste günlük **500 soru** hedeflenir (toplam **2.500**); havuz her ders için 500+ soru içerir, **durumuna göre** karşına çıkar, aynı soru tekrar etmez.

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
| **Tarih** | İlk Türk Devletleri → Osmanlı → Milli Mücadele → Devrimler → Çağdaş Tarih | 509 |
| **Coğrafya** | Harita–iklim → yer şekilleri → nüfus–ekonomi → bölgeler–afetler–çevre | 534 |
| **Vatandaşlık** | Hukuk → Anayasa → haklar → TBMM–yürütme–yargı → insan hakları → seçimler | 503 |
| **Türkçe** | Sözcükte/cümlede anlam → paragraf → **sözel mantık** → dil bilgisi | 519 |
| **Güncel** | Türkiye yönetimi → ekonomi → kurumlar → son olaylar | 501 |

> 📚 **Toplam: 2.566 soru** — bunların **381'i gerçek çıkmış** (resmî kitapçıklardan, kaynak etiketli).
> Havuz her derste günde 500 soruya kadar besler; karşıya **10'luk setler** hâlinde gelir.
> Her 10 soruda otomatik kontrol + telafi döngüsü.
>
> ✅ **Gerçek çıkmış sorular eklendi:** 2014–2026 arası resmî ÖSYM kitapçıklarından (Ortaöğretim +
> Ön Lisans + Lisans oturumları) **381 gerçek çıkmış soru**; cevapların tamamı kitapçıkların resmî
> cevap anahtarlarından alınmıştır. Her sorunun altında ve çözümünde `kaynak` etiketi yazar
> ("2018-KPSS", "2026-KPSS Lisans" gibi).

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
- **📊 İstatistik** — ustalık, ders başı 500 / toplam 2.500 günlük sayaç, net takibi
- **⚙️ Ayarlar** — yedekle / geri yükle / sıfırla

---

## Gerçek Çıkmış KPSS Soruları (2014–2026)

ÖSYM'nin resmî soru kitapçıklarından birebir aktarılmış **381 gerçek çıkmış soru** bankada
kaynak etiketleriyle durur — her sorunun kartında ve çözümünde **kaynak** görünür:

| Yıl | Soru | Not |
|-----|------|-----|
| 2014-KPSS | 84 | Tam kitapçık; ÖSYM'nin **cevap anahtarlı** %10 kitapçığıyla doğrulandı |
| 2016-KPSS | 86 | ÖSYM'nin kitapçık içi **resmî cevap anahtarıyla** doğrulandı |
| 2018-KPSS | 86 | Tam kitapçık; %10'luk kitapçık **resmî cevaplarıyla** doğrulandı |
| 2020-KPSS | 85 | Tam kitapçık; %10'luk kitapçık **resmî cevaplarıyla** doğrulandı |
| 2022-KPSS | 6 | Ortaöğretim kitapçığı; resmî cevap anahtarlı |
| 2022-KPSS Ön Lisans | 7 | Ön Lisans oturumu (Ortaöğretim'den farklı set); resmî anahtarlı |
| 2023-KPSS Lisans | 6 | Lisans GY-GK oturumu; resmî anahtarlı |
| 2024-KPSS | 9 | ÖSYM'nin %10'luk Temel Soru Kitapçığı'ndaki tam metinli sorular + resmî cevaplar |
| 2024-KPSS Ön Lisans | 5 | Ön Lisans oturumu; resmî anahtarlı |
| 2025-KPSS Lisans | 6 | Lisans GY-GK oturumu; resmî anahtarlı |
| 2026-KPSS Lisans | 6 | 6 Eylül 2026 oturumu; resmî anahtarlı |

- Test Çöz sayfasında **🎯 Gerçek Çıkmış KPSS Soruları** paneli: yıla göre (2014…2026) ya da karışık test.
- Cevaplar **yalnızca** kitapçıkların resmî "DOĞRU CEVAP" kayıtlarından alınır; hiçbir soru için cevap üretilmez/yorumlanmaz.
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
- `araclar/refresh_fixtures.py` — sunucudan smoke fixture'ları çeker
- `araclar/smoke_test.js` — jsdom ile uçtan uca arayüz testi (40 test)

Yeni soru eklemek için `data/kaynaklar/*.tsv` dosyasına `ders|konu|gun|zorluk|kok|dogru|sikA..sikD|cozum1|cozum2|kaynak` yazıp `python3 araclar/soru_genislet.py` çalıştır.

---

*Başarılar! İlk 2 günde konuları bitir, sonra yanlışlarından ustalığa — her ders günde 500 soru (10'arlık testler), konular bitince karışık testler, aynı soru tekrar etmeden.* 🚀
