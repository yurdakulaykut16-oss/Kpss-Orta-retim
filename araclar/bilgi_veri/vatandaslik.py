"""Vatandaşlık bilgi tabloları (1982 Anayasası güncel madde düzeni, 2017 değişiklikleri dahil)."""
from .ortak import eslesme, eslestirme, farkli, onculu, q, sec, sec2, siralama, yakin_sec

# madde no | konu | işaret (! = hak değil / ödev ya da düzenleme; statü sorusunda kullanılmaz)
MADDELER = """
1|Devletin şekli|!
2|Cumhuriyetin nitelikleri|!
3|Devletin bütünlüğü, resmî dili, bayrağı, millî marşı ve başkenti|!
4|Değiştirilemeyecek hükümler|!
5|Devletin temel amaç ve görevleri|!
6|Egemenlik|!
7|Yasama yetkisi|!
8|Yürütme yetkisi ve görevi|!
9|Yargı yetkisi|!
10|Kanun önünde eşitlik|!
11|Anayasanın bağlayıcılığı ve üstünlüğü|!
12|Temel hak ve hürriyetlerin niteliği|!
13|Temel hak ve hürriyetlerin sınırlanması|!
14|Temel hak ve hürriyetlerin kötüye kullanılamaması|!
15|Temel hak ve hürriyetlerin kullanılmasının durdurulması|!
16|Yabancıların durumu|!
17|Kişinin dokunulmazlığı, maddi ve manevi varlığı|
18|Zorla çalıştırma yasağı|
19|Kişi hürriyeti ve güvenliği|
20|Özel hayatın gizliliği|
21|Konut dokunulmazlığı|
22|Haberleşme hürriyeti|
23|Yerleşme ve seyahat hürriyeti|
24|Din ve vicdan hürriyeti|
25|Düşünce ve kanaat hürriyeti|
26|Düşünceyi açıklama ve yayma hürriyeti|
27|Bilim ve sanat hürriyeti|
28|Basın hürriyeti|
29|Süreli ve süresiz yayın hakkı|
30|Basın araçlarının korunması|!
31|Kamu tüzel kişilerinin elindeki kitle haberleşme araçlarından yararlanma hakkı|!
32|Düzeltme ve cevap hakkı|
33|Dernek kurma hürriyeti|
34|Toplantı ve gösteri yürüyüşü düzenleme hakkı|
35|Mülkiyet hakkı|
36|Hak arama hürriyeti|
37|Kanuni hâkim güvencesi|!
38|Suç ve cezalara ilişkin esaslar|!
39|İspat hakkı|
40|Temel hak ve hürriyetlerin korunması|!
41|Ailenin korunması ve çocuk hakları|
42|Eğitim ve öğrenim hakkı ve ödevi|!
43|Kıyılardan yararlanma|!
44|Toprak mülkiyeti|!
45|Tarım, hayvancılık ve bu üretim dallarında çalışanların korunması|!
46|Kamulaştırma|!
47|Devletleştirme ve özelleştirme|!
48|Çalışma ve sözleşme hürriyeti|!
49|Çalışma hakkı ve ödevi|!
50|Çalışma şartları ve dinlenme hakkı|
51|Sendika kurma hakkı|!
53|Toplu iş sözleşmesi ve toplu sözleşme hakkı|!
54|Grev hakkı ve lokavt|!
55|Ücrette adalet sağlanması|!
56|Sağlık hizmetleri ve çevrenin korunması|
57|Konut hakkı|
58|Gençliğin korunması|!
59|Sporun geliştirilmesi|!
60|Sosyal güvenlik hakkı|
61|Sosyal güvenlik bakımından özel olarak korunması gerekenler|!
62|Yabancı ülkelerde çalışan Türk vatandaşları|!
63|Tarih, kültür ve tabiat varlıklarının korunması|!
64|Sanatın ve sanatçının korunması|!
65|Sosyal ve ekonomik hakların sınırları|!
66|Türk vatandaşlığı|!
67|Seçme, seçilme ve siyasi faaliyette bulunma hakları|
68|Parti kurma, partilere girme ve partilerden ayrılma|
69|Siyasi partilerin uyacakları esaslar|!
70|Kamu hizmetlerine girme hakkı|
71|Mal bildirimi|!
72|Vatan hizmeti|!
73|Vergi ödevi|!
74|Dilekçe, bilgi edinme ve kamu denetçisine başvurma hakkı|
75|Türkiye Büyük Millet Meclisinin kuruluşu|!
76|Milletvekili seçilme yeterliliği|!
77|TBMM ve Cumhurbaşkanlığı seçimlerinin dönemi|!
78|Seçimlerin ertelenmesi ve ara seçimler|!
83|Yasama dokunulmazlığı|!
84|Milletvekilliğinin düşmesi|!
87|TBMM'nin görev ve yetkileri|!
88|Kanunların teklif edilmesi ve görüşülmesi|!
89|Kanunların Cumhurbaşkanınca yayımlanması|!
90|Milletlerarası antlaşmaları uygun bulma|!
92|Savaş hâli ilanına ve silahlı kuvvet kullanılmasına izin verilmesi|!
93|TBMM'nin toplanması ve tatili|!
94|TBMM Başkanlık Divanı|!
98|TBMM'nin bilgi edinme ve denetim yolları|!
101|Cumhurbaşkanlığına aday olma ve seçilme|!
102|Cumhurbaşkanının seçimi|!
103|Cumhurbaşkanının andiçmesi|!
104|Cumhurbaşkanının görev ve yetkileri|!
105|Cumhurbaşkanının cezai sorumluluğu|!
106|Cumhurbaşkanı yardımcıları ve bakanlar|!
116|Seçimlerin yenilenmesi|!
117|Millî savunma|!
118|Millî Güvenlik Kurulu|!
119|Olağanüstü hâl yönetimi|!
123|İdarenin esasları|!
124|Yönetmelikler|!
125|İdari işlemlere karşı yargı yolu|!
126|Merkezî idare|!
127|Mahallî idareler|!
128|Kamu görevlileriyle ilgili genel ilkeler|!
129|Kamu görevlilerinin ödev ve sorumlulukları, disiplin kovuşturmasında güvence|!
130|Yükseköğretim kurumları|!
131|Yükseköğretim kurumlarının üst kuruluşları|!
133|Radyo ve televizyon üst kurulu ve kamu radyo-televizyon kurumu|!
134|Atatürk Kültür, Dil ve Tarih Yüksek Kurumu|!
135|Kamu kurumu niteliğindeki meslek kuruluşları|!
136|Diyanet İşleri Başkanlığı|!
138|Mahkemelerin bağımsızlığı|!
139|Hâkimlik ve savcılık teminatı|!
140|Hâkimlik ve savcılık mesleği|!
141|Duruşmaların açık ve kararların gerekçeli olması|!
142|Mahkemelerin kuruluşu|!
146|Anayasa Mahkemesinin kuruluşu|!
148|Anayasa Mahkemesinin görev ve yetkileri|!
153|Anayasa Mahkemesinin kararları|!
154|Yargıtay|!
155|Danıştay|!
158|Uyuşmazlık Mahkemesi|!
159|Hâkimler ve Savcılar Kurulu|!
160|Sayıştay|!
161|Bütçe ve kesin hesap|!
166|Planlama|!
167|Piyasaların denetimi ve dış ticaretin düzenlenmesi|!
168|Tabii servetlerin ve kaynakların aranması ve işletilmesi|!
169|Ormanların korunması ve geliştirilmesi|!
170|Orman köylüsünün korunması|!
171|Kooperatifçiliğin geliştirilmesi|!
172|Tüketicilerin korunması|!
173|Esnaf ve sanatkârların korunması|!
174|İnkılap kanunlarının korunması|!
175|Anayasanın değiştirilmesi|!
176|Başlangıç ve kenar başlıkları|!
177|Yürürlüğe giriş|!
"""


def kisim(n):
    if n <= 11: return 'Genel Esaslar'
    if n <= 74: return 'Temel Haklar ve Ödevler'
    if n <= 160: return 'Cumhuriyetin Temel Organları'
    if n <= 173: return 'Mali ve Ekonomik Hükümler'
    if n == 174: return 'Çeşitli Hükümler'
    return 'Son Hükümler'


KISIMLAR = ['Genel Esaslar', 'Temel Haklar ve Ödevler', 'Cumhuriyetin Temel Organları', 'Mali ve Ekonomik Hükümler', 'Son Hükümler', 'Çeşitli Hükümler']


def hak_bolum(n):
    if 12 <= n <= 16: return 'Genel Hükümler'
    if 17 <= n <= 40: return 'Kişinin Hakları ve Ödevleri'
    if 41 <= n <= 65: return 'Sosyal ve Ekonomik Haklar ve Ödevler'
    if 66 <= n <= 74: return 'Siyasi Haklar ve Ödevler'


def organ(n):
    if 75 <= n <= 100: return 'Yasama'
    if 101 <= n <= 137: return 'Yürütme'
    if 138 <= n <= 160: return 'Yargı'


STATU = {'Kişinin Hakları ve Ödevleri': 'Negatif statü (koruyucu) hakları',
         'Sosyal ve Ekonomik Haklar ve Ödevler': 'Pozitif statü (isteme) hakları',
         'Siyasi Haklar ve Ödevler': 'Aktif statü (katılma) hakları'}

