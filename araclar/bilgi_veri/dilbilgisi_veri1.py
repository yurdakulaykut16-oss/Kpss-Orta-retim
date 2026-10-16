"""KPSS Türkçe dil bilgisi ve anlam bankası (1): anlatım bozukluğu, cümlede anlam.

Her satır elle yazılmış ve tek tek denetlenmiş bir örnektir. Soru üreticisi
(dilbilgisi.py) bu örnekleri numaralı cümle / öncül biçiminde birleştirir; bu
yüzden her örneğin etiketi o boyutta TAM ve TEK olmalıdır (ör. "neden-sonuç"
etiketli cümlede amaç ya da koşul ilişkisi bulunmamalıdır).
"""

# ---------------------------------------------------------------- anlatım bozukluğu
# B|tür kodu|bozuk cümle|düzeltilmiş cümle|açıklama
# D|doğru cümle (bağımsız)
AB_TURLER = {
    'G': 'Gereksiz sözcük kullanılması',
    'A': 'Sözcüğün yanlış anlamda kullanılması',
    'O': 'Özne ile yüklem arasında kişi ya da sayı uyumsuzluğu',
    'E': 'Ortak kullanılan ögenin uygun olmaması (öge eksikliği)',
    'C': 'Çatı uyuşmazlığı',
    'M': 'Mantık hatası',
    'Z': 'Anlamca çelişen sözcüklerin bir arada kullanılması',
    'S': 'Sözcüğün cümlede yanlış yerde kullanılması',
    'K': 'Ek eksikliği ya da ek yanlışlığı',
    'B': 'Anlam belirsizliği',
}
# Birbirine karışabilecek türler aynı "neden" sorusunda seçenek olarak yan yana gelmez.
AB_KARISIR = [{'G', 'Z'}, {'A', 'M'}, {'E', 'K'}, {'O', 'K'}, {'S', 'B'}]

