#!/usr/bin/env python3
"""Elle yazılmış 188 ek sorudaki yapay / KPSS dışı kalıpları düzeltir (tek seferlik editoryal geçiş).

KOK: yalnız kök değişir (şıklar ve çözüm korunur).
TAM: bilgi düzeyi KPSS'nin altında kalan sorular aynı konu alanında yeni bir soruyla değiştirilir.
Değişiklik TSV'ye, bankadaki kayda ve kapsam/inceleme özetlerine birlikte yazılır.

    python3 araclar/ek_kok_duzelt.py
"""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ek_gunluk500 import SOURCE, build  # noqa: E402
from kpss_kapsam import record_hash  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

KOK = {
    'GUN-EK-0005': 'Zorla yerinden edilmiş kişilerin korunması ile çocuk hakları ve çocukların esenliği alanlarında çalışan BM kuruluşları sırasıyla hangileridir?',
    'GUN-EK-0007': 'Hükûmet, işçi ve işveren temsilcilerinin birlikte karar aldığı üçlü yapısıyla bilinen BM uzmanlık kuruluşu hangisidir?',
    'GUN-EK-0008': 'Uluslararası sivil havacılık ile denizcilik güvenliği alanlarında standart belirleyen BM uzmanlık kuruluşları sırasıyla hangileridir?',
    'GUN-EK-0009': 'Telif hakları, patent ve marka gibi fikrî mülkiyet haklarının uluslararası düzeyde korunmasından sorumlu BM uzmanlık kuruluşu hangisidir?',
    'GUN-EK-0010': 'Telekomünikasyon ve bilgi-iletişim teknolojileri alanında uluslararası standartları belirleyen BM uzmanlık kuruluşu hangisidir?',
    'GUN-EK-0011': 'Birleşmiş Milletler Çevre Programı ile Birleşmiş Milletler Kalkınma Programının kısaltmaları sırasıyla hangileridir?',
    'GUN-EK-0013': 'Dünya Ticaret Örgütü ile Dünya Sağlık Örgütünün İngilizce kısaltmaları sırasıyla hangileridir?',
    'GUN-EK-0014': 'Devletler arasındaki hukuki uyuşmazlıkları çözen BM yargı organı ile soykırım ve insanlığa karşı suçlar gibi ağır suçlarda bireyleri yargılayan mahkeme sırasıyla hangileridir?',
    'GUN-EK-0017': 'NATO ile Avrupa Konseyinin merkezleri sırasıyla hangi şehirlerdedir?',
    'GUN-EK-0018': 'Ulusal polis teşkilatları arasında uluslararası iş birliğini sağlayan, merkezi Lyon’da bulunan kuruluş hangisidir?',
    'GUN-EK-0019': 'Ekonomik İşbirliği ve Kalkınma Örgütü ile Petrol İhraç Eden Ülkeler Örgütünün kısaltmaları sırasıyla hangileridir?',
    'GUN-EK-0020': 'UNESCO ile FAO’nun temel faaliyet alanları sırasıyla hangileridir?',
    'GUN-EK-0021': 'Yurt dışında Türk dili ve kültürünün tanıtımı ile kalkınma iş birliği projelerinin yürütülmesinden sorumlu kurumlar sırasıyla hangileridir?',
    'GUN-EK-0022': 'Marka ve patent tescili ile afet ve acil durum yönetiminden sorumlu kurumlar sırasıyla hangileridir?',
    'GUN-EK-0023': 'Bağımlılıkla mücadele ve insani yardım alanlarında faaliyet gösteren köklü sivil toplum kuruluşları sırasıyla hangileridir?',
    'GUN-EK-0024': 'Afet sonrası müdahale ve koordinasyon ile zorunlu deprem sigortası sisteminin yürütülmesinden sorumlu kuruluşlar sırasıyla hangileridir?',
    'GUN-EK-0028': 'Müzelerin, ören yerlerinin ve taşınmaz kültür varlıklarının yönetiminden sorumlu bakanlık hangisidir?',
    'GUN-EK-0039': 'Sefiller ile Notre-Dame’ın Kamburu romanlarının yazarı kimdir?',
    'GUN-EK-0040': 'Semaver ve Lüzumsuz Adam adlı öykü kitaplarının yazarı kimdir?',
    'GUN-EK-0041': 'Keşanlı Ali Destanı adlı oyunun yazarı kimdir?',
    'GUN-EK-0044': 'Ölmeye Yatmak ve Bir Düğün Gecesi romanlarının yazarı kimdir?',
    'GUN-EK-0048': 'Kuvâyi Milliye Destanı ve Memleketimden İnsan Manzaraları adlı eserlerin şairi kimdir?',
    'GUN-EK-0050': 'Çocuk ve Allah ile Çakırcalı Efe adlı eserlerin şairi kimdir?',
    'GUN-EK-0052': '2014 Cannes Film Festivali’nde Altın Palmiye ödülünü kazanan Kış Uykusu filminin yönetmeni kimdir?',
    'GUN-EK-0053': 'Susuz Yaz ve Sevmek Zamanı filmlerinin yönetmeni kimdir?',
    'GUN-EK-0054': '“Son Akşam Yemeği” freskinin ve “Mona Lisa” tablosunun sanatçısı aşağıdakilerden hangisidir?',
    'GUN-EK-0058': 'Kommagene Krallığı’na ait dev heykelleriyle tanınan Nemrut Dağı ören yeri hangi ilimizdedir?',
    'GUN-EK-0059': 'Homeros’un İlyada destanına konu olan ve UNESCO Dünya Mirası Listesi’nde yer alan Troya Antik Kenti hangi ilimizdedir?',
    'GUN-EK-0061': 'Xanthos ve Letoon antik kentleri hangi Anadolu uygarlığının merkezleri arasındadır?',
    'GUN-EK-0062': 'Heykel okuluyla ünlü Afrodisias Antik Kenti hangi ilimizdedir?',
    'GUN-EK-0063': 'Lidya Krallığı’nın başkenti Sardes’in kalıntıları hangi ilimizdedir?',
    'GUN-EK-0064': 'Zeugma antik kentinden çıkarılan mozaiklerin sergilendiği müze hangi ilimizdedir?',
    'GUN-EK-0065': 'Tarihî Odunpazarı evleriyle tanınan şehir hangisidir?',
    'GUN-EK-0066': 'Roma döneminden günümüze en iyi korunarak ulaşmış tiyatrolardan biri olan Aspendos hangi ilimizdedir?',
    'GUN-EK-0072': 'Tarihî Kırkpınar Yağlı Güreşleri hangi ilimizde düzenlenir?',
    'GUN-EK-0073': 'Horon ve zeybek halk oyunlarının yaygın olduğu yöreler sırasıyla hangileridir?',
    'GUN-EK-0075': 'Ney ve kudüm sırasıyla hangi çalgı türlerindendir?',
    'GUN-EK-0076': 'Doğu Karadeniz halk müziğinin temel çalgılarından kemençe hangi çalgı grubunda yer alır?',
    'GUN-EK-0077': 'Risâletü’n-Nushiyye adlı mesnevinin ve tasavvufi şiirlerinden oluşan Divan’ın sahibi olan şair kimdir?',
    'GUN-EK-0078': 'Avustralya’nın en kalabalık şehirleri Sidney ve Melbourne olmakla birlikte ülkenin başkenti hangisidir?',
    'GUN-EK-0082': 'Avrupa Birliği’nin başlıca kurumlarına ve NATO karargâhına ev sahipliği yapan Brüksel hangi ülkenin başkentidir?',
    'GUN-EK-0085': 'İrlanda Cumhuriyeti’nin başkenti aşağıdakilerden hangisidir?',
    'GUN-EK-0088': 'İzlanda’nın başkenti aşağıdakilerden hangisidir?',
    'GUN-EK-0092': 'Saraybosna ve Tiran sırasıyla hangi ülkelerin başkentleridir?',
    'GUN-EK-0096': 'Hanoi ve Bangkok sırasıyla hangi ülkelerin başkentleridir?',
    'GUN-EK-0099': 'İnka uygarlığına ait Machu Picchu antik kenti hangi ülkededir?',
    'GUN-EK-0103': 'Gobi ve Sahra çölleri sırasıyla hangi kıtalarda yer alır?',
    'GUN-EK-0106': 'Titicaca Gölü hangi iki ülkenin sınırında yer alır?',
    'GUN-EK-0108': 'Aşağıdaki Avrupa ülkelerinden hangisinin Akdeniz’e kıyısı yoktur?',
    'GUN-EK-0109': 'Süveyş Kanalı hangi iki denizi birbirine bağlar?',
    'GUN-EK-0111': 'Cebelitarık Boğazı hangi iki su kütlesini birbirine bağlar?',
    'GUN-EK-0124': '1999 Nobel Barış Ödülü’nü alan Médecins Sans Frontières kuruluşunun Türkçe adı hangisidir?',
    'GUN-EK-0126': 'Altın Ayı ödülü hangi uluslararası film festivalinde verilir?',
    'GUN-EK-0133': 'Grammy ve Emmy ödüllerinin verildiği alanlar sırasıyla hangileridir?',
    'GUN-EK-0141': '2016 ve 2024 Yaz Olimpiyat Oyunlarının ev sahibi şehirleri sırasıyla hangileridir?',
    'GUN-EK-0145': 'FIBA ve FIVB sırasıyla hangi spor dallarının uluslararası federasyonlarıdır?',
    'GUN-EK-0149': 'Tour de France hangi spor dalının en prestijli yarışlarındandır?',
    'GUN-EK-0151': 'Mete Gazoz 2020 Tokyo Olimpiyat Oyunları’nda hangi branşta altın madalya kazanmıştır?',
    'GUN-EK-0152': 'Naim Süleymanoğlu ve Halil Mutlu olimpiyat şampiyonluklarını hangi spor dalında kazanmıştır?',
    'GUN-EK-0153': 'Yaşar Doğu ve Celal Atik hangi spor dalında tanınmış sporculardır?',
    'GUN-EK-0155': 'Dekatlon hangi spor dalının çoklu yarışmasıdır?',
    'GUN-EK-0157': 'Epe, flöre ve kılıç hangi spor dalının silah türleridir?',
}

