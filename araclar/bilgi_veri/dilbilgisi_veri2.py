"""KPSS Türkçe dil bilgisi bankası (2): yazım, noktalama, cümle ögeleri, cümle türleri.

Etiketler TDK Yazım Kılavuzu ve ortaöğretim dil bilgisi terimlerine göredir.
"""

# ---------------------------------------------------------------- yazım
# W|yanlış yazılmış cümle|doğru yazılışı|açıklama   (her yanlış cümlede tek yazım yanlışı vardır)
# C|yazımı doğru cümle
YAZIM = """
W|Bu konuyu her kes farklı yorumladı.|Bu konuyu herkes farklı yorumladı.|“Herkes” sözcüğü bitişik yazılır.
W|Toplantıya bir çok kişi katıldı.|Toplantıya birçok kişi katıldı.|“Birçok” bitişik yazılır.
W|Hiç bir şey söylemeden odadan çıktı.|Hiçbir şey söylemeden odadan çıktı.|“Hiçbir” bitişik yazılır.
W|Akşam ki toplantıya ben de katılacağım.|Akşamki toplantıya ben de katılacağım.|Sıfat yapan “-ki” eki bitişik yazılır: akşamki.
W|Kardeşimde bu kitabı çok beğendi.|Kardeşim de bu kitabı çok beğendi.|Bağlaç olan “de” ayrı yazılır.
W|Duydumki yeni bir işe başlamışsın.|Duydum ki yeni bir işe başlamışsın.|Bağlaç olan “ki” ayrı yazılır.
W|Toplantı 15 mayıs 2026 tarihinde yapılacak.|Toplantı 15 Mayıs 2026 tarihinde yapılacak.|Belirli bir tarih bildiren ay adları büyük harfle başlar.
W|Her yıl Mayıs ayında bu şenlik yapılır.|Her yıl mayıs ayında bu şenlik yapılır.|Belirli bir tarih bildirmeyen ay adları küçük harfle yazılır.
W|Yazın Ege'ye, kışın ise doğu Anadolu'ya gideriz.|Yazın Ege'ye, kışın ise Doğu Anadolu'ya gideriz.|Bölge adlarındaki yön sözcükleri büyük harfle başlar: Doğu Anadolu.
W|Dün akşam Annem bize kek yaptı.|Dün akşam annem bize kek yaptı.|Akrabalık bildiren sözcükler cümle içinde küçük harfle yazılır.
W|Yarın ki sınava çok iyi hazırlandım.|Yarınki sınava çok iyi hazırlandım.|“-ki” eki bitişik yazılır: yarınki.
W|Bu güne kadar hiç böyle bir şey görmedim.|Bugüne kadar hiç böyle bir şey görmedim.|“Bugün” bitişik yazılır.
W|Pekçok insan bu karara karşı çıktı.|Pek çok insan bu karara karşı çıktı.|“Pek çok” ayrı yazılır.
W|Herşey yolunda gidiyor.|Her şey yolunda gidiyor.|“Her şey” ayrı yazılır.
W|Bir kaç gün sonra yeniden görüşeceğiz.|Birkaç gün sonra yeniden görüşeceğiz.|“Birkaç” bitişik yazılır.
W|Bu işi yanlız başına bitirdi.|Bu işi yalnız başına bitirdi.|Doğru yazılış “yalnız”dır.
W|Türkçe'nin zengin bir söz varlığı vardır.|Türkçenin zengin bir söz varlığı vardır.|“-ce/-ça” ile kurulan dil adlarına gelen ekler kesmeyle ayrılmaz.
W|Ankara'lı bir ailenin çocuğuydu.|Ankaralı bir ailenin çocuğuydu.|Özel adlara gelen yapım ekleri kesmeyle ayrılmaz: Ankaralı.
W|Bu raporu TDK'ya gönderdik.|Bu raporu TDK'ye gönderdik.|Kısaltmalara ekler okunuşa göre getirilir: TDK (te de ke) → TDK'ye.
W|Meclis bu yıl ki ilk oturumunu yaptı.|Meclis bu yılki ilk oturumunu yaptı.|“-ki” eki bitişik yazılır: yılki.
W|Tatilde Karadenize gideceğiz.|Tatilde Karadeniz'e gideceğiz.|Özel adlara gelen çekim ekleri kesmeyle ayrılır.
W|Bu kitabı okudunmu?|Bu kitabı okudun mu?|Soru eki “mı/mi” ayrı yazılır.
W|Sizde mi bu akşam sinemaya geliyorsunuz?|Siz de mi bu akşam sinemaya geliyorsunuz?|Bağlaç olan “de” ayrı yazılır.
W|Cumhuriyet bayramı coşkuyla kutlandı.|Cumhuriyet Bayramı coşkuyla kutlandı.|Bayram adlarının her sözcüğü büyük harfle başlar.
W|Bizde bu akşam size gelecektik.|Biz de bu akşam size gelecektik.|Bağlaç olan “de” ayrı yazılır.
W|Öğretmenler günü için öğrenciler küçük bir tören hazırladı.|Öğretmenler Günü için öğrenciler küçük bir tören hazırladı.|Belirli gün adlarının her sözcüğü büyük harfle başlar.
W|Yeni yasa TBMM'nde kabul edildi.|Yeni yasa TBMM'de kabul edildi.|Kısaltmalara ek getirilirken kısaltmanın okunuşu esas alınır; “TBMM'de” yazılır.
W|Bu soruyu sende biliyorsun.|Bu soruyu sen de biliyorsun.|Bağlaç olan “de” ayrı yazılır.
W|O da benim gibi İstanbul'ludur.|O da benim gibi İstanbulludur.|Özel adlara gelen yapım ekleri kesmeyle ayrılmaz.
W|Rüzgar sabahtan beri hiç dinmedi.|Rüzgâr sabahtan beri hiç dinmedi.|“Rüzgâr” sözcüğünde düzeltme işareti kullanılır.
W|Haftaya Pazartesi günü yola çıkacağız.|Haftaya pazartesi günü yola çıkacağız.|Belirli bir tarih bildirmeyen gün adları küçük harfle yazılır.
W|Bu konuyu birdaha konuşmayalım.|Bu konuyu bir daha konuşmayalım.|“Bir daha” ayrı yazılır.
C|Toplantıya birçok kişi katıldı.
C|Hiçbir şey söylemeden odadan çıktı.
C|Akşamki toplantıya ben de katılacağım.
C|Duydum ki yeni bir işe başlamışsın.
C|Her yıl mayıs ayında bu şenlik yapılır.
C|Toplantı 15 Mayıs 2026 tarihinde yapılacak.
C|Yazın Ege'ye, kışın ise Doğu Anadolu'ya gideriz.
C|Rüzgâr kuzeyden esiyor, hava giderek soğuyordu.
C|Dün akşam annem bize kek yaptı.
C|Yarınki sınava çok iyi hazırlandım.
C|Bugüne kadar hiç böyle bir şey görmedim.
C|Pek çok insan bu karara karşı çıktı.
C|Her şey yolunda gidiyor.
C|Birkaç gün sonra yeniden görüşeceğiz.
C|Bu işi yalnız başına bitirdi.
C|Türkçenin zengin bir söz varlığı vardır.
C|Ankaralı bir ailenin çocuğuydu.
C|Bu raporu TDK'ye gönderdik.
C|Tatilde Karadeniz'e gideceğiz.
C|Bu kitabı okudun mu?
C|Siz de mi bu akşam sinemaya geliyorsunuz?
C|Cumhuriyet Bayramı coşkuyla kutlandı.
C|Biz de bu akşam size gelecektik.
C|Kardeşim de bu kitabı çok beğendi.
C|Meclis bu yılki ilk oturumunu yaptı.
C|Herkes bu konuyu farklı yorumladı.
C|Ne yazık ki o gün toplantıya gelemedi.
C|Kitabın ikinci baskısı geçen ay çıktı.
C|Bu konuyu bir an önce çözmeliyiz.
C|Haftaya pazartesi günü yola çıkacağız.
C|Yeni yasa TBMM'de kabul edildi.
C|Bu konuyu bir daha konuşmayalım.
C|Kitabı okurken birçok yerin altını çizdim.
C|Tatilde Muğla'nın koylarını tek tek gezdik.
C|Bu yılki şenliğe her zamankinden daha çok kişi katıldı.
"""