# kavram | tanım | konu | hukuk dalı (- = belirsiz, dal sorusu üretilmez)
KAVRAMLAR = """
Hukuk|Toplum hayatını düzenleyen ve uyulması devlet yaptırımıyla sağlanan kurallar bütünü|Hukuk|-
Yaptırım|Hukuk kurallarına uyulmaması hâlinde uygulanan müeyyide|Hukuk|-
Tazminat|Hukuka aykırı bir eylemle verilen zararın para ile giderilmesi|Hukuk|-
Cebri icra|Borcun devlet gücüyle zorla yerine getirilmesi|Hukuk|-
Örf ve âdet hukuku|Toplumda uzun süre tekrarlanarak uyulması zorunlu hâle gelen yazısız kurallar|Hukuk|-
Kanun|TBMM tarafından yapılan genel, sürekli ve soyut hukuk kuralı|Hukuk|-
Yönetmelik|İdarenin kanunların ve Cumhurbaşkanlığı kararnamelerinin uygulanmasını sağlamak için çıkardığı düzenleyici işlem|Hukuk|İdare hukuku
Cumhurbaşkanlığı kararnamesi|Cumhurbaşkanının yürütme yetkisine ilişkin konularda çıkardığı düzenleyici işlem|Yürütme|-
Tüzel kişi|Belirli bir amaç için bir araya gelen kişi ya da mal topluluklarının hukuken kişilik kazanmış hâli|Hukuk|Medeni hukuk
Hak ehliyeti|Haklara ve borçlara sahip olabilme yeteneği|Hukuk|Medeni hukuk
Fiil ehliyeti|Kendi fiilleriyle hak edinip borç altına girebilme yeteneği|Hukuk|Medeni hukuk
Ayırt etme gücü|Kişinin davranışlarının sebep ve sonuçlarını kavrayabilme yeteneği|Hukuk|Medeni hukuk
Kısıtlı|Akıl hastalığı, savurganlık gibi sebeplerle mahkeme kararıyla fiil ehliyeti sınırlanan ergin|Hukuk|Medeni hukuk
Vasi|Velayet altında olmayan küçüğün ya da kısıtlının kişisel ve malvarlığı işlerini yürütmek için atanan kişi|Hukuk|Medeni hukuk
Kayyım|Belirli bir işin görülmesi veya bir malvarlığının yönetimi için atanan temsilci|Hukuk|Medeni hukuk
Yasal danışman|Kısıtlanmayı gerektirecek ölçüde olmayan durumlarda kişiye atanan ve belirli işlemlerde onayı aranan kişi|Hukuk|Medeni hukuk
Velayet|Ergin olmayan çocuk üzerinde anne ve babanın sahip olduğu hak ve yükümlülükler|Hukuk|Medeni hukuk
Yerleşim yeri|Kişinin sürekli kalma niyetiyle oturduğu yer|Hukuk|Medeni hukuk
Kayın hısımlığı|Evlilik nedeniyle eşlerden biri ile diğerinin kan hısımları arasında oluşan bağ|Hukuk|Medeni hukuk
Kan hısımlığı|Birbirinden gelen ya da ortak bir kökten gelen kişiler arasındaki bağ|Hukuk|Medeni hukuk
Gaiplik|Ölüm tehlikesi içinde kaybolan ya da uzun süredir haber alınamayan kişi hakkında mahkemece verilen karar|Hukuk|Medeni hukuk
Ölüm karinesi|Ölümüne kesin gözle bakılmasını gerektiren bir durumda cesedi bulunamayan kişinin ölmüş sayılması|Hukuk|Medeni hukuk
Nişanlanma|Evlenme vaadiyle kurulan hukuki ilişki|Hukuk|Medeni hukuk
Soybağı|Çocuk ile ana ve babası arasındaki hukuki bağ|Hukuk|Medeni hukuk
Evlat edinme|Mahkeme kararıyla kurulan yapay soybağı|Hukuk|Medeni hukuk
Edinilmiş mallara katılma|Türk Medeni Kanunu'na göre eşler arasında geçerli olan yasal mal rejimi|Hukuk|Medeni hukuk
Saklı pay|Mirasbırakanın tasarruf edemeyeceği, belirli yasal mirasçılara ayrılmış miras payı|Hukuk|Medeni hukuk
Vasiyetname|Kişinin ölümünden sonra malvarlığının nasıl paylaşılacağına ilişkin tek taraflı ölüme bağlı tasarrufu|Hukuk|Medeni hukuk
Mirasın reddi|Mirasçının mirası kabul etmediğini açıklaması|Hukuk|Medeni hukuk
Zilyetlik|Bir şey üzerindeki fiilî hâkimiyet|Hukuk|Medeni hukuk
Mülkiyet hakkı|Sahibine bir şeyi kullanma, ondan yararlanma ve onun üzerinde tasarrufta bulunma yetkisi veren ayni hak|Hukuk|Medeni hukuk
İrtifak hakkı|Başkasının taşınmazından belirli biçimde yararlanma imkânı veren sınırlı ayni hak|Hukuk|Medeni hukuk
İpotek|Taşınmaz üzerinde alacağa güvence olarak kurulan rehin hakkı|Hukuk|Medeni hukuk
Tapu sicili|Taşınmazlar üzerindeki hakların gösterildiği resmî sicil|Hukuk|Medeni hukuk
Sözleşme|Tarafların karşılıklı ve birbirine uygun irade beyanlarıyla kurulan hukuki işlem|Hukuk|Borçlar hukuku
Haksız fiil|Hukuka aykırı ve kusurlu bir davranışla başkasına zarar verilmesi|Hukuk|Borçlar hukuku
Sebepsiz zenginleşme|Haklı bir sebep olmaksızın başkasının malvarlığından zenginleşme|Hukuk|Borçlar hukuku
Kefalet|Kefilin, borçlunun borcunu ödememesinin sonuçlarından sorumlu olmayı üstlendiği sözleşme|Hukuk|Borçlar hukuku
Zamanaşımı|Belirli bir sürenin geçmesiyle bir hakkın dava yoluyla istenebilirliğini yitirmesi|Hukuk|-
Hak düşürücü süre|Süresi içinde kullanılmayan hakkın tamamen ortadan kalktığı süre|Hukuk|-
Tacir|Bir ticari işletmeyi kısmen de olsa kendi adına işleten kişi|Hukuk|Ticaret hukuku
Ticaret unvanı|Tacirin ticari işletmesine ilişkin işlemleri yaparken kullandığı ve imza olarak attığı ad|Hukuk|Ticaret hukuku
Kıymetli evrak|Hakkın senetten ayrı olarak ileri sürülemediği çek, bono ve poliçe gibi senetler|Hukuk|Ticaret hukuku
Suç|Kanunda tanımlanan ve karşılığında ceza öngörülen hukuka aykırı fiil|Hukuk|Ceza hukuku
Kast|Suçun kanuni tanımındaki unsurların bilerek ve istenerek gerçekleştirilmesi|Hukuk|Ceza hukuku
Taksir|Dikkat ve özen yükümlülüğüne aykırılık nedeniyle bir davranışın sonucunun öngörülmeyerek suçun işlenmesi|Hukuk|Ceza hukuku
Meşru müdafaa|Kendisine ya da başkasına yönelmiş haksız bir saldırıyı o anda orantılı biçimde savuşturma|Hukuk|Ceza hukuku
Suçta ve cezada kanunilik ilkesi|Kanunun açıkça suç saymadığı bir fiil için kimseye ceza verilemeyeceği ilkesi|Hukuk|-
Ceza sorumluluğunun şahsiliği|Kimsenin başkasının fiilinden dolayı cezalandırılamayacağı ilkesi|Hukuk|-
Masumiyet karinesi|Suçluluğu hükmen sabit oluncaya kadar kimsenin suçlu sayılamayacağı ilkesi|Hukuk|-
Genel af|Suçu ve cezayı bütün sonuçlarıyla ortadan kaldıran ve TBMM'nin kanunla yaptığı düzenleme|Hukuk|-
Özel af|Hükümlülüğü kaldırmadan cezanın kısmen ya da tamamen kaldırılması veya hafifletilmesi|Hukuk|-
Kamu davası|Suç şüphesi üzerine Cumhuriyet savcısı tarafından açılan ceza davası|Yargı|Ceza muhakemesi hukuku
İddianame|Cumhuriyet savcısının kamu davasını açmak için düzenlediği belge|Yargı|Ceza muhakemesi hukuku
Uzlaşma|Kanunda belirtilen suçlarda şüpheli ile mağdurun uzlaştırmacı aracılığıyla anlaşması|Yargı|Ceza muhakemesi hukuku
Yargılamanın yenilenmesi|Kesinleşmiş bir hükmün kanunda sayılan sebeplerle yeniden incelenmesi|Yargı|-
İstinaf|İlk derece mahkemesi kararlarının bölge mahkemelerince hem maddi hem hukuki yönden incelenmesi|Yargı|-
Temyiz|Kararların Yargıtay veya Danıştay tarafından hukuka uygunluk yönünden incelenmesi|Yargı|-
Tabii hâkim ilkesi|Kimsenin kanunen tabi olduğu mahkemeden başka bir merci önüne çıkarılamaması|Yargı|-
Bireysel başvuru|Anayasa'da güvence altına alınan bir hakkının kamu gücü tarafından ihlal edildiğini iddia eden kişinin Anayasa Mahkemesine başvurması|Yargı|Anayasa hukuku
Somut norm denetimi|Bakmakta olduğu davada uygulanacak kanunu Anayasa'ya aykırı gören mahkemenin Anayasa Mahkemesine başvurması (itiraz yolu)|Yargı|Anayasa hukuku
Soyut norm denetimi|Kanunların yayımından sonra belirli sürede belirli kişilerce Anayasa Mahkemesinde açılan iptal davası|Yargı|Anayasa hukuku
Yüce Divan|Anayasa Mahkemesinin üst düzey devlet görevlilerini görevleriyle ilgili suçlardan yargılarken aldığı ad|Yargı|Anayasa hukuku
Merkezden yönetim|Kamu hizmetlerinin merkezî idare tarafından tek elden yürütülmesi|İdare|İdare hukuku
Yerinden yönetim|Kamu hizmetlerinin merkezî idareden ayrı tüzel kişiliğe sahip kuruluşlarca yürütülmesi|İdare|İdare hukuku
Yetki genişliği|Merkezî idarenin taşra teşkilatına bazı konularda karar alma yetkisi tanıması|İdare|İdare hukuku
Hiyerarşi|Merkezî idarede üst makamın astları üzerindeki emir ve denetim yetkisi|İdare|İdare hukuku
İdari vesayet|Merkezî idarenin yerinden yönetim kuruluşları üzerinde kanunla sınırlı denetim yetkisi|İdare|İdare hukuku
Hizmet yönünden yerinden yönetim|Belirli bir kamu hizmetinin üniversiteler, TRT gibi ayrı tüzel kişiliği olan kuruluşlarca yürütülmesi|İdare|İdare hukuku
Yer yönünden yerinden yönetim|Belirli bir bölgede yaşayanların ortak ihtiyaçlarının il özel idaresi, belediye ve köy tarafından karşılanması|İdare|İdare hukuku
Kamu hizmeti|Devlet veya diğer kamu tüzel kişilerince ya da onların denetiminde toplumun ortak ihtiyaçlarını karşılamak için sürekli yürütülen faaliyet|Kamu Hizmetleri|İdare hukuku
Süreklilik ilkesi|Kamu hizmetinin kesintisiz ve düzenli biçimde sunulması gerektiği ilkesi|Kamu Hizmetleri|İdare hukuku
Değişkenlik (uyum) ilkesi|Kamu hizmetinin değişen ihtiyaç ve teknolojiye göre uyarlanması gerektiği ilkesi|Kamu Hizmetleri|İdare hukuku
İmtiyaz|Bir kamu hizmetinin yürütülmesinin sözleşmeyle özel kişiye bırakılması|Kamu Hizmetleri|İdare hukuku
İdari işlem|İdarenin kamu gücüne dayanarak tek yanlı irade açıklamasıyla yaptığı hukuki işlem|İdare|İdare hukuku
İdari yargıda iptal davası|İdari işlemlerin yetki, şekil, sebep, konu ve amaç yönlerinden hukuka aykırılığı nedeniyle açılan dava|Yargı|İdare hukuku
Tam yargı davası|İdari eylem ve işlemlerle hakları ihlal edilenlerin zararlarının giderilmesi için açtıkları dava|Yargı|İdare hukuku
Kamulaştırma|Kamu yararı için özel mülkiyetteki taşınmazın bedeli peşin ödenerek idarece alınması|İdare|İdare hukuku
Özelleştirme|Kamu kuruluşlarının mülkiyetinin ya da işletme hakkının özel sektöre devredilmesi|İdare|İdare hukuku
Vali|İlde devletin ve Cumhurbaşkanının temsilcisi olan mülki idare amiri|İdare|İdare hukuku
Kaymakam|İlçenin genel idaresinden sorumlu mülki idare amiri|İdare|İdare hukuku
Muhtar|Köy ve mahallede halkın seçtiği yönetici|İdare|İdare hukuku
Kamu denetçisi (ombudsman)|İdarenin işleyişiyle ilgili şikâyetleri inceleyen, TBMM Başkanlığına bağlı kurumun denetçisi|İdare|İdare hukuku
Genel oy ilkesi|Kanunun aradığı yaşı dolduran her vatandaşın oy kullanabilmesi ilkesi|Seçimler|Anayasa hukuku
Eşit oy ilkesi|Her seçmenin bir oy hakkı olması ve oyların eşit değer taşıması ilkesi|Seçimler|Anayasa hukuku
Gizli oy ilkesi|Seçmenin oyunu kimseye göstermeden kullanması ilkesi|Seçimler|Anayasa hukuku
Açık sayım ve döküm ilkesi|Oyların herkesin izleyebileceği biçimde sayılıp dökümünün yapılması ilkesi|Seçimler|Anayasa hukuku
Tek dereceli seçim|Seçmenlerin temsilcilerini aracı olmadan doğrudan seçmesi|Seçimler|Anayasa hukuku
Serbest seçim ilkesi|Seçmenin oyunu hiçbir baskı altında kalmadan kullanması ilkesi|Seçimler|Anayasa hukuku
Seçim barajı|Siyasi partilerin milletvekili çıkarabilmek için ülke genelinde almaları gereken en düşük oy oranı|Seçimler|Anayasa hukuku
Nispi temsil|Partilerin aldıkları oy oranında temsilci çıkardığı seçim sistemi|Seçimler|Anayasa hukuku
Çoğunluk sistemi|Seçim çevresinde en çok oyu alan aday ya da partinin temsilciliği kazandığı seçim sistemi|Seçimler|Anayasa hukuku
D'Hondt sistemi|Türkiye'de milletvekili seçimlerinde kullanılan nispi temsil hesaplama yöntemi|Seçimler|Anayasa hukuku
Ara seçim|Boşalan milletvekillikleri için genel seçimler arasında yapılan seçim|Seçimler|Anayasa hukuku
Halkoylaması (referandum)|Bir konunun doğrudan halkın oyuna sunulması|Seçimler|Anayasa hukuku
Siyasi parti grubu|TBMM'de en az 20 milletvekiline sahip partinin oluşturduğu grup|Siyasi Partiler|Anayasa hukuku
Yasama dokunulmazlığı|Milletvekilinin, suç işlediği ileri sürülse bile Meclis kararı olmadan tutulamaması, sorguya çekilememesi ve yargılanamaması|TBMM|Anayasa hukuku
Yasama sorumsuzluğu|Milletvekilinin Meclis çalışmalarındaki oy ve sözlerinden dolayı sorumlu tutulamaması|TBMM|Anayasa hukuku
Meclis araştırması|Belli bir konuda bilgi edinmek amacıyla TBMM'nin yaptığı inceleme|TBMM|Anayasa hukuku
Genel görüşme|Toplumu ve devlet faaliyetlerini ilgilendiren belli bir konunun TBMM Genel Kurulunda görüşülmesi|TBMM|Anayasa hukuku
Yazılı soru|Milletvekillerinin Cumhurbaşkanı yardımcıları ve bakanlardan yazılı olarak bilgi istemesi|TBMM|Anayasa hukuku
Meclis soruşturması|Cumhurbaşkanı yardımcıları ve bakanların görevleriyle ilgili suçları hakkında TBMM'nin başlattığı soruşturma|TBMM|Anayasa hukuku
Kanun teklifi|Milletvekillerinin kanun yapılması amacıyla TBMM Başkanlığına sunduğu metin|TBMM|Anayasa hukuku
Başkanlık Divanı|TBMM Başkanı, başkanvekilleri, kâtip üyeler ve idare amirlerinden oluşan kurul|TBMM|Anayasa hukuku
Negatif statü hakları|Bireyi devlete karşı koruyan, devlete müdahale etmeme yükümlülüğü yükleyen kişi hakları|Haklar|Anayasa hukuku
Pozitif statü hakları|Devletten olumlu bir edim, hizmet istemeyi sağlayan sosyal ve ekonomik haklar|Haklar|Anayasa hukuku
Aktif statü hakları|Bireyin devlet yönetimine katılmasını sağlayan siyasi haklar|Haklar|Anayasa hukuku
Birinci kuşak haklar|Kişisel ve siyasi haklardan oluşan klasik haklar|İnsan Hakları|-
İkinci kuşak haklar|Sosyal ve ekonomik haklar|İnsan Hakları|-
Üçüncü kuşak haklar|Barış, temiz çevre ve gelişme hakkı gibi dayanışma hakları|İnsan Hakları|-
Hukuk devleti|Devletin bütün eylem ve işlemlerinin hukuka bağlı ve yargı denetimine açık olduğu devlet|Hukukun Üstünlüğü|Anayasa hukuku
Sosyal devlet|Bireylerin insan onuruna yaraşır bir yaşam düzeyine ulaşmasını sağlamayı görev edinen devlet|Anayasa|Anayasa hukuku
Laik devlet|Din ve devlet işlerinin ayrı tutulduğu ve devletin bütün inançlara eşit uzaklıkta durduğu devlet|Anayasa|Anayasa hukuku
Üniter devlet|Tek bir yasama, yürütme ve yargı teşkilatına sahip devlet|Anayasa|Anayasa hukuku
Federal devlet|Birden fazla yasama, yürütme ve yargı teşkilatı bulunan, federe birimlerden oluşan devlet|Anayasa|Anayasa hukuku
Kuvvetler ayrılığı|Yasama, yürütme ve yargı yetkilerinin ayrı organlarca kullanılması|Anayasa|Anayasa hukuku
Memur|Kamu hizmetlerini genel idare esaslarına göre asli ve sürekli görev olarak yürüten kamu görevlisi|Memuriyet|İdare hukuku
Sözleşmeli personel|Zaruri hâllerde özel bir mesleki bilgi isteyen işler için sözleşmeyle çalıştırılan personel|Memuriyet|İdare hukuku
Geçici personel|Bir yıldan az süreli ya da mevsimlik hizmetlerde sözleşmeyle çalıştırılan personel|Memuriyet|İdare hukuku
Aday memur|Asli memurluğa atanmadan önce adaylık süresini tamamlaması gereken memur|Memuriyet|İdare hukuku
Uyarma cezası|Memura görevinde ve davranışlarında daha dikkatli olması gerektiğinin yazı ile bildirilmesi|Disiplin|İdare hukuku
Kınama cezası|Memura görevinde ve davranışlarında kusurlu sayıldığının yazı ile bildirilmesi|Disiplin|İdare hukuku
Aylıktan kesme cezası|Memurun brüt aylığından 1/30 ile 1/8 arasında kesinti yapılması|Disiplin|İdare hukuku
Kademe ilerlemesinin durdurulması|Memurun bulunduğu kademede ilerlemesinin 1 ila 3 yıl süreyle durdurulması|Disiplin|İdare hukuku
Devlet memurluğundan çıkarma|Memurun bir daha devlet memurluğuna atanmamak üzere memurluktan çıkarılması|Disiplin|İdare hukuku
Görevden uzaklaştırma|Kamu hizmetinin gerekleri bakımından görevi başında kalmasında sakınca görülen memur hakkında alınan ihtiyati tedbir|Disiplin|İdare hukuku
Kademe|Memurun derecesi içindeki ilerleme basamağı|Memuriyet|İdare hukuku
Katı anayasa|Değiştirilmesi kanunlardan daha zor ve özel usullere bağlı olan anayasa|Anayasa|Anayasa hukuku
Yumuşak anayasa|Kanunlarla aynı usulle değiştirilebilen anayasa|Anayasa|Anayasa hukuku
Asli kurucu iktidar|Hukuki bir boşluk içinde yeni bir anayasa yapan iktidar|Anayasa|Anayasa hukuku
Tali kurucu iktidar|Mevcut anayasanın gösterdiği usule göre anayasayı değiştirme yetkisi|Anayasa|Anayasa hukuku
Monarşi|Egemenliğin tek bir kişide toplandığı ve genellikle babadan oğula geçtiği yönetim|Anayasa|Anayasa hukuku
Oligarşi|Egemenliğin küçük ve ayrıcalıklı bir zümrenin elinde bulunduğu yönetim|Anayasa|Anayasa hukuku
Teokrasi|Devlet yönetiminin din kurallarına dayandığı yönetim|Anayasa|Anayasa hukuku
Doğrudan demokrasi|Halkın yönetime aracısız olarak bizzat katıldığı demokrasi türü|Anayasa|Anayasa hukuku
Temsilî demokrasi|Halkın egemenliğini seçtiği temsilciler aracılığıyla kullandığı demokrasi türü|Anayasa|Anayasa hukuku
Yarı doğrudan demokrasi|Temsilî demokrasinin halkoylaması, halk girişimi gibi araçlarla desteklendiği demokrasi türü|Anayasa|Anayasa hukuku
Parlamenter sistem|Yürütmenin yasama organından doğduğu ve ona karşı sorumlu olduğu hükümet sistemi|Anayasa|Anayasa hukuku
Başkanlık sistemi|Yasama ve yürütmenin birbirinden sert biçimde ayrıldığı, yürütmenin halkça seçilen başkanda toplandığı sistem|Anayasa|Anayasa hukuku
Meclis hükümeti sistemi|Yasama ve yürütme yetkilerinin mecliste toplandığı hükümet sistemi|Anayasa|Anayasa hukuku
Gensoru|Hükümetin siyasi sorumluluğunu harekete geçiren ve 2017 değişikliğiyle kaldırılan denetim yolu|TBMM|Anayasa hukuku
Güvenoyu|Parlamenter sistemde hükümetin meclisten güven alması işlemi|TBMM|Anayasa hukuku
Pozitif hukuk|Belirli bir ülkede belirli bir zamanda yürürlükte olan hukuk kuralları|Hukuk|-
Tabii hukuk|İnsan doğasından ve akıldan kaynaklandığı kabul edilen, değişmez ve evrensel hukuk|Hukuk|-
Sübjektif hak|Hukuk düzeninin kişilere tanıdığı yetki|Hukuk|-
Mutlak hak|Herkese karşı ileri sürülebilen hak|Hukuk|-
Nisbi hak|Yalnızca belirli kişilere karşı ileri sürülebilen hak|Hukuk|-
Emredici hukuk kuralı|Uygulanması zorunlu olan ve tarafların aksini kararlaştıramayacağı kural|Hukuk|-
Tamamlayıcı hukuk kuralı|Tarafların düzenlemediği konularda uygulanan ve aksi kararlaştırılabilen kural|Hukuk|-
Yorumlayıcı hukuk kuralı|Tarafların açık olmayan iradelerini açıklığa kavuşturan kural|Hukuk|-
Tanımlayıcı hukuk kuralı|Bir kavramın ya da kurumun ne olduğunu açıklayan kural|Hukuk|-
İçtihat|Yüksek mahkemelerin benzer olaylarda verdikleri ve yol gösterici olan kararlar|Hukuk|-
Doktrin (öğreti)|Hukuk bilim insanlarının görüş ve eserleri|Hukuk|-
Kazanılmış hak|Hukuka uygun olarak elde edilmiş ve sonradan çıkan kurallarla ortadan kaldırılamayan hak|Hukuk|-
Dürüstlük kuralı|Herkesin haklarını kullanırken ve borçlarını yerine getirirken uyması gereken objektif iyiniyet ölçüsü|Hukuk|Medeni hukuk
İspat yükü|İddia edilen bir olgunun varlığını kanıtlama yükümlülüğü|Hukuk|-
Kesin hükümsüzlük|Kanunun emredici hükümlerine aykırı hukuki işlemin baştan itibaren geçersiz olması|Hukuk|-
Bağışlama|Bağışlayanın malvarlığından bağışlanana karşılıksız kazandırma yaptığı sözleşme|Hukuk|Borçlar hukuku
Kira sözleşmesi|Kiraya verenin bir şeyin kullanılmasını bedel karşılığında kiracıya bıraktığı sözleşme|Hukuk|Borçlar hukuku
Vekâlet sözleşmesi|Vekilin, vekâlet verenin bir işini görmeyi ya da işlemini yapmayı üstlendiği sözleşme|Hukuk|Borçlar hukuku
Eser sözleşmesi|Yüklenicinin bir eser meydana getirmeyi, iş sahibinin de bedel ödemeyi üstlendiği sözleşme|Hukuk|Borçlar hukuku
Anonim şirket|Sermayesi paylara bölünmüş ve borçlarından yalnız malvarlığıyla sorumlu olan sermaye şirketi|Hukuk|Ticaret hukuku
Limited şirket|Ortaklarının sorumluluğu taahhüt ettikleri sermaye payıyla sınırlı olan sermaye şirketi|Hukuk|Ticaret hukuku
Kollektif şirket|Ortaklarının tamamının şirket borçlarından sınırsız sorumlu olduğu şahıs şirketi|Hukuk|Ticaret hukuku
Komandit şirket|Ortaklarından bir kısmının sınırsız, bir kısmının sınırlı sorumlu olduğu şahıs şirketi|Hukuk|Ticaret hukuku
Çek|Bankaya hitaben yazılan ve görüldüğünde ödenmesi gereken ödeme aracı kıymetli evrak|Hukuk|Ticaret hukuku
Bono|Düzenleyenin belirli bir tarihte belirli bir bedeli ödemeyi üstlendiği kıymetli evrak|Hukuk|Ticaret hukuku
Konkordato|Borçlarını ödeyemeyecek durumdaki borçlunun alacaklılarıyla vade ve indirim konusunda mahkeme denetiminde anlaşması|Hukuk|-
Haciz|Borcun ödenmemesi hâlinde borçlunun mallarına icra dairesince el konulması|Hukuk|-
İhtiyati tedbir|Dava sonuçlanıncaya kadar hakkın elde edilmesinin zorlaşmasını önlemek için verilen geçici koruma kararı|Yargı|-
Arabuluculuk|Uyuşmazlığın tarafsız bir üçüncü kişinin yardımıyla tarafların iradesiyle çözülmesi yöntemi|Yargı|-
Tahkim|Uyuşmazlığın taraflarca seçilen hakemlerce çözülmesi|Yargı|-
Teşebbüs|Kişinin işlemeyi kastettiği suçu elverişli hareketlerle doğrudan başlayıp elinde olmayan nedenlerle tamamlayamaması|Hukuk|Ceza hukuku
Azmettirme|Başkasını suç işlemeye karar verdirme|Hukuk|Ceza hukuku
Haksız tahrik|Haksız bir fiilin oluşturduğu hiddet veya şiddetli elemin etkisi altında suç işlenmesi hâli|Hukuk|Ceza hukuku
Zorunluluk hâli|Kendisine veya başkasına ait bir hakka yönelik ağır ve muhakkak bir tehlikeden kurtulmak için başka çare bulunmaması durumu|Hukuk|Ceza hukuku
Etkin pişmanlık|Fail suçu işledikten sonra zararı gidermeye yönelik davranışta bulunduğunda cezasında indirim yapılması|Hukuk|Ceza hukuku
Adli para cezası|Beş günden az ve kanunda aksine hüküm yoksa yedi yüz otuz günden fazla olmamak üzere belirlenen tam gün sayısının bir gün karşılığı miktarla çarpılmasıyla hesaplanan ceza|Hukuk|Ceza hukuku
Güvenlik tedbiri|Suç işleyen kişiye ceza yerine ya da cezayla birlikte uygulanan, korunma ve tedavi gibi amaçlı yaptırım|Hukuk|Ceza hukuku
Gözaltı|Yakalanan kişinin soruşturma işlemleri için kanunda belirtilen süre boyunca özgürlüğünün kısıtlanması|Yargı|Ceza muhakemesi hukuku
Tutuklama|Kuvvetli suç şüphesi bulunan kişinin hâkim kararıyla özgürlüğünün geçici olarak kısıtlanması|Yargı|Ceza muhakemesi hukuku
Adli kontrol|Tutuklama yerine şüpheli veya sanık hakkında yurt dışına çıkış yasağı gibi yükümlülükler getirilmesi|Yargı|Ceza muhakemesi hukuku
Soruşturma|Suç şüphesinin öğrenilmesinden iddianamenin kabulüne kadar geçen evre|Yargı|Ceza muhakemesi hukuku
Kovuşturma|İddianamenin kabulüyle başlayıp hükmün kesinleşmesine kadar geçen evre|Yargı|Ceza muhakemesi hukuku
Şüpheli|Soruşturma evresinde suç şüphesi altında bulunan kişi|Yargı|Ceza muhakemesi hukuku
Sanık|Kovuşturmanın başlamasından hükmün kesinleşmesine kadar suç şüphesi altında bulunan kişi|Yargı|Ceza muhakemesi hukuku
Kovuşturmaya yer olmadığına dair karar|Yeterli şüphe oluşturacak delil bulunamadığında Cumhuriyet savcısının verdiği karar|Yargı|Ceza muhakemesi hukuku
Kamu tüzel kişisi|Kamu hukuku kurallarıyla kurulan ve kamu gücü kullanabilen tüzel kişi|İdare|İdare hukuku
Kamu kurumu niteliğindeki meslek kuruluşu|Belirli bir mesleğe mensup olanlarca oluşturulan, organlarını üyelerin seçtiği kamu tüzel kişisi (barolar, tabip odaları gibi)|İdare|İdare hukuku
Bağımsız idari otorite|Belirli bir sektörü düzenleyip denetleyen, hiyerarşi ve vesayet dışında kalan idari kurum|İdare|İdare hukuku
Kamu malı|Kamunun ortak kullanımına ya da bir kamu hizmetine ayrılmış mallar|İdare|İdare hukuku
Kolluk|Kamu düzenini korumak amacıyla yürütülen idari faaliyet ve bunu yürüten birimler|İdare|İdare hukuku
İl idare kurulu|Valinin başkanlığında il hukuk işleri müdürü ve bazı müdürlerden oluşan kurul|İdare|İdare hukuku
İl encümeni|İl özel idaresinde valinin başkanlığında il genel meclisi ve birim amirleri arasından oluşan kurul|İdare|İdare hukuku
İl genel meclisi|İl özel idaresinin seçimle oluşan karar organı|İdare|İdare hukuku
Belediye meclisi|Belediyenin seçimle oluşan karar organı|İdare|İdare hukuku
Belediye encümeni|Belediye başkanının başkanlığında meclis üyeleri ve birim amirlerinden oluşan kurul|İdare|İdare hukuku
Köy derneği|Köyde yaşayan seçmenlerden oluşan köyün karar organı|İdare|İdare hukuku
İhtiyar meclisi|Muhtarın başkanlığında köy ya da mahallede seçimle oluşan kurul|İdare|İdare hukuku
Büyükşehir belediyesi|Sınırları il mülki sınırı olan ve ilçe belediyeleri arasında koordinasyonu sağlayan belediye|İdare|İdare hukuku
Mal bildirimi|Kamu görevlilerinin göreve başlarken ve belirli dönemlerde mal varlıklarını bildirme yükümlülüğü|Memuriyet|İdare hukuku
Memurlukta vekâlet|Görevden ayrılan memurun yerine başka bir memurun geçici olarak görevlendirilmesi|Memuriyet|İdare hukuku
Disiplin amiri|Memura disiplin cezası verme yetkisine sahip amir|Disiplin|İdare hukuku
Derece|Memurların kadro seviyesini gösteren ve birden on beşe kadar sıralanan basamak|Memuriyet|İdare hukuku
Halk girişimi|Belirli sayıda seçmenin kanun ya da anayasa değişikliği önerebilmesi|Seçimler|Anayasa hukuku
Plebisit|Bir kişiye ya da yönetime güven belirtme amacı taşıyan halkoylaması|Seçimler|Anayasa hukuku
Seçim çevresi|Seçmenlerin oy kullandığı ve temsilci çıkardığı coğrafi birim|Seçimler|Anayasa hukuku
Seçmen kütüğü|Seçmenlerin kayıtlı olduğu resmî liste|Seçimler|Anayasa hukuku
Seçim yasakları|Seçim dönemlerinde propaganda, yayın ve benzeri konularda getirilen sınırlamalar|Seçimler|Anayasa hukuku
Kapatma davası|Anayasa'ya aykırı eylemleri nedeniyle siyasi parti hakkında Yargıtay Cumhuriyet Başsavcısının Anayasa Mahkemesinde açtığı dava|Siyasi Partiler|Anayasa hukuku
Hazine yardımı|Belirli oy oranını aşan siyasi partilere devlet bütçesinden yapılan yardım|Siyasi Partiler|Anayasa hukuku
Ölüme bağlı tasarruf|Kişinin ölümünden sonra hüküm doğuracak şekilde malvarlığı hakkında yaptığı vasiyetname veya miras sözleşmesi|Hukuk|Medeni hukuk
Yasal mirasçı|Kanunun mirasçı olarak belirlediği kan hısımları ve sağ kalan eş|Hukuk|Medeni hukuk
Edinilmiş mallara katılma rejimi|Aksi kararlaştırılmadıkça eşler arasında geçerli olan yasal mal rejimi|Hukuk|Medeni hukuk
Ad (isim) hakkı|Kişinin adının korunmasını ve kullanılmasını sağlayan kişilik hakkı|Hukuk|Medeni hukuk
Taşınmaz rehni|İpotek gibi bir taşınmaz üzerinde alacağı güvence altına alan sınırlı ayni hak|Hukuk|Medeni hukuk
Temerrüt|Borçlunun muaccel borcunu zamanında ifa etmemesi|Hukuk|Borçlar hukuku
Ceza koşulu|Borcun hiç veya gereği gibi ifa edilmemesi hâlinde ödenmesi kararlaştırılan bedel|Hukuk|Borçlar hukuku
Ticari işletme|Esnaf işletmesi sınırını aşan gelir sağlamayı hedef tutan faaliyetlerin sürekli yürütüldüğü işletme|Hukuk|Ticaret hukuku
Ticaret sicili|Tacirlere ve ticari işletmelere ilişkin bilgilerin kaydedildiği resmî sicil|Hukuk|Ticaret hukuku
Marka|Bir işletmenin mal veya hizmetlerini diğerlerinden ayırt etmeye yarayan işaret|Hukuk|Ticaret hukuku
Toplu iş sözleşmesi|İşçi sendikası ile işveren veya işveren sendikası arasında yapılan sözleşme|Hukuk|İş hukuku
Kıdem tazminatı|Kanunda belirtilen hâllerde iş sözleşmesi sona eren işçiye çalışma süresine göre ödenen tazminat|Hukuk|İş hukuku
İhbar süresi|İş sözleşmesini fesheden tarafın karşı tarafa önceden bildirimde bulunması gereken süre|Hukuk|İş hukuku
Lokavt|İşverenin işçileri topluca işten uzaklaştırması|Hukuk|İş hukuku
Yıllık ücretli izin|İşçiye belirli süre çalıştıktan sonra ücreti ödenerek verilen dinlenme izni|Hukuk|İş hukuku
İş kazası|Sigortalının işyerinde veya işin yürütümü sırasında uğradığı ve bedenen ya da ruhen zarara yol açan olay|Hukuk|-
Vergi mükellefi|Vergi kanunlarına göre kendisine vergi borcu düşen kişi|Hukuk|Vergi hukuku
Tarh|Vergi alacağının vergi dairesince hesaplanarak miktar olarak belirlenmesi|Hukuk|Vergi hukuku
Tahakkuk|Tarh edilen verginin ödenmesi gereken aşamaya gelmesi|Hukuk|Vergi hukuku
Tahsil|Vergi borcunun kanuna uygun olarak ödenmesi|Hukuk|Vergi hukuku
Vergi muafiyeti|Belirli kişilerin vergi yükümlülüğü dışında tutulması|Hukuk|Vergi hukuku
Vergi istisnası|Belirli konu ya da işlemlerin vergi dışında bırakılması|Hukuk|Vergi hukuku
Kamu ihalesi|İdarelerin mal, hizmet ve yapım işlerini kanundaki usullerle temin etmesi|İdare|İdare hukuku
Mülki idare amiri|Vali ve kaymakam gibi illerde ve ilçelerde devleti temsil eden yönetici|İdare|İdare hukuku
Hukuki işlem|Bir veya birden çok kişinin hukuki sonuç doğurmaya yönelik irade açıklaması|Hukuk|-
Ayıplı mal|Satıcının bildirdiği niteliklere sahip olmayan ya da değerini azaltan eksiklik taşıyan mal|Hukuk|Borçlar hukuku
Tüketici hakem heyeti|Belirli değerin altındaki tüketici uyuşmazlıklarına bakmakla görevli kurul|Hukuk|-
Vatandaşlık|Kişiyi devlete bağlayan hukuki ve siyasi bağ|Anayasa|Anayasa hukuku
Çifte vatandaşlık|Bir kişinin aynı anda iki devletin vatandaşı olması|Anayasa|-
Sığınma|Ülkesinde zulüm gören kişinin başka bir devletten koruma istemesi|İnsan Hakları|-
Fesih (meclis için)|Yasama organının görev süresi dolmadan sona erdirilmesi|TBMM|Anayasa hukuku
Kanun hükmünde kararname|2017 değişikliğiyle kaldırılan, yetki kanununa dayanılarak çıkarılan düzenleyici işlem|Yürütme|Anayasa hukuku
Torba kanun|Birbiriyle ilgisi az olan pek çok düzenlemeyi tek metinde toplayan kanun|TBMM|-
İç tüzük|TBMM'nin çalışma usul ve esaslarını düzenleyen ve yalnızca Meclis tarafından yapılan düzenleme|TBMM|Anayasa hukuku
Tüketici|Ticari veya mesleki olmayan amaçlarla hareket eden gerçek ya da tüzel kişi|Hukuk|-
Kişilik hakkı|Kişinin yaşamı, sağlığı, onuru ve özel hayatı gibi kişisel değerleri üzerindeki hakkı|Hukuk|Medeni hukuk
Ortaklığın giderilmesi|Paylı veya elbirliği mülkiyetindeki malın paylaştırılması ya da satılarak bedelinin bölüştürülmesi|Hukuk|Medeni hukuk
"""

