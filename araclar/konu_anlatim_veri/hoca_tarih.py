"""Tarih — üç hocadan anlatım (Kemal: hikâye/neden-sonuç, Ayşe: sistem/şema, Murat: soru avcılığı)."""

HOCA = {}

HOCA['İlk Türk Devletleri'] = (
"""§ Büyük resim
Bozkırda yaşayan bir toplum düşün: otlak biterse göç eder, at olmadan yaşayamaz, kışın hayvanı ölürse aç kalır. İlk Türk devletlerinin bütün özellikleri bu bozkır hayatından doğar. Göçebe oldukları için kalıcı mimari az, buna karşılık taşınabilir sanat (hayvan üslubu, kilim, maden işçiliği) çoktur.

§ Hikâye: dededen toruna
Asya Hun Devleti'ni MÖ 220 civarında Teoman kurar; ama devleti büyüten oğlu Mete'dir. Mete orduyu onlu sisteme göre (10, 100, 1000, 10 000) örgütler; bu sistem binlerce yıl Türk ordularının iskeleti olur. Çinliler bu atlı akınlardan korunmak için Çin Seddi'ni güçlendirir. Hunların bir kolu batıya kayar; 375'te Balamir önderliğindeki Avrupa Hunları Kavimler Göçü'nü tetikler, Attila zamanında Roma'yı vergiye bağlar.
552'de Bumin Kağan Avarları yıkar ve Kök Türk (Göktürk) Devleti'ni kurar: tarihte ilk kez "Türk" adı bir devletin resmî adı olur. Batıyı kardeşi İstemi Yabgu yönetir; bu ikili teşkilattır. Devlet 630'da Çin egemenliğine girer, fakat Kutluk (İlteriş) Kağan 682'de bağımsızlığı yeniden kazanır (II. Göktürk / Kutluk Devleti). Bilge Kağan, kardeşi Kül Tigin ve vezir Tonyukuk'un anısına dikilen Orhun Yazıtları, Türklerin kendi dilleriyle yazdıkları ilk tarih belgesidir.
744'te Uygurlar devralır. Bögü Kağan Maniheizm'i benimser; bu din et yemeyi ve savaşçılığı hoş görmediği için Uygurlar tarıma, şehir hayatına, kâğıt ve matbaa kullanımına yönelir. 840'ta Kırgızlar başkenti yıkınca Uygurlar dağılır; bir kısmı batıya göç ederek Karahanlıların kuruluşunda rol oynar.

§ Neden–sonuç zinciri
Göçebelik → at ve ordu merkezli hayat → "ordu-millet" anlayışı.
Kut inancı (yönetme yetkisi Tanrı'dan gelir ve hanedan üyeleri arasında paylaşılır) → her şehzadenin taht hakkı → taht kavgaları → devletlerin kısa ömürlü olması.
Uygurların yerleşik hayata geçmesi → tarım, mimari, yazılı kültür → "ilk"lerin çoğu Uygurlarda.

§ Tek cümlede
Bozkır şartları ortak özellikleri, kut anlayışı ise kısa ömrü açıklar; Hun ordu kurdu, Göktürk adını ve yazısını verdi, Uygur yerleşti.""",

"""§ Kavram haritası
İlk Türk devletleri üç başlıkta incelenir: 1) Devletler ve "ilk"leri, 2) Devlet yönetimi, 3) Kültür ve inanç.

§ 1) Devletler — tek satırlık kimlik kartları
• Asya Hun (MÖ 220 – MS 216): kurucu Teoman, en güçlü Mete; onlu ordu sistemi.
• Avrupa Hun: Balamir 375 Kavimler Göçü; Attila; Margos (435) ve Anatolios (443) antlaşmaları.
• I. Göktürk (552–630): Bumin; "Türk" adlı ilk devlet; İstemi Yabgu batıda.
• II. Göktürk / Kutluk (682–744): Kutluk, Kapgan, Bilge Kağan; Orhun Yazıtları (Tonyukuk, Kül Tigin, Bilge Kağan).
• Uygur (744–840): Mani dini, yerleşik hayat, Uygur alfabesi, kâğıt ve matbaa.
• Diğer: Avarlar (İstanbul'u kuşatan ilk Türk topluluğu, 626), Hazarlar (yönetici kesimi Musevi), Peçenek, Kuman-Kıpçak, Bulgar.

§ 2) Devlet yönetimi
• Hükümdar: kağan / han; eşi hatun (devlet işlerine katılır).
• Kut: yönetme yetkisi Gök Tanrı'dan gelir.
• Kurultay (toy): danışma meclisi; son söz hükümdarda.
• İkili teşkilat: doğu (merkez, kağan) – batı (yabgu).
• Töre: yazısız hukuk kuralları; hükümdar da töreye uymak zorundadır.

§ 3) Kültür ve inanç
• Gök Tanrı inancı; ölüm sonrası: kurgan (mezar), balbal (öldürülen düşman sayısı), yuğ (cenaze töreni).
• Ekonomi: hayvancılık; ticaret yolu (İpek Yolu) denetimi önemli.
• Sanat: hayvan üslubu, maden işçiliği, halı-kilim.

§ Kural ve istisna
Kural: ilk Türk devletleri göçebedir. İstisna: Uygurlar yerleşiktir.
Kural: Türkler Gök Tanrı inancındadır. İstisna: Uygur yöneticileri Maniheizm, Hazar yöneticileri Musevilik.
Kural: kurucu = en güçlü hükümdar değildir (Hun'da Teoman ↔ Mete).

§ Adım adım çözüm algoritması
1. Soruda geçen bilgi göçebe hayatla mı ilgili, yerleşik hayatla mı? Yerleşikse Uygur'u düşün.
2. "Türk adı / yazıt" geçiyorsa Göktürk.
3. "Ordu teşkilatı / Çin Seddi" geçiyorsa Hun.
4. Ortak özellik soruluyorsa istisnayı (Uygur, Hazar) eleyerek kalanı seç.""",

"""§ Soru kalıpları
1) "Aşağıdakilerden hangisi ilk Türk devletlerinin ortak özelliklerinden biri değildir?" → cevap genellikle yerleşik hayat ya da tek tanrılı din gibi istisnadır.
2) "Göktürklere ait bilgiler hangileridir?" öncüllü soru → Göktürk ve Uygur özellikleri çaprazlanır.
3) "Türklerin yerleşik hayata geçtiğinin kanıtı olabilecek gelişme hangisidir?" → tapınak, saray, tarım, kâğıt-matbaa.

§ Anahtar kelime → cevap
• "Türk adı resmî olarak / Orhun / Tonyukuk" → Göktürk
• "Onlu sistem / Çin Seddi / Mete" → Asya Hun
• "Mani / matbaa / kâğıt / yerleşik / Bögü" → Uygur
• "Kavimler Göçü / 375 / Balamir / Attila" → Avrupa Hun
• "İstanbul'u kuşatan ilk Türk" → Avar (626)
• "Musevi yönetici" → Hazar

§ Tuzaklar
• Kurucu ile en güçlü hükümdar: Teoman ↔ Mete.
• Yazıtların "yazarı" ile "adına dikilen": Kül Tigin ve Bilge Kağan yazıtlarının metni Yolluğ Tigin'e, Tonyukuk yazıtı Tonyukuk'un kendisine aittir.
• "İlk Müslüman Türk devleti" sorusunda Uygur seçeneği çeldiricidir; doğrusu Karahanlı.
• "Yerleşik hayata geçen ilk Türk devleti" için Hun, Göktürk seçenekleri çeldiricidir.

§ Hafıza kodu
"TE-ME-BU-KU-BÖ": TEoman kurdu, MEte ordu, BUmin Türk adı, KUtluk yeniden kurdu, BÖgü Mani'ye geçti.
Yerleşiklik kodu: "UY = Uyudu, Yerleşti" (Uygur çadırı bıraktı, eve yerleşti).

§ Mini test (cevabı okumadan dene)
1. Kut anlayışının taht kavgalarına yol açmasının nedeni nedir? — Cevap: Yönetme yetkisinin hanedanın bütün erkek üyelerine geçebileceği inancı.
2. "Kâğıt ve matbaa kullanımı" hangi devlette görülür? — Cevap: Uygurlar.
3. Hükümdarın da uymak zorunda olduğu yazısız kurallara ne denir? — Cevap: Töre.""",
)

HOCA['Türk-İslam Devletleri'] = (
"""§ Büyük resim
Bir yol ayrımı düşün: 751'de Talas'ta Abbasi ordusu ile Çinliler karşı karşıyadır. Savaşın ortasında Karluk Türkleri Abbasi tarafına geçer ve Çin yenilir. Bu an, Türklerin yüzünü Çin'den İslam dünyasına çeviren dönüm noktasıdır. Bundan sonra Türkler hem İslam'ı benimseyecek hem de kısa süre içinde İslam dünyasının siyasi koruyucusu olacaktır.

§ Hikâye: üç devlet, üç rol
Karahanlılar (840–1212) "kültür" rolünü üstlenir: Satuk Buğra Han'ın Müslüman olmasıyla İslam'ı benimseyen ilk Türk devletidir. Türkçeyi resmî dil olarak korurlar; Yusuf Has Hacip Kutadgu Bilig'i (mutluluk veren bilgi, bir siyasetname), Kaşgarlı Mahmut Divanü Lügati't-Türk'ü (Araplara Türkçe öğretmek için sözlük) yazar.
Gazneliler (963–1187) "fetih" rolünü üstlenir: Sultan Mahmut "sultan" unvanını kullanan ilk Türk hükümdarıdır ve Hindistan'a 17 sefer düzenleyerek İslam'ı oraya taşır. Firdevsi Şehname'yi ona sunar.
Büyük Selçuklular (1040–1157) "koruyucu" rolünü üstlenir: Tuğrul ve Çağrı Beyler 1040 Dandanakan'da Gaznelileri yenip devleti kurar. Tuğrul Bey 1055'te Bağdat'a girerek halifeyi Büveyhoğullarından kurtarır ve "Doğunun ve Batının Sultanı" unvanını alır. Alparslan 1071 Malazgirt'te Bizans'ı yenerek Anadolu'nun kapısını açar. Melikşah döneminde devlet en geniş sınırlarına ulaşır; veziri Nizamülmülk Nizamiye Medreselerini kurar ve Siyasetname'yi yazar. Sencer 1141 Katvan'da Karahıtaylara yenilince devlet zayıflar, 1157'de dağılır.

§ Neden–sonuç zinciri
Talas (751) → Türklerin İslam'a girişi hızlanır → Karahanlılar ilk Müslüman Türk devleti olur.
Dandanakan (1040) → Selçuklu kuruluşu → Pasinler (1048) Bizans'la ilk karşılaşma → Malazgirt (1071) → Anadolu Türk yurdu olmaya başlar.
Halifeyi koruma → Selçukluların İslam dünyasında siyasi liderliği → Haçlılara karşı mücadele ilerde Türklere kalır.

§ Tek cümlede
Karahanlı kültürü, Gazneli fethi, Selçuklu ise koruyuculuğu ve Anadolu'nun kapısını temsil eder.""",

"""§ Kavram haritası
Türk-İslam devletleri = 1) Geçiş (Talas), 2) Devletler, 3) Yönetim kurumları, 4) Bilim-kültür eserleri.

§ 1) Geçiş
• Talas Savaşı 751: Abbasi + Karluk ↔ Çin. Sonuç: Çin'in Orta Asya'daki etkisi azaldı, Türkler İslam'a yöneldi, kâğıt yapımı İslam dünyasına geçti.

§ 2) Devletler karşılaştırması
Devlet | Kurucu / önemli hükümdar | Ayırt edici bilgi
Karahanlı | Bilge Kül Kadir Han; Satuk Buğra Han | İlk Müslüman Türk devleti; Türkçe resmî dil; 1042'de doğu-batı diye ikiye ayrıldı
Gazneli | Alptekin; Sultan Mahmut | Sultan unvanını ilk kullanan; Hindistan'a 17 sefer; Dandanakan'da yenildi
Büyük Selçuklu | Tuğrul-Çağrı; Alparslan; Melikşah; Sencer | Dandanakan 1040 kuruluş; Bağdat 1055; Malazgirt 1071; Katvan 1141
Harzemşahlar | — | Moğol baskısıyla yıkıldı (1231); Celaleddin Harzemşah Yassıçemen'de (1230) Anadolu Selçuklu'ya yenildi

§ 3) Yönetim kurumları
• Sultan; melik (şehzade) sistemi; atabey (şehzadeyi yetiştiren devlet adamı).
• Divan-ı Saltanat: devlet işlerinin görüşüldüğü merkez divan.
• İkta: toprağın vergi geliri karşılığında asker yetiştirme düzeni; hazineye yük olmadan ordu, üretimin sürmesi.
• Nizamiye Medreseleri: devlet eliyle kurulan ilk düzenli medreseler (1067 Bağdat).

§ 4) Eser–yazar eşleşmesi
Kutadgu Bilig – Yusuf Has Hacip (siyasetname) | Divanü Lügati't-Türk – Kaşgarlı Mahmut (sözlük) | Atabetü'l-Hakayık – Edip Ahmet (ahlak) | Divan-ı Hikmet – Ahmet Yesevi (tasavvuf) | Siyasetname – Nizamülmülk | Şehname – Firdevsi.

§ Kural ve istisna
Kural: Türk-İslam devletlerinde ülke hanedanın ortak malıdır (eski kut anlayışı sürer). Sonuç: taht kavgaları ve bölünmeler devam eder.
İstisna sorulursa: sultan unvanını ilk kullanan (Gazneli Mahmut) ile halifeden resmen alan (Tuğrul Bey) farklıdır.

§ Adım adım kronoloji
8. yy: Talas (751) → 10. yy: Karahanlıların Müslümanlığı, Gazne (963) → 11. yy: Dandanakan 1040, Pasinler 1048, Bağdat 1055, Malazgirt 1071 → 12. yy: Katvan 1141, yıkılış 1157.""",

"""§ Soru kalıpları
1) Eser–yazar eşleştirmesi (en sık).
2) Savaş sıralaması: Talas, Dandanakan, Pasinler, Malazgirt, Katvan.
3) "Hangisi ilk kez ... devletinde görülür?" (ilk Müslüman Türk devleti, ilk sultan, ilk medrese).
4) "Malazgirt'in sonuçlarından biri değildir" tarzı neden-sonuç.

§ Anahtar kelime → cevap
• "İlk Müslüman Türk devleti / Türkçe resmî dil / Kutadgu Bilig" → Karahanlı
• "17 sefer / Hindistan / sultan unvanını ilk kullanan" → Gazneli
• "Bağdat'a giren / halifeyi koruyan" → Tuğrul Bey (Büyük Selçuklu)
• "Anadolu'nun kapıları" → Malazgirt 1071
• "Nizamiye / Siyasetname / ikta düzenleyen vezir" → Nizamülmülk, Melikşah dönemi
• "Karahıtay" → Katvan 1141, Sencer

§ Tuzaklar
• Dandanakan Bizans'a karşı değil, Gaznelilere karşıdır. Bizans'la ilk savaş Pasinler'dir.
• Divanü Lügati't-Türk bir siyasetname değil sözlüktür; siyasetname olan Kutadgu Bilig'dir.
• Kösedağ (1243) Büyük Selçuklu değil, Anadolu Selçuklu yenilgisidir.
• "Sultan unvanını kullanan ilk" (Mahmut) ile "halifeden alan ilk" (Tuğrul) karıştırılır.

§ Hafıza kodu
"Da-Pa-Ma": DAndanakan 1040 → PAsinler 1048 → MAlazgirt 1071 (alfabe sırası = kronoloji).
Eserler için "KuYu-DiKa-AtEd-DiYe": KUtadgu-YUsuf, DİvanüLügat-KAşgarlı, ATabetü'l-EDip, DİvanHikmet-YEsevi.

§ Mini test
1. "Talas, Malazgirt, Dandanakan, Katvan" sırası? — Cevap: Talas (751) → Dandanakan (1040) → Malazgirt (1071) → Katvan (1141).
2. İkta sisteminin hazineye katkısı nedir? — Cevap: Ordu, hazineden maaş ödenmeden toprak gelirleriyle beslenir.
3. Araplara Türkçe öğretmek amacıyla yazılan eser? — Cevap: Divanü Lügati't-Türk.""",
)

