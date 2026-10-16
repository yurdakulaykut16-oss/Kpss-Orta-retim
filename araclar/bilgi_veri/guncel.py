"""Güncel bilgiler / genel kültür tabloları (kalıcı, tartışmasız bilgiler).

Zamanla değişebilecek bilgiler (görevdeki kişiler, anlık sıralamalar) bilerek
kullanılmamıştır. Birden fazla doğru cevaba yol açabilecek kayıtlar (ör. birden
çok resmî başkenti olan ülkeler, kıtalararası ülkeler) çıkarılmıştır.
"""
from .ortak import eslesme, q, sec

# ülke | başkent | kıta ('-' = kıta sorusu sorulmaz)
ULKELER = """
Almanya|Berlin|Avrupa
Fransa|Paris|Avrupa
İtalya|Roma|Avrupa
İspanya|Madrid|Avrupa
Portekiz|Lizbon|Avrupa
Birleşik Krallık|Londra|Avrupa
İrlanda|Dublin|Avrupa
Hollanda|Amsterdam|Avrupa
Belçika|Brüksel|Avrupa
İsviçre|Bern|Avrupa
Avusturya|Viyana|Avrupa
Polonya|Varşova|Avrupa
Çekya|Prag|Avrupa
Slovakya|Bratislava|Avrupa
Macaristan|Budapeşte|Avrupa
Romanya|Bükreş|Avrupa
Bulgaristan|Sofya|Avrupa
Yunanistan|Atina|Avrupa
Arnavutluk|Tiran|Avrupa
Kuzey Makedonya|Üsküp|Avrupa
Sırbistan|Belgrad|Avrupa
Karadağ|Podgorica|Avrupa
Bosna-Hersek|Saraybosna|Avrupa
Hırvatistan|Zagreb|Avrupa
Slovenya|Lubliyana|Avrupa
Danimarka|Kopenhag|Avrupa
Norveç|Oslo|Avrupa
İsveç|Stockholm|Avrupa
Finlandiya|Helsinki|Avrupa
İzlanda|Reykjavik|Avrupa
Estonya|Tallinn|Avrupa
Letonya|Riga|Avrupa
Litvanya|Vilnius|Avrupa
Belarus|Minsk|Avrupa
Ukrayna|Kiev|Avrupa
Moldova|Kişinev|Avrupa
Malta|Valletta|Avrupa
Kosova|Priştine|Avrupa
Lihtenştayn|Vaduz|Avrupa
Japonya|Tokyo|Asya
Çin|Pekin|Asya
Güney Kore|Seul|Asya
Kuzey Kore|Pyongyang|Asya
Moğolistan|Ulan Batur|Asya
Hindistan|Yeni Delhi|Asya
Pakistan|İslamabad|Asya
Bangladeş|Dakka|Asya
Nepal|Katmandu|Asya
Butan|Thimphu|Asya
Afganistan|Kabil|Asya
İran|Tahran|Asya
Irak|Bağdat|Asya
Suriye|Şam|Asya
Lübnan|Beyrut|Asya
Ürdün|Amman|Asya
Suudi Arabistan|Riyad|Asya
Umman|Maskat|Asya
Birleşik Arap Emirlikleri|Abu Dabi|Asya
Katar|Doha|Asya
Bahreyn|Manama|Asya
Azerbaycan|Bakü|-
Gürcistan|Tiflis|-
Ermenistan|Erivan|-
Kazakistan|Astana|-
Özbekistan|Taşkent|Asya
Türkmenistan|Aşkabat|Asya
Kırgızistan|Bişkek|Asya
Tacikistan|Duşanbe|Asya
Tayland|Bangkok|Asya
Vietnam|Hanoi|Asya
Laos|Vientiane|Asya
Kamboçya|Phnom Penh|Asya
Myanmar|Naypyidaw|Asya
Malezya|Kuala Lumpur|Asya
Filipinler|Manila|Asya
Doğu Timor|Dili|Asya
Maldivler|Male|Asya
Mısır|Kahire|-
Libya|Trablus|Afrika
Fas|Rabat|Afrika
Sudan|Hartum|Afrika
Etiyopya|Addis Ababa|Afrika
Kenya|Nairobi|Afrika
Tanzanya|Dodoma|Afrika
Uganda|Kampala|Afrika
Ruanda|Kigali|Afrika
Somali|Mogadişu|Afrika
Nijerya|Abuja|Afrika
Gana|Akra|Afrika
Senegal|Dakar|Afrika
Mali|Bamako|Afrika
Nijer|Niamey|Afrika
Çad|Encamena|Afrika
Kamerun|Yaunde|Afrika
Angola|Luanda|Afrika
Zambiya|Lusaka|Afrika
Zimbabve|Harare|Afrika
Mozambik|Maputo|Afrika
Madagaskar|Antananarivo|Afrika
Namibya|Windhoek|Afrika
Botsvana|Gaborone|Afrika
Demokratik Kongo Cumhuriyeti|Kinşasa|Afrika
Kongo Cumhuriyeti|Brazzaville|Afrika
Gabon|Libreville|Afrika
Burkina Faso|Vagadugu|Afrika
Gine|Konakri|Afrika
Sierra Leone|Freetown|Afrika
Liberya|Monrovia|Afrika
Moritanya|Nuakşot|Afrika
Eritre|Asmara|Afrika
Malavi|Lilongwe|Afrika
Togo|Lome|Afrika
Amerika Birleşik Devletleri|Washington|Kuzey Amerika
Kanada|Ottawa|Kuzey Amerika
Küba|Havana|-
Jamaika|Kingston|-
Honduras|Tegucigalpa|-
Nikaragua|Managua|-
Kosta Rika|San José|-
El Salvador|San Salvador|-
Haiti|Port-au-Prince|-
Dominik Cumhuriyeti|Santo Domingo|-
Brezilya|Brasilia|Güney Amerika
Arjantin|Buenos Aires|Güney Amerika
Şili|Santiago|Güney Amerika
Peru|Lima|Güney Amerika
Kolombiya|Bogota|Güney Amerika
Venezuela|Karakas|Güney Amerika
Ekvador|Quito|Güney Amerika
Paraguay|Asuncion|Güney Amerika
Uruguay|Montevideo|Güney Amerika
Guyana|Georgetown|Güney Amerika
Surinam|Paramaribo|Güney Amerika
Avustralya|Kanberra|Okyanusya
Yeni Zelanda|Wellington|Okyanusya
Papua Yeni Gine|Port Moresby|Okyanusya
Fiji|Suva|Okyanusya
Rusya|Moskova|-
"""
KITALAR = ['Avrupa', 'Asya', 'Afrika', 'Kuzey Amerika', 'Güney Amerika', 'Okyanusya']

# ülke | para birimi
PARA = """
Japonya|yen
Çin|yuan
Hindistan|rupi
Pakistan|rupi
Rusya|ruble
Birleşik Krallık|sterlin
İsviçre|frank
Amerika Birleşik Devletleri|dolar
Almanya|avro
Fransa|avro
İtalya|avro
Hırvatistan|avro
Brezilya|real
Meksika|peso
Arjantin|peso
Güney Kore|won
Suudi Arabistan|riyal
Katar|riyal
Polonya|zloti
Macaristan|forint
İsveç|kron
Norveç|kron
Danimarka|kron
Romanya|ley
Ukrayna|grivna
Azerbaycan|manat
Türkmenistan|manat
Kazakistan|tenge
Gürcistan|lari
Ermenistan|dram
Özbekistan|som
Kırgızistan|som
Tacikistan|somoni
Moğolistan|tugrik
Tayland|baht
Vietnam|dong
Endonezya|rupiah
Malezya|ringgit
Bangladeş|taka
Güney Afrika|rand
Nijerya|naira
Gana|cedi
Kenya|şilin
İsrail|şekel
Ürdün|dinar
Irak|dinar
Kuveyt|dinar
Cezayir|dinar
Tunus|dinar
Sırbistan|dinar
Fas|dirhem
Birleşik Arap Emirlikleri|dirhem
Venezuela|bolivar
Peru|sol
Paraguay|guarani
Kosta Rika|colon
Etiyopya|birr
Arnavutluk|lek
Kuzey Makedonya|denar
Bosna-Hersek|konvertibl mark
"""