# yetki | sahibi
YETKILER = """
Kanun koymak, değiştirmek ve kaldırmak|TBMM
Bütçe ve kesin hesap kanunlarını kabul etmek|TBMM
Para basılmasına karar vermek|TBMM
Savaş ilanına karar vermek|TBMM
Genel ve özel af ilanına karar vermek|TBMM
Milletlerarası antlaşmaların onaylanmasını uygun bulmak|TBMM
Cumhurbaşkanını Yüce Divan'a sevk etmek|TBMM
Anayasa Mahkemesine üç üye seçmek|TBMM
Hâkimler ve Savcılar Kurulunun yedi üyesini seçmek|TBMM
Sayıştay Başkanı ve üyelerini seçmek|TBMM
Kamu Başdenetçisini seçmek|TBMM
Bütçe kanun teklifini hazırlayıp TBMM'ye sunmak|Cumhurbaşkanı
Cumhurbaşkanlığı kararnamesi çıkarmak|Cumhurbaşkanı
Kanunları yayımlamak|Cumhurbaşkanı
Kanunları bir daha görüşülmek üzere TBMM'ye geri göndermek|Cumhurbaşkanı
Cumhurbaşkanı yardımcılarını ve bakanları atamak ve görevden almak|Cumhurbaşkanı
Olağanüstü hâl ilan etmek|Cumhurbaşkanı
Millî Güvenlik Kurulunu toplantıya çağırmak|Cumhurbaşkanı
Türk Silahlı Kuvvetlerinin kullanılmasına karar vermek|Cumhurbaşkanı
Sürekli hastalık, sakatlık ve kocama sebebiyle kişilerin cezalarını hafifletmek veya kaldırmak|Cumhurbaşkanı
Rektörleri atamak|Cumhurbaşkanı
Anayasa Mahkemesinin on iki üyesini seçmek|Cumhurbaşkanı
Hâkimler ve Savcılar Kurulunun dört üyesini atamak|Cumhurbaşkanı
Danıştay üyelerinin dörtte birini seçmek|Cumhurbaşkanı
Diyanet İşleri Başkanını atamak|Cumhurbaşkanı
Kanunların Anayasa'ya şekil ve esas bakımından uygunluğunu denetlemek|Anayasa Mahkemesi
Siyasi partilerin kapatılmasına ilişkin davaları karara bağlamak|Anayasa Mahkemesi
Bireysel başvuruları karara bağlamak|Anayasa Mahkemesi
Siyasi partilerin mali denetimini yapmak|Anayasa Mahkemesi
Yüce Divan sıfatıyla yargılama yapmak|Anayasa Mahkemesi
Hâkim ve savcıları mesleğe kabul etmek, atamak ve nakletmek|Hâkimler ve Savcılar Kurulu
Yargıtay üyelerini seçmek|Hâkimler ve Savcılar Kurulu
Danıştay üyelerinin dörtte üçünü seçmek|Hâkimler ve Savcılar Kurulu
Seçimlerin başlangıcından bitimine kadar genel yönetim ve denetimini yapmak|Yüksek Seçim Kurulu
Seçim sonuçlarını kesinleştirmek|Yüksek Seçim Kurulu
Merkezî yönetim kapsamındaki kamu idarelerinin gelir ve giderlerini TBMM adına denetlemek|Sayıştay
İdare ve vergi mahkemelerince verilen kararların son inceleme mercii olmak|Danıştay
Adliye mahkemelerince verilen karar ve hükümlerin son inceleme mercii olmak|Yargıtay
Adli ve idari yargı mercileri arasındaki görev uyuşmazlıklarını kesin olarak çözmek|Uyuşmazlık Mahkemesi
İdarenin işleyişiyle ilgili şikâyetleri incelemek|Kamu Denetçiliği Kurumu
Devletin millî güvenlik siyasetiyle ilgili tavsiye kararları almak|Millî Güvenlik Kurulu
Yükseköğretim kurumlarını planlamak, düzenlemek ve denetlemek|Yükseköğretim Kurulu
Radyo ve televizyon yayınlarını düzenlemek ve denetlemek|Radyo ve Televizyon Üst Kurulu
İslam dininin inançları, ibadeti ve ahlak esaslarıyla ilgili işleri yürütmek|Diyanet İşleri Başkanlığı
Belediye bütçesini kabul etmek|Belediye meclisi
"""

