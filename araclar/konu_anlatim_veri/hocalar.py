"""Üç hoca: aynı konuyu üç farklı öğretim kuramıyla anlatan üç anlatıcı.

Her ders modülü (hoca_<ders>.py) HOCA sözlüğü tanımlar:
    HOCA = {ana_konu: (kemal_metni, ayse_metni, murat_metni)}
Metinlerde "§ " ile başlayan satırlar ara başlık olarak gösterilir.
"""

HOCALAR = [
    {
        'id': 'kemal',
        'ikon': '📜',
        'ad': 'Kemal Hoca',
        'unvan': 'Hikâyeci',
        'yontem': 'Bütünden parçaya: önce büyük resim, sonra hikâye ve neden–sonuç zinciri. '
                  '“Neden böyle oldu?” sorusuyla anlamlı öğrenme.',
    },
    {
        'id': 'ayse',
        'ikon': '📐',
        'ad': 'Ayşe Hoca',
        'unvan': 'Sistemci',
        'yontem': 'Parçadan bütüne: kavram haritası, sınıflandırma, kural–istisna, '
                  'karşılaştırma ve adım adım çözüm algoritması (şema kuramı).',
    },
    {
        'id': 'murat',
        'ikon': '🎯',
        'ad': 'Murat Hoca',
        'unvan': 'Soru Avcısı',
        'yontem': 'Sınavdan geriye: soru kalıpları, anahtar kelime → cevap, tuzaklar, eleme, '
                  'hafıza kodu ve mini test (geri getirme pratiği).',
    },
]

# Her hocanın metninde bulunması gereken ara başlık sayısı (kalite kontrolü için alt sınır).
MIN_BASLIK = 3
MIN_UZUNLUK = 700
