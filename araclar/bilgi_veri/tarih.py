"""Tarih bilgi tabloları (elle derlenmiş; yalnız ders kitaplarında yaygın kabul gören bilgiler)."""
from .ortak import eslesme, q, sec, yuzyil, yy_ad

# yıl | olay | konu | dönem hükümdarı (O: Osmanlı padişahı, S: Selçuklu sultanı)
OLAYLAR = """
375|Kavimler Göçü'nün başlaması|İlk Türk Devletleri|
453|Attila'nın ölümü|İlk Türk Devletleri|
552|I. Göktürk Devleti'nin kurulması|Göktürkler|
582|Göktürklerin Doğu ve Batı olarak ikiye ayrılması|Göktürkler|
630|Doğu Göktürklerin Çin egemenliğine girmesi|Göktürkler|
682|II. Göktürk (Kutluk) Devleti'nin kurulması|Göktürkler|
732|Kül Tigin Yazıtı'nın dikilmesi|Göktürkler|
735|Bilge Kağan Yazıtı'nın dikilmesi|Göktürkler|
751|Talas Savaşı|İlk Türk Devletleri|
840|Kırgızların Uygur Devleti'ni yıkması|Uygurlar|
963|Gazneli Devleti'nin kurulması|Gazneliler|
1040|Dandanakan Savaşı|Selçuklu|S:Tuğrul Bey
1048|Pasinler Savaşı|Selçuklu|S:Tuğrul Bey
1055|Tuğrul Bey'in Bağdat'a girmesi|Selçuklu|S:Tuğrul Bey
1071|Malazgirt Savaşı|Selçuklu|S:Alparslan
1075|Türkiye Selçuklu Devleti'nin kurulması|Anadolu Selçuklu|
1092|Melikşah'ın ölümü|Selçuklu|
1096|I. Haçlı Seferi'nin başlaması|Anadolu Selçuklu|S:I. Kılıç Arslan
1141|Katvan Savaşı|Selçuklu|S:Sultan Sencer
1157|Büyük Selçuklu Devleti'nin yıkılması|Selçuklu|
1176|Miryokefalon Savaşı|Anadolu Selçuklu|S:II. Kılıç Arslan
1187|Hıttin Savaşı|Türk-İslam Kültürü|
1207|Antalya'nın fethi|Anadolu Selçuklu|S:I. Gıyaseddin Keyhüsrev
1214|Sinop'un fethi|Anadolu Selçuklu|S:I. İzzeddin Keykavus
1230|Yassıçemen Savaşı|Anadolu Selçuklu|S:I. Alaeddin Keykubat
1240|Babai Ayaklanması|Anadolu Selçuklu|S:II. Gıyaseddin Keyhüsrev
1243|Kösedağ Savaşı|Anadolu Selçuklu|S:II. Gıyaseddin Keyhüsrev
1258|Moğolların Bağdat'ı alarak Abbasi Halifeliğine son vermesi|Türk-İslam Kültürü|
1260|Ayn Calut Savaşı|Türk-İslam Kültürü|
1277|Karamanoğlu Mehmet Bey'in Türkçeyi resmî dil ilan etmesi|Beylikler|
1299|Osmanlı Devleti'nin kurulması|Osmanlı Kuruluş|O:Osman Bey
1302|Koyunhisar (Bafeus) Savaşı|Osmanlı Kuruluş|O:Osman Bey
1308|Türkiye Selçuklu Devleti'nin yıkılması|Anadolu Selçuklu|
1326|Bursa'nın fethi|Osmanlı Kuruluş|O:Orhan Bey
1329|Maltepe (Palekanon) Savaşı|Osmanlı Kuruluş|O:Orhan Bey
1331|İznik'in fethi|Osmanlı Kuruluş|O:Orhan Bey
1337|İzmit'in fethi|Osmanlı Kuruluş|O:Orhan Bey
1345|Karesi Beyliği'nin Osmanlı topraklarına katılması|Osmanlı Kuruluş|O:Orhan Bey
1353|Çimpe Kalesi'nin alınması|Osmanlı Kuruluş|O:Orhan Bey
1364|Sırpsındığı Savaşı|Osmanlı Kuruluş|O:I. Murat
1371|Çirmen Savaşı|Osmanlı Kuruluş|O:I. Murat
1389|I. Kosova Savaşı|Osmanlı Kuruluş|O:I. Murat
1396|Niğbolu Savaşı|Osmanlı Kuruluş|O:Yıldırım Bayezid
1402|Ankara Savaşı|Osmanlı Kuruluş|O:Yıldırım Bayezid
1413|Fetret Devri'nin sona ermesi|Osmanlı Kuruluş|O:Çelebi Mehmet
1416|Şeyh Bedrettin İsyanı|Osmanlı Kuruluş|O:Çelebi Mehmet
1444|Varna Savaşı|Osmanlı Kuruluş|O:II. Murat
1448|II. Kosova Savaşı|Osmanlı Kuruluş|O:II. Murat
1453|İstanbul'un fethi|Fatih Dönemi|O:Fatih Sultan Mehmet
1456|Belgrad Kuşatması (Fatih dönemi)|Fatih Dönemi|O:Fatih Sultan Mehmet
1461|Trabzon Rum İmparatorluğu'na son verilmesi|Fatih Dönemi|O:Fatih Sultan Mehmet
1463|Bosna'nın fethi|Fatih Dönemi|O:Fatih Sultan Mehmet
1473|Otlukbeli Savaşı|Fatih Dönemi|O:Fatih Sultan Mehmet
1475|Kırım'ın Osmanlı'ya bağlanması|Fatih Dönemi|O:Fatih Sultan Mehmet
1479|Venedik ile İstanbul Antlaşması|Fatih Dönemi|O:Fatih Sultan Mehmet
1480|Otranto'nun alınması|Fatih Dönemi|O:Fatih Sultan Mehmet
1484|Kili ve Akkerman'ın alınması|Fatih Dönemi|O:II. Bayezid
1492|Amerika kıtasının keşfi|Kanuni Dönemi|
1498|Vasco da Gama'nın Ümit Burnu yoluyla Hindistan'a ulaşması|Kanuni Dönemi|
1514|Çaldıran Savaşı|Kanuni Dönemi|O:Yavuz Sultan Selim
1515|Turnadağ Savaşı|Kanuni Dönemi|O:Yavuz Sultan Selim
1516|Mercidabık Savaşı|Kanuni Dönemi|O:Yavuz Sultan Selim
1517|Ridaniye Savaşı|Kanuni Dönemi|O:Yavuz Sultan Selim
1521|Belgrad'ın fethi|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1522|Rodos'un fethi|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1526|Mohaç Meydan Savaşı|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1529|I. Viyana Kuşatması|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1533|Avusturya ile İstanbul Antlaşması|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1538|Preveze Deniz Savaşı|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1555|Amasya Antlaşması|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1560|Cerbe Deniz Savaşı|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1566|Zigetvar Seferi|Kanuni Dönemi|O:Kanuni Sultan Süleyman
1569|Astrahan Seferi|Kanuni Dönemi|O:II. Selim
1571|Kıbrıs'ın fethi|Kanuni Dönemi|O:II. Selim
1574|Tunus'un fethi|Kanuni Dönemi|O:II. Selim
1590|Ferhat Paşa Antlaşması|Duraklama|O:III. Murat
1606|Zitvatorok Antlaşması|Duraklama|O:I. Ahmet
1612|Nasuh Paşa Antlaşması|Duraklama|O:I. Ahmet
1621|Hotin Seferi|Duraklama|O:II. Osman
1622|II. Osman'ın öldürülmesi (Haile-i Osmaniye)|Duraklama|
1638|Bağdat'ın fethi|Duraklama|O:IV. Murat
1639|Kasr-ı Şirin Antlaşması|Duraklama|O:IV. Murat
1669|Girit'in fethi|Duraklama|O:IV. Mehmet
1672|Bucaş Antlaşması|Duraklama|O:IV. Mehmet
1683|II. Viyana Kuşatması|Duraklama|O:IV. Mehmet
1699|Karlofça Antlaşması|Duraklama|O:II. Mustafa
1700|Rusya ile İstanbul Antlaşması|Duraklama|O:II. Mustafa
1711|Prut Savaşı|Lale Devri|O:III. Ahmet
1718|Pasarofça Antlaşması|Lale Devri|O:III. Ahmet
1727|İbrahim Müteferrika matbaasının kurulması|Lale Devri|O:III. Ahmet
1730|Patrona Halil İsyanı|Lale Devri|O:III. Ahmet
1739|Belgrad Antlaşması|Islahatlar|O:I. Mahmut
1770|Çeşme Baskını|Islahatlar|O:III. Mustafa
1774|Küçük Kaynarca Antlaşması|Islahatlar|O:I. Abdülhamit
1783|Kırım'ın Rusya tarafından ilhakı|Islahatlar|O:I. Abdülhamit
1789|Fransız İhtilali|Islahatlar|
1791|Ziştovi Antlaşması|Islahatlar|O:III. Selim
1792|Yaş Antlaşması|Islahatlar|O:III. Selim
1793|Nizam-ı Cedit ordusunun kurulması|Islahatlar|O:III. Selim
1798|Napolyon'un Mısır'ı işgali|Islahatlar|O:III. Selim
1807|Kabakçı Mustafa İsyanı|Islahatlar|O:III. Selim
1808|Sened-i İttifak'ın imzalanması|Islahatlar|O:II. Mahmut
1812|Bükreş Antlaşması|Islahatlar|O:II. Mahmut
1821|Mora İsyanı|Islahatlar|O:II. Mahmut
1826|Yeniçeri Ocağı'nın kaldırılması (Vaka-i Hayriye)|Islahatlar|O:II. Mahmut
1827|Navarin Baskını|Islahatlar|O:II. Mahmut
1829|Edirne Antlaşması|Islahatlar|O:II. Mahmut
1830|Yunanistan'ın bağımsızlığını kazanması|Islahatlar|O:II. Mahmut
1831|Osmanlı'da ilk nüfus sayımının yapılması|Islahatlar|O:II. Mahmut
1833|Hünkâr İskelesi Antlaşması|Islahatlar|O:II. Mahmut
1838|Balta Limanı Ticaret Antlaşması|Islahatlar|O:II. Mahmut
1839|Tanzimat Fermanı'nın ilanı|Tanzimat|O:Abdülmecit
1840|Mısır sorununa ilişkin Londra Antlaşması|Tanzimat|O:Abdülmecit
1841|Londra Boğazlar Sözleşmesi|Tanzimat|O:Abdülmecit
1853|Kırım Savaşı'nın başlaması|Tanzimat|O:Abdülmecit
1854|Osmanlı Devleti'nin ilk dış borcu alması|Tanzimat|O:Abdülmecit
1856|Islahat Fermanı'nın ilanı|Tanzimat|O:Abdülmecit
1859|Kuleli Vakası|Tanzimat|O:Abdülmecit
1860|Tercüman-ı Ahval gazetesinin yayımlanması|Tanzimat|O:Abdülmecit
1865|Genç Osmanlılar (Yeni Osmanlılar) Cemiyeti'nin kurulması|Tanzimat|O:Abdülaziz
1869|Süveyş Kanalı'nın açılması|Tanzimat|O:Abdülaziz
1875|Ramazan Kararnamesi'nin yayımlanması|Tanzimat|O:Abdülaziz
1876|I. Meşrutiyet'in ilanı|Meşrutiyet|O:II. Abdülhamit
1877|93 Harbi'nin (Osmanlı-Rus Savaşı) başlaması|Meşrutiyet|O:II. Abdülhamit
1881|Duyun-u Umumiye İdaresi'nin kurulması|Meşrutiyet|O:II. Abdülhamit
1882|İngiltere'nin Mısır'ı işgali|Meşrutiyet|O:II. Abdülhamit
1889|İttihat ve Terakki Cemiyeti'nin kurulması|Meşrutiyet|O:II. Abdülhamit
1897|Osmanlı-Yunan (Dömeke) Savaşı|Meşrutiyet|O:II. Abdülhamit
1908|II. Meşrutiyet'in ilanı|Meşrutiyet|O:II. Abdülhamit
1909|31 Mart Olayı|Meşrutiyet|
1911|Trablusgarp Savaşı'nın başlaması|Trablusgarp|O:V. Mehmet Reşat
1912|Uşi Antlaşması|Trablusgarp|O:V. Mehmet Reşat
1913|Bab-ı Ali Baskını|Balkan Savaşları|O:V. Mehmet Reşat
1914|Osmanlı Devleti'nin I. Dünya Savaşı'na girmesi|I. Dünya Savaşı|O:V. Mehmet Reşat
1915|18 Mart Çanakkale Deniz Zaferi|I. Dünya Savaşı|O:V. Mehmet Reşat
1916|Kut'ül-Amare Zaferi|I. Dünya Savaşı|O:V. Mehmet Reşat
1917|Rusya'da Bolşevik İhtilali|I. Dünya Savaşı|
1918|Mondros Ateşkes Antlaşması|I. Dünya Savaşı|
1919|Mustafa Kemal'in Samsun'a çıkışı|Milli Mücadele|
1920|Türkiye Büyük Millet Meclisi'nin açılması|Milli Mücadele|
1921|Sakarya Meydan Muharebesi|Kurtuluş Savaşı|
1922|Saltanatın kaldırılması|Devrimler|
1923|Lozan Barış Antlaşması|Lozan|
1924|Halifeliğin kaldırılması|Devrimler|
1925|Şapka Kanunu'nun kabulü|Devrimler|
1926|Türk Medeni Kanunu'nun kabulü|Devrimler|
1927|Nutuk'un okunması|Devrimler|
1928|Harf İnkılabı (yeni Türk harflerinin kabulü)|Devrimler|
1930|Kadınlara belediye seçimlerinde seçme ve seçilme hakkının tanınması|Devrimler|
1931|Türk Tarihi Tetkik Cemiyeti'nin kurulması|Devrimler|
1932|Türkiye'nin Milletler Cemiyeti'ne üye olması|Çağdaş Tarih|
1933|Darülfünun'un kaldırılarak İstanbul Üniversitesi'nin kurulması|Devrimler|
1934|Soyadı Kanunu'nun kabulü|Devrimler|
1935|Hafta tatilinin pazar gününe alınması|Devrimler|
1936|Montrö Boğazlar Sözleşmesi|Çağdaş Tarih|
1937|Sadabat Paktı|Çağdaş Tarih|
1938|Atatürk'ün vefatı|Çağdaş Tarih|
1939|Hatay'ın Türkiye'ye katılması|Çağdaş Tarih|
1945|Birleşmiş Milletler'in kurulması|Çağdaş Tarih|
1946|Türkiye'de ilk çok partili genel seçim|Çağdaş Tarih|
1947|Truman Doktrini|Çağdaş Tarih|
1948|İsrail Devleti'nin kurulması|Çağdaş Tarih|
1949|NATO'nun kurulması|Çağdaş Tarih|
1950|Kore Savaşı'nın başlaması|Çağdaş Tarih|
1952|Türkiye'nin NATO'ya üye olması|Çağdaş Tarih|
1955|Varşova Paktı'nın kurulması|Çağdaş Tarih|
1957|Sovyetlerin Sputnik uydusunu fırlatması|Çağdaş Tarih|
1959|Küba Devrimi|Çağdaş Tarih|
1961|Berlin Duvarı'nın inşası|Çağdaş Tarih|
1962|Küba Füze Bunalımı|Çağdaş Tarih|
1963|Türkiye ile AET arasında Ankara Antlaşması|Çağdaş Tarih|
1964|Johnson Mektubu|Çağdaş Tarih|
1969|Ay'a ilk insanlı inişin gerçekleşmesi|Çağdaş Tarih|
1973|Boğaziçi Köprüsü'nün açılması|Çağdaş Tarih|
1974|Kıbrıs Barış Harekâtı|Çağdaş Tarih|
1975|Helsinki Nihai Senedi|Çağdaş Tarih|
1979|İran İslam Devrimi|Çağdaş Tarih|
1983|Kuzey Kıbrıs Türk Cumhuriyeti'nin kurulması|Çağdaş Tarih|
1987|Türkiye'nin Avrupa Topluluğu'na tam üyelik başvurusu|Çağdaş Tarih|
1989|Berlin Duvarı'nın yıkılması|Çağdaş Tarih|
1990|Irak'ın Kuveyt'i işgali|Çağdaş Tarih|
1991|Sovyetler Birliği'nin dağılması|Çağdaş Tarih|
1992|Maastricht Antlaşması|Çağdaş Tarih|
1999|Helsinki Zirvesi'nde Türkiye'ye AB adaylık statüsü verilmesi|Çağdaş Tarih|
2001|11 Eylül saldırıları|Çağdaş Tarih|
2005|Türkiye ile AB arasında katılım müzakerelerinin başlaması|Çağdaş Tarih|
"""

