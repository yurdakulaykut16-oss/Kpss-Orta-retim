"""Özgün paragraflardan KPSS tipi paragraf soruları.

Paragraf metinleri paragraf_metin1..4.py dosyalarında şu blok biçimiyle tutulur:

    @ alan | konu | yakın ama yanlış konu
    1 .. 5      : paragrafın beş cümlesi (sırasıyla)
    A <no> | <ana düşünce>   : ana düşünceyi taşıyan TEK cümlenin numarası ve özeti
    Y <yargı>   : konuyla ilgili ama parçayla çelişen / parçadan çıkarılamayan güçlü çeldirici
    D d1 / d2 / d3 : parçada geçen yardımcı düşünceler (doğru ama ana düşünce olmayan)
    N <yargı>   : konuyla ilgili ama parçada DEĞİNİLMEYEN bilgi
    B <cümle>   : konuyu değiştiren, hangi konuma girse akışı bozan cümle

Her paragraftan yedi farklı soru kökü üretilir: konu, ana düşünce, ana düşünce
cümlesi, değinilmeyen, çıkarılamayan, akışı bozan cümle ve boşluk doldurma.
Çeldiriciler bilinçli olarak "iki şık arasında" bırakacak biçimde seçilir
(yakın konu, parçayla çelişen yakın yargı, parçada geçen yardımcı düşünceler).
"""
from .ortak import q, roma
from . import paragraf_metin1, paragraf_metin2, paragraf_metin3, paragraf_metin4

KONU = 'Paragraf'
NL = '\\n'


def paragraflar():
    out = []
    for mod in (paragraf_metin1, paragraf_metin2, paragraf_metin3, paragraf_metin4):
        p = None
        for satir in mod.METIN.splitlines():
            satir = satir.strip()
            if not satir:
                continue
            bas, _, govde = satir.partition(' ')
            govde = govde.strip()
            if bas == '@':
                alan, konu, yakin = [x.strip() for x in govde.split('|')]
                p = dict(alan=alan, konu=konu, yakin=yakin, c={})
                out.append(p)
            elif bas.isdigit():
                p['c'][int(bas)] = govde
            elif bas == 'A':
                no, ana = govde.split('|', 1)
                p['ana_no'], p['ana'] = int(no), ana.strip()
            elif bas == 'Y':
                p['y'] = govde
            elif bas == 'D':
                p['d'] = [x.strip() for x in govde.split(' / ')]
            elif bas == 'N':
                p['n'] = govde
            elif bas == 'B':
                p['b'] = govde
            else:
                raise ValueError('Tanınmayan paragraf satırı: ' + satir)
    for p in out:
        p['cumleler'] = [p['c'][i] for i in range(1, 6)]
        assert len(p['d']) == 3 and 1 <= p['ana_no'] <= 5, p['konu']
        for k in ('y', 'n', 'b'):
            assert p.get(k), (p['konu'], k)
    konular = [p['konu'].casefold() for p in out]
    assert len(set(konular)) == len(konular), 'Aynı konulu iki paragraf var'
    return out


def _metin(cumleler):
    return ' '.join(cumleler)


def _numarali(cumleler, ilk_numarasiz=False):
    parca = []
    n = 0
    for i, c in enumerate(cumleler):
        if ilk_numarasiz and i == 0:
            parca.append(c)
        else:
            n += 1
            parca.append(f'({roma(n)}) {c}')
    return ' '.join(parca)


def _kisa(c, n=60):
    return c if len(c) <= n else c[:n].rsplit(' ', 1)[0] + '…'