AB = """
B|G|Yaklaşık beş saat kadar süren toplantıda önemli kararlar alındı.|Yaklaşık beş saat süren toplantıda önemli kararlar alındı.|“Yaklaşık” ile “kadar” aynı anlamı (tahmini miktar) verdiğinden biri gereksizdir.
B|G|Bu konuyu ileride gelecekte yeniden ele alacağız.|Bu konuyu ileride yeniden ele alacağız.|“İleride” ile “gelecekte” aynı anlamdadır; biri gereksizdir.
B|G|Herkesin bildiği gibi, bu sorunun tek çözümü yalnızca diyalogdur.|Herkesin bildiği gibi, bu sorunun tek çözümü diyalogdur.|“Tek” sözcüğü “yalnızca” anlamını zaten karşıladığından “yalnızca” gereksizdir.
B|G|Kardeşim, geçen yıl kazandığı üniversitede şu anda hâlen ikinci sınıfta okuyor.|Kardeşim, geçen yıl kazandığı üniversitede hâlen ikinci sınıfta okuyor.|“Şu anda” ile “hâlen” aynı anlamdadır; biri gereksizdir.
B|G|Babam her sabah düzenli olarak her gün yürüyüş yapar.|Babam her sabah düzenli olarak yürüyüş yapar.|“Her sabah” sözü “her gün” anlamını içerdiğinden “her gün” gereksizdir.
B|G|Bu yarışmaya katılmak için mutlaka ve kesinlikle başvuru formunu doldurmanız gerekir.|Bu yarışmaya katılmak için başvuru formunu mutlaka doldurmanız gerekir.|“Mutlaka” ile “kesinlikle” aynı anlamdadır; biri gereksizdir.
B|G|Geçmişteki eski anılarını anlatırken gözleri doldu.|Geçmişteki anılarını anlatırken gözleri doldu.|“Geçmişteki” ile “eski” aynı anlamı verir; biri gereksizdir.
B|G|Kitabın ön sözünde, yazarın bu eseri yazma amacı ve gayesi açıklanıyor.|Kitabın ön sözünde, yazarın bu eseri yazma amacı açıklanıyor.|“Amaç” ile “gaye” eş anlamlıdır; biri gereksizdir.
B|G|Aşağı yukarı otuz kırk kişilik bir grup salonu doldurdu.|Otuz kırk kişilik bir grup salonu doldurdu.|“Otuz kırk” sözü yaklaşıklık bildirdiğinden “aşağı yukarı” gereksizdir.
B|G|Yeni açılan mağazada her şey ucuz fiyatlıydı.|Yeni açılan mağazada her şey ucuzdu.|“Ucuz” sözcüğü fiyatın düşük olduğunu zaten anlatır; “fiyatlı” gereksizdir.
B|G|Sınavda başarısız olmasının nedeni, derslerine yeterince önem vermemesinden kaynaklanıyor.|Sınavda başarısız olmasının nedeni, derslerine yeterince önem vermemesiydi.|“Nedeni” sözüyle “-den kaynaklanıyor” aynı işlevi görür; “kaynaklanıyor” gereksizdir.
B|G|Toplantıya katılan üyelerin hepsi de tümüyle bu öneriye karşı çıktı.|Toplantıya katılan üyelerin hepsi bu öneriye karşı çıktı.|“Hepsi” ile “tümüyle” aynı anlamı verir; biri gereksizdir.
B|A|Ev almayı düşündüğümüz semtte konut fiyatları çok pahalıymış.|Ev almayı düşündüğümüz semtte konut fiyatları çok yüksekmiş.|“Pahalı” sözcüğü malı niteler; fiyat “pahalı” olmaz, “yüksek” olur.
B|A|Müdür, yeni gelen memurun çalışkanlığını görünce ona karşı önyargılı davranmaya başladı.|Müdür, yeni gelen memurun çalışkanlığını görünce ona karşı olumlu davranmaya başladı.|Önyargı, bir şeyi tanımadan verilen yargıdır; çalışkanlığı görüldükten sonra oluşan tutum önyargı olamaz.
B|A|Sanatçı, sergisinde yer alan tabloların hepsini tek tek imal etmişti.|Sanatçı, sergisinde yer alan tabloların hepsini tek tek yapmıştı.|“İmal etmek” fabrikada üretmek anlamındadır; sanat eseri için uygun değildir.
B|A|Sevgili dostum, mektubunu alınca çok bedbaht oldum; uzun zamandır senden haber bekliyordum.|Sevgili dostum, mektubunu alınca çok sevindim; uzun zamandır senden haber bekliyordum.|“Bedbaht” mutsuz demektir; beklenen mektubu almanın sevinciyle uyuşmaz, sözcük yanlış anlamda kullanılmıştır.
B|A|Bu sanatçının resimlerinde doğa sevgisi belirsiz bir biçimde kendini gösterir ve hemen fark edilir.|Bu sanatçının resimlerinde doğa sevgisi belirgin bir biçimde kendini gösterir ve hemen fark edilir.|Hemen fark edilen bir özellik “belirsiz” değil “belirgin”dir; sözcük yanlış seçilmiştir.
B|M|Hasta, ameliyattan sonra hızla iyileşerek hastaneden taburcu olmayı başaramadı.|Hasta, ameliyattan sonra hızla iyileşerek hastaneden taburcu olmayı başardı.|Hızla iyileşen hastanın taburcu olamaması anlamca çelişir; yüklem yanlış seçilmiştir.
B|O|Sen ve kardeşin bu akşam bize gelecekler.|Sen ve kardeşin bu akşam bize geleceksiniz.|“Sen ve kardeşin” özneleri “siz” anlamı verir; yüklem “geleceksiniz” olmalıdır.
B|O|Bu konuda hem öğretmenler hem de ben çok uğraştı.|Bu konuda hem öğretmenler hem de ben çok uğraştık.|Özneler içinde “ben” bulunduğundan yüklem birinci çoğul kişiyle (“uğraştık”) çekimlenmelidir.
B|O|Evin pencereleri dünkü fırtınada kırıldılar.|Evin pencereleri dünkü fırtınada kırıldı.|İnsan dışındaki varlıkları bildiren çoğul özne tekil yüklem alır.
B|O|Bu yıl üretilen arabalar yurt dışına ihraç edildiler.|Bu yıl üretilen arabalar yurt dışına ihraç edildi.|Cansız varlık bildiren çoğul özneyle yüklem tekil kullanılır.
B|O|Siz bu konuyu benden daha iyi biliyor.|Siz bu konuyu benden daha iyi biliyorsunuz.|“Siz” öznesiyle yüklem “biliyorsunuz” biçiminde uyumlu olmalıdır.
B|O|Sen ve ben bu işi birlikte başaracaksınız.|Sen ve ben bu işi birlikte başaracağız.|“Sen ve ben” “biz” anlamı verir; yüklem “başaracağız” olmalıdır.
B|O|Kardeşimle ben tatilde dedemin köyüne gittiler.|Kardeşimle ben tatilde dedemin köyüne gittik.|Özne “kardeşimle ben” (biz) olduğundan yüklem “gittik” olmalıdır.
B|O|Bu sorunun çözümü için hepimiz elimizden geleni yapmalıdır.|Bu sorunun çözümü için hepimiz elimizden geleni yapmalıyız.|“Hepimiz” öznesi birinci çoğul kişidir; yüklem “yapmalıyız” olmalıdır.
B|E|Ailesini çok seviyor ve sık sık görüşüyor.|Ailesini çok seviyor ve onlarla sık sık görüşüyor.|“Sevmek” belirtme (-i), “görüşmek” “ile” ister; ortak kullanılan “ailesini” ikinci yükleme uymaz, “onlarla” eksiktir.
B|E|Spora ilgi duyuyor ama düzenli olarak yapamıyor.|Spora ilgi duyuyor ama onu düzenli olarak yapamıyor.|“İlgi duymak” yönelme (-e), “yapmak” belirtme (-i) ister; ikinci yüklemin nesnesi eksiktir.
B|E|Bu tür filmleri hem izliyor hem de çok hoşlanıyor.|Bu tür filmleri hem izliyor hem de onlardan çok hoşlanıyor.|“İzlemek” belirtme (-i), “hoşlanmak” ayrılma (-den) ister; “onlardan” eksiktir.
B|E|Doğaya saygı göstermeli, korumalıyız.|Doğaya saygı göstermeli, onu korumalıyız.|“Saygı göstermek” -e, “korumak” -i ister; ortak öge ikinci yükleme uymaz.
B|E|Kitaplarını çok seviyor, hiçbir zaman ayrılmıyor.|Kitaplarını çok seviyor, onlardan hiçbir zaman ayrılmıyor.|“Sevmek” -i, “ayrılmak” -den ister; “onlardan” eksiktir.
B|E|Bu mesleğe gönül vermiş, yıllarca uğraşmıştı.|Bu mesleğe gönül vermiş, onunla yıllarca uğraşmıştı.|“Gönül vermek” -e, “uğraşmak” “ile” ister; “onunla” eksiktir.
B|E|Eski dostlarını hiç unutmuyor, sık sık mektup yazıyor.|Eski dostlarını hiç unutmuyor, onlara sık sık mektup yazıyor.|“Unutmak” -i, “mektup yazmak” -e ister; “onlara” eksiktir.
B|C|Okulun bahçesine ağaç dikilmiş ve düzenli olarak sulamışlar.|Okulun bahçesine ağaç dikilmiş ve düzenli olarak sulanmış.|“Dikilmiş” edilgen, “sulamışlar” etken çatılıdır; yüklemler çatıca uyuşmaz.
B|C|Yeni yasa meclise sunuldu ve kısa sürede kabul ettiler.|Yeni yasa meclise sunuldu ve kısa sürede kabul edildi.|“Sunuldu” edilgen, “kabul ettiler” etkendir; çatı uyuşmazlığı vardır.
B|C|Toplantıda bu konular ayrıntılı biçimde konuşulmalı ve bir karara varmalıyız.|Toplantıda bu konular ayrıntılı biçimde konuşulmalı ve bir karara varılmalı.|Edilgen “konuşulmalı” ile etken “varmalıyız” bir arada kullanılmıştır.
B|C|Kaçak yapılar yıkılacak, yerine geniş bir park yapacaklar.|Kaçak yapılar yıkılacak, yerine geniş bir park yapılacak.|“Yıkılacak” edilgen, “yapacaklar” etken çatılıdır.
B|C|Sorunlar tek tek tespit edildi ve çözüm önerileri sundular.|Sorunlar tek tek tespit edildi ve çözüm önerileri sunuldu.|Edilgen “tespit edildi” ile etken “sundular” uyuşmaz.
B|C|Kitap yeniden basıldı ve kısa sürede okurlarına ulaştırdılar.|Kitap yeniden basıldı ve kısa sürede okurlarına ulaştırıldı.|“Basıldı” edilgen, “ulaştırdılar” etkendir.
B|M|Yazarın son kitabı okurlar tarafından büyük bir ilgisizlikle karşılandı ve kısa sürede tükendi.|Yazarın son kitabı okurlar tarafından büyük bir ilgiyle karşılandı ve kısa sürede tükendi.|İlgisizlikle karşılanan bir kitabın kısa sürede tükenmesi mantıkla çelişir.
B|M|Şirket bu yıl beklenenin üzerinde zarar ederek hissedarlarını sevindirdi.|Şirket bu yıl beklenenin üzerinde kâr ederek hissedarlarını sevindirdi.|Zarar etmenin hissedarları sevindirmesi mantığa aykırıdır.
B|M|Son on yılda kente göç edenlerin artmasıyla kentin nüfusu azaldı.|Son on yılda kente göç edenlerin artmasıyla kentin nüfusu arttı.|Kente göçün artması nüfusu azaltmaz; neden ile sonuç çelişmektedir.
B|M|Kitabı okumaya başlayınca bir türlü elimden bırakamadım; o kadar sıkıcıydı ki.|Kitabı okumaya başlayınca bir türlü elimden bırakamadım; o kadar sürükleyiciydi ki.|Sıkıcı bir kitabın elden bırakılamaması mantıkla çelişir.
B|M|Bu yıl yaşanan kuraklık nedeniyle tarlalardan geçen yıldan daha fazla ürün alındı.|Bu yıl yaşanan kuraklık nedeniyle tarlalardan geçen yıldan daha az ürün alındı.|Kuraklığın ürünü artırması mantığa aykırıdır.
B|M|Çocuklarına karşı çok hoşgörülü olduğu için onlara en küçük hatalarında bile ceza verirdi.|Çocuklarına karşı çok hoşgörülü olduğu için onların küçük hatalarını görmezden gelirdi.|Hoşgörülü olmak ile en küçük hataya ceza vermek arasında neden-sonuç ilişkisi kurulamaz.
B|M|Hasta, doktorun önerilerine hiç uymadığı için kısa sürede iyileşti.|Hasta, doktorun önerilerine uyduğu için kısa sürede iyileşti.|Önerilere uymamanın iyileşmeye neden olması mantıkla çelişir.
B|Z|Bu konuda kesinlikle haklı olabilirsiniz.|Bu konuda haklı olabilirsiniz.|“Kesinlikle” kesinlik, “-abilir” olasılık bildirir; birlikte kullanılamaz.
B|Z|Toplantıya galiba mutlaka o da katılacak.|Toplantıya galiba o da katılacak.|“Galiba” tahmin, “mutlaka” kesinlik bildirir; anlamca çelişir.
B|Z|Herhâlde sınav sonuçları kesin olarak yarın açıklanacak.|Herhâlde sınav sonuçları yarın açıklanacak.|“Herhâlde” ile “kesin olarak” çelişen anlamlar taşır.
B|Z|Salona yaklaşık tam olarak yüz kişi alınabiliyor.|Salona yaklaşık yüz kişi alınabiliyor.|“Yaklaşık” ile “tam olarak” birbiriyle çelişir.
B|Z|Belki de bu işi kesinlikle zamanında bitiremeyeceğiz.|Belki de bu işi zamanında bitiremeyeceğiz.|“Belki” olasılık, “kesinlikle” kesinlik bildirir.
B|Z|Bu akşam şüphesiz yağmur yağabilir.|Bu akşam yağmur yağabilir.|“Şüphesiz” kesinlik bildirirken “yağabilir” olasılık bildirir.
B|S|Kısa çocuğun saçları rüzgârda dağılmıştı.|Çocuğun kısa saçları rüzgârda dağılmıştı.|“Kısa” sözcüğü “saçlar”ı nitelemelidir; yanlış yerde kullanıldığı için çocuğu niteliyor.
B|S|Kırık çocuğun oyuncağını babası özenle tamir etti.|Çocuğun kırık oyuncağını babası özenle tamir etti.|“Kırık” oyuncağı nitelemeli; yanlış yerde olduğu için “çocuk”u niteliyor.
B|S|Sıcak bir bardak çay içip yola koyulduk.|Bir bardak sıcak çay içip yola koyulduk.|“Sıcak” sözcüğü “çay”ı nitelemeli; yeri yanlış olduğu için “bardak”ı niteliyor.
B|S|Soğuk bir şişe su alıp parka gittik.|Bir şişe soğuk su alıp parka gittik.|“Soğuk” suyu nitelemelidir; “şişe”nin önüne getirilmesi anlatımı bozmuştur.
B|S|Yaşlı köyün öğretmeni bize eski günleri anlattı.|Köyün yaşlı öğretmeni bize eski günleri anlattı.|“Yaşlı” öğretmeni nitelemelidir; yanlış yerde kullanıldığı için “köy”ü niteliyor.
B|K|Ben bu filmi daha önce izlemiş, arkadaşım ise hiç izlememişti.|Ben bu filmi daha önce izlemiştim, arkadaşım ise hiç izlememişti.|İki yargının kişileri farklı olduğundan ilk yüklemdeki ek ortak kullanılamaz; “izlemiştim” olmalıdır.
B|K|Okulumuzda düzenlenen yarışmada dereceye giren öğrencileri ödüllendirildi.|Okulumuzda düzenlenen yarışmada dereceye giren öğrenciler ödüllendirildi.|Edilgen yüklemin öznesi belirtme eki almaz; “öğrenciler” olmalıdır.
B|O|Ben her gün spor yapıyorum, kardeşim ise hiç yapmıyorum.|Ben her gün spor yapıyorum, kardeşim ise hiç yapmıyor.|İkinci yargının öznesi “kardeşim” (o) olduğu hâlde yüklem birinci kişi ekiyle çekimlenmiştir.
B|B|Ben de onu senin kadar özledim.|Ben de onu, senin onu özlediğin kadar özledim.|Cümle “senin onu özlediğin kadar” mı yoksa “seni özlediğim kadar” mı anlamında olduğu belirsizdir.
B|B|Arkadaşın evine gittik ama kimseyi bulamadık.|Arkadaşının evine gittik ama kimseyi bulamadık.|“Arkadaşın evi” sözü “senin arkadaşın” mı “arkadaşının evi” mi belirsizdir; ilgi/iyelik eki eksiktir.
B|B|Kardeşin arkadaşları bu akşam bize gelecek.|Kardeşinin arkadaşları bu akşam bize gelecek.|“Kardeşin” sözü “senin kardeşin” mi yoksa ilgi ekli “kardeşin (arkadaşları)” mı belirsizdir.
D|Toplantıda alınan kararlar, bütün çalışanlara yazılı olarak bildirildi.
D|Ben ve arkadaşım hafta sonu sinemaya gideceğiz.
D|Bu kitabı bir solukta okudum ve çok beğendim.
D|Yeni evimize taşındık ama henüz mahalleye alışamadık.
D|Müzeyi gezdik, sergilenen eserlere hayran kaldık.
D|Ağaçlar sonbaharda yapraklarını döktü.
D|Akşam yemeğinden sonra tatlı olarak sütlaç ikram edildi.
D|Yazar, romanında köy yaşamını bütün gerçekliğiyle ele almış; olayları abartmaktan kaçınmıştır.
D|Uzmanlar, binaların denetiminin artırılması gerektiğini vurguladı.
D|Kazada yaralananlar ambulansla en yakın hastaneye kaldırıldı.
D|Öğretmen, öğrencilere ödevlerini zamanında teslim etmelerini hatırlattı.
D|Doktor, hastanın birkaç gün daha hastanede kalması gerektiğini söyledi.
D|Bu konuda sizinle aynı fikirde değilim ama görüşlerinize saygı duyuyorum.
D|Yağmur dinince maç kaldığı yerden yeniden başladı.
D|Sınav sonuçlarının önümüzdeki hafta açıklanması bekleniyor.
D|Bu kentin tarihî dokusu, özenle yapılan restorasyonlarla korunmaya çalışılıyor.
D|Ne yazık ki bu yıl kuraklık nedeniyle tarlalardan beklenen ürün alınamadı.
D|Toplantıya büyük olasılıkla o da katılacak.
D|Çocukların dengeli beslenmesi, sağlıklı büyümelerinde önemli bir rol oynar.
D|Romanın kahramanı, yaşadığı kasabadan ayrılıp büyük şehre yerleşir.
D|Gece boyunca yağan kar, sabah bütün yolları kapatmıştı.
D|Kütüphaneye yeni gelen kitaplar raflara yerleştirildi.
D|Bu şehre ilk geldiğimde sokakları çok dar ve karışık bulmuştum.
D|Yarışmaya katılanların çoğu, ilk kez böyle bir deneyim yaşadıklarını söyledi.
D|Babamın en büyük hayali, emekli olunca köyüne dönmektir.
D|Komşumuz, bahçesinde yetiştirdiği domateslerden bize de bir sepet getirdi.
D|Sergiyi gezenler, genç ressamın renk kullanımını çok beğendi.
D|Belediye, kentin dört bir yanına yeni bisiklet yolları yapmayı planlıyor.
"""