HOCA['Anadolu Selçuklu ve Beylikler'] = (
"""§ Büyük resim
Malazgirt (1071) kapıyı açtı ama Anadolu'yu yurt yapmak kolay değildi: batıda Bizans, güneyde Haçlılar, doğuda önce Harzemşahlar sonra Moğollar vardı. Anadolu Selçuklu Devleti'nin hikâyesi, bu üç baskı arasında Anadolu'yu Türkleştirme ve zenginleştirme hikâyesidir.

§ Hikâye
Süleyman Şah 1075'te İznik'i başkent yaparak devleti kurar. I. Haçlı Seferi (1096–1099) İznik'i kaybettirir, başkent Konya'ya taşınır. II. Kılıçarslan 1176'da Miryokefalon'da Bizans'ı yenince Bizans, Anadolu'yu geri alma umudunu kaybeder; Anadolu'nun Türk yurdu olduğu kesinleşir.
Ardından "denize açılma" dönemi gelir: Antalya (1207) ve Sinop (1214) alınır, Alâeddin Keykubat Alanya'yı alır ve Kırım'daki Suğdak'a sefer düzenler. Kervansaraylar yapılır, tüccarın malı yolda kaybolursa devlet tazmin eder; bu bir tür devlet sigortasıdır. Ahi Evran'ın kurduğu Ahilik, esnafı hem meslek hem ahlak açısından örgütler.
Sonra kader değişir: 1230 Yassıçemen'de Harzemşahlar yenilir, ama bu zafer Moğollarla aradaki tamponu kaldırır. 1240'ta Babai İsyanı devleti sarsar, 1243 Kösedağ'da Moğollara yenilen devlet dağılma sürecine girer. Merkezî otorite çökünce uç bölgelerde beylikler güçlenir; bunlardan biri, Söğüt'teki küçük Osmanlı Beyliği'dir.

§ Neden–sonuç zinciri
Miryokefalon → Bizans savunmaya geçer → Anadolu Türkleşir.
Limanların alınması + kervansaray + sigorta → ticaret canlanır → şehirler ve esnaf (Ahilik) gelişir.
Yassıçemen → tampon kalkar → Kösedağ → Moğol hâkimiyeti → beylikler dönemi → Osmanlı'nın doğuşu.
Karamanoğlu Mehmet Bey'in 1277'de Türkçeyi resmî dil ilan etmesi, Selçuklu sarayında Farsçanın ağırlığına bir tepkidir.

§ Tek cümlede
Miryokefalon Anadolu'yu kesinleştirdi, ticaret onu zenginleştirdi, Kösedağ onu beyliklere böldü.""",

"""§ Kavram haritası
1) Anadolu Selçuklu siyasi tarihi, 2) Birinci dönem beylikleri, 3) İkinci dönem beylikleri, 4) Kültür ve ekonomi kurumları.

§ 1) Siyasi tarih — beş durak
Kuruluş 1075 İznik (Süleyman Şah) → Konya'ya taşınma (I. Haçlı sonrası) → Miryokefalon 1176 (II. Kılıçarslan) → Yassıçemen 1230 (Alâeddin Keykubat, Harzemşahlara karşı) → Kösedağ 1243 (II. Gıyaseddin Keyhüsrev, Moğollara yenilgi).

§ 2) Birinci dönem (Malazgirt sonrası) beylikleri
Saltuklu – Erzurum | Mengücekli – Erzincan, Divriği (Divriği Ulu Camii ve Darüşşifası) | Danişmentli – Sivas, Tokat, Amasya (Danişmentname) | Artuklu – Hasankeyf, Mardin, Diyarbakır (Malabadi Köprüsü) | Çaka – İzmir (ilk Türk donanması).

§ 3) İkinci dönem (Kösedağ sonrası) beylikleri
Karamanoğulları – Konya, Karaman (1277 Türkçe resmî dil) | Germiyanoğulları – Kütahya | Aydınoğulları – Aydın, İzmir (Umur Bey, denizcilik) | Candaroğulları – Kastamonu, Sinop | Karesioğulları – Balıkesir (Osmanlı'ya katılan ilk beylik; donanmasıyla Osmanlı'nın Rumeli'ye geçişine katkı) | Menteşe – Muğla | Saruhan – Manisa | Dulkadiroğulları – Maraş, Elbistan | Ramazanoğulları – Adana | Eretna – Sivas, Kayseri.

§ 4) Kurumlar
• Kervansaray: ticaret yolları üzerinde konaklama ve güvenlik.
• Devlet sigortası: yolda zarara uğrayan tüccarın kaybını devlet karşılar.
• Ahilik: esnaf-sanatkâr teşkilatı (Ahi Evran); kalite ve ahlak denetimi. Kadınlar kolu: Bacıyân-ı Rûm.
• Darüşşifa: hastane (Kayseri Gevher Nesibe, Divriği).

§ Kural ve istisna
Kural: ilk beylikler doğu ve iç Anadolu'dadır. İstisna: Çaka Beyliği batıda, İzmir'dedir ve denizcidir.
Kural: Selçuklu yenilgisi = Moğol. İstisna: Haçlılar başkent değişikliğine yol açmıştır (İznik → Konya).

§ Adım adım
Soruda tarih 1071–1243 arasıysa Selçuklu, 1243 sonrasıysa beylikler; "deniz" geçiyorsa Çaka / Aydınoğulları / Karesi; "Türkçe" geçiyorsa Karamanoğulları.""",

"""§ Soru kalıpları
1) "Miryokefalon Savaşı'nın önemi nedir?" → Bizans'ın Anadolu'yu geri alma umudu kalmadı.
2) Beylik – merkez – özellik eşleştirmesi.
3) "Anadolu Selçuklularının ticareti geliştirmek için aldığı önlemlerden biri değildir" → seçeneklerde kapitülasyon / tımar gibi Osmanlı kavramı çeldiricidir.
4) Kösedağ'ın sonuçları (Moğol hâkimiyeti, beyliklerin güçlenmesi).

§ Anahtar kelime → cevap
• "Anadolu'nun Türk yurdu olduğu kesinleşti" → Miryokefalon 1176
• "Anadolu'nun kapıları açıldı" → Malazgirt 1071 (karıştırma!)
• "İlk Türk donanması" → Çaka Bey
• "Türkçe resmî dil (1277)" → Karamanoğlu Mehmet Bey
• "Osmanlı'ya katılan ilk beylik" → Karesioğulları
• "Moğol / dağılma" → Kösedağ 1243
• "Esnaf teşkilatı" → Ahilik

§ Tuzaklar
• Malazgirt "kapıyı açar", Miryokefalon "kesinleştirir". İkisinin sonuç cümleleri yer değiştirilerek sorulur.
• Yassıçemen bir zaferdir ama olumsuz sonucu vardır (Moğol tamponunun kalkması). "Olumsuz sonuç doğuran zafer" ifadesi Yassıçemen'i işaret eder.
• Divriği Ulu Camii Mengücekli eseridir, Artuklu değil.

§ Hafıza kodu
Birinci dönem beylikleri: "SAMEDAÇ" → SAltuklu, MEngücekli, DAnişmentli, Artuklu, ÇAka.
Selçuklu durakları: "İK-MY-YK" → İznik-Konya, Miryokefalon-Yassıçemen, Kösedağ (75-76-30-43 rakamlarıyla: 1075, 1176, 1230, 1243).

§ Mini test
1. Moğollarla aradaki tamponun kalkmasına yol açan savaş? — Cevap: Yassıçemen (1230).
2. Danişmentname hangi beyliğin destanıdır? — Cevap: Danişmentliler.
3. Tüccarın zararını devletin karşılaması hangi amaca hizmet eder? — Cevap: Ticaret yollarını güvenli kılarak ticareti canlandırmak.""",
)

