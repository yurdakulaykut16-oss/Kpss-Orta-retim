"""Coğrafya bilgi tabloları (elle derlenmiş) ve kodla doğrulanan hesap soruları.

Yön soruları il merkezlerinin yaklaşık koordinatlarıyla kurulur; belirsizliği
önlemek için doğru il en az 1°, çeldiriciler ters yönde en az 0,5° uzakta seçilir.
"""
from .ortak import eslesme, q, sec, sec2

# il | bölge | enlem | boylam | kıyı (K=Karadeniz, M=Marmara, E=Ege, A=Akdeniz, - yok, 2 iki deniz, ? belirsiz)
ILLER = """
Adana|Akdeniz|37.00|35.32|A
Adıyaman|Güneydoğu Anadolu|37.76|38.28|-
Afyonkarahisar|Ege|38.76|30.54|-
Ağrı|Doğu Anadolu|39.72|43.05|-
Amasya|Karadeniz|40.65|35.83|-
Ankara|İç Anadolu|39.93|32.86|-
Antalya|Akdeniz|36.89|30.71|A
Artvin|Karadeniz|41.18|41.82|K
Aydın|Ege|37.85|27.84|E
Balıkesir|Marmara|39.65|27.88|2
Bilecik|Marmara|40.14|29.98|-
Bingöl|Doğu Anadolu|38.88|40.50|-
Bitlis|Doğu Anadolu|38.40|42.11|-
Bolu|Karadeniz|40.74|31.61|-
Burdur|Akdeniz|37.72|30.29|-
Bursa|Marmara|40.19|29.06|M
Çanakkale|Marmara|40.15|26.41|2
Çankırı|İç Anadolu|40.60|33.62|-
Çorum|Karadeniz|40.55|34.95|-
Denizli|Ege|37.78|29.09|-
Diyarbakır|Güneydoğu Anadolu|37.91|40.23|-
Edirne|Marmara|41.68|26.56|E
Elazığ|Doğu Anadolu|38.67|39.22|-
Erzincan|Doğu Anadolu|39.75|39.49|-
Erzurum|Doğu Anadolu|39.90|41.27|-
Eskişehir|İç Anadolu|39.78|30.52|-
Gaziantep|Güneydoğu Anadolu|37.07|37.38|-
Giresun|Karadeniz|40.91|38.39|K
Gümüşhane|Karadeniz|40.46|39.48|-
Hakkari|Doğu Anadolu|37.58|43.74|-
Hatay|Akdeniz|36.20|36.16|A
Isparta|Akdeniz|37.76|30.55|-
Mersin|Akdeniz|36.80|34.63|A
İstanbul|Marmara|41.01|28.98|2
İzmir|Ege|38.42|27.14|E
Kars|Doğu Anadolu|40.60|43.10|-
Kastamonu|Karadeniz|41.38|33.78|K
Kayseri|İç Anadolu|38.72|35.49|-
Kırklareli|Marmara|41.73|27.22|K
Kırşehir|İç Anadolu|39.15|34.16|-
Kocaeli|Marmara|40.77|29.92|2
Konya|İç Anadolu|37.87|32.48|-
Kütahya|Ege|39.42|29.98|-
Malatya|Doğu Anadolu|38.35|38.31|-
Manisa|Ege|38.61|27.43|-
Kahramanmaraş|Akdeniz|37.58|36.94|-
Mardin|Güneydoğu Anadolu|37.31|40.74|-
Muğla|Ege|37.22|28.36|2
Muş|Doğu Anadolu|38.74|41.49|-
Nevşehir|İç Anadolu|38.62|34.71|-
Niğde|İç Anadolu|37.97|34.68|-
Ordu|Karadeniz|40.98|37.88|K
Rize|Karadeniz|41.02|40.52|K
Sakarya|Marmara|40.78|30.40|K
Samsun|Karadeniz|41.29|36.33|K
Siirt|Güneydoğu Anadolu|37.93|41.94|-
Sinop|Karadeniz|42.03|35.15|K
Sivas|İç Anadolu|39.75|37.02|-
Tekirdağ|Marmara|40.98|27.51|2
Tokat|Karadeniz|40.31|36.55|-
Trabzon|Karadeniz|41.00|39.72|K
Tunceli|Doğu Anadolu|39.11|39.55|-
Şanlıurfa|Güneydoğu Anadolu|37.16|38.79|-
Uşak|Ege|38.68|29.41|-
Van|Doğu Anadolu|38.49|43.38|-
Yozgat|İç Anadolu|39.82|34.81|-
Zonguldak|Karadeniz|41.45|31.79|K
Aksaray|İç Anadolu|38.37|34.03|-
Bayburt|Karadeniz|40.26|40.23|-
Karaman|İç Anadolu|37.18|33.22|-
Kırıkkale|İç Anadolu|39.85|33.51|-
Batman|Güneydoğu Anadolu|37.89|41.13|-
Şırnak|Güneydoğu Anadolu|37.52|42.46|-
Bartın|Karadeniz|41.64|32.34|K
Ardahan|Doğu Anadolu|41.11|42.70|-
Iğdır|Doğu Anadolu|39.92|44.04|-
Yalova|Marmara|40.65|29.27|M
Karabük|Karadeniz|41.20|32.62|-
Kilis|Güneydoğu Anadolu|36.72|37.12|-
Osmaniye|Akdeniz|37.07|36.25|?
Düzce|Karadeniz|40.84|31.16|K
"""
DENIZ = {'K': 'Karadeniz', 'M': 'Marmara Denizi', 'E': 'Ege Denizi', 'A': 'Akdeniz', '-': 'Denize kıyısı yoktur'}
KIYI_IKLIM = {  # kıyı ili -> iklim / bitki (yalnız açık durumlar)
    'K': ('Karadeniz iklimi', 'Orman'),
}
AKDENIZ_KIYI = ['Antalya', 'Mersin', 'Adana', 'Hatay', 'İzmir', 'Aydın', 'Muğla']