# ---------------------------------------------------------------- cümlede anlam ilişkileri
# Her cümlede yalnız bir ilişki bulunur.
ILISKI_AD = {'NS': 'neden-sonuç', 'AS': 'amaç-sonuç', 'KS': 'koşul-sonuç', 'KR': 'karşılaştırma'}
ILISKI = """
NS|Yağmur çok yağdığı için maç ertelendi.
NS|Gece geç yattığından sabah derse yetişemedi.
NS|Yollar buz tuttuğundan okullar tatil edildi.
NS|Çok çalıştığından sınavı kolayca kazandı.
NS|Hastalandığı için toplantıya katılamadı.
NS|Trafik sıkışık olduğundan uçağı kaçırdı.
NS|Sesi kısıldığından konserini iptal etmek zorunda kaldı.
NS|Kitabın son sayfaları eksik olduğu için romanın sonunu öğrenemedim.
NS|Bütün gün yürüdüğümüzden akşam çok yorulmuştuk.
NS|Su borusu patladığı için mahallede sular kesildi.
NS|Çok heyecanlandığından sahnede sözlerini unuttu.
NS|Rüzgâr şiddetlendiği için vapur seferleri iptal edildi.
NS|Erken yola çıktığımızdan trafiğe takılmadık.
NS|Ödevini yapmadığı için öğretmeninden uyarı aldı.
NS|Fiyatlar çok yükseldiği için bu yıl tatile çıkamadık.
AS|Sınavı kazanmak için gece gündüz çalışıyor.
AS|Trene yetişmek için koşarak istasyona gitti.
AS|Kilo vermek amacıyla her gün yürüyüş yapıyor.
AS|Annesini sevindirmek için evi baştan sona temizledi.
AS|Daha iyi bir iş bulmak için İngilizce kursuna yazıldı.
AS|Sesini duyurabilmek için mikrofona yaklaştı.
AS|Çocuklar uyanmasın diye parmaklarının ucuna basarak yürüdü.
AS|Güneşin doğuşunu izlemek üzere sabah erkenden tepeye çıktık.
AS|Kitabı zamanında yetiştirmek için yazar aylarca evden çıkmadı.
AS|Üşümemek için kalın bir mont giydi.
AS|Yeni şehrini tanımak amacıyla her hafta sonu farklı bir semti geziyor.
AS|Ödevine kaynak bulmak için kütüphaneye gitti.
AS|Bitkiler kurumasın diye onları her akşam suluyor.
AS|Toplantıya geç kalmamak için taksiye bindi.
AS|Arkadaşına sürpriz yapmak için doğum günü pastasını gizlice hazırladı.
KS|Erken yatarsan sabah dinç uyanırsın.
KS|Hava güzel olursa pikniğe gideceğiz.
KS|Düzenli çalışmazsan sınavda başarılı olamazsın.
KS|Bu ilacı aç karnına içersen miden ağrıyabilir.
KS|Biletleri bugün alırsak indirimden yararlanabiliriz.
KS|Kar yağmaya devam ederse yollar kapanacak.
KS|Toplantı uzarsa akşam yemeğine yetişemem.
KS|Sözünü tutarsan sana yeniden güvenirim.
KS|Bitkiyi güneş alan bir yere koyarsan daha hızlı büyür.
KS|Bu kitabı okursan yazarın diğer eserlerini de merak edersin.
KS|Kurallara uymazsan cezayla karşılaşırsın.
KS|Erken gelirsen seni istasyonda karşılarım.
KS|Yağmur yağmazsa bu yıl ürün az olacak.
KS|Kapıyı kilitlemezsen eve hırsız girebilir.
KR|Bu yılki yarışma geçen yılkinden çok daha çekişmeli geçti.
KR|Kardeşim benden daha uzun boyludur.
KR|Yazarın yeni romanı ilk romanı kadar sürükleyici değil.
KR|Kentte yaşam köydekine göre çok daha hızlı akıyor.
KR|Bu yolun trafiği diğerinden daha az.
KR|Onun resimleri, hocasınınkiler kadar renkli ve canlıdır.
KR|Kıyıdaki kasabalar iç kesimdekilerden daha ılıman bir iklime sahiptir.
KR|Bu bilgisayar eskisinden iki kat daha hızlı çalışıyor.
KR|Kitabın ikinci bölümü birinci bölümden daha akıcı yazılmış.
KR|Bu dağın zirvesi komşu dağlardan çok daha yüksektir.
KR|Şiirlerinde, öykülerindeki kadar ince bir mizah yoktur.
KR|Bu yılki hasat geçen yılınkinden daha bereketli oldu.
"""

