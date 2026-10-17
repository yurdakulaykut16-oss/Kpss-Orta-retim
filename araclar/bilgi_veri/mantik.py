"""Sözel mantık soru motoru (KPSS tarzı).

Her bulmaca için koşulları sağlayan TÜM olası düzenler bilgisayarla sayılır
(bit maskeleri). Böylece:

- "kesinlikle doğrudur" sorusunda doğru seçenek bütün olası düzenlerde sağlanır;
  çeldiricilerin çoğu bazı düzenlerde doğru olan ("olabilir") ifadelerdir —
  öğrenci tipik olarak iki seçenek arasında kalır ama yalnız biri kesindir.
- "kesinlikle yanlıştır", "doğru olabilir", "hangisi bilinirse kesin belirlenir"
  ve "... ise hangisi kesinlikle doğrudur" soruları da aynı sayımla doğrulanır.
- Tek çözümlü eşleştirme bulmacalarında soru, tek düzenden okunur.

Gereksiz (diğer koşullardan çıkarılabilen) koşullar atılır; seçenekler tek bir
koşulun doğrudan tekrarı ya da doğrudan çelişkisi olamaz.
"""
from itertools import permutations

from .ortak import q

GUNLER = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']


def _say(m):
    return bin(m).count('1')


def _bitler(m):
    i = 0
    while m:
        if m & 1:
            yield i
        m >>= 1
        i += 1


class Evren:
    def __init__(self, durumlar):
        self.D = durumlar
        self.TUM = (1 << len(durumlar)) - 1
        self._onbellek = {}

    def maske(self, anahtar, f):
        if anahtar not in self._onbellek:
            m = 0
            for i, d in enumerate(self.D):
                if f(d):
                    m |= 1 << i
            self._onbellek[anahtar] = m
        return self._onbellek[anahtar]


