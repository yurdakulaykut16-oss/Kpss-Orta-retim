"""KPSS Türkçe bankası (3): sözcük türleri, sözcükte yapı, gerçek/mecaz anlam.

Köşeli ayraç içindeki sözcük, soruda tırnak içinde gösterilir ve yalnız o sözcük
değerlendirilir.
"""

# tür | cümle ([...] incelenen sözcük)
SOZCUK_TURU = """
Sıfat|[Güzel] bir gün geçirdik.
Zarf|Çocuk şarkıyı çok [güzel] söyledi.
İsim|Ressam, [güzeli] çirkinden ayırmayı öğrencilerine öğretiyordu.
Zarf|Bu kitabı [çok] beğendim.
Sıfat|[Çok] insan bu karara karşı çıktı.
Sıfat|[Bu] kitabı daha önce okudun mu?
Zamir|[Bu], benim en sevdiğim kitaptır.
Edat|Senin [için] her şeyi yaparım.
Edat|Arkadaşı [ile] sinemaya gitti.
Bağlaç|Ali [ile] Ayşe aynı sınıfta okuyor.
Bağlaç|Çok çalıştı [ama] sınavı kazanamadı.
Bağlaç|Ben [de] yarın toplantıya geleceğim.
Edat|Kardeşi [gibi] o da çok çalışkandır.
Sıfat|[Yalnız] bir adam kapıda bekliyordu.
Bağlaç|Seninle gelirim, [yalnız] erken dönmeliyim.
Zarf|Haberi alınca [hemen] eve döndü.
Zarf|[Akşam] bize misafir gelecek.
İsim|Bütün gün [akşamı] dört gözle bekledi.
Zarf|Merdivenlerden [yukarı] çıktı.
İsim|Evin [yukarısı] kışın çok soğuk olur.
Zamir|[Kimse] bu soruyu çözemedi.
Zamir|[Herkes] onun bu davranışını takdir etti.
Sıfat|[Hangi] kitabı almak istiyorsun?
Zarf|Bu soruyu [nasıl] çözdün?
Sıfat|O [nasıl] bir insandır, biliyor musun?
Ünlem|[Eyvah], otobüsü kaçırdık!
Ünlem|[Ah], ne güzel günlerdi onlar!
Edat|Akşamüstü eve [doğru] yürümeye başladı.
Sıfat|Sınavda [doğru] cevabı bulan tek kişi oydu.
Edat|Akşama [kadar] hiç durmadan çalıştı.
Edat|Dersten [sonra] kütüphanede buluşalım.
Zarf|Bu konuyu [sonra] konuşuruz.
Edat|Yemekten [önce] ellerimizi yıkadık.
Zarf|Bu filmi daha [önce] izlemiştim.
Bağlaç|Davet edildi [ancak] toplantıya gelmedi.
Sıfat|O, çok [iyi] bir insandır.
Zarf|Toplantıda çok [iyi] konuştu.
Zamir|[Ben] yarın erkenden yola çıkacağım.
Zamir|Bu işi tek başına [kendisi] yaptı.
Sıfat|[Birkaç] gün sonra köyüne döndü.
Zamir|Öğrencilerin [birçoğu] sınavı geçti.
Sıfat|[Hızlı] tren seferleri yeniden başladı.
Zarf|Yarışta en [hızlı] o koştu.
Zarf|[Dün] sinemaya gittik.
İsim|[Dünü] unutalım, yarına bakalım.
Zarf|Kapıyı çalmadan [içeri] girdi.
İsim|[İçerisi] çok sıcak ve havasızdı.
Bağlaç|Kitaplar [ve] defterler masanın üstünde duruyordu.
Edat|Denize [karşı] oturup çay içtik.
Bağlaç|Bir de baktım [ki] kapı açık kalmış.
Zamir|[Onlar] bu akşam bize gelecekler.
Sıfat|[Bazı] öğrenciler ödevlerini getirmemişti.
Zamir|[Bazıları] bu kararı doğru bulmadı.
Sıfat|[Her] sabah erkenden yürüyüşe çıkar.
Zarf|Dedem [yavaş yavaş] yürüyordu.
Sıfat|[Yavaş] adımlarla yanımıza geldi.
İsim|[Gençler] bu etkinliğe büyük ilgi gösterdi.
Sıfat|[Genç] öğretmen sınıfa girince herkes sustu.
Ünlem|[Hey], oraya girmek yasak!
Bağlaç|[Hem] okuyor hem çalışıyordu.
Edat|Sabaha [dek] uyuyamadı.
Zarf|Yazar, olayları [açıkça] anlatmış.
"""