HOCA['Osmanlı Kuruluş-Yükselme'] = (
"""§ Büyük resim
Söğüt'te küçük bir uç beyliği nasıl üç kıtaya yayılan bir imparatorluğa dönüştü? Cevap üç kelimede saklıdır: konum, gaza ve kurumlar. Osmanlı, Bizans sınırında olduğu için gaza (cihat) ruhuyla gönüllüleri topladı; zayıflayan Bizans'a karşı genişledi; sonra kurduğu kurumlarla (tımar, devşirme, divan) fethettiği yerleri elde tuttu.

§ Hikâye: babadan oğula bir imparatorluk
Osman Bey 1299'da beyliği kurar, 1302 Koyunhisar'da Bizans'ı yener. Oğlu Orhan Bey Bursa'yı (1326) alıp başkent yapar, Maltepe (Pelekanon, 1329) ile Bizans'ı Anadolu'dan uzaklaştırır, Karesioğulları'nı alıp donanma kazanır ve 1353'te Çimpe Kalesi ile Rumeli'ye adım atar. I. Murat Edirne'yi alır; Sırpsındığı (1364) ve I. Kosova (1389) ile Balkanlarda tutunur, devşirme ve yeniçeri ocağını kurar. Yıldırım Bayezid Niğbolu'da (1396) Haçlıları yener, İstanbul'u kuşatır; fakat 1402'de Ankara'da Timur'a yenilince devlet Fetret Devri'ne (1402–1413) düşer, şehzadeler taht için savaşır. Çelebi Mehmet birliği kurar, II. Murat Varna (1444) ve II. Kosova (1448) ile Balkanları kesinleştirir.
II. Mehmet (Fatih) 1453'te İstanbul'u alır: Orta Çağ kapanır, Yeni Çağ başlar. Kanunname ile padişahın yetkisini güçlendirir. Yavuz Sultan Selim Çaldıran (1514), Mercidabık (1516) ve Ridaniye (1517) ile Doğu'yu ve Mısır'ı alır, halifelik Osmanlı'ya geçer. Kanuni Sultan Süleyman (1520–1566) döneminde Belgrad (1521), Rodos (1522), Mohaç (1526), Viyana Kuşatması (1529), Preveze (1538) ile devlet zirveye çıkar.

§ Neden–sonuç zinciri
Bizans sınırı + gaza → gönüllü savaşçılar → hızlı büyüme.
Ankara Savaşı → Fetret → ama devşirme ve tımar kurumları sağlam olduğu için devlet yıkılmaz.
İstanbul'un fethi → ticaret yollarının denetimi → Avrupalıların yeni yollar araması → Coğrafi Keşifler.
Halifeliğin geçişi → Osmanlı İslam dünyasının lideri olur.

§ Tek cümlede
Osman kurdu, Orhan Rumeli'ye geçti, Murat kurumları kurdu, Fatih imparatorluğa, Yavuz halifeliğe, Kanuni zirveye taşıdı.""",

"""§ Kavram haritası
Kuruluş (1299–1453) ve Yükselme (1453–1579) dönemleri; her padişah için "fetih – savaş – kurum" üçlüsü.

§ Kuruluş dönemi tablosu
Osman Bey: Koyunhisar 1302 (Bizans'la ilk savaş).
Orhan Bey: Bursa 1326, Maltepe 1329 (Bizans'la son savunma savaşı), İznik 1331, İzmit 1337, Karesi'nin alınması, Çimpe 1353 (Rumeli'ye geçiş); ilk para, ilk medrese (İznik), ilk düzenli ordu (yaya-müsellem).
I. Murat: Edirne, Sırpsındığı 1364 (Haçlılarla ilk savaş), I. Kosova 1389; devşirme, yeniçeri, pençik; tımar sisteminin yaygınlaşması.
Yıldırım Bayezid: Niğbolu 1396, Anadolu Hisarı, Ankara 1402 (Timur'a yenilgi).
II. Murat: Edirne-Segedin 1444, Varna 1444, II. Kosova 1448.

§ Yükselme dönemi tablosu
Fatih: İstanbul 1453, Rumeli Hisarı, Trabzon 1461, Otlukbeli 1473 (Akkoyunlu), Kırım 1475; Kanunname-i Âl-i Osman.
II. Bayezid: Cem Sultan olayı (ilk kez bir şehzadenin yabancı devlete sığınması).
Yavuz: Çaldıran 1514 (Safevi), Turnadağ 1515 (Dulkadir), Mercidabık 1516 ve Ridaniye 1517 (Memlük) → halifelik, Kutsal Emanetler.
Kanuni: Belgrad 1521, Rodos 1522, Mohaç 1526, Viyana 1529, Irakeyn 1534, Preveze 1538, Amasya Antlaşması 1555 (Safevi), Zigetvar 1566; Fransa'ya ticari ayrıcalıklar.

§ Kurumlar sınıflandırması
Askerî: yeniçeri (kapıkulu, merkez) – tımarlı sipahi (eyalet) – donanma.
Toprak: tımar (miri arazi gelirinin asker yetiştirme karşılığı verilmesi).
Yönetim: Divan-ı Hümayun (vezir-i azam, kazasker, defterdar, nişancı); merkeziyetçilik.

§ Kural ve istisna
Kural: Osmanlı fethettiği yerlerde istimalet (hoşgörü) politikası uyguladı. Sonuç: yerel halkın direnci azaldı.
Kural: yenilgi = gerileme değildir. Ankara (1402) bir yenilgidir ama kuruluş dönemi içindedir.

§ Adım adım
Sorudaki olay "Rumeli / Balkan" ise Orhan–I. Murat–II. Murat; "doğu / Safevi / Memlük" ise Yavuz; "Avrupa ortası / deniz" ise Kanuni. Yıla göre önce yüzyılı belirle (14. yy kuruluş, 15. yy Fatih, 16. yy Yavuz-Kanuni).""",

"""§ Soru kalıpları
1) Padişah – olay eşleştirmesi.
2) Savaş sıralaması (Kosova I-II, Niğbolu, Ankara, Varna).
3) "İstanbul'un fethinin sonuçlarından biri değildir" → cevap çoğu zaman başka bir döneme aittir (ör. Kapitülasyonların verilmesi).
4) "Hangisi Osmanlı'nın merkeziyetçi yapısını güçlendirmiştir?" → Kanunname, devşirme.

§ Anahtar kelime → cevap
• "Rumeli'ye ilk geçiş" → Çimpe 1353, Orhan
• "Haçlılarla ilk savaş" → Sırpsındığı 1364
• "Fetret" → Ankara 1402 sonrası
• "Orta Çağ'ın sonu" → İstanbul'un fethi 1453
• "Halifelik" → Ridaniye 1517, Yavuz
• "Akdeniz Türk gölü" → Preveze 1538, Barbaros
• "Macaristan / tek saatte kazanılan meydan savaşı" → Mohaç 1526

§ Tuzaklar
• Maltepe (Pelekanon) ile Koyunhisar karıştırılır: Bizans'la ilk savaş Koyunhisar, Bizans'ın Anadolu'dan ümidini kestiği Maltepe.
• I. Kosova (1389) ile II. Kosova (1448) arasında 59 yıl vardır; Varna 1444 ikisinin arasındadır.
• Halifelik Fatih'te değil, Yavuz döneminde geçmiştir.
• Kapitülasyon ilk kez Kanuni döneminde Fransa'ya verilmiştir; "kalıcı/sürekli" hâle gelmesi 1740'tır.

§ Hafıza kodu
Yavuz'un doğu seferleri: "ÇaTuMeRi" → ÇAldıran, TUrnadağ, MErcidabık, RİdaniYe (1514-15-16-17, her yıl bir savaş).
Kanuni: "BeRoMoVi-PreZi" → Belgrad, Rodos, Mohaç, Viyana, Preveze, Zigetvar.

§ Mini test
1. Fetret Devri'ne yol açan savaş? — Cevap: Ankara Savaşı (1402).
2. Osmanlı'ya donanma kazandıran beylik? — Cevap: Karesioğulları.
3. Mısır'ın alınmasıyla Osmanlı'ya geçen dinî unvan? — Cevap: Halifelik.""",
)

HOCA['Duraklama-Gerileme'] = (
"""§ Büyük resim
Bir şirket düşün: yıllarca büyüyor, sonra yeni rakipler çıkıyor, çalışanlar maaş alamıyor, yöneticiler sık değişiyor. 17. yüzyıl Osmanlısı tam böyledir. Avrupa Coğrafi Keşifler ve Rönesans ile güçlenirken Osmanlı'da tımar bozulur, yeniçeri düzeni karışır, ticaret yolları önemini kaybeder. Duraklama "çöküş" değildir; büyüme durmuştur ama devlet hâlâ güçlüdür.

§ Hikâye
1606 Zitvatorok'ta Osmanlı padişahı, Avusturya arşidükünü ilk kez kendine eşit kabul eder. 1639 Kasr-ı Şirin ile İran sınırı büyük ölçüde bugünkü hâline yakın biçimde çizilir. Köprülüler döneminde kısa bir toparlanma yaşanır; Girit alınır (1669), Bucaş (1672) ile batıda en geniş sınıra ulaşılır. Sonra 1683'te II. Viyana Kuşatması başarısız olur. Avrupa, Kutsal İttifak'ta birleşir ve 16 yıl süren savaşlar 1699 Karlofça ile biter: Osmanlı ilk kez büyük çapta toprak kaybeder, Macaristan elden çıkar.
18. yüzyıl "kaybedileni geri alma" çabasıdır. 1711 Prut'ta Rus Çarı Petro kuşatılır ama tam sonuç alınamaz. 1718 Pasarofça'dan sonra barışçı Lale Devri başlar: Nevşehirli Damat İbrahim Paşa Avrupa'ya elçiler gönderir, İbrahim Müteferrika ilk Türk matbaasını kurar (1727). Ama lüks ve israfa tepki 1730'da Patrona Halil İsyanı'yla devri bitirir. 1774 Küçük Kaynarca ile Kırım bağımsız olur ve Rusya Ortodoksların hamiliğini kazanır. III. Selim'in Nizam-ı Cedit ordusu (1793) Kabakçı Mustafa İsyanı (1807) ile yıkılır. II. Mahmut 1826'da yeniçeri ocağını kaldırır (Vaka-i Hayriye) ve modernleşmenin yolunu açar.

§ Neden–sonuç zinciri
Coğrafi Keşifler → ticaret yolları değişir → gümrük gelirleri düşer → maaş ödenemez → isyanlar.
Tımarın bozulması → eyalet ordusu zayıflar → yeniçeri sayısı artar → hazine yükü artar.
Karlofça → Osmanlı Avrupa'yı ciddiye alır → ilk kez Batı'nın askerî ve teknik üstünlüğü kabul edilir → 18. yy ıslahatları Batı örnek alınarak yapılır.
Küçük Kaynarca → Rusya iç işlerine karışma hakkı kazanır → "Doğu Sorunu".

§ Tek cümlede
17. yy'da sebebi içeride arayıp eskiye dönmeye çalıştılar, 18. yy'da Batı'yı örnek aldılar, 19. yy başında köklü değişime (yeniçerinin kaldırılması) geçtiler.""",

"""§ Kavram haritası
1) Dönemler: Duraklama (17. yy), Gerileme (18. yy), Dağılma (19. yy). 2) Antlaşmalar. 3) Islahatlar ve ıslahatçılar.

§ 1) Duraklamanın nedenleri — iç / dış ayrımı
İç: merkezî otoritenin zayıflaması, şehzadelerin sancağa çıkarılmaması (kafes usulü), ekber ve erşed sistemi, tımarın bozulması, yeniçerilerin bozulması, iltizam, Celali isyanları.
Dış: Coğrafi Keşifler, Rönesans-Reform, Avrupa'da mutlak krallıkların güçlenmesi, Avusturya-Rusya rekabeti.

§ 2) Antlaşmalar tablosu
Zitvatorok 1606 – Avusturya – Osmanlı üstünlüğü sarsıldı, eşitlik kabul edildi.
Kasr-ı Şirin 1639 – İran – bugünkü sınıra yakın sınır.
Bucaş 1672 – Lehistan – batıda en geniş sınır.
Karlofça 1699 – Avusturya, Lehistan, Venedik – ilk büyük toprak kaybı.
İstanbul 1700 – Rusya – Azak Rusya'ya.
Prut 1711 – Rusya – Azak geri alındı.
Pasarofça 1718 – Avusturya, Venedik – kayıp; Lale Devri'ni başlattı.
Belgrad 1739 – Avusturya, Rusya – Fransa arabuluculuk; 1740'ta kapitülasyonlar sürekli hâle geldi.
Küçük Kaynarca 1774 – Rusya – Kırım bağımsız, Ortodoks hamiliği, ilk savaş tazminatı.
Yaş 1792 – Rusya – Kırım'ın Rusya'ya geçişi tanındı.

§ 3) Islahat dönemleri — anlayış değişimi
17. yy: sorunu kişilerde ve kurallardan sapmada görür; baskı ve sertlikle düzeltme (II. Osman, IV. Murat, Köprülüler). Raporlar: Koçi Bey Risalesi.
18. yy: Batı'nın askerî ve teknik üstünlüğünü kabul eder; Lale Devri (matbaa, elçilikler), I. Mahmut (Humbaracı Ahmet Paşa), III. Mustafa, I. Abdülhamit, III. Selim (Nizam-ı Cedit, ilk sürekli elçilikler).
19. yy başı: II. Mahmut — Sened-i İttifak 1808 (padişahın yetkisi ilk kez sınırlandı), Vaka-i Hayriye 1826, Asakir-i Mansure-i Muhammediye, Takvim-i Vekayi (1831, ilk resmî gazete), ilk nüfus sayımı (1831), Tercüme Odası, nazırlıklar.

§ Kural ve istisna
Kural: Duraklama döneminde büyük toprak kaybı yaşanmaz; sınırlar korunur, hatta Girit (1669) ve Podolya (Bucaş, 1672) kazanılır. İlk büyük kayıp dönemin sonunu belirleyen Karlofça'dadır (1699).
Kural: 18. yy'da kazanılan tek önemli başarı Prut (1711) ve Belgrad (1739) ile sınırlıdır.

§ Adım adım
Soru "ıslahatın amacı/niteliği" soruyorsa önce yüzyılı bul: 17. yy → geleneksel, baskıcı; 18. yy → Batılı, askerî; 19. yy → köklü, kurumsal.""",

"""§ Soru kalıpları
1) "Hangisi Osmanlı'nın Batı'nın üstünlüğünü kabul ettiğinin göstergesidir?" → 18. yy ıslahatları, Avrupa'ya elçi gönderilmesi.
2) Antlaşma – sonuç eşleştirmesi (Karlofça, Küçük Kaynarca, Zitvatorok).
3) "17. yüzyıl ıslahatlarının ortak özelliği" → kalıcı olmadı, kişilere bağlı kaldı, Batı örnek alınmadı.
4) Lale Devri yenilikleri (matbaa, kâğıt fabrikası, itfaiye teşkilatı).

§ Anahtar kelime → cevap
• "Eşitlik / Avusturya arşidükü" → Zitvatorok 1606
• "İlk büyük toprak kaybı / Macaristan" → Karlofça 1699
• "Kırım bağımsız / Ortodoks hamiliği / ilk savaş tazminatı" → Küçük Kaynarca 1774
• "Matbaa / İbrahim Müteferrika / Nevşehirli" → Lale Devri (1718–1730)
• "Patrona Halil" → Lale Devri'nin sonu
• "Nizam-ı Cedit / Kabakçı Mustafa" → III. Selim
• "Sened-i İttifak / Vaka-i Hayriye" → II. Mahmut

§ Tuzaklar
• Prut bir antlaşmadır ve Osmanlı açısından olumlu sonuçludur; "kayıp" listesine konarak çeldirici yapılır.
• Kapitülasyonların verilmesi (Kanuni) ile sürekli hâle gelmesi (1740) karıştırılır.
• Lale Devri'nin padişahı III. Ahmet, sadrazamı Nevşehirli Damat İbrahim Paşa'dır.
• Sened-i İttifak padişah ile ayanlar arasında imzalandı; halkla değil.

§ Hafıza kodu
"ZiKaKaKü": ZItvatorok (1606) → KAsr-ı Şirin (1639) → KArlofça (1699) → KÜçük Kaynarca (1774).
Islahat ruhu: "17 Sert, 18 Batı, 19 Köklü".

§ Mini test
1. Rusya'ya Osmanlı iç işlerine karışma imkânı veren antlaşma? — Cevap: Küçük Kaynarca (1774).
2. İlk resmî gazete hangi padişah döneminde çıktı? — Cevap: II. Mahmut (Takvim-i Vekayi, 1831).
3. Kapitülasyonları sürekli hâle getiren gelişme? — Cevap: Belgrad Antlaşması'ndaki Fransız arabuluculuğu (1740).""",
)

