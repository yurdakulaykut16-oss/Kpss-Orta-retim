#!/usr/bin/env python3
"""Etiketi kısa ad (slug) olan 24 aktif konu için eksik anlatım kartlarını ekler.

Bu konuların soruları vardı ama data/konu_yeniden.json içinde kartları yoktu;
yanlış cevapta konu tekrar anlatılamıyordu. Var olan kartlar değiştirilmez.
"""
import json
from pathlib import Path

YOL = Path(__file__).resolve().parent.parent / 'data' / 'konu_yeniden.json'

KARTLAR = {
 "tarih|tanzimat": {
  "ozet": "Tanzimat Fermanı (3 Kasım 1839, Abdülmecit dönemi, Mustafa Reşid Paşa): can-mal-namus güvenliği, vergide adalet, düzenli askerlik, yargılamasız ceza verilmemesi. Padişah kendi yetkisini ilk kez sınırlamayı kabul etti. Islahat Fermanı (1856): gayrimüslimlere eşitlik ve yeni haklar; Paris Antlaşması öncesinde Avrupa baskısıyla. Sened-i İttifak (1808) ise padişahla âyanlar arasındaki ilk yetki sınırlama belgesidir. I. Meşrutiyet ve Kanun-i Esasi: 1876.",
  "hikaye": "Bir apartman düşün: 1808'de yönetici (padişah) güçlü komşularla (âyan) bir sözleşme imzaladı. 1839'da tüm kiracılara 'canınız, malınız, namusunuz güvende' diye yazılı söz verdi. 1856'da 'hangi dinden olursanız olun eşitsiniz' dedi. 1876'da ise apartmana bir yönetim kurulu (Meclis-i Mebusan) ve yazılı tüzük (Kanun-i Esasi) geldi.",
  "tuzak": "Tuzak: 'Hukuk devleti yolunda ilk adım' Tanzimat'tır ama 'ilk anayasa' Kanun-i Esasi'dir (1876). 'Gayrimüslimlere geniş haklar' Islahat Fermanı'dır (1856), Tanzimat değil. Tanzimat halkın isteğiyle değil, yukarıdan (devlet eliyle) ve dış destek sağlama amacıyla ilan edildi.",
  "nasil_sorulur": "Sınavda: belge-yıl-içerik eşleştirmesi (1808-1839-1856-1876), 'padişahın yetkisini sınırlayan ilk belge', Tanzimat'ın amaçları ve sonuçları I-II-III öncülleriyle sorulur. Önce belgenin kime yönelik olduğunu (âyan, tüm halk, gayrimüslim, meclis) belirle."
 },
 "cografya|tarim_hayvancilik": {
  "ozet": "Tarımı iklim (sıcaklık, yağış), yer şekilleri (eğim, yükselti), toprak ve sulama belirler. Çay ve fındık Karadeniz'in nemli ılıman ikliminde; pamuk Çukurova, Ege ve GAP'ta (sıcaklık + sulama); zeytin Akdeniz ikliminde (Ege, Akdeniz, Güney Marmara); buğday ve arpa İç Anadolu'da (kuru tarım); şeker pancarı İç Anadolu ve Trakya'da yetişir. Büyükbaş besi Karadeniz ve Marmara'da; büyükbaş mera hayvancılığı Doğu Anadolu'da (Erzurum-Kars); küçükbaş (koyun) İç Anadolu'da; kıl keçisi Akdeniz-Toroslarda yaygındır.",
  "hikaye": "Her ürün 'evini' seçen bir kiracıdır: çay yağmursever, sadece Rize-Artvin gibi her mevsim yağış alan yere taşınır. Pamuk güneşsever ama susuz kalamaz; sulama kanalı olan sıcak ovaları sever. Koyun bozkırın kısa otlarıyla, inek ise Doğu Anadolu'nun yaz yağışlı gür çayırlarıyla yetinir.",
  "tuzak": "Tuzak: 'Verim artışı' (makine, gübre, sulama, tohum ıslahı) ile 'üretim artışı' (ekim alanı genişlemesi de olabilir) aynı şey değildir. Doğu Anadolu'da büyükbaş, İç Anadolu'da küçükbaş öne çıkar; karıştırılır. Nadas kuru tarım alanlarında toprağın nemini korumak içindir.",
  "nasil_sorulur": "Sınavda: ürün-bölge eşleştirmesi, ürünün yetişmesini sağlayan koşul (iklim mi, sulama mı, toprak mı), hayvancılık türü-bölge ve verimi artıran faktörler sorulur. Ürünün 'neden orada' yetiştiğini iklim + yer şekli ile açıkla."
 },
 "cografya|sanayi": {
  "ozet": "Sanayi tesisinin yerini ham madde, enerji, ulaşım, pazar, iş gücü ve sermaye belirler. Ham maddesi çabuk bozulan veya ağırlık kaybeden ürünlerin fabrikası ham maddeye yakın kurulur (şeker fabrikası pancar tarlasına, çay fabrikası Rize'ye, çimento kireç taşına yakın). Marmara (özellikle İstanbul-Kocaeli-Bursa) sanayinin merkezidir: pazar, liman, sermaye ve nitelikli iş gücü bir aradadır. Demir-çelik: Karabük, Ereğli (Zonguldak), İskenderun.",
  "hikaye": "Fabrika kuracak bir girişimci listesine bakar: Ham madde nerede? Enerji var mı? Mal kime satılacak? İşçi bulunur mu? Liman yakın mı? Marmara listenin hemen her maddesine 'evet' dediği için fabrikalar oraya toplanır. Şeker pancarı ise yolda bekleyince şekeri azaldığından fabrika tarlanın yanına gelir.",
  "tuzak": "Tuzak: Her fabrikanın yerini ham madde belirlemez; Marmara'daki çoğu sanayinin asıl nedeni pazar, ulaşım ve sermayedir. 'Organize sanayi bölgesi' (altyapısı hazır sanayi alanı) ile 'serbest bölge' (gümrük ve vergi kolaylığı olan alan) karıştırılır.",
  "nasil_sorulur": "Sınavda: bir tesisin kuruluş yerinde etkili olan faktör (ham madde, enerji, pazar), sanayi kolu-şehir eşleştirmesi ve sanayinin çevreye etkileri I-II-III öncülleriyle sorulur. Ürünün bozulabilirliği ve taşıma maliyeti ipucudur."
 },
 "cografya|ulasim": {
  "ozet": "Türkiye'de ulaşımı en çok yer şekilleri etkiler: Karadeniz ve Akdeniz'de dağlar kıyıya paralel uzandığı için kıyı-iç kesim bağlantısı zordur, yollar vadi ve geçitleri izler. Ege'de dağlar kıyıya dik uzanır; doğu-batı yönlü grabenler (Gediz, Büyük Menderes) iç kesimle bağlantıyı kolaylaştırır. Kara yolu yolcu ve yükte en çok kullanılan yoldur. Deniz yolu ağır ve hacimli yükte en ucuzdur; hava yolu en hızlı ama en pahalıdır; boru hatları petrol ve doğal gaz taşır. Kışın kar ve sis ulaşımı aksatır.",
  "hikaye": "Ulaşım suyun yolunu izler: Ege'de dağlar kapı gibi denize açıldığı için vadiler iç Anadolu'ya giden geniş koridorlardır. Karadeniz'de ise dağlar kıyıya duvar örmüştür; yol ancak bu duvardaki yarıklardan (vadi, geçit) geçebilir. Ağır demir cevherini gemiye, acil kalp ilacını uçağa, doğal gazı boruya verirsin.",
  "tuzak": "Tuzak: 'Dağların uzanışı kıyıya paralel' ile 'kıyıya dik' karıştırılır; paralel olan Karadeniz-Akdeniz, dik olan Ege'dir. Hava yolu en ucuz değil en hızlıdır. Boru hatları yolcu taşımaz. Ege vadileri bağlantıyı engellemez, kolaylaştırır.",
  "nasil_sorulur": "Sınavda: yer şekli-ulaşım ilişkisi, ulaşım türlerinin üstün ve zayıf yanları, iklimin ulaşıma etkisi I-II-III öncülleriyle sorulur. 'Her zaman, yalnız, bütünüyle' gibi kesin ifadeler genellikle yanlış öncülün işaretidir."
 },
 "cografya|cevre": {
  "ozet": "Çevre sorunları: hava kirliliği (fosil yakıt, sanayi, trafik; sıcaklık terselmesi ve rüzgârsız hava kirliliği artırır), su kirliliği (sanayi ve evsel atık, tarım ilaçları), toprak kaybı (erozyon: eğim, bitki örtüsünün yok edilmesi, sağanak yağış, yanlış tarım), orman tahribi ve küresel iklim değişikliği. Korunan alanlar: milli park, tabiat parkı, tabiatı koruma alanı, yaban hayatı geliştirme sahası. Yenilenebilir enerji (güneş, rüzgâr, hidroelektrik, jeotermal) çevre baskısını azaltır.",
  "hikaye": "Doğa bir banka hesabıdır: orman, toprak ve su 'ana para'dır, insan faizi kullanırsa hesap büyür; ana paraya dokunursa (ormanı kesip eğimli yamacı sürerse) sel ve erozyon gelir, borç geri dönmez. Toprak birkaç santimi yüzyıllarda oluşur ama bir sağanakta gidebilir.",
  "tuzak": "Tuzak: Erozyonu eğim, seyrek bitki örtüsü ve sağanak artırır; 'bitki örtüsü sık olan düz alanda erozyon fazladır' yanlıştır. Sera etkisi doğal bir süreçtir; sorun sera gazlarının artmasıdır. Milli park ile tabiat parkı aynı statü değildir.",
  "nasil_sorulur": "Sınavda: bir çevre sorununun nedeni veya sonucu, erozyonu artıran/azaltan etkenler, sürdürülebilir kullanım örnekleri ve korunan alan türleri sorulur. Neden-sonuç zincirini kur: insan etkisi → doğal denge → sonuç."
 },
 "cografya|dis_ticaret": {
  "ozet": "Dış ticaret: ihracat (yurt dışına satış) ve ithalat (yurt dışından alım). İthalat ihracattan fazlaysa dış ticaret açığı oluşur. İhracatın ithalatı karşılama oranı = (ihracat ÷ ithalat) × 100. Türkiye ihracatında sanayi ürünleri (otomotiv, tekstil-hazır giyim, demir-çelik, makine, elektrikli eşya) öne çıkar; ithalatta enerji (petrol, doğal gaz), ara malı ve makine önemli yer tutar. Ham maddeyi işleyerek satmak katma değeri artırır. Turizm gelirleri hizmet ihracatı sayılır.",
  "hikaye": "Ülkeni bir ev bütçesi gibi düşün: dışarı ürün satınca para girer (ihracat), dışarıdan alınca para çıkar (ithalat). Fındığı ham satarsan az, çikolata yapıp satarsan çok kazanırsın; işte katma değer. Yabancı turist otelinde kaldığında da ülkeye döviz girer; bu yüzden turizm de bir tür 'satış'tır.",
  "tuzak": "Tuzak: Karşılama oranı ihracat/ithalat'tır; 80 ihracat ve 100 ithalatta oran %80'dir, %125 değil. İhracatın artması tek başına açığın kapandığını göstermez; ithalat daha hızlı artmış olabilir. Bir ürün hem ithal hem ihraç edilebilir (çeşit, kalite, mevsim farkı).",
  "nasil_sorulur": "Sınavda: oran hesabı, ihracat-ithalat ürün grupları, katma değer ve hizmet ihracatı kavramları I-II-III veya beş yargılı sorularla ölçülür. Sayısal yargıda formülü yaz, sonra yerine koy."
 },
 "cografya|yeryuzu_sekilleri": {
  "ozet": "Türkiye'nin ortalama yükseltisi fazladır (yaklaşık 1100 m) ve yükselti genel olarak batıdan doğuya artar. Kuzeyde Kuzey Anadolu Dağları ve güneyde Toroslar kıvrımla oluşmuş, kıyıya paralel uzanır. Ege'de horst-graben yapısı vardır; dağlar kıyıya dik uzanır, grabenlerde verimli ovalar oluşur (Gediz, Büyük Menderes). Volkanik dağlar: Ağrı, Erciyes, Hasan, Nemrut, Süphan. Karstik şekiller (mağara, polye, traverten) kalkerli arazide, özellikle Akdeniz Bölgesi'nde yaygındır. Kıyı tipleri: boyuna (Karadeniz, Akdeniz), enine (Ege), ria (İstanbul ve Çanakkale boğazları), dalmaçya (Antalya batısı), limanlı (Ege).",
  "hikaye": "Anadolu'yu bir kumaş gibi düşün: kuzeyden ve güneyden itilince kenarları kıvrılıp yükseldi (Kuzey Anadolu Dağları, Toroslar). Batıda ise kumaş gerildi ve yırtıldı: yükselen parçalar horst, çöken parçalar graben oldu. Yırtıklardan magma sızınca volkan dağları doğdu; kireçli taşları su yavaş yavaş eritince mağaralar açıldı.",
  "tuzak": "Tuzak: Ege'de dağlar kıyıya diktir, Karadeniz ve Akdeniz'de paraleldir. Ria kıyı akarsu vadilerinin sular altında kalmasıyla, dalmaçya kıyı kıyıya paralel dağ sıralarının sular altında kalmasıyla oluşur. Karstik şekiller her yerde değil kalkerli (kireç taşı) arazide oluşur.",
  "nasil_sorulur": "Sınavda: yer şekli-oluşum (iç kuvvet/dış kuvvet) eşleştirmesi, kıyı tipi-yer, dağların uzanışının iklime ve ulaşıma etkisi, volkanik ve karstik şekil örnekleri sorulur. Önce şeklin hangi kuvvetle oluştuğunu belirle."
 },
 "cografya|iklim_bitki_orfu": {
  "ozet": "Türkiye'de üç ana iklim vardır: Karadeniz iklimi (her mevsim yağışlı, yazlar serin; bitki örtüsü orman), Akdeniz iklimi (yazlar sıcak ve kurak, kışlar ılık ve yağışlı; maki), karasal iklim (yazlar sıcak-kurak, kışlar soğuk-karlı; bozkır). Doğu Anadolu'da kışlar çok sert geçer, yaz yağışlarıyla gür çayırlar oluşur. Yağış türleri: orografik (yamaç; Karadeniz, Akdeniz), konveksiyonel (yerel ısınma; İç Anadolu'da ilkbahar kırkikindileri), cephesel (Marmara, Akdeniz kışları). Maki, kızılçam ormanı tahrip edildiğinde oluşan kuraklığa dayanıklı çalı topluluğudur.",
  "hikaye": "Üç komşu düşün: Karadenizli her gün şemsiyeyle çıkar ve bahçesi orman gibidir. Akdenizli yaz boyunca güneşte kurur, kışın ılık yağmurla rahatlar; bahçesinde sert yapraklı makiler vardır. İç Anadolulu ise yazın kavrulur, kışın üşür; bahçesi yaz başında yeşerip sonra sararan bozkırdır.",
  "tuzak": "Tuzak: Bozkır kuraklıktan dolayı oluşur, sıcaklıktan değil; 'yaz kuraklığı' bozkır ve makide ortak etkendir. Karadeniz'de en çok yağış kıyıda, özellikle doğu kesimde (Rize) düşer. Doğu Anadolu çayırları yaz yağışlarına bağlıdır. 'Muson' Türkiye'nin temel iklim tipi değildir.",
  "nasil_sorulur": "Sınavda: iklim-bitki örtüsü eşleştirmesi, sıcaklık-yağış grafiğinden iklim tipini bulma, yağış türünün oluşum nedeni ve iklimin tarım, yerleşme, turizme etkisi sorulur. Grafikte önce yaz kuraklığına ve kış sıcaklığına bak."
 },
 "cografya|nufus_yerlesme": {
  "ozet": "Türkiye'de nüfus kıyılarda, sanayi ve ticaret merkezlerinde, verimli ovalarda yoğundur (Marmara, Ege kıyıları, Çukurova). Seyrek alanlar: yükseltisi fazla ve engebeli yerler (Doğu Anadolu'nun yüksek kesimleri, Toroslar), kurak alanlar (Tuz Gölü çevresi), sert iklimli yerler. Türkiye'de kentleşme, sanayileşme ve köyden kente göç ile hızlanmıştır. Nüfus artış hızı düşmekte, ortalama yaş yükselmektedir. Karadeniz'de dağınık yerleşme (engebe ve her yerde su), İç Anadolu'da toplu yerleşme (su kaynaklarının az olması) görülür.",
  "hikaye": "İnsanlar mıknatısa çekilen demir tozları gibidir: iş, ulaşım ve verimli toprak mıknatıs; dağ, soğuk ve kuraklık itici kuvvettir. Karadeniz'de her yamaçta su olduğu için evler dağılır; bozkırda ise herkes aynı çeşmenin başına toplanır, köyler toplu olur.",
  "tuzak": "Tuzak: Doğu Karadeniz'de dağınık yerleşmenin nedeni engebe ve suyun her yerde bulunmasıdır, kuraklık değil. Nüfus yoğunluğu (aritmetik: nüfus ÷ alan) ile tarımsal yoğunluk (tarım nüfusu ÷ tarım alanı) aynı değildir. Kentleşme doğal artıştan çok göçle hızlanır.",
  "nasil_sorulur": "Sınavda: nüfusun dağılışını etkileyen doğal ve beşeri faktörler, nüfus piramidi yorumu, göçün nedenleri-sonuçları ve yerleşme dokusu sorulur. Faktörün doğal mı beşeri mi olduğunu ayır."
 },
 "cografya|turizm": {
  "ozet": "Turizm türleri yararlanılan kaynağa göre ayrılır: deniz-kum-güneş (Ege, Akdeniz), kış ve kayak (Uludağ, Palandöken, Erciyes, Kartalkaya), termal/sağlık (kaplıca ve sıcak su: Pamukkale, Afyon, Bursa), yayla (Doğu Karadeniz), kültür (tarihî yapı ve müze: İstanbul, Efes, Göbeklitepe), inanç (Mardin, Hatay), kongre (bilimsel ve mesleki toplantılar), ekoturizm (doğaya saygılı, yerel yaşamı destekleyen). Akdeniz kıyılarında turizm sezonu uzundur (güneşli gün sayısı fazla, deniz suyu ılık). Turizm gelirleri hizmet ihracatıdır.",
  "hikaye": "Her turist bir şey arar: kimi güneş ve deniz (Antalya), kimi kar (Palandöken), kimi şifalı su (Pamukkale), kimi tarih (Efes), kimi serin yayla (Rize). Ülkemiz bir 'turizm marketi' gibidir; her rafında başka bir doğal veya kültürel kaynak vardır.",
  "tuzak": "Tuzak: Ekoturizm 'konaklama' demek değildir; doğal çevreyi ve yerel kültürü koruyarak yapılan turizmdir. Termal turizm kaplıca ve sıcak suya, kongre turizmi toplantılara dayanır. Turizm yalnız yaz mevsimine bağlı değildir (kış, kültür ve termal turizm).",
  "nasil_sorulur": "Sınavda: turizm türü-kaynak eşleştirmesi, merkez-turizm türü, turizm sezonunun uzunluğunu etkileyen iklim faktörleri ve turizmin ekonomiye etkisi sorulur. Tanımdaki anahtar kelimeyi (kaplıca, toplantı, tarihî yapı) bul."
 },
 "turkce|cumlede_anlam": {
  "ozet": "Cümlede anlam soruları cümleler arasındaki ilişkiyi ve cümlenin anlam özelliğini ölçer: neden-sonuç (-dığı için, -den dolayı), amaç-sonuç (için, -mek üzere; eylemden ÖNCE hedeflenen), koşul (-sa, -dıkça), karşılaştırma (daha, en, kadar), öznel-nesnel yargı (kanıtlanabilir mi?), örtülü anlam ('de, bile, yeniden' gibi sözcüklerin sezdirdiği), varsayım, olasılık, ön yargı, pişmanlık (keşke ... -saydı), dilek-istek. 'Yeniden okudum' önceki bir okumayı sezdirir.",
  "hikaye": "Cümleler arasındaki bağı köprü gibi düşün: 'Yağmur yağdığı için ıslandım' neden köprüsü; 'Islanmamak için şemsiye aldım' amaç köprüsü (hedef önceden konmuş). 'Keşke dinleseydim' geçmişe uzanan bir pişmanlık köprüsüdür, geleceğe değil.",
  "tuzak": "Tuzak: Amaç-sonuç ile neden-sonuç karışır; 'için' sözcüğünün yerine 'amacıyla' koyabiliyorsan amaç-sonuçtur, 'yüzünden' koyabiliyorsan neden-sonuçtur. 'Keşke ...-saydı' gelecek planı değil, geçmişe pişmanlıktır. Öznel yargı kişiden kişiye değişir; nesnel yargı kanıtlanabilir.",
  "nasil_sorulur": "Sınavda: hangi cümlede amaç-sonuç/neden-sonuç var, hangi cümle öznel/nesnel, hangi cümlede örtülü anlam var ve I-II-III değerlendirme biçiminde sorulur. Her cümleye 'neden?' ve 'ne amaçla?' sorularını ayrı ayrı sor."
 },
 "turkce|ses_bilgisi": {
  "ozet": "Başlıca ses olayları: ünlü düşmesi (ağız → ağzı, burun → burnu), ünlü daralması (başla- → başlıyor, de- → diyor), ünsüz yumuşaması (kitap → kitabı, ağaç → ağacı; tek heceliler genelde yumuşamaz: top → topu), ünsüz benzeşmesi/sertleşmesi (kitap-cı → kitapçı, sokak-da → sokakta), kaynaştırma ünsüzleri (y, ş, s, n: kapı-y-a), ünsüz türemesi (af → affı, his → hissi), ünsüz düşmesi (küçük → küçücük), göçüşme (toprak → torpak, halk ağzı). Büyük ünlü uyumu kalın-ince, küçük ünlü uyumu düz-yuvarlak uyumudur.",
  "hikaye": "Sesler komşuluk ilişkisi içindedir: sert bir komşu (p, ç, t, k) yanına ünlüyle başlayan bir ek gelince yumuşar (kitap → kitabı); yanına sert bir ünsüz gelince ek de sertleşir (sokak + da → sokakta). Bazen ev daralır ve bir ünlü çıkar gider (ağız → ağzı).",
  "tuzak": "Tuzak: 'Kitapçı' sertleşmedir, yumuşama değil. Tek heceli sözcüklerin çoğu yumuşamaz (saç → saçı), ama istisnalar vardır (uç → ucu). Ünlü daralması yalnız -yor ekinde olur; 'başlayan' sözcüğünde daralma yoktur. Ünlü düşmesi ile ünlü daralması karıştırılır.",
  "nasil_sorulur": "Sınavda: verilen sözcüklerde hangi ses olayı var, hangi sözcükte farklı ses olayı var, bir cümlede ünsüz yumuşaması olan sözcük hangisi gibi sorular gelir. Sözcüğü kök + ek olarak ayır, değişen sesi bul."
 },
 "turkce|sozcuk_yapisi": {
  "ozet": "Sözcükler yapıca üçe ayrılır: basit (yalnız kök veya kök + çekim eki: ev, evler, kitabı), türemiş (kök + yapım eki: kitaplık, gözlük, gelişmek), birleşik (iki ayrı sözcükten yeni anlam: hanımeli, başöğretmen, kahvaltı). Yapım eki yeni anlamlı sözcük türetir (-lık, -cı, -lı, -sız, -la-, -ış); çekim eki sözcüğün türünü değiştirmez (çoğul -ler, hâl ekleri, iyelik, kişi ekleri). İsimden isim, isimden fiil, fiilden isim, fiilden fiil yapım ekleri vardır.",
  "hikaye": "Sözcüğü bir LEGO parçası gibi düşün: kök tek parçadır (göz). Yapım eki yeni bir model çıkarır (göz-lük = başka bir nesne). Çekim eki ise modeli değiştirmeden ona renk ya da konum verir (gözler, gözde). İki ayrı model birleşip yeni bir şekil olursa birleşik sözcük olur (gözyaşı).",
  "tuzak": "Tuzak: 'Kitaplar, evde' gibi çekim eki almış sözcükler türemiş değil basittir. 'Gelişmek' türemiştir (gel-iş-mek: -iş- fiilden fiil yapım eki). Birleşik sözcükte anlam kaymalıysa bitiştirilir (hanımeli); 'güzel ev' gibi sıradan söz öbekleri birleşik sözcük sayılmaz.",
  "nasil_sorulur": "Sınavda: altı çizili sözcüklerden hangisi yapıca farklı, hangisinde yapım eki var, hangi ek fiilden isim yapmıştır gibi sorular gelir. Eki attığında kalan parçanın anlamlı olup olmadığına ve yeni anlam doğup doğmadığına bak."
 },
 "turkce|yazim_kurallari": {
  "ozet": "Temel yazım kuralları: Büyük harf (cümle başı, özel adlar, kurum adları, unvanlar özel adla birlikte), sayıların yazımı (yazıyla ayrı: on beş; Romen rakamı ve sıra sayıları: 3., üçüncü), 'de/da' bağlacı ayrı ('Sen de gel'), bulunma eki bitişik ('evde'); 'ki' bağlacı ayrı ('Biliyorum ki'), sıfat yapan -ki bitişik ('evdeki'); 'mi' soru eki ayrı ve uyuma uyar; birleşik fiiller: ses düşmesi/türemesi varsa bitişik (affetmek, kaybolmak), yoksa ayrı (yardım etmek); özel adlara getirilen ekler kesme işaretiyle ayrılır (Ankara'da), kurum adlarına getirilen ekler ayrılmaz (Türk Dil Kurumunda).",
  "hikaye": "'de' ve 'ki' iki kardeştir: bağlaç olanlar 'yalnız gezmeyi' sever, ayrı yazılır; ek olanlar sözcüğe yapışık yaşar. Ayırt etmek için cümleden çıkar: anlam bozulmuyorsa bağlaçtır, ayrıdır ('Ben de geldim' → 'Ben geldim').",
  "tuzak": "Tuzak: Kurum, kuruluş ve kitap adlarına getirilen ekler kesmeyle ayrılmaz. 'Herkes' tek s ile yazılır; 'birkaç, birçok, hiçbir, herhangi' bitişik yazılır. 'Yardım etmek' ayrı, 'affetmek' bitişik yazılır. Unvanlar özel adla kullanılınca büyük harfle başlar ('Doktor Ayşe Hanım').",
  "nasil_sorulur": "Sınavda: hangi cümlede yazım yanlışı vardır, altı çizili sözcüklerden hangisinin yazımı yanlıştır biçiminde sorulur; çoğu kez noktalamayla birlikte gelir. Önce de/da, ki, mi, büyük harf ve kesme işaretini kontrol et."
 },
 "turkce|sozcukte_anlam": {
  "ozet": "Sözcükte anlam: gerçek (temel) anlam, yan anlam (temel anlamla ilgili yeni anlam: 'masanın ayağı'), mecaz anlam (temel anlamdan tamamen uzaklaşan: 'soğuk adam'), terim anlam (bilim/sanat alanına özgü). Söz sanatları ve ilişkiler: eş anlam, zıt anlam, eş sesli (yüz: sayı / yüz: surat / yüz-mek), deyim (kalıplaşmış, mecazlı söz), ikileme, ad aktarması (mecazımürsel), dolaylama, somut-soyut, genel-özel, nitel-nicel anlam.",
  "hikaye": "Bir sözcüğün ailesini düşün: 'göz' asıl anlamıyla yüzdeki organdır (gerçek). 'Çekmecenin gözü' benzerlikten gelen akrabadır (yan anlam). 'Gözü yükseklerde' ise artık bambaşka bir kılığa girmiştir (mecaz). Aynı sözcük farklı cümlelerde farklı kıyafet giyer.",
  "tuzak": "Tuzak: Yan anlam ile mecaz anlam karıştırılır; yan anlamda temel anlamla benzerlik/ilgi açıkça sürer ('kapının kolu'), mecazda anlam tamamen değişir ('kolu uzun'). Soyut sözcük beş duyuyla algılanmaz ('sevgi'); 'rüzgâr' duyuyla algılandığı için somuttur.",
  "nasil_sorulur": "Sınavda: altı çizili sözcüğün hangi anlamda kullanıldığı, cümlede mecaz/yan anlam kullanılan sözcük, deyimin anlamı, aynı anlam ilişkisinin bulunduğu çift sorulur. Sözcüğü bağlamdan çıkarıp temel anlamıyla karşılaştır."
 },
 "turkce|sozcuk_turu": {
  "ozet": "Sözcük türleri: isim (varlık adı), sıfat (ismi niteler veya belirtir: 'güzel çiçek', 'üç kitap'), zamir (ismin yerini tutar: o, bu, bazıları, kimse), zarf (fiili, sıfatı veya başka zarfı niteler: 'çok güzel', 'hızlı koştu'), edat (tek başına anlamı zayıf, ilgi kurar: için, gibi, kadar, ile), bağlaç (sözcük veya cümleleri bağlar: ve, ama, ile, de), ünlem (duygu ve seslenme: ah, hey), fiil. Aynı sözcük görevine göre tür değiştirir: 'Güzel konuştu' → zarf; 'güzel kız' → sıfat; 'Güzeli sev' → isim.",
  "hikaye": "Sözcükler oyuncu, cümle sahnedir: aynı oyuncu 'güzel' bir sahnede ismin yanında durup onu tanıtır (sıfat), başka bir sahnede eylemin nasıl yapıldığını anlatır (zarf). Türü sözcüğün kendisi değil, o sahnedeki rolü belirler.",
  "tuzak": "Tuzak: 'Çok güzel konuştu' cümlesinde 'güzel' fiili nitelediği için zarftır, sıfat değil. 'İle' yerine 've' gelebiliyorsa bağlaç, gelemiyorsa edattır. 'Bazı kitaplar' (sıfat) ile 'Bazıları geldi' (zamir) karışır. 'Ne güzel!' sözündeki 'ne' derece bildiren zarftır.",
  "nasil_sorulur": "Sınavda: altı çizili sözcüğün türü, hangisinde farklı türde sözcük kullanılmış, sıfat-zarf-zamir ayrımı ve edat-bağlaç ayrımı sorulur. Sözcüğün yanındaki kelimeye bak: ismi niteliyorsa sıfat, fiili niteliyorsa zarf."
 },
 "turkce|cumle_olgulari": {
  "ozet": "Cümlenin ögeleri: yüklem (yargı bildiren temel öge), özne (işi yapan; 'kim/ne' sorusu), nesne (belirtili: 'neyi/kimi' — kitabı okudu; belirtisiz: 'ne' — kitap okudu), dolaylı tümleç (yönelme-bulunma-ayrılma: 'nereye, nerede, nereden' — eve geldi, parkta oynadı), zarf tümleci ('nasıl, ne zaman, niçin, ne kadar' — dün geldi). Ögeler yükleme soru sorularak bulunur; önce yüklem bulunur. Cümle türleri: yüklemine göre isim/fiil cümlesi, yerine göre kurallı/devrik, yapısına göre basit/birleşik/sıralı/bağlı.",
  "hikaye": "Yüklem bir orkestra şefidir; diğer ögeler ona soru sorularak çağrılır. 'Ayşe dün parkta kitabı okudu.' Şef 'okudu' der: 'Kim?' → Ayşe (özne), 'Neyi?' → kitabı (nesne), 'Nerede?' → parkta (dolaylı tümleç), 'Ne zaman?' → dün (zarf tümleci).",
  "tuzak": "Tuzak: 'Eve geldi'deki 'eve' dolaylı tümleçtir, nesne değil. 'Dün' zaman bildirdiği için zarf tümlecidir. Belirtisiz nesne ile özne karışır; 'Ne?' sorusuna 'kim tarafından' cevabı vermeyen öge özne değildir. Ögeler hep yükleme sorulmalı.",
  "nasil_sorulur": "Sınavda: altı çizili ögenin görevi, cümlenin öge dizilişi, hangi cümlede dolaylı tümleç/zarf tümleci yok gibi sorular gelir; bazen noktalama ve yazımla birlikte. Önce yüklemi bul, sonra sırayla soruları sor."
 },
 "turkce|paragraf": {
  "ozet": "Paragraf soruları: ana düşünce (yazarın asıl vermek istediği mesaj; çoğu zaman giriş ya da sonuç cümlesinde), yardımcı düşünceler, konu (paragrafın neden söz ettiği), başlık, paragrafın yapısı (giriş-gelişme-sonuç cümlesi, akışı bozan cümle, cümlelerin sıralanması, paragrafın ikiye bölünmesi), anlatım biçimleri (açıklayıcı, tartışmacı, öyküleyici, betimleyici) ve düşünceyi geliştirme yolları (tanımlama, örnekleme, karşılaştırma, tanık gösterme, sayısal verilerden yararlanma).",
  "hikaye": "Paragraf bir ev gibidir: giriş cümlesi kapıdır (bağlaçla başlamaz), gelişme cümleleri odalardır, sonuç cümlesi pencereden görülen manzaradır. Ana düşünce evin sahibi; yardımcı düşünceler misafirlerdir. Misafiri ev sahibi sanmak en sık hatadır.",
  "tuzak": "Tuzak: Doğru ama paragrafta söylenmeyen bir yargı 'paragraftan çıkarılabilir' değildir. Ana düşünce soru kökünde 'asıl, vurgulanmak istenen, en kapsamlı' kelimeleriyle aranır; tek bir ayrıntıya odaklanan şık genellikle yardımcı düşüncedir. Betimleyici anlatımda tablo çizilir, öyküleyicide olay akar.",
  "nasil_sorulur": "Sınavda: ana düşünce, konu, çıkarılabilecek/çıkarılamayacak yargı, anlatım biçimi, akışı bozan cümle ve boşluk doldurma sorulur. Önce soru kökünü oku, sonra paragrafı; şıkları paragraftaki kanıta dayandır."
 },
 "turkce|noktalama_isaretleri": {
  "ozet": "Başlıca noktalama işaretleri: nokta (cümle sonu, kısaltma, sıra sayısı: 3.), virgül (eş görevli sözcükleri ayırma, uzun cümlede özneyi belirtme, hitaplardan sonra, ara sözü ayırma), noktalı virgül (ögeleri arasında virgül bulunan eş görevli grupları ve sıralı cümleleri ayırma), iki nokta (açıklama ve örnek öncesi, alıntıdan önce), üç nokta (tamamlanmamış cümle), soru işareti (soru, bilinmeyen tarih: (1330?-1390)), ünlem (duygu, seslenme, alay için parantez içinde (!)), tırnak (alıntı), kesme (özel ada gelen ek: Ankara'da), kısa çizgi (satır sonu bölme, ara), yay ayraç (açıklama).",
  "hikaye": "Noktalama işaretleri trafik işaretleri gibidir: nokta kırmızı ışık (dur), virgül sarı ışık (yavaşla), iki nokta 'dikkat, açıklama geliyor' tabelası, ünlem korna, soru işareti yol soran bir yolcu. Yanlış işaret, okuru yanlış yöne yollar.",
  "tuzak": "Tuzak: İçinde soru eki olsa da soru anlamı taşımayan cümlenin sonuna soru işareti konmaz ('Gelir mi gelmez mi bilmiyorum.'). Alay ve küçümseme için ayraç içinde ünlem (!) kullanılır, ayraç içinde soru işareti (?) ise bilinmeyen/şüpheli bilgi içindir. Kurum adlarına gelen ekler kesmeyle ayrılmaz.",
  "nasil_sorulur": "Sınavda: numaralanmış yerlerin hangisine hangi işaret gelmeli, hangi cümlede noktalama yanlışı var, bir işaretin hangi görevle kullanıldığı sorulur. Her numaralı yerde 'açıklama mı, sıralama mı, ara söz mü?' diye sor."
 },
 "turkce|anlatim_bozuklugu": {
  "ozet": "Anlatım bozuklukları iki gruptur. Anlamsal: gereksiz sözcük kullanımı (aynı anlamı veren iki sözcük: 'geri iade', 'yaklaşık 15 kadar'), sözcüğün yanlış anlamda kullanılması, mantık hatası, çelişki, sözcüklerin yanlış yerde kullanılması, deyim yanlışlığı. Yapısal (dil bilgisel): özne-yüklem uyumsuzluğu (tekillik-çoğulluk, kişi), ortak öge yanlışlığı (ortak kullanılan ögenin her yüklemle uyuşmaması: 'Bu konuyu düşündüm ve karar verdim' — 'konuyu karar verdim' olmaz), tamlama yanlışlığı, ek eksikliği veya yanlışlığı, çatı uyumsuzluğu, yüklem eksikliği.",
  "hikaye": "Cümleyi bir makine gibi düşün: Fazladan parça (gereksiz sözcük) gürültü yapar, eksik parça (öge eksikliği) makineyi durdurur, yanlış parça (yanlış anlamlı sözcük) makineyi ters çalıştırır. Ortak öge, iki makineye aynı anda takılan tek kayıştır; her iki makineye de uymalıdır.",
  "tuzak": "Tuzak: Ortak öge yanlışlığını bulmak için ortak ögeyi her yüklemle ayrı ayrı oku. 'Yaklaşık' ve 'kadar' aynı cümlede gereksizlik yapar. Cümlenin uzun olması tek başına bozukluk değildir. 'Ve' ile bağlanan yüklemlerin çatısı (etken-edilgen) uyumlu olmalıdır.",
  "nasil_sorulur": "Sınavda: hangi cümlede anlatım bozukluğu var, hangi cümlenin bozukluğu farklı nedenden kaynaklanıyor, verilen cümlenin bozukluğu nasıl giderilir biçiminde sorulur. Önce gereksiz sözcük ve anlam çelişkisi, sonra öge uyumunu kontrol et."
 },
 "guncel|spor": {
  "ozet": "Güncel spor soruları: büyük organizasyonlar (Olimpiyat ve Paralimpik Oyunları, Dünya ve Avrupa şampiyonaları), bu organizasyonların ev sahibi şehir/ülkeleri ve yılları, milli sporcularımızın ve takımlarımızın derece aldığı branşlar, uluslararası federasyonlar (FIFA, UEFA, IOC) ve önemli rekorlar. Olimpiyat Oyunları dört yılda bir yapılır; Yaz ve Kış Olimpiyatları iki yıl arayla dönüşümlüdür. Bilgiler soru çözümlerinde kaynaklarıyla verilir; tarih ve sporcu adını birlikte ezberle.",
  "hikaye": "Spor gündemini bir zaman çizelgesi gibi kur: her organizasyon için 'Ne? Nerede? Ne zaman? Biz ne kazandık?' kartı hazırla. Sporcu adını branşıyla, branşı organizasyonla bağlarsan bilgi tek başına kaybolmaz; bir zincirin halkası olur.",
  "tuzak": "Tuzak: Olimpiyat ile Dünya Şampiyonası, Yaz ile Kış Oyunları, Olimpiyat ile Paralimpik Oyunları karıştırılır. Sporcunun branşı benzer branşla (güreş-judo, okçuluk-atıcılık) şıklara konur. Sadece son organizasyonu değil, ev sahibi ülkeyi de doğrula.",
  "nasil_sorulur": "Sınavda: sporcu-branş, organizasyon-ev sahibi şehir, takım-kazandığı kupa eşleştirmeleri ve I-II-III öncüllü doğruluk soruları gelir. Yanlış öncül genellikle benzer branş veya yakın yıl değiştirilerek kurulur."
 },
 "guncel|kultur_sanat": {
  "ozet": "Kültür-sanat soruları: UNESCO Dünya Mirası Listesi'ndeki Türkiye varlıkları (Göbeklitepe - Şanlıurfa, Efes - İzmir, Selimiye Camii - Edirne, Safranbolu - Karabük, Ani Arkeolojik Alanı - Kars, Arslantepe Höyüğü - Malatya, Nemrut Dağı - Adıyaman, Hattuşa - Çorum, Çatalhöyük - Konya, Pamukkale-Hierapolis - Denizli, Göreme - Nevşehir), UNESCO Somut Olmayan Kültürel Miras (Karagöz, Nasreddin Hoca fıkraları geleneği, Türk kahvesi kültürü, ebru, âşıklık geleneği gibi), müzeler, ödüller, anma ve kutlama yılları.",
  "hikaye": "Türkiye haritası üzerinde bir gezi planla: batıdan Edirne'de Selimiye, aşağı inip İzmir'de Efes, Denizli'de Pamukkale; ortada Konya'da Çatalhöyük, Nevşehir'de Göreme, Çorum'da Hattuşa; doğuya Malatya'da Arslantepe, Adıyaman'da Nemrut, Şanlıurfa'da Göbeklitepe, en doğuda Kars'ta Ani. Mekânı il ile eşleştirmek akılda kalıcı olur.",
  "tuzak": "Tuzak: Ani Kars'tadır, Ağrı'da değil; Arslantepe Malatya'dadır, Şanlıurfa'da değil; Efes İzmir'de (Selçuk), Safranbolu Karabük'tedir. Somut miras (yapı, alan) ile somut olmayan miras (gelenek, uygulama) listeleri karıştırılır.",
  "nasil_sorulur": "Sınavda: miras alanı-il eşleştirmesi, gezi rotası sıralaması, bir geleneğin hangi listede olduğu ve sanatçı-eser eşleştirmeleri sorulur. Yanlış şıklar komşu illerle kurulur; haritada yerini düşün."
 },
 "guncel|turkiye_gundemi": {
  "ozet": "Türkiye gündemi soruları kurumlar ve görevlerine yoğunlaşır: RTÜK (radyo-televizyon yayınlarını düzenler ve denetler), BDDK (bankacılığı düzenler ve denetler), SPK (sermaye piyasalarını düzenler), Rekabet Kurumu (rekabet ihlallerini inceler), TÜBİTAK (bilimsel araştırma ve teknoloji projelerini destekler), TÜİK (resmî istatistikleri üretir), TCMB (para politikası, fiyat istikrarı), KVKK (kişisel verilerin korunması), Türkiye Uzay Ajansı, AFAD (afet ve acil durum yönetimi). Ayrıca büyük projeler, millî teknoloji hamleleri ve önemli günler sorulur.",
  "hikaye": "Her kurumu bir 'mahalle görevlisi' gibi düşün: RTÜK televizyon kanallarının bekçisi, BDDK bankaların müfettişi, SPK borsanın hakemi, Rekabet Kurumu pazardaki 'haksız oyun' hakemi, TÜİK mahallenin sayım memuru, TCMB paranın değerini koruyan kasadar, AFAD afet anında koşan ekip.",
  "tuzak": "Tuzak: SPK ile Rekabet Kurumu, BDDK ile TCMB, TÜBİTAK ile TÜİK birbirinin yerine şıklara konur. Kurumun adındaki anahtar kelime (Radyo-Televizyon, Bankacılık, Sermaye Piyasası, İstatistik) görevin ipucudur.",
  "nasil_sorulur": "Sınavda: kurum-görev eşleştirmesi I-II-III öncülleriyle, kısaltmanın açılımı ve bir görevin hangi kuruma ait olduğu sorulur. Önce kısaltmayı aç, sonra görevle karşılaştır."
 },
 "guncel|dunya_gundemi": {
  "ozet": "Dünya gündemi soruları uluslararası kuruluşları ve dünya genelindeki önemli olayları ölçer. BM (1945, merkez New York) organları: Genel Kurul (tüm üyeler), Güvenlik Konseyi (5 daimî üye: ABD, Rusya, Çin, Fransa, Birleşik Krallık + 10 geçici üye), Uluslararası Adalet Divanı (Lahey). BM uzmanlık kuruluşları: WHO (sağlık), UNESCO (eğitim, bilim, kültür), ILO (çalışma hayatı), FAO (gıda ve tarım), UNICEF (çocuklar). NATO (1949, Türkiye 1952) askerî ittifaktır; AB ayrı bir birliktir. Dünya Ticaret Örgütü (WTO) ticaret kurallarıyla ilgilenir. Türk Devletleri Teşkilatı Türk dünyası iş birliğidir.",
  "hikaye": "BM'yi büyük bir okul gibi düşün: Genel Kurul tüm öğrencilerin toplandığı salon, Güvenlik Konseyi veto hakkı olan 5 kalıcı kurul üyesi, uzmanlık kuruluşları ise okulun kulüpleri: WHO sağlık kulübü, UNESCO kültür kulübü, ILO işçi kulübü, FAO beslenme kulübü. NATO ise okulun dışındaki bir 'güvenlik ittifakı'dır.",
  "tuzak": "Tuzak: NATO üyeliği AB üyeliği anlamına gelmez. Genel Kurul ile Güvenlik Konseyi farklı organlardır; Genel Kurulda tüm üyeler vardır. ILO çalışma hayatıyla ilgilenir, gümrük tarifeleri değil (o WTO'nun alanı). UNESCO ile UNICEF karıştırılır.",
  "nasil_sorulur": "Sınavda: kuruluş-görev, kuruluş-merkez, organ-yapı eşleştirmeleri ve beş yargılı 'hangisi yanlıştır' soruları gelir. Kısaltmanın İngilizce açılımı görevi verir (World Health Organization = sağlık)."
 }
}


def main():
    veri = json.loads(YOL.read_text(encoding='utf-8'))
    eklenen = 0
    for k, kart in KARTLAR.items():
        if k in veri:
            continue  # var olan kart ezilmez
        assert set(kart) == {'ozet', 'hikaye', 'tuzak', 'nasil_sorulur'}, k
        veri[k] = kart
        eklenen += 1
    YOL.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding='utf-8')
    print('eklenen kart:', eklenen, 'toplam:', len(veri))


if __name__ == '__main__':
    main()