# ---------------------------------------------------------------- noktalama (işlev)
# görev kodu|cümle  — cümlede (son nokta dışında) yalnız bu göreve ait işaret(ler) vardır.
NOKTALAMA_GOREV = {
    'V_ES': 'Virgül — eş görevli sözcükleri ayırmak',
    'V_SIR': 'Virgül — sıralı cümleleri birbirinden ayırmak',
    'V_HIT': 'Virgül — hitap sözünü cümleden ayırmak',
    'V_OZN': 'Virgül — yüklemden uzaktaki özneyi belirtmek',
    'V_ARA': 'Virgül — ara sözü cümleden ayırmak',
    'V_EVT': 'Virgül — “evet, hayır, peki” gibi cevap sözlerini cümleden ayırmak',
    'NV': 'Noktalı virgül — “ama, fakat, ancak” gibi bağlaçlardan önce cümleleri ayırmak',
    'IN_ACK': 'İki nokta — kendisinden sonra açıklama yapılacak sözden önce kullanılmak',
    'IN_KON': 'İki nokta — karşılıklı konuşmalarda konuşanın adından sonra kullanılmak',
    'K_OZ': 'Kesme işareti — özel adlara getirilen ekleri ayırmak',
    'K_KIS': 'Kesme işareti — kısaltmalara getirilen ekleri ayırmak',
    'K_SAY': 'Kesme işareti — sayılara getirilen ekleri ayırmak',
    'T_ALI': 'Tırnak işareti — başkasından olduğu gibi aktarılan sözü göstermek',
    'T_VUR': 'Tırnak işareti — özellikle belirtilmek istenen sözü göstermek',
    'T_ESR': 'Tırnak işareti — eser adını göstermek',
    'SI': 'Ayraç içinde soru işareti — bilginin kesin olmadığını belirtmek',
    'UN': 'Ayraç içinde ünlem — alay ya da küçümseme anlamı katmak',
    'KC': 'Kısa çizgi — “arasında, ile” anlamı vermek',
}
NOKTALAMA = """
V_ES|Elma, armut ve portakal aldık.
V_ES|Kitap, defter ve kalemlerini çantasına koydu.
V_ES|Kırmızı, beyaz ve sarı güller bahçeyi süslüyordu.
V_ES|Annem, babam ve kardeşim bu akşam sinemaya gidecek.
V_SIR|Kapıyı açtı, içeri girdi.
V_SIR|Yağmur dindi, güneş açtı.
V_SIR|Rüzgâr durdu, deniz duruldu.
V_SIR|Ders bitti, öğrenciler bahçeye koştu.
V_HIT|Sevgili dostum, mektubunu dün aldım.
V_HIT|Çocuklar, yarın erken toplanacağız.
V_HIT|Değerli konuklar, aramıza hoş geldiniz.
V_HIT|Arkadaşlar, bu konuyu yarın konuşalım.
V_OZN|Yazar, romanında köy hayatını anlatıyor.
V_OZN|Doktor, hastasına birkaç gün dinlenmesini önerdi.
V_OZN|Öğretmen, sınav sonuçlarını yarın açıklayacağını söyledi.
V_OZN|Komşumuz, bahçesinde yetiştirdiği domatesleri bize getirdi.
V_ARA|Babam, emekli bir öğretmen, her sabah gazetesini okur.
V_ARA|Bu romanı, yazarın en çok bilinen eserini, bir solukta okudum.
V_ARA|Komşumuz Ayşe Hanım, mahallenin en eski sakini, bize tatlı getirdi.
V_ARA|Dedem, köyün en yaşlı insanı, bize eski bayramları anlattı.
V_EVT|Evet, yarın toplantıya ben de geleceğim.
V_EVT|Hayır, bu konuda sana katılmıyorum.
V_EVT|Peki, nasıl istersen öyle olsun.
V_EVT|Tamam, akşam seni arayacağım.
NV|Çok çalıştı; ama sınavı kazanamadı.
NV|Seni aradım; fakat telefonun kapalıydı.
NV|Kitabı okudum; ancak sonunu pek beğenmedim.
NV|Erken yola çıktık; ama yine de trafiğe takıldık.
IN_ACK|Başarının sırrı tekti: çok çalışmak.
IN_ACK|Hayatta tek bir amacı vardı: iyi bir insan olmak.
IN_ACK|Yolculuk için yanına bir tek şey almıştı: eski bir defter.
IN_ACK|Bu işin en zor yanı belliydi: sabırlı olmak.
IN_KON|Öğretmen: Ödevlerinizi getirdiniz mi?
IN_KON|Satıcı: Size nasıl yardımcı olabilirim?
IN_KON|Müşteri: Bu ürünün başka rengi var mı?
K_OZ|Ankara'da üç gün kaldık.
K_OZ|Yunus Emre'nin şiirlerini okuyoruz.
K_OZ|Tatilde Antalya'ya gideceğiz.
K_OZ|Mehmet'i yıllardır görmedim.
K_KIS|Yeni yasa TBMM'de kabul edildi.
K_KIS|Raporu TDK'ye gönderdik.
K_KIS|Tören TRT'de canlı yayımlandı.
K_KIS|Bu bilgiye NATO'nun resmî sitesinden ulaştık.
K_SAY|Cumhuriyet 1923'te ilan edildi.
K_SAY|Toplantı saat 10'da başlayacak.
K_SAY|Bu yasa 2004'te yürürlüğe girdi.
K_SAY|Kitabın 3'üncü baskısı geçen ay çıktı.
T_ALI|Dedem her zaman “Sabreden derviş muradına ermiş.” derdi.
T_ALI|Annem “Akşama misafir gelecek.” dedi.
T_ALI|Kapıdaki görevli “Burada beklemeyin.” diye uyardı.
T_VUR|Bu öyküde “yalnızlık” kavramı farklı bir anlam kazanıyor.
T_VUR|Yazar “sabır” sözcüğünü bilerek her bölümde tekrarlıyor.
T_VUR|Bu şiirde “deniz” özgürlüğün simgesidir.
T_ESR|Dün akşam “Çalıkuşu” romanını bitirdim.
T_ESR|Kütüphaneden “Sinekli Bakkal” adlı romanı ödünç aldım.
T_ESR|Bu hafta derste “Kuyucaklı Yusuf” romanını inceleyeceğiz.
SI|Ünlü ozan 1520 (?) yılında doğmuştur.
SI|Bu cami 1550 (?) yılında yapılmıştır.
SI|Destanın ilk kez 1600 (?) yılında yazıya geçirildiği düşünülüyor.
UN|Çok çalışkan (!) arkadaşımız bu yıl da sınıfta kaldı.
UN|Pek cömert (!) komşumuz bize bir bardak su bile ikram etmedi.
UN|Dakik (!) arkadaşımız toplantıya yine bir saat geç geldi.
KC|Ankara-İstanbul hızlı treni her saat sefer yapıyor.
KC|1914-1918 yılları arasında büyük bir savaş yaşandı.
KC|Türkiye-Yunanistan maçı berabere bitti.
"""