# şehir | ülke
SEHIRLER = """
Marsilya|Fransa
Lyon|Fransa
Milano|İtalya
Napoli|İtalya
Venedik|İtalya
Floransa|İtalya
Barselona|İspanya
Sevilla|İspanya
Valensiya|İspanya
Porto|Portekiz
Münih|Almanya
Hamburg|Almanya
Frankfurt|Almanya
Köln|Almanya
Manchester|Birleşik Krallık
Liverpool|Birleşik Krallık
Edinburgh|Birleşik Krallık
Cenevre|İsviçre
Zürih|İsviçre
Salzburg|Avusturya
Krakov|Polonya
Selanik|Yunanistan
Rotterdam|Hollanda
Anvers|Belçika
Göteborg|İsveç
Sankt-Peterburg|Rusya
Kazan|Rusya
Odessa|Ukrayna
Prizren|Kosova
Mostar|Bosna-Hersek
Filibe|Bulgaristan
Köstence|Romanya
Batum|Gürcistan
Gence|Azerbaycan
Semerkant|Özbekistan
Buhara|Özbekistan
Almatı|Kazakistan
Şanghay|Çin
Osaka|Japonya
Kyoto|Japonya
Busan|Güney Kore
Mumbai|Hindistan
Kalküta|Hindistan
Karaçi|Pakistan
Lahor|Pakistan
Tebriz|İran
İsfahan|İran
Meşhed|İran
Musul|Irak
Basra|Irak
Kerkük|Irak
Halep|Suriye
Mekke|Suudi Arabistan
Medine|Suudi Arabistan
Cidde|Suudi Arabistan
Dubai|Birleşik Arap Emirlikleri
İskenderiye|Mısır
Kazablanka|Fas
Marakeş|Fas
Lagos|Nijerya
Cape Town|Güney Afrika
Johannesburg|Güney Afrika
Zanzibar|Tanzanya
New York|Amerika Birleşik Devletleri
Los Angeles|Amerika Birleşik Devletleri
Chicago|Amerika Birleşik Devletleri
Toronto|Kanada
Montreal|Kanada
Vancouver|Kanada
Rio de Janeiro|Brezilya
São Paulo|Brezilya
Sidney|Avustralya
Melbourne|Avustralya
Auckland|Yeni Zelanda
Ho Chi Minh|Vietnam
Nice|Fransa
Bordeaux|Fransa
Strazburg|Fransa
Torino|İtalya
Palermo|İtalya
Bologna|İtalya
Granada|İspanya
Bilbao|İspanya
Dresden|Almanya
Leipzig|Almanya
Stuttgart|Almanya
Glasgow|Birleşik Krallık
Oxford|Birleşik Krallık
Basel|İsviçre
Lozan|İsviçre
Graz|Avusturya
Gdansk|Polonya
Brno|Çekya
Debrecen|Macaristan
Cluj-Napoca|Romanya
Varna|Bulgaristan
Split|Hırvatistan
Dubrovnik|Hırvatistan
Bergen|Norveç
Tampere|Finlandiya
Malmö|İsveç
Aarhus|Danimarka
Novosibirsk|Rusya
Vladivostok|Rusya
Harkov|Ukrayna
Lviv|Ukrayna
Kandahar|Afganistan
Herat|Afganistan
Şiraz|İran
Necef|Irak
Kerbela|Irak
Erbil|Irak
Humus|Suriye
Lazkiye|Suriye
Akabe|Ürdün
Agra|Hindistan
Bangalore|Hindistan
Hiroşima|Japonya
Nagazaki|Japonya
Guangzhou|Çin
Kaşgar|Çin
Urumçi|Çin
Fergana|Özbekistan
Hive|Özbekistan
Oş|Kırgızistan
Şuşa|Azerbaycan
Nahçıvan|Azerbaycan
Luksor|Mısır
Asvan|Mısır
Bingazi|Libya
Kayrevan|Tunus
Fes|Fas
Tanca|Fas
Timbuktu|Mali
Durban|Güney Afrika
Mombasa|Kenya
Boston|Amerika Birleşik Devletleri
Miami|Amerika Birleşik Devletleri
San Francisco|Amerika Birleşik Devletleri
Houston|Amerika Birleşik Devletleri
Las Vegas|Amerika Birleşik Devletleri
Québec|Kanada
Guadalajara|Meksika
Medellín|Kolombiya
Cusco|Peru
Valparaíso|Şili
Rosario|Arjantin
Manaus|Brezilya
Perth|Avustralya
Brisbane|Avustralya
"""

# yapı / eser | ülke
YAPILAR = """
Eyfel Kulesi|Fransa
Louvre Müzesi|Fransa
Kolezyum|İtalya
Pisa Kulesi|İtalya
Tac Mahal|Hindistan
Çin Seddi|Çin
Özgürlük Heykeli|Amerika Birleşik Devletleri
Golden Gate Köprüsü|Amerika Birleşik Devletleri
Big Ben|Birleşik Krallık
Stonehenge|Birleşik Krallık
Petra Antik Kenti|Ürdün
Machu Picchu|Peru
Kremlin Sarayı|Rusya
Ermitaj Müzesi|Rusya
Akropolis|Yunanistan
Sagrada Familia|İspanya
Elhamra Sarayı|İspanya
Prado Müzesi|İspanya
Burç Halife|Birleşik Arap Emirlikleri
Sidney Opera Binası|Avustralya
Kurtarıcı İsa Heykeli|Brezilya
Angkor Vat Tapınağı|Kamboçya
Keops Piramidi|Mısır
Brandenburg Kapısı|Almanya
Neuschwanstein Şatosu|Almanya
Petronas İkiz Kuleleri|Malezya
Chichen Itza|Meksika
Atomium|Belçika
Moai Heykelleri|Şili
"""

# ülke | resmî dil
DILLER = """
Brezilya|Portekizce
Angola|Portekizce
Mozambik|Portekizce
Arjantin|İspanyolca
Meksika|İspanyolca
Kolombiya|İspanyolca
Şili|İspanyolca
Avusturya|Almanca
Hollanda|Felemenkçe
İran|Farsça
Mısır|Arapça
Suudi Arabistan|Arapça
Senegal|Fransızca
Macaristan|Macarca
Moğolistan|Moğolca
Polonya|Lehçe
Yunanistan|Yunanca
Bulgaristan|Bulgarca
Japonya|Japonca
Vietnam|Vietnamca
"""
DIL_HAVUZ = ['Portekizce', 'İspanyolca', 'Almanca', 'Felemenkçe', 'Farsça', 'Arapça', 'Fransızca', 'Macarca',
             'Moğolca', 'Lehçe', 'Yunanca', 'Bulgarca', 'Japonca', 'Vietnamca', 'İngilizce', 'İtalyanca', 'Rusça']

# kısaltma | Türkçe adı | merkez | kuruluş yılı ('-' = sorulmaz)
ORGUTLER = """
NATO|Kuzey Atlantik Antlaşması Örgütü|Brüksel|1949
BM|Birleşmiş Milletler|New York|1945
UNESCO|Birleşmiş Milletler Eğitim, Bilim ve Kültür Örgütü|Paris|1945
UNICEF|Birleşmiş Milletler Çocuklara Yardım Fonu|New York|1946
DSÖ (WHO)|Dünya Sağlık Örgütü|Cenevre|1948
DTÖ (WTO)|Dünya Ticaret Örgütü|Cenevre|1995
OPEC|Petrol İhraç Eden Ülkeler Örgütü|Viyana|1960
OECD|Ekonomik İşbirliği ve Kalkınma Örgütü|Paris|1961
FAO|Gıda ve Tarım Örgütü|Roma|1945
ILO|Uluslararası Çalışma Örgütü|Cenevre|1919
IAEA|Uluslararası Atom Enerjisi Ajansı|Viyana|1957
ASEAN|Güneydoğu Asya Uluslar Birliği|Cakarta|1967
İİT|İslam İşbirliği Teşkilatı|Cidde|1969
KEİ|Karadeniz Ekonomik İşbirliği Örgütü|İstanbul|1992
EİT|Ekonomik İşbirliği Teşkilatı|Tahran|1985
UNHCR|Birleşmiş Milletler Mülteciler Yüksek Komiserliği|Cenevre|1950
WIPO|Dünya Fikri Mülkiyet Örgütü|Cenevre|1967
WMO|Dünya Meteoroloji Örgütü|Cenevre|1950
ITU|Uluslararası Telekomünikasyon Birliği|Cenevre|1865
UPU|Dünya Posta Birliği|Bern|1874
CERN|Avrupa Nükleer Araştırma Merkezi|Cenevre|1954
ESA|Avrupa Uzay Ajansı|Paris|1975
TDT|Türk Devletleri Teşkilatı|İstanbul|2009
TÜRKSOY|Uluslararası Türk Kültürü Teşkilatı|Ankara|1993
D-8|Gelişen Sekiz Ülke Ekonomik İşbirliği Örgütü|İstanbul|1997
INTERPOL|Uluslararası Kriminal Polis Teşkilatı|Lyon|1923
FIFA|Uluslararası Futbol Federasyonları Birliği|Zürih|1904
UEFA|Avrupa Futbol Federasyonları Birliği|Nyon|1954
IOC|Uluslararası Olimpiyat Komitesi|Lozan|1894
ŞİÖ|Şanghay İşbirliği Örgütü|Pekin|2001
ICRC|Uluslararası Kızılhaç Komitesi|Cenevre|1863
AB|Avrupa Birliği|Brüksel|1993
AİHM|Avrupa İnsan Hakları Mahkemesi|Strazburg|1959
UAD|Uluslararası Adalet Divanı|Lahey|1945
UCM|Uluslararası Ceza Mahkemesi|Lahey|2002
AK|Avrupa Konseyi|Strazburg|1949
AfB|Afrika Birliği|Addis Ababa|2002
ArB|Arap Birliği|Kahire|1945
"""
KISALTMA_SOR = {'NATO', 'UNESCO', 'UNICEF', 'OPEC', 'OECD', 'FAO', 'ILO', 'IAEA', 'ASEAN', 'İİT', 'KEİ', 'EİT',
                'UNHCR', 'WIPO', 'WMO', 'ITU', 'UPU', 'CERN', 'ESA', 'TÜRKSOY', 'INTERPOL', 'FIFA', 'UEFA', 'IOC',
                'ŞİÖ', 'AİHM', 'DSÖ (WHO)', 'DTÖ (WTO)', 'D-8'}

