# KPSS Ortaöğretim — Hızlandırılmış Kamp

**Sınav: 25 Ekim 2026 (Pazar) — Saat 10:15** · Senin için özel 8 günlük hızlandırılmış kamp (**17–24 Ekim 2026**; 17–23 Ekim test günleri, 24 Ekim deneme/tekrar).
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

Otomatik kontrol (jsdom smoke — 645 kontrol):

```bash
python3 araclar/refresh_fixtures.py               # sunucu açıkken
(cd /tmp/kpss_test && npm i jsdom >/dev/null)
NODE_PATH=/tmp/kpss_test/node_modules node araclar/smoke_test.js
```

---

## 8 Günlük Kamp (17–24 Ekim 2026)

| Gün | Tarih | Tema | Deneme |
|-----|-------|------|--------|
| 1. gün | 17 Ekim Cumartesi | **Konu Maratonu** — 5 derste TÜM konular (hızlı tur + 10'luk testler) | DEN-01, DEN-02 |
| 2–6. gün | 18–22 Ekim | **Ustalık Günleri 1–5** — hatalardan ustalığa; zayıf konu tekrarı + test | DEN-03 … DEN-07 (20 Ekim: DEN-05, 50 soruluk büyük prova) |
| 7. gün | 23 Ekim Cuma | Genel Tekrar — zayıf konu atağı | DEN-08 |
| 8. gün | 24 Ekim Cumartesi | **Final Provası** — yalnızca deneme ve tekrar (test hedefi yok) | DEN-09, DEN-10 |

Önceki 15–16 Ekim günlerinin içeriği ve denemeleri bu günlere dağıtıldı.

Her gün **sırayla** 5 ders: **Tarih → Coğrafya → Vatandaşlık → Türkçe → Güncel**. Gün, denemeyle biter.

> 📌 **Günlük soru hedefi ve üst sınırı:** Ders başına **400 soru** (toplam 2.000), **10'ar soruluk testler** hâlinde.
> 400 aynı zamanda **günlük üst sınırdır**: bir derste o gün 400 test sorusu ayrıldıktan sonra yeni test başlatılamaz; fazla sorular **sonraki günlere kalır**. Denemeler bu hedefe ve sınıra dahil değildir. 7 test günü × 400 = **ders başına 2.800 test sorusu**; geçmişi boş bir profil için her dersin başlangıç test kapasitesi tam **2.800**'dür (denemelere ayrılan sorular hariç).
> Güncel havuz hedefi ayrıca **3.000** olarak belirlenmiştir; bu henüz tamamlanmış değildir.
> ✅ **Gerçek durum:** Aynı soru tekrar gelmediği hâlde her dersin günlük dağılımı **400 × 7** (17–23 Ekim) olarak tam karşılanır. Bu sayılar daha önce soru çözmemiş profil içindir; önceden kullanılan sorular kalan kapasiteyi azaltır.
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
- Yanlış yaparsan **Öğrenme Modu** devreye girer (aşağıda).

### 2b. Öğrenme Modu — yanlış yaptığın konuyu öğrenene kadar
- Bir soruda yanlış şıkkı seçtiğinde, çözümün hemen altında **o konu yeniden anlatılır**.
  Aynı konuda tekrar yanlış yaparsan anlatım değişir: 1. seferde *özet + sınav tuzağı*,
  2. seferde *hikâyeyle anlatım + nasıl sorulur*, 3. seferde *hepsi bir arada*.
- **Sıradaki soru aynı konudan** gelir (kullanılmamış yeni bir soru). O konuda **art arda 2 doğru**
  yapana kadar bu devam eder; sonra “🎉 öğrenildi” denir ve normal akışa dönülür.
  Bir testte tek konu için en fazla 8 soru araya eklenir; sonra derin modülü okuman önerilir.
- Öğrenilmemiş konular kalıcı olarak **🔁 Öğrenmekte olduğun konular** listesinde tutulur (Bugünün
  Rehberi, Test Çöz, Günlük Akış ve kontrol ekranlarında görünür). Sonraki karışık/maraton/günlük
  testlerde bu konular **setin yarısına kadar** (10 sorudan 5'i) öncelikli gelir; Yanlış Telafisi
  önce bu konulardan soru seçer. `#/tekrar/<ders>/<konu>` sayfası konunun tam anlatımını gösterir.
- Denemede yanlış yapılan konular da bu listeye eklenir.
- Aynı soru yine tekrar edilmez: öğrenme soruları da kalıcı kullanım kaydından ve deneme rezervinden
  ayrılarak seçilir. Bu nedenle zayıf konular havuzda daha hızlı tükenebilir.
- Etiketi kısa ad olan 24 aktif konunun (ör. `cumlede_anlam`, `dunya_gundemi`) anlatım kartı yoktu;
  `araclar/konu_kartlari_ekle.py` ile `data/konu_yeniden.json` dosyasına eklendi ve arayüzde okunur
  adlarla (“Cümlede Anlam”, “Dünya Gündemi”) gösterilir.

### 3. Ustalık Sistemi
- Her konunun ustalığı takip edilir: **son 10 soruda 8+ doğru = Usta** (rozet yeşile döner).
- Usta olmadığın konular öncelikli gelir; ustalaştığın konular geri planda kalır.
- Her derste günlük **400 soru** hedeflenir ve bu sayı günlük üst sınırdır (toplam **2.000**); fazlası sonraki günlere kalır. Yalnız onaylı konu havuzu kullanılır; deneme rezervleri sayılmaz. Kullanılmış sorular gün değişince yeniden açılmaz; eksik kamp kapasitesi gizlenmez.

### 4. Aynı Soru Tekrar Gelmez
- Aynı profilin test, telafi ve denemeleri ortak **kalıcı kullanım kaydı** kullanır; gün değişmesi eski soruları yeniden açmaz.
- Hem soru id'si hem normalleştirilmiş kök denetlenir; numara veya şık sırası değişikliği yeni soru sayılmaz.
- Yanlış yapılan **konular**, farklı ve kullanılmamış sorularla çalışılır. Aynı yanlış soru yeni testte yeniden dağıtılmaz.
- Deneme şablonlarının toplam **220 sorusu** test seçiminden ayrılır; 10 deneme birbiriyle de id/kök çakışmaz.
- Oturum başlatılmadan önce `/api/soru-ayir/<kullanici>` sunucuda atomik kontrol ve ayırma yapar. İki eşzamanlı isteğin aynı soruyu ayırmasına izin verilmez.
- Cevaplanmadan bırakılan set de tüketilmiş sayılır. Havuz yetmezse eski soru veya başka dersle doldurulmaz; açık uyarı gösterilir.
- Günlük hedef için kullanılabilir sayı, arşivden veya aktif toplamdan farklıdır: geçmiş kullanım ve deneme rezervleri çıkarılır. Menüde kalan test sayısı ayrıca gösterilir.
- Kaydın açıkça sıfırlanması veya sunucu kayıtlarının silinmesi bu korumayı kaldırır. Hata Defteri ve sonuç incelemesi, eski soruların bilinçli incelemesidir; yeni test dağıtımı değildir.
- Metinsel kök denetimi, farklı yazılmış iki sorunun anlamsal olarak aynı olup olmadığını kanıtlamaz; bu ayrıca editoryal inceleme gerektirir.

### 5. Denemeler
- 10 deneme (**DEN-01…DEN-10**) 8 güne dağıtılmıştır: 1. gün DEN-01 ve DEN-02, 2–7. günler birer deneme,
  8. gün DEN-09 ve DEN-10. DEN-05 (20 Ekim) ve DEN-10 (24 Ekim) **50 soruluk büyük prova**, diğerleri 15 soruluk mini.
- Denemeler her dersi dengeli dağıtır, şıklar karışık gelir (sınav gibi).
- Süre geri sayar; bitirince **net + ders analizi + tüm çözümler**.

---

## Deneme hariç ders başına günlük 400 test sorusu (üst sınır)

Tek ayar kaynağı `data/calisma_hedefleri.json`: **400 soru/ders/gün**, **10 soru/set**, **40 setlik hedef/ders**, **2.000 test sorusu/gün**, `"gunluk_ust_sinir": true`. Deneme bu sayılara eklenir; deneme doğru/yanlış/boşları test sayacını artırmaz. Her dersin 400'ü ayrı değerlendirilir; tek derste fazladan soru çözmek diğer dersin eksiğini kapatmaz. Sunucu (`/api/soru-ayir`) o gün o derste 400'ü aşacak test ayırmasını **429** ile reddeder; arayüz son seti kalan sayıya göre kısaltır ve kalan soruları sonraki günlere bırakır. `/api/meta.calisma_hedefi.dersler.<ders>.gun_dagilimi` mevcut havuzun hangi güne kaç soru yettiğini gösterir.

İlk-gün eksiği için **26 Vatandaşlık + 162 Güncel = 188 yeni özgün soru** elle yazıldı. `ek_188_gunluk500.tsv` kök, beş seçenek ve gerekçeli çözümü içerir; `ek_188_inceleme.json` ayrı kapsam kararlarının içerik özetlerini saklar. Şık sıralaması dışında otomatik varyant üretimi yoktur. `soru_yukselt.py` ekleri de doğrulayarak uygular; mevcut farklı içerik veya korumalı kaynak sessizce ezilemez. Önceki 2.865 kayıt değiştirilmedi.

Ardından **her dersten 50, toplam 250 yeni soru** (`yeni_parti_01…05_*.tsv`, `*-YS-0001…0050`), sonra **her dersten 200, toplam 1.000 yeni soru** (`yeni_parti_06a…10b_*.tsv`, `*-YS-0051…0250`), ardından **her dersten 400, toplam 2.000 yeni soru** daha (`yeni_parti_11a…15d_*.tsv`, `*-YS-0251…0650`) elle yazıldı; yeni partilerin toplamı **3.250 (ders başına 650)**. Her satır kendi kökü, beş seçeneği ve gerekçeli çözümüyle ayrı bir sorudur; kökler birbirinden ve bankadaki diğer sorulardan farklıdır (`araclar/ek_yeni_sorular.py` aynı kökü reddeder). Onay: `python3 araclar/soru_yukselt.py && python3 araclar/ek_yeni_sorular.py --onayla`. Yeni parti eklemek için aynı biçimde `yeni_parti_17_*.tsv` yazmak yeterlidir.

**8 günlük programa geçişte eksik kalan 8.101 soru** bilgi tablosu üreticisiyle eklendi (`yeni_parti_16_<ders>.tsv`, `*-YS-0651…`): Tarih 1.600, Coğrafya 1.639, Vatandaşlık 1.650, Türkçe 1.562, Güncel 1.650. Bu sorular elle tek tek yazılmadı; `araclar/bilgi_veri/<ders>.py` içindeki doğrulanmış bilgi tablolarından `araclar/bilgi_soru_uret.py` ile üretildi ve `bilgi-tablosu` etiketi taşır.

Çeldirici ve akıl yürütme ağırlığı:
- **Düz bilgi soruları** (olay–yıl, il–bölge, madde–konu, ülke–başkent vb.): çeldiriciler rastgele değil, en yakın kayıtlardan (aynı dönem/yakın yıl, aynı bölge/komşu il, aynı kıta, aynı Anayasa bölümü) seçilir.
- **Öncüllü (I–II–III) sorular**: yanlış öncüller gerçeğe çok yakın tuzaklardır (ör. bir sonraki yüzyıla düşen olay, başka kavramın tanımı, komşu ilin kıyısı); şıklar doğru kombinasyona en yakın kombinasyonlardır ("I ve II" ↔ "I, II ve III" gibi iki şık arasında bırakır). Her öncülün neden doğru/yanlış olduğu çözümde tek tek yazılır.
- **Sıralama ve eşleştirme soruları**: kronolojik/coğrafi sıralamada şıklar doğru sıraya en yakın permütasyonlardır; eşleştirmede tek bir eşleşme farkıyla ayrışan şıklar bulunur.
- **Genel Kültür bilgi/ezber ağırlıklıdır**: Tarih, Coğrafya, Vatandaşlık ve Güncel'de üretilen soruların ≈%70'i düz bilgi sorusudur (≈1.120–1.175); öncüllü, sıralama ve eşleştirme soruları hedefin en çok %30'u ile sınırlıdır (`bilgi_soru_uret.py` → `AKIL_ORANI`). Bu derslerde paragraf sorusu yoktur.

**Türkçe (Genel Yetenek) paragraf ve dil bilgisi ağırlıklıdır** (1.562 soru):
- **Paragraf (693)**: `paragraf_metin1..4.py` içindeki 99 özgün paragraftan konu, ana düşünce, ana düşünce cümlesi, değinilmeyen, ulaşılamayan yargı, akışı bozan cümle ve boşluk doldurma soruları. Yakın-yanlış yargılar ve parçada geçen yardımcı düşünceler çeldiricidir; ana düşünce yalnız tek cümlede verilir.
- **Sözel mantık (230)**: sıralama ve eşleştirme bulmacaları; her soru tüm olası düzenler denenerek doğrulanır.
- **Dil bilgisi ve anlam (639)**: `dilbilgisi.py` + `dilbilgisi_veri1..3.py` içindeki elle denetlenmiş örnek cümlelerden, çıkmış sorulardaki gibi **numaralı cümle** ("Numaralanmış cümlelerin hangisinde … vardır/yoktur?"), **öncüllü** ve **ögelere ayırma** kalıplarında: anlatım bozukluğu (var/yok/nedeni/öncüllü), cümlede anlam ilişkileri (amaç-neden-koşul-karşılaştırma), anlam türleri, öznel-nesnel, yazım, noktalama (işaretin görevi), cümle ögeleri (diziliş, hangisinde X yoktur, hem X hem Y), cümle türleri (iki ölçüt birlikte), sözcük türleri (aynı sözcüğün farklı türde kullanımı çeldirici), yapı, ses olayları, fiilimsi, gerçek/mecaz anlam, deyim/atasözü/eş-zıt anlam öncüllüleri. Bozuk cümle ile kendi düzeltilmiş hâli aynı soruya konmaz; tek doğru cevap `test_dilbilgisi.py` ile sınanır.
- Tek bilgi soran kolay türler (deyimin anlamı, kısaltma, tek sözcüğün yazımı) artık üretilmez. Numaralı/öncüllü seçenekler KPSS'deki gibi sıralı gösterilir (I, II, …; Yalnız I, Yalnız II, I ve II, …).

**Farklı yollardan konu anlatımı**: `data/konu_yeniden.json` içindeki 123 konu kartının her birine `anlatimlar` alanı eklendi (toplam 519 blok): 🗂️ tablo/şema, ❓ soru–cevap, 🧩 çözümlü KPSS örneği, 🧠 hafıza kodu ve karıştırılanlar. Kaynak `araclar/konu_anlatim_veri/<ders>.py`; güncellemek için `python3 araclar/konu_anlatim_ekle.py`. Konu anlatımları sayfasındaki kartta hepsi, yanlış cevap sonrası tekrarda her seferinde başka bir anlatım yolu, test sonunda yanlış konularda tüm anlatımlar gösterilir.

**👩‍🏫 Üç hocadan konu anlatımı**: Beş dersin 50 ana konusunun her biri, öğretim tarzı birbirinden farklı üç hoca tarafından baştan sona anlatılır (50 × 3 = 150 tam anlatım, her biri ~1.400–3.000 karakter):

| Hoca | Tarz | Kuram / mantık | Bölümler |
|---|---|---|---|
| 📜 Kemal Hoca | Hikâyeci | Bütünden parçaya, anlamlı öğrenme: “Neden böyle oldu?” | Büyük resim → Hikâye → Neden–sonuç zinciri → Tek cümlede |
| 📐 Ayşe Hoca | Sistemci | Parçadan bütüne, şema kuramı: sınıflandırma, kural–istisna | Kavram haritası → numaralı bölümler → Kural ve istisna → Adım adım |
| 🎯 Murat Hoca | Soru Avcısı | Sınavdan geriye, geri getirme pratiği | Soru kalıpları → Anahtar kelime → cevap → Tuzaklar → Hafıza kodu → Mini test (3 soru) |

Kaynak `araclar/konu_anlatim_veri/hocalar.py` (hoca bilgileri) ve `hoca_<ders>.py` (`HOCA = {ana_konu: (kemal, ayşe, murat)}`; Türkçe ikinci yarısı `hoca_turkce_2.py`). `python3 araclar/konu_anlatim_ekle.py` her karta `hocalar` alanını yazar (`--kontrol` yalnızca kapsam ve kalite raporu verir; her metinde en az 3 ara başlık ve 700 karakter aranır). Arayüzde sekmelerle hoca değiştirilir: konu kartında (Hızlı Tur), her modül sayfasının sonunda (“3 hocadan anlatım”), yanlış cevap sonrası tekrarda (her yanlışta konuyu sıradaki hoca anlatır: Kemal → Ayşe → Murat) ve test sonu yanlış konu incelemesinde (Ayşe Hoca'dan başlar). Eski kısa kartlar “Ek çalışma kartları” olarak kapalı durur. Testler: `araclar/test_hocalar.py` (kapsam, hoca imza başlıkları, mini test, metinlerin birbirinden farklılığı, JSON'un kaynakla güncelliği) ve `smoke_test.js` (sekmeler).

Aynı kök iki kez üretilmez, bankadaki köklerle ve diğer derslerin çıktılarıyla çakışmaz; üretim deterministiktir. Hata bulunursa TSV yerine tabloyu düzeltip `python3 araclar/bilgi_soru_uret.py <ders>` → `python3 araclar/ek_yeni_sorular.py --onayla` → `python3 araclar/soru_yukselt.py` sırası izlenmelidir (bilgi tablosu kayıtları aynı kimlikle yerinde güncellenir; birden çok ders yeniden üretilecekse Tarih → Coğrafya → Vatandaşlık → Türkçe → Güncel sırası kullanılmalıdır).

| Ders | Aktif toplam | Deneme rezervi | Başlangıç test kapasitesi |
|---|---:|---:|---:|
| Tarih | 1.260 | 60 | 1.200 |
| Coğrafya | 1.207 | 46 | 1.161 |
| Vatandaşlık | 1.192 | 42 | 1.150 |
| Türkçe | 1.284 | 46 | 1.238 |
| Güncel | 1.176 | 26 | 1.150 |
| **Toplam** | **6.119** | **220** | **5.899** |

- Bu kapasite geçmişi boş profil içindir. Önceden kullanılan kayıtlar yeniden dağıtılmaz. Test menüsü kişisel kullanılmamış sayıyı da gösterir.
- Yarım kalan testin ayrılmış soruları kaybolmaz: **aynı oturumdan devam** bağlantısı vardır. Yeni oturuma tekrar dağıtılmaz; ilk cevaplanmamış sorudan devam edilir. İçerik veya kapsam değişmişse eski cevaplarla farklı bir soru gösterilmez.
- Günlük sayım tekil test id'lerine dayanır; gün **Europe/Istanbul** saat diliminde değişir. Gün değişimi kalıcı tekrar engelini kaldırmaz.
- `/api/meta.calisma_hedefi` günlük hedefi, deneme hariç kapasiteyi ve kamp açığını ayrı verir. **7 test günü boyunca ders başına 400 tekrarsız test sorusu için 2.800/ders, toplam 14.000 test + 220 ayrı deneme sorusu gerekir; mevcut havuz bunu tam karşılar (eksik 0).** Güncel'in 3.000'lik havuz hedefi ayrıca izlenir (şu an 2.826 aktif).

## Güncel için 3.000 soru hedefi ve mevcut soruların kalite turu

- **3.000, yalnız Güncel dersinin hedefidir; mevcut sayı değildir.** Güncel'de **1.176 aktif soru**, ara hedefe **1.824 soru eksik** vardır. Bu hedef `/api/meta` ve test menüsünde ayrı gösterilir.
- Önceki editoryal kalite turunda **her dersten 10, toplam 50 mevcut özgün soru** yeniden yazıldı. Havuz sayısı değişmedi.
- `kalite_01.tsv` senaryo, çıkarım ve kavram ayrımı odaklı yeniden yazımları; `kalite_01_inceleme.json` önceki tam kayıtları, önce/sonra SHA-256 özetlerini ve konu kararlarını saklar. Değişiklikler mevcut `yukselt_*.tsv` kaynaklarına da işlendi.
- Kısa eşleştirmelerin bir bölümü bağlama dönüştürüldü; çözümler yanlış seçeneklerin dayandığı yaygın karışıklıkları açıklar. Önceki 500'lük üretici de bu açık revizyonları korur.
- **ÖSYM görevlisi tarafından hazırlanmış resmî sorular değildir.** Özgün çalışma soruları KPSS ölçme yaklaşımı hedeflenerek yazılır; teknik testler güçlük kalibrasyonu veya tam puan garantisi vermez.
- Gerçek çıkmış/kitap metinleri ve basılı cevapları bu turda değiştirilmedi. 3.000'e tamamlandı veya bütün havuz yeniden editoryal olarak incelendi iddiası yoktur.

## Kapsam (Sınav Mufredatı — geçmiş KPSS konuları)

| Ders | Aktif konu alanları | Arşiv | Aktif |
|------|---------------------|-------|-------|
| **Tarih** | İlk Türk Devletleri → Osmanlı → Milli Mücadele → Devrimler → Çağdaş Tarih | 1.260 | 1.260 |
| **Coğrafya** | Harita–iklim → yer şekilleri → nüfus–ekonomi → bölgeler–afetler–çevre | 1.207 | 1.207 |
| **Vatandaşlık** | Hukuk → Anayasa → haklar → TBMM–yürütme–yargı → seçimler | 1.192 | 1.192 |
| **Türkçe** | Sözcükte/cümlede anlam → paragraf → **sözel mantık** → dil bilgisi | 1.284 | 1.284 |
| **Güncel** | Kurumlar → kültür–sanat → ülkeler → ödüller → spor | 1.360 | 1.176 |

### Bütün çözüm yollarında geçmiş KPSS konu kapsamı

- **6.119 aktif, 184 inceleme bekleyen kayıt** vardır. Arşiv silinmez; bekleyen kayıtlar
  konu/karışık test, telafi, doğrudan soru API'si veya denemede gösterilmez.
- `data/kpss_kapsam.json` 44 konu alanını, bankadaki **aynı dersten yıl/oturum etiketli**
  konu örneklerini ve her kayıt için içerik özeti + aktif/bekleyen kararını saklar.
  Konu dayanakları yalnız inceleme yılından önce tamamlanan yıllardan seçilir.
- **Konu eşleştirmesi geniş konu alanı düzeyindedir.** Özgün sorunun geçmiş sınavda
  sorulduğu veya her alt bilgisinin aynı geçmiş soruda bulunduğu ileri sürülmez.
  Banka kayıtlarının eşleştirilmesi, bağımsız ÖSYM kitapçık doğrulaması yerine geçmez.
- 184 bekleyen kaydın **63'ü haricen doğrulanmamış olay/atama/sonuç bilgileri**,
  **121'i bu incelemede aynı dersten konu dayanağı gösterilmeyen özgün genel bilim,
  teknoloji ve ekonomi içerikleridir**. Bunların hepsinin kesinlikle müfredat dışı olduğu
  iddia edilmez; belirsizlikte çözüm havuzuna alma yerine bekletme uygulanır.
- `kpss_kapsam.py` yalnız başlığa güvenmez: içerik değiştiğinde, yeni kayıt geldiğinde,
  konu örneği değiştiğinde veya başka dersten dayanak verildiğinde aktif izin düşer.
  Eksik/bozuk kapsam dosyasında ham banka yedek olarak servis edilmez.
- Her soru kartında kaynak satırından ayrı **Geçmiş KPSS konusu** bölümü vardır.
  Konu örneğinin yılı, özgün sorunun kaynak yılı gibi gösterilmez.
- `/api/meta` aktif sayıları; `/api/kapsam` sayıları ve bekleme gerekçelerini verir.
  `/api/soru/<id>` bekleyen kayıt için 404 döndürür; arşiv sorgusuyla aşılamaz.
- Arşiv denemeleri bellekte aynı ders dağılımı, soru sayısı ve tekillikle aktif havuza
  yansıtılır; denemeler arası id ve kök tekilliği de korunur. `data/denemeler.json`
  ve eski sonuçlar yerinde kalır; yeni oturumların gerçek soru idleri ayrıca kaydedilir.
  `araclar/deneme_uret.py` ile yeni üretimde de aynı filtre uygulanır.
- Yeni/değişmiş içerik için `python3 araclar/kapsam_taslagi.py --output /tmp/kapsam_taslak.json`
  **onaysız taslak** oluşturur. Etiketten önerilen konu otomatik onay değildir;
  taslak üretim kapsam dosyasının üzerine yazılamaz. İnceleme sonrası açık onay gerekir.
- `python3 araclar/veri_kontrol.py` arşiv bütünlüğü yanında kapsam envanterini de kontrol eder.
  Yeni veya değiştirilmiş soru onayı eksikse denetim hata verir.


> 📚 **Arşiv: 6.303; aktif çözüm havuzu: 6.119 soru** — arşivdeki kayıtların **404'ü KPSS yıl/oturum etiketi taşıyor**,
> **88'i yayınevi soru bankasından** (kitapların kendi cevap anahtarlarıyla, `📌 Kaynak` notlu).
>
> **Zorluk standardı (hedef: her dersi fullemek):** Yalnızca bizim yazdığımız
> "KPSS formatında" sorular, **çıkmış KPSS düzeyi hedeflenerek** yeniden
> yazılıyor: senaryolu/anlamlı kökler, olumsuz sorular, I-II-III kombinasyonları,
> eşleştirme; ayırt edici tuzak şıklar; her soruda "KPSS mantığı ile çözüm"
> (doğru + tuzak açıklaması). `araclar/soru_yukselt.py` ile yerinde güncellenir;
> `data/kaynaklar/yukselt_*.tsv` kaynak dosyalarıdır. **İlk havuzdaki yeniden yazım: 2116/2116; ayrıca 194 yeni özgün soru.**
> Yedinci turda kalan Coğrafya (6) ve Vatandaşlık (4) kayıtları da yenilendi (TSV 25–26).
> Arşivdeki 2310 özgün soru için yeniden yazım tamamlandı; bunların 121'i yukarıdaki
> kapsam incelemesinde bekletilir. Yeniden yazım ile aktif kapsam onayı farklıdır.
> Bu sayılar güçlük kalibrasyonu veya tam puan garantisi değildir.
> İkinci parti: 50 yeni yeniden yazım; önceki partide ayrıca 25 içerik düzeltmesi.
> Üçüncü parti: her dersten 10 olmak üzere 50 özgün soru daha yenilendi; toplam 200.
> Dördüncü parti: her dersten 20 olmak üzere **100 özgün soru** yenilendi; toplam 300.
> Beşinci parti: **her dersten 100, toplam 500 özgün soru** yenilendi; o parti sonunda kalan **1316** idi.
> Altıncı parti: **her dersten 300, toplam 1500 soru**: 1306 mevcut kayıt yeniden yazıldı,
> Tarih'e 71, Türkçe'ye 76, Güncel'e 47 yeni kayıt eklendi. Parti büyüklüğü artık
> **o partide ders başına 300**; günlük ders başı 500 hedefi değişmedi.
> `parti_1500_editor.txt` ve `parti_1500_senaryolar.txt` toplam **459 doğru/yanlış bilgi-çıkarım çifti**,
> 51 konu grubu içerir. `python3 araclar/parti_1500_uret.py` bunlardan 20–24 numaralı TSV'leri üretir.
> Aynı bilgiler farklı kümelerde yeniden ölçülebilir: bu **1500 ayrı elle yazılmış senaryo değildir**.
> 899 üç öncüllü, 306 yanlış yargıyı seçme, 295 doğru yargıyı seçme maddesi vardır. Aynı
> bilgi kümesi yalnız sırası veya doğruluk deseni değiştirilerek ikinci kez sayılmaz.
> `parti_1500_plan.json` hedefleri, yeni/eski ayrımını ve önce/sonra SHA-256 özetlerini sabitler.
> Önceden yenilenmiş 800 kayıt ve korumalı 555 kayıt altıncı turda değişmedi. Eski özgün kayıtların
> **734 konu etiketi yeni içeriğe uygun başlığa taşındı**; id, ders ve günleri değişmedi.
> Her yargı çözümde açıklanır; yanlış yargının doğru biçimi gösterilir. Açıklamadaki numaralar
> kökteki yargıya atıf yapar; A–E şıkları karıştırıldığında açıklama kaymaz.
> Kaynaklar özgün çalışma etiketiyle gösterilir; tahminî 2026 atama/ödül bilgileri eklenmez.
> Yeni id ekleme ve konu geçişi de kaynak korumasına tabidir; planla dahi çıkmış/kitap kaydı
> değiştirilemez. Beklenmeyen yerel düzenleme, eksik TSV veya son içerik uyuşmazlığı yazmayı durdurur.
> Hedef planı yalnız ilk hazırlamada `--plan` ile oluşturulmuştur; normal tekrar üretimde
> bu seçenek kullanılmaz. Plan var olduğunda üzerine yazma reddedilir.
> `parti_500_editor.json` elle hazırlanmış bilgi/cümle tablolarını ve sabit hedef id'lerini içerir;
> `python3 araclar/parti_500_uret.py` bunlardan yeniden üretilebilir TSV'ler hazırlar.
> Öncüllü eşleştirmeler, cümle değerlendirmeleri ve bağlam soruları kullanılır.
> Aynı öncül kümesini yalnızca sıralayarak yeni soru saymak engellenir. Çözümler
> doğru eşleşmeleri tek tek gösterir. Bunlar **özgün çalışma sorularıdır**, kitap alıntısı değildir.
> TSV'de `\n` ile saklanan kök satır sonları, uygulamada öncülleri ayrı satırlarda gösterir.
> `python3 -m unittest discover -s araclar -p 'test_*.py' -v` aktarım ve üretim testlerini çalıştırır.
> Bu sürümde **81 Python testi** ve `node --test araclar/test_soru_secimi.js` ile
> **24 seçim testi** başarılıdır. Güncel sunucudan fixture çekilerek çalıştırılan
> `araclar/smoke_test.js` **645 kontrolü** geçer (10'u öğrenme modu); her derste hem üç öncüllü hem beş yargılı
> kaydın satır sonu, kaynak, doğru şık ve çözüm gösterimi ayrıca kontrol edilir.
> Bu teknik testler editoryal bilgi doğruluğunu veya sınavla eş güçlüğü tek başına kanıtlamaz.
> Tüm yeniden yazımların şık, cevap ve çözüm aktarımı `test_yukselt_banka.py` ile denetlenir.
> Gerçek çıkmışlar ve yayınevi soruları araç tarafından değişikliğe karşı korunur.
> Girişler topluca doğrulanır; eksik id, tekrarlı şık veya korumalı kaynak varsa yazma yapılmaz.

> 📚 **Günlük 400 soruluk akışta kitap soruları önceliklidir:** her 10'luk sette önce Pegem / Öğreti
> kitap soruları, yalnız kullanılmamış ve denemeye ayrılmamışlarsa önceliklidir; sonra diğer uygun sorular seçilir. Setin
> başındaki `📚 Kitap` rozeti ve soru altındaki `📌 Kaynak` satırı hangi kitaptan olduğunu gösterir.
> Sorular yalnız aktif kapsamdan **10'luk setler** hâlinde gelir. Denemeler ayrıldıktan sonraki
> gerçek test kapasitesi, kişisel geçmiş ve günlük eksik sayı menüde gösterilir.
> Her 10 cevapta otomatik kontrol + telafi döngüsü. Havuzun sonundaki set 10 sorudan kısa olabilir; sayı için tekrar eklenmez.
>
> ✅ **Gerçek çıkmış sorular eklendi:** 2014–2026 arası resmî ÖSYM kitapçıklarından (Ortaöğretim +
> Ön Lisans + Lisans oturumları) **404 yıl/oturum etiketli soru** bankada bulunur. Bu turda bu kayıtlar
> değiştirilmemiştir. Her sorunun altında ve çözümünde `kaynak` etiketi yazar
> ("2018-KPSS", "2026-KPSS Lisans" gibi).

> ✅ **Yayınevi kitap soruları eklendi (12 Ekim):** 47 zorlu soru, yayınevi soru bankalarının **kendi
> basılı çözümleriyle** birebir aktarıldı; her sorunun altında `📌 Kaynak: <yıl> <yayınevi> <kitap>`
> yazıyor. Cevaplar yalnızca kitabın cevap anahtarından alınmıştır.
>
> | Kaynak (sorunun altında yazan) | Ders | Konu | Soru |
> |---|---|---|---|
> | 2022 Pegem Ezberbozan Tarih Soru Bankası | Tarih | İlk Türk Devletleri | 15 |
> | 2024 Pegem Ezberbozan Türkçe Soru Bankası | Türkçe | Sözcükte Anlam | 19 |
> | 2026 Pegem Ezberbozan Vatandaşlık Soru Bankası | Vatandaşlık | Hukuk | 13 |
> | 2024 Öğreti Akademi Efsane Tarih Soru Bankası | Tarih | İlk Türk Devletleri | 15 |
> | 2024 Öğreti Akademi Efsane Türkçe Soru Bankası | Türkçe | Sözcükte Anlam | 20 |
> | 2024 Öğreti Akademi Efsane Coğrafya Soru Bankası | Coğrafya | Koordinat (Konum) | 6 |

**Konu seçimi kuralı:** *Geçmiş KPSS konu alanlarıyla ilişkilendirilmiş ve kayıt bazında onaylanmış sorular.*
Bir konunun hiç sorulmadığına etiketlerden karar verilmez. Konu dayanağı gösterilemeyen kayıtlar
bekletilir; geniş konu eşleştirmesi her alt bilginin geçmişte sorulduğunun kanıtı değildir.

---

## Deneme Sonuçları Ertesi Günü Şekillendirir

Gün sonu denemesi bitince **yanlış/boş bıraktığın konular** otomatik olarak "odak listene" yazılır:

- Ertesi günün rehberinde **"🎯 Dünkü Denemeden Gelen Odakların"** paneli çıkar.
- Maraton ve testlerde bu konulardan gelen sorular **öncelikli** gelir.
- **Odak Testi** (10 soru) ile zayıf konularını doğrudan çalışabilirsin.
- Bir konudan doğru çözdükçe o konu listeden silinir — ta ustalaşana kadar.

## Sayfalar

- **🏠 Bugünün Rehberi** — 1. gün…8. gün numaralı, her gün için 3 adım: konu turu → 10'luk testler → deneme
- **📖 Konu Anlatımları** — 55 konunun hızlı turu + farklı anlatımı + 50 derin modül
- **✏️ Test Çöz** — Günün Maratonu / Konu Testi (10) / Yanlış Telafisi / Hata Atölyesi — hepsi 10'luk
- **📝 Denemeler** — 10 deneme + çözüm analizi
- **🎯 Hata Defteri** — zayıf konular + yanlış sorular + saldırı butonları
- **📊 İstatistik** — ustalık, ders başı 400 / toplam 2.000 günlük sayaç, net takibi
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
- `data/program.json` — 8 günlük plan (17–24 Ekim; `test_hedefi: false` olan 24 Ekim yalnızca deneme/tekrar)
- `data/denemeler.json` — 10 deneme
- `data/ilerleme/` — ilerleme kaydı (otomatik yedek)
- `araclar/soru_genislet.py` — yeni soru ekleme (TSV → JSONL)
- `araclar/deneme_uret.py` — denemeleri yeniden üret
- `araclar/veri_kontrol.py` — banka bütünlük kontrolü (`python3 araclar/veri_kontrol.py`)
- `araclar/refresh_fixtures.py` — sunucudan smoke fixture'ları çeker
- `araclar/smoke_test.js` — jsdom ile uçtan uca arayüz testi (645 kontrol)
- `araclar/konu_kartlari_ekle.py` — eksik konu anlatım kartlarını ekler (var olanı ezmez)

Yeni soru eklemek için `data/kaynaklar/*.tsv` dosyasına `ders|konu|gun|zorluk|kok|dogru|sikA..sikD|cozum1|cozum2|kaynak` yazıp `python3 araclar/soru_genislet.py` çalıştır.

---

*Başarılar! Önce konular, sonra yanlışlardan ustalığa — 10'luk testler, yalnız geçmiş KPSS konu havuzu; sayı için kapsam dışı soru yok.* 🚀