# Aynı yıl içinde başka olaylar: yıl ve yüzyıl sorularında kullanılır, "o yıl hangi olay" sorusunda kullanılmaz.
AYNI_YIL = """
1444|Edirne-Segedin Antlaşması|Osmanlı Kuruluş|O:II. Murat
1571|İnebahtı Deniz Savaşı|Kanuni Dönemi|O:II. Selim
1831|Takvim-i Vekayi gazetesinin yayımlanması|Islahatlar|O:II. Mahmut
1856|Paris Antlaşması|Tanzimat|O:Abdülmecit
1876|Kanun-i Esasi'nin ilanı|Meşrutiyet|O:II. Abdülhamit
1878|Ayastefanos Antlaşması|Meşrutiyet|O:II. Abdülhamit
1878|Berlin Antlaşması|Meşrutiyet|O:II. Abdülhamit
1908|Bulgaristan'ın bağımsızlığını ilan etmesi|Meşrutiyet|O:II. Abdülhamit
1908|Bosna-Hersek'in Avusturya-Macaristan tarafından ilhakı|Meşrutiyet|O:II. Abdülhamit
1912|I. Balkan Savaşı'nın başlaması|Balkan Savaşları|O:V. Mehmet Reşat
1913|II. Balkan Savaşı|Balkan Savaşları|O:V. Mehmet Reşat
1913|Bükreş Antlaşması (Balkan Savaşları)|Balkan Savaşları|O:V. Mehmet Reşat
1914|Saraybosna suikastı|I. Dünya Savaşı|
1915|Anafartalar Zaferi|I. Dünya Savaşı|O:V. Mehmet Reşat
1916|Sykes-Picot Antlaşması|I. Dünya Savaşı|
1917|ABD'nin I. Dünya Savaşı'na girmesi|I. Dünya Savaşı|
1918|Brest-Litovsk Antlaşması|I. Dünya Savaşı|
1919|Amasya Genelgesi|Milli Mücadele|
1919|Erzurum Kongresi|Milli Mücadele|
1919|Sivas Kongresi|Milli Mücadele|
1919|İzmir'in Yunanlılar tarafından işgali|Milli Mücadele|
1919|Havza Genelgesi|Milli Mücadele|
1919|Versay Antlaşması|I. Dünya Savaşı|
1920|Misak-ı Milli'nin kabulü|Milli Mücadele|
1920|İstanbul'un İtilaf Devletlerince resmen işgali|Milli Mücadele|
1920|Sevr Antlaşması|Milli Mücadele|
1920|Gümrü Antlaşması|Kurtuluş Savaşı|
1921|I. İnönü Muharebesi|Kurtuluş Savaşı|
1921|İstiklal Marşı'nın kabulü|Kurtuluş Savaşı|
1921|Moskova Antlaşması|Kurtuluş Savaşı|
1921|II. İnönü Muharebesi|Kurtuluş Savaşı|
1921|Kütahya-Eskişehir Muharebeleri|Kurtuluş Savaşı|
1921|Tekalif-i Milliye Emirleri|Kurtuluş Savaşı|
1921|Kars Antlaşması|Kurtuluş Savaşı|
1921|Fransa ile Ankara Antlaşması|Kurtuluş Savaşı|
1921|Teşkilat-ı Esasiye Kanunu'nun kabulü|Milli Mücadele|
1922|Büyük Taarruz|Kurtuluş Savaşı|
1922|Mudanya Ateşkes Antlaşması|Kurtuluş Savaşı|
1923|Cumhuriyet'in ilanı|Devrimler|
1923|İzmir İktisat Kongresi|Devrimler|
1923|Ankara'nın başkent ilan edilmesi|Devrimler|
1924|Tevhid-i Tedrisat Kanunu'nun kabulü|Devrimler|
1924|1924 Anayasası'nın kabulü|Devrimler|
1925|Tekke ve zaviyelerin kapatılması|Devrimler|
1925|Aşar vergisinin kaldırılması|Devrimler|
1925|Şeyh Sait İsyanı|Devrimler|
1925|Uluslararası takvim ve saat sisteminin kabulü|Devrimler|
1926|Musul sorununa ilişkin Ankara Antlaşması|Çağdaş Tarih|
1927|Cumhuriyet döneminin ilk nüfus sayımı|Devrimler|
1928|Uluslararası rakamların kabulü|Devrimler|
1928|Anayasa'dan "Devletin dini İslam'dır" ifadesinin çıkarılması|Atatürk İlkeleri|
1930|Serbest Cumhuriyet Fırkası'nın kurulması|Devrimler|
1930|Menemen Olayı|Devrimler|
1931|Ölçüler Kanunu'nun kabulü|Devrimler|
1932|Türk Dili Tetkik Cemiyeti'nin kurulması|Devrimler|
1932|Halkevlerinin açılması|Devrimler|
1934|Kadınlara milletvekili seçme ve seçilme hakkının tanınması|Devrimler|
1934|Balkan Antantı|Çağdaş Tarih|
1934|I. Beş Yıllık Sanayi Planı'nın uygulamaya konması|Atatürk İlkeleri|
1937|Atatürk ilkelerinin Anayasa'ya girmesi|Atatürk İlkeleri|
1939|II. Dünya Savaşı'nın başlaması|Çağdaş Tarih|
1945|Hiroşima'ya atom bombası atılması|Çağdaş Tarih|
1949|Çin Halk Cumhuriyeti'nin kurulması|Çağdaş Tarih|
1950|Demokrat Parti'nin iktidara gelmesi|Çağdaş Tarih|
1955|Bağdat Paktı|Çağdaş Tarih|
1957|Roma Antlaşması ile AET'nin kurulması|Çağdaş Tarih|
1960|27 Mayıs askerî müdahalesi|Çağdaş Tarih|
1960|Kıbrıs Cumhuriyeti'nin kurulması|Çağdaş Tarih|
1961|1961 Anayasası'nın kabulü|Çağdaş Tarih|
1969|İslam Konferansı Örgütü'nün kurulması|Çağdaş Tarih|
1979|Sovyetler Birliği'nin Afganistan'ı işgali|Çağdaş Tarih|
1980|12 Eylül askerî müdahalesi|Çağdaş Tarih|
1982|1982 Anayasası'nın kabulü|Çağdaş Tarih|
1990|Almanya'nın birleşmesi|Çağdaş Tarih|
1991|Körfez Savaşı|Çağdaş Tarih|
1992|Karadeniz Ekonomik İşbirliği Örgütü'nün kurulması|Çağdaş Tarih|
1922|Sovyet Sosyalist Cumhuriyetler Birliği'nin kurulması|Çağdaş Tarih|
1929|Büyük Buhran (Dünya Ekonomik Krizi)|Çağdaş Tarih|
1933|Hitler'in Almanya'da iktidara gelmesi|Çağdaş Tarih|
1941|Pearl Harbor baskını|Çağdaş Tarih|
"""