# Göl | oluşum | konu
GOLLER = """
Tuz Gölü|Tektonik göl
Hazar Gölü|Tektonik göl
Sapanca Gölü|Tektonik göl
İznik Gölü|Tektonik göl
Ulubat Gölü|Tektonik göl
Manyas (Kuş) Gölü|Tektonik göl
Eğirdir Gölü|Tektonik göl
Burdur Gölü|Tektonik göl
Beyşehir Gölü|Tektonik göl
Van Gölü|Volkanik set gölü
Çıldır Gölü|Volkanik set gölü
Balık Gölü|Volkanik set gölü
Nemrut Krater Gölü|Krater gölü
Gölcük Gölü (Isparta)|Krater gölü
Meke Gölü|Krater gölü
Tortum Gölü|Heyelan set gölü
Sera Gölü|Heyelan set gölü
Uzungöl|Heyelan set gölü
Yedigöller|Heyelan set gölü
Bafa Gölü|Alüvyal set gölü
Köyceğiz Gölü|Alüvyal set gölü
Mogan Gölü|Alüvyal set gölü
Eymir Gölü|Alüvyal set gölü
Avlan Gölü|Karstik göl
Suğla Gölü|Karstik göl
Cilo-Sat gölleri|Buzul gölü
"""
GOL_TURLERI = ['Tektonik göl', 'Volkanik set gölü', 'Krater gölü', 'Heyelan set gölü', 'Alüvyal set gölü', 'Karstik göl', 'Buzul gölü']

# yer | il | tür (dağ, ova, göl, milli park, turizm) | konu
YERLER = """
Erciyes Dağı|Kayseri|dağ|Yer Şekilleri
Uludağ|Bursa|dağ|Yer Şekilleri
Süphan Dağı|Bitlis|dağ|Yer Şekilleri
Nemrut Dağı (volkan)|Bitlis|dağ|Yer Şekilleri
Palandöken Dağı|Erzurum|dağ|Yer Şekilleri
Spil Dağı|Manisa|dağ|Yer Şekilleri
Honaz Dağı|Denizli|dağ|Yer Şekilleri
Cudi Dağı|Şırnak|dağ|Yer Şekilleri
Bafra Ovası|Samsun|ova|Yer Şekilleri
Çarşamba Ovası|Samsun|ova|Yer Şekilleri
Menemen Ovası|İzmir|ova|Yer Şekilleri
İnegöl Ovası|Bursa|ova|Yer Şekilleri
Adapazarı Ovası|Sakarya|ova|Yer Şekilleri
Erzurum Ovası|Erzurum|ova|Yer Şekilleri
Pasinler Ovası|Erzurum|ova|Yer Şekilleri
Muş Ovası|Muş|ova|Yer Şekilleri
Iğdır Ovası|Iğdır|ova|Yer Şekilleri
Harran Ovası|Şanlıurfa|ova|Yer Şekilleri
Suruç Ovası|Şanlıurfa|ova|Yer Şekilleri
Amik Ovası|Hatay|ova|Yer Şekilleri
Elbistan Ovası|Kahramanmaraş|ova|Yer Şekilleri
Malatya Ovası|Malatya|ova|Yer Şekilleri
Kazova|Tokat|ova|Yer Şekilleri
Niksar Ovası|Tokat|ova|Yer Şekilleri
Merzifon Ovası|Amasya|ova|Yer Şekilleri
Suluova|Amasya|ova|Yer Şekilleri
Eskişehir Ovası|Eskişehir|ova|Yer Şekilleri
Söke Ovası|Aydın|ova|Yer Şekilleri
Silifke Ovası|Mersin|ova|Yer Şekilleri
Yüksekova|Hakkari|ova|Yer Şekilleri
Develi Ovası|Kayseri|ova|Yer Şekilleri
Hazar Gölü|Elazığ|göl|Su Kaynakları
İznik Gölü|Bursa|göl|Su Kaynakları
Ulubat Gölü|Bursa|göl|Su Kaynakları
Manyas (Kuş) Gölü|Balıkesir|göl|Su Kaynakları
Eğirdir Gölü|Isparta|göl|Su Kaynakları
Balık Gölü|Ağrı|göl|Su Kaynakları
Nemrut Krater Gölü|Bitlis|göl|Su Kaynakları
Tortum Gölü|Erzurum|göl|Su Kaynakları
Uzungöl|Trabzon|göl|Su Kaynakları
Sera Gölü|Trabzon|göl|Su Kaynakları
Abant Gölü|Bolu|göl|Su Kaynakları
Köyceğiz Gölü|Muğla|göl|Su Kaynakları
Mogan Gölü|Ankara|göl|Su Kaynakları
Salda Gölü|Burdur|göl|Su Kaynakları
Meke Gölü|Konya|göl|Su Kaynakları
Yozgat Çamlığı Millî Parkı|Yozgat|millî park|turizm
Kuşcenneti Millî Parkı|Balıkesir|millî park|turizm
Uludağ Millî Parkı|Bursa|millî park|turizm
Göreme Tarihî Millî Parkı|Nevşehir|millî park|turizm
Nemrut Dağı Millî Parkı|Adıyaman|millî park|turizm
Köprülü Kanyon Millî Parkı|Antalya|millî park|turizm
Olimpos-Beydağları Millî Parkı|Antalya|millî park|turizm
Dilek Yarımadası-Büyük Menderes Deltası Millî Parkı|Aydın|millî park|turizm
Altındere Vadisi Millî Parkı|Trabzon|millî park|turizm
Munzur Vadisi Millî Parkı|Tunceli|millî park|turizm
Spil Dağı Millî Parkı|Manisa|millî park|turizm
Kızıldağ Millî Parkı|Isparta|millî park|turizm
Kovada Gölü Millî Parkı|Isparta|millî park|turizm
Truva Tarihî Millî Parkı|Çanakkale|millî park|turizm
Soğuksu Millî Parkı|Ankara|millî park|turizm
Boğazköy-Alacahöyük Millî Parkı|Çorum|millî park|turizm
Malazgirt Meydan Muharebesi Tarihî Millî Parkı|Muş|millî park|turizm
Yedigöller Millî Parkı|Bolu|millî park|turizm
Marmaris Millî Parkı|Muğla|millî park|turizm
Beyşehir Gölü Millî Parkı|Konya|millî park|turizm
Karagöl-Sahara Millî Parkı|Artvin|millî park|turizm
Altınbeşik Mağarası Millî Parkı|Antalya|millî park|turizm
Kazdağı Millî Parkı|Balıkesir|millî park|turizm
Nene Hatun Tarihî Millî Parkı|Erzurum|millî park|turizm
Pamukkale travertenleri|Denizli|turizm|turizm
Hierapolis Antik Kenti|Denizli|turizm|turizm
Laodikya Antik Kenti|Denizli|turizm|turizm
Efes Antik Kenti|İzmir|turizm|turizm
Bergama Akropolü|İzmir|turizm|turizm
Sümela Manastırı|Trabzon|turizm|turizm
Ani Ören Yeri|Kars|turizm|turizm
İshak Paşa Sarayı|Ağrı|turizm|turizm
Safranbolu evleri|Karabük|turizm|turizm
Çatalhöyük Neolitik Kenti|Konya|turizm|turizm
Mevlana Müzesi|Konya|turizm|turizm
Göbeklitepe|Şanlıurfa|turizm|turizm
Balıklıgöl|Şanlıurfa|turizm|turizm
Harran evleri|Şanlıurfa|turizm|turizm
Hattuşa Antik Kenti|Çorum|turizm|turizm
Afrodisias Antik Kenti|Aydın|turizm|turizm
Didim Apollon Tapınağı|Aydın|turizm|turizm
Priene Antik Kenti|Aydın|turizm|turizm
Milet Antik Kenti|Aydın|turizm|turizm
Divriği Ulu Camii ve Darüşşifası|Sivas|turizm|turizm
Selimiye Camii|Edirne|turizm|turizm
Zeugma Mozaik Müzesi|Gaziantep|turizm|turizm
Akdamar Kilisesi|Van|turizm|turizm
Hasankeyf|Batman|turizm|turizm
Aspendos Antik Tiyatrosu|Antalya|turizm|turizm
Perge Antik Kenti|Antalya|turizm|turizm
Side Antik Kenti|Antalya|turizm|turizm
Phaselis Antik Kenti|Antalya|turizm|turizm
Damlataş Mağarası|Antalya|turizm|turizm
Karain Mağarası|Antalya|turizm|turizm
Peribacaları (Ürgüp-Göreme)|Nevşehir|turizm|turizm
Derinkuyu Yeraltı Şehri|Nevşehir|turizm|turizm
Kaymaklı Yeraltı Şehri|Nevşehir|turizm|turizm
Ihlara Vadisi|Aksaray|turizm|turizm
Soğanlı Vadisi|Kayseri|turizm|turizm
Sultan Sazlığı|Kayseri|turizm|turizm
Ayder Yaylası|Rize|turizm|turizm
Sagalassos Antik Kenti|Burdur|turizm|turizm
Aizanoi Antik Kenti|Kütahya|turizm|turizm
Arslantepe Höyüğü|Malatya|turizm|turizm
Gordion Antik Kenti|Ankara|turizm|turizm
Anıtkabir|Ankara|turizm|turizm
Kızkalesi|Mersin|turizm|turizm
Cennet ve Cehennem obrukları|Mersin|turizm|turizm
Ölüdeniz|Muğla|turizm|turizm
Dalyan kaya mezarları|Muğla|turizm|turizm
Knidos Antik Kenti|Muğla|turizm|turizm
Halikarnas Mozolesi|Muğla|turizm|turizm
Ahlat Selçuklu Meydan Mezarlığı|Bitlis|turizm|turizm
Cumalıkızık köyü|Bursa|turizm|turizm
Bursa Ulu Camii|Bursa|turizm|turizm
Ballıca Mağarası|Tokat|turizm|turizm
Hamsilos Koyu|Sinop|turizm|turizm
Assos Antik Kenti|Çanakkale|turizm|turizm
Rumeli Hisarı|İstanbul|turizm|turizm
Topkapı Sarayı|İstanbul|turizm|turizm
"""