# id -> (kök, doğru, yanlış1, yanlış2, yanlış3, yanlış4, gerekçe)
TAM = {
    'GUN-EK-0002': ('Aşağıdaki devletlerden hangisi BM Güvenlik Konseyinin daimi üyelerinden biri değildir?',
                    'Almanya', 'Çin', 'Fransa', 'Rusya', 'Birleşik Krallık',
                    'Güvenlik Konseyinin beş daimi üyesi ABD, Rusya, Çin, Fransa ve Birleşik Krallık’tır. Almanya daimi üye değildir; zaman zaman geçici üye seçilir.'),
    'GUN-EK-0006': ('Aşağıdakilerden hangisi Birleşmiş Milletler Dünya Gıda Programının (WFP) temel görev alanıdır?',
                    'Acil durumlarda ihtiyaç sahiplerine gıda yardımı ulaştırmak', 'Tarım ve gıda politikalarına yönelik istatistik ve standart üretmek',
                    'Uluslararası çalışma standartlarını belirlemek', 'Salgın hastalıklarla küresel mücadeleyi koordine etmek',
                    'Mültecilerin hukuki korunmasını sağlamak',
                    'WFP acil gıda yardımı yapan BM kuruluşudur. Tarım politikaları FAO’nun, çalışma standartları ILO’nun, salgınlarla mücadele WHO’nun, mültecilerin korunması UNHCR’nin alanıdır.'),
    'GUN-EK-0012': ('1944 Bretton Woods Konferansı sonucunda kurulan ve uluslararası para sisteminin istikrarından sorumlu kuruluş aşağıdakilerden hangisidir?',
                    'Uluslararası Para Fonu (IMF)', 'Dünya Ticaret Örgütü (WTO)', 'Ekonomik İşbirliği ve Kalkınma Örgütü (OECD)',
                    'Avrupa İmar ve Kalkınma Bankası', 'Asya Altyapı Yatırım Bankası',
                    'IMF, Dünya Bankası ile birlikte 1944 Bretton Woods Konferansı’nda kurulmuştur. WTO 1995’te, OECD 1961’de, Avrupa İmar ve Kalkınma Bankası 1991’de kurulmuştur.'),
    'GUN-EK-0015': ('Avrupa İnsan Hakları Mahkemesi aşağıdaki kuruluşlardan hangisinin bünyesinde yer alır?',
                    'Avrupa Konseyi', 'Avrupa Birliği', 'Birleşmiş Milletler', 'Avrupa Güvenlik ve İşbirliği Teşkilatı', 'NATO',
                    'Strazburg’daki AİHM, Avrupa Konseyi bünyesindedir ve Avrupa İnsan Hakları Sözleşmesi’nin uygulanmasını denetler. Avrupa Birliği’nin yargı organı ise Lüksemburg’daki Avrupa Birliği Adalet Divanıdır.'),
    'GUN-EK-0025': ('Aşağıdakilerden hangisi Türkiye İstatistik Kurumunun (TÜİK) görevleri arasında yer almaz?',
                    'Para politikasını belirleyip uygulamak', 'Resmî istatistikleri derleyip yayımlamak', 'Adrese dayalı nüfus kayıt sistemi sonuçlarını açıklamak',
                    'Tüketici fiyat endeksini (enflasyon verisini) açıklamak', 'İşgücü istatistiklerini derlemek',
                    'TÜİK resmî istatistik üretir: nüfus, enflasyon (TÜFE) ve işgücü verileri bunlardandır. Para politikasını belirleyip uygulamak ise Türkiye Cumhuriyet Merkez Bankasının görevidir.'),
    'GUN-EK-0029': ('Türk Tarih Kurumu ile Türk Dil Kurumunun kuruluş yılları sırasıyla hangileridir?',
                    '1931 — 1932', '1932 — 1931', '1930 — 1933', '1931 — 1934', '1933 — 1932',
                    'Türk Tarih Kurumu 1931’de Türk Tarihi Tetkik Cemiyeti, Türk Dil Kurumu 1932’de Türk Dili Tetkik Cemiyeti adıyla kurulmuştur.'),
    'GUN-EK-0030': ('Kızılhaç Hareketi’nin kurucusu kabul edilen ve 1901’de ilk Nobel Barış Ödülü’nü paylaşan kişi kimdir?',
                    'Henry Dunant', 'Florence Nightingale', 'Fridtjof Nansen', 'Woodrow Wilson', 'Albert Schweitzer',
                    'Henry Dunant, Solferino Savaşı’ndaki gözlemleriyle Kızılhaç Hareketi’nin doğuşuna öncülük etmiş ve 1901 Nobel Barış Ödülü’nü Frédéric Passy ile paylaşmıştır.'),
    'GUN-EK-0031': ('Aşağıdakilerden hangisi UNESCO İnsanlığın Somut Olmayan Kültürel Mirası listesinde yer alan Türkiye unsurlarından biri değildir?',
                    'Safranbolu evleri', 'Karagöz', 'Türk kahvesi kültürü ve geleneği', 'Geleneksel Türk okçuluğu', 'Kırkpınar Yağlı Güreş Festivali',
                    'Safranbolu Şehri somut bir kültür varlığı olarak UNESCO Dünya Mirası Listesi’ndedir. Karagöz, Türk kahvesi, geleneksel Türk okçuluğu ve Kırkpınar ise somut olmayan kültürel miras listesindedir.'),
    'GUN-EK-0051': ('Senaryosunu Yılmaz Güney’in yazdığı ve 1982 Cannes Film Festivali’nde Altın Palmiye ödülünü kazanan film hangisidir?',
                    'Yol', 'Sürü', 'Umut', 'Düşman', 'Arkadaş',
                    'Yol, 1982 Cannes Film Festivali’nde Altın Palmiye’yi kazanmıştır. Sürü, Umut, Düşman ve Arkadaş da Yılmaz Güney’le anılan filmlerdir ama bu ödülü almamıştır.'),
    'GUN-EK-0067': ('Mimar Sinan’ın “ustalık eserim” olarak nitelendirdiği yapı hangisidir?',
                    'Selimiye Camii', 'Süleymaniye Camii', 'Şehzade Camii', 'Sultanahmet Camii', 'Mihrimah Sultan Camii',
                    'Sinan, Şehzade Camii’ni “çıraklık”, Süleymaniye’yi “kalfalık”, Edirne’deki Selimiye’yi “ustalık” eseri olarak niteler. Sultanahmet Camii ise Sedefkâr Mehmet Ağa’nındır.'),
    'GUN-EK-0079': ('Aşağıdaki ülke – başkent eşleştirmelerinden hangisi yanlıştır?',
                    'Kanada – Toronto', 'Avustralya – Canberra', 'Brezilya – Brasília', 'Fas – Rabat', 'Nijerya – Abuja',
                    'Kanada’nın başkenti Ottawa’dır; Toronto ülkenin en kalabalık şehridir. Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0080': ('Aşağıdaki ülke – başkent eşleştirmelerinden hangisi doğrudur?',
                    'Brezilya – Brasília', 'Kazakistan – Almatı', 'Myanmar – Yangon', 'Tanzanya – Darüsselam', 'Fildişi Sahili – Abidjan',
                    'Brezilya’nın başkenti Brasília’dır. Diğer seçeneklerdeki şehirler ülkelerinin eski başkenti ya da en büyük şehridir: Kazakistan’ın başkenti Astana, Myanmar’ınki Nepido, Tanzanya’nınki Dodoma, Fildişi Sahili’ninki Yamusukro’dur.'),
    'GUN-EK-0081': ('Aşağıdaki şehirlerden hangisi bulunduğu ülkenin başkenti değildir?',
                    'Kazablanka', 'Rabat', 'Lizbon', 'Dublin', 'Canberra',
                    'Kazablanka Fas’ın en büyük ticaret şehridir; başkent Rabat’tır. Lizbon, Dublin ve Canberra da kendi ülkelerinin başkentleridir.'),
    'GUN-EK-0084': ('Aşağıdaki şehir – ülke eşleştirmelerinden hangisi yanlıştır?',
                    'Porto – İspanya', 'Lyon – Fransa', 'Münih – Almanya', 'Milano – İtalya', 'Göteborg – İsveç',
                    'Porto Portekiz’in ikinci büyük şehridir; İspanya’da değildir. Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0097': ('Aşağıdaki ülkelerden hangisinin toprakları hem Asya hem Afrika kıtasında yer alır?',
                    'Mısır', 'Libya', 'Suudi Arabistan', 'Fas', 'Sudan',
                    'Mısır’ın büyük bölümü Afrika’dadır; Sina Yarımadası ise Asya kıtasında kalır. Libya, Fas ve Sudan yalnız Afrika’da, Suudi Arabistan yalnız Asya’dadır.'),
    'GUN-EK-0102': ('Aşağıdaki coğrafi unsurlardan hangisi Güney Amerika kıtasında yer almaz?',
                    'Kalahari Çölü', 'Atacama Çölü', 'And Dağları', 'Titicaca Gölü', 'Amazon Havzası',
                    'Kalahari Çölü Afrika’nın güneyindedir (Botsvana, Namibya). Atacama, And Dağları, Titicaca Gölü ve Amazon Havzası Güney Amerika’dadır.'),
    'GUN-EK-0104': ('Aşağıdaki çöl – kıta eşleştirmelerinden hangisi yanlıştır?',
                    'Gobi – Afrika', 'Sahra – Afrika', 'Atacama – Güney Amerika', 'Kalahari – Afrika', 'Rub’ül Hali – Asya',
                    'Gobi Çölü Asya’dadır (Moğolistan ve Çin). Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0105': ('Dünyanın en yüksek zirvesi Everest aşağıdaki ülkelerden hangi ikisinin sınırında yer alır?',
                    'Nepal — Çin', 'Hindistan — Nepal', 'Pakistan — Çin', 'Butan — Hindistan', 'Nepal — Butan',
                    'Everest (8.849 m) Himalayalar’da Nepal ile Çin (Tibet) sınırında yer alır.'),
    'GUN-EK-0107': ('Aşağıdaki ülkelerden hangisinin hem Hazar Denizi’ne hem Karadeniz’e kıyısı vardır?',
                    'Rusya', 'Türkiye', 'İran', 'Gürcistan', 'Kazakistan',
                    'Rusya hem Hazar Denizi’ne hem Karadeniz’e kıyısı olan tek seçenektir. Türkiye ve Gürcistan’ın yalnız Karadeniz’e, İran ve Kazakistan’ın yalnız Hazar Denizi’ne kıyısı vardır.'),
    'GUN-EK-0110': ('Aşağıdaki su yolu – bağladığı su kütleleri eşleştirmelerinden hangisi yanlıştır?',
                    'Panama Kanalı – Akdeniz ile Kızıldeniz', 'Süveyş Kanalı – Akdeniz ile Kızıldeniz',
                    'Cebelitarık Boğazı – Akdeniz ile Atlas Okyanusu', 'Babülmendep Boğazı – Kızıldeniz ile Aden Körfezi',
                    'Hürmüz Boğazı – Basra Körfezi ile Umman Denizi',
                    'Panama Kanalı Atlas Okyanusu ile Büyük Okyanus’u bağlar; Akdeniz ile Kızıldeniz’i bağlayan Süveyş Kanalı’dır. Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0127': ('Aşağıdaki film festivali – ana ödül eşleştirmelerinden hangisi yanlıştır?',
                    'Venedik – Altın Ayı', 'Cannes – Altın Palmiye', 'San Sebastián – Altın İstiridye', 'Antalya – Altın Portakal', 'Adana – Altın Koza',
                    'Venedik Film Festivali’nin büyük ödülü Altın Aslan’dır; Altın Ayı Berlin Film Festivali’nde verilir. Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0131': ('Türk sinemasına uluslararası alanda ilk büyük ödülü kazandıran, 1964 Berlin Film Festivali’nde Altın Ayı alan film hangisidir?',
                    'Susuz Yaz', 'Yol', 'Kış Uykusu', 'Sürü', 'Uzak',
                    'Metin Erksan’ın Susuz Yaz filmi 1964’te Berlin’de Altın Ayı kazanmıştır. Yol (1982) ve Kış Uykusu (2014) Cannes’da Altın Palmiye almıştır.'),
    'GUN-EK-0132': ('Aşağıdaki ödül – alan eşleştirmelerinden hangisi yanlıştır?',
                    'Pritzker – Edebiyat', 'Oscar – Sinema', 'Grammy – Müzik', 'Emmy – Televizyon', 'Booker – Edebiyat',
                    'Pritzker Ödülü mimarlık alanında verilir. Oscar sinema, Grammy müzik, Emmy televizyon, Booker edebiyat ödülüdür.'),
    'GUN-EK-0134': ('Mimarlık alanında verilen ve “mimarlığın Nobel’i” olarak anılan ödül hangisidir?',
                    'Pritzker Ödülü', 'Pulitzer Ödülü', 'Booker Ödülü', 'Grammy Ödülü', 'Fields Madalyası',
                    'Pritzker mimarlık ödülüdür. Pulitzer gazetecilik-edebiyat-müzik, Booker roman, Grammy müzik, Fields Madalyası matematik alanında verilir.'),
    'GUN-EK-0136': ('Matematik alanında dört yılda bir verilen ve “matematiğin Nobel’i” olarak anılan ödül hangisidir?',
                    'Fields Madalyası', 'Pritzker Ödülü', 'Booker Ödülü', 'Pulitzer Ödülü', 'Altın Palmiye',
                    'Fields Madalyası dört yılda bir, Uluslararası Matematik Kongresi’nde 40 yaş altındaki matematikçilere verilir.'),
    'GUN-EK-0137': ('Nuri Bilge Ceylan’ın Kış Uykusu filmiyle 2014’te kazandığı ödül hangisidir?',
                    'Cannes Altın Palmiye', 'Berlin Altın Ayı', 'Venedik Altın Aslan', 'Oscar En İyi Uluslararası Film', 'San Sebastián Altın İstiridye',
                    'Kış Uykusu 2014 Cannes Film Festivali’nde Altın Palmiye’yi kazanmıştır; Yol’dan (1982) sonra bu ödülü alan ikinci Türk filmidir.'),
    'GUN-EK-0146': ('Aşağıdaki uluslararası spor federasyonu – branş eşleştirmelerinden hangisi yanlıştır?',
                    'FIDE – Eskrim', 'FIFA – Futbol', 'FIBA – Basketbol', 'FIVB – Voleybol', 'FIG – Cimnastik',
                    'FIDE Dünya Satranç Federasyonudur; eskrimin federasyonu FIE’dir. Diğer eşleştirmeler doğrudur.'),
    'GUN-EK-0148': ('Türkiye A Millî Futbol Takımı 2002 FIFA Dünya Kupası’nı hangi derece ile tamamlamıştır?',
                    'Üçüncülük', 'İkincilik', 'Dördüncülük', 'Çeyrek final', 'Son 16',
                    'Türkiye 2002 Güney Kore-Japonya Dünya Kupası’nda üçüncülük maçında Güney Kore’yi yenerek turnuvayı üçüncü bitirmiştir.'),
    'GUN-EK-0158': ('Aşağıdaki sporlardan hangisi Kış Olimpiyat Oyunları programında yer alır?',
                    'Skeleton', 'Badminton', 'Hentbol', 'Eskrim', 'Golf',
                    'Skeleton, buz pistinde yüzüstü kızakla yapılan bir kış sporudur. Badminton, hentbol, eskrim ve golf Yaz Olimpiyatları’nda yer alır.'),
}


def main():
    src = ROOT / SOURCE
    satirlar = src.read_text(encoding='utf-8').splitlines()
    gorulen = set()
    for i, line in enumerate(satirlar):
        if not line.strip() or line.startswith('#'):
            continue
        p = line.split('|')
        sid = p[0]
        if sid in KOK:
            p[3] = KOK[sid]
        elif sid in TAM:
            kok, d, a, b, c, e, g = TAM[sid]
            p = [sid, p[1], '3', kok, d, a, b, c, e, g]
        else:
            continue
        assert all('|' not in x for x in p) and len(p) == 10, sid
        satirlar[i] = '|'.join(p)
        gorulen.add(sid)
    assert gorulen == set(KOK) | set(TAM), set(KOK) | set(TAM) - gorulen
    src.write_text('\n'.join(satirlar) + '\n', encoding='utf-8')

    records, topics = build(ROOT)
    yeni = {r['id']: r for r in records if r['id'] in gorulen}
    # Banka kaydı
    bank = ROOT / 'data/sorular/guncel.jsonl'
    out = []
    for line in bank.read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.startswith('#'):
            r = json.loads(line)
            if r['id'] in yeni:
                kap = r.get('kpss_kapsam')
                r = dict(yeni[r['id']])
                if kap is not None:
                    r['kpss_kapsam'] = kap
                line = json.dumps(r, ensure_ascii=False)
        out.append(line)
    bank.write_text('\n'.join(out) + '\n', encoding='utf-8')
    # Kapsam ve inceleme özetleri
    for yol, ind in (('data/kpss_kapsam.json', None), ('data/kaynaklar/ek_188_inceleme.json', None)):
        f = ROOT / yol
        txt = f.read_text(encoding='utf-8')
        d = json.loads(txt)
        for sid, r in yeni.items():
            d['questions'][sid]['sha256'] = record_hash(r)
        ind = 1 if txt.startswith('{\n ') and not txt.startswith('{\n  ') else 2 if txt.startswith('{\n  ') else None
        f.write_text(json.dumps(d, ensure_ascii=False, indent=ind) + '\n', encoding='utf-8')
    print(len(yeni), 'ek soru düzeltildi')


if __name__ == '__main__':
    main()