HOCA['Tanzimat-Meşrutiyet'] = (
"""§ Büyük resim
19. yüzyılda Osmanlı'nın önünde iki tehlike vardı: içeride Fransız İhtilali'nin yaydığı milliyetçilikle ayaklanan halklar, dışarıda "hasta adamı" paylaşmak isteyen büyük devletler. Tanzimat'tan Meşrutiyet'e kadar her belge aynı amaca hizmet eder: "Halkları devlete bağla, Avrupa'nın müdahalesini önle." Bu yüzden her belge bir dış krizle aynı zamana denk gelir.

§ Hikâye
1839'da Mısır Valisi Mehmet Ali Paşa isyanı sürerken Mustafa Reşit Paşa, Gülhane Parkı'nda Tanzimat Fermanı'nı okur. Padişah Abdülmecit ilk kez kendi yetkisini kanunla sınırlamayı kabul eder: herkesin can, mal, namus güvenliği; vergilerin gelire göre alınması; askerliğin düzenlenmesi; kimsenin yargılanmadan cezalandırılmaması.
1856'da Kırım Savaşı biterken, Paris Konferansı'nda Avrupalıların araya girmesini önlemek için Islahat Fermanı ilan edilir: gayrimüslimlere memurluk, okul açma, ibadet yeri onarma gibi geniş haklar verilir. Paris Antlaşması ile Osmanlı "Avrupa devleti" sayılır.
1876'da Balkan isyanları ve Tersane Konferansı sırasında, Genç Osmanlıların (Namık Kemal, Ziya Paşa) baskısı ve Mithat Paşa'nın öncülüğüyle ilk anayasa Kanun-i Esasi ilan edilir: I. Meşrutiyet. Meclis iki kanatlıdır: seçimle gelen Meclis-i Mebusan, padişahın atadığı Meclis-i Ayan. II. Abdülhamit 93 Harbi'ni (1877–78) gerekçe göstererek meclisi 1878'de kapatır.
1908'de İttihat ve Terakki'nin baskısıyla II. Meşrutiyet ilan edilir. 1909'daki 31 Mart Vakası'nı Selanik'ten gelen Hareket Ordusu bastırır; II. Abdülhamit tahttan indirilir ve Kanun-i Esasi değiştirilerek padişahın yetkileri azaltılır, meclisin yetkileri artırılır.

§ Neden–sonuç zinciri
Milliyetçilik → azınlık isyanları → Osmanlıcılık fikri (herkes eşit Osmanlı vatandaşı) → Tanzimat ve Islahat.
Avrupa müdahalesi korkusu → belgeler hep konferans/kriz zamanında ilan edilir.
Islahat'taki ayrıcalıklar → Müslüman halkta tepki ve azınlıklarda ayrılıkçılığın sürmesi → Osmanlıcılık hedefine ulaşamaz.
Meşrutiyet → halk ilk kez yönetime katılır → ama padişah meclisi kapatabildiği için gerçek bir anayasal düzen kurulamaz.

§ Tek cümlede
Tanzimat "hukuk", Islahat "eşitlik", I. Meşrutiyet "anayasa ve meclis", II. Meşrutiyet "meclisin padişaha karşı güçlenmesi" demektir.""",

"""§ Kavram haritası
Dört belge, dört soru: Kim? Ne zaman? Hangi kriz? Ne getirdi?

§ Karşılaştırma tablosu
Belge | Yıl / padişah | Kriz ortamı | Temel yenilik
Sened-i İttifak | 1808 / II. Mahmut | Ayanların gücü | Padişah yetkisi ilk kez sınırlandı (ayanlara karşı)
Tanzimat Fermanı | 1839 / Abdülmecit | Mehmet Ali isyanı | Kanun üstünlüğü; can-mal güvenliği; vergide adalet
Islahat Fermanı | 1856 / Abdülmecit | Kırım Savaşı, Paris Konf. | Gayrimüslimlere geniş haklar
Kanun-i Esasi (I. Meşrutiyet) | 1876 / II. Abdülhamit | Balkan isyanları, Tersane Konf. | İlk anayasa, ilk meclis
II. Meşrutiyet | 1908 / II. Abdülhamit | İttihat ve Terakki baskısı | Meclis yeniden açıldı; 1909 değişikliği ile meclis güçlendi

§ Kanun-i Esasi'nin yapısı
• Meclis-i Umumi = Meclis-i Mebusan (seçimle, 4 yıl) + Meclis-i Ayan (padişah atar, ömür boyu).
• Padişah: meclisi açma-kapatma, sürgün yetkisi (md. 113), kanunları onaylama yetkisi.
• Sonuç: egemenlik hâlâ padişahtadır; millet yönetime "katılır" ama egemen değildir.

§ Fikir akımları sınıflandırması
Osmanlıcılık (Tanzimat'tan itibaren, tüm halkları birleştirme) → Balkan Savaşları ile iflas.
İslamcılık (II. Abdülhamit, Müslümanları birleştirme) → I. Dünya Savaşı'nda Arap isyanlarıyla iflas.
Türkçülük (Ziya Gökalp; II. Meşrutiyet'ten sonra güçlendi) → Cumhuriyet'in milliyetçilik anlayışına zemin.
Batıcılık (Batı'nın bilim ve kurumlarını alma) → Cumhuriyet inkılaplarında etkili.

§ II. Abdülhamit dönemi kutusu
Düyun-u Umumiye (1881, Muharrem Kararnamesi: Avrupalı alacaklıların Osmanlı gelirlerini toplaması); Hicaz Demiryolu; Darülaceze; Tunus (1881, Fransa) ve Mısır (1882, İngiltere) kayıpları; denge politikası.

§ Adım adım
"Gayrimüslim" → Islahat; "kanun önünde eşitlik ilk kez" → Tanzimat; "seçim / meclis / anayasa ilk kez" → I. Meşrutiyet; "Hareket Ordusu / 31 Mart" → II. Meşrutiyet dönemi (1909).""",

"""§ Soru kalıpları
1) "Tanzimat Fermanı ile ilk kez ... " cümlesini tamamlama.
2) Belgeleri kronolojik sıralama.
3) "Kanun-i Esasi'ye göre aşağıdakilerden hangisi söylenemez?" → "Egemenlik millete aittir" çeldiricisi (yanlış; o 1921'de gelir).
4) Fikir akımı – dönem eşleştirmesi.

§ Anahtar kelime → cevap
• "Mustafa Reşit Paşa / Gülhane / can-mal güvenliği" → Tanzimat 1839
• "Kırım Savaşı / gayrimüslim / Paris" → Islahat 1856
• "Mithat Paşa / Genç Osmanlılar / iki meclis" → Kanun-i Esasi 1876
• "93 Harbi / meclisin kapatılması" → 1878
• "Hareket Ordusu / 31 Mart" → 1909
• "Muharrem Kararnamesi" → Düyun-u Umumiye 1881

§ Tuzaklar
• Sened-i İttifak bir anayasa değildir; "ilk anayasal gelişme / padişah yetkisinin ilk kez sınırlanması" olarak sorulur.
• Kanun-i Esasi'de egemenlik millete geçmez; meclis vardır ama padişah üstündür.
• Islahat Fermanı yalnızca gayrimüslimler için değil, genel düzenlemeler de içerir; ama ayırt edici yönü gayrimüslim haklarıdır.
• I. Meşrutiyet'i ilan eden II. Abdülhamit'tir; II. Meşrutiyet'i de o ilan etmiştir.

§ Hafıza kodu
"8-39-56-76-08": Sened 1808 → Tanzimat 1839 → Islahat 1856 → Meşrutiyet I 1876 → Meşrutiyet II 1908.
"T-H-İ": Tanzimat = Hukuk, Islahat = İmtiyaz (gayrimüslim), Kanun-i Esasi = Meclis.

§ Mini test
1. Osmanlı'nın "Avrupa devleti" sayılmasını sağlayan antlaşma? — Cevap: Paris Antlaşması (1856).
2. Kanun-i Esasi'de padişahın atadığı meclis? — Cevap: Meclis-i Ayan.
3. Balkan Savaşları hangi fikir akımının etkisini yitirmesine yol açtı? — Cevap: Osmanlıcılık.""",
)