# kurum | bağlı ya da ilişkili bakanlık
BAKANLIK = """
Devlet Su İşleri Genel Müdürlüğü|Tarım ve Orman Bakanlığı
Orman Genel Müdürlüğü|Tarım ve Orman Bakanlığı
Tapu ve Kadastro Genel Müdürlüğü|Çevre, Şehircilik ve İklim Değişikliği Bakanlığı
Göç İdaresi Başkanlığı|İçişleri Bakanlığı
Sahil Güvenlik Komutanlığı|İçişleri Bakanlığı
Jandarma Genel Komutanlığı|İçişleri Bakanlığı
Emniyet Genel Müdürlüğü|İçişleri Bakanlığı
Afet ve Acil Durum Yönetimi Başkanlığı (AFAD)|İçişleri Bakanlığı
Nüfus ve Vatandaşlık İşleri Genel Müdürlüğü|İçişleri Bakanlığı
Türk İşbirliği ve Koordinasyon Ajansı (TİKA)|Kültür ve Turizm Bakanlığı
Yurtdışı Türkler ve Akraba Topluluklar Başkanlığı|Kültür ve Turizm Bakanlığı
Vakıflar Genel Müdürlüğü|Kültür ve Turizm Bakanlığı
Devlet Tiyatroları Genel Müdürlüğü|Kültür ve Turizm Bakanlığı
Kredi ve Yurtlar Genel Müdürlüğü|Gençlik ve Spor Bakanlığı
Türk Patent ve Marka Kurumu|Sanayi ve Teknoloji Bakanlığı
Türk Standardları Enstitüsü|Sanayi ve Teknoloji Bakanlığı
TÜBİTAK|Sanayi ve Teknoloji Bakanlığı
Türkiye Uzay Ajansı|Sanayi ve Teknoloji Bakanlığı
KOSGEB|Sanayi ve Teknoloji Bakanlığı
Gelir İdaresi Başkanlığı|Hazine ve Maliye Bakanlığı
Sosyal Güvenlik Kurumu|Çalışma ve Sosyal Güvenlik Bakanlığı
Türkiye İş Kurumu (İŞKUR)|Çalışma ve Sosyal Güvenlik Bakanlığı
Karayolları Genel Müdürlüğü|Ulaştırma ve Altyapı Bakanlığı
Devlet Hava Meydanları İşletmesi|Ulaştırma ve Altyapı Bakanlığı
TCDD|Ulaştırma ve Altyapı Bakanlığı
BOTAŞ|Enerji ve Tabii Kaynaklar Bakanlığı
Türkiye Petrolleri Anonim Ortaklığı (TPAO)|Enerji ve Tabii Kaynaklar Bakanlığı
Maden Tetkik ve Arama Genel Müdürlüğü (MTA)|Enerji ve Tabii Kaynaklar Bakanlığı
Ceza ve Tevkifevleri Genel Müdürlüğü|Adalet Bakanlığı
Adli Tıp Kurumu|Adalet Bakanlığı
Gümrükler Muhafaza Genel Müdürlüğü|Ticaret Bakanlığı
Türkiye İlaç ve Tıbbi Cihaz Kurumu|Sağlık Bakanlığı
"""

# eser | yazar | grup (T = Türk, D = dünya)
ESERLER = """
Çalıkuşu|Reşat Nuri Güntekin|T
Yaprak Dökümü|Reşat Nuri Güntekin|T
Dudaktan Kalbe|Reşat Nuri Güntekin|T
Sinekli Bakkal|Halide Edib Adıvar|T
Ateşten Gömlek|Halide Edib Adıvar|T
Yaban|Yakup Kadri Karaosmanoğlu|T
Kiralık Konak|Yakup Kadri Karaosmanoğlu|T
Sodom ve Gomore|Yakup Kadri Karaosmanoğlu|T
Huzur|Ahmet Hamdi Tanpınar|T
Saatleri Ayarlama Enstitüsü|Ahmet Hamdi Tanpınar|T
İnce Memed|Yaşar Kemal|T
Tutunamayanlar|Oğuz Atay|T
Bir Bilim Adamının Romanı|Oğuz Atay|T
Kuyucaklı Yusuf|Sabahattin Ali|T
İçimizdeki Şeytan|Sabahattin Ali|T
Kürk Mantolu Madonna|Sabahattin Ali|T
Aşk-ı Memnu|Halit Ziya Uşaklıgil|T
Mai ve Siyah|Halit Ziya Uşaklıgil|T
Kırık Hayatlar|Halit Ziya Uşaklıgil|T
Araba Sevdası|Recaizade Mahmut Ekrem|T
İntibah|Namık Kemal|T
Vatan yahut Silistre|Namık Kemal|T
Şair Evlenmesi|Şinasi|T
Taaşşuk-ı Talat ve Fitnat|Şemsettin Sami|T
Eylül|Mehmet Rauf|T
Safahat|Mehmet Akif Ersoy|T
Kendi Gök Kubbemiz|Yahya Kemal Beyatlı|T
Han Duvarları|Faruk Nafiz Çamlıbel|T
Memleketimden İnsan Manzaraları|Nazım Hikmet Ran|T
Çile|Necip Fazıl Kısakürek|T
Otuz Beş Yaş|Cahit Sıtkı Tarancı|T
Benim Adım Kırmızı|Orhan Pamuk|T
Kar|Orhan Pamuk|T
Masumiyet Müzesi|Orhan Pamuk|T
Yorgun Savaşçı|Kemal Tahir|T
Devlet Ana|Kemal Tahir|T
Bereketli Topraklar Üzerinde|Orhan Kemal|T
Fatih-Harbiye|Peyami Safa|T
Dokuzuncu Hariciye Koğuşu|Peyami Safa|T
Kaşağı|Ömer Seyfettin|T
Puslu Kıtalar Atlası|İhsan Oktay Anar|T
Yılanların Öcü|Fakir Baykurt|T
Kutadgu Bilig|Yusuf Has Hacib|T
Divanü Lügati't-Türk|Kaşgarlı Mahmud|T
Atabetü'l-Hakayık|Edip Ahmet Yükneki|T
Nutuk|Mustafa Kemal Atatürk|T
Felatun Bey ile Rakım Efendi|Ahmet Mithat Efendi|T
Karabibik|Nabizade Nazım|T
Sergüzeşt|Samipaşazade Sezai|T
Şıpsevdi|Hüseyin Rahmi Gürpınar|T
Leyla ile Mecnun (Leyla vü Mecnun)|Fuzuli|T
Hüsn ü Aşk|Şeyh Galip|T
Seyahatname|Evliya Çelebi|T
Cihannüma|Kâtip Çelebi|T
Mesnevi|Mevlana Celaleddin Rumi|T
Muhakemetü'l-Lugateyn|Ali Şir Nevai|T
Babürname|Babür Şah|T
Göl Saatleri|Ahmet Haşim|T
Rübab-ı Şikeste|Tevfik Fikret|T
Makber|Abdülhak Hamit Tarhan|T
Türkçülüğün Esasları|Ziya Gökalp|T
Memleket Hikâyeleri|Refik Halit Karay|T
Ayaşlı ile Kiracıları|Memduh Şevket Esendal|T
Semaver|Sait Faik Abasıyanık|T
Alemdağ'da Var Bir Yılan|Sait Faik Abasıyanık|T
Keşanlı Ali Destanı|Haldun Taner|T
Zübük|Aziz Nesin|T
Hababam Sınıfı|Rıfat Ilgaz|T
Küçük Ağa|Tarık Buğra|T
Ben Sana Mecburum|Attila İlhan|T
Üvercinka|Cemal Süreya|T
Hasretinden Prangalar Eskittim|Ahmet Arif|T
Monna Rosa|Sezai Karakoç|T
Anayurt Oteli|Yusuf Atılgan|T
Ölmeye Yatmak|Adalet Ağaoğlu|T
Sevgili Arsız Ölüm|Latife Tekin|T
Mavi Sürgün|Cevat Şakir Kabaağaçlı (Halikarnas Balıkçısı)|T
Çankaya|Falih Rıfkı Atay|T
Kara Kitap|Orhan Pamuk|T
Beyaz Kale|Orhan Pamuk|T
Yer Demir Gök Bakır|Yaşar Kemal|T
Teneke|Yaşar Kemal|T
Ağrıdağı Efsanesi|Yaşar Kemal|T
Tehlikeli Oyunlar|Oğuz Atay|T
Korkuyu Beklerken|Oğuz Atay|T
Mahur Beste|Ahmet Hamdi Tanpınar|T
Beş Şehir|Ahmet Hamdi Tanpınar|T
Mor Salkımlı Ev|Halide Edib Adıvar|T
Vurun Kahpeye|Halide Edib Adıvar|T
Ankara|Yakup Kadri Karaosmanoğlu|T
Yeşil Gece|Reşat Nuri Güntekin|T
Acımak|Reşat Nuri Güntekin|T
Esir Şehrin İnsanları|Kemal Tahir|T
Murtaza|Orhan Kemal|T
Cemile|Orhan Kemal|T
Sözde Kızlar|Peyami Safa|T
Matmazel Noraliya'nın Koltuğu|Peyami Safa|T
Sırça Köşk|Sabahattin Ali|T
Değirmen|Sabahattin Ali|T
Bizim Köy|Mahmut Makal|T
Kuyruklu Yıldız Altında Bir İzdivaç|Hüseyin Rahmi Gürpınar|T
Gulyabani|Hüseyin Rahmi Gürpınar|T
Zehra|Nabizade Nazım|T
Cezmi|Namık Kemal|T
Bir Düğün Gecesi|Adalet Ağaoğlu|T
Fikrimin İnce Gülü|Adalet Ağaoğlu|T
Berci Kristin Çöp Masalları|Latife Tekin|T
Aylak Adam|Yusuf Atılgan|T
Sefiller|Victor Hugo|D
Notre Dame'ın Kamburu|Victor Hugo|D
Suç ve Ceza|Fyodor Dostoyevski|D
Karamazov Kardeşler|Fyodor Dostoyevski|D
Kumarbaz|Fyodor Dostoyevski|D
Budala|Fyodor Dostoyevski|D
Savaş ve Barış|Lev Tolstoy|D
Anna Karenina|Lev Tolstoy|D
Diriliş|Lev Tolstoy|D
Don Kişot|Miguel de Cervantes|D
Hamlet|William Shakespeare|D
Romeo ve Juliet|William Shakespeare|D
Macbeth|William Shakespeare|D
Othello|William Shakespeare|D
Faust|Johann Wolfgang von Goethe|D
İlahi Komedya|Dante Alighieri|D
Dönüşüm|Franz Kafka|D
Dava|Franz Kafka|D
Yüzyıllık Yalnızlık|Gabriel García Márquez|D
Simyacı|Paulo Coelho|D
Küçük Prens|Antoine de Saint-Exupéry|D
Bülbülü Öldürmek|Harper Lee|D
1984|George Orwell|D
Hayvan Çiftliği|George Orwell|D
Yabancı|Albert Camus|D
Veba|Albert Camus|D
Madam Bovary|Gustave Flaubert|D
Germinal|Émile Zola|D
Babalar ve Oğullar|İvan Turgenyev|D
Oliver Twist|Charles Dickens|D
İki Şehrin Hikâyesi|Charles Dickens|D
Robinson Crusoe|Daniel Defoe|D
Gulliver'in Gezileri|Jonathan Swift|D
Fareler ve İnsanlar|John Steinbeck|D
Gazap Üzümleri|John Steinbeck|D
Yaşlı Adam ve Deniz|Ernest Hemingway|D
Çanlar Kimin İçin Çalıyor|Ernest Hemingway|D
Martin Eden|Jack London|D
Beyaz Diş|Jack London|D
Ölü Canlar|Nikolay Gogol|D
Palto|Nikolay Gogol|D
Vişne Bahçesi|Anton Çehov|D
Monte Kristo Kontu|Alexandre Dumas|D
Üç Silahşörler|Alexandre Dumas|D
Seksen Günde Devrialem|Jules Verne|D
Denizler Altında Yirmi Bin Fersah|Jules Verne|D
Uğultulu Tepeler|Emily Brontë|D
Jane Eyre|Charlotte Brontë|D
Gurur ve Önyargı|Jane Austen|D
Frankenstein|Mary Shelley|D
Drakula|Bram Stoker|D
Moby Dick|Herman Melville|D
Tom Sawyer'ın Maceraları|Mark Twain|D
Pinokyo|Carlo Collodi|D
Alice Harikalar Diyarında|Lewis Carroll|D
Şeker Portakalı|José Mauro de Vasconcelos|D
Körlük|José Saramago|D
Otomatik Portakal|Anthony Burgess|D
Ana|Maksim Gorki|D
Satranç|Stefan Zweig|D
Bulantı|Jean-Paul Sartre|D
Kırmızı ve Siyah|Stendhal|D
Goriot Baba|Honoré de Balzac|D
Dorian Gray'in Portresi|Oscar Wilde|D
Cesur Yeni Dünya|Aldous Huxley|D
Fahrenheit 451|Ray Bradbury|D
Yüzüklerin Efendisi|J. R. R. Tolkien|D
Sineklerin Tanrısı|William Golding|D
Çavdar Tarlasında Çocuklar|J. D. Salinger|D
Muhteşem Gatsby|F. Scott Fitzgerald|D
Kayıp Zamanın İzinde|Marcel Proust|D
Ulysses|James Joyce|D
İlyada|Homeros|D
Odysseia|Homeros|D
Prens|Niccolò Machiavelli|D
Ütopya|Thomas More|D
Devlet|Platon|D
Toplum Sözleşmesi|Jean-Jacques Rousseau|D
Kanunların Ruhu|Montesquieu|D
Ulusların Zenginliği|Adam Smith|D
Türlerin Kökeni|Charles Darwin|D
Mukaddime|İbn Haldun|D
El-Kanun fi't-Tıb|İbn Sina|D
Şehname|Firdevsi|D
Rubailer|Ömer Hayyam|D
Bostan ve Gülistan|Sadi Şirazi|D
"""

