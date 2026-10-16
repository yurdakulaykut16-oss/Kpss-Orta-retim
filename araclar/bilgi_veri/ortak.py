"""Bilgi tablosu soru üreticileri için ortak yardımcılar."""

ROMA = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
        (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]


def roma(n):
    s = ''
    for v, r in ROMA:
        while n >= v:
            s += r
            n -= v
    return s


def yuzyil(y):
    return (y - 1) // 100 + 1


def yy_ad(c):
    return f'{roma(c)}. yüzyıl'


def sec(dogru, havuz, rng, n=4, haric=()):
    gor = {str(dogru).casefold(), *(str(h).casefold() for h in haric)}
    aday = []
    for h in havuz:
        if str(h).casefold() not in gor:
            gor.add(str(h).casefold())
            aday.append(h)
    if len(aday) < n:
        return None
    return rng.sample(aday, n)


def sec2(dogru, birincil, ikincil, rng, n=4, haric=()):
    """Önce birincil havuzdan (ör. aynı konu), yetmezse ikincil havuzdan seç."""
    gor = {str(dogru).casefold(), *(str(h).casefold() for h in haric)}
    aday = []
    for h in birincil:
        if str(h).casefold() not in gor:
            gor.add(str(h).casefold())
            aday.append(h)
    a = rng.sample(aday, min(n, len(aday)))
    if len(a) < n:
        b = sec(dogru, ikincil, rng, n - len(a), [*haric, *a])
        if b is None:
            return None
        a += b
    return a


def q(tur, konu, kok, dogru, yanlis, gerekce, z=2):
    if yanlis is None:
        return None
    return dict(tur=tur, konu=konu, kok=kok, dogru=str(dogru), yanlis=[str(x) for x in yanlis],
                gerekce=gerekce, z=z)


def eslesme(rng, tur, kayitlar, kok_ileri, kok_geri, ger_ileri, ger_geri, z=2, grup=None):
    """(anahtar, değer, konu) kayıtlarından iki yönlü soru üretir.

    Çeldiriciler önce aynı gruptan (grup fonksiyonu verilmişse), yetmezse tüm
    tablodan seçilir. Aynı değere sahip birden çok anahtar varsa geri yönde
    belirsizlik olmaması için o anahtarlar çeldirici yapılmaz.
    """
    out = []
    deger_say, anahtar_say = {}, {}
    for a, d, _ in kayitlar:
        deger_say.setdefault(d.casefold(), set()).add(a.casefold())
        anahtar_say.setdefault(a.casefold(), set()).add(d.casefold())
    for a, d, konu in kayitlar:
        g = grup(a, d, konu) if grup else None
        ayni = [x for x in kayitlar if grup and grup(*x) == g]
        tum = list(kayitlar)
        rng.shuffle(ayni)
        rng.shuffle(tum)
        if kok_ileri:
            yasak = anahtar_say[a.casefold()]
            b = [x[1] for x in ayni if x[1].casefold() not in yasak]
            i = [x[1] for x in tum if x[1].casefold() not in yasak]
            out.append(q(tur + '_ileri', konu, kok_ileri(a, d), d, sec2(d, b, i, rng), ger_ileri(a, d), z))
        if kok_geri:
            # Aynı değeri paylaşan anahtarlar çeldirici olamaz.
            yasak = deger_say[d.casefold()]
            b = [x[0] for x in ayni if x[0].casefold() not in yasak]
            i = [x[0] for x in tum if x[0].casefold() not in yasak]
            out.append(q(tur + '_geri', konu, kok_geri(a, d), a, sec2(a, b, i, rng), ger_geri(a, d), z))
    return out


# ------------------------------------------------------------------ akıl yürütme
# Aşağıdaki yardımcılar düz bilgi sorusunun yanında, seçeneklerin birbirine çok
# yakın olduğu (iki şık arasında bırakan) ama tek doğru cevabı olan soru kalıpları
# üretir: öncüllü (I-II-III), kronolojik/konumsal sıralama ve eşleştirme.
ONCUL = {'Yalnız I': {1}, 'Yalnız II': {2}, 'Yalnız III': {3}, 'I ve II': {1, 2}, 'I ve III': {1, 3},
         'II ve III': {2, 3}, 'I, II ve III': {1, 2, 3}}


def _yakin_oncul(dogru_set, rng):
    """Doğru kümeye en yakın (tek madde farklı) seçenekleri öne alır."""
    etiket = next(k for k, v in ONCUL.items() if v == dogru_set)
    digerleri = sorted((k for k in ONCUL if k != etiket),
                       key=lambda k: (len(ONCUL[k] ^ dogru_set), rng.random()))
    return etiket, digerleri[:4]


