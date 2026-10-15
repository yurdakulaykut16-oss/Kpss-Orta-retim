"""Türkçe bilgi tabloları: deyim, atasözü, eş/zıt anlam, Türkçe karşılıklar,
kısaltmalar, yazım, ses olayları, fiilimsiler ve kaba kuvvetle doğrulanan
sözel mantık soruları.

Anlamca yakın kayıtlar aynı etiketi taşır; bir kaydın çeldiricileri asla aynı
etiketten seçilmez, böylece birden fazla doğru cevap oluşmaz.
"""
from itertools import permutations

from .ortak import q, sec

# deyim | anlam | etiket
DEYIMLER = """
ağzı kulaklarına varmak|çok sevinmek|sevinç
eli kulağında olmak|bir şeyin gerçekleşmesi çok yakın olmak|yakın
göz yummak|bir yanlışı görmezden gelmek|hoşgörü
kulak asmamak|söyleneni önemsememek, dinlememek|önemseme
dili tutulmak|heyecan ya da korku yüzünden konuşamaz hâle gelmek|şaşkınlık
etekleri tutuşmak|çok telaşlanmak|telaş
burnu havada olmak|kendini beğenmiş, kibirli olmak|kibir
ayağını denk almak|dikkatli ve tedbirli davranmak|dikkat
kılı kırk yarmak|en ince ayrıntısına kadar titizlik göstermek|titizlik
pabucu dama atılmak|yerine başkası geçtiği için eski değerini yitirmek|değer
ateş pahası|çok pahalı|pahalı
eli açık|cömert|cömert
eli sıkı|cimri|cimri
göz boyamak|aldatıcı davranışlarla iyi izlenim bırakmaya çalışmak|aldatma
kafa tutmak|karşı gelmek, direnmek|karşı
dört gözle beklemek|büyük bir özlem ve istekle beklemek|bekleme
yüzü kızarmak|utanmak|utanç
küplere binmek|çok öfkelenmek|öfke
tepesi atmak|birden sinirlenmek|öfke
içi içine sığmamak|sevinç ya da heyecandan yerinde duramamak|sabırsız
gözden düşmek|itibarını, sevgisini yitirmek|değer
ağzı sıkı|sır saklayan|sır
ağzında bakla ıslanmamak|hiçbir sırrı saklayamamak|sır
baltayı taşa vurmak|farkında olmadan kırıcı söz söylemek|pot
pot kırmak|yersiz söz ya da davranışla uygunsuz duruma düşmek|pot
dut yemiş bülbül gibi|susup hiç konuşmayan|susma
kulak kabartmak|gizlice dinlemeye çalışmak|dinleme
can kulağıyla dinlemek|büyük bir dikkatle dinlemek|dinleme
nabzına göre şerbet vermek|kişinin hoşuna gidecek biçimde davranmak|yaranma
ayvayı yemek|kötü bir duruma düşmek|zor
dara düşmek|sıkıntılı duruma düşmek, parasız kalmak|zor
elinden tutmak|yardım etmek, desteklemek|yardım
sırt çevirmek|ilgisini kesmek, yüz çevirmek|ilgi
göz atmak|kısaca bakmak|bakma
göz kulak olmak|korumak, gözetmek|koruma
göze girmek|beğenilip sevgi kazanmak|beğenme
göz koymak|ele geçirmeyi istemek|istek
burun kıvırmak|beğenmemek, küçümsemek|küçümseme
iğneyle kuyu kazmak|güç bir işi büyük sabırla yapmaya çalışmak|sabır
deveye hendek atlatmak|çok zor bir işi başarmaya uğraşmak|zorluk
su koyvermek|işi bozmak, uyumsuzluk çıkarmak|bozma
suya sabuna dokunmamak|başını belaya sokacak işlere karışmamak|kaçınma
sudan çıkmış balığa dönmek|bulunduğu ortamda bunalmak, uyum sağlayamamak|uyum
havadan sudan konuşmak|önemsiz konular üzerine konuşmak|konuşma
ipe un sermek|bir işi yapmamak için bahaneler ileri sürmek|bahane
kırk dereden su getirmek|bir isteği yerine getirmemek için türlü sebepler sıralamak|bahane
ipin ucunu kaçırmak|bir işi denetim altında tutamaz duruma gelmek|denetim
kendi göbeğini kendi kesmek|işini başkasının yardımı olmadan kendisi görmek|bağımsız
bindiği dalı kesmek|kendi çıkarına zarar verecek davranışta bulunmak|zarar
kuyusunu kazmak|birine gizlice kötülük hazırlamak|kötülük
başına çorap örmek|birinin zararına olacak işleri gizlice düzenlemek|kötülük
sözünü tutmak|verdiği söze uymak|söz
ağzından kaçırmak|söylememesi gereken bir şeyi istemeden söylemek|sır
baş göstermek|ortaya çıkmak|ortaya
baş kaldırmak|isyan etmek|karşı
başı göğe ermek|çok onurlanmak, büyük mutluluk duymak|sevinç
başını taştan taşa vurmak|yaptığı işten çok pişman olmak|pişman
eli kolu bağlı kalmak|hiçbir şey yapamayacak duruma düşmek|çaresiz
kolu kanadı kırılmak|güçsüz ve çaresiz kalmak|çaresiz
omuz omuza vermek|birlikte çalışıp dayanışmak|dayanışma
bir taşla iki kuş vurmak|bir işle iki yarar sağlamak|yarar
elini çabuk tutmak|acele etmek|acele
yangından mal kaçırır gibi|büyük bir telaş ve aceleyle|acele
apar topar|aceleyle, alelacele|acele
abayı yakmak|âşık olmak|aşk
gönlünü almak|kırılan birini hoşnut etmek|gönül
kalbini kırmak|üzmek, incitmek|incitme
içi kan ağlamak|derin bir acı duymak|acı
ciğeri yanmak|çok büyük acı çekmek|acı
kan ter içinde kalmak|çok yorulup terlemek|yorgunluk
ağzıyla kuş tutmak|olağanüstü başarı göstermek|başarı
göğsü kabarmak|övünç duymak|övünç
yerin dibine geçmek|çok utanmak|utanç
kulağına küpe olmak|yaşanan bir olaydan ders çıkarmak|ders
aklı başına gelmek|doğru düşünmeye başlamak|akıl
akıl almamak|inanılmayacak, anlaşılamayacak derecede olmak|şaşkınlık
aklı karışmak|ne yapacağını bilemez hâle gelmek|şaşkınlık
ağzı açık kalmak|çok şaşırmak|şaşkınlık
ayak diremek|bir şeyi yapmamak için direnmek, ısrar etmek|ısrar
dil dökmek|inandırmak için tatlı sözler söylemek|ikna
dilinden düşürmemek|bir şeyi sürekli söylemek|tekrar
eli boş dönmek|istediğini elde edemeden geri dönmek|başarısız
eli ermek|bir şeye gücü yetmek|güç
el kaldırmak|vurmaya yeltenmek|şiddet
göz göre göre|bile bile, açıkça|bilerek
gözü kara|hiçbir şeyden çekinmeyen, atılgan|cesaret
gözünü budaktan sakınmamak|hiçbir tehlikeden çekinmemek|cesaret
ödü kopmak|çok korkmak|korku
tüyleri diken diken olmak|korku ya da heyecandan ürpermek|korku
dizinin dibinden ayırmamak|yanından hiç ayırmamak|yakın
boyun eğmek|karşı koymayıp kabullenmek|boyun
yüz vermek|şımartacak kadar hoşgörülü davranmak|şımartma
cin gibi|çok zeki ve çevik|zeka
kafa yormak|bir konu üzerinde çok düşünmek|düşünme
tas tamam|hiç eksiği olmayan, eksiksiz|tam
sütten çıkmış ak kaşık|hiçbir suçu olmayan, temiz kimse|suçsuz
kabak tadı vermek|sık tekrarlandığı için bıktırıcı olmak|bıkma
burnundan gelmek|bir iyiliğin karşılığında çok sıkıntı çekmek|sıkıntı
burnunun dikine gitmek|kimseyi dinlemeden bildiğini yapmak|inat
kaş yapayım derken göz çıkarmak|düzelteyim derken daha da bozmak|bozma
kül yutmamak|kolay aldanmamak|aldanma
dolma yutmak|kandırılmak, aldatılmak|aldanma
taş çatlasa|ne olursa olsun, en fazla|en
gün yüzü görmemek|hiç rahat yüzü görmemek|sıkıntı
dişini sıkmak|acıya ve sıkıntıya sabırla katlanmak|sabır
eli işe yatmak|bir işi yapmaya yatkın olmak|yetenek
parmakla gösterilmek|üstün niteliğiyle tanınmak|ün
adı çıkmak|kötü bir şeyle tanınır olmak|kötü ün
şapka çıkarmak|üstünlüğünü kabul edip saygı göstermek|saygı
canına okumak|perişan etmek, çok zarar vermek|zarar
ağzı var dili yok|çok sessiz ve uysal|susma
hık demiş burnundan düşmüş|birine çok benzeyen|benzerlik
aynı telden çalmak|aynı düşünceleri paylaşmak|ortak
iki dirhem bir çekirdek|çok süslü giyinmiş|süs
dokuz doğurmak|bir şeyi beklerken çok sıkıntı çekmek|sabırsız
kulağı delik|her şeyden haberi olan|haber
son nefesini vermek|ölmek|ölüm
göz nuru dökmek|el emeği gerektiren bir işi büyük özenle yapmak|emek
alın teri dökmek|emek harcayarak çalışmak|emek
ağzını aramak|birinin düşüncesini dolaylı yoldan öğrenmeye çalışmak|öğrenme
gözden geçirmek|incelemek, denetlemek|bakma
baştan savma|özensiz, gelişigüzel yapılmış|özensiz
yarım ağızla|istemeyerek, gönülsüzce|gönülsüz
hem nalına hem mıhına|iki tarafı da idare ederek|idare
ateşle oynamak|tehlikeli bir işe girişmek|tehlike
ipiyle kuyuya inilmez|güvenilmeyecek kişi|güven
sinek avlamak|işsiz kalmak, müşterisi olmamak|işsiz
dili çözülmek|konuşmaya başlamak|konuşma2
pes etmek|direnmeyi bırakıp vazgeçmek|vazgeçme
gözü doymak|hırsı kalmamak, yetinmek|yetinme
gözü aç|doymak bilmeyen, açgözlü|hırs
boş vermek|bir şeyi önemsemeyip üzerinde durmamak|önemseme
kulak vermek|dikkatle dinlemek|dinleme
eteğine yapışmak|birine yardım için sığınmak|yardım
göz dikmek|başkasının olan bir şeyi elde etmek istemek|istek
el üstünde tutmak|çok değer verip saygı göstermek|saygı
ağır basmak|daha etkili ya da önemli olmak|üstünlük
kendini dev aynasında görmek|kendini olduğundan çok büyük görmek|kibir
çam devirmek|düşüncesizce kırıcı bir söz söylemek ya da davranışta bulunmak|pot
yüreğine su serpilmek|rahatlamak, içi ferahlamak|rahatlama
içine kurt düşmek|kuşkulanmak|kuşku
kuyruğu titretmek|ölmek (alaycı)|ölüm
"""