# ------------------------------------------------------------------ sıralama
def _baglam(tip, ad, gen, abl):
    """Sıralama bağlamı: (koşul türü -> (metin üretici, sınama)), konum adı, giriş."""
    if tip == 'sira':
        T = {
            'hemen_once': lambda x, y: f'{ad[x]}, {gen[y]} hemen solunda oturmaktadır.',
            'once': lambda x, y: f'{ad[x]}, {abl[y]} daha solda oturmaktadır.',
            'yan': lambda x, y: f'{ad[x]} ile {ad[y]} yan yana oturmaktadır.',
            'yan_degil': lambda x, y: f'{ad[x]} ile {ad[y]} yan yana oturmamaktadır.',
            'iki_ara': lambda x, y: f'{ad[x]} ile {ad[y]} arasında yalnızca bir kişi oturmaktadır.',
            'yer': lambda x, k: f'{ad[x]}, soldan {k}. sandalyede oturmaktadır.',
            'yer_degil': lambda x, k: f'{ad[x]}, soldan {k}. sandalyede oturmamaktadır.',
            'kenar': lambda x, _: f'{ad[x]}, uçtaki sandalyelerden birinde oturmaktadır.',
            'kenar_degil': lambda x, _: f'{ad[x]}, uçtaki sandalyelerde oturmamaktadır.',
        }
        konum = lambda k: f'Soldan {k}.'
        giris = lambda: f'{", ".join(ad[:4])} ve {ad[4]}; yan yana dizilmiş beş sandalyeye birer kişi olacak biçimde oturmuştur.'
        duzen = lambda p: 'Soldan sağa: ' + ' – '.join(ad[j] for j in sorted(range(5), key=lambda j: p[j]))
    elif tip == 'kat':
        T = {
            'hemen_once': lambda x, y: f'{ad[x]}, {gen[y]} hemen bir alt katında oturmaktadır.',
            'once': lambda x, y: f'{ad[x]}, {abl[y]} daha alt bir katta oturmaktadır.',
            'yan': lambda x, y: f'{ad[x]} ile {gen[y]} katları ardışıktır.',
            'yan_degil': lambda x, y: f'{ad[x]} ile {gen[y]} katları ardışık değildir.',
            'iki_ara': lambda x, y: f'{ad[x]} ile {gen[y]} katları arasında yalnızca bir kat vardır.',
            'yer': lambda x, k: f'{ad[x]}, {k}. katta oturmaktadır.',
            'yer_degil': lambda x, k: f'{ad[x]}, {k}. katta oturmamaktadır.',
            'kenar': lambda x, _: f'{ad[x]}, en alt ya da en üst katta oturmaktadır.',
            'kenar_degil': lambda x, _: f'{ad[x]}, en alt ve en üst katlarda oturmamaktadır.',
        }
        konum = lambda k: f'{k}. kat'
        giris = lambda: (f'{", ".join(ad[:4])} ve {ad[4]}; beş katlı bir apartmanın her katında bir kişi olacak '
                         f'biçimde oturmaktadır (1. kat en alt kattır).')
        duzen = lambda p: 'Alttan üste: ' + ' – '.join(ad[j] for j in sorted(range(5), key=lambda j: p[j]))
    elif tip == 'yaris':
        T = {
            'hemen_once': lambda x, y: f'{ad[x]}, yarışı {abl[y]} hemen önce bitirmiştir.',
            'once': lambda x, y: f'{ad[x]}, yarışı {abl[y]} önce bitirmiştir.',
            'yan': lambda x, y: f'{ad[x]} ile {ad[y]} yarışı art arda bitirmiştir.',
            'yan_degil': lambda x, y: f'{ad[x]} ile {ad[y]} yarışı art arda bitirmemiştir.',
            'iki_ara': lambda x, y: f'{ad[x]} ile {ad[y]} arasında yarışı yalnızca bir kişi bitirmiştir.',
            'yer': lambda x, k: f'{ad[x]}, yarışı {k}. sırada bitirmiştir.',
            'yer_degil': lambda x, k: f'{ad[x]}, yarışı {k}. sırada bitirmemiştir.',
            'kenar': lambda x, _: f'{ad[x]}, yarışı ya ilk ya da son sırada bitirmiştir.',
            'kenar_degil': lambda x, _: f'{ad[x]}, yarışı ilk ya da son sırada bitirmemiştir.',
        }
        konum = lambda k: f'{k}. sıra'
        giris = lambda: (f'{", ".join(ad[:4])} ve {ad[4]} bir koşu yarışına katılmış ve yarışı farklı sıralarda '
                         f'bitirmiştir (aynı anda bitiren yoktur).')
        duzen = lambda p: 'Bitiriş sırası: ' + ' – '.join(ad[j] for j in sorted(range(5), key=lambda j: p[j]))
    else:  # gün
        T = {
            'hemen_once': lambda x, y: f'{ad[x]}, {abl[y]} bir gün önce nöbet tutmuştur.',
            'once': lambda x, y: f'{ad[x]}, {abl[y]} önceki günlerden birinde nöbet tutmuştur.',
            'yan': lambda x, y: f'{ad[x]} ile {ad[y]} ardışık günlerde nöbet tutmuştur.',
            'yan_degil': lambda x, y: f'{ad[x]} ile {ad[y]} ardışık günlerde nöbet tutmamıştır.',
            'iki_ara': lambda x, y: f'{ad[x]} ile {gen[y]} nöbet günleri arasında yalnızca bir gün vardır.',
            'yer': lambda x, k: f'{ad[x]}, {GUNLER[k - 1]} günü nöbet tutmuştur.',
            'yer_degil': lambda x, k: f'{ad[x]}, {GUNLER[k - 1]} günü nöbet tutmamıştır.',
            'kenar': lambda x, _: f'{ad[x]}, ya Pazartesi ya da Cuma günü nöbet tutmuştur.',
            'kenar_degil': lambda x, _: f'{ad[x]}, Pazartesi ve Cuma günleri nöbet tutmamıştır.',
        }
        konum = lambda k: GUNLER[k - 1]
        giris = lambda: (f'{", ".join(ad[:4])} ve {ad[4]}; pazartesiden cumaya kadar her gün bir kişi olmak üzere '
                         f'birer gün nöbet tutmuştur.')
        duzen = lambda p: ', '.join(f'{GUNLER[p[j] - 1]}: {ad[j]}' for j in sorted(range(5), key=lambda j: p[j]))
    S = {
        'hemen_once': lambda x, y: (lambda p: p[x] == p[y] - 1),
        'once': lambda x, y: (lambda p: p[x] < p[y]),
        'yan': lambda x, y: (lambda p: abs(p[x] - p[y]) == 1),
        'yan_degil': lambda x, y: (lambda p: abs(p[x] - p[y]) != 1),
        'iki_ara': lambda x, y: (lambda p: abs(p[x] - p[y]) == 2),
        'yer': lambda x, k: (lambda p: p[x] == k),
        'yer_degil': lambda x, k: (lambda p: p[x] != k),
        'kenar': lambda x, _: (lambda p: p[x] in (1, 5)),
        'kenar_degil': lambda x, _: (lambda p: p[x] not in (1, 5)),
    }
    return T, S, konum, giris, duzen