# ---------------------------------------------------------------- anlam türleri (tek anlam)
ANLAM_AD = {'TAN': 'tanımlama', 'ONE': 'öneri', 'TAH': 'tahmin', 'ABA': 'abartma', 'ELE': 'eleştiri',
            'PIS': 'pişmanlık', 'ONY': 'ön yargı', 'SIT': 'sitem', 'OZL': 'özlem'}
ANLAM = """
TAN|Deneme, yazarın herhangi bir konudaki kişisel görüşlerini kesin yargılara varmadan anlattığı yazı türüdür.
TAN|Ada, dört tarafı sularla çevrili kara parçasıdır.
TAN|Biyografi, tanınmış bir kişinin hayatını anlatan yazı türüdür.
TAN|Erozyon, toprağın rüzgâr ve su gibi etkenlerle aşınıp taşınmasıdır.
TAN|Fabl, hayvanların konuşturulduğu ve sonunda bir ders verilen kısa anlatılardır.
TAN|Termometre, sıcaklığı ölçmeye yarayan bir araçtır.
TAN|Sözlük, bir dilin sözcüklerini belli bir düzen içinde açıklayan kitaptır.
TAN|Mektup, uzaktaki birine duygu ve düşünceleri iletmek için yazılan yazıdır.
ONE|Bu kitabı okumadan önce yazarın ilk romanına göz atmanızı öneririm.
ONE|Yorgun hissettiğinde kısa bir yürüyüşe çıkmayı denemelisin.
ONE|Bu tatilde kalabalık şehirler yerine sakin bir kasabayı seçmenizi tavsiye ederim.
ONE|Kahvaltıyı atlamamalı, güne sağlıklı bir öğünle başlamalısınız.
ONE|Yeni başlayan yazarlar, ilk kitaplarını yayımlatmakta acele etmemeli.
ONE|Çocuğunuzun ekran süresini sınırlandırıp onunla daha çok kitap okumanızı öneririz.
ONE|Sınava hazırlanırken her gün en az bir deneme çözmeni tavsiye ederim.
ONE|Bu kadar yoğun çalışacaksan arada kısa molalar vermeyi ihmal etmemelisin.
TAH|Bu gidişle yarışmayı bizim takım kazanacak gibi görünüyor.
TAH|Hava kararıyor; galiba akşama doğru yağmur yağacak.
TAH|Sanırım toplantı beklenenden uzun sürecek.
TAH|Yeni film, gişede rekor kıracağa benziyor.
TAH|Bu yıl kış oldukça sert geçecek gibi.
TAH|Herhâlde otobüs yine trafiğe takıldı.
TAH|Muhtemelen bu sorunu yarın akşama kadar çözeriz.
TAH|Yüzündeki ifadeye bakılırsa sınavı iyi geçmiş olmalı.
ABA|Onu görmeyeli bin yıl oldu.
ABA|Bu çanta öyle ağırdı ki taşırken kollarım koptu.
ABA|Fıkrayı duyunca gülmekten kırıldık.
ABA|Bu soğukta kemiklerim bile dondu.
ABA|Telefonda saatlerce, belki bir asır konuştular.
ABA|Yemek o kadar acıydı ki ağzımdan alevler çıktı.
ABA|Bu dağ kadar ödevi bir gecede nasıl bitireyim?
ABA|Sabahtan beri yürümekten ayaklarım dizlerime kadar aşındı.
ELE|Yazar, romanın sonunu aceleye getirmiş; karakterlerin değişimini inandırıcı kılamamış.
ELE|Filmde görüntüler etkileyici olsa da senaryo oldukça zayıf kalmış.
ELE|Şair son kitabında kendini tekrar etmekten kurtulamamış.
ELE|Bu sergide eserler gelişigüzel yerleştirilmiş, ziyaretçi neye bakacağını şaşırıyor.
ELE|Dizinin son bölümleri, hikâyeyi gereksiz yere uzatmaktan öteye geçmiyor.
ELE|Oyunun dekorları göz alıcı ama oyuncuların performansı bunun çok gerisinde kalmış.
ELE|Ders kitabındaki konular birbirinden kopuk, örnekler de öğrencinin dünyasından uzak.
PIS|Keşke o gün onu dinleseydim.
PIS|Gençliğimde daha çok kitap okumadığım için şimdi hayıflanıyorum.
PIS|O sözleri söylemeseydim şimdi aramız bozulmazdı.
PIS|Eski dostuma vaktinde bir telefon açmadığım için kendime kızıyorum.
PIS|O teklifi kabul etmeliydim; fırsatı kaçırdığıma hâlâ üzülüyorum.
PIS|Ah, o yıllarda biraz daha sabırlı olabilseydim!
PIS|Sınava son haftada değil de en baştan hazırlansaydım bu sonucu almazdım.
ONY|Bu yazarın kitabını hiç okumadım ama sıkıcı olduğundan eminim.
ONY|Yeni gelen öğretmeni henüz tanımıyorum ama çok sert biri olduğu belli.
ONY|Bu filmi izlemeye gerek yok; o yönetmenin bütün filmleri kötüdür.
ONY|Daha tatmadan bu yemeği beğenmeyeceğimi biliyorum.
ONY|O mahalleden kimseyle arkadaşlık etmem; orada oturanların hepsi kabadır.
ONY|Konuşmasını dinlemeden onun söyleyeceklerinin yanlış olduğunu söyleyebilirim.
SIT|Bunca yıllık dostun olarak bir telefonu bile çok mu gördün?
SIT|Hastalandığımda bir kez olsun aramadın; ben senden bunu beklemezdim.
SIT|Doğum günümü herkes hatırladı, bir tek sen unuttun.
SIT|Yıllarca seni bekledim; sen bir mektup bile yazmadın.
SIT|Bu kadar emek verdim, sen bir teşekkürü bile esirgedin.
SIT|Şehre geldiğini başkalarından duydum, bana haber vermeye bile gerek görmedin.
OZL|Çocukluğumun geçtiği o küçük kasabayı, sokaklarındaki ıhlamur kokusunu çok özledim.
OZL|Annemin pişirdiği tarhana çorbasının tadını yıllardır arıyorum.
OZL|Gurbette geçen her gün memleketimin dağlarını biraz daha özlüyorum.
OZL|Yıllar geçse de köydeki evimizin bahçesini, dut ağacının gölgesini unutamıyorum.
OZL|Okul arkadaşlarımla bahçede koşturduğumuz o günler gözümde tütüyor.
OZL|Uzaklarda yaşayan kardeşimin sesini duymak için sabırsızlanıyorum.
"""
# Tanımlamada kişisel duygu bulunmaz; ön yargı ile tahmin, sitem ile eleştiri, özlem ile
# pişmanlık yakın çeldiricilerdir ama örnekler bu ayrımlar net olacak biçimde yazılmıştır.

