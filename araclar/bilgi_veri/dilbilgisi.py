"""KPSS biçiminde dil bilgisi ve anlam soruları (numaralı cümle / öncüllü / ögelere ayırma).

Sorular, dilbilgisi_veri1..3.py içindeki elle denetlenmiş örneklerden kurulur.
Çıkmış KPSS sorularında olduğu gibi seçenekler tek tek bilgi değil, numaralı
cümleler ya da öncül kombinasyonlarıdır: öğrenci her cümleyi ayrı ayrı
değerlendirmek zorundadır. Yakın çeldiriciler bilerek seçilir:

- amaç-sonuç sorusunda "için"li neden-sonuç cümleleri,
- anlatım bozukluğu sorusunda doğrusu yazılmış "tuzak" cümleler,
- sözcük türü sorusunda aynı sözcüğün başka türde kullanıldığı cümleler,
- ögelere ayırma sorusunda tek ögesi kaydırılmış diziler (ör. dolaylı tümleç ↔ zarf tümleci).

Örnekler en az kullanılan önce seçilerek dağıtılır; böylece aynı cümle kısa
aralıklarla tekrar tekrar karşınıza çıkmaz.
"""
from collections import Counter
from itertools import product

from .ortak import q, roma, onculu
from . import dilbilgisi_veri1 as V1, dilbilgisi_veri2 as V2, dilbilgisi_veri3 as V3

NL = '\\n'
ROMA = [roma(i) for i in range(1, 6)]


def _satirlar(blok, n):
    out = []
    for line in blok.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = [x.strip() for x in line.split('|')]
        if len(p) != n:
            raise ValueError(f'{n} alan bekleniyordu: {line}')
        out.append(p)
    return out


class Havuz:
    """En az kullanılan örnekleri öne alan seçici."""

    def __init__(self, rng):
        self.rng = rng
        self.say = Counter()

    def sec(self, adaylar, n, anahtar, haric=frozenset(), grup=None, gruplar=None):
        gruplar = set(gruplar or ())
        sirali = sorted(adaylar, key=lambda x: (self.say[anahtar(x)], self.rng.random()))
        out = []
        for x in sirali:
            if anahtar(x) in haric:
                continue
            g = grup(x) if grup else None
            if g is not None and g in gruplar:
                continue
            out.append(x)
            if g is not None:
                gruplar.add(g)
            if len(out) == n:
                break
        if len(out) < n:
            return None
        for x in out:
            self.say[anahtar(x)] += 1
        return out


def _numarali(metinler):
    return NL.join(f'{ROMA[i]}. {m}' for i, m in enumerate(metinler))


def _tek(rng, tur, konu, hedef, digerleri, metin, soru, gerekce, z=3):
    """hedef + 4 diğer öğe; numaralı listede hedefin numarası doğru cevaptır."""
    ogeler = [hedef, *digerleri]
    rng.shuffle(ogeler)
    i = ogeler.index(hedef)
    kok = _numarali([metin(x) for x in ogeler]) + NL + soru
    return q(tur, konu, kok, ROMA[i], [r for j, r in enumerate(ROMA) if j != i], gerekce(ROMA[i], ogeler), z)


def _kucuk(s):
    return s.replace('İ', 'i').replace('I', 'ı').lower()


def _isaretli(c):
    return c.replace('[', '“').replace(']', '”')


def _isaretli_soz(c):
    return c[c.index('[') + 1:c.index(']')]


