"""data/konu_yeniden.json kartlarına `anlatimlar` alanını ekler (farklı yollardan konu anlatımı).

Kaynak: araclar/konu_anlatim_veri/<ders>.py (ANLATIM: ana konu → [(başlık, metin)],
ESLEME: kart konusu → ana konu listesi). Betik idempotenttir; yeniden çalıştırıldığında
`anlatimlar` alanı kaynaktan baştan yazılır.

Kullanım: python3 araclar/konu_anlatim_ekle.py [--kontrol]
"""
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOSYA = ROOT / 'data' / 'konu_yeniden.json'
DERSLER = ['tarih', 'cografya', 'vatandaslik', 'turkce', 'guncel']


def anlatimlar():
    sys.path.insert(0, str(ROOT / 'araclar'))
    out = {}
    for d in DERSLER:
        m = importlib.import_module(f'konu_anlatim_veri.{d}')
        for konu, anakonular in m.ESLEME.items():
            liste = []
            for ana in anakonular:
                for baslik, metin in m.ANLATIM[ana]:
                    b = baslik if len(anakonular) == 1 else f'{baslik} — {ana}'
                    liste.append({'baslik': b, 'metin': metin})
            out[f'{d}|{konu}'] = liste
    return out


def main():
    kartlar = json.loads(DOSYA.read_text(encoding='utf-8'))
    ek = anlatimlar()
    eksik = [k for k in kartlar if k not in ek]
    fazla = [k for k in ek if k not in kartlar]
    if '--kontrol' in sys.argv:
        print('anlatımı olmayan kart:', eksik)
        print('kartı olmayan eşleme:', fazla)
        return
    for k, v in ek.items():
        if k in kartlar:
            kartlar[k]['anlatimlar'] = v
    DOSYA.write_text(json.dumps(kartlar, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{sum(1 for k in kartlar if kartlar[k].get("anlatimlar"))}/{len(kartlar)} karta '
          f'{sum(len(v) for k, v in ek.items() if k in kartlar)} anlatım yazıldı. Eksik: {eksik}')


if __name__ == '__main__':
    main()