# baraj | akarsu
BARAJLAR = """
Atatürk Barajı|Fırat
Keban Barajı|Fırat
Karakaya Barajı|Fırat
Birecik Barajı|Fırat
Karkamış Barajı|Fırat
Ilısu Barajı|Dicle
Kralkızı Barajı|Dicle
Hirfanlı Barajı|Kızılırmak
Kesikköprü Barajı|Kızılırmak
Altınkaya Barajı|Kızılırmak
Derbent Barajı|Kızılırmak
Boyabat Barajı|Kızılırmak
Obruk Barajı|Kızılırmak
Hasan Uğurlu Barajı|Yeşilırmak
Almus Barajı|Yeşilırmak
Sarıyar Barajı|Sakarya
Gökçekaya Barajı|Sakarya
Seyhan Barajı|Seyhan
Çatalan Barajı|Seyhan
Aslantaş Barajı|Ceyhan
Menzelet Barajı|Ceyhan
Sır Barajı|Ceyhan
Berke Barajı|Ceyhan
Oymapınar Barajı|Manavgat
Demirköprü Barajı|Gediz
Adıgüzel Barajı|Büyük Menderes
Deriner Barajı|Çoruh
Yusufeli Barajı|Çoruh
Borçka Barajı|Çoruh
Muratlı Barajı|Çoruh
"""