# ------------------------------------------------------------------ anlatım bozukluğu
def anlatim_bozuklugu(rng, H, adet):
    bozuk, dogru = [], []
    for p in V1.AB.strip().splitlines():
        p = p.strip()
        if p.startswith('B|'):
            _, t, c, d, a = [x.strip() for x in p.split('|')]
            bozuk.append(dict(c=c, t=t, d=d, a=a, g=d))
            dogru.append(dict(c=d, g=d))
        elif p.startswith('D|'):
            c = p[2:].strip()
            dogru.append(dict(c=c, g=c))
    K = lambda x: x['c']
    G = lambda x: x['g']
    out = []
    for _ in range(adet['ab_var']):
        h = H.sec(bozuk, 1, K, grup=G)
        d = h and H.sec(dogru, 4, K, grup=G, gruplar={h[0]['g']})
        if not d:
            continue
        b = h[0]
        out.append(_tek(rng, 'ab_var', 'Anlatım Bozuklukları', b, d, K,
                        'Numaralanmış cümlelerin hangisinde anlatım bozukluğu vardır?',
                        lambda r, o, b=b: f'{r} numaralı cümlede {_kucuk(V1.AB_TURLER[b["t"]])} vardır: {b["a"]} '
                                          f'Doğrusu: “{b["d"]}” Diğer cümleler dil bilgisi ve anlam bakımından doğrudur.'))
    for _ in range(adet['ab_yok']):
        h = H.sec(dogru, 1, K, grup=G)
        d = h and H.sec(bozuk, 4, K, grup=lambda x: x['t'], gruplar=set())
        if not d or any(x['g'] == h[0]['g'] for x in d):
            continue
        out.append(_tek(rng, 'ab_yok', 'Anlatım Bozuklukları', h[0], d, K,
                        'Numaralanmış cümlelerin hangisinde anlatım bozukluğu yoktur?',
                        lambda r, o: f'Bozukluk bulunmayan cümle {r} numaralı cümledir. ' + ' '.join(
                            f'{ROMA[i]}: {x["a"]}' for i, x in enumerate(o) if 't' in x)))
    for _ in range(adet['ab_neden']):
        h = H.sec(bozuk, 1, K)
        if not h:
            continue
        b = h[0]
        yasak = {b['t']} | set().union(*[s for s in V1.AB_KARISIR if b['t'] in s])
        diger = [V1.AB_TURLER[k] for k in V1.AB_TURLER if k not in yasak]
        rng.shuffle(diger)
        out.append(q('ab_neden', 'Anlatım Bozuklukları',
                     f'“{b["c"]}”{NL}Bu cümledeki anlatım bozukluğunun nedeni aşağıdakilerden hangisidir?',
                     V1.AB_TURLER[b['t']], diger[:4], f'{b["a"]} Doğrusu: “{b["d"]}”', 3))
    for _ in range(adet['ab_oncul']):
        k = rng.choice([1, 2, 2, 3])
        b = H.sec(bozuk, k, K, grup=G)
        d = b is not None and (H.sec(dogru, 3 - k, K, grup=G, gruplar={x['g'] for x in b}) if k < 3 else [])
        if b is None or d is None or d is False:
            continue
        out.append(onculu(rng, 'ab_oncul', 'Anlatım Bozuklukları',
                          [(x['c'], f'anlatım bozukluğu vardır; {x["a"]}') for x in b],
                          [(x['c'], 'anlatım bozukluğu yoktur.') for x in d],
                          'Yukarıdaki cümlelerin hangilerinde anlatım bozukluğu vardır?', 3, k))
    return out


# ------------------------------------------------------------------ cümlede anlam
YAKIN_ILISKI = {'AS': 'NS', 'NS': 'AS', 'KS': 'NS', 'KR': 'NS'}