def paragraf_sorulari(rng):
    ps = paragraflar()
    out = []
    romalar = [roma(i) for i in range(1, 6)]
    for p in ps:
        cs = p['cumleler']
        metin = _metin(cs)
        baska = [x for x in ps if x['alan'] != p['alan']]

        # 1) Konu: yakın konu + farklı alanlardan konular
        diger = rng.sample([x['konu'] for x in baska], 3)
        out.append(q('par_konu', KONU, f'{metin}{NL}Bu parçanın konusu aşağıdakilerden hangisidir?',
                     p['konu'], [p['yakin'], *diger],
                     f'Parçada baştan sona “{p["konu"]}” işlenmiştir. “{p["yakin"]}” seçeneği konuya yakın görünse de '
                     f'parçada bu konu ele alınmamıştır; diğer seçenekler parçayla ilgisizdir.', 2))

        # 2) Ana düşünce: parçayla çelişen yakın yargı + parçada geçen yardımcı düşünceler
        out.append(q('par_ana', KONU, f'{metin}{NL}Bu parçada asıl anlatılmak istenen aşağıdakilerden hangisidir?',
                     p['ana'], [p['y'], *p['d']],
                     f'Parçanın ana düşüncesi {roma(p["ana_no"])}. cümlede (“{_kisa(cs[p["ana_no"] - 1])}”) verilmiştir: '
                     f'{p["ana"]} “{p["y"]}” yargısı parçada savunulmaz; diğer seçenekler parçada geçen ama '
                     f'ana düşünceyi desteklemekle kalan yardımcı düşüncelerdir.', 3))

        # 3) Ana düşünce cümlesi
        out.append(q('par_cumle', KONU,
                     f'{_numarali(cs)}{NL}Bu parçada ana düşünce numaralanmış cümlelerin hangisinde verilmiştir?',
                     romalar[p['ana_no'] - 1], [r for r in romalar if r != romalar[p['ana_no'] - 1]],
                     f'{roma(p["ana_no"])} numaralı cümle parçanın ana düşüncesini (“{p["ana"]}”) verir; diğer cümleler '
                     f'bu düşünceyi açıklayan, örnekleyen ya da destekleyen yardımcı cümlelerdir.', 3))

        # 4) Değinilmeyen
        out.append(q('par_degin', KONU, f'{metin}{NL}Bu parçada aşağıdakilerden hangisine değinilmemiştir?',
                     p['n'], [p['ana'], *p['d']],
                     f'“{p["n"]}” bilgisi konuyla ilgili görünse de parçada yer almaz. Diğer seçeneklerin '
                     f'hepsi parçada doğrudan ya da ana düşünce olarak dile getirilmiştir.', 3))

        # 5) Çıkarılamayan
        out.append(q('par_cikar', KONU, f'{metin}{NL}Bu parçadan aşağıdaki yargılardan hangisine ulaşılamaz?',
                     p['y'], [p['ana'], *p['d']],
                     f'“{p["y"]}” yargısı parçada savunulan düşünceyle bağdaşmaz; parça bu yargıyı desteklemez. '
                     f'Diğer yargıların hepsi parçadan çıkarılabilir.', 3))

        # 6) Akışı bozan cümle: ilk cümle numarasız, B rastgele konuma girer
        konum = rng.randrange(5)
        govde = cs[1:]
        govde = govde[:konum] + [p['b']] + govde[konum:]
        out.append(q('par_akis', KONU,
                     f'{_numarali([cs[0], *govde], ilk_numarasiz=True)}{NL}'
                     f'Bu parçada numaralanmış cümlelerden hangisi düşüncenin akışını bozmaktadır?',
                     romalar[konum], [r for r in romalar if r != romalar[konum]],
                     f'Parçanın konusu “{p["konu"]}” iken {roma(konum + 1)} numaralı cümle (“{_kisa(p["b"])}”) '
                     f'başka bir konuya geçmektedir; bu cümle çıkarıldığında parça anlam bütünlüğüne kavuşur.', 3))

        # 7) Boşluk doldurma: gerçek cümle; akışı bozan cümle ve çelişen yargı güçlü çeldirici
        j = rng.randrange(1, 5)
        bos = cs[:j] + ['(----)'] + cs[j + 1:]
        yabanci = rng.sample([c for x in baska for c in x['cumleler'][1:]], 2)
        out.append(q('par_bosluk', KONU,
                     f'{_metin(bos)}{NL}Bu parçada boş bırakılan yere düşüncenin akışına göre aşağıdakilerden hangisi getirilmelidir?',
                     cs[j], [p['b'], p['y'], *yabanci],
                     f'Boşluğa “{cs[j]}” cümlesi gelmelidir; önceki ve sonraki cümlelerle anlam bütünlüğünü yalnız bu cümle '
                     f'sağlar. “{_kisa(p["b"])}” cümlesi konudan uzaklaşır, “{_kisa(p["y"])}” ise parçadaki '
                     f'düşünceyle çelişir.', 3))
    return out