SIRA_EVREN = Evren([dict(zip(range(5), p)) for p in permutations(range(1, 6))])


def _atomlar(T, S, ev, turler):
    """(anahtar, metin, maske) listesi."""
    out = []
    for t in turler:
        for x in range(5):
            if t in ('yer', 'yer_degil'):
                for k in range(1, 6):
                    out.append(((t, x, k), T[t](x, k), ev.maske((t, x, k), S[t](x, k))))
            elif t in ('kenar', 'kenar_degil'):
                out.append(((t, x, 0), T[t](x, 0), ev.maske((t, x, 0), S[t](x, 0))))
            else:
                for y in range(5):
                    if y == x or (t in ('yan', 'yan_degil', 'iki_ara') and y < x):
                        continue
                    out.append(((t, x, y), T[t](x, y), ev.maske((t, x, y), S[t](x, y))))
    return out


def _kosul_sec(rng, ev, havuz, gizli, alt, ust, en_cok_yer=1):
    """Gizli düzende doğru koşullardan, olası düzen sayısı [alt, ust] olana dek seç."""
    havuz = [c for c in havuz if c[2] >> gizli & 1]
    rng.shuffle(havuz)
    S, sec_, yer = ev.TUM, [], 0
    for c in havuz:
        if c[0][0] == 'yer':
            if yer >= en_cok_yer:
                continue
        S2 = S & c[2]
        if S2 == S or _say(S2) < alt:
            continue
        sec_.append(c)
        yer += c[0][0] == 'yer'
        S = S2
        if _say(S) <= ust:
            break
    if not (alt <= _say(S) <= ust):
        return None, None
    for c in list(sec_):
        kalan = ev.TUM
        for d in sec_:
            if d is not c:
                kalan &= d[2]
        if kalan == S:
            sec_.remove(c)
    if len(sec_) < 3:
        return None, None
    rng.shuffle(sec_)
    return sec_, S


def _onemsiz(a, kosullar):
    """Seçenek tek bir koşulun doğrudan sonucu ya da doğrudan çelişkisi mi?"""
    return any((c[2] & a[2]) == c[2] or (c[2] & a[2]) == 0 for c in kosullar)


def _duzen_metni(ev, S, duzen):
    return [duzen(ev.D[i]) for i in _bitler(S)]


def _gerekce_kismi(duzenler, secenekler, S_bit, bas):
    satir = ' '.join(f'({i + 1}) {d}.' for i, d in enumerate(duzenler))
    notlar = []
    for metin, m, rol in secenekler:
        hangi = [str(i + 1) for i, b in enumerate(S_bit) if m >> b & 1]
        if not hangi:
            notlar.append(f'“{metin[:-1]}” hiçbir düzende sağlanmaz')
        elif len(hangi) == len(S_bit):
            notlar.append(f'“{metin[:-1]}” bütün düzenlerde sağlanır')
        else:
            notlar.append(f'“{metin[:-1]}” yalnız {", ".join(hangi)} numaralı düzen(ler)de sağlanır')
    return f'{bas} Koşulları sağlayan olası düzenler: {satir} ' + '; '.join(notlar) + '.'


