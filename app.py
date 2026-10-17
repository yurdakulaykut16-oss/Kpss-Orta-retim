#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KPSS Ortaöğretim — 7 Günlük Hızlandırılmış Kamp (18–24 Ekim; 6 test günü + final provası)
Flask sunucusu: tüm içerik (konu anlatımları, soru bankası, program, denemeler)
data/ klasörünün içindedir; ilerleme verisi data/ilerleme/ altında saklanır.

Çalıştırma:
    pip install -r requirements.txt
    python app.py
    -> http://localhost:5000

Masaüstü (exe) kullanımı için bkz. kpss_kamp.py ve KPSS_Kamp.spec.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
import re
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from kpss_kapsam import read_policy, filter_bank, project_exams, question_key
from calisma_hedefi import load_target, summarize

if getattr(sys, "frozen", False):
    # PyInstaller ile paketlenmiş exe: içerik exe'nin içinden (geçici klasör) okunur,
    # ilerleme ise exe'nin yanındaki kalıcı klasöre yazılır (her açılışta silinmesin diye).
    KOK = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    _ILERLEME_VARSAYILAN = Path(sys.executable).resolve().parent / "KPSS_Kamp_ilerleme"
else:
    KOK = Path(__file__).resolve().parent
    _ILERLEME_VARSAYILAN = KOK / "data" / "ilerleme"
VERI = KOK / "data"
ILERLEME = Path(os.environ.get("KPSS_ILERLEME_DIZINI") or _ILERLEME_VARSAYILAN)
ILERLEME.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(KOK / "static"), static_url_path="/static")
_KILIT = threading.Lock()

# ---------------------------------------------------------------- içerik yükleme


def _json_oku(yol: Path):
    with open(yol, "r", encoding="utf-8") as f:
        return json.load(f)


def program_yukle():
    return _json_oku(VERI / "program.json")


def denemeler_yukle():
    return _json_oku(VERI / "denemeler.json")


