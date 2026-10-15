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