def cumlede_anlam(rng, H, adet):
    il = [dict(t=t, c=c) for t, c in _satirlar(V1.ILISKI, 2)]
    an = [dict(t=t, c=c) for t, c in _satirlar(V1.ANLAM, 2)]
    oz = [dict(t=t, c=c) for t, c in _satirlar(V1.OZNEL, 2)]
    K = lambda x: x['c']
    out = []
    ad = V1.ILISKI_AD
    for _ in range(adet['il_var']):
        t = rng.choice(list(ad))
        h = H.sec([x for x in il if x['t'] == t], 1, K)
        yakin = H.sec([x for x in il if x['t'] == YAKIN_ILISKI[t]], 2, K)
        uzak = H.sec([x for x in il if x['t'] not in (t, YAKIN_ILISKI[t])], 2, K)
        if not (h and yakin and uzak):
            continue
        out.append(_tek(rng, 'il_var', 'Cümlede Anlam', h[0], yakin + uzak, K,
                        f'Numaralanmış cümlelerin hangisinde {ad[t]} ilişkisi vardır?',
                        lambda r, o, t=t: f'{r} numaralı cümlede {ad[t]} ilişkisi vardır. ' + ' '.join(
                            f'{ROMA[i]}: {ad[x["t"]]}.' for i, x in enumerate(o) if x['t'] != t)))
    for _ in range(adet['il_yok']):
        t = rng.choice(['NS', 'AS', 'KS'])
        h = H.sec([x for x in il if x['t'] != t], 1, K)
        d = H.sec([x for x in il if x['t'] == t], 4, K)
        if not (h and d):
            continue
        out.append(_tek(rng, 'il_yok', 'Cümlede Anlam', h[0], d, K,
                        f'Numaralanmış cümlelerin hangisinde {ad[t]} ilişkisi yoktur?',
                        lambda r, o, t=t, h=h[0]: f'{r} numaralı cümlede {ad[t]} değil {ad[h["t"]]} ilişkisi vardır; '
                                                    f'diğer cümlelerin hepsinde {ad[t]} ilişkisi kurulmuştur.'))
    for _ in range(adet['il_oncul']):
        t = rng.choice(['NS', 'AS', 'KS'])
        k = rng.choice([1, 2, 2, 3])
        b = H.sec([x for x in il if x['t'] == t], k, K)
        d = H.sec([x for x in il if x['t'] == YAKIN_ILISKI[t] or (t == 'NS' and x['t'] == 'AS')], 3 - k, K) if k < 3 else []
        if b is None or d is None:
            continue
        out.append(onculu(rng, 'il_oncul', 'Cümlede Anlam', [(x['c'], f'{ad[t]} ilişkisi vardır.') for x in b],
                          [(x['c'], f'{ad[x["t"]]} ilişkisi vardır, {ad[t]} değil.') for x in d],
                          f'Yukarıdaki cümlelerin hangilerinde {ad[t]} ilişkisi vardır?', 3, k))
    aa = V1.ANLAM_AD
    for _ in range(adet['an_var']):
        t = rng.choice(list(aa))
        h = H.sec([x for x in an if x['t'] == t], 1, K)
        d = H.sec([x for x in an if x['t'] != t], 4, K, grup=lambda x: x['t'])
        if not (h and d):
            continue
        out.append(_tek(rng, 'an_var', 'Cümlede Anlam', h[0], d, K,
                        f'Numaralanmış cümlelerin hangisinde {aa[t]} söz konusudur?',
                        lambda r, o, t=t: f'{r} numaralı cümlede {aa[t]} vardır. Diğerleri: ' + '; '.join(
                            f'{ROMA[i]} {aa[x["t"]]}' for i, x in enumerate(o) if x['t'] != t) + '.'))
    for _ in range(adet['an_etiket']):
        h = H.sec(an, 1, K)
        if not h:
            continue
        t = h[0]['t']
        diger = [v for k, v in aa.items() if k != t]
        rng.shuffle(diger)
        out.append(q('an_etiket', 'Cümlede Anlam',
                     f'“{h[0]["c"]}”{NL}Bu cümlede aşağıdakilerden hangisi ağır basmaktadır?',
                     aa[t][0].upper() + aa[t][1:], [x[0].upper() + x[1:] for x in diger[:4]],
                     f'Cümlede {aa[t]} anlamı ağır basmaktadır.', 3))
    for _ in range(adet['oz_nesnel']):
        h = H.sec([x for x in oz if x['t'] == 'N'], 1, K)
        d = H.sec([x for x in oz if x['t'] == 'O'], 4, K)
        if h and d:
            out.append(_tek(rng, 'oz_nesnel', 'Cümlede Anlam', h[0], d, K,
                            'Numaralanmış cümlelerin hangisinde nesnel bir yargı vardır?',
                            lambda r, o: f'{r} numaralı cümledeki yargı kanıtlanabilir, kişiden kişiye değişmez (nesnel). '
                                         'Diğer cümleler kişisel beğeni ve değerlendirme içerir (öznel).'))
    for _ in range(adet['oz_oznel']):
        h = H.sec([x for x in oz if x['t'] == 'O'], 1, K)
        d = H.sec([x for x in oz if x['t'] == 'N'], 4, K)
        if h and d:
            out.append(_tek(rng, 'oz_oznel', 'Cümlede Anlam', h[0], d, K,
                            'Numaralanmış cümlelerin hangisinde öznel bir yargı vardır?',
                            lambda r, o: f'{r} numaralı cümle kişisel bir değerlendirme içerir, kanıtlanamaz (öznel). '
                                         'Diğer cümlelerdeki bilgiler doğruluğu araştırılabilir nesnel yargılardır.'))
    for _ in range(adet['oz_oncul']):
        k = rng.choice([1, 2, 2, 3])
        b = H.sec([x for x in oz if x['t'] == 'N'], k, K)
        d = H.sec([x for x in oz if x['t'] == 'O'], 3 - k, K) if k < 3 else []
        if b is None or d is None:
            continue
        out.append(onculu(rng, 'oz_oncul', 'Cümlede Anlam', [(x['c'], 'nesnel yargıdır.') for x in b],
                          [(x['c'], 'kişisel değerlendirme içerdiği için öznel yargıdır.') for x in d],
                          'Yukarıdaki cümlelerden hangileri nesnel bir yargı bildirir?', 3, k))
    return out


# ------------------------------------------------------------------ yazım
def yazim(rng, H, adet):
    yanlis, dogru = [], []
    for p in V2.YAZIM.strip().splitlines():
        p = p.strip()
        if p.startswith('W|'):
            _, c, d, a = [x.strip() for x in p.split('|')]
            yanlis.append(dict(c=c, d=d, a=a, g=d))
        elif p.startswith('C|'):
            c = p[2:].strip()
            dogru.append(dict(c=c, g=c))
    K, G = (lambda x: x['c']), (lambda x: x['g'])
    out = []
    for _ in range(adet['yz_var']):
        h = H.sec(yanlis, 1, K, grup=G)
        d = h and H.sec(dogru, 4, K, grup=G, gruplar={h[0]['g']})
        if d:
            w = h[0]
            out.append(_tek(rng, 'yz_var', 'Yazım', w, d, K, 'Numaralanmış cümlelerin hangisinde yazım yanlışı vardır?',
                            lambda r, o, w=w: f'{r} numaralı cümlede yazım yanlışı vardır: {w["a"]} Doğrusu: “{w["d"]}” '
                                              'Diğer cümlelerin yazımı doğrudur.'))
    for _ in range(adet['yz_yok']):
        h = H.sec(dogru, 1, K, grup=G)
        d = h and H.sec(yanlis, 4, K, grup=G, gruplar={h[0]['g']})
        if d:
            out.append(_tek(rng, 'yz_yok', 'Yazım', h[0], d, K, 'Numaralanmış cümlelerin hangisinde yazım yanlışı yoktur?',
                            lambda r, o: f'Yazımı doğru olan cümle {r} numaralı cümledir. ' + ' '.join(
                                f'{ROMA[i]}: {x["a"]}' for i, x in enumerate(o) if 'a' in x)))
    for _ in range(adet['yz_oncul']):
        k = rng.choice([1, 2, 2, 3])
        b = H.sec(yanlis, k, K, grup=G)
        d = (H.sec(dogru, 3 - k, K, grup=G, gruplar={x['g'] for x in b}) if k < 3 else []) if b else None
        if b is None or d is None:
            continue
        out.append(onculu(rng, 'yz_oncul', 'Yazım', [(x['c'], f'yazım yanlışı vardır; {x["a"]}') for x in b],
                          [(x['c'], 'yazımı doğrudur.') for x in d],
                          'Yukarıdaki cümlelerin hangilerinde yazım yanlışı vardır?', 3, k))
    return out