# konu | soru | doğru | yanlış1..4 | gerekçe
SAYISAL = """
TBMM|1982 Anayasası'na göre TBMM kaç milletvekilinden oluşur?|600|550|450|500|650|2017 değişikliğiyle milletvekili sayısı 600'dür (Anayasa m.75).
TBMM|Milletvekili seçilebilmek için kaç yaşını doldurmuş olmak gerekir?|18|21|25|30|20|2017 değişikliğiyle milletvekili seçilme yaşı 18'dir (m.76).
Seçimler|TBMM ve Cumhurbaşkanlığı seçimleri kaç yılda bir yapılır?|5|4|6|7|3|Seçimler beş yılda bir aynı gün yapılır (m.77).
Yürütme|Cumhurbaşkanı adayı olabilmek için kaç yaşını doldurmuş olmak gerekir?|40|35|45|30|50|Kırk yaşını doldurmuş, yükseköğrenim yapmış Türk vatandaşları aday olabilir (m.101).
Yürütme|Bir kişi en fazla kaç defa Cumhurbaşkanı seçilebilir?|2|1|3|4|Sınırsız|Bir kimse en fazla iki defa Cumhurbaşkanı seçilebilir (m.101).
Yürütme|Cumhurbaşkanının görev süresi kaç yıldır?|5|4|6|7|8|Cumhurbaşkanının görev süresi beş yıldır (m.101).
Yürütme|Cumhurbaşkanı adayı gösterebilmek için seçmenlerin en az kaç imzası gerekir?|100.000|50.000|200.000|20.000|500.000|En az yüz bin seçmen aday gösterebilir (m.101).
Yürütme|Son milletvekili genel seçiminde geçerli oyların toplamda en az yüzde kaçını alan partiler Cumhurbaşkanı adayı gösterebilir?|%5|%3|%7|%10|%1|Tek başına veya birlikte %5 oy alan partiler aday gösterebilir (m.101).
Yürütme|Cumhurbaşkanı seçiminin ilk oylamasında seçilebilmek için geçerli oyların ne kadarı gerekir?|Salt çoğunluk|Üçte bir|Beşte üç|Üçte iki|Dörtte bir|İlk oylamada geçerli oyların salt çoğunluğunu alan aday seçilir (m.102).
Yargı|Anayasa Mahkemesi kaç üyeden oluşur?|15|17|11|13|21|Anayasa Mahkemesi on beş üyeden oluşur (m.146).
Yargı|Anayasa Mahkemesi üyeleri kaç yıl için seçilir?|12|8|10|9|15|Üyeler on iki yıl için seçilir ve bir kişi iki defa seçilemez (m.147).
Yargı|Anayasa Mahkemesi üyeliğine seçilebilmek için kaç yaşını doldurmuş olmak gerekir?|45|40|35|50|30|Üye olabilmek için kırk beş yaşını doldurmuş olmak gerekir (m.146).
Yargı|Hâkimler ve Savcılar Kurulu kaç üyeden oluşur?|13|15|11|7|22|HSK on üç üyeden oluşur (m.159).
Yargı|Hâkimler ve Savcılar Kurulunun başkanı kimdir?|Adalet Bakanı|Cumhurbaşkanı|Yargıtay Başkanı|Anayasa Mahkemesi Başkanı|TBMM Başkanı|HSK'nın başkanı Adalet Bakanıdır (m.159).
Seçimler|Yüksek Seçim Kurulu kaç asıl üyeden oluşur?|7|11|5|9|13|YSK yedi asıl ve dört yedek üyeden oluşur (m.79).
Anayasa|Anayasa değişikliği teklifi en az kaç milletvekili tarafından yazıyla verilebilir?|200|151|301|360|400|TBMM üye tamsayısının en az üçte biri (200) tarafından teklif edilir (m.175).
Anayasa|Anayasa değişikliği teklifinin kabulü için gereken en az oy sayısı kaçtır?|360|301|400|200|151|Teklifin kabulü üye tamsayısının beşte üç (360) çoğunluğuyla mümkündür (m.175).
Anayasa|TBMM'de en az kaç oyla kabul edilen Anayasa değişikliği, Cumhurbaşkanı halkoylamasına sunmazsa doğrudan yürürlüğe girer?|400|360|301|450|200|Üçte iki (400) çoğunlukla kabul edilen değişikliği Cumhurbaşkanı halkoylamasına sunmazsa yayımlanır (m.175).
TBMM|TBMM'nin seçimlerin yenilenmesine karar verebilmesi için gereken çoğunluk nedir?|Üye tamsayısının beşte üçü|Üye tamsayısının salt çoğunluğu|Toplantıya katılanların salt çoğunluğu|Üye tamsayısının üçte biri|Üye tamsayısının dörtte biri|TBMM üye tamsayısının beşte üç çoğunluğuyla seçimlerin yenilenmesine karar verebilir (m.116).
TBMM|TBMM'nin toplantı yeter sayısı nedir?|Üye tamsayısının üçte biri|Üye tamsayısının salt çoğunluğu|Üye tamsayısının beşte üçü|Üye tamsayısının dörtte biri|Üye tamsayısının üçte ikisi|TBMM üye tamsayısının en az üçte biri (200) ile toplanır (m.96).
TBMM|TBMM'de bir siyasi parti grubu kurabilmek için en az kaç milletvekili gerekir?|20|10|25|30|15|Siyasi parti grubu en az yirmi milletvekiliyle kurulur.
Seçimler|Milletvekili genel seçimlerinde ülke geneli seçim barajı yüzde kaçtır?|%7|%10|%5|%3|%12|2022'de yapılan değişiklikle seçim barajı %7'ye indirilmiştir.
Yürütme|Olağanüstü hâl ilk ilanında en fazla kaç ay süreyle ilan edilebilir?|6|3|4|12|2|Olağanüstü hâl altı ayı geçmemek üzere ilan edilebilir (m.119).
Hukuk|Türk Medeni Kanunu'na göre erginlik kaç yaşın doldurulmasıyla başlar?|18|17|21|16|15|Ergin olma yaşı on sekizdir.
Hukuk|Kişi en erken kaç yaşında mahkeme kararıyla ergin kılınabilir?|15|14|16|17|12|On beş yaşını dolduran küçük, kendi isteği ve velisinin rızasıyla mahkemece ergin kılınabilir.
Hukuk|Türk Medeni Kanunu'na göre olağan durumda evlenme yaşı kaçtır?|17|18|16|15|19|Erkek veya kadın on yedi yaşını doldurmadıkça evlenemez; yasal temsilci izni gerekir.
Hukuk|Olağanüstü durumlarda hâkim kararıyla en erken kaç yaşında evlenilebilir?|16|15|17|14|18|Hâkim olağanüstü durumlarda on altı yaşını dolduran kişinin evlenmesine izin verebilir.
Hukuk|Evliliği sona eren kadın için öngörülen bekleme (iddet) süresi kaç gündür?|300|200|100|180|365|Kadın için bekleme süresi evliliğin sona ermesinden itibaren 300 gündür.
Hukuk|Türk Ceza Kanunu'na göre kaç yaşını doldurmamış çocukların ceza sorumluluğu yoktur?|12|15|18|10|14|Fiili işlediği sırada on iki yaşını doldurmamış çocukların ceza sorumluluğu yoktur.
Memuriyet|657 sayılı Kanun'a göre devlet memurluğuna alınmak için kaç yaşını bitirmiş olmak gerekir?|18|17|20|21|16|On sekiz yaşını bitirmiş olmak genel şartlardandır.
Memuriyet|657 sayılı Kanun'a göre adaylık süresi en az ve en çok ne kadardır?|1–2 yıl|6 ay–1 yıl|2–3 yıl|1–3 yıl|3–5 yıl|Adaylık süresi bir yıldan az, iki yıldan fazla olamaz.
Memuriyet|Hizmet süresi on yıla kadar olan memurun yıllık izni kaç gündür?|20|30|15|25|10|Hizmeti 1–10 yıl olanlara 20 gün yıllık izin verilir.
Memuriyet|Hizmet süresi on yıldan fazla olan memurun yıllık izni kaç gündür?|30|20|25|40|45|Hizmeti on yıldan fazla olanlara 30 gün yıllık izin verilir.
Disiplin|Aylıktan kesme cezasında memurun brüt aylığından ne oranda kesinti yapılır?|1/30–1/8|1/10–1/4|1/8–1/4|1/2–1/3|1/40–1/20|Aylıktan kesme brüt aylığın 1/30–1/8'i oranındadır.
Disiplin|Kademe ilerlemesinin durdurulması cezası kaç yıl süreyle uygulanabilir?|1–3 yıl|1–2 yıl|2–4 yıl|3–5 yıl|6 ay–1 yıl|Fiilin ağırlık derecesine göre 1–3 yıl kademe ilerlemesi durdurulur.
Disiplin|Disiplin cezalarına karşı itiraz süresi, kararın tebliğinden itibaren kaç gündür?|7|15|30|10|5|Disiplin cezalarına tebliğden itibaren yedi gün içinde itiraz edilebilir.
Disiplin|Disiplin soruşturması nedeniyle görevden uzaklaştırma tedbiri en çok kaç ay sürebilir?|3|6|1|12|2|Disiplin soruşturması sebebiyle görevden uzaklaştırma süresi üç ayı geçemez.
Disiplin|Devlet memurluğundan çıkarma cezasını gerektiren fiilin öğrenilmesinden itibaren kaç ay içinde soruşturmaya başlanmazsa ceza verme yetkisi zamanaşımına uğrar?|6|1|3|12|2|Memurluktan çıkarma cezasında bu süre altı aydır.
Siyasi Partiler|Siyasi parti kurmak için en az kaç kurucu gerekir?|30|20|50|10|100|Siyasi partiler en az otuz Türk vatandaşı tarafından kurulur.
Siyasi Partiler|Bir siyasi partiye üye olabilmek için kaç yaşını doldurmuş olmak gerekir?|18|21|16|20|25|On sekiz yaşını dolduran vatandaşlar partilere üye olabilir (m.68).
TBMM|1982 Anayasası'na göre TBMM yılda en çok ne kadar süre tatil yapabilir?|3 ay|2 ay|4 ay|6 ay|1 ay|TBMM yılda en çok üç ay tatil yapabilir (m.93).
Yargı|Bireysel başvuru, başvuru yollarının tüketilmesinden itibaren kaç gün içinde yapılmalıdır?|30|15|60|90|45|Bireysel başvuru otuz gün içinde yapılır.
Yargı|Somut norm denetiminde Anayasa Mahkemesi kararını kaç ay içinde vermelidir?|5|3|6|12|2|Anayasa Mahkemesi işi aldığı tarihten itibaren beş ay içinde karar verir (m.152).
Yargı|Soyut norm denetiminde iptal davası, kanunun Resmî Gazete'de yayımlanmasından itibaren kaç gün içinde açılmalıdır?|60|30|90|45|120|İptal davası açma hakkı yayımdan itibaren altmış gün sonra düşer (m.151).
Anayasa|Bilgi edinme başvurularına kural olarak kaç iş günü içinde cevap verilir?|15|10|30|7|20|Bilgi Edinme Hakkı Kanunu'na göre süre on beş iş günüdür.
Anayasa|Dilekçe Kanunu'na göre yapılan başvurulara en geç kaç gün içinde cevap verilmelidir?|30|15|60|10|45|Başvuru sahibine en geç otuz gün içinde cevap verilir.
Yürütme|Cumhurbaşkanı, kabul edilen kanunları kaç gün içinde yayımlar?|15|10|7|30|20|Cumhurbaşkanı kanunları on beş gün içinde yayımlar veya geri gönderir (m.89).
TBMM|Milletvekillerinin yazılı sorularına en geç kaç gün içinde cevap verilir?|15|7|30|10|20|Yazılı soru en geç on beş gün içinde cevaplandırılır (m.98).
Yürütme|Bütçe kanun teklifi mali yılbaşından en az kaç gün önce TBMM'ye sunulur?|75|60|90|45|30|Cumhurbaşkanı bütçe teklifini mali yılbaşından en az yetmiş beş gün önce sunar (m.161).
Yargı|Hâkim ve savcılar kural olarak kaç yaşını bitirinceye kadar görev yapar?|65|60|67|70|62|Hâkim ve savcılar altmış beş yaşını bitirinceye kadar hizmet görürler (m.139).
Seçimler|Seçim kanunlarında yapılan değişiklikler, yürürlüğe girdiği tarihten itibaren ne kadar süre içinde yapılacak seçimlerde uygulanmaz?|1 yıl|6 ay|2 yıl|3 ay|5 yıl|Seçim kanunlarındaki değişiklikler bir yıl içinde yapılacak seçimlerde uygulanmaz (m.67).
Seçimler|Seçme hakkı kaç yaşın doldurulmasıyla kazanılır?|18|21|20|16|25|On sekiz yaşını dolduran vatandaşlar seçimlere katılma hakkına sahiptir (m.67).
İdare|Belediye başkanları kaç yıl için seçilir?|5|4|6|3|7|Mahallî idare seçimleri beş yılda bir yapılır (m.127).
TBMM|2018 milletvekili genel seçimlerinden itibaren Türkiye'de kaç seçim bölgesi bulunmaktadır?|87|81|85|90|79|Milletvekili seçimleri 87 seçim bölgesinde yapılmaktadır.
Memuriyet|Memura doğumdan önce ve sonra toplam kaç hafta analık izni verilir?|16|12|20|8|24|Doğumdan önce 8, doğumdan sonra 8 hafta olmak üzere toplam 16 hafta analık izni verilir.
Memuriyet|Eşi doğum yapan memura kaç gün babalık izni verilir?|10|7|5|15|3|Memura eşinin doğum yapması hâlinde on gün babalık izni verilir.
Memuriyet|Memura kendisinin evlenmesi hâlinde kaç gün mazeret izni verilir?|7|5|10|3|15|Evlenme ve birinci derece yakınların ölümü hâllerinde yedi gün izin verilir.
"""