def _soru_kur(rng, tur_on, metin, ev, kosullar, S, atomlar, duzen, tip):
    """Kısmi bilgili bulmacadan bir soru (tip: kesin/yanlis/olabilir/ek/kosul)."""
    S_bit = list(_bitler(S))
    aday = [a for a in atomlar if not _onemsiz(a, kosullar) and a[1] not in {c[1] for c in kosullar}]
    kesin = [a for a in aday if (a[2] & S) == S]
    asla = [a for a in aday if (a[2] & S) == 0]
    bazen = [a for a in aday if 0 < _say(a[2] & S) < len(S_bit)]
    rng.shuffle(kesin)
    rng.shuffle(asla)
    rng.shuffle(bazen)
    duzenler = _duzen_metni(ev, S, duzen)
    if tip == 'kesin':
        if not kesin or len(bazen) < 2:
            return None
        d = kesin[0]
        yan = bazen[:rng.choice([2, 3, 4])]
        yan += asla[:4 - len(yan)]
        if len(yan) < 4:
            yan += bazen[len(yan):len(yan) + 4 - len(yan)]
        if len(yan) < 4:
            return None
        soru = 'Buna göre aşağıdakilerden hangisi kesinlikle doğrudur?'
        bas = 'Doğru seçenek bütün olası düzenlerde sağlanır; “olabilir” türündeki seçenekler yalnız bazı düzenlerde doğrudur.'
    elif tip == 'yanlis':
        if not asla or len(bazen) < 3:
            return None
        d = asla[0]
        yan = bazen[:rng.choice([3, 4])]
        yan += kesin[:4 - len(yan)]
        if len(yan) < 4:
            yan += bazen[len(yan):len(yan) + 4 - len(yan)]
        if len(yan) < 4:
            return None
        soru = 'Buna göre aşağıdakilerden hangisi kesinlikle yanlıştır?'
        bas = 'Doğru seçenek hiçbir olası düzende sağlanmaz; diğerleri en az bir düzende doğrudur.'
    elif tip == 'olabilir':
        if not bazen or len(asla) < 4:
            return None
        d = bazen[0]
        yan = asla[:4]
        soru = 'Buna göre aşağıdakilerden hangisi doğru olabilir?'
        bas = 'Doğru seçenek en az bir olası düzende sağlanır; diğerleri hiçbir düzende sağlanmaz.'
    elif tip == 'ek':
        if len(S_bit) < 3:
            return None
        tek = [a for a in bazen if _say(a[2] & S) == 1]
        cok = [a for a in bazen if _say(a[2] & S) >= 2]
        if not tek or len(cok) < 4:
            return None
        d, yan = tek[0], cok[:4]
        soru = 'Aşağıdakilerden hangisi bilinirse yerleşimin tamamı kesin olarak belirlenir?'
        bas = 'Doğru seçenek olası düzenlerden yalnız birinde sağlandığı için tek düzeni bırakır; diğerleri birden çok düzende sağlanır.'
    else:  # kosul
        kosul = [a for a in bazen if 2 <= _say(a[2] & S) < len(S_bit) or _say(a[2] & S) == 1]
        rng.shuffle(kosul)
        for c in kosul:
            S2 = S & c[2]
            if c[0][0] not in ('yer', 'hemen_once', 'yan', 'kenar', 'iki_ara'):
                continue
            k2 = [a for a in aday if (a[2] & S2) == S2 and (a[2] & S) != S and a is not c
                  and not ((c[2] & a[2]) == c[2])]
            b2 = [a for a in aday if 0 < _say(a[2] & S2) < _say(S2)]
            n2 = [a for a in aday if (a[2] & S2) == 0 and (a[2] & S) != 0]
            if not k2 or len(b2) + len(n2) < 4:
                continue
            rng.shuffle(k2)
            rng.shuffle(b2)
            rng.shuffle(n2)
            d = k2[0]
            yan = (b2[:2] + n2)[:4]
            if len(yan) < 4:
                yan = (b2 + n2)[:4]
            if len(yan) < 4:
                continue
            soru = f'Bu bilgilere ek olarak “{c[1]}” bilgisi verilirse aşağıdakilerden hangisi kesinlikle doğrudur?'
            S = S2
            S_bit = list(_bitler(S))
            duzenler = _duzen_metni(ev, S, duzen)
            bas = f'Ek bilgiyle ({c[1][:-1]}) kalan düzenler aşağıdadır; doğru seçenek bunların hepsinde sağlanır.'
            break
        else:
            return None
    metinler = [d[1]] + [a[1] for a in yan]
    if len(set(metinler)) != 5:
        return None
    ger = _gerekce_kismi(duzenler, [(d[1], d[2], 'd')] + [(a[1], a[2], 'y') for a in yan], S_bit, bas)
    return q(f'{tur_on}_{tip}', 'Sözel Mantık', metin + ' ' + soru, d[1], [a[1] for a in yan], ger, 3)