# kavram | açıklama | konu
KAVRAMLAR = """
Kurultay (Toy)|Eski Türklerde devlet işlerinin görüşüldüğü meclis|İlk Türk Devletleri
Kut|Hükümdarlık yetkisinin Tanrı tarafından verildiğine inanılan güç|İlk Türk Devletleri
Ordu-Balık|Eski Türklerde hükümdarın oturduğu merkez, başkent|İlk Türk Devletleri
Balbal|Ölen kişinin öldürdüğü düşmanları temsil eden mezar taşları|İlk Türk Devletleri
Kurgan|Eski Türklerde ölülerin eşyalarıyla birlikte gömüldüğü mezar|İlk Türk Devletleri
Yuğ|Eski Türklerde ölen kişi için düzenlenen cenaze töreni|İlk Türk Devletleri
Sagu|Ölen kişinin ardından söylenen ağıt|İlk Türk Devletleri
Koşuk|Eski Türklerde sığır törenlerinde söylenen lirik şiir|İlk Türk Devletleri
Kam (Şaman)|Eski Türk inancında ruhlarla iletişim kurduğuna inanılan din adamı|İlk Türk Devletleri
Töre|Eski Türklerde yazısız hukuk kuralları|İlk Türk Devletleri
Tamga|Boyların hayvanlarına ve eşyalarına vurdukları damga, boy işareti|İlk Türk Devletleri
Yabgu|Göktürklerde devletin batı kanadını yöneten hükümdar ailesi üyesi|Göktürkler
Tudun|Eski Türklerde bağlı topluluklardan vergi toplayan ve denetleyen görevli|İlk Türk Devletleri
Ayukı|Eski Türklerde devlet işlerinde hükümdara danışmanlık yapan kurul|İlk Türk Devletleri
Tigin|Eski Türklerde hükümdarın erkek çocuklarına verilen unvan|İlk Türk Devletleri
Hatun|Eski Türklerde hükümdarın eşine verilen unvan|İlk Türk Devletleri
Ikta|Selçuklularda hizmet karşılığı toprağın vergi gelirinin askerlere ve devlet görevlilerine bırakılması|Selçuklu
Atabey|Selçuklularda melik olarak gönderilen şehzadelerin eğitiminden sorumlu devlet adamı|Selçuklu
Melik|Selçuklularda eyalet yönetimine gönderilen hanedan üyesi şehzade|Selçuklu
Nizamiye Medreseleri|Nizamülmülk tarafından kurulan Selçuklu eğitim kurumları|Selçuklu
Ahilik|Esnaf ve sanatkârların mesleki ve ahlaki eğitimini düzenleyen teşkilat|Türk-İslam Kültürü
Kervansaray|Ticaret yolları üzerinde tüccarların konaklaması için yapılan yapılar|Anadolu Selçuklu
Darüşşifa|Türk-İslam devletlerinde hastane|Türk-İslam Kültürü
Bimarhane|Türk-İslam devletlerinde akıl hastalarının tedavi edildiği yer|Türk-İslam Kültürü
Rasathane|Gök cisimlerinin gözlemlendiği bilim kurumu|Türk-İslam Kültürü
Uç Beyi|Sınır bölgelerini yöneten bey|Beylikler
Gaza|İslam'ı yaymak amacıyla yapılan kutsal savaş|Beylikler
Divan-ı Hümayun|Osmanlı'da devlet işlerinin görüşüldüğü en üst meclis|Osmanlı Kuruluş
Tımar|Geliri 3 bin ile 20 bin akçe arasında olan dirlik|Osmanlı Kuruluş
Zeamet|Geliri 20 bin ile 100 bin akçe arasında olan dirlik|Osmanlı Kuruluş
Has|Geliri 100 bin akçenin üzerinde olan dirlik|Osmanlı Kuruluş
Devşirme|Hristiyan ailelerin çocuklarının alınıp eğitilerek devlet hizmetinde kullanılması sistemi|Osmanlı Kuruluş
Kapıkulu|Merkezde bulunan, maaşlı ve sürekli Osmanlı askerî birlikleri|Osmanlı Kuruluş
Yaya ve Müsellem|Orhan Bey döneminde kurulan ilk düzenli Osmanlı ordusu|Osmanlı Kuruluş
Akıncılar|Düşman topraklarına keşif ve yıpratma akınları yapan Osmanlı hafif süvarileri|Osmanlı Kuruluş
Cebelü|Tımar sahiplerinin gelirlerine göre yetiştirip savaşa götürdüğü atlı asker|Osmanlı Kuruluş
Enderun|Osmanlı sarayında devlet adamı yetiştiren okul|Osmanlı Kuruluş
Kazasker|Divan-ı Hümayun'da adalet ve eğitim işlerinden sorumlu üye|Osmanlı Kuruluş
Nişancı|Divan-ı Hümayun'da padişah fermanlarına tuğra çeken görevli|Osmanlı Kuruluş
Defterdar|Divan-ı Hümayun'da mali işlerden sorumlu üye|Osmanlı Kuruluş
Kaptan-ı Derya|Osmanlı donanmasının komutanı|Osmanlı Kuruluş
Şeyhülislam|Osmanlı'da fetva veren en yüksek din görevlisi|Osmanlı Kuruluş
Sadrazam|Padişahın mutlak vekili olan Osmanlı veziriazamı|Osmanlı Kuruluş
Reaya|Osmanlı'da vergi veren yönetilen halk|Osmanlı Kuruluş
Millet sistemi|Osmanlı'da toplumun dinî inanca göre örgütlenmesi|Fatih Dönemi
Kanunname|Padişahların örfi hukuka dayanarak çıkardığı kanunların toplandığı belge|Fatih Dönemi
Kafes usulü|Şehzadelerin sancağa gönderilmeyip sarayda tutulması uygulaması|Duraklama
Ekber ve erşed|Hanedanın en yaşlı ve akıllı erkek üyesinin tahta geçmesi sistemi|Duraklama
Cülus bahşişi|Yeni padişahın tahta çıkışında askerlere verilen para|Osmanlı Kuruluş
İltizam|Devlet gelirlerinin peşin ödeme karşılığında açık artırmayla özel kişilere bırakılması|Duraklama
Malikane|Vergi toplama hakkının ömür boyu verilmesi sistemi|Lale Devri
Esham|Devlet gelirlerine dayanan, halka satılan ilk iç borçlanma senedi|Islahatlar
Müsadere|Ölen ya da görevden alınan devlet adamlarının mallarına el konulması|Duraklama
Lonca|Osmanlı şehirlerinde aynı mesleği yapan esnafın örgütü|Osmanlı Kuruluş
Gedik|Osmanlı esnafına verilen dükkân açma ve meslek icra etme izni|Osmanlı Kuruluş
Narh|Osmanlı'da malların satış fiyatına konulan resmî sınır|Osmanlı Kuruluş
Muhtesip|Osmanlı çarşılarında fiyat, ölçü ve kaliteyi denetleyen görevli|Osmanlı Kuruluş
Cizye|Osmanlı'da gayrimüslim erkeklerden askerlik karşılığı alınan vergi|Osmanlı Kuruluş
Öşür|Müslüman halktan alınan ürün vergisi|Osmanlı Kuruluş
Avarız|Olağanüstü durumlarda alınan vergi|Osmanlı Kuruluş
Çiftbozan|Toprağını sebepsiz yere üç yıl üst üste boş bırakan köylüden alınan vergi|Osmanlı Kuruluş
Mirî arazi|Mülkiyeti devlete ait olan toprak|Osmanlı Kuruluş
Vakıf|Bir malın gelirinin hayır işlerine kalıcı olarak ayrılması|Osmanlı Kuruluş
Külliye|Cami etrafında medrese, imaret, hamam gibi yapılardan oluşan yapı topluluğu|Osmanlı Kuruluş
İmaret|Yoksullara ücretsiz yemek dağıtılan aşevi|Osmanlı Kuruluş
Bedesten|Değerli malların alınıp satıldığı kapalı çarşı|Osmanlı Kuruluş
Kapitülasyon|Osmanlı'nın yabancı devletlere verdiği ticari ve hukuki ayrıcalıklar|Kanuni Dönemi
Ayan|Taşrada yerel yönetimde söz sahibi olan nüfuzlu kişiler|Islahatlar
Nizam-ı Cedit|III. Selim döneminde yapılan ıslahatların ve kurulan yeni ordunun genel adı|Islahatlar
Sekban-ı Cedit|II. Mahmut döneminde Alemdar Mustafa Paşa'nın kurduğu ordu|Islahatlar
Asakir-i Mansure-i Muhammediye|Yeniçeri Ocağı kaldırıldıktan sonra kurulan ordu|Islahatlar
Mecelle|Ahmet Cevdet Paşa başkanlığında hazırlanan medeni kanun|Tanzimat
Moratoryum|Devletin borçlarını ödeyemeyeceğini ilan etmesi|Tanzimat
Duyun-u Umumiye|Osmanlı dış borçlarını tahsil etmek için kurulan idare|Meşrutiyet
Meşrutiyet|Hükümdarın yetkilerinin anayasa ve seçilmiş meclisle sınırlandırıldığı yönetim|Meşrutiyet
Kanun-i Esasi|Osmanlı Devleti'nin ilk anayasası|Meşrutiyet
Heyet-i Ayan|Osmanlı Meclisi Umumisi'nde üyeleri padişah tarafından atanan kanat|Meşrutiyet
Meclis-i Mebusan|Osmanlı Meclisi Umumisi'nde üyeleri halk tarafından seçilen kanat|Meşrutiyet
Osmanlıcılık|Dil, din ve ırk ayrımı gözetmeksizin tüm tebaayı Osmanlı kimliğinde birleştirme düşüncesi|Meşrutiyet
İslamcılık|Müslüman toplulukları halife etrafında birleştirmeyi amaçlayan düşünce|Meşrutiyet
Türkçülük|Türkleri ortak kimlikte birleştirmeyi amaçlayan düşünce akımı|Meşrutiyet
Batıcılık|Kurtuluşun Batı'nın bilim ve kurumlarını benimsemekte olduğunu savunan düşünce|Meşrutiyet
Misak-ı Milli|Son Osmanlı Mebusan Meclisi'nde kabul edilen milli ant|Milli Mücadele
Kuva-yi Milliye|İşgallere karşı halkın kendiliğinden oluşturduğu silahlı direniş birlikleri|Milli Mücadele
Manda|Bir milletin güçlü bir devletin koruması altına girmesi|Milli Mücadele
Tekalif-i Milliye|Sakarya öncesinde halktan ordu için savaş malzemesi toplanmasını sağlayan emirler|Kurtuluş Savaşı
İstiklal Mahkemeleri|Milli Mücadele döneminde TBMM'nin kurduğu olağanüstü mahkemeler|Milli Mücadele
Hıyanet-i Vataniye Kanunu|TBMM'ye karşı ayaklanmaları önlemek için çıkarılan kanun|Milli Mücadele
Başkomutanlık Kanunu|Mustafa Kemal'e meclisin yetkilerini kullanma hakkı veren kanun|Kurtuluş Savaşı
Takrir-i Sükûn Kanunu|Şeyh Sait İsyanı üzerine hükümete olağanüstü yetkiler veren kanun|Devrimler
Tevhid-i Tedrisat|Tüm eğitim kurumlarının Milli Eğitim Bakanlığına bağlanması|Devrimler
Millet Mektepleri|Harf İnkılabı sonrasında halka okuma yazma öğretmek için açılan kurslar|Devrimler
Halkevleri|Cumhuriyet'in ilkelerini halka benimsetmek için açılan kültür kurumları|Devrimler
Cumhuriyetçilik|Egemenliğin kayıtsız şartsız millete ait olmasını esas alan ilke|Atatürk İlkeleri
Milliyetçilik|Milletin bağımsızlığını ve birliğini esas alan, ırkçılığı reddeden ilke|Atatürk İlkeleri
Halkçılık|Sınıf ayrıcalığını reddeden, kanun önünde eşitliği esas alan ilke|Atatürk İlkeleri
Devletçilik|Özel sermayenin yetersiz kaldığı alanlarda devletin ekonomiye girmesini öngören ilke|Atatürk İlkeleri
Laiklik|Din ve devlet işlerinin birbirinden ayrılmasını esas alan ilke|Atatürk İlkeleri
İnkılapçılık|Yapılan inkılapların korunmasını ve çağdaşlaşmanın sürdürülmesini öngören ilke|Atatürk İlkeleri
Soğuk Savaş|II. Dünya Savaşı sonrasında ABD ve SSCB blokları arasındaki silahlı çatışmasız gerginlik dönemi|Çağdaş Tarih
Yumuşama (Detant)|1960'ların sonundan itibaren iki blok arasındaki gerginliğin azaldığı dönem|Çağdaş Tarih
Glasnost|Gorbaçov'un SSCB'de başlattığı açıklık politikası|Çağdaş Tarih
Perestroyka|Gorbaçov'un SSCB'de başlattığı yeniden yapılanma politikası|Çağdaş Tarih
Truman Doktrini|ABD'nin Türkiye ve Yunanistan'a askerî ve ekonomik yardım öngören politikası|Çağdaş Tarih
Marshall Planı|ABD'nin II. Dünya Savaşı sonrasında Avrupa'ya ekonomik yardım programı|Çağdaş Tarih
"""