# eser | sanatçı | grup (R = resim/heykel, M = müzik)
SANAT = """
Mona Lisa|Leonardo da Vinci|R
Son Akşam Yemeği|Leonardo da Vinci|R
Yıldızlı Gece|Vincent van Gogh|R
Ayçiçekleri|Vincent van Gogh|R
Guernica|Pablo Picasso|R
Çığlık|Edvard Munch|R
İnci Küpeli Kız|Johannes Vermeer|R
Venüs'ün Doğuşu|Sandro Botticelli|R
Belleğin Azmi|Salvador Dalí|R
Kaplumbağa Terbiyecisi|Osman Hamdi Bey|R
Gece Devriyesi|Rembrandt|R
Atina Okulu|Raffaello|R
Davut Heykeli|Michelangelo|R
Öpücük|Gustav Klimt|R
İzlenim: Gün Doğumu|Claude Monet|R
Halka Yol Gösteren Özgürlük|Eugène Delacroix|R
Düşünen Adam|Auguste Rodin|R
Dokuzuncu Senfoni|Ludwig van Beethoven|M
Ay Işığı Sonatı|Ludwig van Beethoven|M
Dört Mevsim|Antonio Vivaldi|M
Sihirli Flüt|Wolfgang Amadeus Mozart|M
Türk Marşı (Rondo alla Turca)|Wolfgang Amadeus Mozart|M
Kuğu Gölü|Pyotr İlyiç Çaykovski|M
Fındıkkıran|Pyotr İlyiç Çaykovski|M
Carmen|Georges Bizet|M
Aida|Giuseppe Verdi|M
La Traviata|Giuseppe Verdi|M
Bolero|Maurice Ravel|M
Mavi Tuna|Johann Strauss (oğul)|M
Yunus Emre Oratoryosu|Ahmet Adnan Saygun|M
Köçekçe|Ulvi Cemal Erkin|M
İstiklal Marşı'nın bestesi|Osman Zeki Üngör|M
"""

# buluş / keşif | bilim insanı
BULUSLAR = """
Telefon|Alexander Graham Bell
Ampulün ticari olarak geliştirilmesi|Thomas Edison
Penisilin|Alexander Fleming
Görelilik kuramı|Albert Einstein
Evrensel çekim yasası|Isaac Newton
Hareketli harfli matbaa|Johannes Gutenberg
Dinamit|Alfred Nobel
Kuduz aşısı|Louis Pasteur
Çiçek aşısı|Edward Jenner
Telsiz telgraf|Guglielmo Marconi
Evrim kuramı (doğal seçilim)|Charles Darwin
DNA'nın çift sarmal yapısı|James Watson ve Francis Crick
Periyodik tablo|Dmitri Mendeleyev
Kalıtım yasaları|Gregor Mendel
Güneş merkezli evren modeli|Nikolas Kopernik
Buhar makinesinin geliştirilmesi|James Watt
X ışınları|Wilhelm Röntgen
World Wide Web (www)|Tim Berners-Lee
Cebir biliminin temelleri|Harezmi
Paratoner|Benjamin Franklin
Motorlu uçak ile ilk uçuş|Wright Kardeşler
Benzinli otomobil|Karl Benz
Sinematograf|Lumière Kardeşler
DNA onarım mekanizmaları|Aziz Sancar
Radyoaktivite araştırmaları (polonyum ve radyum)|Marie Curie
Cıvalı termometre|Daniel Gabriel Fahrenheit
Elektrik pili (Volta pili)|Alessandro Volta
Elektromanyetik indüksiyon|Michael Faraday
Büyük kan dolaşımının tanımlanması|William Harvey
Analitik makine (bilgisayarın öncüsü)|Charles Babbage
Çekirdekli atom modeli|Ernest Rutherford
Mors alfabesi|Samuel Morse
Teleskopla Jüpiter'in uydularının keşfi|Galileo Galilei
Gezegenlerin hareket yasaları|Johannes Kepler
Hücre kavramının ilk kullanımı|Robert Hooke
"""