# Türk Medeni Kanunu kitapları
TMK = """
Ad (isim) hakkı|Kişiler Hukuku
Yerleşim yeri|Kişiler Hukuku
Hısımlık|Kişiler Hukuku
Hak ehliyeti ve fiil ehliyeti|Kişiler Hukuku
Gaiplik|Kişiler Hukuku
Dernekler|Kişiler Hukuku
Vakıflar|Kişiler Hukuku
Nişanlanma|Aile Hukuku
Evlenme|Aile Hukuku
Boşanma|Aile Hukuku
Eşler arasındaki mal rejimleri|Aile Hukuku
Soybağının kurulması|Aile Hukuku
Evlat edinme|Aile Hukuku
Velayet|Aile Hukuku
Vesayet|Aile Hukuku
Aile konutu|Aile Hukuku
Yasal mirasçılar|Miras Hukuku
Saklı paylı mirasçılar|Miras Hukuku
Vasiyetname|Miras Hukuku
Mirasçılık belgesi|Miras Hukuku
Mirasın reddi|Miras Hukuku
Mirasın paylaşılması|Miras Hukuku
Zilyetlik|Eşya Hukuku
Tapu sicili|Eşya Hukuku
Taşınmaz mülkiyeti|Eşya Hukuku
Taşınır mülkiyeti|Eşya Hukuku
İrtifak hakları|Eşya Hukuku
Taşınmaz rehni (ipotek)|Eşya Hukuku
Taşınır rehni|Eşya Hukuku
"""
TMK_SECENEK = ['Kişiler Hukuku', 'Aile Hukuku', 'Miras Hukuku', 'Eşya Hukuku', 'Borçlar Hukuku']