# atasözü | anlam | etiket
ATASOZLERI = """
damlaya damlaya göl olur|küçük birikimler zamanla büyük bir varlık oluşturur|tasarruf
sakla samanı gelir zamanı|gereksiz görülen şeyler bir gün işe yarar|saklama
ağaç yaşken eğilir|eğitim küçük yaşta başlamalıdır|eğitim
bir elin nesi var iki elin sesi var|işbirliğiyle daha büyük başarı sağlanır|işbirliği
ayağını yorganına göre uzat|harcamalarını gelirine göre ayarla|tasarruf
işleyen demir ışıldar|çalışan kişi her zaman canlı ve başarılı olur|çalışma
sabreden derviş muradına ermiş|sabırlı olan isteğine kavuşur|sabır
üzüm üzüme baka baka kararır|insanlar birlikte oldukları kişilerden etkilenir|etkilenme
dost kara günde belli olur|gerçek dost zor zamanda anlaşılır|dost
mum dibine ışık vermez|kişi uzaktakilere yararlı olurken yakınlarını ihmal edebilir|yakınlar
el elden üstündür|herkesten daha üstün biri mutlaka vardır|üstünlük
söz gümüşse sükût altındır|bazen susmak konuşmaktan daha değerlidir|susma
dereyi görmeden paçaları sıvama|bir iş kesinleşmeden ona göre davranmaya başlama|acele
acele işe şeytan karışır|aceleyle yapılan işte hata olur|acele
bugünün işini yarına bırakma|zamanında yapılması gereken işi erteleme|zaman
balık baştan kokar|bozulma önce yönetimden başlar|yönetim
ne ekersen onu biçersin|her işin sonucu yapılan işe göre olur|sonuç
ak akçe kara gün içindir|biriktirilen para zor günde işe yarar|tasarruf
az olsun öz olsun|niceliğe değil niteliğe önem verilmelidir|nitelik
dağ dağa kavuşmaz insan insana kavuşur|insanlar bir gün yeniden karşılaşabilir|karşılaşma
yalancının mumu yatsıya kadar yanar|yalan kısa sürede ortaya çıkar|yalan
bin bilsen de bir bilene danış|ne kadar bilgili olursan ol başkasına da danış|danışma
ateş düştüğü yeri yakar|acıyı en çok ona uğrayan kişi duyar|acı
komşu komşunun külüne muhtaçtır|komşular küçük şeyler için bile birbirine ihtiyaç duyar|komşu
ev alma komşu al|ev alırken komşuların kim olduğuna dikkat et|komşu
gülme komşuna gelir başına|başkasının başına gelen kötülüğe gülen aynı duruma düşebilir|alay
iyilik yap denize at balık bilmezse Halik bilir|karşılık beklemeden iyilik yap|iyilik
tatlı dil yılanı deliğinden çıkarır|güzel söz en sert insanı bile yumuşatır|tatlı dil
keskin sirke küpüne zarar|öfkeli kişi en çok kendine zarar verir|öfke
öfkeyle kalkan zararla oturur|öfkeyle davranan sonunda zarar görür|öfke
sütten ağzı yanan yoğurdu üfleyerek yer|bir kez zarar gören benzer durumlarda aşırı dikkatli olur|ihtiyat
bir musibet bin nasihatten iyidir|yaşanan bir kötülük birçok öğütten daha öğreticidir|ders
emek olmadan yemek olmaz|çalışmadan kazanç elde edilmez|çalışma
gülü seven dikenine katlanır|bir şeyi seven onun sıkıntılarına da katlanır|katlanma
hatasız kul olmaz|herkes yanılabilir|hata
güneş balçıkla sıvanmaz|gerçek gizlenemez|gerçek
lafla peynir gemisi yürümez|yalnızca konuşmakla iş başarılamaz|söz-iş
kaz gelecek yerden tavuk esirgenmez|büyük kazanç için küçük harcamadan kaçınılmaz|yatırım
eşek hoşaftan ne anlar|değer bilmeyen kişi güzel şeyin kıymetini anlamaz|değer
ağlamayan çocuğa meme vermezler|isteğini dile getirmeyen istediğini elde edemez|isteme
her yiğidin bir yoğurt yiyişi vardır|herkesin işini yapma biçimi farklıdır|farklılık
kervan yolda düzülür|işler zamanla yoluna girer|düzen
sona kalan dona kalır|geç kalan fırsatı kaçırır|fırsat
demir tavında dövülür|her iş uygun zamanında yapılmalıdır|fırsat
körle yatan şaşı kalkar|kötü kişiyle arkadaşlık eden onun kötü huyunu edinir|etkilenme
yuvayı dişi kuş yapar|aileyi düzenleyip yaşatan kadındır|aile
ayinesi iştir kişinin lafına bakılmaz|insanın değeri sözüyle değil yaptığı işle ölçülür|söz-iş
çok yaşayan bilmez çok gezen bilir|gezip görmek insanı bilgili yapar|gezme
işten artmaz dişten artar|birikim kazançtan çok tutumlu yaşamakla yapılır|tasarruf
eski dost düşman olmaz|eski dostluklar kolay kolay bozulmaz|dost
dost acı söyler|gerçek dost hoşa gitmese de doğruyu söyler|dost
doğru söyleyeni dokuz köyden kovarlar|doğruyu söyleyen kişi pek sevilmez|doğruluk
akıl akıldan üstündür|bir kişinin düşüncesinden daha iyisi bulunabilir|üstünlük
iki gönül bir olunca samanlık seyran olur|birbirini seven kişiler için yoksulluk önemli değildir|sevgi
taşıma su ile değirmen dönmez|sürekli dışarıdan yardımla iş yürütülemez|kaynak
rüzgâr eken fırtına biçer|kötülük yapan daha büyük kötülükle karşılaşır|sonuç
ısıracak it dişini göstermez|zarar verecek kişi niyetini belli etmez|tehlike
su uyur düşman uyumaz|düşmana karşı her zaman uyanık olunmalıdır|uyanıklık
kurt dumanlı havayı sever|kötü niyetli kişiler karışıklıktan yararlanır|fırsatçılık
denize düşen yılana sarılır|çaresiz kalan kişi her yolu dener|çare
nerde birlik orada dirlik|birlik olan yerde huzur olur|işbirliği
bir çiçekle yaz gelmez|tek bir belirti genel bir sonuç için yeterli değildir|genelleme
ne verirsen elinle o gider seninle|yaptığın iyilikler sana kalır|iyilik
iki cambaz bir ipte oynamaz|iki güçlü kişi aynı işi birlikte yönetemez|yönetim
fazla mal göz çıkarmaz|bir şeyin fazlası zarar vermez|fazlalık
her gördüğün sakallıyı baban sanma|dış görünüşe aldanma|görünüş
kılıç kınını keser|aşırı sertlik sahibine zarar verir|öfke
el atına binen tez iner|başkasının malına güvenen çabuk zor durumda kalır|bağımsızlık
aç ayı oynamaz|karşılığını almayan kişiden verim beklenmez|ücret
kendi düşen ağlamaz|kendi hatasıyla zarara uğrayan kimseden yakınamaz|sorumluluk
söz ola kese savaşı|güzel söz kavgayı önler|tatlı dil
tilkinin dönüp dolaşıp geleceği yer kürkçü dükkânıdır|kötü işler yapan sonunda yakalanır|ceza
yavuz hırsız ev sahibini bastırır|suçlu kendini haklı gösterip suçsuzu suçlar|haksızlık
at ölür meydan kalır yiğit ölür şan kalır|insan ölse de yaptığı işlerle anılır|ün
bal tutan parmağını yalar|değerli bir işle uğraşan ondan biraz yararlanır|çıkar
çivi çiviyi söker|bir kötülük ancak benzeriyle giderilir|karşılık
dervişin fikri ne ise zikri de odur|insan aklındakini sürekli dile getirir|düşünce
ağır kazan geç kaynar|ağırbaşlı kişiler geç öfkelenir|ağırbaşlılık
ne şiş yansın ne kebap|iki tarafı da zarar görmeyecek biçimde davranmak gerekir|idare
mal canın yongasıdır|insan malına canı kadar önem verir|mal
bir kötünün yedi mahalleye zararı var|kötü bir kişi çevresine geniş zarar verir|kötülük
oturan aslandan yürüyen tilki yeğdir|çalışan güçsüz, çalışmayan güçlüden üstündür|çalışma
"""