# film | yönetmen
FILMLER = """
Kış Uykusu|Nuri Bilge Ceylan
Uzak|Nuri Bilge Ceylan
Ahlat Ağacı|Nuri Bilge Ceylan
Bir Zamanlar Anadolu'da|Nuri Bilge Ceylan
Kuru Otlar Üstüne|Nuri Bilge Ceylan
Susuz Yaz|Metin Erksan
Bal|Semih Kaplanoğlu
Mustang|Deniz Gamze Ergüven
Babam ve Oğlum|Çağan Irmak
Eşkıya|Yavuz Turgul
Muhsin Bey|Yavuz Turgul
Selvi Boylum Al Yazmalım|Atıf Yılmaz
Umut|Yılmaz Güney
Sürü|Zeki Ökten
"""

# UNESCO Dünya Mirası | il | listeye giriş yılı
UNESCO = """
Göreme Millî Parkı ve Kapadokya|Nevşehir|1985
Divriği Ulu Camii ve Darüşşifası|Sivas|1985
Hattuşa|Çorum|1986
Nemrut Dağı|Adıyaman|1987
Hierapolis-Pamukkale|Denizli|1988
Safranbolu Şehri|Karabük|1994
Truva Antik Kenti|Çanakkale|1998
Selimiye Camii ve Külliyesi|Edirne|2011
Çatalhöyük Neolitik Kenti|Konya|2012
Bursa ve Cumalıkızık|Bursa|2014
Bergama|İzmir|2014
Diyarbakır Kalesi ve Hevsel Bahçeleri|Diyarbakır|2015
Efes|İzmir|2015
Ani Arkeolojik Alanı|Kars|2016
Afrodisias|Aydın|2017
Göbeklitepe|Şanlıurfa|2018
Arslantepe Höyüğü|Malatya|2021
Gordion|Ankara|2023
"""
IL_HAVUZ = ['Nevşehir', 'Sivas', 'Çorum', 'Adıyaman', 'Denizli', 'Karabük', 'Çanakkale', 'Edirne', 'Konya', 'Bursa',
            'İzmir', 'Diyarbakır', 'Kars', 'Aydın', 'Şanlıurfa', 'Malatya', 'Ankara', 'Kayseri', 'Mardin', 'Trabzon',
            'Erzurum', 'Antalya', 'Muğla', 'Manisa']

# coğrafi işaretli ürün | il
COGRAFI_ISARET = """
Mesir macunu|Manisa
Pestil ve köme|Gümüşhane
Ezine peyniri|Çanakkale
Hereke halısı|Kocaeli
İznik çinisi|Bursa
İnegöl köftesi|Bursa
Akçaabat köftesi|Trabzon
Ayvalık zeytinyağı|Balıkesir
Midyat telkârisi|Mardin
Zile pekmezi|Tokat
Taşköprü sarımsağı|Kastamonu
Öküzgözü üzümü|Elazığ
Milas halısı|Muğla
Kangal köpeği|Sivas
Cağ kebabı|Erzurum
İsot|Şanlıurfa
Pastırma|Kayseri
Mihaliç peyniri|Balıkesir
Gemlik zeytini|Bursa
Devrek bastonu|Zonguldak
Beypazarı kurusu|Ankara
Bafra pidesi|Samsun
Silivri yoğurdu|İstanbul
Kandıra yoğurdu|Kocaeli
"""

# Yaz Olimpiyat Oyunları: yıl | şehir
YAZ_OLIMPIYAT = """
1896|Atina
1900|Paris
1904|St. Louis
1908|Londra
1912|Stockholm
1920|Anvers
1924|Paris
1928|Amsterdam
1932|Los Angeles
1936|Berlin
1948|Londra
1952|Helsinki
1956|Melbourne
1960|Roma
1964|Tokyo
1968|Meksiko
1972|Münih
1976|Montreal
1980|Moskova
1984|Los Angeles
1988|Seul
1992|Barselona
1996|Atlanta
2000|Sidney
2004|Atina
2008|Pekin
2012|Londra
2016|Rio de Janeiro
2020|Tokyo
2024|Paris
2028|Los Angeles
2032|Brisbane
"""
KIS_OLIMPIYAT = """
1924|Chamonix
1928|St. Moritz
1932|Lake Placid
1936|Garmisch-Partenkirchen
1948|St. Moritz
1952|Oslo
1956|Cortina d'Ampezzo
1960|Squaw Valley
1964|Innsbruck
1968|Grenoble
1972|Sapporo
1976|Innsbruck
1980|Lake Placid
1984|Saraybosna
1988|Calgary
1992|Albertville
1994|Lillehammer
1998|Nagano
2002|Salt Lake City
2006|Torino
2010|Vancouver
2014|Soçi
2018|Pyeongchang
2022|Pekin
2026|Milano-Cortina
"""

# FIFA Dünya Kupası: yıl | ev sahibi | şampiyon ('-' = sorulmaz)
DUNYA_KUPASI = """
1930|Uruguay|Uruguay
1934|İtalya|İtalya
1938|Fransa|İtalya
1950|Brezilya|Uruguay
1954|İsviçre|Batı Almanya
1958|İsveç|Brezilya
1962|Şili|Brezilya
1966|İngiltere|İngiltere
1970|Meksika|Brezilya
1974|Batı Almanya|Batı Almanya
1978|Arjantin|Arjantin
1982|İspanya|İtalya
1986|Meksika|Arjantin
1990|İtalya|Batı Almanya
1994|ABD|Brezilya
1998|Fransa|Fransa
2002|Güney Kore ve Japonya|Brezilya
2006|Almanya|İtalya
2010|Güney Afrika|İspanya
2014|Brezilya|Almanya
2018|Rusya|Fransa
2022|Katar|Arjantin
2026|ABD, Kanada ve Meksika|-
"""
DK_ULKE = ['Uruguay', 'İtalya', 'Fransa', 'Brezilya', 'İsviçre', 'İsveç', 'Şili', 'İngiltere', 'Meksika', 'Batı Almanya',
           'Arjantin', 'İspanya', 'ABD', 'Güney Kore ve Japonya', 'Almanya', 'Güney Afrika', 'Rusya', 'Katar',
           'Hollanda', 'Portekiz', 'Belçika', 'Türkiye']

# sporcu | branş
SPORCULAR = """
Naim Süleymanoğlu|Halter
Halil Mutlu|Halter
Taha Akgül|Güreş
Rıza Kayaalp|Güreş
Hamza Yerlikaya|Güreş
Yaşar Doğu|Güreş
Yasemin Adar Yiğit|Güreş
Mete Gazoz|Okçuluk
Yusuf Dikeç|Atıcılık
Şevval İlayda Tarhan|Atıcılık
Busenaz Sürmeneli|Boks
Buse Naz Çakıroğlu|Boks
Süreyya Ayhan|Atletizm
Ramil Guliyev|Atletizm
Elvan Abeylegesse|Atletizm
Servet Tazegül|Tekvando
Nur Tatar|Tekvando
Eda Erdem Dündar|Voleybol
Ebrar Karakurt|Voleybol
Zehra Güneş|Voleybol
Mehmet Okur|Basketbol
Hidayet Türkoğlu|Basketbol
Alperen Şengün|Basketbol
Hakan Şükür|Futbol
Rüştü Reçber|Futbol
Arda Güler|Futbol
Kenan Sofuoğlu|Motosiklet yarışı
Toprak Razgatlıoğlu|Motosiklet yarışı
İbrahim Çolak|Cimnastik
Ferhat Arıcan|Cimnastik
Zeynep Sönmez|Tenis
"""
BRANSLAR = ['Halter', 'Güreş', 'Okçuluk', 'Atıcılık', 'Boks', 'Atletizm', 'Tekvando', 'Voleybol', 'Basketbol', 'Futbol',
            'Motosiklet yarışı', 'Cimnastik', 'Tenis', 'Yüzme', 'Judo', 'Eskrim']

# terim | spor dalı
TERIMLER = """
Ofsayt|Futbol
Korner|Futbol
Ribaund|Basketbol
Turnike|Basketbol
Tuş|Güreş
Nakavt|Boks
Birdie|Golf
Şah mat|Satranç
İppon|Judo
Strike|Bowling
Pit stop|Formula 1
Grand Slam|Tenis
"""
TERIM_HAVUZ = ['Futbol', 'Basketbol', 'Güreş', 'Boks', 'Golf', 'Satranç', 'Judo', 'Bowling', 'Formula 1', 'Tenis',
               'Voleybol', 'Yüzme', 'Okçuluk']