HOCA['Son Dönem Savaşları'] = (
"""§ Büyük resim
1911'den 1918'e kadar Osmanlı neredeyse hiç durmadan savaştı: Trablusgarp, iki Balkan Savaşı, ardından dünya savaşı. Bu yedi yıl, imparatorluğun Avrupa ve Afrika'dan çekilip Anadolu'ya sıkıştığı dönemdir. Aynı zamanda Mustafa Kemal'in sahneye çıktığı dönemdir.

§ Hikâye
1911'de İtalya, Osmanlı'nın Kuzey Afrika'daki son toprağı Trablusgarp'a saldırır. Kara yoluyla asker gönderilemez (Mısır İngiliz denetiminde), bu yüzden gönüllü subaylar gider; Mustafa Kemal Tobruk ve Derne'de savaşır. Balkanlarda savaş tehlikesi doğunca Osmanlı 1912 Uşi Antlaşması ile Trablusgarp ve Bingazi'yi bırakır; Onikiada geçici olarak İtalya'ya kalır.
Aynı yıl Sırbistan, Bulgaristan, Yunanistan ve Karadağ birleşip saldırır (I. Balkan Savaşı). Osmanlı ağır yenilir; Londra Antlaşması (1913) ile Midye-Enez hattının batısı kaybedilir. Ganimeti paylaşamayan Balkan devletleri Bulgaristan'a karşı savaşa girince (II. Balkan Savaşı), Osmanlı fırsatı değerlendirip Edirne'yi geri alır (İstanbul Antlaşması, 1913).
1914'te Almanya'dan gelen Goben ve Breslav gemileri (Yavuz ve Midilli adlarını alır) Karadeniz'de Rus limanlarını bombalar ve Osmanlı İttifak Devletleri yanında savaşa girer. Kafkasya'da Sarıkamış'ta (1914–15) on binlerce asker soğukta şehit olur. Çanakkale'de 18 Mart 1915'te İtilaf donanması geçemez; kara savaşlarında Mustafa Kemal Arıburnu ve Anafartalar'da öne çıkar. Rusya'ya yardım ulaştırılamaz, bu da Bolşevik İhtilali'ni hızlandırır. 1918'de Bulgaristan'ın teslimiyetiyle Almanya ile bağlantı kesilir ve 30 Ekim 1918'de Mondros Ateşkesi imzalanır.

§ Neden–sonuç zinciri
Trablusgarp'a kara yolu kapalı → savaş kaybedilir → Balkan devletleri Osmanlı'nın zayıflığını görür → Balkan Savaşları.
Balkan Savaşları → Osmanlıcılık iflas eder, Türkçülük güçlenir; Rumeli'den Anadolu'ya göç.
Çanakkale zaferi → Rusya'ya yardım engellenir → savaş uzar, Rusya'da devrim olur → Brest-Litovsk ile Kars, Ardahan, Batum geri alınır.
Mondros md. 7 ve 24 → işgallerin hukuki gerekçesi → Kuva-yi Milliye ve Millî Mücadele.

§ Tek cümlede
Trablusgarp son Afrika toprağını, Balkan Savaşları Rumeli'yi götürdü; I. Dünya Savaşı imparatorluğu bitirdi ama Çanakkale Millî Mücadele'nin komutanını doğurdu.""",

"""§ Kavram haritası
Her savaş için: Taraflar → Antlaşma → Toprak sonucu → Fikir/siyaset sonucu.

§ Savaş tablosu
Trablusgarp 1911–12 | İtalya | Uşi 1912 | Trablusgarp-Bingazi İtalya'ya; Onikiada geçici İtalya'ya | Kuzey Afrika'da son toprak kaybı
I. Balkan 1912–13 | Sırbistan, Bulgaristan, Yunanistan, Karadağ | Londra 1913 | Midye-Enez batısı kaybedildi; Arnavutluk bağımsız | Osmanlıcılık iflas
II. Balkan 1913 | Bulgaristan ↔ diğerleri; Osmanlı Edirne'yi aldı | Bükreş (Balkan devletleri arası), İstanbul (Osmanlı-Bulgaristan), Atina (Osmanlı-Yunanistan) | Edirne ve Kırklareli geri alındı | Türkçülük güçlendi
I. Dünya 1914–18 | İttifak: Almanya, Avusturya-Macaristan, Osmanlı, Bulgaristan / İtilaf: İngiltere, Fransa, Rusya, (sonra İtalya, ABD) | Mondros 1918 (ateşkes), Sevr 1920 | Osmanlı fiilen dağıldı | Millî Mücadele

§ I. Dünya Savaşı cepheleri sınıflandırması
Taarruz (saldırı) cepheleri: Kafkasya (Sarıkamış), Kanal (Süveyş'e iki sefer).
Savunma cepheleri: Çanakkale, Irak (Kut'ül-Amare zaferi 1916), Suriye-Filistin, Hicaz-Yemen (Fahrettin Paşa).
Yardım cepheleri: Galiçya, Makedonya, Romanya.
Mustafa Kemal'in bulunduğu cepheler: Çanakkale, Kafkasya (Muş ve Bitlis'i geri aldı), Suriye-Filistin (Yıldırım Orduları).

§ Mondros'un kritik maddeleri
md. 7: İtilaf devletleri güvenliklerini tehdit eden bir durumda herhangi bir stratejik yeri işgal edebilir.
md. 24: Vilayat-ı Sitte'de (altı doğu ili) karışıklık çıkarsa buralar işgal edilebilir.
Diğer: ordu terhis edilecek, Boğazlar açılacak, haberleşme denetime girecek.

§ Kural ve istisna
Kural: I. Dünya Savaşı Osmanlı için yenilgidir. İstisna: Çanakkale ve Kut'ül-Amare zaferleri.
Kural: Balkan Savaşları kayıptır. İstisna: II. Balkan'da Edirne'nin geri alınması.

§ Adım adım
Antlaşma adı → karşı taraf → sonuç. "Ateşkes" kelimesi geçiyorsa Mondros (Mudanya 1922 de ateşkestir, Millî Mücadele'ye aittir).""",

"""§ Soru kalıpları
1) "Osmanlı'nın I. Dünya Savaşı'nda saldırı amacıyla açtığı cephe hangisidir?" → Kafkasya / Kanal.
2) "Çanakkale Savaşı'nın sonuçlarından biri değildir" → seçeneklerde başka cephenin sonucu çeldiricidir.
3) "Mondros'un hangi maddesi işgallere zemin hazırladı?" → 7 ve 24.
4) Balkan Savaşlarının fikir hayatına etkisi.

§ Anahtar kelime → cevap
• "Kuzey Afrika'da son toprak" → Trablusgarp, Uşi
• "Midye-Enez" → Londra Antlaşması (1913)
• "Edirne geri alındı" → II. Balkan, İstanbul Antlaşması
• "Goben-Breslav / Yavuz-Midilli" → Osmanlı'nın savaşa girişi
• "Sarıkamış" → Kafkasya
• "Rusya'ya yardım engellendi / Bolşevik İhtilali" → Çanakkale
• "Vilayat-ı Sitte" → Mondros md. 24

§ Tuzaklar
• Mondros barış değil ateşkestir; Sevr barış antlaşmasıdır ve yürürlüğe girmemiştir.
• Londra Antlaşması (1913) ile Londra Konferansı (1921) karıştırılır.
• Bükreş Antlaşması'nda Osmanlı taraf değildir; Balkan devletleri arasındadır.
• Kut'ül-Amare zaferi Irak cephesindedir, Çanakkale'de değil.

§ Hafıza kodu
Taarruz cepheleri: "KaKa" → KAfkasya, KAnal.
Mondros: "7 her yer, 24 altı il".
Balkan: "Lon-Bük-İst-At" → Londra (I), Bükreş, İstanbul, Atina (II).

§ Mini test
1. Kara yoluyla asker gönderilememesinin nedeni hangi savaşta etkili oldu? — Cevap: Trablusgarp (Mısır İngiliz denetimindeydi).
2. Brest-Litovsk ile geri alınan yerler? — Cevap: Kars, Ardahan, Batum.
3. Çanakkale'de 18 Mart 1915'te ne oldu? — Cevap: İtilaf donanması Boğaz'ı geçemedi; deniz savaşı kazanıldı.""",
)

