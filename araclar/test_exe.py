"""KPSS_Kamp.exe paketlemesi: spec içeriği ve exe (frozen) modunda yol çözümü."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def spec_datas():
    """KPSS_Kamp.spec içindeki datas listesini PyInstaller olmadan hesaplar."""
    import types
    src = (ROOT / 'KPSS_Kamp.spec').read_text(encoding='utf-8').split('a = Analysis(')[0]
    hooks = types.ModuleType('PyInstaller.utils.hooks')
    hooks.collect_data_files = lambda _m: []
    hooks.collect_submodules = lambda _m: []
    eski = {k: sys.modules.get(k) for k in ('PyInstaller', 'PyInstaller.utils', 'PyInstaller.utils.hooks')}
    sys.modules.update({'PyInstaller': types.ModuleType('PyInstaller'),
                        'PyInstaller.utils': types.ModuleType('PyInstaller.utils'),
                        'PyInstaller.utils.hooks': hooks})
    try:
        ns = {'SPECPATH': str(ROOT)}
        exec(src, ns)
        return ns['datas']
    finally:
        for k, v in eski.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


class ExePaketTest(unittest.TestCase):
    def test_spec_uygulamanin_okudugu_her_seyi_gomer(self):
        hedefler = {(Path(s).name, d) for s, d in spec_datas()}
        for ad in ('program.json', 'denemeler.json', 'konu_yeniden.json', 'kpss_kapsam.json', 'calisma_hedefleri.json'):
            self.assertIn((ad, 'data'), hedefler)
        for klasor, hedef in (('static', 'static'), ('sorular', 'data/sorular'), ('dersler', 'data/dersler')):
            self.assertIn((klasor, hedef), hedefler)
        # app.py'nin VERI altında okuduğu her dosya/klasör spec'te olmalı.
        okunan = set(re.findall(r'VERI / "([^"/]+)"', (ROOT / 'app.py').read_text(encoding='utf-8')))
        gomulen = {Path(s).name for s, _ in spec_datas()}
        self.assertTrue(okunan - {'ilerleme'} <= gomulen, okunan - gomulen)
        self.assertNotIn('kaynaklar', gomulen)
        self.assertNotIn('ilerleme', gomulen)

    def test_tzdata_gereksinimi(self):
        self.assertIn('tzdata', (ROOT / 'requirements.txt').read_text(encoding='utf-8'))
        self.assertIn("collect_data_files('tzdata')", (ROOT / 'KPSS_Kamp.spec').read_text(encoding='utf-8'))

    def test_frozen_modda_icerik_paketten_ilerleme_exe_yanina(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            paket, exe_dizin, mods = tmp / 'paket', tmp / 'exe', tmp / 'mods'
            exe_dizin.mkdir()
            mods.mkdir()
            for s, d in spec_datas():
                s = Path(s)
                if s.is_dir():
                    shutil.copytree(s, paket / d)
                else:
                    (paket / d).mkdir(parents=True, exist_ok=True)
                    shutil.copy(s, paket / d / s.name)
            for m in ('app.py', 'kpss_kapsam.py', 'calisma_hedefi.py', 'kpss_kamp.py'):
                shutil.copy(ROOT / m, mods / m)
            kod = textwrap.dedent(f'''
                import json, sys
                sys.frozen = True
                sys._MEIPASS = {str(paket)!r}
                sys.executable = {str(exe_dizin / 'KPSS_Kamp.exe')!r}
                sys.path.insert(0, {str(mods)!r})
                import app
                c = app.app.test_client()
                meta = c.get('/api/meta').get_json()
                c.post('/api/ilerleme/exetest', json={{'gorevler': {{'a': 1}}}})
                print(json.dumps(dict(kok=str(app.KOK), ilerleme=str(app.ILERLEME),
                                      gun=len(meta['gun_ozetleri']), index=c.get('/').status_code,
                                      kart=len(c.get('/api/konu-yeniden').get_json()))))
            ''')
            out = subprocess.run([sys.executable, '-c', kod], capture_output=True, text=True, check=True, cwd=tmp)
            r = json.loads(out.stdout.strip().splitlines()[-1])
            self.assertEqual(r['kok'], str(paket))
            self.assertEqual(r['ilerleme'], str(exe_dizin / 'KPSS_Kamp_ilerleme'))
            self.assertTrue((exe_dizin / 'KPSS_Kamp_ilerleme' / 'exetest.json').exists())
            self.assertEqual((r['gun'], r['index']), (7, 200))
            self.assertEqual(r['kart'], 123)


if __name__ == '__main__':
    unittest.main()