# konu | soru | doğru | yanlış1..4 | gerekçe
OZEL = """
Spor|Futbolda bir takım sahada kaç oyuncuyla oynar?|11|9|10|12|7|Futbolda takımlar sahada 11 oyuncuyla mücadele eder.
Spor|Basketbolda bir takım sahada kaç oyuncuyla oynar?|5|6|7|4|8|Basketbolda sahada her takımdan 5 oyuncu bulunur.
Spor|Voleybolda bir takım sahada kaç oyuncuyla oynar?|6|5|7|8|9|Voleybolda sahada her takımdan 6 oyuncu bulunur.
Spor|Hentbolda bir takım sahada kaç oyuncuyla (kaleci dahil) oynar?|7|6|5|9|11|Hentbolda sahada kaleci dahil 7 oyuncu bulunur.
Spor|Su topunda bir takım suda kaç oyuncuyla (kaleci dahil) oynar?|7|6|5|9|11|Su topunda kaleci dahil 7 oyuncu bulunur.
Spor|Futsalda bir takım sahada kaç oyuncuyla (kaleci dahil) oynar?|5|6|7|4|8|Futsalda kaleci dahil 5 oyuncu bulunur.
Spor|Beşiktaş Jimnastik Kulübü hangi yıl kurulmuştur?|1903|1905|1907|1910|1899|Beşiktaş 1903'te kurulmuştur.
Spor|Galatasaray Spor Kulübü hangi yıl kurulmuştur?|1905|1903|1907|1910|1923|Galatasaray 1905'te kurulmuştur.
Spor|Fenerbahçe Spor Kulübü hangi yıl kurulmuştur?|1907|1903|1905|1911|1923|Fenerbahçe 1907'de kurulmuştur.
Spor|Trabzonspor hangi yıl kurulmuştur?|1967|1963|1971|1959|1975|Trabzonspor 1967'de kurulmuştur.
Spor|2005 UEFA Şampiyonlar Ligi finali hangi şehirde oynanmıştır?|İstanbul|Paris|Atina|Moskova|Roma|2005 finali İstanbul Atatürk Olimpiyat Stadı'nda oynanmıştır.
Spor|2023 UEFA Şampiyonlar Ligi finalinde İstanbul'da kupayı hangi takım kazanmıştır?|Manchester City|Inter|Real Madrid|Liverpool|Bayern Münih|2023 finalinde Manchester City, Inter'i yenmiştir.
Spor|2000 yılında UEFA Kupası'nı kazanan Türk takımı hangisidir?|Galatasaray|Fenerbahçe|Beşiktaş|Trabzonspor|Bursaspor|Galatasaray 2000'de UEFA Kupası'nı ve UEFA Süper Kupası'nı kazanmıştır.
Spor|2013 Akdeniz Oyunları hangi ilimizde düzenlenmiştir?|Mersin|İzmir|Antalya|Adana|Muğla|2013 Akdeniz Oyunları Mersin'de yapılmıştır.
Spor|1971 Akdeniz Oyunları hangi ilimizde düzenlenmiştir?|İzmir|Mersin|İstanbul|Antalya|Ankara|1971 Akdeniz Oyunları İzmir'de yapılmıştır.
Spor|2011 Kış Üniversite Oyunları (Universiade) hangi ilimizde düzenlenmiştir?|Erzurum|Kars|Bolu|Kayseri|Bursa|2011 Kış Universiadı Erzurum'da yapılmıştır.
Spor|2010 FIBA Dünya Basketbol Şampiyonası hangi ülkede düzenlenmiştir?|Türkiye|İspanya|Japonya|Çin|ABD|2010 Dünya Basketbol Şampiyonası Türkiye'de yapılmıştır.
Spor|EURO 2032'ye Türkiye hangi ülkeyle birlikte ev sahipliği yapacaktır?|İtalya|Yunanistan|İspanya|Almanya|Fransa|UEFA, EURO 2032'yi Türkiye ve İtalya'ya vermiştir.
Spor|2002 FIFA Dünya Kupası'nda Türkiye kaçıncı olmuştur?|Üçüncü|İkinci|Dördüncü|Çeyrek finalist|Birinci|Türkiye 2002 Dünya Kupası'nı üçüncü olarak tamamlamıştır.
Son Olaylar|Uzaya giden ilk Türk astronot kimdir?|Alper Gezeravcı|Tuva Cihangir Atasever|Aziz Sancar|Mete Gazoz|Kenan Sofuoğlu|Alper Gezeravcı Ocak 2024'te Uluslararası Uzay İstasyonuna gitmiştir.
Son Olaylar|Uzaya giden ikinci Türk kimdir?|Tuva Cihangir Atasever|Alper Gezeravcı|Daron Acemoğlu|Ramil Guliyev|Arda Güler|Tuva Cihangir Atasever 2024'te alt yörünge uçuşuyla uzaya gitmiştir.
Son Olaylar|1915 Çanakkale Köprüsü hangi yıl hizmete açılmıştır?|2022|2019|2020|2023|2016|1915 Çanakkale Köprüsü 18 Mart 2022'de açılmıştır.
Son Olaylar|Osmangazi Köprüsü hangi körfez üzerinde yer alır?|İzmit Körfezi|Gemlik Körfezi|Edremit Körfezi|İzmir Körfezi|İskenderun Körfezi|Osmangazi Köprüsü İzmit Körfezi'ni geçer.
Son Olaylar|İstanbul Boğazı'ndaki üçüncü köprü hangisidir?|Yavuz Sultan Selim Köprüsü|Fatih Sultan Mehmet Köprüsü|15 Temmuz Şehitler Köprüsü|Osmangazi Köprüsü|1915 Çanakkale Köprüsü|Boğaz'daki üçüncü köprü Yavuz Sultan Selim Köprüsü'dür.
Son Olaylar|Marmaray hangi yıl hizmete açılmıştır?|2013|2010|2016|2018|2008|Marmaray 29 Ekim 2013'te açılmıştır.
Son Olaylar|Avrasya Tüneli hangi yıl hizmete açılmıştır?|2016|2013|2018|2014|2020|Avrasya Tüneli 2016'da açılmıştır.
Son Olaylar|Türkiye'nin ilk nükleer santrali Akkuyu hangi ilimizdedir?|Mersin|Sinop|Kırklareli|Antalya|Adana|Akkuyu Nükleer Güç Santrali Mersin'dedir.
Son Olaylar|Yerli otomobil TOGG'un üretim tesisi hangi ilimizdedir?|Bursa|Kocaeli|Sakarya|Ankara|İzmir|TOGG fabrikası Bursa'nın Gemlik ilçesindedir.
Son Olaylar|Türkiye'nin ilk yerli ve millî haberleşme uydusu hangisidir?|Türksat 6A|Türksat 5A|Göktürk-1|Türksat 4A|İMECE|Türksat 6A 2024'te fırlatılan ilk yerli haberleşme uydusudur.
Son Olaylar|İlk uçuşunu 2024'te yapan Türkiye'nin millî muharip uçağı hangisidir?|KAAN|HÜRJET|Kızılelma|Akıncı|ANKA|KAAN ilk uçuşunu 21 Şubat 2024'te yapmıştır.
Son Olaylar|İstanbul Havalimanı hangi yıl hizmete açılmıştır?|2018|2015|2016|2020|2013|İstanbul Havalimanı 29 Ekim 2018'de açılmıştır.
Son Olaylar|Kahramanmaraş merkezli büyük depremler hangi tarihte yaşanmıştır?|6 Şubat 2023|17 Ağustos 1999|30 Ekim 2020|23 Ekim 2011|12 Kasım 1999|Pazarcık ve Elbistan merkezli depremler 6 Şubat 2023'te yaşanmıştır.
Son Olaylar|2024 Nobel Ekonomi Ödülü'nü kazananlar arasında yer alan Türk asıllı bilim insanı kimdir?|Daron Acemoğlu|Aziz Sancar|Orhan Pamuk|Cahit Arf|Feza Gürsey|Daron Acemoğlu 2024 Nobel Ekonomi Ödülü'nü paylaşmıştır.
Kültür|2015 Nobel Kimya Ödülü'nü kazanan Türk bilim insanı kimdir?|Aziz Sancar|Daron Acemoğlu|Cahit Arf|Gazi Yaşargil|Canan Dağdeviren|Aziz Sancar 2015 Nobel Kimya Ödülü'nü almıştır.
Kültür|Nobel Edebiyat Ödülü'nü kazanan ilk Türk yazar kimdir?|Orhan Pamuk|Yaşar Kemal|Nazım Hikmet|Elif Şafak|Ahmet Hamdi Tanpınar|Orhan Pamuk 2006 Nobel Edebiyat Ödülü'nü almıştır.
Kültür|Orhan Pamuk Nobel Edebiyat Ödülü'nü hangi yıl almıştır?|2006|2004|2008|2010|2002|Orhan Pamuk 2006'da Nobel Edebiyat Ödülü'nü almıştır.
Kültür|Cannes Film Festivali'nde Altın Palmiye kazanan “Kış Uykusu” filmi hangi yıl ödül almıştır?|2014|2008|2011|2018|2010|Kış Uykusu 2014'te Altın Palmiye'yi kazanmıştır.
Kültür|Berlin Film Festivali'nde Altın Ayı kazanan ilk Türk filmi hangisidir?|Susuz Yaz|Bal|Yol|Kış Uykusu|Sürü|Metin Erksan'ın Susuz Yaz filmi 1964'te Altın Ayı kazanmıştır.
Kültür|1982 Cannes Film Festivali'nde Altın Palmiye kazanan Türk filmi hangisidir?|Yol|Susuz Yaz|Sürü|Umut|Kış Uykusu|Yol 1982'de Altın Palmiye'yi paylaşmıştır.
Kültür|Türkiye'de ilk resmî gazete olan Takvim-i Vekayi hangi yıl yayımlanmıştır?|1831|1860|1840|1876|1908|Takvim-i Vekayi 1831'de yayımlanmıştır.
Kültür|İlk özel Türk gazetesi hangisidir?|Tercüman-ı Ahval|Takvim-i Vekayi|Ceride-i Havadis|Tasvir-i Efkâr|Muhbir|Tercüman-ı Ahval 1860'ta Agâh Efendi ve Şinasi tarafından çıkarılmıştır.
Kültür|İlk Türk kadın savaş pilotu kimdir?|Sabiha Gökçen|Halide Edib Adıvar|Türkan Saylan|Bedriye Tahir Gökmen|Leman Bozkurt|Sabiha Gökçen ilk Türk kadın savaş pilotudur.
Kültür|Türkiye'de ilk televizyon yayını hangi kurum tarafından yapılmıştır?|İstanbul Teknik Üniversitesi|TRT|Anadolu Ajansı|Ankara Radyosu|Türk Telekom|İlk deneme yayını 1952'de İTÜ tarafından yapılmıştır.
Kültür|TRT'nin ilk düzenli televizyon yayını hangi yıl başlamıştır?|1968|1964|1972|1974|1960|TRT Ankara Televizyonu 1968'de yayına başlamıştır.
Kültür|Türk kadınlarına milletvekili seçme ve seçilme hakkı hangi yıl tanınmıştır?|1934|1930|1933|1926|1946|Kadınlara milletvekili seçme ve seçilme hakkı 5 Aralık 1934'te tanınmıştır.
Kültür|Türk kadınlarına belediye seçimlerinde seçme ve seçilme hakkı hangi yıl tanınmıştır?|1930|1934|1926|1933|1924|Kadınlara belediye seçimlerinde hak 1930'da tanınmıştır.
Kültür|İlk Türk matbaasını kuran kişi kimdir?|İbrahim Müteferrika|Kâtip Çelebi|Şinasi|Ahmet Vefik Paşa|Evliya Çelebi|İbrahim Müteferrika 1727'de ilk Türk matbaasını kurmuştur.
Kültür|İstiklal Marşı'nın sözleri kime aittir?|Mehmet Akif Ersoy|Yahya Kemal Beyatlı|Ziya Gökalp|Namık Kemal|Tevfik Fikret|İstiklal Marşı 12 Mart 1921'de kabul edilmiştir; sözleri Mehmet Akif Ersoy'undur.
Dünya|Dünyanın en yüksek dağı hangisidir?|Everest|K2|Kilimanjaro|Aconcagua|Mont Blanc|Everest yaklaşık 8.849 m ile en yüksek dağdır.
Dünya|Dünyanın en büyük okyanusu hangisidir?|Büyük Okyanus (Pasifik)|Atlas Okyanusu|Hint Okyanusu|Güney Okyanusu|Kuzey Buz Denizi|Büyük Okyanus en geniş okyanustur.
Dünya|Dünyanın en büyük sıcak çölü hangisidir?|Sahra|Gobi|Kalahari|Atakama|Arap Çölü|Sahra en büyük sıcak çöldür.
Dünya|Yüzölçümü en büyük ülke hangisidir?|Rusya|Kanada|Çin|ABD|Brezilya|Rusya yüzölçümü en büyük ülkedir.
Dünya|Yüzölçümü en küçük ülke hangisidir?|Vatikan|Monako|San Marino|Lihtenştayn|Malta|Vatikan en küçük bağımsız devlettir.
Dünya|Dünyanın en büyük adası hangisidir?|Grönland|Madagaskar|Borneo|Yeni Gine|Büyük Britanya|Grönland en büyük adadır.
Dünya|Dünyanın en derin gölü hangisidir?|Baykal Gölü|Tanganika Gölü|Hazar Denizi|Victoria Gölü|Van Gölü|Baykal Gölü en derin göldür.
Dünya|Dünyanın en derin noktası hangisidir?|Mariana Çukuru|Tonga Çukuru|Ölü Deniz|Baykal Gölü|Japon Çukuru|Mariana Çukuru okyanusların en derin noktasıdır.
Dünya|Dünyanın en uzun sıradağı hangisidir?|And Dağları|Himalayalar|Alpler|Rocky Dağları|Ural Dağları|And Dağları en uzun kara sıradağıdır.
Dünya|Dünyanın en yüksek şelalesi hangisidir?|Angel Şelalesi|Niagara Şelalesi|Victoria Şelalesi|İguazu Şelalesi|Ren Şelalesi|Venezuela'daki Angel Şelalesi en yüksek şelaledir.
Dünya|Dünyanın en geniş yağmur ormanı hangisidir?|Amazon|Kongo|Borneo|Daintree|Sundarbans|Amazon en geniş tropikal yağmur ormanıdır.
Dünya|Ay'a ayak basan ilk insan kimdir?|Neil Armstrong|Yuri Gagarin|Buzz Aldrin|Valentina Tereşkova|Alan Shepard|Neil Armstrong 1969'da Ay'a ayak basmıştır.
Dünya|Uzaya çıkan ilk insan kimdir?|Yuri Gagarin|Neil Armstrong|Alan Shepard|John Glenn|Valentina Tereşkova|Yuri Gagarin 1961'de uzaya çıkmıştır.
Dünya|Uzaya çıkan ilk kadın kimdir?|Valentina Tereşkova|Sally Ride|Yuri Gagarin|Marie Curie|Svetlana Savitskaya|Valentina Tereşkova 1963'te uzaya çıkmıştır.
Dünya|Dünyanın ilk yapay uydusu hangisidir?|Sputnik 1|Explorer 1|Vostok 1|Apollo 11|Hubble|Sputnik 1 1957'de fırlatılmıştır.
"""