def siralama_bulmacalari(rng, adlar, adet):
    out = []
    ev = SIRA_EVREN
    deneme = 0
    while len(out) < adet and deneme < adet * 30:
        deneme += 1
        kisiler = rng.sample(adlar, 5)
        ad, gen, abl = [k[0] for k in kisiler], [k[1] for k in kisiler], [k[2] for k in kisiler]
        tip = rng.choice(['sira', 'kat', 'yaris', 'gun'])
        T, S, konum, giris, duzen = _baglam(tip, ad, gen, abl)
        havuz = _atomlar(T, S, ev, ['hemen_once', 'once', 'once', 'yan', 'yan_degil', 'iki_ara', 'yer', 'yer_degil',
                                    'kenar', 'kenar_degil'])
        gizli = rng.randrange(len(ev.D))
        kos, Sm = _kosul_sec(rng, ev, havuz, gizli, 2, 6)
        if not kos:
            continue
        metin = giris() + ' Bilinenler: ' + ' '.join(f'({j + 1}) {c[1]}' for j, c in enumerate(kos))
        secenek = _atomlar(T, S, ev, ['yer', 'once', 'hemen_once', 'yan', 'kenar', 'iki_ara'])
        tipler = ['kesin', 'kesin', 'yanlis', 'olabilir', 'ek', 'kosul', 'kosul']
        rng.shuffle(tipler)
        alinan = set()
        for t in tipler:
            if t in alinan or len(alinan) >= 2:
                continue
            r = _soru_kur(rng, 'mantik', metin, ev, kos, Sm, secenek, duzen, t)
            if r:
                out.append(r)
                alinan.add(t)
    return out