# ------------------------------------------------------------------ noktalama
NK_SORU = {
    'V_ES': ('virgül (,)', 'eş görevli sözcükleri ayırmak için kullanılmıştır'),
    'V_SIR': ('virgül (,)', 'sıralı cümleleri birbirinden ayırmak için kullanılmıştır'),
    'V_HIT': ('virgül (,)', 'hitap sözünden sonra kullanılmıştır'),
    'V_OZN': ('virgül (,)', 'yüklemden uzaktaki özneyi belirtmek için kullanılmıştır'),
    'V_ARA': ('virgül (,)', 'ara sözü cümleden ayırmak için kullanılmıştır'),
    'V_EVT': ('virgül (,)', '“evet, hayır, peki” gibi sözlerden sonra kullanılmıştır'),
    'NV': ('noktalı virgül (;)', 'bağlaçla bağlanan cümleleri ayırmak için kullanılmıştır'),
    'IN_ACK': ('iki nokta (:)', 'kendisinden sonra açıklama yapılacak sözden önce kullanılmıştır'),
    'IN_KON': ('iki nokta (:)', 'karşılıklı konuşmada konuşanın adından sonra kullanılmıştır'),
    'K_OZ': ('kesme işareti (’)', 'özel ada getirilen eki ayırmak için kullanılmıştır'),
    'K_KIS': ('kesme işareti (’)', 'kısaltmaya getirilen eki ayırmak için kullanılmıştır'),
    'K_SAY': ('kesme işareti (’)', 'sayıya getirilen eki ayırmak için kullanılmıştır'),
    'T_ALI': ('tırnak işareti (“ ”)', 'başkasından olduğu gibi aktarılan sözü göstermek için kullanılmıştır'),
    'T_VUR': ('tırnak işareti (“ ”)', 'özellikle belirtilmek istenen sözü göstermek için kullanılmıştır'),
    'T_ESR': ('tırnak işareti (“ ”)', 'eser adını göstermek için kullanılmıştır'),
    'SI': ('ayraç içindeki soru işareti', 'bilginin kesin olmadığını belirtmek için kullanılmıştır'),
    'UN': ('ayraç içindeki ünlem işareti', 'alay ya da küçümseme anlamı katmak için kullanılmıştır'),
    'KC': ('kısa çizgi (-)', '“arasında, ile” anlamı vermek için kullanılmıştır'),
}


def noktalama(rng, H, adet):
    nk = [dict(t=t, c=c) for t, c in _satirlar(V2.NOKTALAMA, 2)]
    K = lambda x: x['c']
    ad = V2.NOKTALAMA_GOREV
    out = []
    for _ in range(adet['nk_gorev']):
        t = rng.choice(list(NK_SORU))
        isaret = NK_SORU[t][0]
        h = H.sec([x for x in nk if x['t'] == t], 1, K)
        ayni = [x for x in nk if x['t'] != t and NK_SORU[x['t']][0] == isaret]
        y1 = H.sec(ayni, min(2, len({x['t'] for x in ayni})), K, grup=lambda x: x['t']) if ayni else []
        y2 = H.sec([x for x in nk if NK_SORU[x['t']][0] != isaret], 4 - len(y1 or []), K, grup=lambda x: x['t'])
        if not h or y1 is None or not y2:
            continue
        out.append(_tek(rng, 'nk_gorev', 'Noktalama', h[0], (y1 or []) + y2, K,
                        f'Numaralanmış cümlelerin hangisinde {isaret} {NK_SORU[t][1]}?',
                        lambda r, o: f'Doğru cevap {r}. ' + ' '.join(f'{ROMA[i]}: {ad[x["t"]]}.' for i, x in enumerate(o))))
    virgul = [k for k in NK_SORU if k.startswith('V_')]
    for _ in range(adet['nk_islev']):
        h = H.sec([x for x in nk if x['t'] in virgul], 1, K)
        if not h:
            continue
        t = h[0]['t']
        diger = [ad[k].split(' — ')[1] for k in virgul if k != t]
        rng.shuffle(diger)
        dogru = ad[t].split(' — ')[1]
        out.append(q('nk_islev', 'Noktalama', f'“{h[0]["c"]}”{NL}Bu cümlede virgülün kullanılma amacı aşağıdakilerden hangisidir?',
                     dogru[0].upper() + dogru[1:], [x[0].upper() + x[1:] for x in diger[:4]], f'{ad[t]}.', 3))
    return out