HOCA['Milli Mücadele'] = (
"""§ Büyük resim
Mondros'tan sonra ordu terhis edilmiş, İstanbul işgal altında, padişah İtilaf'la uzlaşmaya çalışıyor. Mustafa Kemal'in sorusu şuydu: "İstanbul'daki hükümet milleti kurtaramıyorsa, millet kendini nasıl kurtarır?" Bütün Millî Mücadele bu sorunun adım adım cevabıdır: önce halkı uyandır (genelgeler), sonra temsilci topla (kongreler), sonra meclis kur (TBMM), sonra ordu kur ve savaş, en sonunda diplomasiyle tanıt.

§ Hikâye
19 Mayıs 1919'da Samsun'a çıkar. Havza Genelgesi ile halkı işgalleri protesto mitinglerine çağırır. 22 Haziran 1919 Amasya Genelgesi bir bildiridir: "Vatanın bütünlüğü, milletin bağımsızlığı tehlikededir. Milletin bağımsızlığını yine milletin azim ve kararı kurtaracaktır." Bu cümle millî egemenliğin ilk ilanıdır. Mustafa Kemal ardından askerlikten istifa eder ve sivil olarak devam eder.
Erzurum Kongresi (23 Temmuz – 7 Ağustos 1919) bölgesel toplanır ama ulusal kararlar alır: manda ve himaye ilk kez reddedilir, Temsil Heyeti seçilir. Sivas Kongresi (4–11 Eylül 1919) ulusaldır: bütün cemiyetler "Anadolu ve Rumeli Müdafaa-i Hukuk Cemiyeti" adı altında birleşir, manda kesin reddedilir. Amasya Görüşmeleri'nde İstanbul hükümeti Temsil Heyeti'ni fiilen tanır. Son Osmanlı Mebusan Meclisi Misak-ı Millî'yi kabul eder (28 Ocak 1920); İtilaf buna 16 Mart 1920'de İstanbul'u resmen işgal ederek cevap verir. Mustafa Kemal 23 Nisan 1920'de TBMM'yi açar.
Doğu'da Kazım Karabekir Ermenilere karşı kazanır: Gümrü Antlaşması (Aralık 1920), TBMM'nin ilk askerî ve siyasi başarısıdır. Güneyde Maraş, Antep, Urfa halkı Fransızlara direnir. Batıda düzenli ordu I. İnönü'de (Ocak 1921) ilk zaferini kazanır; ardından II. İnönü gelir. Kütahya-Eskişehir yenilgisi üzerine Mustafa Kemal Başkomutan olur, Tekâlif-i Milliye ile ordu donatılır ve Sakarya'da (Ağustos–Eylül 1921) Yunan ilerleyişi durdurulur; Mustafa Kemal'e Mareşal ve Gazi unvanları verilir. 26 Ağustos 1922 Büyük Taarruz, 30 Ağustos Başkomutan Meydan Muharebesi, 9 Eylül İzmir'in kurtuluşu ve 11 Ekim 1922 Mudanya Ateşkesi ile savaş biter.

§ Neden–sonuç zinciri
Mondros + işgaller → Kuva-yi Milliye → düzenli orduya geçiş ihtiyacı → I. İnönü.
Her askerî zafer → bir diplomatik kazanç: I. İnönü → Londra Konferansı ve Moskova Antlaşması; Sakarya → Kars ve Ankara Antlaşması (Fransa); Büyük Taarruz → Mudanya, Lozan.
İstanbul'un işgali → Mebusan dağılır → TBMM'nin kurulmasına meşru zemin.

§ Tek cümlede
Genelgeler uyandırdı, kongreler örgütledi, TBMM yönetti, ordu kazandı, diplomasi tescil etti.""",

"""§ Kavram haritası
1) Hazırlık dönemi belgeleri, 2) TBMM ve iç isyanlar, 3) Cepheler, 4) Antlaşmalar.

§ 1) Hazırlık dönemi — belge türüne göre
Genelge: Havza (protesto mitingleri), Amasya (millî egemenlik, kongre çağrısı; ihtilal beyannamesi niteliği).
Kongre: Erzurum (bölgesel toplanma, ulusal karar; manda ilk kez reddedildi; Temsil Heyeti), Sivas (ulusal; cemiyetlerin birleşmesi; İrade-i Milliye gazetesi; manda kesin reddi), Balıkesir ve Alaşehir kongreleri (Batı'da Kuva-yi Milliye'yi örgütleme).
Görüşme: Amasya Görüşmeleri (İstanbul hükümetinin Temsil Heyeti'ni tanıması).
Meclis kararı: Misak-ı Millî (son Osmanlı Mebusan Meclisi; millî sınırlar, kapitülasyonların reddi).

§ 2) TBMM
Açılış 23 Nisan 1920; güçler birliği ilkesi (yasama-yürütme-yargı mecliste); Hıyanet-i Vataniye Kanunu; İstiklal Mahkemeleri; Teşkilat-ı Esasiye (20 Ocak 1921; egemenlik kayıtsız şartsız milletindir); İstiklal Marşı (12 Mart 1921).
İç isyan türleri: İstanbul hükümeti kışkırtması (Anzavur), Kuva-yi Milliye yanlısı ama düzenli orduya karşı (Çerkez Ethem), azınlık (Pontus), ayrılıkçı (Koçgiri).

§ 3) Cepheler
Doğu: Kazım Karabekir – Ermeniler – Gümrü (2/3 Aralık 1920).
Güney: Kuva-yi Milliye – Fransız ve Ermeniler – Ankara Antlaşması (20 Ekim 1921).
Batı: I. İnönü (6–10 Ocak 1921) → II. İnönü (23 Mart–1 Nisan 1921) → Kütahya-Eskişehir (Temmuz 1921) → Sakarya (23 Ağustos–13 Eylül 1921) → Büyük Taarruz (26 Ağustos 1922) → Mudanya (11 Ekim 1922).

§ 4) Zafer → diplomasi eşlemesi
I. İnönü → Teşkilat-ı Esasiye, Londra Konferansı (TBMM ilk kez uluslararası alanda), Afganistan ve Moskova (16 Mart 1921) antlaşmaları.
Sakarya → Kars Antlaşması (13 Ekim 1921, Kafkas cumhuriyetleri), Ankara Antlaşması (Fransa; İtilaf bloğunun dağılması).
Büyük Taarruz → Mudanya (Doğu Trakya savaşmadan kurtuldu; İstanbul ve Boğazlar TBMM'ye) → Lozan.

§ Kural ve istisna
Kural: Kongrelerde alınan kararlar ulusaldır. İstisna değil, ince ayrım: Erzurum'un toplanışı bölgesel, kararları ulusaldır.
Kural: Sakarya'ya kadar ordu savunmadadır; Büyük Taarruz ilk büyük saldırıdır.

§ Adım adım
Bir gelişmenin yerini bul: "millî egemenlik ilk kez" → Amasya Genelgesi; "manda ilk red" → Erzurum; "birleşme" → Sivas; "sınır" → Misak-ı Millî; "egemenlik kayıtsız şartsız" → Teşkilat-ı Esasiye.""",

"""§ Soru kalıpları
1) "Hangisinde ilk kez ..." (millî egemenlik, manda reddi, TBMM'nin tanınması).
2) Olay sıralaması: Amasya Genelgesi, Erzurum, Sivas, Misak-ı Millî, TBMM.
3) Zafer – antlaşma eşleştirmesi.
4) "Amasya Genelgesi'nin hangi maddesi millî egemenliği vurgular?" → milletin istiklalini yine milletin azim ve kararı kurtaracaktır.

§ Anahtar kelime → cevap
• "Mitingler" → Havza Genelgesi
• "Milletin azim ve kararı" → Amasya Genelgesi
• "Manda ve himaye kabul olunamaz (ilk)" → Erzurum Kongresi
• "Cemiyetlerin birleştirilmesi / İrade-i Milliye" → Sivas Kongresi
• "Temsil Heyeti'nin İstanbul tarafından tanınması" → Amasya Görüşmeleri
• "Millî sınırlar" → Misak-ı Millî
• "TBMM'nin ilk askerî ve siyasi zaferi" → Gümrü
• "Düzenli ordunun ilk zaferi" → I. İnönü
• "Mareşal ve Gazi" → Sakarya
• "Savaşmadan Doğu Trakya" → Mudanya

§ Tuzaklar
• Gümrü TBMM'nin ilk siyasi başarısıdır; "ilk uluslararası antlaşma" sorulursa yine Gümrü; Londra Konferansı ise "ilk kez uluslararası alanda bulunma"dır (toplantı, antlaşma değil).
• Misak-ı Millî TBMM'de değil, son Osmanlı Mebusan Meclisi'nde kabul edildi.
• Sakarya'dan sonra Mustafa Kemal'e verilen unvanlar Mareşal ve Gazi'dir; Başkomutanlık Sakarya'dan önce (Kütahya-Eskişehir sonrası) verildi.
• Kars Antlaşması Sovyet Rusya ile değil, Kafkas cumhuriyetleriyle (Sovyet aracılığıyla) imzalandı; Moskova Antlaşması Sovyet Rusya ile.

§ Hafıza kodu
"HAES-MİT": Havza → Amasya → Erzurum → Sivas → Misak-ı Millî → İstanbul'un işgali → TBMM.
Batı cephesi: "İnİn-KüSa-BüMu" → I. İnönü, II. İnönü, Kütahya, Sakarya, Büyük Taarruz, Mudanya.

§ Mini test
1. Kongre kararlarıyla manda ilk kez nerede reddedildi? — Cevap: Erzurum Kongresi.
2. Fransa ile imzalanan ve İtilaf bloğunda çatlak oluşturan antlaşma? — Cevap: Ankara Antlaşması (20 Ekim 1921).
3. Tekâlif-i Milliye hangi savaşa hazırlık için çıkarıldı? — Cevap: Sakarya Meydan Muharebesi.""",
)

HOCA['Lozan'] = (
"""§ Büyük resim
Lozan, savaş meydanında kazanılanın masada tescil edilmesidir. Ama sıradan bir barış değildir: Sevr'in yırtılıp atılması, kapitülasyonların bitmesi ve yeni Türk devletinin dünyaya kabulüdür. Türk heyetinin başkanı İsmet Paşa'dır; masada Mustafa Kemal'in talimatı tektir: "Tam bağımsızlıktan taviz yok."

§ Hikâye
Konferans 20 Kasım 1922'de toplanır. İtilaf devletleri hem Ankara'yı hem İstanbul hükümetini çağırınca TBMM 1 Kasım 1922'de saltanatı kaldırır; masada tek Türk temsilci kalır. İngiltere'nin Lord Curzon'u kapitülasyonlarda ve Musul'da sert davranır. İsmet Paşa geri adım atmayınca görüşmeler Şubat 1923'te kesilir. Türk tarafı İzmir İktisat Kongresi ile ekonomik bağımsızlık kararlılığını gösterir. Görüşmeler yeniden başlar ve 24 Temmuz 1923'te antlaşma imzalanır.
Sonuç: kapitülasyonlar tamamen kaldırılır. Osmanlı borçları, Osmanlı'dan ayrılan devletler arasında paylaştırılır; Türkiye'ye düşen pay taksitlendirilir. Azınlık olarak yalnızca gayrimüslimler kabul edilir. Türk-Yunan nüfus mübadelesi yapılır (İstanbul Rumları ve Batı Trakya Türkleri hariç). Boğazlar, başkanı Türk olan uluslararası bir komisyona bırakılır ve kıyıları silahsızlandırılır. Yunanistan savaş tazminatı yerine Karaağaç'ı verir. Musul ise çözülemez: Türkiye ile İngiltere arasında görüşmelere bırakılır.

§ Neden–sonuç zinciri
Kapitülasyonların kaldırılması → ekonomik ve hukuki bağımsızlık → tam bağımsızlık ilkesinin gerçekleşmesi.
Musul'un ertelenmesi → 1926 Ankara Antlaşması ile Musul Irak'a (İngiliz mandası) bırakılır.
Boğazlar komisyonu ve silahsızlandırma → egemenlik eksikliği → 1936 Montrö ile Boğazlar tam Türk denetimine geçer.
Lozan'da kalan bir başka konu Hatay değildir; Hatay 1921 Ankara Antlaşması'yla Fransız mandası Suriye'nin içinde özel statüde kalmış, 1939'da Türkiye'ye katılmıştır.

§ Misak-ı Millî ile karşılaştır
Hedefler büyük ölçüde gerçekleşti; gerçekleşemeyenler: Musul, Batı Trakya, Hatay (o tarihte), Ege adalarının bir kısmı (Onikiada İtalya'ya bırakıldı; Gökçeada ve Bozcaada Türkiye'de kaldı).

§ Tek cümlede
Lozan, Sevr'in yerine geçen, tam bağımsızlığı tescil eden ve yalnızca Musul'u ertelenmiş bırakan kuruluş belgesidir.""",

"""§ Kavram haritası
Lozan'ı altı başlıkta öğren: 1) Sınırlar, 2) Kapitülasyonlar, 3) Borçlar, 4) Azınlıklar ve mübadele, 5) Boğazlar, 6) Diğer (tazminat, yabancı okullar, Patrikhane).

§ Başlık → karar
1) Sınırlar: Suriye sınırı 1921 Ankara Antlaşması'ndaki gibi; Irak sınırı (Musul) ertelendi; Trakya'da Meriç sınırı ve Karaağaç; Gökçeada ve Bozcaada Türkiye'de; Onikiada İtalya'da; diğer Ege adaları Yunanistan'da.
2) Kapitülasyonlar: tamamen kaldırıldı.
3) Borçlar: Osmanlı borçları ayrılan devletler arasında paylaştırıldı; Türkiye payını taksitle ödeyecekti.
4) Azınlıklar: yalnızca gayrimüslimler; Türk vatandaşı sayılırlar. Mübadele: İstanbul Rumları ve Batı Trakya Türkleri hariç.
5) Boğazlar: başkanı Türk olan uluslararası komisyon; iki yakada askerden arındırılmış bölge.
6) Diğer: Yunanistan tazminat yerine Karaağaç'ı verdi; yabancı okullar Türk kanunlarına tabi; Patrikhane yalnızca dinî görevle İstanbul'da kaldı.

§ Sevr – Lozan karşılaştırması
Sevr (10 Ağustos 1920): Osmanlı hükümeti imzaladı; yürürlüğe girmedi; kapitülasyonlar genişletildi; Doğu'da Ermeni devleti ve özerk bölge; Boğazlar uluslararası.
Lozan (24 Temmuz 1923): TBMM imzaladı; yürürlüğe girdi; kapitülasyonlar kaldırıldı; Doğu Anadolu Türkiye'de; Boğazlar Türk başkanlı komisyon.

§ Çözülemeyen ve sonradan çözülen konular
Musul → 1926 Ankara Antlaşması (İngiltere, Irak) → Irak'a bırakıldı.
Boğazların tam egemenliği → 1936 Montrö.
Hatay → 1939 Türkiye'ye katıldı (Lozan'ın çözümsüz konusu değil, Ankara Antlaşması kaynaklı).
Yabancı şirketler ve nüfus mübadelesinin uygulanması → ikili görüşmelerle çözüldü.

§ Adım adım
Lozan sorusunda seçenekleri "kesin karar" ve "ertelenen" diye ikiye ayır; ertelenen olarak yalnızca Musul'u işaretle. Boğazlar karara bağlanmıştır (komisyon), ertelenmemiştir.""",

"""§ Soru kalıpları
1) "Lozan'da çözülemeyen sorun hangisidir?" → Musul.
2) "Lozan'da aşağıdakilerden hangisi tam olarak gerçekleşmiştir?" → kapitülasyonların kaldırılması.
3) Sevr – Lozan karşılaştırması.
4) "Lozan'da egemenliği kısıtlayıcı hüküm hangisidir?" → Boğazlar komisyonu ve silahsızlandırma.

§ Anahtar kelime → cevap
• "Ertelenen / ikili görüşmeye bırakılan" → Musul
• "Montrö'ye zemin" → Boğazlar maddesi
• "Tazminat yerine" → Karaağaç
• "Azınlık tanımı" → yalnızca gayrimüslimler
• "Mübadele dışı" → İstanbul Rumları, Batı Trakya Türkleri
• "Kapitülasyon" → tamamen kaldırıldı

§ Tuzaklar
• "Boğazlar sorunu ertelendi" yanlıştır: karar verildi, sadece sonradan Türkiye lehine değiştirildi.
• "Hatay Lozan'da çözülemedi" ifadesi çeldiricidir; Hatay'ın durumu Ankara Antlaşması'na (1921) dayanır.
• Borçlar silinmedi, paylaştırıldı ve taksitlendirildi.
• Lozan'da Türk heyetinin başkanı İsmet Paşa'dır; Rıza Nur ve Hasan Saka (Hasan Bey) yardımcı delegedir. Mudanya'yı da İsmet Paşa yürütmüştür.

§ Hafıza kodu
"Lozan'da tek Musul kaldı" — tek ertelenen.
"KaBoAzBoSı": KApitülasyon (kalktı), BOrç (paylaştı), AZınlık (gayrimüslim), BOğaz (komisyon), SInır (Musul hariç).

§ Mini test
1. Lozan'da Türkiye'nin egemenliğini sınırlayan iki hüküm? — Cevap: Boğazlarda uluslararası komisyon ve kıyıların silahsızlandırılması.
2. Lozan Konferansı toplanmadan saltanatın kaldırılmasının nedeni? — Cevap: İtilaf'ın İstanbul hükümetini de davet etmesi; ikili temsili önlemek.
3. Musul sorunu nasıl sonuçlandı? — Cevap: 1926 Ankara Antlaşması ile Irak'a bırakıldı.""",
)