# sözcük | eş anlamlısı | etiket (yakın anlamlı çiftler aynı etiketi taşır)
ES_ANLAM = """
akıl|us|akıl
akıllı|zeki|akıl
cevap|yanıt|cevap
okul|mektep|okul
öğrenci|talebe|öğrenci
öğretmen|muallim|öğretmen
hekim|doktor|hekim
yıl|sene|yıl
hayat|yaşam|hayat
kelime|sözcük|kelime
cümle|tümce|cümle
misafir|konuk|misafir
ihtiyar|yaşlı|yaşlı
fakir|yoksul|fakir
cesur|yürekli|cesur
korkak|ödlek|korkak
hediye|armağan|hediye
millet|ulus|millet
vatan|yurt|vatan
şehir|kent|şehir
nehir|ırmak|nehir
neden|sebep|neden
amaç|gaye|amaç
istek|arzu|istek
umut|ümit|umut
sevinç|neşe|sevinç
mutlu|bahtiyar|sevinç
keder|tasa|keder
mutsuz|bedbaht|keder
düşman|hasım|düşman
barış|sulh|barış
savaş|harp|savaş
zafer|utku|zafer
özgürlük|hürriyet|özgürlük
bağımsızlık|istiklal|özgürlük
doğa|tabiat|doğa
gök|sema|gök
kalp|yürek|kalp
yüz|çehre|yüz
ses|seda|ses
sınav|imtihan|sınav
örnek|misal|örnek
soru|sual|soru
sorun|problem|sorun
olay|vaka|olay
hikâye|öykü|hikâye
yazar|müellif|yazar
şair|ozan|şair
anı|hatıra|anı
rüya|düş|rüya
kuvvet|güç|kuvvet
zayıf|cılız|zayıf
çabuk|tez|çabuk
eski|köhne|eski
temiz|pak|temiz
kirli|pis|kirli
büyük|iri|büyük
küçük|ufak|küçük
yüksek|yüce|yüksek
işçi|amele|işçi
cimri|pinti|cimri
kibirli|mağrur|kibir
alçakgönüllü|mütevazı|kibir
aptal|ahmak|akıl
öfke|hiddet|öfke
kıskançlık|haset|kıskançlık
bilgi|malumat|bilgi
bilim|ilim|bilim
bilgin|âlim|bilim
düşünce|fikir|düşünce
duygu|his|duygu
anlam|mana|anlam
ad|isim|ad
uçak|tayyare|uçak
sınır|hudut|sınır
bölge|yöre|bölge
halk|ahali|halk
zaman|vakit|zaman
sabah|seher|sabah
deneyim|tecrübe|deneyim
öğrenim|tahsil|öğrenim
sağlık|sıhhat|sağlık
şans|talih|şans
kader|yazgı|kader
ölüm|vefat|ölüm
kural|kaide|kural
yasa|kanun|yasa
yönetim|idare|yönetim
başkan|reis|başkan
toplum|cemiyet|toplum
özen|itina|özen
zor|çetin|zor
çaba|gayret|çaba
görev|vazife|görev
yer|mekân|yer
vatandaş|yurttaş|vatandaş
sözlük|lügat|sözlük
dil|lisan|dil
tören|merasim|tören
koku|rayiha|koku
tat|lezzet|tat
uyarı|ikaz|uyarı
evren|kâinat|evren
hız|sürat|hız
saygı|hürmet|saygı
sevgi|muhabbet|sevgi
tutsak|esir|tutsak
iktisat|ekonomi|iktisat
tüccar|tacir|tüccar
gelenek|anane|gelenek
öneri|teklif|öneri
birey|fert|birey
bağış|hibe|bağış
fayda|yarar|fayda
zarar|ziyan|zarar
şart|koşul|şart
sonuç|netice|sonuç
başarı|muvaffakiyet|başarı
yanlış|hata|yanlış
"""