# ------------------------------------------------------------------ cümle ögeleri
OGE_YAKIN = {'Ö': ['N'], 'N': ['Ö', 'DT'], 'DT': ['ZT', 'N'], 'ZT': ['DT'], 'Y': []}


def _oge_cumle(parcalar):
    m = ' '.join(t for t, _ in parcalar)
    return m[0].upper() + m[1:] + '.' if m[0] != 'İ' else m + '.'


def cumle_ogeleri(rng, H, adet):
    cumleler = []
    for line in V2.OGE.strip().splitlines():
        parcalar = [tuple(x.strip().rsplit('/', 1)) for x in line.split(' | ')]
        cumleler.append(parcalar)
    K = lambda p: _oge_cumle(p)
    ad = V2.OGE_AD
    dizi = lambda etiketler: ' – '.join(ad[e] for e in etiketler)
    out = []
    for _ in range(adet['og_dizilis']):
        h = H.sec(cumleler, 1, K)
        if not h:
            continue
        p = h[0]
        et = [e for _, e in p]
        adaylar = set()
        for i, e in enumerate(et):
            for a in OGE_YAKIN[e]:
                adaylar.add(tuple(et[:i] + [a] + et[i + 1:]))
        for i, j in product(range(len(et)), repeat=2):
            if i < j:
                for a, b in product(OGE_YAKIN[et[i]], OGE_YAKIN[et[j]]):
                    yeni = list(et)
                    yeni[i], yeni[j] = a, b
                    adaylar.add(tuple(yeni))
        adaylar.discard(tuple(et))
        adaylar = {a for a in adaylar if a.count('Ö') <= 1 and a.count('N') <= 1}
        adaylar = sorted(adaylar)
        if len(adaylar) < 4:
            continue
        rng.shuffle(adaylar)
        tekli = [a for a in adaylar if sum(x != y for x, y in zip(a, et)) == 1]
        ciftli = [a for a in adaylar if a not in tekli]
        sec = (tekli[:3] + ciftli)[:4] if len(tekli) >= 2 else adaylar[:4]
        if len(sec) < 4:
            continue
        out.append(q('og_dizilis', 'Cümle Ögeleri',
                     f'“{K(p)}”{NL}Bu cümlenin ögeleri sırasıyla aşağıdakilerin hangisinde doğru verilmiştir?',
                     dizi(et), [dizi(a) for a in sec],
                     'Ögeler: ' + '; '.join(f'“{t}” → {_kucuk(ad[e])}' for t, e in p) + '.', 3))
    sorular = {'DT': 'dolaylı tümleç yoktur', 'ZT': 'zarf tümleci yoktur', 'N': 'nesne yoktur',
               'Ö': 'özne gizlidir (cümlede söylenmemiştir)'}
    for _ in range(adet['og_yok']):
        e = rng.choice(list(sorular))
        h = H.sec([p for p in cumleler if e not in [x for _, x in p]], 1, K)
        d = H.sec([p for p in cumleler if e in [x for _, x in p]], 4, K)
        if not (h and d):
            continue
        out.append(_tek(rng, 'og_yok', 'Cümle Ögeleri', h[0], d, K, f'Numaralanmış cümlelerin hangisinde {sorular[e]}?',
                        lambda r, o, e=e: f'{r} numaralı cümlede {_kucuk(ad[e])} bulunmaz. ' + ' '.join(
                            f'{ROMA[i]}: ' + ', '.join(f'“{t}” {_kucuk(ad[x])}' for t, x in p if x == e) + '.'
                            for i, p in enumerate(o) if e in [x for _, x in p])))
    for _ in range(adet['og_var']):
        a, b = rng.choice([('N', 'DT'), ('N', 'ZT'), ('DT', 'ZT'), ('Ö', 'N')])
        var = lambda p, e: e in [x for _, x in p]
        h = H.sec([p for p in cumleler if var(p, a) and var(p, b)], 1, K)
        d = H.sec([p for p in cumleler if var(p, a) != var(p, b)], 4, K)
        if not (h and d):
            continue
        out.append(_tek(rng, 'og_var', 'Cümle Ögeleri', h[0], d, K,
                        f'Numaralanmış cümlelerin hangisinde hem {_kucuk(ad[a])} hem de {_kucuk(ad[b])} vardır?',
                        lambda r, o, a=a, b=b: f'{r} numaralı cümlede ikisi de vardır: ' + ', '.join(
                            f'“{t}” {_kucuk(ad[x])}' for t, x in o[ROMA.index(r)] if x in (a, b)) +
                            '. Diğer cümlelerde bu iki ögeden yalnız biri bulunur.'))
    return out