# akarsu | döküldüğü yer
AKARSULAR = """
Kızılırmak|Karadeniz
Yeşilırmak|Karadeniz
Sakarya Nehri|Karadeniz
Filyos Çayı|Karadeniz
Çoruh Nehri|Karadeniz
Gediz Nehri|Ege Denizi
Büyük Menderes Nehri|Ege Denizi
Küçük Menderes Nehri|Ege Denizi
Bakırçay|Ege Denizi
Meriç Nehri|Ege Denizi
Seyhan Nehri|Akdeniz
Ceyhan Nehri|Akdeniz
Göksu Nehri|Akdeniz
Manavgat Çayı|Akdeniz
Köprüçay|Akdeniz
Dalaman Çayı|Akdeniz
Asi Nehri|Akdeniz
Fırat Nehri|Basra Körfezi
Dicle Nehri|Basra Körfezi
Aras Nehri|Hazar Denizi
Kura Nehri|Hazar Denizi
Susurluk Çayı|Marmara Denizi
Biga Çayı|Marmara Denizi
Gönen Çayı|Marmara Denizi
"""

# yer | maden/kaynak
MADENLER = """
Zonguldak|Taş kömürü
Afşin-Elbistan|Linyit
Soma|Linyit
Divriği|Demir
Hekimhan|Demir
Murgul|Bakır
Ergani|Bakır
Küre|Bakır
Guleman|Krom
Kırka|Bor
Emet|Bor
Bigadiç|Bor
Batman|Petrol
Seydişehir|Boksit
Marmara Adası|Mermer
Eskişehir (Sivrihisar-Mihalıççık)|Lületaşı
Çankırı|Kaya tuzu
Çamaltı (İzmir)|Deniz tuzu
Keban|Kurşun-çinko
Ovacık (Bergama)|Altın
Çöpler (İliç)|Altın
"""

# ürün | doğru il | çeldirici ilin seçileceği bölgeler | konu
URUNLER = """
Çay|Rize|İç Anadolu,Güneydoğu Anadolu,Ege,Akdeniz|Tarım
Fındık|Ordu|İç Anadolu,Güneydoğu Anadolu,Doğu Anadolu,Akdeniz|Tarım
Kayısı|Malatya|Karadeniz,Marmara|Tarım
Antep fıstığı|Gaziantep|Karadeniz,Doğu Anadolu,Marmara|Tarım
Yağ gülü|Isparta|Karadeniz,Doğu Anadolu,Güneydoğu Anadolu|Tarım
Haşhaş|Afyonkarahisar|Doğu Anadolu,Güneydoğu Anadolu|Tarım
İncir|Aydın|Doğu Anadolu,İç Anadolu|Tarım
Muz|Mersin|İç Anadolu,Doğu Anadolu,Karadeniz|Tarım
Turunçgiller|Adana|İç Anadolu,Doğu Anadolu|Tarım
Zeytin|Aydın|İç Anadolu,Doğu Anadolu|Tarım
Pamuk|Şanlıurfa|Karadeniz|Tarım
Kırmızı mercimek|Şanlıurfa|Karadeniz|Tarım
Çekirdeksiz üzüm|Manisa|Karadeniz|Tarım
Ayçiçeği|Tekirdağ|Doğu Anadolu|Tarım
Tiftik keçisi (Ankara keçisi)|Ankara|Karadeniz,Akdeniz,Güneydoğu Anadolu|Hayvancılık
İpek böcekçiliği|Bursa|Doğu Anadolu,Güneydoğu Anadolu|Hayvancılık
"""