# sözcük | zıt anlamlısı | etiket
ZIT_ANLAM = """
büyük|küçük|boyut
uzun|kısa|uzunluk
sıcak|soğuk|sıcaklık
yeni|eski|yenilik
genç|yaşlı|yaş
iyi|kötü|iyilik
güzel|çirkin|güzellik
zengin|fakir|varlık
açık|kapalı|açıklık
kalın|ince|kalınlık
geniş|dar|genişlik
derin|sığ|derinlik
yüksek|alçak|yükseklik
hızlı|yavaş|hız
erken|geç|erken
ön|arka|yön1
alt|üst|yön2
iç|dış|yön3
sağ|sol|yön4
gece|gündüz|gün
sabah|akşam|gün
aşağı|yukarı|yön2
ileri|geri|yön1
var|yok|varlık2
az|çok|miktar
dolu|boş|doluluk
ıslak|kuru|ıslaklık
temiz|kirli|temizlik
kolay|zor|kolaylık
doğru|yanlış|doğruluk
acı|tatlı|tat
sert|yumuşak|sertlik
aydınlık|karanlık|ışık
ak|kara|renk
tembel|çalışkan|çalışma
cömert|cimri|cömertlik
korkak|cesur|cesaret
sevinç|keder|sevinç
savaş|barış|savaş
dost|düşman|dostluk
giriş|çıkış|giriş
alış|satış|ticaret
gelir|gider|gelir
kâr|zarar|kazanç
başlangıç|son|başlangıç
gelmek|gitmek|gelme
almak|vermek|alma
açmak|kapamak|açma
gülmek|ağlamak|gülme
oturmak|kalkmak|oturma
artmak|azalmak|artma
unutmak|hatırlamak|bellek
girmek|çıkmak|giriş
inmek|binmek|binme
doğmak|batmak|doğma
bağlamak|çözmek|bağlama
yakmak|söndürmek|yakma
kabul|ret|kabul
olumlu|olumsuz|olumluluk
somut|soyut|somutluk
nesnel|öznel|nesnellik
genel|özel|genellik
ham|olgun|olgunluk
canlı|cansız|canlılık
sağlıklı|hasta|sağlık
bilgili|cahil|bilgi
pahalı|ucuz|fiyat
uzak|yakın|uzaklık
sessiz|gürültülü|ses
mutlu|mutsuz|sevinç
yorgun|dinç|yorgunluk
eksik|tam|tamlık
tek|çift|sayı
düz|eğri|düzlük
kuzey|güney|yön5
doğu|batı|yön6
yaz|kış|mevsim
ilkbahar|sonbahar|mevsim
yerli|yabancı|yerlilik
kalıcı|geçici|süre
hızlanmak|yavaşlamak|hız
sevinmek|üzülmek|sevinç
övmek|yermek|övme
ödül|ceza|ödül
bağımlı|bağımsız|bağımlılık
zafer|yenilgi|zafer
alıcı|satıcı|ticaret
berrak|bulanık|berraklık
seyrek|sık|sıklık
verimli|verimsiz|verim
dürüst|yalancı|dürüstlük
kazanmak|kaybetmek|kazanma
yükselmek|alçalmak|yükseklik
"""

# yabancı sözcük | Türkçe karşılığı
KARSILIK = """
e-mail|e-posta
feedback|geri bildirim
hardware|donanım
software|yazılım
online|çevrim içi
offline|çevrim dışı
mouse|fare
printer|yazıcı
scanner|tarayıcı
laptop|dizüstü bilgisayar
link|bağlantı
selfie|öz çekim
hashtag|etiket
follower|takipçi
alternatif|seçenek
spontane|kendiliğinden
motivasyon|güdülenme
trend|eğilim
prestij|saygınlık
objektif|nesnel
sübjektif|öznel
konsantrasyon|yoğunlaşma
kriter|ölçüt
empati|eş duyum
global|küresel
lokal|yerel
versiyon|sürüm
dizayn|tasarım
deklarasyon|bildiri
performans|başarım
aktivite|etkinlik
negatif|olumsuz
pozitif|olumlu
maksimum|en yüksek
minimum|en düşük
total|toplam
stres|gerginlik
konsensüs|uzlaşma
fonksiyon|işlev
sirkülasyon|dolaşım
transfer|aktarma
kompleks|karmaşık
proje|tasarı
mesaj|ileti
prezentasyon|sunum
spiker|sunucu
rezervasyon|yer ayırtma
lider|önder
legal|yasal
illegal|yasa dışı
jenerasyon|kuşak
analiz|çözümleme
sentez|bireşim
hipotez|varsayım
teori|kuram
kontrol|denetim
enformasyon|bilgilendirme
organizasyon|düzenleme
diyalog|karşılıklı konuşma
star|yıldız
"""