# Türkiye'nin üyelikleri: soru | yıl
UYELIK = """
Türkiye NATO'ya hangi yıl üye olmuştur?|1952
Türkiye Avrupa Konseyi'ne hangi yıl üye olmuştur?|1949
Türkiye ile AB arasındaki Gümrük Birliği hangi yıl yürürlüğe girmiştir?|1996
Türkiye'ye AB adaylık statüsü hangi yıl (Helsinki Zirvesi) tanınmıştır?|1999
Türkiye ile AB arasında katılım müzakereleri hangi yıl başlamıştır?|2005
Türkiye Milletler Cemiyeti'ne hangi yıl üye olmuştur?|1932
Balkan Antantı hangi yıl imzalanmıştır?|1934
Sadabat Paktı hangi yıl imzalanmıştır?|1937
Bağdat Paktı hangi yıl kurulmuştur?|1955
Türkiye IMF'ye hangi yıl üye olmuştur?|1947
Türk Keneşi (bugünkü Türk Devletleri Teşkilatı) Nahçıvan Anlaşması ile hangi yıl kurulmuştur?|2009
Türk Keneşi'nin adı hangi yıl Türk Devletleri Teşkilatı olarak değiştirilmiştir?|2021
"""

# kurum | kuruluş yılı
KURUM_YIL = """
Anadolu Ajansı|1920
Türk Tarih Kurumu|1931
Türk Dil Kurumu|1932
Halkevleri|1932
Türkiye İş Bankası|1924
Diyanet İşleri Başkanlığı|1924
Türk Hava Kurumu (Türk Tayyare Cemiyeti)|1925
Sümerbank|1933
Etibank|1935
Köy Enstitüleri|1940
Ankara Üniversitesi|1946
Millî Kütüphane|1946
Devlet Tiyatroları|1949
Orta Doğu Teknik Üniversitesi|1956
TÜBİTAK|1963
TRT|1964
Anayasa Mahkemesi|1962
TUSAŞ|1973
ASELSAN|1975
Yükseköğretim Kurulu (YÖK)|1981
Atatürk Kültür, Dil ve Tarih Yüksek Kurumu|1983
AFAD|2009
Türkiye Uzay Ajansı|2018
Sayıştay (Divan-ı Muhasebat)|1862
Kızılay (Hilal-i Ahmer'in öncülü)|1868
"""


def _satir(blok, n):
    out = []
    for line in blok.strip().splitlines():
        p = [x.strip() for x in line.split('|')]
        if len(p) != n:
            raise ValueError(f'{n} alan beklenirken: {line}')
        out.append(p)
    return out


def _yillar(y, rng, n=4, aralik=8):
    aday = [y + d for d in range(-aralik, aralik + 1) if d != 0]
    return rng.sample(aday, n)


