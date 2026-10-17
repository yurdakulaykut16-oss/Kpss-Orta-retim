"""Günlük test hedefi ve denemelerden ayrı gerçek başlangıç kapasitesi."""
import json
from kpss_kapsam import SUBJECTS, question_key


def load_target(root):
    target=json.loads((root/'data/calisma_hedefleri.json').read_text(encoding='utf-8'))
    count,size=target['ders_basina_gunluk_test'],target['set_boyutu']
    if (target.get('version')!=1 or type(count) is not int or count<400
            or type(size) is not int or size!=10 or count%size
            or target.get('gunluk_ust_sinir') is not True
            or target.get('denemeler_hedefe_dahil') is not False
            or target.get('saat_dilimi')!='Europe/Istanbul'):
        raise ValueError('Günlük hedef: en az 400 test sorusu/ders (günlük üst sınır), 10 soru/set; deneme hariç olmalı')
    return target


def summarize(target, bank, exams, days):
    index={s['id']:s for rows in bank.values() for s in rows}
    reserved={sid for d in exams['denemeler'] for sid in d['sorular']}
    reserved_roots={question_key(index[sid]) for sid in reserved}
    count,size=target['ders_basina_gunluk_test'],target['set_boyutu']
    subjects={}
    for d in SUBJECTS:
        roots={question_key(s) for s in bank[d] if s['id'] not in reserved and question_key(s) not in reserved_roots}
        reserve=sum(index[sid]['ders']==d for sid in reserved)
        subjects[d]=dict(aktif=len(bank[d]),denemeye_ayrilan=reserve,
                        baslangic_test_kapasitesi=len(roots),
                        ilk_gun_eksik=max(0,count-len(roots)),
                        kamp_test_ihtiyaci=count*days,
                        kamp_test_eksigi=max(0,count*days-len(roots)),
                        kamp_asgari_havuz=count*days+reserve,
                        tam_gun=min(days,len(roots)//count),
                        gun_dagilimi=[max(0,min(count,len(roots)-i*count)) for i in range(days)])
    return dict(**target,gunluk_toplam_test=count*len(SUBJECTS),ders_basina_test_seti=count//size,
                gunluk_toplam_set=count//size*len(SUBJECTS),kamp_gun_sayisi=days,
                dersler=subjects,
                notu='Başlangıç kapasitesi geçmişi boş profil içindir. Önceki kullanım ve yarım bırakılan rezervler güncel kullanılabilir sayıyı azaltır. Kamp hedefi tamamlandı anlamına gelmez.')