def sorular_yukle(ders: str) -> list:
    yol = VERI / "sorular" / f"{ders}.jsonl"
    if not yol.exists():
        return []
    liste = []
    with open(yol, "r", encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            if not satir or satir.startswith("#"):
                continue
            liste.append(json.loads(satir))
    return liste


def ders_md_bol(ders: str) -> dict:
    """data/dersler/<ders>.md dosyasını gün modüllerine böler.

    Biçim:
        # GUN 1 | Başlık
        Konular: a; b; c
        Kilit: tek cümle
        ## Giriş
        ## Anlatım | Bölüm
        ## Yöntem 1 | Ad
        ## Yöntem 2 | Ad
        ## Sık Hatalar
        ## Cebe Kart
        ## Ağız Tekrarı
    """
    yol = VERI / "dersler" / f"{ders}.md"
    if not yol.exists():
        return {"ders": ders, "gunler": []}
    metin = yol.read_text(encoding="utf-8")
    parcalar = re.split(r"^# GUN (\d+)\s*\|\s*(.*)$", metin, flags=re.MULTILINE)
    gunler = []
    # parcalar: [önce, no, baslik, gövde, no, baslik, gövde, ...]
    for i in range(1, len(parcalar), 3):
        no = int(parcalar[i])
        baslik = parcalar[i + 1].strip()
        govde = parcalar[i + 2]
        gun = _gun_govdesi(no, baslik, govde)
        gunler.append(gun)
    gunler.sort(key=lambda g: g["gun"])
    return {"ders": ders, "gunler": gunler}


def _gun_govdesi(no: int, baslik: str, govde: str) -> dict:
    konular = []
    kilit = ""
    ilk_satirlar = []
    bolumler = []
    yontemler = []
    sik_hatalar = []
    kart = ""
    agiz = []

    aktif = ("meta", None)
    kutular = []
    for satir in govde.splitlines():
        m = re.match(r"^##\s+(.*)$", satir)
        if m:
            aktif = ("bolum", m.group(1).strip())
            kutular.append({"tip": aktif[1], "satirlar": []})
            continue
        if kutular:
            kutular[-1]["satirlar"].append(satir)
        else:
            ilk_satirlar.append(satir)

    meta = "\n".join(ilk_satirlar)
    for s in meta.splitlines():
        s = s.strip()
        if s.startswith("Konular:"):
            konular = [k.strip() for k in s[len("Konular:"):].split(";") if k.strip()]
        elif s.startswith("Kilit:"):
            kilit = s[len("Kilit:"):].strip()

    gun_baslik = baslik  # parametreyi bölüm başlıkları ezmesin
    for kutu in kutular:
        baslik = kutu["tip"]
        icerik = "\n".join(kutu["satirlar"]).strip()
        if baslik.startswith("Giriş"):
            giris = icerik
            bolumler.append({"baslik": "Giriş", "html": giris, "tur": "giris"})
        elif baslik.startswith("Anlatım"):
            ad = baslik.split("|", 1)[1].strip() if "|" in baslik else "Konu Anlatımı"
            bolumler.append({"baslik": ad, "html": icerik, "tur": "anlatim"})
        elif baslik.startswith("Yöntem 1"):
            ad = baslik.split("|", 1)[1].strip() if "|" in baslik else "1. Yöntem"
            yontemler.append({"ad": ad, "html": icerik})
        elif baslik.startswith("Yöntem 2"):
            ad = baslik.split("|", 1)[1].strip() if "|" in baslik else "2. Yöntem"
            yontemler.append({"ad": ad, "html": icerik})
        elif baslik.startswith("Sık Hatalar"):
            sik_hatalar = [s.strip("- ").strip() for s in icerik.splitlines() if s.strip()]
        elif baslik.startswith("Cebe Kart"):
            kart = icerik
        elif baslik.startswith("Ağız Tekrarı"):
            agiz = [s.strip("- ").strip() for s in icerik.splitlines() if s.strip().startswith("?") or s.strip()]
        else:
            bolumler.append({"baslik": baslik, "html": icerik, "tur": "ek"})

    # Giriş yoksa ilk bölümü giriş say
    giris = ""
    kalan = []
    for b in bolumler:
        if b["tur"] == "giris" and not giris:
            giris = b["html"]
        else:
            kalan.append(b)

    return {
        "gun": no,
        "baslik": gun_baslik,
        "konular": konular,
        "kilit": kilit,
        "giris": giris,
        "bolumler": {b["baslik"]: b["html"] for b in kalan},
        "yontemler": {y["ad"]: y["html"] for y in yontemler},
        "sik_hatalar": sik_hatalar,
        "kart": kart,
        "agiz_tekrari": agiz,
    }


DERSLER = {
    "tarih": {"ad": "Tarih", "renk": "#c2410c", "sira": 1},
    "cografya": {"ad": "Coğrafya", "renk": "#0f766e", "sira": 2},
    "vatandaslik": {"ad": "Vatandaşlık", "renk": "#1d4ed8", "sira": 3},
    "turkce": {"ad": "Türkçe", "renk": "#7c3aed", "sira": 4},
    "guncel": {"ad": "Güncel Bilgiler", "renk": "#b45309", "sira": 5},
}

_cache = {}
_cache_kilit = threading.Lock()


def her_seyi_yukle(zorla: bool = False):
    with _cache_kilit:
        if _cache and not zorla:
            return _cache
        _cache.clear()  # Zorunlu yenileme başarısızsa eski izinleri de servis etme.
        # Önce kapsamı doğrula. Eksik/bozuk kapsamda ham bankayı veya yarım
        # cache'i servis etme; bütün çözüm yolları aynı aktif indeksi kullanır.
        raw = {d: sorular_yukle(d) for d in DERSLER}
        active, report = filter_bank(raw, read_policy(KOK))
        program = program_yukle()
        exams = project_exams(denemeler_yukle(), raw, active)
        target = summarize(load_target(KOK), active, exams,
                           sum(1 for g in program['gunler'] if g.get('test_hedefi', True)))
        fresh = dict(program=program, kapsam=report, sorular=active, calisma_hedefi=target,
                     denemeler=exams,
                     konu_yeniden=_json_oku(VERI / "konu_yeniden.json") if (VERI / "konu_yeniden.json").exists() else {},
                     dersler={d: ders_md_bol(d) for d in DERSLER})
        for d in DERSLER:
            fresh["dersler"][d]["bilgi"] = DERSLER[d]
        fresh["soru_index"] = {d: {s["id"]: s for s in active[d]} for d in DERSLER}
        _cache.clear()
        _cache.update(fresh)
        return _cache


# ---------------------------------------------------------------- ilerleme


def ilerleme_dosya(kullanici: str) -> Path:
    guvenli = re.sub(r"[^a-zA-Z0-9_-]", "_", kullanici)[:64] or "varsayilan"
    return ILERLEME / f"{guvenli}.json"


def ilerleme_oku(kullanici: str) -> dict:
    yol = ilerleme_dosya(kullanici)
    if yol.exists():
        try:
            return _json_oku(yol)
        except Exception:
            pass
    return {"kullanici": kullanici, "gorevler": {}, "soru_kayit": {}, "etiketler": {}, "denemeler": [], "oturumlar": []}


def _ilerleme_yaz_kilitsiz(kullanici: str, veri: dict) -> dict:
    yol = ilerleme_dosya(kullanici)
    onceki = ilerleme_oku(kullanici)
    cache = her_seyi_yukle()
    index = {sid:s for rows in cache['soru_index'].values() for sid,s in rows.items()}
    old_ids, old_roots = kullanim_gecmisi(onceki, index)
    onceki['ayrilan_sorular'] = {**{sid:True for sid in old_ids}, **onceki.get('ayrilan_sorular', {})}
    onceki['ayrilan_kokler'] = {**onceki.get('ayrilan_kokler', {}), **{k:True for k in old_roots}}
    # Gecikmiş sekme/yedek, sunucuda ayrılmış soruları serbest bırakamaz.
    for alan in ("ayrilan_sorular", "ayrilan_kokler"):
        eski, yeni = onceki.get(alan, {}), veri.get(alan, {})
        eski = eski if isinstance(eski, dict) else {}
        veri[alan] = {**eski, **(yeni if isinstance(yeni, dict) else {})}
        # Sunucunun yazdığı gün/ders bilgisi (günlük üst sınır sayacı) istemci kaydıyla silinemez.
        veri[alan].update({k: v for k, v in eski.items() if isinstance(v, dict) and v.get('gun')})
    old_sessions = onceki.get('devam_testleri', {})
    incoming_sessions = veri.get('devam_testleri', {})
    sessions = dict(old_sessions) if isinstance(old_sessions, dict) else {}
    for uid, session in (incoming_sessions.items() if isinstance(incoming_sessions, dict) else []):
        if not isinstance(session, dict):
            continue
        if uid not in sessions or session.get('guncelleme', 0) >= sessions[uid].get('guncelleme', 0):
            sessions[uid] = session
    veri['devam_testleri'] = sessions
    veri["kullanici"] = kullanici
    tmp = yol.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(yol)  # Okuyucu yarım yazılmış kayıt görmez.
    return veri


def ilerleme_yaz(kullanici: str, veri: dict) -> dict:
    with _KILIT:
        return _ilerleme_yaz_kilitsiz(kullanici, veri)


def kullanim_gecmisi(veri, index):
    ids = set(veri.get('ayrilan_sorular', {}))
    roots = set(veri.get('ayrilan_kokler', {}))
    for sid, k in veri.get('soru_kayit', {}).items():
        if isinstance(k, dict) and (k.get('son') or k.get('d', 0) > 0 or k.get('y', 0) > 0):
            ids.add(sid)
    ids.update(veri.get('gunluk', {}).get('ids', {}))
    for g in veri.get('ders_gunluk', {}).values():
        ids.update(g.get('ids', {}))
    for d in veri.get('denemeler', []):
        ids.update(d.get('sorular', []))
    roots.update(question_key(index[sid]) for sid in ids if sid in index)
    return ids, roots


# ---------------------------------------------------------------- rotalar


@app.get("/")
def ana_sayfa():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/meta")
def api_meta():
    c = her_seyi_yukle()
    program = c["program"]
    soru_sayilari = {d: len(c["sorular"][d]) for d in DERSLER}
    return jsonify(
        {
            "sinav": program["sinav"],
            "dersler": DERSLER,
            "soru_sayilari": soru_sayilari,
            "havuz_hedefleri": {"guncel": c["calisma_hedefi"]["guncel_ara_havuz_hedefi"]},
            "calisma_hedefi": c["calisma_hedefi"],
            "kapsam": {k: v for k, v in c['kapsam'].items() if k != 'bekleyen_kayitlar'},
            "gun_ozetleri": [
                {"no": g["no"], "tarih": g["tarih"], "tema": g["tema"], "test_hedefi": g.get("test_hedefi", True)} for g in program["gunler"]
            ],
            "denemeler": [
                {"id": d["id"], "ad": d["ad"], "gun": d["gun"], "soru_sayisi": len(d["sorular"]), "sure_dk": d["sure_dk"]}
                for d in c["denemeler"]["denemeler"]
            ],
        }
    )


@app.get("/api/program")
def api_program():
    return jsonify(her_seyi_yukle()["program"])


@app.get("/api/kapsam")
def api_kapsam():
    return jsonify(her_seyi_yukle()['kapsam'])


@app.get("/api/konu-yeniden")
def api_konu_yeniden():
    return jsonify(her_seyi_yukle().get("konu_yeniden", {}))


@app.get("/api/ders/<ders>")
def api_ders(ders: str):
    c = her_seyi_yukle()
    if ders not in c["dersler"]:
        return jsonify({"hata": "ders yok"}), 404
    return jsonify(c["dersler"][ders])


@app.get("/api/sorular/<ders>")
def api_sorular(ders: str):
    c = her_seyi_yukle()
    if ders not in c["sorular"]:
        return jsonify({"hata": "ders yok"}), 404
    veri = c["sorular"][ders]
    if request.args.get("cikmis"):
        return jsonify([s for s in veri if re.match(r"^\d{4}-KPSS(?:\s|$)", s.get("kaynak", ""))])
    return jsonify(veri)


@app.get("/api/soru/<sid>")
def api_soru(sid: str):
    c = her_seyi_yukle()
    for d in DERSLER:
        s = c["soru_index"][d].get(sid)
        if s:
            return jsonify(s)
    return jsonify({"hata": "soru yok"}), 404


@app.get("/api/denemeler")
def api_denemeler():
    return jsonify(her_seyi_yukle()["denemeler"])


@app.get("/api/deneme/<did>")
def api_deneme(did: str):
    c = her_seyi_yukle()
    for d in c["denemeler"]["denemeler"]:
        if d["id"] == did:
            sorular = []
            for sid in d["sorular"]:
                for dr in DERSLER:
                    s = c["soru_index"][dr].get(sid)
                    if s:
                        sorular.append(s)
                        break
            return jsonify({**d, "soru_nesneleri": sorular})
    return jsonify({"hata": "deneme yok"}), 404


def bugun_tarihi(target) -> str:
    return datetime.now(ZoneInfo(target['saat_dilimi'])).date().isoformat()


def bugun_ayrilan_testler(veri, gun) -> Counter:
    """Bugün test için ayrılan yeni soruların ders bazında sayısı (günlük üst sınır)."""
    sayac = Counter()
    for meta in veri.get('ayrilan_sorular', {}).values():
        if isinstance(meta, dict) and meta.get('tur') == 'test' and meta.get('gun') == gun and meta.get('ders'):
            sayac[meta['ders']] += 1
    return sayac


@app.post("/api/soru-ayir/<kullanici>")
def api_soru_ayir(kullanici):
    """Aynı profil için kontrol + ayırma atomik; gösterimden önce çağrılır."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(hata='Geçersiz istek'), 400
    ids, tur, oturum = payload.get('ids'), payload.get('tur'), payload.get('oturum')
    if (tur not in ('test', 'deneme') or not isinstance(oturum, str) or not 1 <= len(oturum) <= 160
            or not isinstance(ids, list) or not 1 <= len(ids) <= 50
            or not all(isinstance(i, str) for i in ids) or len(ids) != len(set(ids))):
        return jsonify(hata='Geçersiz soru ayırma bilgisi'), 400
    cache = her_seyi_yukle()
    index = {sid:s for rows in cache['soru_index'].values() for sid,s in rows.items()}
    if any(sid not in index for sid in ids):
        return jsonify(hata='Kapsam dışı veya bilinmeyen soru ayrılamaz'), 400
    exams = cache['denemeler']['denemeler']
    did = payload.get('deneme_id') if tur == 'deneme' else None
    if tur == 'deneme':
        exam = next((d for d in exams if d['id'] == did), None)
        if not exam or Counter(index[i]['ders'] for i in ids) != Counter(index[i]['ders'] for i in exam['sorular']):
            return jsonify(hata='Deneme sayısı veya ders dağılımı değiştirilemez'), 400
    reserved = {sid for d in exams if d['id'] != did for sid in d['sorular']}
    reserved_roots = {question_key(index[sid]) for sid in reserved}
    roots = [question_key(index[sid]) for sid in ids]
    if len(set(roots)) != len(roots) or any(sid in reserved for sid in ids) or set(roots) & reserved_roots:
        return jsonify(hata='Tekrarlı veya başka denemeye ayrılmış soru'), 409
    with _KILIT:
        veri = ilerleme_oku(kullanici)
        used, used_roots = kullanim_gecmisi(veri, index)
        if used.intersection(ids) or used_roots.intersection(roots):
            return jsonify(hata='Bu sorulardan biri daha önce ayrıldı veya çözüldü. Yeni oturum açın.',
                           ayrilan_sorular={sid:True for sid in used},
                           ayrilan_kokler={k:True for k in used_roots}), 409
        target = cache.get('calisma_hedefi') or load_target(KOK)
        gun = bugun_tarihi(target)
        if tur == 'test':
            sinir = target['ders_basina_gunluk_test']
            bugun = bugun_ayrilan_testler(veri, gun)
            istenen = Counter(index[sid]['ders'] for sid in ids)
            dolu = sorted(d for d, n in istenen.items() if bugun[d] + n > sinir)
            if dolu:
                return jsonify(hata=f'Bugünkü günlük sınır ({sinir} yeni test sorusu/ders) doldu: '
                                    + ', '.join(DERSLER[d]['ad'] if isinstance(DERSLER.get(d), dict) else d for d in dolu)
                                    + '. Kalan sorular sonraki günlere ayrıldı.',
                               gunluk_sinir=sinir, bugun_ayrilan=dict(bugun), gun=gun), 429
        added_ids = {sid:dict(tur=tur, oturum=oturum, gun=gun, ders=index[sid]['ders']) for sid in ids}
        added_roots = {k:True for k in roots}
        veri['ayrilan_sorular'] = {**{sid:True for sid in used},
                                  **veri.get('ayrilan_sorular', {}), **added_ids}
        veri.setdefault('ayrilan_kokler', {}).update({k:True for k in used_roots})
        veri['ayrilan_kokler'].update(added_roots)
        _ilerleme_yaz_kilitsiz(kullanici, veri)
    return jsonify(ok=True, ayrilan_sorular=added_ids, ayrilan_kokler=added_roots)


@app.get("/api/ilerleme/<kullanici>")
def api_ilerleme_get(kullanici: str):
    return jsonify(ilerleme_oku(kullanici))


@app.post("/api/ilerleme/<kullanici>")
def api_ilerleme_post(kullanici: str):
    veri = request.get_json(force=True, silent=True) or {}
    return jsonify(ilerleme_yaz(kullanici, veri))


@app.get("/api/sifirla/<kullanici>")
def api_sifirla(kullanici: str):
    yol = ilerleme_dosya(kullanici)
    if yol.exists():
        yol.unlink()
    return jsonify(ilerleme_oku(kullanici))


if __name__ == "__main__":
    her_seyi_yukle()
    toplam = sum(len(v) for v in her_seyi_yukle()["sorular"].values())
    print(f"[KPSS Kamp] {len(DERSLER)} ders yüklendi — toplam {toplam} soru bankada.")
    print("[KPSS Kamp] http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