# eser | yazar | konu
ESERLER = """
Kutadgu Bilig|Yusuf Has Hacip|Türk-İslam Kültürü
Divanü Lügati't-Türk|Kaşgarlı Mahmut|Türk-İslam Kültürü
Atabetü'l-Hakayık|Edip Ahmet Yükneki|Türk-İslam Kültürü
Divan-ı Hikmet|Hoca Ahmet Yesevi|Türk-İslam Kültürü
Siyasetname|Nizamülmülk|Selçuklu
Şehname|Firdevsi|Gazneliler
Mesnevi|Mevlana Celaleddin Rumi|Anadolu Selçuklu
Garipname|Âşık Paşa|Beylikler
Kitab-ı Bahriye|Piri Reis|Kanuni Dönemi
Muhakemetü'l-Lugateyn|Ali Şir Nevai|Türk-İslam Kültürü
Seyahatname|Evliya Çelebi|Duraklama
Cihannüma|Kâtip Çelebi|Duraklama
Keşfü'z-Zünun|Kâtip Çelebi|Duraklama
Usulü'l-Hikem fi Nizami'l-Ümem|İbrahim Müteferrika|Lale Devri
Mukaddime|İbn Haldun|Türk-İslam Kültürü
Tarih-i Cevdet|Ahmet Cevdet Paşa|Tanzimat
Vatan yahut Silistre|Namık Kemal|Tanzimat
Şair Evlenmesi|Şinasi|Tanzimat
Türkçülüğün Esasları|Ziya Gökalp|Meşrutiyet
Üç Tarz-ı Siyaset|Yusuf Akçura|Meşrutiyet
Nutuk|Mustafa Kemal Atatürk|Devrimler
Geometri (terimleri Türkçeleştiren kitap)|Mustafa Kemal Atatürk|Devrimler
İstiklal Marşı|Mehmet Akif Ersoy|Kurtuluş Savaşı
Safahat|Mehmet Akif Ersoy|Kurtuluş Savaşı
Ateşten Gömlek|Halide Edip Adıvar|Kurtuluş Savaşı
Kiralık Konak|Yakup Kadri Karaosmanoğlu|Meşrutiyet
Yaban|Yakup Kadri Karaosmanoğlu|Kurtuluş Savaşı
Çalıkuşu|Reşat Nuri Güntekin|Meşrutiyet
"""