# ---------------------------------------------------------------- cümle ögeleri
# Ögeler "metin/ETİKET" biçiminde, " | " ile ayrılır.
# Ö: özne, N: nesne, DT: dolaylı tümleç, ZT: zarf tümleci, Y: yüklem.
# "-la/ile" ve edat grupları zarf tümleci sayılır (güncel ortaöğretim terimleri).
OGE_AD = {'Ö': 'Özne', 'N': 'Nesne', 'DT': 'Dolaylı tümleç', 'ZT': 'Zarf tümleci', 'Y': 'Yüklem'}
OGE = """
Küçük kız/Ö | dün akşam/ZT | annesine/DT | güzel bir resim/N | çizdi/Y
Yaşlı adam/Ö | her sabah/ZT | parkta/DT | güvercinleri/N | besler/Y
Öğretmen/Ö | sınav kâğıtlarını/N | hafta sonu/ZT | evde/DT | okudu/Y
Bu yıl/ZT | köyümüze/DT | yeni bir okul/Ö | yapıldı/Y
Kardeşim/Ö | kitaplarını/N | özenle/ZT | rafa/DT | dizdi/Y
Akşamları/ZT | balkonda/DT | dedemle/ZT | satranç/N | oynarız/Y
Yarın sabah/ZT | trenle/ZT | Ankara'ya/DT | gideceğiz/Y
Bahçedeki ağaçların yaprakları/Ö | sonbaharda/ZT | sararır/Y
Annem/Ö | pazardan/DT | taze sebzeler/N | aldı/Y
Bu romanı/N | yazar/Ö | üç yılda/ZT | tamamlamış/Y
Sınavı kazanan öğrenciler/Ö | ödüllerini/N | törende/DT | aldılar/Y
Gece boyunca/ZT | sokakta/DT | köpekler/Ö | havladı/Y
Mektubu/N | postaneye/DT | ben/Ö | götürdüm/Y
Çocuklar/Ö | okul bahçesinde/DT | neşeyle/ZT | top/N | oynuyordu/Y
Dedem/Ö | gençliğinde/ZT | bu köprünün yapımında/DT | çalışmış/Y
Hasta/Ö | doktorun önerilerine/DT | dikkatle/ZT | uydu/Y
Bu kitabı/N | sana/DT | yarın/ZT | getiririm/Y
Yaz tatilinde/ZT | ailecek/ZT | Karadeniz'e/DT | gittik/Y
Pencereden/DT | içeri/ZT | serin bir rüzgâr/Ö | doldu/Y
Müdür/Ö | yeni öğretmeni/N | öğrencilere/DT | tanıttı/Y
Ağabeyim/Ö | geçen ay/ZT | yeni bir ev/N | satın aldı/Y
Kuşlar/Ö | kışın/ZT | sıcak ülkelere/DT | göç eder/Y
O/Ö | bu haberi/N | gazeteden/DT | öğrenmiş/Y
Kapının önünde/DT | iki küçük çocuk/Ö | bekliyordu/Y
Babam/Ö | arabayı/N | her hafta/ZT | yıkar/Y
Toplantıda/DT | yeni kararlar/Ö | alındı/Y
Ünlü yazar/Ö | son kitabını/N | okurlarına/DT | imzaladı/Y
Komşumuz/Ö | bize/DT | bir sepet elma/N | getirdi/Y
Sabahleyin/ZT | herkes/Ö | işine/DT | koşar/Y
Bu soruyu/N | sınıfta/DT | kimse/Ö | çözemedi/Y
Öğrenciler/Ö | müzeyi/N | rehberle birlikte/ZT | gezdi/Y
Gelecek hafta/ZT | sinemada/DT | yeni bir film/Ö | gösterilecek/Y
Çiftçiler/Ö | tarlalarını/N | ilkbaharda/ZT | sürer/Y
Kediler/Ö | güneşli bir köşede/DT | uyuyordu/Y
Arkadaşım/Ö | bana/DT | uzun bir mektup/N | yazdı/Y
Ders bittikten sonra/ZT | öğrenciler/Ö | bahçeye/DT | çıktı/Y
Annesinin sözlerini/N | hiç/ZT | unutmadı/Y
Uçak/Ö | gecikmeyle/ZT | piste/DT | indi/Y
Bu şehirde/DT | yıllardır/ZT | kimse/Ö | böyle bir kar/N | görmemişti/Y
Yazar/Ö | romanında/DT | köy hayatını/N | anlatıyor/Y
Bütün gün/ZT | evde/DT | kitap/N | okudum/Y
Rüzgâr/Ö | ağaçların dallarını/N | sertçe/ZT | salladı/Y
Misafirler/Ö | akşam yemeğinden sonra/ZT | salona/DT | geçti/Y
Ressam/Ö | tablosunu/N | yıllar sonra/ZT | bir müzeye/DT | bağışladı/Y
Her yaz/ZT | binlerce turist/Ö | bu koylara/DT | gelir/Y
Torunlarına/DT | dedeleri/Ö | eski masalları/N | anlatırdı/Y
"""

