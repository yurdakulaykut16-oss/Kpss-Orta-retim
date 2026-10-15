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

Otomatik kontrol (jsdom smoke — 645 kontrol):

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

> 📌 **Günlük soru hedefi:** Ders başına **500 soru** (toplam 2.500), **10'ar soruluk testler** hâlinde.
> Denemeler bu hedefe dahil değildir. Başlangıç test kapasitesi her derste en az 500'e çıkarıldı; geçmişi boş profil için ilk gün karşılanır. Bu, 10 gün boyunca tekrarsız 500'ün bütün içeriğinin hazır olduğu anlamına gelmez.
> Güncel havuz hedefi ayrıca **3.000** olarak belirlenmiştir; bu henüz tamamlanmış değildir.
> ⚠️ **Gerçek durum:** Aynı soru tekrar gelmediği için 1. gün her dersten 500 çözülürse 2. günden itibaren yeni test sorusu kalan: Tarih **50**, Coğrafya **11**, Vatandaşlık **0**, Türkçe **88**, Güncel **0**. Yani her gün her dersten 500 soru şu an **yalnız ilk gün** sağlanabiliyor.
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
- Her derste günlük **500 soru** hedeflenir (toplam **2.500**). Yalnız onaylı konu havuzu kullanılır; deneme rezervleri sayılmaz. Kullanılmış sorular gün değişince yeniden açılmaz; eksik kamp kapasitesi gizlenmez.

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
- 10 deneme (**DEN-01…DEN-10**), her gün 1 tanesi o günün rehberine bağlı: 5. ve 10. gün
  **50 soruluk büyük prova**, diğer günler 15 soruluk mini.
- Denemeler her dersi dengeli dağıtır, şıklar karışık gelir (sınav gibi).
- Süre geri sayar; bitirince **net + ders analizi + tüm çözümler**.

---

## Deneme hariç ders başına günlük minimum 500 test sorusu

Tek ayar kaynağı `data/calisma_hedefleri.json`: **500 soru/ders/gün**, **10 soru/set**, **50 setlik hedef/ders**, **2.500 test sorusu/gün**. Deneme bu sayılara eklenir; deneme doğru/yanlış/boşları test sayacını artırmaz. Her dersin 500'ü ayrı değerlendirilir; tek derste fazladan soru çözmek diğer dersin eksiğini kapatmaz.

İlk-gün eksiği için **26 Vatandaşlık + 162 Güncel = 188 yeni özgün soru** elle yazıldı. `ek_188_gunluk500.tsv` kök, beş seçenek ve gerekçeli çözümü içerir; `ek_188_inceleme.json` ayrı kapsam kararlarının içerik özetlerini saklar. Şık sıralaması dışında otomatik varyant üretimi yoktur. `soru_yukselt.py` ekleri de doğrulayarak uygular; mevcut farklı içerik veya korumalı kaynak sessizce ezilemez. Önceki 2.865 kayıt değiştirilmedi.

| Ders | Aktif toplam | Deneme rezervi | Başlangıç test kapasitesi |
|---|---:|---:|---:|
| Tarih | 610 | 60 | 550 |
| Coğrafya | 557 | 46 | 511 |
| Vatandaşlık | 542 | 42 | 500 |
| Türkçe | 634 | 46 | 588 |
| Güncel | 526 | 26 | 500 |
| **Toplam** | **2.869** | **220** | **2.649** |

- Bu kapasite geçmişi boş profil içindir. Önceden kullanılan kayıtlar yeniden dağıtılmaz. Test menüsü kişisel kullanılmamış sayıyı da gösterir.
- Yarım kalan testin ayrılmış soruları kaybolmaz: **aynı oturumdan devam** bağlantısı vardır. Yeni oturuma tekrar dağıtılmaz; ilk cevaplanmamış sorudan devam edilir. İçerik veya kapsam değişmişse eski cevaplarla farklı bir soru gösterilmez.
- Günlük sayım tekil test id'lerine dayanır; gün **Europe/Istanbul** saat diliminde değişir. Gün değişimi kalıcı tekrar engelini kaldırmaz.
- `/api/meta.calisma_hedefi` günlük hedefi, deneme hariç kapasiteyi ve kamp açığını ayrı verir. **10 gün boyunca ders başına 500 tekrarsız test sorusu için 5.000/ders, toplam 25.000 test + 220 ayrı deneme sorusu gerekir.** Mevcut test havuzuyla bu hedefe **22.351 test sorusu eksiktir**; bütün kampın hazır olduğu iddia edilmez. Güncel'in 3.000 hedefi bu daha büyük ihtiyacın ara hedefidir.