KAMU = ['Anayasa hukuku', 'İdare hukuku', 'Ceza hukuku', 'Vergi hukuku', 'Ceza muhakemesi hukuku', 'Medeni usul hukuku', 'Devletler genel hukuku']
OZEL = ['Medeni hukuk', 'Borçlar hukuku', 'Ticaret hukuku', 'Kişiler hukuku', 'Aile hukuku', 'Miras hukuku', 'Eşya hukuku',
        'Şirketler hukuku', 'Kıymetli evrak hukuku', 'Deniz ticareti hukuku', 'Sigorta hukuku']

# belge | yıl | ülke/kuruluş
BELGELER = """
Magna Carta|1215|İngiltere
Haklar Dilekçesi (Petition of Rights)|1628|İngiltere
Habeas Corpus|1679|İngiltere
Haklar Bildirgesi (Bill of Rights)|1689|İngiltere
Virginia Haklar Bildirgesi|1776|Amerika Birleşik Devletleri
İnsan ve Yurttaş Hakları Bildirgesi|1789|Fransa
İnsan Hakları Evrensel Beyannamesi|1948|Birleşmiş Milletler
Avrupa İnsan Hakları Sözleşmesi|1950|Avrupa Konseyi
Avrupa Sosyal Şartı|1961|Avrupa Konseyi
Helsinki Nihai Senedi|1975|Avrupa Güvenlik ve İşbirliği Konferansı
Çocuk Haklarına Dair Sözleşme|1989|Birleşmiş Milletler
Yeni Bir Avrupa İçin Paris Şartı|1990|Avrupa Güvenlik ve İşbirliği Konferansı
"""

# Türk anayasa/seçim tarihi: olay | yıl | konu
TARIHCE = """
Sened-i İttifak'ın imzalanması|1808|Anayasa
Tanzimat Fermanı'nın ilanı|1839|Anayasa
Islahat Fermanı'nın ilanı|1856|Anayasa
Kanun-i Esasi'nin ilanı|1876|Anayasa
Teşkilat-ı Esasiye Kanunu'nun kabulü|1921|Anayasa
1924 Anayasası'nın kabulü|1924|Anayasa
Kadınlara belediye seçimlerinde seçme ve seçilme hakkı tanınması|1930|Seçimler
Kadınlara muhtarlık seçimlerinde seçme ve seçilme hakkı tanınması|1933|Seçimler
Kadınlara milletvekili seçme ve seçilme hakkı tanınması|1934|Seçimler
Laiklik ilkesinin Anayasa'ya girmesi|1937|Anayasa
İlk çok partili genel seçim (açık oy, gizli tasnif)|1946|Seçimler
Gizli oy, açık tasnif ilkesinin ilk uygulandığı genel seçim|1950|Seçimler
1961 Anayasası'nın halkoylamasıyla kabulü|1961|Anayasa
1982 Anayasası'nın halkoylamasıyla kabulü|1982|Anayasa
Eski siyasetçilerin siyasi yasaklarına ilişkin halkoylaması|1987|Seçimler
Cumhurbaşkanının halk tarafından seçilmesini öngören halkoylaması|2007|Anayasa
Bireysel başvuru hakkını getiren Anayasa değişikliği halkoylaması|2010|Anayasa
Anayasa Mahkemesine bireysel başvurunun uygulanmaya başlaması|2012|Yargı
Cumhurbaşkanının ilk kez halkoyuyla seçilmesi|2014|Seçimler
Cumhurbaşkanlığı Hükümet Sistemi'ni getiren halkoylaması|2017|Anayasa
Cumhurbaşkanlığı Hükümet Sistemi'nde ilk genel seçimlerin yapılması|2018|Seçimler
"""