# ------------------------------------------------------------------ cümle türleri
def _karisik(H, a, b, K):
    """İki özellikten yalnız birini taşıyan cümlelerden, mümkünse ikişer tane."""
    na = min(2, len(a)) if len(b) >= 2 else 4 - min(len(b), 4)
    x = H.sec(a, na, K) if na else []
    y = H.sec(b, 4 - na, K) if x is not None else None
    return (x + y) if x is not None and y is not None else None


YUKLEM_AD = {'F': 'fiil cümlesi', 'I': 'isim cümlesi'}


def cumle_turleri(rng, H, adet):
    ct = [dict(y=y, yp=yp, d=d, a=a, c=c) for y, yp, d, a, c in _satirlar(V2.CUMLE_TURU, 5)]
    K = lambda x: x['c']
    ozet = lambda x: f'{"isim" if x["y"] == "I" else "fiil" if x["y"] == "F" else "karma yüklemli"}, {_kucuk(x["yp"])}, ' \
                     f'{_kucuk(x["d"])}' + (f', {_kucuk(x["a"])}' if x['a'] != '-' else '')
    out = []
    yapilar = ['Basit', 'Birleşik', 'Sıralı', 'Bağlı']
    for _ in range(adet['ct_farkli']):
        y = rng.choice(yapilar)
        d = H.sec([x for x in ct if x['yp'] == y], 4, K)
        h = H.sec([x for x in ct if x['yp'] != y], 1, K)
        if not (h and d):
            continue
        out.append(_tek(rng, 'ct_farkli', 'Cümle Türleri', h[0], d, K,
                        'Numaralanmış cümlelerden hangisi yapısı bakımından diğerlerinden farklıdır?',
                        lambda r, o, y=y, h=h[0]: f'{r} numaralı cümle yapıca {_kucuk(h["yp"])} cümledir; diğerleri '
                                                    f'{_kucuk(y)} cümledir. ' + ' '.join(f'{ROMA[i]}: {ozet(x)}.' for i, x in enumerate(o))))
    for _ in range(adet['ct_iki']):
        yk, yp = rng.choice(['F', 'I']), rng.choice(yapilar)
        tam = [x for x in ct if x['y'] == yk and x['yp'] == yp]
        h = H.sec(tam, 1, K)
        d = _karisik(H, [x for x in ct if x['y'] == yk and x['yp'] != yp],
                     [x for x in ct if x['y'] not in (yk, '-') and x['yp'] == yp], K)
        if not (h and d):
            continue
        out.append(_tek(rng, 'ct_iki', 'Cümle Türleri', h[0], d, K,
                        f'Numaralanmış cümlelerden hangisi hem {YUKLEM_AD[yk]} hem de yapıca {_kucuk(yp)} bir cümledir?',
                        lambda r, o: ' '.join(f'{ROMA[i]}: {ozet(x)}.' for i, x in enumerate(o))))
    for _ in range(adet['ct_dizanl']):
        dz, an = rng.choice(['Kurallı', 'Devrik']), rng.choice(['Olumlu', 'Olumsuz', 'Soru'])
        uygun = [x for x in ct if x['a'] != '-']
        h = H.sec([x for x in uygun if x['d'] == dz and x['a'] == an], 1, K)
        d = _karisik(H, [x for x in uygun if x['d'] == dz and x['a'] != an],
                     [x for x in uygun if x['d'] != dz and x['a'] == an], K)
        if not (h and d):
            continue
        anl = {'Olumlu': 'olumlu', 'Olumsuz': 'olumsuz', 'Soru': 'soru'}[an]
        out.append(_tek(rng, 'ct_dizanl', 'Cümle Türleri', h[0], d, K,
                        f'Numaralanmış cümlelerden hangisi hem {_kucuk(dz)} hem de {anl} bir cümledir?',
                        lambda r, o: ' '.join(f'{ROMA[i]}: {ozet(x)}.' for i, x in enumerate(o))))
    return out