# ------------------------------------------------------------------ eşleştirme
BOYUT = {
    'meslek': dict(
        degerler=['doktor', 'öğretmen', 'mühendis', 'avukat', 'mimar', 'eczacı', 'hemşire'],
        yuklem={'doktor': 'doktordur', 'öğretmen': 'öğretmendir', 'mühendis': 'mühendistir', 'avukat': 'avukattır',
                'mimar': 'mimardır', 'eczacı': 'eczacıdır', 'hemşire': 'hemşiredir'},
        olumsuz=lambda v: f'{v} değildir', ozne=lambda v: f'{v[0].upper() + v[1:]} olan kişi',
        tanim='meslekleri', liste='Meslekler: {}.', soru=lambda x: f'Buna göre {x} kişinin mesleği nedir?',
        sec=lambda v: v[0].upper() + v[1:]),
    'sehir': dict(
        degerler=['Ankara', 'İzmir', 'Bursa', 'Trabzon', 'Antalya', 'Konya', 'Sivas', 'Van'],
        yonelme={'Ankara': "Ankara'ya", 'İzmir': "İzmir'e", 'Bursa': "Bursa'ya", 'Trabzon': "Trabzon'a",
                 'Antalya': "Antalya'ya", 'Konya': "Konya'ya", 'Sivas': "Sivas'a", 'Van': "Van'a"},
        tanim='tatilde gittikleri şehirler', liste='Şehirler: {}.', soru=lambda x: f'Buna göre {x} kişi hangi şehre gitmiştir?',
        sec=lambda v: v),
    'ulasim': dict(
        degerler=['otobüs', 'tren', 'uçak', 'gemi', 'otomobil'],
        araclik={'otobüs': 'otobüsle', 'tren': 'trenle', 'uçak': 'uçakla', 'gemi': 'gemiyle', 'otomobil': 'otomobille'},
        tanim='kullandıkları ulaşım araçları', liste='Ulaşım araçları: {}.',
        soru=lambda x: f'Buna göre {x} kişi hangi ulaşım aracını kullanmıştır?', sec=lambda v: v[0].upper() + v[1:]),
}


def _yuklem(b, v, olumlu=True):
    B = BOYUT[b]
    if b == 'meslek':
        return B['yuklem'][v] if olumlu else B['olumsuz'](v)
    if b == 'sehir':
        return f"{B['yonelme'][v]} {'gitmiştir' if olumlu else 'gitmemiştir'}"
    return f"{B['araclik'][v]} {'yolculuk etmiştir' if olumlu else 'yolculuk etmemiştir'}"


def _ozne(b, v):
    B = BOYUT[b]
    if b == 'meslek':
        return B['ozne'](v)
    if b == 'sehir':
        return f"{B['yonelme'][v]} giden kişi"
    return f"{B['araclik'][v][0].upper() + B['araclik'][v][1:]} yolculuk eden kişi"


def _ozne_kucuk(b, v):
    s = _ozne(b, v)
    return s if b == 'sehir' else s[0].lower() + s[1:]


_ESLES_EVREN = {}


def _esles_evren(n):
    if n not in _ESLES_EVREN:
        P = list(permutations(range(n)))
        _ESLES_EVREN[n] = Evren([(a, b) for a in P for b in P])
    return _ESLES_EVREN[n]


