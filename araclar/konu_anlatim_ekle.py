"""data/konu_yeniden.json kartlarına `anlatimlar` ve `hocalar` alanlarını ekler.

`anlatimlar`: farklı yollardan kısa çalışma kartları (tablo, soru–cevap, çözümlü örnek, hafıza kodu).
`hocalar`: her ana konu için üç hocadan (Kemal – Hikâyeci, Ayşe – Sistemci, Murat – Soru Avcısı)
farklı kuramla yazılmış tam konu anlatımı. Kaynak: konu_anlatim_veri/hocalar.py + hoca_<ders>.py.

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


def hoca_gruplari():
    """Kart anahtarı → [{ana, anlatimlar: [3 hoca]}]."""
    sys.path.insert(0, str(ROOT / 'araclar'))
    meta = importlib.import_module('konu_anlatim_veri.hocalar')
    out = {}
    for d in DERSLER:
        es = importlib.import_module(f'konu_anlatim_veri.{d}').ESLEME
        hoca = importlib.import_module(f'konu_anlatim_veri.hoca_{d}').HOCA
        for konu, anakonular in es.items():
            gruplar = []
            for ana in anakonular:
                metinler = hoca[ana]
                assert len(metinler) == len(meta.HOCALAR), (d, ana)
                gruplar.append({'ana': ana, 'anlatimlar': [
                    {'hoca': h['id'], 'ikon': h['ikon'], 'ad': h['ad'], 'unvan': h['unvan'],
                     'yontem': h['yontem'], 'metin': metin.strip()}
                    for h, metin in zip(meta.HOCALAR, metinler)]})
            out[f'{d}|{konu}'] = gruplar
    return out


def kalite_sorunlari(gruplar_map):
    meta = importlib.import_module('konu_anlatim_veri.hocalar')
    sorun = []
    gorulen = set()
    for k, gruplar in gruplar_map.items():
        for g in gruplar:
            anahtar = (k.split('|')[0], g['ana'])
            if anahtar in gorulen:
                continue
            gorulen.add(anahtar)
            for a in g['anlatimlar']:
                baslik = sum(1 for sat in a['metin'].split('\n') if sat.startswith('§ '))
                if baslik < meta.MIN_BASLIK or len(a['metin']) < meta.MIN_UZUNLUK:
                    sorun.append(f"{anahtar} {a['hoca']}: {baslik} başlık, {len(a['metin'])} karakter")
    return sorun, len(gorulen)


def main():
    kartlar = json.loads(DOSYA.read_text(encoding='utf-8'))
    ek = anlatimlar()
    hg = hoca_gruplari()
    sorun, ana_sayisi = kalite_sorunlari(hg)
    eksik = [k for k in kartlar if k not in ek]
    hoca_eksik = [k for k in kartlar if not hg.get(k)]
    fazla = [k for k in ek if k not in kartlar]
    if '--kontrol' in sys.argv:
        print('anlatımı olmayan kart:', eksik)
        print('kartı olmayan eşleme:', fazla)
        print('hoca anlatımı olmayan kart:', hoca_eksik)
        print(f'{ana_sayisi} ana konu × 3 hoca; kalite sorunu: {sorun or "yok"}')
        return
    if sorun:
        sys.exit('Kalite sorunu: ' + '; '.join(sorun))
    for k, v in ek.items():
        if k in kartlar:
            kartlar[k]['anlatimlar'] = v
    for k, v in hg.items():
        if k in kartlar:
            kartlar[k]['hocalar'] = v
    DOSYA.write_text(json.dumps(kartlar, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{sum(1 for k in kartlar if kartlar[k].get("anlatimlar"))}/{len(kartlar)} karta '
          f'{sum(len(v) for k, v in ek.items() if k in kartlar)} anlatım yazıldı. Eksik: {eksik}')
    print(f'{sum(1 for k in kartlar if kartlar[k].get("hocalar"))}/{len(kartlar)} karta 3 hocalı anlatım '
          f'({ana_sayisi} ana konu × 3 = {ana_sayisi * 3} metin). Eksik: {hoca_eksik}')


if __name__ == '__main__':
    main()