# Özellikle tanınan olay/devlet: soru kökü, doğru cevap, çeldirici grubu, konu
OZELLIKLER = """
Türk adının devlet adı olarak ilk kez kullanıldığı Türk devleti hangisidir?|Göktürkler|devlet|Göktürkler
Yerleşik hayata geçen ve Mani dinini benimseyen ilk Türk devleti hangisidir?|Uygurlar|devlet|Uygurlar
İslamiyet'i devlet dini olarak kabul eden ilk Türk devleti hangisidir?|Karahanlılar|devlet|Karahanlılar
Türk-İslam tarihinde Hindistan'a 17 sefer düzenleyen hükümdar kimdir?|Gazneli Mahmut|kisi|Gazneliler
Anadolu'nun kapılarını Türklere açan savaş hangisidir?|Malazgirt Savaşı|savas|Selçuklu
Anadolu'nun Türk yurdu olduğunun kesinleştiği savaş hangisidir?|Miryokefalon Savaşı|savas|Anadolu Selçuklu
Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş hangisidir?|Dandanakan Savaşı|savas|Selçuklu
Türklerle Bizans arasındaki ilk büyük savaş hangisidir?|Pasinler Savaşı|savas|Selçuklu
Türkiye Selçuklularının Moğol egemenliğine girmesine yol açan savaş hangisidir?|Kösedağ Savaşı|savas|Anadolu Selçuklu
Abbasiler ile Çinliler arasında yapılan ve kâğıdın İslam dünyasına geçmesini sağlayan savaş hangisidir?|Talas Savaşı|savas|İlk Türk Devletleri
Osmanlı Devleti'nin Bizans ile yaptığı ilk savaş hangisidir?|Koyunhisar (Bafeus) Savaşı|savas|Osmanlı Kuruluş
Osmanlıların Haçlılarla yaptığı ilk savaş hangisidir?|Sırpsındığı Savaşı|savas|Osmanlı Kuruluş
Fetret Devri'nin başlamasına yol açan savaş hangisidir?|Ankara Savaşı|savas|Osmanlı Kuruluş
Osmanlı'nın Akkoyunlularla yaptığı ve Doğu Anadolu'da Türk birliğini sağlamaya yönelik savaş hangisidir?|Otlukbeli Savaşı|savas|Fatih Dönemi
Halifeliğin Osmanlılara geçmesini sağlayan seferin son savaşı hangisidir?|Ridaniye Savaşı|savas|Kanuni Dönemi
Macaristan'ın büyük kısmının Osmanlı egemenliğine girmesini sağlayan savaş hangisidir?|Mohaç Meydan Savaşı|savas|Kanuni Dönemi
Akdeniz'in bir Türk gölü hâline gelmesini sağlayan deniz savaşı hangisidir?|Preveze Deniz Savaşı|savas|Kanuni Dönemi
Osmanlı donanmasının ilk kez büyük bir yenilgiye uğradığı deniz savaşı hangisidir?|İnebahtı Deniz Savaşı|savas|Kanuni Dönemi
Osmanlı Devleti'nin Avusturya ile eşit sayıldığı ve Avusturya arşidükünün Osmanlı padişahına eşit kabul edildiği antlaşma hangisidir?|Zitvatorok Antlaşması|antlasma|Duraklama
Osmanlı Devleti'nin batıda en geniş sınırlara ulaştığı antlaşma hangisidir?|Bucaş Antlaşması|antlasma|Duraklama
Osmanlı Devleti'nin ilk kez büyük toprak kaybettiği antlaşma hangisidir?|Karlofça Antlaşması|antlasma|Duraklama
Bugünkü Türkiye-İran sınırının büyük ölçüde çizildiği antlaşma hangisidir?|Kasr-ı Şirin Antlaşması|antlasma|Duraklama
Lale Devri'ni başlatan antlaşma hangisidir?|Pasarofça Antlaşması|antlasma|Lale Devri
Osmanlı'nın son kazançlı antlaşması kabul edilen ve Belgrad'ın geri alındığı antlaşma hangisidir?|Belgrad Antlaşması|antlasma|Islahatlar
Kırım'ın bağımsız olduğu ve Rusya'ya Ortodoksların koruyuculuğu hakkının tanındığı antlaşma hangisidir?|Küçük Kaynarca Antlaşması|antlasma|Islahatlar
Rusya'nın Kırım'ı ilhakının Osmanlı tarafından tanındığı antlaşma hangisidir?|Yaş Antlaşması|antlasma|Islahatlar
Osmanlı'dan bağımsızlığını kazanan ilk Hristiyan milletin bağımsızlığına zemin hazırlayan antlaşma hangisidir?|Edirne Antlaşması|antlasma|Islahatlar
Boğazların Rusya dışındaki savaş gemilerine kapatılmasını öngören antlaşma hangisidir?|Hünkâr İskelesi Antlaşması|antlasma|Islahatlar
Osmanlı ekonomisini açık pazar hâline getiren İngiltere ile ticaret antlaşması hangisidir?|Balta Limanı Ticaret Antlaşması|antlasma|Islahatlar
Boğazların uluslararası bir statüye kavuştuğu ilk sözleşme hangisidir?|Londra Boğazlar Sözleşmesi|antlasma|Tanzimat
Osmanlı Devleti'nin Avrupa devleti sayıldığı ve Avrupa hukukundan yararlanacağının belirtildiği antlaşma hangisidir?|Paris Antlaşması|antlasma|Tanzimat
Osmanlı Devleti'nin Kuzey Afrika'daki son toprağını kaybettiği antlaşma hangisidir?|Uşi Antlaşması|antlasma|Trablusgarp
Osmanlı Devleti'ni fiilen sona erdiren ateşkes antlaşması hangisidir?|Mondros Ateşkes Antlaşması|antlasma|I. Dünya Savaşı
TBMM'nin ilk askerî ve siyasi başarısı olan antlaşma hangisidir?|Gümrü Antlaşması|antlasma|Kurtuluş Savaşı
TBMM'yi tanıyan ilk Avrupalı devletle imzalanan antlaşma hangisidir?|Fransa ile Ankara Antlaşması|antlasma|Kurtuluş Savaşı
Kurtuluş Savaşı'nın silahlı mücadele döneminin sona erdiği antlaşma hangisidir?|Mudanya Ateşkes Antlaşması|antlasma|Kurtuluş Savaşı
Kapitülasyonların tamamen kaldırıldığı antlaşma hangisidir?|Lozan Barış Antlaşması|antlasma|Lozan
Boğazların yönetiminin Türkiye'ye bırakıldığı sözleşme hangisidir?|Montrö Boğazlar Sözleşmesi|antlasma|Çağdaş Tarih
Kurtuluş Savaşı'nın gerekçesinin, amacının ve yönteminin ilk kez belirtildiği belge hangisidir?|Amasya Genelgesi|belge|Milli Mücadele
Milli Mücadele'de "Ulusun bağımsızlığını yine ulusun azim ve kararı kurtaracaktır." ifadesinin yer aldığı belge hangisidir?|Amasya Genelgesi|belge|Milli Mücadele
Toplanış şekli bakımından bölgesel, aldığı kararlar bakımından ulusal olan kongre hangisidir?|Erzurum Kongresi|belge|Milli Mücadele
Bütün Kuva-yi Milliye cemiyetlerinin Anadolu ve Rumeli Müdafaa-i Hukuk Cemiyeti adı altında birleştirildiği kongre hangisidir?|Sivas Kongresi|belge|Milli Mücadele
Milli Mücadele'de İrade-i Milliye gazetesinin çıkarıldığı kongre hangisidir?|Sivas Kongresi|belge|Milli Mücadele
TBMM'nin düzenli ordu ile kazandığı ilk zafer hangisidir?|I. İnönü Muharebesi|savas|Kurtuluş Savaşı
"Hattı müdafaa yoktur, sathı müdafaa vardır." sözünün söylendiği muharebe hangisidir?|Sakarya Meydan Muharebesi|savas|Kurtuluş Savaşı
Mustafa Kemal'e mareşallik rütbesi ve gazilik unvanı verilmesine yol açan muharebe hangisidir?|Sakarya Meydan Muharebesi|savas|Kurtuluş Savaşı
TBMM'nin kabul ettiği ilk anayasa hangisidir?|Teşkilat-ı Esasiye Kanunu|belge|Milli Mücadele
Osmanlı Devleti'nde padişahın gücünü ilk kez sınırlandıran belge hangisidir?|Sened-i İttifak|belge|Islahatlar
Osmanlı'da kanun üstünlüğü ilkesinin ilk kez kabul edildiği belge hangisidir?|Tanzimat Fermanı|belge|Tanzimat
Gayrimüslimlere geniş haklar tanıyan ve Avrupa devletlerinin baskısıyla ilan edilen ferman hangisidir?|Islahat Fermanı|belge|Tanzimat
"""

