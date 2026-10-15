#!/usr/bin/env python3
"""Günlük test havuzundaki ilk-gün eksiği için elle yazılan 188 soru.

TSV soru varyantı üretmez: her kayıt kendi kökü, beş seçeneği ve çözümüyle
editoryal girdidir. Yalnız şık sıralaması deterministiktir. Konu anahtarı
bir inceleme adayıdır; kapsam onayı ayrıca kayıt özetiyle verilir.
"""
import random
from pathlib import Path

SOURCE = 'data/kaynaklar/ek_188_gunluk500.tsv'
TOPICS = {'v-hukuk':'Hukuk','v-anayasa':'Anayasa','v-tbmm':'TBMM','v-yurutme':'Yürütme',
          'v-yargi':'Yargı','v-idare':'Kamu Hizmetleri','v-secim':'Seçimler','v-memur':'Memuriyet',
          'g-kurum':'Kurumlar','g-kultur':'Kültür','g-dunya':'Dünya','g-odul':'Kültür','g-spor':'Spor'}


def build(root):
    records,topics=[],{}
    for no,line in enumerate((root/SOURCE).read_text(encoding='utf-8').splitlines(),1):
        if not line.strip() or line.startswith('#'):continue
        p=[x.strip() for x in line.split('|')]
        if len(p)!=10 or not all(p):raise ValueError(f'{SOURCE}:{no}: 10 dolu alan gerekir')
        sid,topic,z,stem,correct,*rest=p
        if topic not in TOPICS or z not in ('2','3') or sid in topics:raise ValueError(f'{no}: geçersiz konu/zorluk/id')
        ders='vatandaslik' if sid.startswith('VAT-EK-') else 'guncel' if sid.startswith('GUN-EK-') else None
        if not ders or topic[0]!=('v' if ders=='vatandaslik' else 'g'):raise ValueError(f'{no}: ders/konu uyumsuz')
        options=[correct,*rest[:4]]
        if len(set(x.casefold() for x in options))!=5:raise ValueError(f'{no}: beş farklı şık gerekir')
        random.Random(sid+'-gunluk500').shuffle(options)
        n=int(sid.rsplit('-',1)[1])
        records.append(dict(id=sid,ders=ders,gun=1+(n-1)%10,konu=TOPICS[topic],zorluk=int(z),
                            kok=stem.replace(r'\n','\n'),siklar=options,dogru=options.index(correct),
                            kaynak='KPSS formatında',etiketler=['ozgun','ek-gunluk500'],
                            cozumler=[dict(yontem='KPSS mantığı ile çözüm',metin=rest[4])]))
        topics[sid]=topic
    expected={f'VAT-EK-{i:04d}' for i in range(1,27)}|{f'GUN-EK-{i:04d}' for i in range(1,163)}
    if set(topics)!=expected:raise ValueError('26 Vatandaşlık ve 162 Güncel sabit id gerekir')
    if len({r['kok'].strip().casefold() for r in records})!=188:raise ValueError('Tekrarlanan yeni kök')
    return records,topics


def add_to_bank(root,by_ders,index):
    if not (root/SOURCE).exists():return
    records,_=build(root)
    for s in records:
        if s['id'] in index:
            if index[s['id']]!=s:raise ValueError('Ek kayıt beklenmeyen içerikle değişti: '+s['id'])
        else:
            index[s['id']]=s;by_ders[s['ders']][1].append(s)