# ---------------------------------------------------------------- cümle türleri
# yüklem (F: fiil, I: isim, -: karışık) | yapı | diziliş | anlam (-: soruda kullanılmaz) | cümle
# Birleşik: fiilimsi, şart eki ya da "ki" ile kurulan yan cümle içerir.
# Sıralı/bağlı cümlelerde fiilimsi bulunmaz.
CUMLE_TURU = """
F|Basit|Kurallı|Olumlu|Annem pazardan taze sebzeler aldı.
I|Basit|Kurallı|Olumlu|Bu kitap çok ilginçti.
F|Basit|Devrik|Olumlu|Dün akşam bize geldi eski bir dostum.
I|Basit|Devrik|Olumsuz|Hiç de kolay değildi bu yılki sınav.
F|Basit|Kurallı|Soru|Yarın sinemaya gelecek misin?
I|Basit|Kurallı|Soru|Bu çanta senin mi?
F|Basit|Kurallı|Olumsuz|Kardeşim bu akşam bize gelmedi.
I|Basit|Kurallı|Olumsuz|Hava bugün pek soğuk değil.
F|Basit|Devrik|Soru|Gördün mü bu sabahki yağmuru?
I|Basit|Kurallı|Olumlu|Dedem köyün en yaşlı insanıdır.
F|Basit|Kurallı|Olumlu|Kuşlar kışın sıcak ülkelere göç eder.
I|Basit|Devrik|Olumlu|Çok güzeldi o eski bayramlar.
F|Basit|Devrik|Olumsuz|Bu yıl hiç kar yağmadı bizim köye.
I|Basit|Devrik|Soru|Senin mi bu kırmızı şemsiye?
F|Birleşik|Kurallı|Olumlu|Okula giderken yolda eski bir arkadaşıyla karşılaştı.
I|Birleşik|Kurallı|Olumlu|Bahçede açan çiçekler çok renkliydi.
F|Birleşik|Kurallı|Olumlu|Erken yatarsan sabah dinç uyanırsın.
F|Birleşik|Kurallı|Olumsuz|Ödevini bitirmeden dışarı çıkmadı.
I|Birleşik|Kurallı|Olumlu|En büyük isteği doktor olmaktı.
F|Birleşik|Devrik|Olumlu|Çok sevindim seni burada gördüğüme.
F|Birleşik|Kurallı|Soru|Annemin yaptığı keki beğendin mi?
F|Birleşik|Kurallı|Olumlu|Öğretmen yarın sınav olacağını söyledi.
F|Birleşik|Kurallı|Olumlu|Duydum ki yeni bir işe başlamışsın.
I|Birleşik|Kurallı|Olumsuz|Bu kitabı okumak hiç kolay değildi.
F|Birleşik|Devrik|Olumsuz|Kimseye söylemedi gördüklerini.
I|Birleşik|Kurallı|Soru|Okuduğun kitap güzel miydi?
I|Birleşik|Devrik|Olumlu|Çok güzeldi dün izlediğimiz film.
F|Sıralı|Kurallı|Olumlu|Kapıyı açtı, içeri girdi.
F|Sıralı|Kurallı|Olumlu|Yağmur dindi, güneş açtı.
I|Sıralı|Kurallı|Olumlu|Hava güzel, deniz sakindi.
F|Sıralı|Kurallı|Olumsuz|Bize gelmedi, haber göndermedi.
F|Sıralı|Kurallı|Soru|Ödevini yaptın mı, kitabını okudun mu?
I|Sıralı|Kurallı|Olumlu|Ev küçük, bahçe genişti.
F|Sıralı|Kurallı|Olumlu|Sabah erkenden kalktı, kahvaltısını yaptı, evden çıktı.
I|Sıralı|Kurallı|Olumsuz|Yemek sıcak değildi, çay taze değildi.
F|Bağlı|Kurallı|Olumlu|Çok çalıştı ve sınavı kazandı.
I|Bağlı|Kurallı|Olumlu|Ev küçüktü fakat çok kullanışlıydı.
F|Bağlı|Kurallı|Olumlu|Kitabı okudum ve çok beğendim.
I|Bağlı|Kurallı|Olumlu|Oda küçük ama aydınlıktı.
F|Bağlı|Kurallı|Olumlu|Hem şarkı söyledi hem dans etti.
F|Bağlı|Kurallı|-|Seni aradım ama ulaşamadım.
-|Bağlı|Kurallı|Olumlu|Erken yattım çünkü çok yorgundum.
F|Bağlı|Kurallı|-|Ne aradı ne de mesaj attı.
"""