DEVLETLER = """
I. Göktürk Devleti|Bumin Kağan|Ötüken|Göktürkler
II. Göktürk (Kutluk) Devleti|İlteriş Kutluk Kağan|-|Göktürkler
Uygur Devleti|Kutluk Bilge Kül Kağan|Karabalgasun|Uygurlar
Gazneli Devleti|Alp Tegin|Gazne|Gazneliler
Büyük Selçuklu Devleti|Tuğrul ve Çağrı Beyler|Nişabur|Selçuklu
Türkiye Selçuklu Devleti|Kutalmışoğlu Süleyman Şah|İznik|Anadolu Selçuklu
Osmanlı Beyliği|Osman Bey|Söğüt|Osmanlı Kuruluş
Eyyubi Devleti|Selahaddin Eyyubi|Kahire|Türk-İslam Kültürü
"""


def _satirlar(blok, n):
    out = []
    for line in blok.strip().splitlines():
        p = [x.strip() for x in line.split('|')]
        assert len(p) == n, line
        out.append(p)
    return out


def olaylar():
    tek = [(int(y), o, k, h) for y, o, k, h in _satirlar(OLAYLAR, 4)]
    ek = [(int(y), o, k, h) for y, o, k, h in _satirlar(AYNI_YIL, 4)]
    return tek, ek