# açılım | doğru kısaltma | yanlış1..yanlış4
KISALTMA = """
Doktor|Dr.|Dok.|dr|Dktr.|D.r.
Profesör|Prof.|Pr.|prof|Prf.|Pro.
Doçent|Doç.|Dç.|doç|Do.|Doçt.
Avukat|Av.|Avk.|av|A.v.|Avu.
Caddesi|Cad.|Cd|cad|Cadd.|C.d.
Sokağı|Sok.|Sk|sok|Skk.|S.k.
Mahallesi|Mah.|Mh|mah|Mhl.|M.h.
sayfa|s.|S|sf|say.|sh.
ve benzeri|vb.|v.b.|vb|veb.|v.bnz.
ve saire|vs.|v.s.|vs|vsr.|v.sr.
kilometre|km|km.|k.m.|klm|kilom.
santimetre|cm|cm.|s.m.|sntm|santim.
milimetre|mm|mm.|m.m.|mlm|milim.
kilogram|kg|kg.|k.g.|klg|kilog.
Türkiye Büyük Millet Meclisi|TBMM|T.B.M.M.|TBMM.|T.B.M.M|TBMMeclisi
Türk Dil Kurumu|TDK|T.D.K.|TDK.|T.D.K|TDKur.
Türk Standartları Enstitüsü|TSE|T.S.E.|TSE.|T.S.E|TSEns.
Türkiye Cumhuriyeti|T.C.|TC|T.C|TC.|Tc.
dakika|dk.|dak.|dk|dkk.|d.k.
saniye|sn.|san.|sn|snn.|s.n.
yüzyıl|yy.|yy|yüz.|y.y.|yzy.
telefon|tel.|tlf|tel|t.l.|tlfn.
Albay|Alb.|Alby.|alb|Ab.|A.l.b.
Binbaşı|Bnb.|Bnbş.|bnb|Bin.|B.n.b.
Yüzbaşı|Yzb.|Yüzb.|yzb|Yb.|Y.z.b.
Teğmen|Tğm.|Teğ.|tğm|Tm.|T.ğ.m.
Üsteğmen|Ütğm.|Üteğ.|ütğm|Ütm.|Ü.t.ğ.m.
örnek|örn.|ör|örk.|ö.r.n.|örnk
kuruş|kr.|krş|kr|k.r.|kur
Türk lirası|TL|T.L.|TL.|T.L|TLr.
"""

# yanlış yazım | doğru yazım
YAZIM = """
yanlız|yalnız
yalnış|yanlış
herkez|herkes
şöför|şoför
kirpit|kibrit
makina|makine
eşortman|eşofman
orjinal|orijinal
traş|tıraş
süpriz|sürpriz
entellektüel|entelektüel
klavuz|kılavuz
pantalon|pantolon
egzos|egzoz
antrönör|antrenör
antreman|antrenman
sandaviç|sandviç
laboratuar|laboratuvar
kurdela|kurdele
ahçı|aşçı
mütevazi|mütevazı
deterjen|deterjan
zerafet|zarafet
heycan|heyecan
pisikoloji|psikoloji
şemşiye|şemsiye
mutemelen|muhtemelen
mahale|mahalle
tiyatıro|tiyatro
poaça|poğaça
kuvaför|kuaför
ezcane|eczane
hakkaten|hakikaten
birbiri|birbiri
her hangi|herhangi
bir çok|birçok
pekçok|pek çok
herşey|her şey
herzaman|her zaman
şuan|şu an
kayın valide|kayınvalide
kilomentre|kilometre
jöri|jüri
parağraf|paragraf
porgram|program
hoperlör|hoparlör
ambülans|ambulans
zatüre|zatürre
kütübhane|kütüphane
tecrüpe|tecrübe
bir denbire|birdenbire
hanım efendi|hanımefendi
bey efendi|beyefendi
kahve altı|kahvaltı
dedi kodu|dedikodu
kuş başı|kuşbaşı
hoşçakal|hoşça kal
iyiki|iyi ki
herbiri|her biri
bir kaç|birkaç
birdaha|bir daha
bir az|biraz
hiç bir|hiçbir
nekadar|ne kadar
yada|ya da
hergün|her gün
diyorumki|diyorum ki
geldinmi|geldin mi
yalnızmı|yalnız mı
bilmiyormusun|bilmiyor musun
"""

SES_OLAYLARI = ['Ünlü düşmesi', 'Ünsüz yumuşaması', 'Ünsüz benzeşmesi', 'Ünlü daralması',
                'Ünsüz türemesi', 'Ünsüz düşmesi', 'Kaynaştırma']

# sözcük | ses olayı (sözcükte seçeneklerdeki ses olaylarından yalnızca biri bulunur)
SES = """
ağzı|Ünlü düşmesi
burnu|Ünlü düşmesi
oğlu|Ünlü düşmesi
beyni|Ünlü düşmesi
alnı|Ünlü düşmesi
gönlü|Ünlü düşmesi
karnı|Ünlü düşmesi
boynu|Ünlü düşmesi
göğsü|Ünlü düşmesi
şehri|Ünlü düşmesi
nehri|Ünlü düşmesi
zihni|Ünlü düşmesi
fikri|Ünlü düşmesi
sabrı|Ünlü düşmesi
ömrü|Ünlü düşmesi
ismi|Ünlü düşmesi
devrim|Ünlü düşmesi
çevre|Ünlü düşmesi
kavşak|Ünlü düşmesi
ayrılmak|Ünlü düşmesi
kitabı|Ünsüz yumuşaması
ağacı|Ünsüz yumuşaması
kanadı|Ünsüz yumuşaması
dolabı|Ünsüz yumuşaması
çorabı|Ünsüz yumuşaması
sokağa|Ünsüz yumuşaması
ekmeği|Ünsüz yumuşaması
yurdu|Ünsüz yumuşaması
rengi|Ünsüz yumuşaması
kâğıdı|Ünsüz yumuşaması
gidiyor|Ünsüz yumuşaması
ediyor|Ünsüz yumuşaması
tadı|Ünsüz yumuşaması
kebabı|Ünsüz yumuşaması
yoğurdu|Ünsüz yumuşaması
armudu|Ünsüz yumuşaması
bıçağı|Ünsüz yumuşaması
kulağı|Ünsüz yumuşaması
çocuğu|Ünsüz yumuşaması
köpeği|Ünsüz yumuşaması
kitapçı|Ünsüz benzeşmesi
sütçü|Ünsüz benzeşmesi
işçi|Ünsüz benzeşmesi
yurtta|Ünsüz benzeşmesi
sokakta|Ünsüz benzeşmesi
ağaçta|Ünsüz benzeşmesi
gitti|Ünsüz benzeşmesi
baktı|Ünsüz benzeşmesi
kaçtı|Ünsüz benzeşmesi
yaptı|Ünsüz benzeşmesi
düştü|Ünsüz benzeşmesi
aşçı|Ünsüz benzeşmesi
Türkçe|Ünsüz benzeşmesi
kitaptan|Ünsüz benzeşmesi
dişçi|Ünsüz benzeşmesi
simitçi|Ünsüz benzeşmesi
saatte|Ünsüz benzeşmesi
sepette|Ünsüz benzeşmesi
başlıyor|Ünlü daralması
söylüyor|Ünlü daralması
ağlıyor|Ünlü daralması
bekliyor|Ünlü daralması
izliyor|Ünlü daralması
diyor|Ünlü daralması
yiyor|Ünlü daralması
anlıyor|Ünlü daralması
oynuyor|Ünlü daralması
hazırlıyor|Ünlü daralması
temizliyor|Ünlü daralması
dinliyor|Ünlü daralması
hissetmek|Ünsüz türemesi
affetmek|Ünsüz türemesi
reddetmek|Ünsüz türemesi
hallolmak|Ünsüz türemesi
zannetmek|Ünsüz türemesi
hakkı|Ünsüz türemesi
şıkkı|Ünsüz türemesi
sırrı|Ünsüz türemesi
zammı|Ünsüz türemesi
hattı|Ünsüz türemesi
haddi|Ünsüz türemesi
hazzı|Ünsüz türemesi
hissi|Ünsüz türemesi
küçülmek|Ünsüz düşmesi
alçalmak|Ünsüz düşmesi
yükselmek|Ünsüz düşmesi
ufalmak|Ünsüz düşmesi
sıcacık|Ünsüz düşmesi
ufacık|Ünsüz düşmesi
küçücük|Ünsüz düşmesi
alçacık|Ünsüz düşmesi
yumuşacık|Ünsüz düşmesi
kapıyı|Kaynaştırma
masaya|Kaynaştırma
odası|Kaynaştırma
arabası|Kaynaştırma
ikişer|Kaynaştırma
altışar|Kaynaştırma
ninesi|Kaynaştırma
kedisi|Kaynaştırma
pencereye|Kaynaştırma
kahveyi|Kaynaştırma
aileye|Kaynaştırma
kuzunun|Kaynaştırma
elmanın|Kaynaştırma
bahçeyi|Kaynaştırma
"""