# ------------------------------------------------------------------ sözcük türleri, yapı
def sozcuk_turu_yapi(rng, H, adet):
    st = [dict(t=t, c=c, s=_isaretli_soz(c).casefold()) for t, c in _satirlar(V3.SOZCUK_TURU, 2)]
    K = lambda x: x['c']
    M = lambda x: _isaretli(x['c'])
    out = []
    turler = sorted({x['t'] for x in st})
    for _ in range(adet['st_var']):
        t = rng.choice([x for x in turler if sum(1 for y in st if y['t'] == x) >= 2])
        h = H.sec([x for x in st if x['t'] == t], 1, K)
        if not h:
            continue
        ayni_soz = [x for x in st if x['t'] != t and x['s'][:4] == h[0]['s'][:4]]
        y1 = H.sec(ayni_soz, min(1, len(ayni_soz)), K) or []
        y2 = H.sec([x for x in st if x['t'] != t and x not in y1], 4 - len(y1), K,
                   grup=lambda x: x['s'], gruplar={h[0]['s']} | {x['s'] for x in y1})
        if not y2:
            continue
        out.append(_tek(rng, 'st_var', 'sozcuk_turu', h[0], y1 + y2, M,
                        f'Numaralanmış cümlelerin hangisinde tırnak içindeki sözcük {_kucuk(t)} olarak kullanılmıştır?',
                        lambda r, o: ' '.join(f'{ROMA[i]}: “{_isaretli_soz(x["c"])}” {_kucuk(x["t"])}.' for i, x in enumerate(o))))
    for _ in range(adet['st_farkli']):
        t = rng.choice([x for x in turler if sum(1 for y in st if y['t'] == x) >= 4])
        d = H.sec([x for x in st if x['t'] == t], 4, K, grup=lambda x: x['s'])
        h = d and H.sec([x for x in st if x['t'] != t], 1, K, grup=lambda x: x['s'], gruplar={x['s'] for x in d})
        if not (h and d):
            continue
        out.append(_tek(rng, 'st_farkli', 'sozcuk_turu', h[0], d, M,
                        'Numaralanmış cümlelerde tırnak içindeki sözcüklerden hangisi türü bakımından diğerlerinden farklıdır?',
                        lambda r, o: ' '.join(f'{ROMA[i]}: “{_isaretli_soz(x["c"])}” {_kucuk(x["t"])}.' for i, x in enumerate(o))))
    yp = [dict(t=t, s=s) for t, s in _satirlar(V3.YAPI, 2)]
    KS = lambda x: x['s']
    ad = V3.YAPI_AD
    for _ in range(adet['yp_farkli']):
        t = rng.choice(list(ad))
        d = H.sec([x for x in yp if x['t'] == t], 4, KS)
        h = H.sec([x for x in yp if x['t'] != t], 1, KS)
        if not (h and d):
            continue
        out.append(_tek(rng, 'yp_farkli', 'Yapı Bilgisi', h[0], d, KS,
                        'Yukarıdaki sözcüklerden hangisi yapı bakımından diğerlerinden farklıdır?',
                        lambda r, o, t=t, h=h[0]: f'{r} numaralı “{h["s"]}” {ad[h["t"]]} bir sözcüktür; diğer sözcüklerin hepsi {ad[t]} yapılıdır. '
                                                    + ' '.join(f'{x["s"]}: {ad[x["t"]]}.' for x in o)))
    for _ in range(adet['yp_hangisi']):
        t = rng.choice(['Bİ', 'T'])
        h = H.sec([x for x in yp if x['t'] == t], 1, KS)
        d = H.sec([x for x in yp if x['t'] != t], 4, KS)
        if not (h and d):
            continue
        out.append(_tek(rng, 'yp_hangisi', 'Yapı Bilgisi', h[0], d, KS,
                        f'Yukarıdaki sözcüklerden hangisi yapıca {ad[t]} bir sözcüktür?',
                        lambda r, o: ' '.join(f'{x["s"]}: {ad[x["t"]]}.' for x in o)))
    return out