OZELLIK = """
Anayasa|Türk tarihinin ilk anayasası hangisidir?|Kanun-i Esasi|Teşkilat-ı Esasiye Kanunu|1924 Anayasası|1961 Anayasası|Sened-i İttifak|1876 tarihli Kanun-i Esasi Türk tarihinin ilk anayasasıdır.
Anayasa|Yalnızca 23 maddeden oluşan ve meclis hükümeti sistemini benimseyen anayasa hangisidir?|1921 Teşkilat-ı Esasiye Kanunu|1876 Kanun-i Esasi|1924 Anayasası|1961 Anayasası|1982 Anayasası|1921 Anayasası 23 maddelik kısa bir metindir ve meclis hükümeti sistemini benimsemiştir.
Anayasa|Anayasa Mahkemesini ilk kez kuran anayasa hangisidir?|1961 Anayasası|1924 Anayasası|1982 Anayasası|1921 Teşkilat-ı Esasiye Kanunu|1876 Kanun-i Esasi|Anayasa Mahkemesi 1961 Anayasası ile kurulmuştur.
Anayasa|Millet Meclisi ve Cumhuriyet Senatosu'ndan oluşan iki meclisli yapıyı getiren Cumhuriyet dönemi anayasası hangisidir?|1961 Anayasası|1924 Anayasası|1982 Anayasası|1921 Teşkilat-ı Esasiye Kanunu|2017 Anayasa değişikliği|1961 Anayasası TBMM'yi Millet Meclisi ve Cumhuriyet Senatosu olarak iki kanatlı kurmuştur.
Anayasa|Sosyal devlet ilkesine ilk kez yer veren Türk anayasası hangisidir?|1961 Anayasası|1924 Anayasası|1876 Kanun-i Esasi|1921 Teşkilat-ı Esasiye Kanunu|1982 Anayasası|Sosyal devlet ilkesi ilk kez 1961 Anayasası'nda yer almıştır.
Anayasa|1876 Kanun-i Esasi'ye göre Meclis-i Umumi'nin üyeleri padişah tarafından atanan kanadı hangisidir?|Heyet-i Ayan|Meclis-i Mebusan|Divan-ı Hümayun|Meclis-i Vükela|Şura-yı Devlet|Heyet-i Ayan üyelerini padişah atardı; Meclis-i Mebusan seçimle oluşurdu.
Anayasa|Egemenliğin kayıtsız şartsız millete ait olduğunu ilk kez belirten Türk anayasası hangisidir?|1921 Teşkilat-ı Esasiye Kanunu|1876 Kanun-i Esasi|1961 Anayasası|1982 Anayasası|Sened-i İttifak|"Hâkimiyet bilakaydüşart milletindir" ilkesi ilk kez 1921 Anayasası'nda yer almıştır.
Anayasa|1982 Anayasası'nın değiştirilmesi teklif dahi edilemeyen maddeleri hangileridir?|İlk üç madde|İlk beş madde|İlk on madde|Başlangıç ve 1. madde|1. ve 2. maddeler|Anayasa'nın 4. maddesine göre ilk üç maddenin değiştirilmesi teklif edilemez.
İdare|İl özel idaresinin yürütme organının başı kimdir?|Vali|İl genel meclisi başkanı|Belediye başkanı|Kaymakam|İçişleri Bakanı|Vali il özel idaresinin başı ve yürütme organıdır.
İdare|İl encümenine kim başkanlık eder?|Vali|Belediye başkanı|İl genel meclisi başkanı|Kaymakam|İl jandarma komutanı|İl encümeninin başkanı validir.
İdare|Belediye encümenine kim başkanlık eder?|Belediye başkanı|Vali|Kaymakam|Muhtar|Belediye meclisinin en yaşlı üyesi|Belediye encümeninin başkanı belediye başkanıdır.
İdare|Belediye meclisine kim başkanlık eder?|Belediye başkanı|Vali|Kaymakam|Meclisin en genç üyesi|Encümenin en yaşlı üyesi|Belediye meclisinin başkanı belediye başkanıdır.
İdare|Köy ihtiyar meclisine kim başkanlık eder?|Muhtar|Kaymakam|Köy öğretmeni|Köy imamı|Köy derneğinin en yaşlı üyesi|İhtiyar meclisinin başkanı muhtardır.
İdare|İl idare kuruluna kim başkanlık eder?|Vali|Belediye başkanı|İl genel meclisi başkanı|Cumhuriyet başsavcısı|İl jandarma komutanı|İl idare kurulunun başkanı validir.
İdare|Köyün karar organı hangisidir?|Köy derneği|Muhtar|İhtiyar meclisi|Kaymakam|Köy encümeni|Köyün karar organı köydeki seçmenlerden oluşan köy derneğidir.
İdare|İl genel meclisinin başkanı nasıl belirlenir?|Meclis üyeleri arasından seçilir|Vali başkanlık eder|İçişleri Bakanı atar|Belediye başkanı başkanlık eder|Cumhurbaşkanı atar|İl genel meclisi başkanını üyeleri arasından seçer.
Anayasa|1982 Anayasası'na göre Türkiye Devleti'nin başkenti neresidir?|Ankara|İstanbul|İzmir|Bursa|Konya|Anayasa m.3'e göre başkent Ankara'dır.
Anayasa|1982 Anayasası'na göre Türkiye Devleti'nin dili hangisidir?|Türkçe|Türkçe ve İngilizce|Osmanlıca|Türkçe ve Arapça|Kanunla belirlenen diller|Anayasa m.3'e göre devletin dili Türkçedir.
Anayasa|1982 Anayasası'na göre millî marş hangisidir?|İstiklal Marşı|Onuncu Yıl Marşı|Harbiye Marşı|Cumhuriyet Marşı|Gençlik Marşı|Anayasa m.3'e göre millî marş İstiklal Marşı'dır.
Anayasa|1982 Anayasası'na göre egemenlik kime aittir?|Kayıtsız şartsız Millete|TBMM'ye|Cumhurbaşkanına|Yargı organlarına|Siyasi partilere|Anayasa m.6: Egemenlik kayıtsız şartsız Milletindir.
Anayasa|1982 Anayasası'na göre yasama yetkisi kime aittir ve devredilebilir mi?|TBMM'ye aittir, devredilemez|Cumhurbaşkanına aittir, devredilebilir|TBMM'ye aittir, Cumhurbaşkanına devredilebilir|Millete aittir, TBMM'ye devredilir|Bakanlar Kuruluna aittir, devredilemez|Anayasa m.7: Yasama yetkisi TBMM'nindir, bu yetki devredilemez.
Anayasa|1982 Anayasası'na göre yürütme yetkisi ve görevi kime aittir?|Cumhurbaşkanına|Bakanlar Kuruluna|TBMM Başkanına|Cumhurbaşkanı yardımcılarına|Başbakana|Anayasa m.8: Yürütme yetkisi ve görevi Cumhurbaşkanı tarafından kullanılır ve yerine getirilir.
Anayasa|1982 Anayasası'na göre yargı yetkisi kim tarafından kullanılır?|Bağımsız ve tarafsız mahkemeler|Cumhurbaşkanı|TBMM|Adalet Bakanlığı|Hâkimler ve Savcılar Kurulu|Anayasa m.9: Yargı yetkisi Türk Milleti adına bağımsız ve tarafsız mahkemelerce kullanılır.
Yargı|Siyasi partilerin kapatılması davasını kim açar?|Yargıtay Cumhuriyet Başsavcısı|Adalet Bakanı|TBMM Başkanı|Anayasa Mahkemesi Başkanı|Yüksek Seçim Kurulu|Kapatma davası Yargıtay Cumhuriyet Başsavcısınca Anayasa Mahkemesinde açılır.
Yargı|Yüce Divan'da yargılanan Cumhurbaşkanı yardımcıları ve bakanların davası en geç ne kadar sürede sonuçlandırılır?|3 ay, gerekirse 3 ay uzatma|1 yıl|6 ay, uzatma yapılamaz|2 ay|1 ay, gerekirse 1 ay uzatma|Yüce Divan yargılamayı üç ay içinde bitirir; bitmezse bir defaya mahsus üç ay ek süre verilir.
"""


def _satir(blok, n):
    out = []
    for l in blok.strip().splitlines():
        if l.strip():
            p = [x.strip() for x in l.split('|')]
            assert len(p) == n, l
            out.append(p)
    return out


# Yetki sorularında birbiriyle karıştırılan organ ve kurumlar (çeldirici önceliği)
KARISAN = {
    'TBMM': ['Cumhurbaşkanı', 'Anayasa Mahkemesi', 'Sayıştay', 'Yüksek Seçim Kurulu'],
    'Cumhurbaşkanı': ['TBMM', 'Millî Güvenlik Kurulu', 'Hâkimler ve Savcılar Kurulu', 'Anayasa Mahkemesi'],
    'Anayasa Mahkemesi': ['Yargıtay', 'Danıştay', 'Uyuşmazlık Mahkemesi', 'Hâkimler ve Savcılar Kurulu'],
    'Hâkimler ve Savcılar Kurulu': ['Anayasa Mahkemesi', 'Yargıtay', 'Danıştay', 'Cumhurbaşkanı'],
    'Yargıtay': ['Danıştay', 'Anayasa Mahkemesi', 'Uyuşmazlık Mahkemesi', 'Sayıştay'],
    'Danıştay': ['Yargıtay', 'Sayıştay', 'Anayasa Mahkemesi', 'Uyuşmazlık Mahkemesi'],
    'Sayıştay': ['Danıştay', 'TBMM', 'Yargıtay', 'Kamu Denetçiliği Kurumu'],
    'Uyuşmazlık Mahkemesi': ['Anayasa Mahkemesi', 'Yargıtay', 'Danıştay', 'Hâkimler ve Savcılar Kurulu'],
    'Yüksek Seçim Kurulu': ['Anayasa Mahkemesi', 'TBMM', 'Yargıtay', 'Danıştay'],
    'Kamu Denetçiliği Kurumu': ['Sayıştay', 'Danıştay', 'TBMM', 'Anayasa Mahkemesi'],
    'Millî Güvenlik Kurulu': ['Cumhurbaşkanı', 'TBMM', 'Danıştay', 'Yüksek Seçim Kurulu'],
}


def uret(rng):
    out = []
    md = [(int(a), b, c) for a, b, c in _satir(MADDELER, 3)]
    nos = [m[0] for m in md]
    for n, k, f in md:
        yakin = sorted(md, key=lambda m: abs(m[0] - n))[1:12]
        out.append(q('madde_konu', 'Anayasa', f'1982 Anayasası\'nın {n}. maddesi aşağıdaki konulardan hangisini düzenler?', k,
                     sec2(k, [m[1] for m in yakin], [m[1] for m in md], rng), f'Anayasa m.{n}: {k}.', 3))
        ny = [str(m[0]) for m in yakin]
        out.append(q('konu_madde', 'Anayasa', f'1982 Anayasası\'nda “{k}” kaçıncı maddede düzenlenmiştir?', f'{n}. madde',
                     sec(f'{n}. madde', [f'{x}. madde' for x in ny], rng), f'“{k}” Anayasa\'nın {n}. maddesindedir.', 3))
        ks = kisim(n)
        out.append(q('kisim', 'Anayasa', f'1982 Anayasası\'nda “{k}” hangi kısımda yer alır?', ks,
                     sec(ks, KISIMLAR, rng), f'“{k}” (m.{n}) {ks} kısmındadır.', 2))
        hb = hak_bolum(n)
        if hb:
            secenek = ['Genel Hükümler', 'Kişinin Hakları ve Ödevleri', 'Sosyal ve Ekonomik Haklar ve Ödevler', 'Siyasi Haklar ve Ödevler', 'Cumhuriyetin Temel Organları']
            out.append(q('hak_bolum', 'Haklar', f'“{k}” 1982 Anayasası\'nın Temel Haklar ve Ödevler kısmında hangi bölümde düzenlenmiştir?', hb,
                         sec(hb, secenek, rng), f'“{k}” (m.{n}) {hb} bölümündedir.', 3))
            ayni = [m for m in md if hak_bolum(m[0]) == hb and m[0] != n and hb != 'Genel Hükümler']
            diger = [m[1] for m in md if hak_bolum(m[0]) and hak_bolum(m[0]) not in (hb, 'Genel Hükümler')]
            if ayni:
                d = rng.choice(ayni)
                out.append(q('ayni_bolum', 'Haklar', f'Aşağıdakilerden hangisi 1982 Anayasası\'nda “{k}” ile aynı bölümde düzenlenmiştir?', d[1],
                             sec(d[1], diger, rng), f'“{k}” ve “{d[1]}” {hb} bölümündedir.', 3))
            if f != '!' and hb in STATU:
                st = STATU[hb]
                out.append(q('statu', 'Haklar', f'Statü teorisine göre “{k}” hangi grupta yer alır?', st,
                             [v for v in STATU.values() if v != st] + ['Ödevler', 'Sınırlanamayan haklar'][:2],
                             f'“{k}” {hb} arasında olduğundan {st} içindedir.', 3))
        ayni_k = [m for m in md if kisim(m[0]) == ks and m[0] != n]
        diger_k = [m[1] for m in md if kisim(m[0]) != ks]
        if ayni_k:
            d = rng.choice(ayni_k)
            out.append(q('ayni_kisim', 'Anayasa', f'Aşağıdakilerden hangisi 1982 Anayasası\'nda “{k}” ile aynı kısımda yer alır?', d[1],
                         sec(d[1], diger_k, rng), f'“{k}” ve “{d[1]}” {ks} kısmındadır.', 3))
        og = organ(n)
        if og:
            out.append(q('organ', {'Yasama': 'TBMM', 'Yürütme': 'Yürütme', 'Yargı': 'Yargı'}[og],
                         f'“{k}” 1982 Anayasası\'nın Cumhuriyetin Temel Organları kısmında hangi bölümdedir?', og,
                         [x for x in ['Yasama', 'Yürütme', 'Yargı', 'Genel Esaslar', 'Mali ve Ekonomik Hükümler'] if x != og],
                         f'“{k}” (m.{n}) {og} bölümündedir.', 2))
    kav = [(a, d, k) for a, d, k, _ in _satir(KAVRAMLAR, 4)]
    out += eslesme(rng, 'kavram', kav,
                   lambda a, d: f'“{a}” kavramı aşağıdakilerden hangisini ifade eder?',
                   lambda a, d: f'“{d}” aşağıdaki kavramlardan hangisiyle ifade edilir?',
                   lambda a, d: f'{a}: {d}.', lambda a, d: f'{d} = {a}.', 3, grup=lambda a, d, k: k)
    dallar = ['Medeni hukuk', 'Borçlar hukuku', 'Ticaret hukuku', 'Ceza hukuku', 'İdare hukuku', 'Anayasa hukuku', 'Ceza muhakemesi hukuku', 'İş hukuku', 'Vergi hukuku']
    for a, d, k, dal in _satir(KAVRAMLAR, 4):
        if dal != '-':
            out.append(q('dal', k, f'“{a}” kavramı öncelikle hangi hukuk dalının konusudur?', dal, sec(dal, dallar, rng),
                         f'{a} ({d.lower()[:60]}…) {dal} ile ilgilidir.', 2))
    yet = _satir(YETKILER, 2)
    sahip = sorted({x[1] for x in yet}) + ['Milletvekilleri', 'Vali']
    for y, s in yet:
        konu = {'TBMM': 'TBMM', 'Cumhurbaşkanı': 'Yürütme', 'Belediye meclisi': 'İdare', 'Millî Güvenlik Kurulu': 'Yürütme',
                'Diyanet İşleri Başkanlığı': 'İdare', 'Yükseköğretim Kurulu': 'İdare', 'Radyo ve Televizyon Üst Kurulu': 'İdare',
                'Kamu Denetçiliği Kurumu': 'İdare', 'Yüksek Seçim Kurulu': 'Seçimler'}.get(s, 'Yargı')
        yakin = KARISAN.get(s, [])
        out.append(q('yetki', konu, f'1982 Anayasası’na göre “{y}” görev veya yetkisi aşağıdakilerden hangisine aittir?', s,
                     sec2(s, yakin, sahip, rng),
                     f'{y}: {s}. Seçeneklerdeki diğer organ ve kurumlar bu yetkiyle sık karıştırılır.', 3))
    for k, soru, d, a, b, c, e, g in _satir(SAYISAL, 8):
        out.append(q('sayisal', k, soru, d, [a, b, c, e], g, 3))
    for k, soru, d, a, b, c, e, g in _satir(OZELLIK, 8):
        out.append(q('ozellik', k, soru, d, [a, b, c, e], g, 3))
    for x, kit in _satir(TMK, 2):
        out.append(q('tmk', 'Hukuk', f'“{x}” Türk Medeni Kanunu\'nun hangi kitabında düzenlenmiştir?', kit,
                     [v for v in TMK_SECENEK if v != kit], f'{x}, Türk Medeni Kanunu\'nun {kit} kitabındadır.', 2))
    for x in KAMU + OZEL:
        ayni, diger = (KAMU, OZEL) if x in KAMU else (OZEL, KAMU)
        ana = 'kamu hukuku' if x in KAMU else 'özel hukuk'
        d = rng.choice([y for y in ayni if y != x])
        out.append(q('ana_dal', 'Hukuk', f'Aşağıdaki hukuk dallarından hangisi {x} ile aynı ana dala (kamu hukuku / özel hukuk) girer?', d,
                     sec(d, diger, rng), f'{x} ve {d} {ana} dalındadır; diğerleri öbür ana daldadır.', 3))
    bel = _satir(BELGELER, 3)
    for b, y, u in bel:
        yy = [x[1] for x in bel if x[1] != y] + [str(int(y) + d) for d in (-3, 3, 10, -10)]
        out.append(q('belge_yil', 'İnsan Hakları', f'{b} hangi yılda kabul edilmiştir?', y, sec(y, yy, rng), f'{b}: {y} ({u}).', 3))
        out.append(q('belge_yer', 'İnsan Hakları', f'{b} hangi ülke ya da uluslararası kuruluş bünyesinde ortaya çıkmıştır?', u,
                     sec(u, [x[2] for x in bel] + ['Almanya', 'İtalya'], rng), f'{b} ({y}): {u}.', 2))
    tc = _satir(TARIHCE, 3)
    for o, y, k in tc:
        yy = [x[1] for x in tc if x[1] != y and abs(int(x[1]) - int(y)) <= 40]
        out.append(q('tarihce', k, f'“{o}” hangi yılda gerçekleşmiştir?', y, sec(y, yy, rng), f'{o}: {y}.', 3))
        h = [x[0] for x in tc if x[1] != y]
        rng.shuffle(h)
        out.append(q('tarihce_ters', k, f'{y} yılında Türk anayasa ve seçim tarihinde aşağıdakilerden hangisi gerçekleşmiştir?', o,
                     sec(o, h, rng), f'{y}: {o}.', 3))
    sahip_yet = {}
    for y, s_ in yet:
        sahip_yet.setdefault(s_, []).append(y)
    for sh, ys in sahip_yet.items():
        if len(ys) < 4:
            continue
        dis = [(y, f'“{y}” ise {s_} yetkisidir.') for y, s_ in yet if s_ in KARISAN.get(sh, [])]
        for kok in (f'1982 Anayasası’na göre aşağıdakilerden hangisi {sh} görev ve yetkilerinden biri değildir?',
                    f'Aşağıdakilerden hangisi 1982 Anayasası’na göre {sh} tarafından kullanılan yetkilerden biri değildir?',
                    f'1982 Anayasası’nda {sh} için sayılan görev ve yetkiler arasında aşağıdakilerden hangisi yer almaz?'):
            out.append(farkli(rng, 'yetki_degil', konu_of(sh), kok, [(y, '') for y in ys], dis,
                              lambda m, a, ic, sh=sh: f'{a} Diğer seçenekler {sh} yetkileridir.'))
    for hb in ('Kişinin Hakları ve Ödevleri', 'Sosyal ve Ekonomik Haklar ve Ödevler', 'Siyasi Haklar ve Ödevler'):
        ic = [(k, '') for n, k, f in md if hak_bolum(n) == hb]
        dis = [(k, f'“{k}” (m.{n}) {hak_bolum(n)} bölümündedir.') for n, k, f in md
               if hak_bolum(n) and hak_bolum(n) not in (hb, 'Genel Hükümler')]
        for kok in (f'Aşağıdakilerden hangisi 1982 Anayasası’nda “{hb}” bölümünde düzenlenmemiştir?',
                    f'1982 Anayasası’na göre aşağıdakilerden hangisi “{hb}” arasında yer almaz?',
                    f'Aşağıdakilerden hangisi 1982 Anayasası’nın “{hb}” bölümünde yer alan hak ve ödevlerden biri değildir?'):
            out.append(farkli(rng, 'bolum_degil', 'Haklar', kok, ic, dis,
                              lambda m, a, ic_, hb=hb: f'{a} Diğer seçenekler {hb} bölümündedir.'))
    out += akil_yurutme(rng, md, kav, yet, bel, tc)
    return out