FIILIMSI_TUR = {'Z': 'Zarf-fiil (bağ-eylem)', 'S': 'Sıfat-fiil (ortaç)', 'I': 'İsim-fiil (ad-eylem)'}
FIILIMSI_EK = ['Fiilimsi yoktur', 'Birleşik fiil']

# tür | cümle ([...] içindeki öge fiilimsidir; cümlede başka fiilimsi yoktur)
FIILIMSI = """
Z|Okula [giderken] yolda eski bir arkadaşıyla karşılaştı.
Z|Kapıyı [açınca] içeri serin bir rüzgâr doldu.
Z|Kitabı [okudukça] yazarın üslubunu daha çok sevdi.
Z|Çocuk bahçede [koşarak] annesinin yanına geldi.
Z|Sabah erkenden [kalkıp] parka gittik.
Z|Ödevini [bitirmeden] akşam televizyon izlemedi.
Z|Seni [göreli] uzun yıllar geçti.
Z|Yağmur [yağdığında] köyün yolları çamur olurdu.
Z|Öğretmen sınıfa [girer girmez] herkes sustu.
Z|Adam bana [bakmaksızın] odadan çıktı.
Z|Toplantı [bitince] herkes evine döndü.
Z|Dedem gazetesini [okurken] gözlüğünü takar.
Z|Misafirler [gelmeden] evi baştan sona temizledik.
Z|Martılar denizin üzerinde [süzülerek] uçuyordu.
Z|Sınavı [kazanınca] ailesine haber verdi.
Z|Bu yolu [yürüdükçe] eski günleri hatırlıyorum.
Z|Küçük kardeşim [ağlayarak] odasına koştu.
Z|Annem bahçede [yorulunca] biraz dinlendi.
Z|Akşam [olunca] sokak lambaları yandı.
Z|Çocuklar [gülüşerek] parka doğru koştular.
S|[Okuduğum] kitabı arkadaşıma ödünç verdim.
S|Bahçede [açan] çiçekler herkesin ilgisini çekti.
S|Yolda [kaybolan] köpeği sonunda bulduk.
S|[Kırılan] vazoyu kimse fark etmedi.
S|Masada [unuttuğun] defter şimdi bende duruyor.
S|Bu, spor tarihinde [görülmemiş] bir başarıydı.
S|Derste [konuşan] çocuğu öğretmen uyardı.
S|Annemin [pişirdiği] pilav çok lezzetlidir.
S|Sokakta [oynayan] çocukların sesi geliyordu.
S|[Yazacağım] mektubu yarın sabah postalayacağım.
S|Herkes [tükenmez] bir sabırla bekledi.
S|[Uçan] kuşlar ağacın dallarına kondu.
S|Tatilde [okunası] bir roman arıyorum.
S|[Bildiğim] her şeyi sana anlattım.
S|Yarışmayı [kazanan] öğrenci ödülünü aldı.
S|[Ekilen] fidanlar kısa sürede büyüdü.
S|[Yanan] ormanın dumanı kilometrelerce uzaktan görüldü.
S|Dün akşam [dinlediğimiz] şarkı hepimizi duygulandırdı.
S|Babam [eskimiş] ayakkabılarını dün değiştirdi.
I|[Yüzmek] onun için en keyifli spordu.
I|Akşamları kitap [okumayı] çok severim.
I|Onun bu kadar erken [uyanması] hepimizi şaşırttı.
I|Her gün [yürümek] sağlık için faydalıdır.
I|Bu kış kayak [yapmayı] öğreneceğim.
I|Erken [kalkmak] ona zor geliyordu.
I|Kuşlar sabahın ilk ışıklarıyla [ötmeye] başladı.
I|Resim [yapmak] onun en büyük tutkusudur.
I|Sınavlarda kopya [çekmek] kesinlikle yasaktır.
I|Senin bize [gelmen] hepimizi çok sevindirdi.
I|Doktor ona tuzu [azaltmasını] önerdi.
I|Yeni bir dil [öğrenmek] sabır ister.
I|Askerlerin törende düzenli [yürümesi] herkesi etkiledi.
I|Annem sebze [doğramayı] bana bıraktı.
I|Onun bu kadar geç [kalması] beni endişelendirdi.
I|Fidan ve ağaç [dikmek] hepimizin görevidir.
I|Denizde [yüzmeyi] bu yaz öğrendim.
I|Kardeşim bisiklet [sürmeyi] çok sever.
I|Kitapları rafa [dizmek] yarım saat sürdü.
I|Bu sorunu [çözmek] kolay değildi.
"""

# Sözel mantık: ad | -nın eki | -dan eki
ADLAR = """
Ali|Ali'nin|Ali'den
Berk|Berk'in|Berk'ten
Can|Can'ın|Can'dan
Deniz|Deniz'in|Deniz'den
Ece|Ece'nin|Ece'den
Selin|Selin'in|Selin'den
Murat|Murat'ın|Murat'tan
Oya|Oya'nın|Oya'dan
Kerem|Kerem'in|Kerem'den
Tuna|Tuna'nın|Tuna'dan
Hakan|Hakan'ın|Hakan'dan
Zeynep|Zeynep'in|Zeynep'ten
Ufuk|Ufuk'un|Ufuk'tan
Gül|Gül'ün|Gül'den
İpek|İpek'in|İpek'ten
Emre|Emre'nin|Emre'den
Nazlı|Nazlı'nın|Nazlı'dan
Pelin|Pelin'in|Pelin'den
"""


def _bas(x):
    """Türkçe kurala uygun ilk harf büyütme (i → İ)."""
    return {'i': 'İ', 'ı': 'I'}.get(x[0], x[0].upper()) + x[1:]


def _satir(blok, n):
    out = []
    for line in blok.strip().splitlines():
        p = [x.strip() for x in line.split('|')]
        if len(p) != n:
            raise ValueError(f'{n} alan beklenirken: {line}')
        out.append(p)
    return out