# ---------------------------------------------------------------- öznel / nesnel yargı
OZNEL = """
N|Türkiye'nin en yüksek dağı Ağrı Dağı'dır.
N|Su, deniz seviyesinde 100 derecede kaynar.
N|Kitap, on iki bölümden oluşuyor.
N|Kütüphane, hafta sonları saat on yedide kapanır.
N|Toplantıya kırk iki kişi katıldı.
N|Şair, ilk şiirlerinde aruz ölçüsünü kullanmıştır.
N|Romanda olaylar İstanbul'da geçmektedir.
N|Ankara, Türkiye'nin başkentidir.
N|Dünya, Güneş'in çevresindeki bir turunu yaklaşık 365 günde tamamlar.
N|Eser, yazarın ölümünden sonra yayımlanmıştır.
N|Öykünün kahramanı emekli bir öğretmendir.
N|Bu köprünün uzunluğu bin metreyi aşar.
N|Yazar, bu romanında köyden kente göçü anlatır.
N|Sergide genç ressamın otuz tablosu yer alıyor.
O|Bu romanın en etkileyici yanı, sade ve içten dilidir.
O|Şairin son kitabı, önceki kitaplarından çok daha başarılı.
O|İstanbul, dünyanın en güzel şehridir.
O|Bu film, izlediğim en sıkıcı filmlerden biriydi.
O|Yazarın üslubu okuru yormayan bir akıcılığa sahip.
O|Bence bu sorunun en doğru çözümü diyalogdur.
O|Romanın sonu, okuru derinden sarsan bir hüzünle bitiyor.
O|Bu köprü, kentin en zarif yapılarından biri.
O|Öykünün kahramanı, okurun kolayca sevebileceği sıcak bir karakter.
O|Sanatçının resimlerinde renkler çok uyumlu kullanılmış.
O|Kütüphanenin yeni binası eskisinden çok daha ferah ve kullanışlı.
O|Kitabın kapak tasarımı oldukça zevksiz olmuş.
O|Sergideki tablolar, ressamın en olgun dönemini yansıtıyor.
O|Bu yazarın romanları gereğinden uzun ve ağır.
"""