def uret(rng):
    tek, ek = olaylar()
    tum = tek + ek
    yil_say = {}
    for y, *_ in tum:
        yil_say[y] = yil_say.get(y, 0) + 1
    out = []
    for y, o, konu, h in tum:
        yakin = sorted({yy for yy, *_ in tum if yy != y and abs(yy - y) <= 80}, key=lambda v: abs(v - y))
        havuz = [str(v) for v in yakin[:10]]
        if len(havuz) < 4:
            havuz += [str(y + d) for d in (-7, -5, -3, -2, 2, 3, 5, 7) if str(y + d) not in havuz]
        out.append(q('yil', konu, f'{o} hangi yılda gerçekleşmiştir?', y, sec(str(y), havuz, rng),
                     f'{o} {y} yılında gerçekleşmiştir. Diğer seçeneklerdeki yıllar başka olaylara aittir.', 3))
        c = yuzyil(y)
        yy = [yy_ad(x) for x in (c - 2, c - 1, c + 1, c + 2, c + 3) if x >= 1]
        out.append(q('yuzyil', konu, f'{o} hangi yüzyılda yaşanmıştır?', yy_ad(c), sec(yy_ad(c), yy, rng),
                     f'{o} {y} yılındadır; {y} yılı {yy_ad(c)} içinde yer alır.', 2))
        # önce / sonra (yalnız yılı kesin farklı olaylarla, aynı dönem penceresinde)
        pencere = [x for x in tum if abs(x[0] - y) <= 150 and x[0] != y]
        once = [x for x in pencere if x[0] < y]
        sonra = [x for x in pencere if x[0] > y]
        rng.shuffle(once)
        rng.shuffle(sonra)
        if once and len(sonra) >= 4:
            dogru = once[0]
            yan = []
            for x in sonra:
                if x[1] not in yan and len(yan) < 4:
                    yan.append(x[1])
            if len(yan) == 4:
                out.append(q('once', konu, f'Aşağıdakilerden hangisi “{o}” olayından önce gerçekleşmiştir?', dogru[1], yan,
                             f'{o} {y} yılındadır. {dogru[1]} {dogru[0]} yılında, yani daha önce gerçekleşmiştir; diğerleri {y} yılından sonradır.', 3))
        if sonra and len(once) >= 4:
            dogru = sonra[0]
            yan = []
            for x in once:
                if x[1] not in yan and len(yan) < 4:
                    yan.append(x[1])
            if len(yan) == 4:
                out.append(q('sonra', konu, f'Aşağıdakilerden hangisi “{o}” olayından sonra gerçekleşmiştir?', dogru[1], yan,
                             f'{o} {y} yılındadır. {dogru[1]} {dogru[0]} yılında, yani daha sonra gerçekleşmiştir; diğerleri {y} yılından öncedir.', 3))
        if h:
            tip, kisi = h.split(':', 1)
            grup = [x[3].split(':', 1)[1] for x in tum if x[3].startswith(tip + ':')]
            unvan = 'Osmanlı padişahı' if tip == 'O' else 'Selçuklu sultanı'
            out.append(q('kisi', konu, f'{o} hangi {unvan} döneminde gerçekleşmiştir?', kisi, sec(kisi, grup, rng),
                         f'{o} ({y}) {kisi} döneminde gerçekleşmiştir.', 2))
    # o yıl hangi olay (yalnız tek olaylı yıllar)
    for y, o, konu, h in tek:
        if yil_say[y] != 1:
            continue
        havuz = [x[1] for x in tum if x[0] != y and abs(x[0] - y) <= 120]
        rng.shuffle(havuz)
        out.append(q('yil_olay', konu, f'{y} yılında aşağıdaki gelişmelerden hangisi yaşanmıştır?', o, sec(o, havuz, rng),
                     f'{y} yılında {o} gerçekleşmiştir. Diğer seçenekler başka yıllara aittir.', 3))
    # kavramlar
    kav = [(a, d, k) for a, d, k in _satirlar(KAVRAMLAR, 3)]
    out += eslesme(rng, 'kavram', kav,
                   lambda a, d: f'Tarih terimi olarak “{a}” aşağıdakilerden hangisini ifade eder?',
                   lambda a, d: f'“{d}” aşağıdaki kavramlardan hangisiyle ifade edilir?',
                   lambda a, d: f'{a}: {d}.', lambda a, d: f'{d} = {a}.', 2, grup=lambda a, d, k: k)
    es = [(a, d, k) for a, d, k in _satirlar(ESERLER, 3)]
    out += eslesme(rng, 'eser', es,
                   lambda a, d: f'“{a}” adlı eser kime aittir?',
                   lambda a, d: f'Aşağıdaki eserlerden hangisi {d} tarafından yazılmıştır?',
                   lambda a, d: f'{a}, {d} tarafından yazılmıştır.', lambda a, d: f'{d}: {a}.', 2)
    # özellikler
    oz = _satirlar(OZELLIKLER, 4)
    for kok, dogru, grup, konu in oz:
        havuz = list({x[1] for x in oz if x[2] == grup and x[1] != dogru})
        if grup in ('savas', 'antlasma'):
            havuz += [x[1] for x in tum if 'başlaması' not in x[1] and 'Bunalımı' not in x[1] and
                      (('Savaşı' in x[1] or 'Muharebe' in x[1]) if grup == 'savas'
                       else ('Antlaşma' in x[1] or 'Sözleşme' in x[1]))]
        if grup == 'devlet':
            havuz += ['Hun İmparatorluğu', 'Avarlar', 'Hazarlar', 'Kırgızlar', 'Peçenekler', 'Büyük Selçuklu Devleti', 'İdil Bulgarları']
        if grup == 'kisi':
            havuz += ['Alparslan', 'Tuğrul Bey', 'Melikşah', 'Sultan Sencer', 'Alp Tegin']
        if grup == 'belge':
            havuz += ['Havza Genelgesi', 'Erzurum Kongresi', 'Amasya Genelgesi', 'Sivas Kongresi', 'Misak-ı Milli', 'Islahat Fermanı', 'Tanzimat Fermanı', 'Sened-i İttifak']
        rng.shuffle(havuz)
        out.append(q('ozellik', konu, kok, dogru, sec(dogru, havuz, rng), f'Doğru cevap: {dogru}. ' + kok.replace(' hangisidir?', '').replace(' kimdir?', '') + f' → {dogru}.', 3))
    dev = _satirlar(DEVLETLER, 4)
    for ad, kurucu, merkez, konu in dev:
        if merkez == '-':
            merkez = None
        out.append(q('kurucu', konu, f'{ad} kimin tarafından kurulmuştur?', kurucu,
                     sec(kurucu, [x[1] for x in dev] + ['Mete Han', 'Attila', 'Satuk Buğra Han', 'Orhan Bey'], rng),
                     f'{ad}, {kurucu} tarafından kurulmuştur.', 2))
        if merkez:
          out.append(q('merkez', konu, f'{ad} ilk merkezi (başkenti) olarak hangi şehri kullanmıştır?', merkez,
                     sec(merkez, [x[2] for x in dev if x[2] != '-'] + ['Bursa', 'Konya', 'Balasagun', 'Kaşgar'], rng),
                     f'{ad} kuruluşunda {merkez} merkezliydi.', 3))
    return out