def _etiketli(rng, tur, konu, rows, kok_i, kok_g, ger, z=2):
    """(anahtar, değer, etiket): çeldiriciler farklı etiketli kayıtlardan."""
    out = []
    for a, d, e in rows:
        diger = [r for r in rows if r[2] != e]
        rng.shuffle(diger)
        out.append(q(tur + '_anlam', konu, kok_i(a), d, sec(d, [r[1] for r in diger], rng), ger(a, d), z))
        rng.shuffle(diger)
        out.append(q(tur + '_bul', konu, kok_g(d), a, sec(a, [r[0] for r in diger], rng), ger(a, d), z))
    return out


def _cift(rng, tur, rows, kok, ger, z=2):
    """Eş/zıt anlam çiftleri: her iki yönde soru; çeldiriciler başka etiketlerden."""
    out = []
    kelimeler = [(w, r[2]) for r in rows for w in r[:2]]
    for a, b, e in rows:
        for x, y in ((a, b), (b, a)):
            havuz = [w for w, et in kelimeler if et != e and w[:3] not in (x[:3], y[:3])]
            rng.shuffle(havuz)
            out.append(q(tur, 'Sözcükte Anlam', kok(x), y, sec(y, havuz, rng), ger(x, y), z))
    return out


HARFLER = 'abcçdefgğhıijklmnoprsştuüvyz'
UNLU_ES = {'a': 'e', 'e': 'a', 'ı': 'i', 'i': 'ı', 'o': 'ö', 'ö': 'o', 'u': 'ü', 'ü': 'u',
           'k': 'g', 'g': 'k', 's': 'z', 'z': 's', 'c': 'ç', 'ç': 'c', 't': 'd', 'd': 't', 'p': 'b', 'b': 'p', 'ğ': 'g'}


def _bozuk(dogru, rng, n, yasak):
    """Doğru yazımdan farklı, birbirinden ayrı n hatalı biçim üret."""
    gor = {dogru.casefold(), *(y.casefold() for y in yasak)}
    out = []
    deneme = 0
    while len(out) < n and deneme < 500:
        deneme += 1
        s = list(dogru)
        i = rng.randrange(len(s))
        islem = rng.choice('ude')
        if s[i] == ' ':
            if islem == 'd':
                del s[i]
            else:
                continue
        elif islem == 'u' and s[i] in UNLU_ES:
            s[i] = UNLU_ES[s[i]]
        elif islem == 'd' and len(s) > 3 and s[i].isalpha():
            s.insert(i, s[i])
        elif islem == 'e' and len(s) > 4 and 0 < i < len(s) - 1 and s[i].isalpha():
            del s[i]
        else:
            continue
        w = ''.join(s)
        if w.casefold() not in gor:
            gor.add(w.casefold())
            out.append(w)
    return out if len(out) == n else None


# ---------------------------------------------------------------- sözel mantık
def _kisitlar(baglam, ad, gen, abl):
    """Bağlama göre (metin, sınama) kısıt üreticileri."""
    if baglam == 'sira':
        return {
            'hemen_once': lambda x, y: (f'{ad[x]}, {gen[y]} hemen solunda oturmaktadır.', lambda p: p[x] == p[y] - 1),
            'once': lambda x, y: (f'{ad[x]}, {abl[y]} daha solda oturmaktadır.', lambda p: p[x] < p[y]),
            'yan_degil': lambda x, y: (f'{ad[x]} ile {ad[y]} yan yana oturmamaktadır.', lambda p: abs(p[x] - p[y]) != 1),
            'yan': lambda x, y: (f'{ad[x]} ile {ad[y]} yan yana oturmaktadır.', lambda p: abs(p[x] - p[y]) == 1),
            'yer': lambda x, k: (f'{ad[x]}, soldan {k}. sandalyede oturmaktadır.', lambda p: p[x] == k),
            'yer_degil': lambda x, k: (f'{ad[x]}, soldan {k}. sandalyede oturmamaktadır.', lambda p: p[x] != k),
            'kenar': lambda x, _: (f'{ad[x]}, uçtaki sandalyelerden birinde oturmaktadır.', lambda p: p[x] in (1, 5)),
        }
    return {
        'hemen_once': lambda x, y: (f'{ad[x]}, {gen[y]} hemen bir alt katında oturmaktadır.', lambda p: p[x] == p[y] - 1),
        'once': lambda x, y: (f'{ad[x]}, {abl[y]} daha alt bir katta oturmaktadır.', lambda p: p[x] < p[y]),
        'yan_degil': lambda x, y: (f'{ad[x]} ile {gen[y]} katları ardışık değildir.', lambda p: abs(p[x] - p[y]) != 1),
        'yan': lambda x, y: (f'{ad[x]} ile {gen[y]} katları ardışıktır.', lambda p: abs(p[x] - p[y]) == 1),
        'yer': lambda x, k: (f'{ad[x]}, {k}. katta oturmaktadır.', lambda p: p[x] == k),
        'yer_degil': lambda x, k: (f'{ad[x]}, {k}. katta oturmamaktadır.', lambda p: p[x] != k),
        'kenar': lambda x, _: (f'{ad[x]}, en alt ya da en üst katta oturmaktadır.', lambda p: p[x] in (1, 5)),
    }


def _bulmaca(rng, adlar):
    kisiler = rng.sample(adlar, 5)
    ad = [k[0] for k in kisiler]
    gen = [k[1] for k in kisiler]
    abl = [k[2] for k in kisiler]
    baglam = rng.choice(['sira', 'kat'])
    K = _kisitlar(baglam, ad, gen, abl)
    gizli = list(range(1, 6))
    rng.shuffle(gizli)  # gizli[i] = i. kişinin yeri
    tum = [dict(zip(range(5), p)) for p in permutations(range(1, 6))]
    gizli_p = dict(zip(range(5), gizli))
    secilen, kalan, dogrudan = [], tum, set()
    for _ in range(40):
        tip = rng.choice(['hemen_once', 'once', 'once', 'yan_degil', 'yan', 'yer_degil', 'yer_degil', 'kenar', 'yer'])
        x, y = rng.sample(range(5), 2)
        if tip == 'yer' and dogrudan:
            continue
        if tip in ('yer', 'yer_degil'):
            k = gizli_p[x] if tip == 'yer' else rng.choice([v for v in range(1, 6) if v != gizli_p[x]])
            metin, f = K[tip](x, k)
        else:
            metin, f = K[tip](x, y)
        if not f(gizli_p) or metin in [m for m, _ in secilen]:
            continue
        yeni = [p for p in kalan if f(p)]
        if len(yeni) == len(kalan):
            continue
        secilen.append((metin, f))
        if tip == 'yer':
            dogrudan.add(x)
        kalan = yeni
        if len(kalan) == 1:
            break
    if len(kalan) != 1:
        return []
    # Gereksiz (diğerlerinden çıkarılabilen) kısıtları at.
    for c in list(secilen):
        dene = [x for x in secilen if x is not c]
        if sum(1 for p in tum if all(f(p) for _, f in dene)) == 1:
            secilen = dene
    if len(secilen) > 6:
        return []
    dogrudan = {i for i in dogrudan if any(m.startswith(ad[i] + ',') and 'oturmamaktadır' not in m
                                           and ('sandalyede' in m or '. katta' in m) for m, _ in secilen)}
    cozum = kalan[0]
    if baglam == 'sira':
        giris = f'{", ".join(ad[:4])} ve {ad[4]}; yan yana dizilmiş beş sandalyeye birer kişi olacak biçimde oturmuştur.'
        yer_ad = lambda k: f'Soldan {k}.'
        soru_yer = lambda i: f'Buna göre {ad[i]} soldan kaçıncı sandalyede oturmaktadır?'
        soru_kim = lambda k: f'Buna göre soldan {k}. sandalyede kim oturmaktadır?'
    else:
        giris = (f'{", ".join(ad[:4])} ve {ad[4]}; beş katlı bir apartmanın her katında bir kişi olacak biçimde oturmaktadır '
                 f'(1. kat en alt kattır).')
        yer_ad = lambda k: f'{k}. kat'
        soru_yer = lambda i: f'Buna göre {ad[i]} kaçıncı katta oturmaktadır?'
        soru_kim = lambda k: f'Buna göre {k}. katta kim oturmaktadır?'
    metin = giris + ' Bilinenler: ' + ' '.join(f'({j + 1}) {m}' for j, (m, _) in enumerate(secilen))
    aday = [i for i in range(5) if i not in dogrudan]
    if not aday:
        return []
    i = rng.choice(aday)
    k = cozum[i]
    gerekce = 'Tüm olası yerleşimler denendiğinde koşulları sağlayan tek düzen: ' + ', '.join(
        f'{yer_ad(cozum[j])} {ad[j]}' for j in sorted(range(5), key=lambda j: cozum[j])) + '.'
    out = [q('mantik_yer', 'Sözel Mantık', metin + ' ' + soru_yer(i), yer_ad(k),
             [yer_ad(v) for v in range(1, 6) if v != k], gerekce, 3)]
    k2 = rng.choice([cozum[j] for j in aday])
    kim = [j for j in range(5) if cozum[j] == k2][0]
    out.append(q('mantik_kim', 'Sözel Mantık', metin + ' ' + soru_kim(k2), ad[kim],
                 [ad[j] for j in range(5) if j != kim], gerekce, 3))
    return out