def uret(rng):
    out = []
    ulk = _satir(ULKELER, 3)
    kay = [(u, b, k) for u, b, k in ulk]
    out += eslesme(rng, 'baskent', [(u, b, 'Dünya') for u, b, _ in kay],
                   lambda a, d: f'{a} ülkesinin başkenti aşağıdakilerden hangisidir?',
                   lambda a, d: f'{d} hangi ülkenin başkentidir?',
                   lambda a, d: f'{a} ülkesinin başkenti {d}’dir.', lambda a, d: f'{d}, {a} ülkesinin başkentidir.', 2,
                   grup=None)
    for u, b, k in kay:
        if k == '-':
            continue
        out.append(q('kita', 'Dünya', f'{u} hangi kıtada yer alır?', k, sec(k, KITALAR, rng),
                     f'{u} {k} kıtasındadır.', 2))
    out += eslesme(rng, 'para', [(u, p, 'Dünya') for u, p in _satir(PARA, 2)],
                   lambda a, d: f'{a} ülkesinin para birimi aşağıdakilerden hangisidir?',
                   lambda a, d: f'Para birimi “{d}” olan ülke aşağıdakilerden hangisidir?',
                   lambda a, d: f'{a} ülkesinin para birimi {d}’dir.', lambda a, d: f'{d}, {a} ülkesinin para birimidir.', 2)
    out += eslesme(rng, 'sehir', [(s, u, 'Dünya') for s, u in _satir(SEHIRLER, 2)],
                   lambda a, d: f'{a} şehri hangi ülkededir?', None,
                   lambda a, d: f'{a} şehri {d} sınırları içindedir.', None, 2)
    out += eslesme(rng, 'yapi', [(y, u, 'Dünya') for y, u in _satir(YAPILAR, 2)],
                   lambda a, d: f'“{a}” hangi ülkededir?',
                   lambda a, d: f'Aşağıdaki yapı ve eserlerden hangisi {d} sınırları içindedir?',
                   lambda a, d: f'{a} {d} sınırları içindedir.', lambda a, d: f'{a} {d} sınırları içindedir.', 2)
    for u, d in _satir(DILLER, 2):
        out.append(q('dil', 'Dünya', f'{u} ülkesinin resmî dili aşağıdakilerden hangisidir?', d, sec(d, DIL_HAVUZ, rng),
                     f'{u} ülkesinin resmî dili {d}’dır.', 2))
    org = _satir(ORGUTLER, 4)
    out += eslesme(rng, 'orgut_merkez', [(a, m, 'Kurumlar') for a, _, m, _ in org],
                   lambda a, d: f'{a} kuruluşunun merkezi hangi şehirdedir?',
                   lambda a, d: f'Aşağıdaki uluslararası kuruluşlardan hangisinin merkezi {d} şehrindedir?',
                   lambda a, d: f'{a} merkezi: {d}.', lambda a, d: f'{a} kuruluşunun merkezi {d} şehrindedir.', 2)
    out += eslesme(rng, 'orgut_ad', [(a, t, 'Kurumlar') for a, t, _, _ in org if a in KISALTMA_SOR],
                   lambda a, d: f'“{a}” kısaltmasıyla bilinen uluslararası kuruluşun Türkçe adı aşağıdakilerden hangisidir?',
                   lambda a, d: f'“{d}” aşağıdaki kısaltmalardan hangisiyle bilinir?',
                   lambda a, d: f'{a} = {d}.', lambda a, d: f'{d} = {a}.', 2)
    for a, t, _, y in org:
        if y != '-':
            out.append(q('orgut_yil', 'Kurumlar', f'{t} ({a}) hangi yıl kurulmuştur?', y, _yillar(int(y), rng),
                         f'{t} {y} yılında kurulmuştur.', 3))
    out += eslesme(rng, 'bakanlik', [(k, b, 'Kurumlar') for k, b in _satir(BAKANLIK, 2)],
                   lambda a, d: f'{a} hangi bakanlığın bağlı ya da ilişkili kuruluşudur?', None,
                   lambda a, d: f'{a}, {d} ile bağlantılıdır.', None, 2)
    for soru, y in _satir(UYELIK, 2):
        out.append(q('uyelik', 'Kurumlar', soru, y, _yillar(int(y), rng), f'Cevap: {y}.', 3))
    for k, y in _satir(KURUM_YIL, 2):
        out.append(q('kurum_yil', 'Kurumlar', f'{k} hangi yıl kurulmuştur?', y, _yillar(int(y), rng),
                     f'{k} {y} yılında kurulmuştur.', 3))
    es = _satir(ESERLER, 3)
    out += eslesme(rng, 'eser', [(e, y, 'Kültür') for e, y, g in es],
                   lambda a, d: f'“{a}” adlı eser kime aittir?',
                   lambda a, d: f'Aşağıdaki eserlerden hangisi {d} tarafından yazılmıştır?',
                   lambda a, d: f'“{a}” {d} tarafından yazılmıştır.', lambda a, d: f'“{a}” {d} tarafından yazılmıştır.', 2,
                   grup=lambda a, d, k: dict((e, g) for e, _, g in es)[a])
    sn = _satir(SANAT, 3)
    out += eslesme(rng, 'sanat', [(e, s, 'Kültür') for e, s, _ in sn],
                   lambda a, d: f'“{a}” adlı eser hangi sanatçıya aittir?',
                   lambda a, d: f'Aşağıdaki eserlerden hangisi {d} imzasını taşır?',
                   lambda a, d: f'“{a}” {d} eseridir.', lambda a, d: f'“{a}” {d} eseridir.', 2,
                   grup=lambda a, d, k: dict((e, g) for e, _, g in sn)[a])
    out += eslesme(rng, 'bulus', [(b, k, 'Kültür') for b, k in _satir(BULUSLAR, 2)],
                   lambda a, d: f'“{a}” aşağıdaki bilim insanlarından hangisiyle özdeşleşmiştir?',
                   lambda a, d: f'{d} aşağıdakilerden hangisiyle tanınır?',
                   lambda a, d: f'{a}: {d}.', lambda a, d: f'{d}: {a}.', 2)
    out += eslesme(rng, 'film', [(f, y, 'Kültür') for f, y in _satir(FILMLER, 2)],
                   lambda a, d: f'“{a}” filminin yönetmeni kimdir?',
                   lambda a, d: f'Aşağıdaki filmlerden hangisi {d} tarafından yönetilmiştir?',
                   lambda a, d: f'“{a}” filmini {d} yönetmiştir.', lambda a, d: f'“{a}” filmini {d} yönetmiştir.', 2)
    for ad, il, y in _satir(UNESCO, 3):
        out.append(q('unesco_il', 'Kültür', f'UNESCO Dünya Mirası Listesi’ndeki “{ad}” hangi ilimizdedir?', il,
                     sec(il, IL_HAVUZ, rng), f'{ad} {il} ilindedir.', 2))
        out.append(q('unesco_yil', 'Kültür', f'“{ad}” UNESCO Dünya Mirası Listesi’ne hangi yıl alınmıştır?', y,
                     _yillar(int(y), rng, aralik=6), f'{ad} {y} yılında listeye alınmıştır.', 3))
    out += eslesme(rng, 'cografi_isaret', [(u, il, 'Kültür') for u, il in _satir(COGRAFI_ISARET, 2)],
                   lambda a, d: f'Coğrafi işaretli “{a}” hangi ilimizle özdeşleşmiştir?', None,
                   lambda a, d: f'{a} {d} iline ait coğrafi işaretli üründür.', None, 2)
    for blok, ad in ((YAZ_OLIMPIYAT, 'Yaz'), (KIS_OLIMPIYAT, 'Kış')):
        rows = _satir(blok, 2)
        sehirler = sorted({s for _, s in rows})
        say = {}
        for _, s in rows:
            say[s] = say.get(s, 0) + 1
        for y, s in rows:
            fiil = 'düzenlenecektir' if int(y) > 2026 else 'düzenlenmiştir'
            out.append(q(f'olimpiyat_{ad.lower()}', 'Spor', f'{y} {ad} Olimpiyat Oyunları hangi şehirde {fiil}?', s,
                         sec(s, sehirler, rng), f'{y} {ad} Olimpiyatları: {s}.', 2))
            if say[s] == 1 and int(y) < 2026:
                yil_havuz = [r[0] for r in rows if r[0] != y]
                out.append(q(f'olimpiyat_{ad.lower()}_yil', 'Spor', f'{s} hangi yıl {ad} Olimpiyat Oyunları’na ev sahipliği yapmıştır?',
                             y, sec(y, yil_havuz, rng), f'{s}, {y} {ad} Olimpiyatları’nın ev sahibidir.', 3))
    for y, ev, sam in _satir(DUNYA_KUPASI, 3):
        zaman = 'düzenlenmiştir'
        out.append(q('dk_ev', 'Spor', f'{y} FIFA Dünya Kupası hangi ülkede {zaman}?', ev, sec(ev, DK_ULKE, rng),
                     f'{y} Dünya Kupası ev sahibi: {ev}.', 2))
        if sam != '-':
            out.append(q('dk_sampiyon', 'Spor', f'{y} FIFA Dünya Kupası’nı hangi ülke kazanmıştır?', sam,
                         sec(sam, [u for u in DK_ULKE if u != 'Güney Kore ve Japonya'], rng), f'{y} şampiyonu: {sam}.', 3))
    for s, b in _satir(SPORCULAR, 2):
        out.append(q('sporcu', 'Spor', f'{s} hangi spor dalında tanınmıştır?', b, sec(b, BRANSLAR, rng),
                     f'{s} {b.lower()} dalında tanınmıştır.', 2))
    for t, b in _satir(TERIMLER, 2):
        out.append(q('terim', 'Spor', f'“{t}” terimi hangi spor dalına aittir?', b, sec(b, TERIM_HAVUZ, rng),
                     f'“{t}” {b} terimidir.', 2))
    for k, soru, d, a, b, c, e, g in _satir(OZEL, 8):
        out.append(q('ozel', k, soru, d, [a, b, c, e], g, 2))
    return out