## Güncel için 3.000 soru hedefi ve mevcut soruların kalite turu

- **3.000, yalnız Güncel dersinin hedefidir; mevcut sayı değildir.** Güncel'de **526 aktif soru**, ara hedefe **2.474 soru eksik** vardır. Bu hedef `/api/meta` ve test menüsünde ayrı gösterilir.
- Önceki editoryal kalite turunda **her dersten 10, toplam 50 mevcut özgün soru** yeniden yazıldı. Havuz sayısı değişmedi.
- `kalite_01.tsv` senaryo, çıkarım ve kavram ayrımı odaklı yeniden yazımları; `kalite_01_inceleme.json` önceki tam kayıtları, önce/sonra SHA-256 özetlerini ve konu kararlarını saklar. Değişiklikler mevcut `yukselt_*.tsv` kaynaklarına da işlendi.
- Kısa eşleştirmelerin bir bölümü bağlama dönüştürüldü; çözümler yanlış seçeneklerin dayandığı yaygın karışıklıkları açıklar. Önceki 500'lük üretici de bu açık revizyonları korur.
- **ÖSYM görevlisi tarafından hazırlanmış resmî sorular değildir.** Özgün çalışma soruları KPSS ölçme yaklaşımı hedeflenerek yazılır; teknik testler güçlük kalibrasyonu veya tam puan garantisi vermez.
- Gerçek çıkmış/kitap metinleri ve basılı cevapları bu turda değiştirilmedi. 3.000'e tamamlandı veya bütün havuz yeniden editoryal olarak incelendi iddiası yoktur.

## Kapsam (Sınav Mufredatı — geçmiş KPSS konuları)

| Ders | Aktif konu alanları | Arşiv | Aktif |
|------|---------------------|-------|-------|
| **Tarih** | İlk Türk Devletleri → Osmanlı → Milli Mücadele → Devrimler → Çağdaş Tarih | 610 | 610 |
| **Coğrafya** | Harita–iklim → yer şekilleri → nüfus–ekonomi → bölgeler–afetler–çevre | 557 | 557 |
| **Vatandaşlık** | Hukuk → Anayasa → haklar → TBMM–yürütme–yargı → seçimler | 542 | 542 |
| **Türkçe** | Sözcükte/cümlede anlam → paragraf → **sözel mantık** → dil bilgisi | 634 | 634 |
| **Güncel** | Kurumlar → kültür–sanat → ülkeler → ödüller → spor | 710 | 526 |

### Bütün çözüm yollarında geçmiş KPSS konu kapsamı

- **2.869 aktif, 184 inceleme bekleyen kayıt** vardır. Arşiv silinmez; bekleyen kayıtlar
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


> 📚 **Arşiv: 3.053; aktif çözüm havuzu: 2.869 soru** — arşivdeki kayıtların **404'ü KPSS yıl/oturum etiketi taşıyor**,
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

> 📚 **Günlük 500 soruluk akışta kitap soruları önceliklidir:** her 10'luk sette önce Pegem / Öğreti
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
- `araclar/smoke_test.js` — jsdom ile uçtan uca arayüz testi (645 kontrol)
- `araclar/konu_kartlari_ekle.py` — eksik konu anlatım kartlarını ekler (var olanı ezmez)

Yeni soru eklemek için `data/kaynaklar/*.tsv` dosyasına `ders|konu|gun|zorluk|kok|dogru|sikA..sikD|cozum1|cozum2|kaynak` yazıp `python3 araclar/soru_genislet.py` çalıştır.

---

*Başarılar! Önce konular, sonra yanlışlardan ustalığa — 10'luk testler, yalnız geçmiş KPSS konu havuzu; sayı için kapsam dışı soru yok.* 🚀