def uret(rng):
    out = []
    dey = _satir(DEYIMLER, 3)
    out += _etiketli(rng, 'deyim', 'Sözcükte Anlam', dey,
                     lambda a: f'“{a}” deyiminin anlamı aşağıdakilerden hangisidir?',
                     lambda d: f'“{d}” anlamına gelen deyim aşağıdakilerden hangisidir?',
                     lambda a, d: f'“{a}” deyimi “{d}” anlamındadır.')
    ata = _satir(ATASOZLERI, 3)
    out += _etiketli(rng, 'atasozu', 'Sözcükte Anlam', ata,
                     lambda a: f'“{_bas(a)}.” atasözünün anlamı aşağıdakilerden hangisidir?',
                     lambda d: f'“{_bas(d)}.” düşüncesini anlatan atasözü aşağıdakilerden hangisidir?',
                     lambda a, d: f'“{_bas(a)}.” atasözü, {d} düşüncesini anlatır.', 3)
    out += _cift(rng, 'es_anlam', _satir(ES_ANLAM, 3),
                 lambda x: f'“{x}” sözcüğünün eş anlamlısı aşağıdakilerden hangisidir?',
                 lambda x, y: f'“{x}” ile “{y}” eş anlamlıdır.')
    out += _cift(rng, 'zit_anlam', _satir(ZIT_ANLAM, 3),
                 lambda x: f'“{x}” sözcüğünün zıt (karşıt) anlamlısı aşağıdakilerden hangisidir?',
                 lambda x, y: f'“{x}” ile “{y}” zıt anlamlıdır.')
    kar = _satir(KARSILIK, 2)
    for a, d in kar:
        diger = [r for r in kar if r[0] != a]
        rng.shuffle(diger)
        out.append(q('karsilik', 'Sözcükte Anlam', f'Yabancı kökenli “{a}” sözcüğü yerine kullanılabilecek Türkçe karşılık aşağıdakilerden hangisidir?',
                     d, sec(d, [r[1] for r in diger], rng), f'“{a}” yerine “{d}” kullanılabilir.'))
        rng.shuffle(diger)
        out.append(q('karsilik_ters', 'Sözcükte Anlam', f'“{d}” sözcüğü aşağıdaki yabancı sözcüklerden hangisinin Türkçe karşılığıdır?',
                     a, sec(a, [r[0] for r in diger], rng), f'“{d}”, “{a}” sözcüğünün Türkçe karşılığıdır.'))
    kis = _satir(KISALTMA, 6)
    for acilim, dogru, *yanlis in kis:
        out.append(q('kisaltma', 'Yazım', f'“{acilim}” sözünün Yazım Kılavuzu’na uygun kısaltması aşağıdakilerden hangisidir?',
                     dogru, yanlis, f'{acilim}: {dogru}', 2))
        diger = [r[0] for r in kis if r[0] != acilim]
        rng.shuffle(diger)
        out.append(q('kisaltma_ters', 'Yazım', f'“{dogru}” kısaltması aşağıdakilerden hangisinin kısaltmasıdır?',
                     acilim, sec(acilim, diger, rng), f'{dogru} = {acilim}.', 2))
    for yanlis, dogru in _satir(YAZIM, 2):
        if yanlis == dogru:
            continue
        b = _bozuk(dogru, rng, 4, [yanlis])
        out.append(q('yazim', 'Yazım', f'“{yanlis}” biçiminde yanlış yazılan sözcüğün doğru yazılışı aşağıdakilerden hangisidir?',
                     dogru, b, f'Doğru yazım: {dogru}.', 2))
    for soz, olay in _satir(SES, 2):
        out.append(q('ses', 'Ses Bilgisi', f'“{soz}” sözcüğünde aşağıdaki ses olaylarından hangisi görülür?', olay,
                     sec(olay, SES_OLAYLARI, rng), f'“{soz}” sözcüğünde {olay.lower()} vardır.', 2))
    for tur, cumle in _satir(FIILIMSI, 2):
        f = cumle[cumle.index('[') + 1:cumle.index(']')]
        duz = cumle.replace('[', '').replace(']', '')
        tur_ad = FIILIMSI_TUR[tur]
        out.append(q('fiilimsi_tur', 'Fiilimsi', f'“{duz}” cümlesindeki fiilimsinin türü aşağıdakilerden hangisidir?', tur_ad,
                     [v for k, v in FIILIMSI_TUR.items() if k != tur] + FIILIMSI_EK, f'“{f}” {tur_ad.lower()}dir.', 3))
        kalan = cumle[:cumle.index('[')] + cumle[cumle.index(']') + 1:]
        kelimeler = [w.strip('.,;:!?') for w in kalan.split()]
        kelimeler = [w for w in kelimeler if w]
        out.append(q('fiilimsi_bul', 'Fiilimsi', f'“{duz}” cümlesinde aşağıdakilerden hangisi fiilimsidir?', f,
                     sec(f, kelimeler, rng), f'“{f}” {tur_ad.lower()}dir; diğerleri fiilimsi değildir.', 2))
    adlar = _satir(ADLAR, 3)
    say = 0
    while say < 600:
        r = _bulmaca(rng, adlar)
        if r:
            out += r
            say += 1
    return out