# ------------------------------------------------------------------ ses, fiilimsi, sözcükte anlam
def ses_fiilimsi_anlam(rng, H, adet, ses, fiilimsi, fiilimsi_tur, deyimler, atasozleri, es, zit):
    out = []
    S = [dict(s=s, o=o) for s, o in ses]
    KS = lambda x: x['s']
    olaylar = sorted({x['o'] for x in S})
    for _ in range(adet['ses_yok']):
        o = rng.choice([x for x in olaylar if sum(1 for y in S if y['o'] == x) >= 4])
        d = H.sec([x for x in S if x['o'] == o], 4, KS)
        h = H.sec([x for x in S if x['o'] != o], 1, KS)
        if not (h and d):
            continue
        out.append(_tek(rng, 'ses_yok', 'Ses Bilgisi', h[0], d, KS,
                        f'Yukarıdaki sözcüklerin hangisinde {_kucuk(o)} görülmez?',
                        lambda r, o_, o=o, h=h[0]: f'{r} numaralı “{h["s"]}” sözcüğünde {_kucuk(h["o"])} vardır; diğer '
                                                     f'sözcüklerin hepsinde {_kucuk(o)} görülür.'))
    F = []
    for t, c in fiilimsi:
        F.append(dict(t=t, c=c, s=_isaretli_soz(c)))
    KF = lambda x: x['c']
    MF = lambda x: _isaretli(x['c'])
    for _ in range(adet['fm_farkli']):
        t = rng.choice(list(fiilimsi_tur))
        d = H.sec([x for x in F if x['t'] == t], 4, KF)
        h = H.sec([x for x in F if x['t'] != t], 1, KF)
        if not (h and d):
            continue
        out.append(_tek(rng, 'fm_farkli', 'Fiilimsi', h[0], d, MF,
                        'Numaralanmış cümlelerde tırnak içindeki fiilimsilerden hangisi türü bakımından diğerlerinden farklıdır?',
                        lambda r, o: ' '.join(f'“{x["s"]}” {_kucuk(fiilimsi_tur[x["t"]])}.' for x in o)))
    for _ in range(adet['fm_var']):
        t = rng.choice(list(fiilimsi_tur))
        h = H.sec([x for x in F if x['t'] == t], 1, KF)
        d = H.sec([x for x in F if x['t'] != t], 4, KF)
        if not (h and d):
            continue
        ad = fiilimsi_tur[t]
        out.append(_tek(rng, 'fm_var', 'Fiilimsi', h[0], d, lambda x: x['c'].replace('[', '').replace(']', ''),
                        f'Numaralanmış cümlelerin hangisinde {_kucuk(ad)} kullanılmıştır?',
                        lambda r, o: ' '.join(f'{ROMA[i]}: “{x["s"]}” {_kucuk(fiilimsi_tur[x["t"]])}.' for i, x in enumerate(o))))
    MZ = [dict(t=t, w=w, c=c) for t, w, c in _satirlar(V3.MECAZ, 3)]
    for tur, hedef, ad in (('mz_mecaz', 'M', 'mecaz'), ('mz_gercek', 'G', 'gerçek')):
        for _ in range(adet[tur]):
            h = H.sec([x for x in MZ if x['t'] == hedef], 1, KF)
            d = h and H.sec([x for x in MZ if x['t'] != hedef], 4, KF, grup=lambda x: x['w'], gruplar={h[0]['w']})
            if not d:
                continue
            out.append(_tek(rng, tur, 'Sözcükte Anlam', h[0], d, MF,
                            f'Numaralanmış cümlelerde tırnak içindeki sözcüklerden hangisi {ad} anlamıyla kullanılmıştır?',
                            lambda r, o: ' '.join(f'{ROMA[i]}: “{_isaretli_soz(x["c"])}” '
                                                  f'{"mecaz" if x["t"] == "M" else "gerçek"} anlamda.' for i, x in enumerate(o))))
    for tur, rows, adi, n_ in (('deyim_oncul', deyimler, 'deyim', adet['deyim_oncul']),
                               ('atasozu_oncul', atasozleri, 'atasözü', adet['atasozu_oncul'])):
        KD = lambda x: x[0]
        for _ in range(n_):
            k = rng.choice([1, 2, 2, 3])
            uc = H.sec(rows, 3, KD, grup=lambda x: x[2])
            if not uc:
                continue
            d = [(f'“{a}”: {m}', f'“{a}” {m} anlamındadır.') for a, m, e in uc[:k]]
            w = []
            for a, m, e in uc[k:]:
                baska = [r for r in rows if r[2] != e and r[0] != a]
                b = rng.choice(baska)
                w.append((f'“{a}”: {b[1]}', f'“{a}” “{b[1]}” değil, {m} anlamındadır.'))
            out.append(onculu(rng, tur, 'Sözcükte Anlam', d, w,
                              f'Yukarıdaki {adi} – anlam eşleştirmelerinden hangileri doğrudur?', 3, k))
    for _ in range(adet['eszit_oncul']):
        k = rng.choice([1, 2, 2, 3])
        hedef_es = rng.random() < 0.5
        dogru_rows, yanlis_rows = (es, zit) if hedef_es else (zit, es)
        d = H.sec(dogru_rows, k, lambda x: x[0])
        w = H.sec(yanlis_rows, 3 - k, lambda x: x[0]) if k < 3 else []
        if d is None or w is None:
            continue
        ad, karsi = ('eş', 'zıt') if hedef_es else ('zıt', 'eş')
        out.append(onculu(rng, 'eszit_oncul', 'Sözcükte Anlam',
                          [(f'{a} – {b}', f'“{a}” ile “{b}” {ad} anlamlıdır.') for a, b, _ in d],
                          [(f'{a} – {b}', f'“{a}” ile “{b}” {karsi} anlamlıdır.') for a, b, _ in w],
                          f'Yukarıdaki sözcük çiftlerinden hangileri {ad} anlamlıdır?', 3, k))
    return out


def dilbilgisi_sorulari(rng, adet, ses, fiilimsi, fiilimsi_tur, deyimler, atasozleri, es, zit):
    """adet: tür → üretim denemesi sayısı (KOTA'dan biraz fazla verilir; fazlası seçimde elenir)."""
    H = Havuz(rng)
    out = []
    out += anlatim_bozuklugu(rng, H, adet)
    out += cumlede_anlam(rng, H, adet)
    out += yazim(rng, H, adet)
    out += noktalama(rng, H, adet)
    out += cumle_ogeleri(rng, H, adet)
    out += cumle_turleri(rng, H, adet)
    out += sozcuk_turu_yapi(rng, H, adet)
    out += ses_fiilimsi_anlam(rng, H, adet, ses, fiilimsi, fiilimsi_tur, deyimler, atasozleri, es, zit)
    return [x for x in out if x]