HOCA['Devrimler ve İlkeler'] = (
"""§ Büyük resim
Savaş bitti; şimdi asıl soru "nasıl bir devlet?"ti. Atatürk devrimlerinin mantığı bir binayı temelden yenilemeye benzer: önce temel (siyasi rejim: saltanat, cumhuriyet, halifelik), sonra taşıyıcı kolonlar (hukuk ve eğitim), sonra iç düzen (toplumsal hayat), sonra da tesisat (ekonomi). İlkeler ise bu binanın mimari projesidir.

§ Hikâye
1 Kasım 1922'de saltanat kaldırılır; 29 Ekim 1923'te Cumhuriyet ilan edilir, böylece "devlet başkanı kim?" sorusu çözülür. 3 Mart 1924'te halifelik kaldırılır; aynı gün Tevhid-i Tedrisat Kanunu ile bütün okullar Maarif Vekâletine bağlanır, Şeriye ve Evkaf Vekâleti ile Erkân-ı Harbiye Vekâleti kaldırılır. 1924 Anayasası kabul edilir.
1925'te Şapka Kanunu çıkar, tekke-zaviye-türbeler kapatılır, uluslararası saat ve takvim kabul edilir. 1926'da Türk Medeni Kanunu (İsviçre'den) ile kadın-erkek eşitliği hukuka girer, tek eşlilik ve resmî nikâh gelir. 1928'de anayasadan "devletin dini İslam'dır" ibaresi çıkarılır ve 1 Kasım 1928'de yeni Türk harfleri kabul edilir; Millet Mektepleri ile okuma-yazma seferberliği başlar. 1931'de Türk Tarih, 1932'de Türk Dil kurumları kurulur. 1934'te Soyadı Kanunu çıkar ve Mustafa Kemal'e "Atatürk" soyadı verilir; aynı yıl kadınlar milletvekili seçme ve seçilme hakkı kazanır.
Ekonomide 1923 İzmir İktisat Kongresi "Misak-ı İktisadi"yi belirler, 1925'te aşar kaldırılır, 1926'da Kabotaj Kanunu ile kıyı taşımacılığı Türk gemilerine verilir, 1927 Teşvik-i Sanayi Kanunu çıkar. 1929 dünya ekonomik bunalımı sonrası devletçilik benimsenir ve 1934'te I. Beş Yıllık Sanayi Planı uygulanır.

§ Neden–sonuç zinciri
Egemenliğin millete geçmesi (cumhuriyetçilik) → saltanat ve halifeliğin kaldırılması.
Eğitim birliği (Tevhid-i Tedrisat) → laik ve millî eğitim → harf devrimi → okuryazarlığın artması (halkçılık).
Medeni Kanun → kadın hakları → siyasal haklar (1930 belediye, 1933 muhtarlık, 1934 milletvekilliği).
Özel girişimin sermayesizliği + 1929 bunalımı → devletçilik.

§ Tek cümlede
Devrimler binayı yeniledi, ilkeler (Cumhuriyetçilik, Milliyetçilik, Halkçılık, Devletçilik, Laiklik, İnkılapçılık) bu yenilenmenin pusulası oldu ve 1937'de anayasaya girdi.""",

"""§ Kavram haritası
Devrimler beş alanda sınıflandırılır; her devrim en az bir ilkeyle ilişkilidir.

§ 1) Siyasi alan
Saltanatın kaldırılması (1 Kasım 1922) – Cumhuriyetin ilanı (29 Ekim 1923) – Halifeliğin kaldırılması (3 Mart 1924) – 1924 Anayasası – Çok partili hayat denemeleri: Terakkiperver Cumhuriyet Fırkası (1924), Serbest Cumhuriyet Fırkası (1930).

§ 2) Hukuk alanı
Türk Medeni Kanunu (1926, İsviçre), Borçlar Kanunu (1926, İsviçre), Ceza Kanunu (1926, İtalya), Ticaret Kanunu (1926, Almanya). Amaç: hukuk birliği ve laik hukuk.

§ 3) Eğitim ve kültür alanı
Tevhid-i Tedrisat (1924), Harf İnkılabı (1928), Millet Mektepleri (1929), Türk Tarih Kurumu (1931), Türk Dil Kurumu (1932), Halkevleri (1932), Üniversite reformu (1933, Darülfünun → İstanbul Üniversitesi).

§ 4) Toplumsal alan
Şapka Kanunu (1925), tekke-zaviye ve türbelerin kapatılması (1925), uluslararası saat ve takvim (1925 kabul / 1926 yürürlük), ölçü birimleri (1931), Soyadı Kanunu (1934), lakap ve unvanların kaldırılması (1934), hafta tatilinin pazar günü olması (1935), kadınlara siyasal haklar (1930, 1933, 1934).

§ 5) Ekonomik alan
İzmir İktisat Kongresi (1923), aşarın kaldırılması (1925), Kabotaj Kanunu (1926), Teşvik-i Sanayi (1927), Merkez Bankası (1930), I. Beş Yıllık Sanayi Planı (1934), Sümerbank (1933), Etibank (1935).

§ İlke → devrim eşleşmesi
Cumhuriyetçilik: saltanatın kaldırılması, cumhuriyetin ilanı, kadınlara siyasi haklar.
Milliyetçilik: kabotaj, TTK-TDK, Türkçe ezan (1932), Misak-ı Millî.
Halkçılık: aşarın kaldırılması, soyadı ve unvanların kaldırılması, Medeni Kanun (eşitlik).
Devletçilik: beş yıllık plan, KİT'ler (Sümerbank, Etibank).
Laiklik: halifeliğin kaldırılması, Tevhid-i Tedrisat, Medeni Kanun, 1928 din maddesinin çıkarılması.
İnkılapçılık: tüm devrimlerin korunması ve sürekliliği; akıl ve bilim.

§ İlkelerin anayasaya girişi
1927 CHF tüzüğünde dört ilke, 1931 programında altı ok, 5 Şubat 1937'de anayasaya girdi.

§ Adım adım
Bir devrimin hangi ilkeyle ilgili olduğunu bulmak için "neyi değiştirdi?" sorusunu sor: yönetim → Cumhuriyetçilik; din-devlet ilişkisi → Laiklik; sınıf ayrımı / eşitlik → Halkçılık; millî kültür / ekonomi bağımsızlığı → Milliyetçilik; devletin ekonomideki rolü → Devletçilik.""",

"""§ Soru kalıpları
1) "Aşağıdaki devrimlerden hangisi halkçılık ilkesiyle doğrudan ilgilidir?"
2) Devrimleri kronolojik sıralama (aynı yıldakiler en çok şaşırtır: 1924 ve 1925 grupları).
3) "Hangisi laikliğe yönelik bir adım değildir?" → Soyadı Kanunu gibi farklı ilkeye ait seçenek.
4) "Bütünleyici ilke" sorusu: Laiklik ve İnkılapçılık bütünleyici ilkeler olarak geçer.

§ Anahtar kelime → cevap
• "3 Mart 1924" → halifelik, Tevhid-i Tedrisat, Şeriye ve Evkaf Vekâleti
• "İsviçre" → Medeni Kanun ve Borçlar Kanunu (1926)
• "Kıyı taşımacılığı" → Kabotaj (1926), milliyetçilik
• "Aşar" → 1925, halkçılık ve köylünün durumu
• "1 Kasım" → hem saltanatın kaldırılması (1922) hem harf devrimi (1928)
• "5 Şubat 1937" → ilkelerin anayasaya girişi

§ Tuzaklar
• "1 Kasım" iki farklı yılda iki farklı devrimdir; yılı kontrol et.
• Laiklik ilkesi 1937'de anayasaya girdi; "devletin dini İslam'dır" ibaresi 1928'de çıkarıldı. İkisi karıştırılır.
• Kadınlara siyasal hak sırası: belediye (1930) → muhtarlık (1933) → milletvekili (1934). Sırayı değiştiren seçenek çeldiricidir.
• Uluslararası takvim 1925'te kabul edildi, 1926'da yürürlüğe girdi.

§ Hafıza kodu
İlkeler: "CuMiHaDeLaİn" — Cumhuriyetçilik, Milliyetçilik, Halkçılık, Devletçilik, Laiklik, İnkılapçılık.
Kadın hakları: "Be-Mu-Mi" 30-33-34 (BElediye, MUhtar, MIlletvekili).
1926 kanunları: "İsviçre iki (Medeni, Borçlar), İtalya ceza, Almanya ticaret" → "İİ-İC-AT".

§ Mini test
1. Tevhid-i Tedrisat hangi ilkeyle en çok ilgilidir? — Cevap: Laiklik (ve millî eğitim yönüyle milliyetçilik).
2. Devletçiliğe geçişte etkili dış gelişme? — Cevap: 1929 Dünya Ekonomik Bunalımı.
3. Cumhuriyet'in ilanı hangi soruyu çözmüştür? — Cevap: Devlet başkanlığı (rejimin adı) sorununu.""",
)