# kavram | tanım | konu
KAVRAMLAR = """
Enlem|Herhangi bir noktanın Ekvator'a olan açısal uzaklığı|Koordinat
Boylam|Herhangi bir noktanın başlangıç meridyenine olan açısal uzaklığı|Koordinat
Paralel|Ekvator'a paralel olarak çizildiği varsayılan daireler|Koordinat
Meridyen|Kutuplar arasında uzanan ve yerel saati aynı olan noktaları birleştiren yarım daireler|Koordinat
Yerel saat|Güneş'in gökyüzündeki konumuna göre belirlenen ve her meridyende farklı olan saat|Koordinat
Ortak saat|Bir ülkede ya da saat diliminde kullanılan, belirli bir meridyene göre ayarlanmış saat|Koordinat
Ölçek|Haritadaki uzunluk ile gerçek uzunluk arasındaki oran|Harita
İzohips|Deniz seviyesinden aynı yükseltideki noktaları birleştiren eğriler|Harita
İzobat|Deniz ve göllerde aynı derinlikteki noktaları birleştiren eğriler|Harita
İzobar|Aynı basınçtaki noktaları birleştiren eğriler|Harita
İzoterm|Aynı sıcaklıktaki noktaları birleştiren eğriler|Harita
İzohyet|Aynı miktarda yağış alan noktaları birleştiren eğriler|Harita
Profil|Bir yerin yer şekillerinin düşey kesitini gösteren çizim|Harita
Horst|Kırılma sonucu yükselen blok|İç Kuvvetler
Graben|Kırılma sonucu çöken blok|İç Kuvvetler
Fay|Yer kabuğundaki kırık hattı|İç Kuvvetler
Orojenez|Dağ oluşumu hareketleri|İç Kuvvetler
Epirojenez|Kıta oluşumu, geniş alanların yükselip alçalması hareketleri|İç Kuvvetler
Episantr (dış merkez)|Depremin yer yüzeyinde ilk ve en şiddetli hissedildiği nokta|İç Kuvvetler
Hiposantr (iç merkez)|Depremin yer kabuğu içinde oluştuğu nokta|İç Kuvvetler
Volkanizma|Magmanın yer kabuğunun zayıf yerlerinden yeryüzüne çıkması|İç Kuvvetler
Delta|Akarsuların denize döküldüğü yerde biriktirdiği alüvyonlarla oluşan üçgen biçimli düzlük|Dış Kuvvetler
Kıyı oku|Kıyı akıntılarının taşıdığı malzemeyi bir koyun önünde biriktirmesiyle oluşan dil biçimli şekil|Dış Kuvvetler
Tombolo|Bir adayı kıyıya bağlayan kıyı birikim şekli|Dış Kuvvetler
Lagün|Kıyı okunun koyun önünü kapatmasıyla oluşan göl|Dış Kuvvetler
Falez|Dalgaların aşındırmasıyla oluşan dik kıyı yarı|Dış Kuvvetler
Kanyon|Akarsuların derine aşındırmasıyla oluşan dar ve derin vadi|Dış Kuvvetler
Menderes|Akarsuların eğimin azaldığı düzlüklerde çizdiği büklümler|Dış Kuvvetler
Peribacası|Volkanik tüflerin sel suları ve rüzgârla aşınmasıyla oluşan külah biçimli yer şekli|Dış Kuvvetler
Lapya|Kalkerli arazide suyun eritmesiyle oluşan küçük oluklar|Dış Kuvvetler
Dolin|Karstik arazide erime sonucu oluşan küçük çukurlar|Dış Kuvvetler
Polye|Karstik arazide dolin ve uvalaların birleşmesiyle oluşan geniş tabanlı çukurlar|Dış Kuvvetler
Obruk|Mağara tavanlarının çökmesiyle oluşan derin karstik çukurlar|Dış Kuvvetler
Traverten|Kalsiyum karbonatlı suların yeryüzünde çökeltmesiyle oluşan basamaklı birikim şekli|Dış Kuvvetler
Sarkıt|Mağara tavanından aşağı doğru sarkan kireç birikintisi|Dış Kuvvetler
Dikit|Mağara tabanında yukarı doğru yükselen kireç birikintisi|Dış Kuvvetler
Sirk|Buzulların yüksek dağlarda oluşturduğu çanak biçimli aşınım çukuru|Dış Kuvvetler
Moren|Buzulların taşıyıp biriktirdiği malzeme|Dış Kuvvetler
Barkan|Rüzgârın biriktirdiği hilal biçimli kum tepesi|Dış Kuvvetler
Mantar kaya|Rüzgârın taşıdığı kumların kayaları alttan aşındırmasıyla oluşan şekil|Dış Kuvvetler
Kumul|Rüzgârın biriktirdiği kum tepeleri|Dış Kuvvetler
Heyelan|Eğimli yamaçlardaki toprak ve kaya kütlelerinin kayması|Afetler
Çığ|Eğimli yamaçlarda biriken kar kütlesinin aniden kayması|Afetler
Tsunami|Deniz tabanındaki deprem veya volkanizma sonucu oluşan dev dalgalar|Afetler
Erozyon|Toprağın su ve rüzgâr gibi etkenlerle aşınıp taşınması|Çevre
Debi|Bir akarsuyun belirli bir kesitinden bir saniyede geçen su miktarı|Su Kaynakları
Rejim|Akarsu debisinin yıl içinde gösterdiği değişim|Su Kaynakları
Kapalı havza|Sularını denize ulaştıramayan akarsuların oluşturduğu havza|Su Kaynakları
Ria kıyı|Akarsu vadilerinin sular altında kalmasıyla oluşan girintili kıyı|Yer Şekilleri
Dalmaçya kıyı|Kıyıya paralel uzanan dağların sular altında kalmasıyla oluşan adalı kıyı|Yer Şekilleri
Fiyort|Buzul vadilerinin sular altında kalmasıyla oluşan derin kıyı|Yer Şekilleri
Boyuna kıyı|Dağların kıyıya paralel uzandığı kıyı tipi|Yer Şekilleri
Enine kıyı|Dağların kıyıya dik uzandığı kıyı tipi|Yer Şekilleri
Bağıl nem|Havadaki nem miktarının havanın taşıyabileceği en fazla neme oranı|Türkiye İklimleri
Mutlak nem|Bir metreküp havadaki su buharının gram cinsinden miktarı|Türkiye İklimleri
Muson|Kara ve denizlerin farklı ısınmasıyla oluşan mevsimlik rüzgâr|Türkiye İklimleri
Meltem|Kara ile deniz arasında günlük sıcaklık farkıyla esen rüzgâr|Türkiye İklimleri
Föhn|Dağ yamacından aşağı inerken ısınan kuru ve sıcak rüzgâr|Türkiye İklimleri
Orografik yağış|Nemli havanın dağ yamaçları boyunca yükselerek soğumasıyla oluşan yağış|Türkiye İklimleri
Konveksiyonel yağış|Isınan nemli havanın yükselip soğumasıyla oluşan yağış|Türkiye İklimleri
Cephesel yağış|Sıcak ve soğuk hava kütlelerinin karşılaşmasıyla oluşan yağış|Türkiye İklimleri
Kırağı|Su buharının soğuk yüzeylerde donarak buz kristalleri oluşturması|Türkiye İklimleri
Çiy|Su buharının soğuk yüzeylerde yoğunlaşarak su damlacıklarına dönüşmesi|Türkiye İklimleri
Kırç|Sisli havada su damlacıklarının ağaç dallarında donmasıyla oluşan buz tabakası|Türkiye İklimleri
Maki|Akdeniz ikliminde ormanların tahrip edilmesiyle oluşan, yaz kuraklığına dayanıklı çalı topluluğu|iklim_bitki_orfu
Garig|Makilerin tahrip edildiği alanlarda gelişen seyrek ve bodur bitki topluluğu|iklim_bitki_orfu
Bozkır (step)|İlkbahar yağışlarıyla yeşerip yazın kuruyan cılız ot toplulukları|iklim_bitki_orfu
Tundra|Kutup çevresinde kısa yazda yeşeren yosun ve likenlerden oluşan bitki örtüsü|iklim_bitki_orfu
Savan|Tropikal bölgelerde yağışlı dönemde boy atan uzun otlar|iklim_bitki_orfu
Tayga|Soğuk iklimlerde görülen iğne yapraklı orman kuşağı|iklim_bitki_orfu
Aritmetik nüfus yoğunluğu|Toplam nüfusun yüzölçümüne bölünmesiyle bulunan değer|Nüfus
Fizyolojik nüfus yoğunluğu|Toplam nüfusun tarım alanlarına bölünmesiyle bulunan değer|Nüfus
Tarımsal nüfus yoğunluğu|Tarımla geçinen nüfusun tarım alanlarına bölünmesiyle bulunan değer|Nüfus
Doğal nüfus artışı|Doğum ve ölüm oranları arasındaki fark|Nüfus
Beyin göçü|Nitelikli ve eğitimli insanların başka ülkelere göç etmesi|Göç
Mevsimlik göç|Tarım, turizm gibi işler için yılın belirli dönemlerinde yapılan geçici göç|Göç
Şehirleşme|Kır nüfusunun şehirlere göç etmesiyle şehir nüfusu oranının artması|Şehirleşme
Nadas|Toprağın verimini artırmak için tarlanın bir yıl ekilmeden bırakılması|Tarım
Seracılık|Örtü altında sıcaklık kontrol edilerek yapılan tarım|Tarım
Ekstansif tarım|Doğal koşullara bağlı, verimin düşük olduğu ilkel tarım|Tarım
Entansif tarım|Makine, gübre ve sulama kullanılarak yapılan modern tarım|Tarım
Mera|Hayvanların otlatıldığı doğal çayır alanları|Hayvancılık
Yayla|Yaz aylarında hayvancılık için çıkılan yüksek otlak yerleşmesi|nufus_yerlesme
Kom|Doğu Anadolu'da hayvancılıkla uğraşan ailelerin yaşadığı kır yerleşmesi|nufus_yerlesme
Mezra|Köyden uzakta tarım yapılan yerde kurulan geçici yerleşme|nufus_yerlesme
Oba|Göçebelerin çadırlardan oluşan geçici yerleşmesi|nufus_yerlesme
Divan|Karadeniz'de birkaç evin bir araya gelmesiyle oluşan köyaltı yerleşme|nufus_yerlesme
Yenilenebilir enerji|Güneş, rüzgâr, su gibi tükenmeyen kaynaklardan elde edilen enerji|Enerji
Jeotermal enerji|Yer altındaki sıcak su ve buhardan elde edilen enerji|Enerji
Hidroelektrik|Akan ya da düşen suyun gücünden elde edilen elektrik|Enerji
Transit ticaret|Bir ülkenin topraklarından başka ülkeler arasında yapılan mal geçişi|dis_ticaret
Dış ticaret açığı|İthalatın ihracattan fazla olması durumu|dis_ticaret
Kabotaj|Bir ülkenin kendi limanları arasında deniz taşımacılığı yapma hakkı|ulasim
"""