def konu_of(sahip):
    return {'TBMM': 'TBMM', 'Cumhurbaşkanı': 'Yürütme'}.get(sahip, 'Yargı')


# Madde numarası ezberi KPSS'de seyrek sorulur; bu türler sınırlı tutulur.
KOTA = {'madde_konu': 60, 'konu_madde': 45}

AGIRLIK = {'oncul_yetki': 3, 'oncul_bolum': 2, 'oncul_hukuk': 2, 'sirala_tarihce': 2, 'oncul_madde': 2,
           'oncul_belge': 2, 'oncul_kavram': 2, 'esle_madde': 2}


def akil_yurutme(rng, md, kav, yet, bel, tc):
    """Seçenekleri birbirine yakın, tek cevaplı akıl yürütme soruları."""
    out = []
    # 1) Görev ve yetkiler: TBMM / Cumhurbaşkanı / AYM / HSK karışık
    sahipler = ['TBMM', 'Cumhurbaşkanı', 'Anayasa Mahkemesi', 'Hâkimler ve Savcılar Kurulu']
    konu = {'TBMM': 'TBMM', 'Cumhurbaşkanı': 'Yürütme', 'Anayasa Mahkemesi': 'Yargı', 'Hâkimler ve Savcılar Kurulu': 'Yargı'}
    for _ in range(260):
        sh = rng.choice(sahipler)
        d = [(y, f'“{y}” {sh} yetkisidir.') for y, s_ in yet if s_ == sh]
        w = [(y, f'“{y}” {sh} yetkisi değildir; {s_} yetkisidir.') for y, s_ in yet if s_ != sh and s_ in sahipler]
        out.append(onculu(rng, 'oncul_yetki', konu[sh], d, w,
                          f'1982 Anayasası’na göre yukarıdaki görev ve yetkilerden hangileri {sh} tarafından kullanılır?', 3))
    # 2) Hak ve ödevler: aynı bölüm mü? (Kişi / Sosyal-Ekonomik / Siyasi)
    bolumler = ['Kişinin Hakları ve Ödevleri', 'Sosyal ve Ekonomik Haklar ve Ödevler', 'Siyasi Haklar ve Ödevler']
    for _ in range(300):
        hb = rng.choice(bolumler)
        d = [(k, f'“{k}” (m.{n}) {hb} bölümündedir.') for n, k, f in md if hak_bolum(n) == hb]
        w = [(k, f'“{k}” (m.{n}) {hak_bolum(n)} bölümündedir.') for n, k, f in md if hak_bolum(n) in bolumler and hak_bolum(n) != hb]
        out.append(onculu(rng, 'oncul_bolum', 'Haklar', d, w,
                          f'Yukarıdakilerden hangileri 1982 Anayasası’nda “{hb}” bölümünde düzenlenmiştir?', 3))
    # 3) Kamu hukuku / özel hukuk
    for _ in range(80):
        ana, ayni, diger = rng.choice([('kamu hukuku', KAMU, OZEL), ('özel hukuk', OZEL, KAMU)])
        ters = 'özel hukuk' if ana == 'kamu hukuku' else 'kamu hukuku'
        out.append(onculu(rng, 'oncul_hukuk', 'Hukuk', [(x, f'{x} {ana} dalıdır.') for x in ayni],
                          [(x, f'{x} {ters} dalıdır.') for x in diger],
                          f'Yukarıdaki hukuk dallarından hangileri {ana} içinde yer alır?', 3))
    # 4) Anayasa ve seçim tarihçesi: kronolojik sıralama
    for _ in range(400):
        n = rng.choice([3, 3, 4])
        sec_ = rng.sample(tc, n)
        if len({x[1] for x in sec_}) != n:
            continue
        out.append(siralama(rng, 'sirala_tarihce', sec_[0][2], [(int(y), o) for o, y, k in sec_],
                            'Yukarıdaki gelişmelerin gerçekleşme sırası (eskiden yeniye) aşağıdakilerden hangisidir?',
                            lambda o: 'Yıllar: ' + '; '.join(f'{m} {k}' for k, m in o) + '.', 3))
    # 5) Madde – konu: yanlış eşleştirmeler komşu maddelerin konusuyla
    konu_n = {n: k for n, k, f in md}
    for _ in range(320):
        uc = rng.sample(md, 3)
        if len({kisim(n) for n, _, _ in uc}) == 1 and rng.random() < 0.5:
            continue
        k_ = rng.choice([1, 2, 2, 3])
        d = [(f'{n}. madde – {k}', f'Anayasa m.{n}: {k}.') for n, k, f in uc[:k_]]
        w = []
        for n, k, f in uc[k_:]:
            yakin = [m for m in konu_n if m != n and abs(m - n) <= 4 and konu_n[m] != k]
            if not yakin:
                break
            m = rng.choice(yakin)
            w.append((f'{n}. madde – {konu_n[m]}', f'“{konu_n[m]}” {n}. maddede değil {m}. maddededir; m.{n}: {k}.'))
        else:
            out.append(onculu(rng, 'oncul_madde', 'Anayasa', d, w,
                              '1982 Anayasası’na ilişkin yukarıdaki madde – konu eşleştirmelerinden hangileri doğrudur?', 3, k_))
    for _ in range(120):
        a = rng.choice(md)
        yakin = [x for x in md if abs(x[0] - a[0]) <= 12]
        if len(yakin) < 5:
            continue
        bes = rng.sample(yakin, 5)
        out.append(eslestirme(rng, 'esle_madde', 'Anayasa', [(f'{n}. madde', k) for n, k, f in sorted(bes)],
                              lambda x, w: konu_n[int(x.split('.')[0])] == w, 'dogru',
                              lambda ks: '1982 Anayasası’nın ' + ', '.join(k.split()[0] for k in ks[:-1]) + f' ve {ks[-1].split()[0]} maddeleriyle ilgili aşağıdaki madde – konu eşleştirmelerinden hangisi doğrudur?'))
    # 6) Belge – yıl (yanlış yıllar doğrusuna yakın)
    for _ in range(90):
        uc = rng.sample(bel, 3)
        k_ = rng.choice([1, 2, 2, 3])
        d = [(f'{b} – {y}', f'{b} {y} yılında kabul edilmiştir.') for b, y, u in uc[:k_]]
        w = [(f'{b} – {int(y) + dd}', f'{b} {int(y) + dd} değil {y} yılında kabul edilmiştir.')
             for (b, y, u), dd in zip(uc[k_:], rng.sample([-3, -2, -1, 1, 2, 3], 3))]
        out.append(onculu(rng, 'oncul_belge', 'İnsan Hakları', d, w,
                          'Yukarıdaki belge – kabul yılı eşleştirmelerinden hangileri doğrudur?', 3, k_))
    # 7) Kavram – açıklama
    kav_konu = {}
    for x in kav:
        kav_konu.setdefault(x[2], []).append(x)
    for _ in range(300):
        uc = rng.sample(rng.choice([v for v in kav_konu.values() if len(v) >= 4]), 3)
        k_ = rng.choice([1, 2, 2, 3])
        d = [(f'{a}: {t}', f'{a}: {t}.') for a, t, k in uc[:k_]]
        w = []
        gosterilen = {x[1] for x in uc}
        for a, t, k in uc[k_:]:
            b = rng.choice([x for x in kav if x[0] != a and x[2] == k and x[1] not in gosterilen] or [x for x in kav if x[0] != a and x[1] not in gosterilen])
            w.append((f'{a}: {b[1]}', f'Bu açıklama {a} kavramına değil {b[0]} kavramına aittir.'))
        out.append(onculu(rng, 'oncul_kavram', uc[0][2], d, w,
                          'Yukarıdaki kavram – açıklama eşleştirmelerinden hangileri doğrudur?', 3, k_))
    return out