HOCA['Çağdaş Tarih'] = (
"""§ Büyük resim
1923'te kurulan Türkiye'nin dış politikası iki kelimeyle özetlenir: "Yurtta sulh, cihanda sulh." Lozan'dan kalan sorunları (Musul, Boğazlar, Hatay) savaşmadan, masada çözmeye çalıştı. 1945'ten sonra ise dünya iki kutba ayrıldı ve Türkiye kendini Batı bloğunun içinde buldu.

§ Hikâye
1926'da Musul sorunu Milletler Cemiyeti'nin İngiltere lehine kararı sonrası Ankara Antlaşması ile Irak'a bırakılır. 1932'de Türkiye Milletler Cemiyeti'ne davetle üye olur. İtalya'nın Akdeniz'deki saldırgan tutumu Balkan ülkelerini birleştirir: 1934 Balkan Antantı (Türkiye, Yunanistan, Yugoslavya, Romanya). 1936'da Montrö Sözleşmesi ile Boğazlar tam olarak Türk egemenliğine geçer, komisyon kaldırılır. 1937'de doğu sınırının güvenliği için Sadabat Paktı (Türkiye, İran, Irak, Afganistan) imzalanır. Hatay 1938'de bağımsız devlet olur ve 1939'da Türkiye'ye katılır; Atatürk bunu göremeden 10 Kasım 1938'de vefat eder.
II. Dünya Savaşı'nda (1939–1945) İnönü hükümeti tarafsızlığı korumaya çalışır; Şubat 1945'te Almanya ve Japonya'ya sembolik savaş ilanı yapar, böylece BM'nin kurucu üyesi olur. Savaştan sonra SSCB Boğazlarda üs ve Kars-Ardahan'ı ister; bu tehdit Türkiye'yi ABD'ye yaklaştırır. Truman Doktrini (1947) ve Marshall Planı (1948) ile yardım alınır, Kore Savaşı'na (1950) asker gönderilir ve 1952'de NATO'ya girilir. İçeride 1946'da çok partili hayata geçilir, 1950'de Demokrat Parti iktidara gelir. 1974'te Kıbrıs Barış Harekâtı yapılır. 1989'da Berlin Duvarı yıkılır, 1991'de SSCB dağılır ve Türkiye bağımsızlığını kazanan Türk cumhuriyetlerini ilk tanıyan ülke olur.

§ Neden–sonuç zinciri
İtalya'nın yayılmacılığı → Balkan Antantı ve Montrö'de Boğazların silahlandırılması isteği.
Almanya-İtalya tehdidi → Avrupa'nın Türkiye'yi kazanmak istemesi → Montrö ve Hatay'da Türkiye lehine ortam.
SSCB talepleri (1945) → Batı'ya yöneliş → Truman, Marshall, NATO.

§ Tek cümlede
1923–1938 barışçı denge ve Lozan'ın eksiklerini tamamlama, 1939–1945 tarafsızlık, 1945 sonrası Batı bloğu demektir.""",

"""§ Kavram haritası
1) Atatürk dönemi dış politika (1923–1938), 2) II. Dünya Savaşı ve İnönü dönemi, 3) Soğuk Savaş ve sonrası.

§ 1) Atatürk dönemi — sorun / çözüm tablosu
Nüfus mübadelesinin uygulanması → 1930 Türk-Yunan dostluğu (Ankara Antlaşması).
Yabancı okullar → Türk kanunlarına tabi kılındı.
Musul → 1926 Ankara Antlaşması (Irak'a bırakıldı; petrol gelirinden 25 yıl %10 pay).
Milletler Cemiyeti → 1932 üyelik.
Balkan güvenliği → 1934 Balkan Antantı.
Boğazlar → 1936 Montrö (komisyon kalktı, Türkiye askerî denetim yetkisi kazandı).
Doğu sınırı → 1937 Sadabat Paktı.
Hatay → 1938 bağımsız Hatay Devleti, 1939 katılım.

§ 2) II. Dünya Savaşı — Türkiye'nin tutumu
Tarafsızlık; 1939 İngiltere-Fransa ile karşılıklı yardım; 1941 Almanya ile saldırmazlık paktı; Adana Görüşmesi (1943); Kahire Konferansı (1943); Şubat 1945 sembolik savaş ilanı → San Francisco'da BM kurucu üyesi.
Ekonomik etkiler: Millî Korunma Kanunu (1940), Varlık Vergisi (1942), karne uygulaması.

§ 3) Soğuk Savaş tablosu
Batı Bloku: Truman Doktrini 1947, Marshall Planı 1948, NATO 1949 (Türkiye 1952), Bağdat Paktı 1955 (sonra CENTO).
Doğu Bloku: Varşova Paktı 1955, COMECON.
Kritik olaylar: Kore Savaşı 1950–53, Küba Füze Krizi 1962 (Jüpiter füzeleri Türkiye'den çekildi), Johnson Mektubu 1964, Kıbrıs Barış Harekâtı 1974, Berlin Duvarı (1961 yapıldı, 1989 yıkıldı), SSCB'nin dağılması 1991.
Türkiye iç siyaset: 1946 çok partili seçim, 1950 DP iktidarı.

§ Kural ve istisna
Kural: Atatürk dönemi dış politikası barışçıdır. "İstisna" gibi görünen Hatay, askerî değil diplomatik yoldan kazanılmıştır.
Kural: Türkiye II. Dünya Savaşı'na girmemiştir; sembolik savaş ilanı fiilî savaş değildir.

§ Adım adım
Tarih 1923–38 → barış ve sorun çözme; 1939–45 → tarafsızlık; 1945–91 → blok politikası. Örgüt sorusunda kuruluş yılı ile Türkiye'nin üyelik yılını ayrı ayrı yaz.""",

"""§ Soru kalıpları
1) Atatürk dönemi dış politika olaylarını sıralama.
2) "Montrö ile hangisi sağlanmıştır?" → Boğazlarda tam egemenlik, komisyonun kaldırılması.
3) "Türkiye'nin NATO'ya girişinde etkili olan gelişme" → Kore Savaşı'na asker gönderilmesi, SSCB tehdidi.
4) "Balkan Antantı'nın kurulmasında etkili olan devlet" → İtalya'nın yayılmacılığı.

§ Anahtar kelime → cevap
• "Boğazlar komisyonu kaldırıldı" → Montrö 1936
• "Doğu sınırı güvenliği / İran, Irak, Afganistan" → Sadabat 1937
• "Yunanistan, Yugoslavya, Romanya" → Balkan Antantı 1934
• "Davetle üye" → Milletler Cemiyeti 1932
• "Kurucu üye olmak için sembolik savaş ilanı" → Şubat 1945, BM
• "Ekonomik yardım" → Marshall Planı 1948
• "Askerî yardım / komünizme karşı" → Truman Doktrini 1947

§ Tuzaklar
• NATO 1949'da kuruldu; Türkiye 1952'de üye oldu.
• Hatay'ın katılımı Atatürk'ün ölümünden sonradır (1939).
• Balkan Antantı'na Bulgaristan ve Arnavutluk katılmadı; Bulgaristan'ın katılmaması en çok sorulan ayrıntıdır.
• Truman (askerî-ekonomik yardım doktrini) ile Marshall (Avrupa'nın ekonomik kalkınması) karıştırılır.

§ Hafıza kodu
"Ba-Mo-Sa-Ha" → BAlkan 1934, MOntrö 1936, SAdabat 1937, HAtay 1939.
Soğuk Savaş: "Tru-Mar-NA-Ko" → Truman 47, Marshall 48, NATO 49, Kore 50 (her yıl bir adım), Türkiye NATO 52.

§ Mini test
1. Türkiye'nin Batı'ya yönelmesindeki temel neden? — Cevap: SSCB'nin 1945'teki Boğazlar ve Kars-Ardahan talepleri.
2. Musul sorunu hangi kurumun kararından sonra çözüldü? — Cevap: Milletler Cemiyeti.
3. Sadabat Paktı'nın üyeleri? — Cevap: Türkiye, İran, Irak, Afganistan.""",
)

HOCA['Kronoloji ve Strateji'] = (
"""§ Büyük resim
Tarih bir ezber listesi değil, bir zincirdir: her olay bir öncekinin sonucu, bir sonrakinin sebebidir. Kronolojiyi tarih rakamlarıyla değil, bu zincirle hatırlarsan bir yılı unutsan bile sırayı kaybetmezsin.

§ Hikâye: 1500 yıl tek nefeste
Bozkırda Hunlar ordu kurdu (MÖ 3. yy), Göktürkler adımızı taşa yazdı (6.–8. yy), Uygurlar yerleşti (8.–9. yy). Talas'ta (751) yüzümüz İslam'a döndü; Karahanlı, Gazneli, Selçuklu ile İslam dünyasının koruyucusu olduk (10.–11. yy). Malazgirt (1071) Anadolu kapısını açtı, Miryokefalon (1176) kilitledi, Kösedağ (1243) dağıttı. Beyliklerden Osmanlı doğdu (1299), Ankara'da (1402) sendeledi, İstanbul'da (1453) imparator oldu, Yavuz ve Kanuni'yle (16. yy) zirveye çıktı. Karlofça'da (1699) ilk kez geri çekildi, 18. yy'da Batı'ya baktı, 19. yy'da Tanzimat'la kendini yeniden yazdı. Balkanlar ve Dünya Savaşı imparatorluğu bitirdi; Millî Mücadele (1919–22) ve Lozan (1923) yeni devleti kurdu; devrimler (1923–38) onu modernleştirdi.

§ Sebep–sonuç ile sıralama tekniği
Bir sıralama sorusunda yılları hatırlamıyorsan şu doğal sırayı kullan:
Savaş → antlaşma → iç tepki / ıslahat.
Örnek: Pasarofça (antlaşma) → Lale Devri (barış ortamı) → Patrona Halil (tepki).
Örnek: Kırım Savaşı → Islahat Fermanı → Paris Antlaşması (aynı yıl ama ferman konferans sırasında, antlaşmadan hemen önce).
Örnek: Genelge → kongre → meclis → savaş → antlaşma.

§ Yüzyıl hesabı
Yılın ilk iki rakamına 1 ekle: 1071 → 11. yy; 1453 → 15. yy; 1923 → 20. yy. Sonu "00" ile biten yıl bir önceki yüzyılın son yılıdır: 1700 → 17. yy.

§ Tek cümlede
Rakamı unutsan da zinciri unutma: sebep önce, sonuç sonra.""",

"""§ Kavram haritası
Strateji üç araçtan oluşur: 1) Yüzyıl iskeleti, 2) Karıştırılan çiftler tablosu, 3) Soru tipine göre çözüm algoritması.

§ 1) Yüzyıl iskeleti
MÖ 3. yy: Asya Hun | 6.–8. yy: Göktürk, Talas 751 | 8.–9. yy: Uygur | 10.–11. yy: Karahanlı, Gazneli, Büyük Selçuklu, Malazgirt 1071 | 12.–13. yy: Anadolu Selçuklu, Miryokefalon 1176, Kösedağ 1243 | 14. yy: Osmanlı kuruluşu, Rumeli | 15. yy: Ankara 1402, İstanbul 1453 | 16. yy: Yavuz, Kanuni | 17. yy: Zitvatorok, Kasr-ı Şirin, Karlofça | 18. yy: Pasarofça, Lale Devri, Küçük Kaynarca, Nizam-ı Cedit | 19. yy: II. Mahmut, Tanzimat, Islahat, I. Meşrutiyet | 20. yy: II. Meşrutiyet, Balkan, I. Dünya, Millî Mücadele, Cumhuriyet.

§ 2) Karıştırılan çiftler
Ankara Savaşı 1402 ↔ Ankara Antlaşması 1921 (Fransa) ↔ Ankara Antlaşması 1926 (Musul) ↔ Ankara Antlaşması 1930 (Yunanistan).
Kosova I 1389 ↔ Kosova II 1448.
Londra Antlaşması 1913 ↔ Londra Konferansı 1921 ↔ Londra Sözleşmesi 1840.
Kanun-i Esasi 1876 ↔ Teşkilat-ı Esasiye 1921 ↔ 1924 Anayasası.
Kapitülasyon verilmesi (Kanuni) ↔ sürekli hâle gelmesi 1740 ↔ kaldırılması 1914 (tek taraflı) / 1923 (Lozan).
Edirne Antlaşması 1829 (Yunanistan'a özerklik) ↔ Edirne'nin geri alınması 1913.

§ 3) Soru tipine göre algoritma
Sıralama sorusu: önce yüzyıllara ayır → aynı yüzyıldakileri sebep-sonuçla sırala → seçeneklerde ilk ve son öğeyi kontrol ederek ele.
Öncüllü soru: en emin olduğun öncülü belirle → onu içermeyen (doğruysa) ya da içeren (yanlışsa) seçenekleri ele.
"Değildir" sorusu: kökteki olumsuzluğu işaretle → her seçeneğe "doğru mu?" diye bak → tek yanlışı bul.
Eşleştirme sorusu: en kesin eşleşmeden başla, seçenekleri daralt.

§ Adım adım zaman yönetimi
Tarih sorusu başına ortalama 45 saniye; bilmediğin soruda 2 seçeneğe indiremiyorsan işaretle ve geç; son turda dön.""",

"""§ Soru kalıpları
1) "Aşağıdaki gelişmeler kronolojik olarak sıralandığında hangisi üçüncü olur?"
2) "Aynı yüzyılda yaşanan gelişmeler hangileridir?"
3) Karıştırılan isimlerle öncüllü sorular (Ankara, Kosova, Londra).
4) "Hangisi diğerlerinden önce gerçekleşmiştir?"

§ Anahtar kelime → zaman
• "İlk" kelimeleri: ilk Türk adı (552), ilk Müslüman Türk devleti (Karahanlı), ilk anayasa (1876), ilk meclis (1877), ilk resmî gazete (1831), ilk matbaa (1727).
• "Son" kelimeleri: son Osmanlı Mebusan Meclisi (1920), Kuzey Afrika'da son toprak (1912).

§ Tuzaklar
• Aynı adı taşıyan farklı olaylar (Ankara, Londra, Kosova, Edirne).
• Kuruluş yılı ↔ üyelik yılı (NATO 1949 / Türkiye 1952).
• Kabul yılı ↔ yürürlük yılı (takvim 1925 / 1926; Merkez Bankası kuruluş 1930 / faaliyet 1931).
• Yüzyıl hesabında "00" ile biten yıllar.

§ Hafıza kodu
Rakam kancaları:
• 1071–1176–1243 → "71 kapı, 76 kilit, 43 dağılış".
• 1299–1402–1453 → "kuruluş, sendeleme, fetih".
• 1606–1699–1774 → "eşitlik, kayıp, Kırım".
• 1839–1856–1876 → "Tanzimat, Islahat, Meşrutiyet" (yaklaşık 20'şer yıl arayla).
• 1919–1920–1921–1922–1923 → "Samsun, Meclis, Sakarya, Taarruz, Lozan-Cumhuriyet".

§ Mini test
1. 1700 yılı kaçıncı yüzyıldır? — Cevap: 17. yüzyıl.
2. "Tanzimat, Karlofça, Küçük Kaynarca, Kösedağ" sırası? — Cevap: Kösedağ (1243) → Karlofça (1699) → Küçük Kaynarca (1774) → Tanzimat (1839).
3. 1921 Ankara Antlaşması kiminle imzalandı? — Cevap: Fransa.""",
)