def _satir(blok, n):
    return [[x.strip() for x in l.split('|')] for l in blok.strip().splitlines() if l.strip()]


def iller():
    return [(a, b, float(c), float(d), k) for a, b, c, d, k in _satir(ILLER, 5)]


def _sayi(n):
    s = f'{n:,}'.replace(',', '.')
    return s


def uret(rng):
    out = []
    il = iller()
    ad = [x[0] for x in il]
    bolge = {x[0]: x[1] for x in il}
    # 1) il -> bölge, aynı bölge
    bolgeler = sorted({x[1] for x in il})
    for a, b, la, lo, k in il:
        out.append(q('il_bolge', 'Bölgeler', f'{a} ili hangi coğrafi bölgemizde yer alır?', f'{b} Bölgesi',
                     sec(f'{b} Bölgesi', [f'{x} Bölgesi' for x in bolgeler], rng),
                     f'{a}, {b} Bölgesi illerindendir.', 2))
        ayni = [x[0] for x in il if x[1] == b and x[0] != a]
        diger = [x[0] for x in il if x[1] != b]
        if ayni:
            d = rng.choice(ayni)
            out.append(q('ayni_bolge', 'Bölgeler', f'Aşağıdaki illerden hangisi {a} ile aynı coğrafi bölgededir?', d,
                         sec(d, diger, rng), f'{a} ve {d} {b} Bölgesi’ndedir; diğer iller başka bölgelerdedir.', 2))
        if k in DENIZ:
            dogru = DENIZ[k]
            out.append(q('kiyi', 'Bölgeler', f'{a} ilinin hangi denize kıyısı vardır?', dogru,
                         [v for kk, v in DENIZ.items() if kk != k],
                         f'{a}: {dogru}.' if k != '-' else f'{a} ilinin denize kıyısı yoktur.', 2))
    # 2) yön, Güneş, gölge, gündüz süresi, yerel saat
    sablon = [
        ('dogu', 'Aşağıdaki illerden hangisi {a} iline göre daha doğudadır?', 'lo', +1, 'boylamı daha büyük (doğuda)'),
        ('bati', 'Aşağıdaki illerden hangisi {a} iline göre daha batıdadır?', 'lo', -1, 'boylamı daha küçük (batıda)'),
        ('kuzey', 'Aşağıdaki illerden hangisi {a} iline göre daha kuzeydedir?', 'la', +1, 'enlemi daha büyük (kuzeyde)'),
        ('guney', 'Aşağıdaki illerden hangisi {a} iline göre daha güneydedir?', 'la', -1, 'enlemi daha küçük (güneyde)'),
        ('gunes', 'Aşağıdaki illerin hangisinde Güneş, {a} iline göre daha önce doğar?', 'lo', +1,
         'daha doğuda olduğu için Güneş orada daha önce doğar'),
        ('saat', 'Aşağıdaki illerden hangisinin yerel saati {a} ilinin yerel saatinden daha ileridir?', 'lo', +1,
         'daha doğuda olduğu için yerel saati daha ileridir'),
        ('golge', 'Aşağıdaki illerin hangisinde öğle vakti cisimlerin gölge boyu, aynı gün {a} iline göre daha kısadır?', 'la', -1,
         'daha güneyde olduğu için Güneş ışınları öğle vakti daha dik açıyla gelir ve gölge daha kısa olur'),
        ('gunduz', 'Aşağıdaki illerin hangisinde 21 Haziran günü gündüz süresi {a} iline göre daha uzundur?', 'la', +1,
         'daha kuzeyde olduğu için 21 Haziran’da (Kuzey Yarım Küre’de yaz gün dönümü) gündüz daha uzundur'),
    ]
    for a, b, la, lo, k in il:
        for tur, kok, eksen, yon, acik in sablon:
            v = la if eksen == 'la' else lo
            dogrular = [x for x in il if x[0] != a and ((x[2] if eksen == 'la' else x[3]) - v) * yon >= 1.0]
            yanlis = [x for x in il if x[0] != a and ((x[2] if eksen == 'la' else x[3]) - v) * yon <= -0.5]
            if not dogrular or len(yanlis) < 4:
                continue
            d = rng.choice(dogrular)
            yy = rng.sample(yanlis, 4)
            out.append(q(tur, 'Koordinat', kok.format(a=a), d[0], [x[0] for x in yy],
                         f'{d[0]}, {a} iline göre {acik}. Diğer seçenekler {a} ilinin ters yönündedir.', 3))
    # 3) iklim / bitki örtüsü
    for a, b, la, lo, k in il:
        if k == 'K' and b == 'Karadeniz':
            out.append(q('iklim', 'Türkiye İklimleri', f'{a} ilinin kıyı kesiminde hangi iklim tipi görülür?', 'Karadeniz iklimi',
                         ['Akdeniz iklimi', 'Karasal iklim', 'Muson iklimi', 'Çöl iklimi'],
                         f'{a} Karadeniz kıyısındadır; her mevsim yağışlı Karadeniz iklimi görülür.', 2))
            out.append(q('bitki', 'iklim_bitki_orfu', f'{a} ilinin kıyı kesimindeki doğal bitki örtüsü hangisidir?', 'Orman',
                         ['Maki', 'Bozkır (step)', 'Tundra', 'Savan'],
                         f'{a} Karadeniz ikliminin etkisindedir; doğal bitki örtüsü ormandır.', 2))
        if a in AKDENIZ_KIYI:
            out.append(q('iklim', 'Türkiye İklimleri', f'{a} ilinin kıyı kesiminde hangi iklim tipi görülür?', 'Akdeniz iklimi',
                         ['Karadeniz iklimi', 'Karasal iklim', 'Muson iklimi', 'Okyanusal iklim'],
                         f'{a} kıyılarında yazları sıcak ve kurak, kışları ılık ve yağışlı Akdeniz iklimi görülür.', 2))
            out.append(q('bitki', 'iklim_bitki_orfu', f'{a} ilinin kıyı kesimindeki doğal bitki örtüsü hangisidir?', 'Maki',
                         ['Bozkır (step)', 'Tundra', 'Savan', 'Tayga'],
                         f'{a} kıyıları Akdeniz iklimindedir; doğal bitki örtüsü makidir.', 2))
        if b == 'İç Anadolu':
            out.append(q('iklim', 'Türkiye İklimleri', f'{a} ilinde hangi iklim tipi görülür?', 'Karasal iklim',
                         ['Karadeniz iklimi', 'Akdeniz iklimi', 'Muson iklimi', 'Okyanusal iklim'],
                         f'{a} İç Anadolu’dadır; yazları sıcak ve kurak, kışları soğuk karasal iklim görülür.', 2))
            out.append(q('bitki', 'iklim_bitki_orfu', f'{a} ilinde yaygın doğal bitki örtüsü hangisidir?', 'Bozkır (step)',
                         ['Maki', 'Tundra', 'Savan', 'Tropikal yağmur ormanı'],
                         f'{a} İç Anadolu’da karasal iklimdedir; doğal bitki örtüsü bozkırdır.', 2))
    # 4) göl oluşumu
    for g, t in _satir(GOLLER, 2):
        out.append(q('gol_olusum', 'Su Kaynakları', f'{g} oluşumu bakımından hangi göl türüne girer?', t,
                     sec(t, GOL_TURLERI, rng), f'{g}: {t}.', 3))
    # 5) yer -> il ve il -> yer
    yer = _satir(YERLER, 4)
    tur_ad = {'dağ': 'dağ', 'ova': 'ova', 'göl': 'göl', 'millî park': 'millî park', 'turizm': 'turistik yer'}
    for y, i, t, konu in yer:
        ayni_tur = [x for x in yer if x[2] == t]
        il_havuz = [x[1] for x in ayni_tur if x[1] != i] + [x for x in ad if x != i]
        out.append(q('yer_il_' + t, konu, f'{y} hangi ilimizde bulunur?', i,
                     sec2(i, [x[1] for x in ayni_tur if x[1] != i], [x for x in ad if x != i], rng),
                     f'{y} {i} ilindedir.', 2))
        ayni_il = {x[0] for x in ayni_tur if x[1] == i}
        havuz = [x[0] for x in ayni_tur if x[0] not in ayni_il]
        out.append(q('il_yer_' + t, konu, f'Aşağıdaki {tur_ad[t]} örneklerinden hangisi {i} ilinde bulunur?', y,
                     sec(y, havuz, rng), f'{y} {i} ilindedir; diğerleri başka illerdedir.', 2))
    # 6) baraj -> akarsu
    bar = _satir(BARAJLAR, 2)
    nehirler = sorted({x[1] for x in bar})
    for b, n in bar:
        out.append(q('baraj', 'Su Kaynakları', f'{b} hangi akarsu üzerinde kurulmuştur?', n, sec(n, nehirler, rng),
                     f'{b} {n} üzerindedir.', 2))
    # 7) akarsu -> döküldüğü yer
    ak = _satir(AKARSULAR, 2)
    yerler = sorted({x[1] for x in ak})
    for a, d in ak:
        out.append(q('akarsu', 'Su Kaynakları', f'{a} hangi denize ya da körfeze dökülür?', d, sec(d, yerler, rng),
                     f'{a} {d}’ne dökülür.' if not d.endswith('i') else f'{a} {d}’ne dökülür.', 2))
        ayni = [x[0] for x in ak if x[1] == d and x[0] != a]
        if ayni:
            dd = rng.choice(ayni)
            out.append(q('akarsu_ayni', 'Su Kaynakları', f'Aşağıdaki akarsulardan hangisi {a} ile aynı denize ya da körfeze dökülür?',
                         dd, sec(dd, [x[0] for x in ak if x[1] != d], rng), f'{a} ve {dd} {d} havzasına dökülür.', 3))
    # 8) madenler
    mad = [(a, d, 'Madenler') for a, d in _satir(MADENLER, 2)]
    out += eslesme(rng, 'maden', mad,
                   lambda a, d: f'{a} yöresi hangi maden ya da kaynak ile öne çıkar?',
                   lambda a, d: f'{d} çıkarılmasıyla öne çıkan yer aşağıdakilerden hangisidir?',
                   lambda a, d: f'{a}: {d}.', lambda a, d: f'{d}: {a}.', 2)
    # 9) ürünler
    for u, i, bol, konu in _satir(URUNLER, 4):
        izin = bol.split(',')
        havuz = [x[0] for x in il if x[1] in izin]
        out.append(q('urun', konu, f'{u} üretimiyle öne çıkan il aşağıdakilerden hangisidir?', i, sec(i, havuz, rng),
                     f'{u} üretiminde {i} öne çıkar; diğer seçeneklerdeki iller bu üründe öne çıkmaz.', 2))
    # 10) kavramlar
    kav = [tuple(x) for x in _satir(KAVRAMLAR, 3)]
    out += eslesme(rng, 'kavram', kav,
                   lambda a, d: f'Coğrafyada “{a}” kavramı aşağıdakilerden hangisini ifade eder?',
                   lambda a, d: f'“{d}” aşağıdaki kavramlardan hangisiyle açıklanır?',
                   lambda a, d: f'{a}: {d}.', lambda a, d: f'{d} = {a}.', 2, grup=lambda a, d, k: k)
    # 11) ölçek hesapları
    olcekler = [20000, 50000, 100000, 200000, 250000, 500000, 1000000, 2000000, 4000000]
    for o in olcekler:
        for cm in (2, 3, 4, 5, 6, 8, 12):
            km = cm * o / 100000
            if km != int(km) and km * 10 != int(km * 10):
                continue
            ks = lambda x: (f'{x:g}'.replace('.', ',')) + ' km'
            dogru = ks(km)
            yan = [ks(km * 10), ks(km / 10), ks(km * 2), ks(km / 2), ks(km * 100)]
            out.append(q('olcek_km', 'Harita', f'1/{_sayi(o)} ölçekli bir haritada {cm} cm olarak gösterilen uzaklık gerçekte kaç km’dir?',
                         dogru, sec(dogru, yan, rng), f'{cm} cm × {_sayi(o)} = {_sayi(cm * o)} cm = {ks(km)}.', 3))
            out.append(q('olcek_cm', 'Harita', f'Gerçekte {ks(km)} olan bir uzaklık 1/{_sayi(o)} ölçekli haritada kaç cm ile gösterilir?',
                         f'{cm} cm', sec(f'{cm} cm', [f'{x:g} cm'.replace('.', ',') for x in (cm * 10, cm / 10, cm * 2, cm / 2, cm * 100, cm + 1)], rng),
                         f'{ks(km)} = {_sayi(cm * o)} cm; {_sayi(cm * o)} / {_sayi(o)} = {cm} cm.', 3))
    # 12) yerel saat farkı (Türkiye boylamları 26°–45° D)
    bo = list(range(26, 46))
    ciftler = [(x, y) for x in bo for y in bo if y - x >= 3]
    rng.shuffle(ciftler)
    for x, y in ciftler[:70]:
        fark = (y - x) * 4
        yan = [f'{v} dakika' for v in (fark + 4, fark - 4, (y - x) * 15, fark * 2, fark + 8) if v > 0 and v != fark]
        out.append(q('saat_farki', 'Koordinat', f'{x}° doğu ve {y}° doğu meridyenleri arasındaki yerel saat farkı kaç dakikadır?',
                     f'{fark} dakika', sec(f'{fark} dakika', yan, rng), f'Her 1° boylam farkı 4 dakikadır: ({y}−{x}) × 4 = {fark} dakika.', 3))
    rng.shuffle(ciftler)
    for x, y in ciftler[:70]:
        fark = (y - x) * 4
        hh = 12 * 60 + fark
        dogru = f'{hh // 60:02d}.{hh % 60:02d}'
        ters = 12 * 60 - fark
        yan = [f'{t // 60:02d}.{t % 60:02d}' for t in (ters, hh + 4, hh - 4, 12 * 60 + (y - x) * 15, hh + 60) if t != hh]
        out.append(q('yerel_saat', 'Koordinat', f'{x}° doğu meridyeninde yerel saat 12.00 iken {y}° doğu meridyeninde yerel saat kaçtır?',
                     dogru, sec(dogru, yan, rng),
                     f'{y}° D daha doğudadır; fark ({y}−{x}) × 4 = {fark} dakika ileri: 12.00 + {fark} dk = {dogru}.', 3))
    # 13) Güneş ışınlarının öğle açısı
    for e in [36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42]:
        es = f'{e:g}'.replace('.', ',')
        for tarih, dek, ac in (('21 Haziran', 23.5, 'yaz gün dönümünde Güneş ışınları Yengeç Dönencesi’ne (23°27′ ≈ 23,5° K) dik gelir'),
                               ('21 Aralık', -23.5, 'kış gün dönümünde Güneş ışınları Oğlak Dönencesi’ne (23,5° G) dik gelir'),
                               ('21 Mart', 0, 'ekinoksta Güneş ışınları Ekvator’a dik gelir')):
            aci = 90 - (e - dek)
            formul = {23.5: '+ 23,5°', -23.5: '− 23,5°', 0: '(sapma yok)'}[dek]
            f = lambda v: f'{v:g}°'.replace('.', ',')
            dogru = f(aci)
            yan = [f(v) for v in (aci + 23.5, aci - 23.5, aci + 47, aci - 47, 90 - e, e, aci + 10) if 0 < v <= 90 and f(v) != dogru]
            out.append(q('gunes_acisi', 'Koordinat',
                         f'{es}° kuzey enlemindeki bir yerde {tarih} günü öğle vakti Güneş ışınlarının geliş açısı kaç derecedir?',
                         dogru, sec(dogru, yan, rng), f'{tarih}: {ac}. Açı = 90° − {es}° {formul} = {dogru}.', 3))
    return out