def eslestirme_bulmacalari(rng, adlar, adet, n=4, mod='kismi'):
    """n kişi, iki boyut (her boyutta n farklı değer). Durum: (p1, p2), p[i] = kişinin değer indisi."""
    out = []
    ev = _esles_evren(n)
    deneme = 0
    while len(out) < adet and deneme < adet * 30:
        deneme += 1
        b1, b2 = rng.sample(['meslek', 'sehir', 'ulasim'], 2)
        v1 = rng.sample(BOYUT[b1]['degerler'], n)
        v2 = rng.sample(BOYUT[b2]['degerler'], n)
        kisiler = rng.sample(adlar, n)
        ad = [k[0] for k in kisiler]
        gen = [k[1] for k in kisiler]
        boy = {b1: (0, v1), b2: (1, v2)}
        atom = []
        for b, (j, vs) in boy.items():
            for x in range(n):
                for vi, v in enumerate(vs):
                    atom.append((('has', b, x, vi), f'{ad[x]} {_yuklem(b, v)}.',
                                 ev.maske(('has', j, x, vi), lambda d, j=j, x=x, vi=vi: d[j][x] == vi)))
                    atom.append((('not', b, x, vi), f'{ad[x]} {_yuklem(b, v, False)}.',
                                 ev.maske(('not', j, x, vi), lambda d, j=j, x=x, vi=vi: d[j][x] != vi)))
        for i1, a in enumerate(v1):
            for i2, c in enumerate(v2):
                f = lambda d, i1=i1, i2=i2: any(d[0][x] == i1 and d[1][x] == i2 for x in range(n))
                m = ev.maske(('link', i1, i2), f)
                atom.append((('link', b1, i1, i2), f'{_ozne(b1, a)} {_yuklem(b2, c)}.', m))
                atom.append((('link_not', b1, i1, i2), f'{_ozne(b1, a)} {_yuklem(b2, c, False)}.', ev.TUM & ~m))
                if rng.random() < 0.5:
                    atom.append((('link2', b2, i2, i1), f'{_ozne(b2, c)} {_yuklem(b1, a)}.', m))
        gizli = rng.randrange(len(ev.D))
        tekil = mod == 'tekil'
        kos, Sm = _kosul_sec(rng, ev, [a for a in atom if a[0][0] != 'has' or rng.random() < 0.35], gizli,
                             1 if tekil else 2, 1 if tekil else 5, en_cok_yer=0)
        if not kos or len(kos) > (8 if tekil else 6):
            continue
        giris = (f'{", ".join(ad[:-1])} ve {ad[-1]} adlı {n} kişinin {BOYUT[b1]["tanim"]} ve {BOYUT[b2]["tanim"]} '
                 f'birbirinden farklıdır. {BOYUT[b1]["liste"].format(", ".join(v1))} {BOYUT[b2]["liste"].format(", ".join(v2))} '
                 'Bilinenler: ' + ' '.join(f'({j + 1}) {c[1]}' for j, c in enumerate(kos)))
        duzen = lambda d: ', '.join(f'{ad[x]}: {v1[d[0][x]]} – {v2[d[1][x]]}' for x in range(n))
        if tekil:
            d = ev.D[next(_bitler(Sm))]
            gerekce = 'Koşulları sağlayan tek eşleştirme: ' + duzen(d) + '.'
            # 1) belirli bir kişinin özelliği (kimin özelliği doğrudan verilmemişse)
            # Doğrudan verilen bilgi sorulmaz (kişi–değer koşulu olan kişi/değer atlanır).
            dogrudan = {(c[0][1], c[0][2]) for c in kos if c[0][0] in ('has', 'not')}
            dogrudan_deger = {(c[0][1], c[0][3]) for c in kos if c[0][0] == 'has'}
            secenek_x = [x for x in range(n) if (b2, x) not in dogrudan]
            if secenek_x:
                x = rng.choice(secenek_x)
                dv = v2[d[1][x]]
                yan = [v for v in v2 if v != dv]
                soru = {'meslek': f'Buna göre {gen[x]} mesleği nedir?',
                        'sehir': f'Buna göre {ad[x]} hangi şehre gitmiştir?',
                        'ulasim': f'Buna göre {ad[x]} hangi ulaşım aracıyla yolculuk etmiştir?'}[b2]
                out.append(q('esles_ozellik', 'Sözel Mantık', giris + ' ' + soru,
                             BOYUT[b2]['sec'](dv), [BOYUT[b2]['sec'](v) for v in yan[:4]], gerekce, 3))
            # 2) belirli bir değere sahip kişi kim?
            vi_aday = [i for i in range(n) if (b2, i) not in dogrudan_deger]
            if not vi_aday:
                continue
            vi = rng.choice(vi_aday)
            kim = [x for x in range(n) if d[1][x] == vi][0]
            yan = [ad[x] for x in range(n) if x != kim]
            out.append(q('esles_kim', 'Sözel Mantık', giris + f' Buna göre {_ozne_kucuk(b2, v2[vi])} kimdir?',
                         ad[kim], yan[:4], gerekce + f' {_ozne(b2, v2[vi])} {ad[kim]}.', 3))
            continue
        secenek = [a for a in atom if a[0][0] in ('has', 'link', 'link2')]
        tipler = ['kesin', 'kesin', 'yanlis', 'olabilir', 'kosul']
        rng.shuffle(tipler)
        alinan = set()
        for t in tipler:
            if t in alinan or len(alinan) >= 2:
                continue
            r = _soru_kur(rng, 'esles', giris, ev, kos, Sm, secenek, duzen, t)
            if r:
                out.append(r)
                alinan.add(t)
    return out