def onculu(rng, tur, konu, dogrular, yanlislar, soru, z=3, k=None, giris=''):
    """dogrular / yanlislar: (madde, açıklama) listeleri. 1-3 doğru madde seçilir.

    Doğru cevaba bir madde farkla yakın seçenekler çeldirici yapılır; böylece
    öğrenci genellikle iki seçenek arasında kalır, ama her maddenin doğruluğu
    tablodan kesin olarak bilindiği için tek cevap vardır.
    """
    k = k or rng.choice([1, 2, 2, 2, 3])
    dogrular = list({m: (m, a) for m, a in dogrular}.values())
    yanlislar = [x for x in {m: (m, a) for m, a in yanlislar}.values() if x[0] not in {m for m, _ in dogrular}]
    if len(dogrular) < k or len(yanlislar) < 3 - k:
        return None
    maddeler = [(m, a, True) for m, a in rng.sample(dogrular, k)] + \
               [(m, a, False) for m, a in rng.sample(yanlislar, 3 - k)]
    rng.shuffle(maddeler)
    dogru_set = {i + 1 for i, x in enumerate(maddeler) if x[2]}
    etiket, yan = _yakin_oncul(dogru_set, rng)
    kok = (giris + '\\n' if giris else '') + '\\n'.join(
        f'{roma(i + 1)}. {m}' for i, (m, _, _) in enumerate(maddeler)) + '\\n' + soru
    gerekce = ' '.join(f'{roma(i + 1)}. {"Doğru" if t else "Yanlış"}: {a}' for i, (_, a, t) in enumerate(maddeler))
    gerekce += f' Bu yüzden doğru cevap: {etiket}.'
    return q(tur, konu, kok, etiket, yan, gerekce, z)


def _kendall(a, b):
    pos = {x: i for i, x in enumerate(b)}
    s = [pos[x] for x in a]
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])


def siralama(rng, tur, konu, ogeler, soru, aciklama, z=3):
    """ogeler: (sıralama anahtarı, metin) — anahtarlar birbirinden farklı olmalı.

    Öğeler karışık numaralanır; doğru sıra ile ona en yakın (bir-iki yer
    değiştirmeli) sıralar seçenek yapılır.
    """
    from itertools import permutations
    if len({k for k, _ in ogeler}) != len(ogeler) or len(ogeler) not in (3, 4):
        return None
    ogeler = list(ogeler)
    rng.shuffle(ogeler)
    etiket = [roma(i + 1) for i in range(len(ogeler))]
    dogru_sira = tuple(etiket[i] for i in sorted(range(len(ogeler)), key=lambda i: ogeler[i][0]))
    perm = [p for p in permutations(etiket) if p != dogru_sira]
    perm.sort(key=lambda p: (_kendall(p, dogru_sira), rng.random()))
    yan = perm[:4]
    fmt = lambda p: ' – '.join(p)
    kok = '\\n'.join(f'{etiket[i]}. {m}' for i, (_, m) in enumerate(ogeler)) + '\\n' + soru
    gerekce = aciklama(sorted(ogeler)) + f' Doğru sıra: {fmt(dogru_sira)}.'
    return q(tur, konu, kok, fmt(dogru_sira), [fmt(p) for p in yan], gerekce, z)


def eslestirme(rng, tur, konu, ciftler, gecerli, mod, soru, ayrac=' – ', z=3, aciklama=None):
    """ciftler: aynı gruptan (birbirine yakın) en az 5 (anahtar, değer) çifti.

    mod='yanlis': dört çift doğru, biri 6. bir çiftin değeriyle bozulur
                  ("hangisi yanlıştır?"). En az 6 çift gerekir.
    mod='dogru' : bir çift doğru, diğer dördünün değerleri kendi aralarında
                  kaydırılır ("hangisi doğrudur?").
    gecerli(a, d) True ise d, a için de doğrudur (çeldirici yapılamaz).
    soru(anahtarlar) kökü üretir; kök, soru kökleri tekrarsız olsun diye
    seçeneklerdeki anahtarları içermelidir.
    """
    ciftler = list(ciftler)
    rng.shuffle(ciftler)
    aciklama = aciklama or (lambda a, d: f'{a}{ayrac}{d}')
    if mod == 'yanlis':
        if len(ciftler) < 6:
            return None
        bes, fazla = ciftler[:5], ciftler[5:]
        for j in range(5):
            a, d = bes[j]
            for _, w in fazla:
                if w != d and not gecerli(a, w):
                    dogru = f'{a}{ayrac}{w}'
                    yan = [f'{x}{ayrac}{y}' for i, (x, y) in enumerate(bes) if i != j]
                    ger = f'{aciklama(a, d)} olmalıdır; “{dogru}” eşleştirmesi yanlıştır. Diğer eşleştirmeler doğrudur: ' + \
                          '; '.join(aciklama(x, y) for i, (x, y) in enumerate(bes) if i != j) + '.'
                    return q(tur, konu, soru(sorted(x for x, _ in bes)), dogru, yan, ger, z)
        return None
    if len(ciftler) < 5:
        return None
    bes = ciftler[:5]
    j = rng.randrange(5)
    diger = [i for i in range(5) if i != j]
    kayik = diger[1:] + diger[:1]
    yan = []
    for i, s in zip(diger, kayik):
        a, w = bes[i][0], bes[s][1]
        if w == bes[i][1] or gecerli(a, w):
            return None
        yan.append(f'{a}{ayrac}{w}')
    dogru = f'{bes[j][0]}{ayrac}{bes[j][1]}'
    ger = f'Doğru eşleştirme: “{dogru}”. Diğerlerinin doğrusu: ' + \
          '; '.join(aciklama(*bes[i]) for i in diger) + '.'
    return q(tur, konu, soru(sorted(x for x, _ in bes)), dogru, yan, ger, z)