# Sözcükte yapı: B basit, T türemiş (yapım eki almış), Bİ birleşik
YAPI_AD = {'B': 'basit', 'T': 'türemiş', 'Bİ': 'birleşik'}
YAPI = """
B|kitap
B|göz
B|deniz
B|kalem
B|ağaç
B|taş
B|masa
B|çiçek
B|kuş
B|dağ
B|bulut
B|demir
B|duvar
B|ev
B|yol
B|su
B|at
B|baş
B|kar
T|gözlük
T|kitaplık
T|yolcu
T|sevgi
T|bilgi
T|balıkçı
T|tuzluk
T|kalemlik
T|denizci
T|başlık
T|evcil
T|dilek
T|çiçekçi
T|sulak
T|dağcı
T|sevinç
T|ödev
T|yazar
T|tuzlu
T|gözcü
Bİ|hanımeli
Bİ|kahverengi
Bİ|buzdolabı
Bİ|demiryolu
Bİ|açıkgöz
Bİ|bilgisayar
Bİ|cumartesi
Bİ|ayakkabı
Bİ|kuşbaşı
Bİ|keçiboynuzu
Bİ|aslanağzı
Bİ|başöğretmen
Bİ|gökdelen
Bİ|ateşböceği
Bİ|karabiber
Bİ|denizaltı
Bİ|külbastı
Bİ|suçiçeği
"""

# Gerçek (G) / mecaz (M) anlam — incelenen sözcük köşeli ayraç içinde.
MECAZ = """
G|ağır|Bu sandık çok [ağır], tek başıma kaldıramam.
M|ağır|Arkadaşının [ağır] sözleri onu çok üzdü.
G|sıcak|[Sıcak] çorbayı içince hepimiz ısındık.
M|sıcak|Ev sahipleri bizi çok [sıcak] bir tavırla karşıladı.
G|soğuk|Terliyken [soğuk] su içme, boğazın ağrır.
M|soğuk|Yeni komşumuz bize karşı çok [soğuk] davranıyor.
G|kırmak|Çocuk topla mutfağın camını [kırdı].
M|kırmak|Bu sözlerinle annenin kalbini [kırdın].
G|tatlı|Bu karpuz bal gibi [tatlı] çıktı.
M|tatlı|Bebeğin [tatlı] gülüşü herkesi büyüledi.
G|keskin|[Keskin] bıçakla ekmeği dilimledi.
M|keskin|Onun [keskin] zekâsı herkesi şaşırttı.
G|yumuşak|[Yumuşak] bir yastıkta deliksiz uyudu.
M|yumuşak|Babam çok [yumuşak] huylu bir insandır.
G|derin|Köyün dışındaki kuyu çok [derin].
M|derin|Yazar, mektubu okuyunca [derin] düşüncelere daldı.
G|karanlık|[Karanlık] odada hiçbir şey göremedik.
M|karanlık|Bu olay, tarihin [karanlık] sayfalarından biridir.
G|boş|[Boş] şişeleri geri dönüşüm kutusuna attık.
M|boş|Bu [boş] sözlere artık kimse inanmıyor.
G|sert|Bu ekmek çok [sert], ısırılmıyor.
M|sert|Müdür, geç kalan memura [sert] bir dille çıkıştı.
G|acı|Salatadaki biber çok [acı] çıktı.
M|acı|Sabah erken saatte [acı] bir haber aldık.
G|parlak|[Parlak] ayakkabılarıyla salona girdi.
M|parlak|Sınıfın en [parlak] öğrencisi oydu.
G|temiz|[Temiz] havlularla ellerimizi kuruladık.
M|temiz|Dedemin çok [temiz] bir kalbi vardı.
G|ince|[İnce] bir kumaştan yazlık bir elbise dikti.
M|ince|Komşumuz çok [ince] düşünceli bir insandır.
G|kör|Doğuştan [kör] olan sanatçı, müzikte büyük başarı kazandı.
M|kör|Bu konuda öfkesi gözünü [kör] etmişti.
G|yıkmak|Belediye eski binayı [yıktı].
M|yıkmak|Aldığı kötü haber onu [yıktı].
G|ateş|Kamp yerinde bir [ateş] yakıp ısındık.
M|ateş|Sınav haftası öğrencileri bir [ateş] sardı.
G|çürük|Sepetteki [çürük] elmaları ayıkladık.
M|çürük|Bu [çürük] gerekçeye kimse inanmadı.
"""
