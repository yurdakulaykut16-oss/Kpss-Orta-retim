/* =========================================================
   KPSS Ortaöğretim — Hızlandırılmış Kamp
   10'luk testler · otomatik kontrol · yanlış telafisi · ustalık
   ========================================================= */
"use strict";

const DERSLER = {
  tarih: { ad: "Tarih", sira: 1 },
  cografya: { ad: "Coğrafya", sira: 2 },
  vatandaslik: { ad: "Vatandaşlık", sira: 3 },
  turkce: { ad: "Türkçe", sira: 4 },
  guncel: { ad: "Güncel Bilgiler", sira: 5 },
};
const SIK_HARF = ["A", "B", "C", "D", "E"];
const KULLANICI = "varsayilan";
const DERS_HEDEF = 500;              // her ders için günlük minimum
const GUNLUK_HEDEF = DERS_HEDEF * 5;  // toplam günlük hedef
const BATCH = 10;

const V = {
  meta: null, program: null, dersler: {}, sorular: {}, soruIdx: {},
  denemeler: null, denemeIdx: {}, kayit: null, oturum: null, denemeOturum: null,
  tumSorular: {}, etiketIdx: {}, konuListe: {}, konuYeniden: {},
};

/* ---------------- ilerleme ---------------- */
function bosKayit() {
  return {
    kullanici: KULLANICI, gorevler: {}, soru_kayit: {}, etiketler: {},
    denemeler: [], oturumlar: [], okunan: {},
    ustalik: {}, gunluk: { tarih: null, sayi: 0, ids: {} }, konu_okuma: {},
    odak: {}, ders_gunluk: {}, ders_akis: {},
  };
}
async function kayitYukle() {
  try {
    const r = await fetch(`/api/ilerleme/${KULLANICI}`);
    V.kayit = await r.json();
    if (!V.kayit || !V.kayit.etiketler) V.kayit = bosKayit();
    const b = bosKayit();
    for (const k of Object.keys(b)) if (V.kayit[k] === undefined) V.kayit[k] = b[k];
  } catch {
    V.kayit = JSON.parse(localStorage.getItem("kpss-kayit") || "null") || bosKayit();
    const b = bosKayit();
    for (const k of Object.keys(b)) if (V.kayit[k] === undefined) V.kayit[k] = b[k];
  }
}
let kayitTimer = null;
function kaydet() {
  localStorage.setItem("kpss-kayit", JSON.stringify(V.kayit));
  clearTimeout(kayitTimer);
  kayitTimer = setTimeout(() => {
    fetch(`/api/ilerleme/${KULLANICI}`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(V.kayit),
    }).catch(() => {});
  }, 400);
}
function soruKaydi(id) {
  return (V.kayit.soru_kayit[id] = V.kayit.soru_kayit[id] || { d: 0, y: 0, son: null });
}
function etiketKaydi(t) {
  return (V.kayit.etiketler[t] = V.kayit.etiketler[t] || { d: 0, y: 0, tekrar: 0 });
}
const okumaAnahtar = (d, gun) => `${d}|${gun}`;
const konuAnahtar = (d, konu) => `${d}|${konu}`;

/* ---------------- veri ---------------- */
async function veriYukle() {
  const [meta, program, denemeler] = await Promise.all([
    fetch("/api/meta").then((r) => r.json()),
    fetch("/api/program").then((r) => r.json()),
    fetch("/api/denemeler").then((r) => r.json()),
  ]);
  V.meta = meta; V.program = program; V.denemeler = denemeler;
  V.denemeIdx = {}; denemeler.denemeler.forEach((d) => (V.denemeIdx[d.id] = d));
  V.konuYeniden = await fetch("/api/konu-yeniden").then((r) => r.json()).catch(() => ({}));
  await Promise.all(
    Object.keys(DERSLER).map(async (d) => {
      V.dersler[d] = await fetch(`/api/ders/${d}`).then((r) => r.json());
      V.sorular[d] = await fetch(`/api/sorular/${d}`).then((r) => r.json());
      V.soruIdx[d] = {}; V.sorular[d].forEach((s) => (V.soruIdx[d][s.id] = s));
    })
  );
  V.tumSorular = {}; V.etiketIdx = {}; V.konuListe = {};
  for (const d of Object.keys(DERSLER)) {
    const konular = new Map();
    for (const s of V.sorular[d]) {
      V.tumSorular[s.id] = s;
      (s.etiketler || []).forEach((t) => {
        (V.etiketIdx[t] = V.etiketIdx[t] || []).push(s.id);
      });
      if (!konular.has(s.konu)) konular.set(s.konu, []);
      konular.get(s.konu).push(s);
    }
    V.konuListe[d] = [...konular.entries()]
      .map(([konu, liste]) => ({ konu, liste, adet: liste.length, gunler: [...new Set(liste.map((s) => s.gun))].sort((a, b) => a - b) }))
      .sort((a, b) => (a.gunler[0] ?? 0) - (b.gunler[0] ?? 0) || a.konu.localeCompare(b.konu, "tr"));
  }
}

/* ---------------- ustalık & anti-tekrar ---------------- */
function ustalikKaydi(key) {
  return (V.kayit.ustalik[key] = V.kayit.ustalik[key] || { g: [], usta: false });
}
function ustalikGuncelle(s, dogru) {
  const u = ustalikKaydi(konuAnahtar(s.ders, s.konu));
  u.g.push(dogru ? 1 : 0);
  if (u.g.length > 10) u.g = u.g.slice(-10);
  u.usta = u.g.length >= 10 && u.g.reduce((a, b) => a + b, 0) >= 8;
}
function ustalikOrani(key) {
  const u = V.kayit.ustalik[key];
  if (!u || !u.g.length) return 0;
  return Math.round((u.g.reduce((a, b) => a + b, 0) / u.g.length) * 100);
}
function dersGunlukKaydi(d) {
  const bugun = new Date().toISOString().slice(0, 10);
  const b = (V.kayit.ders_gunluk[d] = V.kayit.ders_gunluk[d] || { tarih: null, sayi: 0, ids: {} });
  if (b.tarih !== bugun) { b.tarih = bugun; b.sayi = 0; b.ids = {}; }
  return b;
}
function dersAkisKaydi(d) {
  const bugun = new Date().toISOString().slice(0, 10);
  const a = (V.kayit.ders_akis[d] = V.kayit.ders_akis[d] || { gun: bugun, biten: [] });
  if (a.gun !== bugun) { a.gun = bugun; a.biten = []; }
  return a;
}
function dersAkisSonraki(d) {
  // önce konu testleri (müfredat sırasıyla), bitti ise karışık
  const a = dersAkisKaydi(d);
  const konular = (V.konuListe[d] || []).map((x) => x.konu);
  const siradaki = konular.find((k) => !a.biten.includes(k));
  if (siradaki) return { tip: "konu", konu: siradaki, kalan: konular.filter((k) => !a.biten.includes(k)).length };
  return { tip: "karisik" };
}
function gunlukSayac() {
  const bugun = new Date().toISOString().slice(0, 10);
  if (!V.kayit.gunluk || V.kayit.gunluk.tarih !== bugun) {
    V.kayit.gunluk = { tarih: bugun, sayi: 0, ids: {} };
  }
  return V.kayit.gunluk;
}
function secimPuani(s, opts = {}) {
  const k = V.kayit.soru_kayit[s.id];
  const g = V.kayit.gunluk || { ids: {} };
  const u = V.kayit.ustalik[konuAnahtar(s.ders, s.konu)];
  let p = Math.random() * 12;
  if (!k || !k.son) p += 120;                 // hiç görülmemiş → öncelik
  if (g.ids[s.id]) p -= 260;                  // bugün çıktı → gelmesin
  if (k) {
    if (k.y > k.d) p += 55;                   // yanlışlı → ustalana kadar tekrar
    if (k.d >= 2 && k.y === 0) p -= 110;      // ustalaştı → uzak
    p += Math.min(35, (Date.now() - k.son) / 3.6e9); // eski gören öncelik
  }
  if (u && u.usta) p -= 70;
  if (opts.zayifOdak && k && k.y > 0) p += 45;
  const odak = (V.kayit.odak || {})[konuAnahtar(s.ders, s.konu)];
  if (odak > 0) p += 50 + Math.min(40, odak * 10);  // deneme zayıflığı → öncelikli
  return p;
}
function testSeti(havuz, adet, opts = {}) {
  return [...havuz]
    .sort((a, b) => secimPuani(b, opts) - secimPuani(a, opts))
    .slice(0, adet);
}
function etiketZayiflik(t) {
  const k = V.kayit.etiketler[t] || { d: 0, y: 0 };
  return k.y * 3 - k.d + (k.tekrar || 0) * 0.5;
}
function zayifEtiketler(ders, limit = 30) {
  const t = Object.keys(V.etiketIdx).filter((tag) =>
    V.etiketIdx[tag].some((id) => V.tumSorular[id].ders === ders)
  );
  t.sort((a, b) => etiketZayiflik(b) - etiketZayiflik(a));
  return t.slice(0, limit);
}
function zayifKonular(ders, limit = 8) {
  return (V.konuListe[ders] || [])
    .filter((x) => !V.kayit.ustalik[konuAnahtar(ders, x.konu)]?.usta)
    .sort((a, b) => ustalikOrani(konuAnahtar(ders, a.konu)) - ustalikOrani(konuAnahtar(ders, b.konu)))
    .slice(0, limit);
}
function benzerler(soru, n = 2, haric = []) {
  const et = soru.etiketler || [];
  const aday = (V.sorular[soru.ders] || []).filter(
    (s) => s.id !== soru.id && !haric.includes(s.id) && !V.oturumTecih?.[s.id]
  );
  aday.sort((a, b) => {
    const oa = (a.etiketler || []).filter((t) => et.includes(t)).length;
    const ob = (b.etiketler || []).filter((t) => et.includes(t)).length;
    return ob - oa || Math.abs(a.gun - soru.gun) - Math.abs(b.gun - soru.gun);
  });
  return aday.slice(0, n);
}

/* ---------------- yardımcılar ---------------- */
const $ = (s, k = document) => k.querySelector(s);
const $$ = (s, k = document) => [...k.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const tarihTR = (iso) => {
  const aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"];
  const gunler = ["Pazar","Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi"];
  const d = new Date(iso + "T12:00:00");
  return `${d.getDate()} ${aylar[d.getMonth()]} ${d.getFullYear()} ${gunler[d.getDay()]}`;
};
const paragrafla = (t) =>
  String(t || "").split(/\n{2,}/).map((p) => `<p>${esc(p).replace(/\n/g, "<br>")}</p>`).join("");
function sinavSayaci() {
  const simdi = new Date();
  const sinav = new Date(V.meta.sinav.tarih + "T10:00:00");
  return Math.max(0, Math.ceil((sinav - simdi) / 86400000));
}
function bugunKampGunu() {
  const iso = new Date().toISOString().slice(0, 10);
  const g = V.program.gunler.find((x) => x.tarih === iso);
  if (g) return g.no;
  const sinav = new Date(V.meta.sinav.tarih + "T12:00:00");
  const fark = Math.round((sinav - new Date()) / 86400000);
  return Math.min(10, Math.max(1, 10 - fark + 1));
}
function topbar(b) { $("#topbar-baslik").textContent = b; }
function gunSecici(aktif) {
  return `<div class="gun-secici">${V.program.gunler.map((g) =>
    `<a class="gun-chip ${g.no === aktif ? "aktif" : ""}" href="#/gun/${g.no}">${g.no}. Gün</a>`).join("")}</div>`;
}
function gunlukRozet() {
  const g = gunlukSayac();
  return `<span class="badge ${g.sayi >= GUNLUK_HEDEF ? "yesil" : "turuncu"}">Bugün: ${g.sayi}/${GUNLUK_HEDEF} soru</span>`;
}

/* ---------------- ROUTER ---------------- */
window.addEventListener("hashchange", route);
window.addEventListener("load", async () => {
  await veriYukle();
  await kayitYukle();
  $("#menu-btn").onclick = () => $(".sidebar").classList.toggle("acik");
  route();
});
function route() {
  const h = location.hash.replace(/^#\//, "") || "panel";
  const p = h.split("/");
  $$(".nav a").forEach((a) => a.classList.toggle("aktif", a.dataset.r === p[0] || (p[0] === "gun" && a.dataset.r === "panel") || (p[0] === "ders" && a.dataset.r === "konular")));
  $(".sidebar").classList.remove("acik");
  window.scrollTo(0, 0);
  const v = $("#view");
  if (V.oturum && p[0] !== "coz") V.oturum = null;
  if (V.denemeOturum && p[0] !== "deneme-run") V.denemeOturum = null;
  switch (p[0]) {
    case "panel": return viewGun(bugunKampGunu());
    case "gun": return viewGun(+p[1]);
    case "konular": return p[1] ? viewKonularDers(p[1]) : viewKonular();
    case "ders": return viewDers(p[1], +p[2]);
    case "akis": return viewDersAkis(p[1]);
    case "coz":
      if (!p[1]) return viewCozHub();
      if (p[1] === "test") return viewCoz("test", p[3] || "", decodeURIComponent(p.slice(4).join("/") || ""), p[2]);
      return viewCoz(p[1], p[2] || "", decodeURIComponent(p[3] || ""), null);
    case "denemeler": return viewDenemeler();
    case "deneme": return viewDenemeBilgi(p[1]);
    case "deneme-run": return viewDenemeRun(p[1]);
    case "hata": return viewHata();
    case "istatistik": return viewIstatistik();
    case "ayarlar": return viewAyarlar();
    default: v.innerHTML = "<p>Sayfa bulunamadı. <a href='#/panel'>Ana sayfaya dön</a></p>";
  }
}

/* =========================================================
   GÜN REHBERİ
   ========================================================= */
function viewGun(no) {
  const g = V.program.gunler.find((x) => x.no === no);
  if (!g) return (location.hash = "#/panel");
  const den = V.denemeler.denemeler.find((d) => d.gun === no);
  const kalan = sinavSayaci();
  $("#kalan-gun").innerHTML = `SINAVA<br><b>${kalan}</b>gün`;
  const maraton = no <= 2;
  const gk = gunlukSayac();

  /* ADIM 1 — konu anlatımı */
  const okumaSatir = g.dersler.map((d) => {
    const okundu = V.kayit.okunan[okumaAnahtar(d.ders, no)];
    return `<div class="adim-satir ${okundu ? "okundu" : ""}">
      <span class="badge ${d.ders}">${DERSLER[d.ders].ad}</span>
      <div class="adim-bilgi">
        <b>${esc((d.konular || []).slice(0, 4).join(" · "))}${(d.konular || []).length > 4 ? "…" : ""}</b>
        <span>${okundu ? "✅ Okundu" : maraton ? "Konu Maratonu — tüm konular hızlı tur" : "Zayıf konularını farklı anlatımla tekrar et"}</span>
      </div>
      <a class="btn kucuk" href="${maraton ? `#/konular/${d.ders}` : `#/ders/${d.ders}/${no}`}">📖 ${maraton ? "Konu Turu" : "Anlatım"}</a>
    </div>`;
  }).join("");

  /* ADIM 2 — 10'luk testler */
  const testSatir = g.dersler.map((d) => `
    <div class="adim-satir">
      <span class="badge ${d.ders}">${DERSLER[d.ders].ad}</span>
      <div class="adim-bilgi">
        <b>10'luk test — ${esc(d.konular[0])} ağırlıklı</b>
        <span>Her 10 soruda otomatik kontrol · yanlışlar söylenir · ustalana kadar tekrar</span>
      </div>
      <a class="btn kucuk yesil" href="#/coz/test/gun/${d.ders}/${no}">✏️ 10 Soru</a>
    </div>`).join("");

  const denemeBitti = V.kayit.denemeler.some((x) => x.id === den.id);
  const okunanAdet = g.dersler.filter((d) => V.kayit.okunan[okumaAnahtar(d.ders, no)]).length;

  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">🎯 ${g.no}. GÜN REHBERİ · ${tarihTR(g.tarih)}</span>
      <h1>${esc(g.tema)}</h1>
      <p>${esc(g.hedef)}</p>
      <div class="sayac">
        <div><b>${kalan}</b>gün kaldı</div>
        <div><b>${g.no}/10</b>kamp günü</div>
        <div><b>${gk.sayi}/${GUNLUK_HEDEF}</b>bugün çözülen</div>
        <div><b>${okunanAdet}/5</b>tur tamam</div>
      </div>
    </div>

    ${gunSecici(g.no)}
    ${(() => {
      const od = Object.entries(V.kayit.odak || {}).sort((a, b) => b[1] - a[1]);
      if (!od.length) return "";
      return `<div class="kart" style="border-left:4px solid var(--turuncu);margin:14px 0">
        <b>🎯 Dünkü Denemeden Gelen Odakların</b>
        <p class="meta">Son denemenin sonuçları bugünün planını şekillendirdi: bu konular soru seçiminde öncelikli.</p>
        <div class="aks">${od.slice(0, 10).map(([k, n]) => {
          const ko = k.split("|")[1];
          return `<span class="chip chip-sm">${esc(ko)}${n > 1 ? " ×" + n : ""}</span>`;
        }).join("")}</div>
        <div class="adim-alt"><a class="btn turuncu kucuk" href="#/coz/odak/0">🎯 Odak Testi Çöz (10 soru)</a></div>
      </div>`;
    })()}

    <div class="yol-haritasi">
      <div class="adim-kart">
        <div class="adim-no">1</div>
        <div class="adim-ic">
          <h2>📖 ${maraton ? "Konu Maratonı — Tüm Konuları Bitir" : "Konu Tekrarı (Farklı Anlatım)"}</h2>
          <p class="meta">${maraton
            ? "İlk 2 günde 5 dersin TÜM konuları bitirilir: her konunun özeti (hızlı tur) + farklı anlatımı (hikâye + tuzak) var. Oku, sonra 10'luk teste geç."
            : "Yanlış yaptığın konuları farklı anlatımla (hikâye + tuzak) tekrar oku. Konu Anlatımları'nda tüm konuların hızlı turu var."}</p>
          ${okumaSatir}
          <div class="adim-alt">
            <a class="btn seffaf kucuk" href="#/konular">📖 Konu Anlatımları (hızlı tur + modüller)</a>
          </div>
        </div>
      </div>

      <div class="adim-kart">
        <div class="adim-no">2</div>
        <div class="adim-ic">
          <h2>✏️ 10'ar Soruluk Testler ${gunlukRozet()}</h2>
          <p class="meta">Her 10 soruda otomatik kontrol yapılır, yanlışların çözümleri + <b>farklı anlatım</b> kartları gösterilir; o konulara uygun <b>yeni sorular</b> gelir ve tekrar çözersin. <b>Usta olana kadar</b> devam!</p>
          ${testSatir}
          <div class="adim-alt">
            ${Object.keys(DERSLER).map((x) => `<a class="btn yesil kucuk" href="#/akis/${x}">📅 ${DERSLER[x].ad} Akışı</a>`).join("")}
            <a class="btn turuncu kucuk" href="#/coz/telafi/0/0">🔁 Yanlış Telafisi</a>
            <a class="btn seffaf kucuk" href="#/hata">🎯 Hata Atölyesi</a>
          </div>
        </div>
      </div>

      <div class="adim-kart">
        <div class="adim-no">3</div>
        <div class="adim-ic">
          <h2>📝 Gün Sonu Denemesi</h2>
          <p class="meta">${esc(den.ad)} — ${den.soru_sayisi} soru / ${den.sure_dk} dakika. ${esc(g.deneme.odak)}. Sonuçların ertesi günün planını şekillendirir.</p>
          <div class="adim-satir">
            <span class="badge gri">${denemeBitti ? "Çözüldü ✅" : "Sıradaki adım"}</span>
            <div class="adim-bilgi"><b>${esc(g.deneme.ad)}</b><span>4 yanlış 1 doğruyu götürür · net = D − Y/4</span></div>
            <a class="btn yesil kucuk" href="#/deneme/${den.id}">📝 Denemeyi Aç</a>
          </div>
        </div>
      </div>
    </div>

    <details class="kart" style="margin-top:18px">
      <summary style="cursor:pointer;font-weight:700">⏱ Dakika dakika plan (istersen)</summary>
      <ul class="zaman" style="margin-top:12px">${g.plan.map((x) => `
        <li><div class="dk">${x.dk ? x.dk + " dk" : "5 dk"}</div>
        <div class="gorev"><b>${esc(x.baslik)}</b><span>${esc(x.aciklama)}</span></div></li>`).join("")}
      </ul>
    </details>

    <div class="kart motivasyon"><b>💬 ${esc(g.motivasyon)}</b></div>
  `;
  topbar(`${g.no}. Gün — ${g.tema.split("—")[0]}`);
}

/* =========================================================
   GÜNLÜK DERS AKIŞI — konu testleri → karışık (10'ar soru, ders başına 500)
   ========================================================= */
function viewDersAkis(d) {
  if (!DERSLER[d]) return (location.hash = "#/coz");
  const a = dersAkisKaydi(d);
  const dg = dersGunlukKaydi(d);
  const konular = V.konuListe[d] || [];
  const biten = a.biten.length;
  const sonraki = dersAkisSonraki(d);
  const hepsiBitti = biten >= konular.length;
  const konuSatir = konular.map((x, i) => {
    const bitti = a.biten.includes(x.konu);
    const sirada = sonraki.tip === "konu" && sonraki.konu === x.konu;
    return `<div class="adim-satir ${bitti ? "okundu" : ""}">
      <span class="badge ${bitti ? "yesil" : sirada ? "turuncu" : "gri"}">${bitti ? "✓" : i + 1}</span>
      <div class="adim-bilgi"><b>${esc(x.konu)}</b><span>${x.adet} soru · 10'luk test</span></div>
      ${sirada ? `<a class="btn kucuk yesil" href="#/coz/test/konu/${d}/${encodeURIComponent(x.konu)}">▶ Sıradaki</a>`
        : `<a class="btn kucuk seffaf" href="#/coz/test/konu/${d}/${encodeURIComponent(x.konu)}">${bitti ? "Tekrar" : "Test"}</a>`}
    </div>`;
  }).join("");
  const karisikKilit = !hepsiBitti;
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">📅 GÜNLÜK DERS AKIŞI ${gunlukRozet()}</span>
      <h1>${DERSLER[d].ad} — bugün ${DERS_HEDEF} soru</h1>
      <p>Önce <b>konuların testleri</b> (10'ar soru, sırayla): son konu bitene kadar karışık test yok. Konular bitince <b>tüm konulardan karışık testlere</b> geçersin. Her test 10 sorudur, bitince otomatik kontrol yapılır.</p>
      <div class="sayac">
        <div><b>${dg.sayi}/${DERS_HEDEF}</b>bugün bu ders</div>
        <div><b>${biten}/${konular.length}</b>konu testi bitti</div>
        <div><b>${gunlukSayac().sayi}/${GUNLUK_HEDEF}</b>bugün toplam</div>
      </div>
    </div>
    <div class="baslik-satir"><h2>1️⃣ Konu Testleri — ${hepsiBitti ? "hepsi bitti ✅" : biten + " bitti, " + (konular.length - biten) + " kaldı"}</h2></div>
    <div class="card">${konuSatir || "<p class='meta'>Konu yok.</p>"}</div>
    <div class="baslik-satir"><h2>2️⃣ Karışık Testler — tüm konulardan</h2></div>
    <div class="card">
      <p class="meta">${karisikKilit ? "🔒 Önce konu testlerini bitir (kalan: " + (konular.length - biten) + "). Bittiğinde bu bölüm açılır." : "Tüm konular bitti! Karışık testlerle devam et — her 10 soruda otomatik kontrol."}</p>
      <div class="aks">
        ${karisikKilit
          ? `<button class="btn" disabled>Karışık Test (kilitli)</button>`
          : `<a class="btn yesil" href="#/coz/karisik/${d}">🔀 Karışık Test (10 soru)</a>
             <a class="btn turuncu" href="#/coz/karisik/${d}">🔀 Bir Daha (yeni 10)</a>`}
      </div>
    </div>
    <div class="aks" style="margin:18px 0 40px">
      ${sonraki.tip === "konu" ? `<a class="btn yesil" href="#/coz/test/konu/${d}/${encodeURIComponent(sonraki.konu)}">🚀 Devam — Sıradaki Konu Testi</a>`
        : `<a class="btn yesil" href="#/coz/karisik/${d}">🚀 Devam — Karışık Test</a>`}
      <a class="btn seffaf" href="#/coz">Test menüsü</a>
      ${Object.keys(DERSLER).filter((x) => x !== d).map((x) => `<a class="btn seffaf kucuk" href="#/akis/${x}">${DERSLER[x].ad}</a>`).join("")}
    </div>`;
  topbar(`${DERSLER[d].ad} — Günlük Akış`);
}

/* =========================================================
   KONU ANLATIMLARI — hızlı tur (maraton) + modüller
   ========================================================= */
function viewKonular() {
  const dersHtml = Object.keys(DERSLER).map((d) => {
    const liste = V.konuListe[d];
    const okunan = V.dersler[d].gunler.filter((gg) => V.kayit.okunan[okumaAnahtar(d, gg.gun)]).length;
    const konuSatir = liste.map((x) => {
      const key = konuAnahtar(d, x.konu);
      const u = V.kayit.ustalik[key];
      const oku = V.kayit.konu_okuma[key];
      const rozet = u?.usta ? `<span class="badge yesil">Usta</span>` : u ? `<span class="badge turuncu">%${ustalikOrani(key)}</span>` : "";
      return `<div class="adim-satir ${oku ? "okundu" : ""}">
        <div class="adim-bilgi">
          <b>${esc(x.konu)} ${rozet}</b>
          <span>${esc((V.konuYeniden[konuAnahtar(d, x.konu)]?.ozet || "").slice(0, 90))}${(V.konuYeniden[key]?.ozet || "").length > 90 ? "…" : ""}</span>
        </div>
        <div class="adim-butonlar">
          <button class="btn kucuk seffaf" onclick="konuAc('${d}', this)" data-konu="${esc(x.konu)}">📖 Hızlı Tur + Farklı Anlatım</button>
          <a class="btn kucuk" href="#/coz/test/konu/${d}/${encodeURIComponent(x.konu)}">✏️ 10 Soru</a>
        </div>
      </div>`;
    }).join("");
    return `<div class="ders-kart ${d}" style="margin-bottom:16px">
      <h3>${DERSLER[d].ad}</h3>
      <p class="meta">${liste.length} konu · ${V.sorular[d].length} soru · ${okunan}/10 modül okundu</p>
      ${konuSatir}
      <div class="aksiyonlar" style="margin-top:10px">
        <a class="btn kucuk" href="#/konular/${d}">📚 10 derin modül</a>
        <a class="btn kucuk yesil" href="#/coz/maraton/${d}/0">🚀 ${DERSLER[d].ad} Maratonu</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">📖 KONU ANLATIMLARI</span>
      <h1>Hızlı Tur + Farklı Anlatım — ${Object.values(V.konuListe).reduce((a, b) => a + b.length, 0)} konu</h1>
      <p><b>İlk 2 günde tüm konuları buradan bitir:</b> her konunun özeti, sınav tuzağı ve <b>farklı anlatımı</b> (hikâye ile) var. Okuduktan sonra hemen 10 soruluk test çöz; yanlış yaptıkça sistem konuyu yeniden, başka türlü anlatır.</p>
      <div class="sayac"><div><b>${Object.keys(V.kayit.konu_okuma).length}</b>konu okundu</div>
      <div><b>${Object.values(V.kayit.ustalik).filter((u) => u.usta).length}</b>konuda usta</div>
      <div>${gunlukRozet()}</div></div>
    </div>
    ${dersHtml}`;
  topbar("Konu Anlatımları");
}

function viewKonularDers(d) {
  const dObj = V.dersler[d];
  if (!dObj) return (location.hash = "#/konular");
  const satirlar = dObj.gunler.map((gg) => {
    const okundu = V.kayit.okunan[okumaAnahtar(d, gg.gun)];
    return `<div class="adim-satir ${okundu ? "okundu" : ""}">
      <div class="gun-no mini">${gg.gun}</div>
      <div class="adim-bilgi"><b>${esc(gg.baslik)}</b><span>${esc((gg.konular || []).join(" · "))}${okundu ? " · ✅ Okundu" : ""}</span></div>
      <div class="adim-butonlar">
        <a class="btn kucuk" href="#/ders/${d}/${gg.gun}">📖 Oku</a>
        <a class="btn kucuk seffaf" href="#/coz/test/gun/${d}/${gg.gun}">✏️ 10 Soru</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">📖 ${DERSLER[d].ad.toUpperCase()} — DERİN MODÜLLER</span>
      <h1>${DERSLER[d].ad} — 10 konu modülü</h1>
      <p>Detaylı anlatım isteyenler için. Kısa tur için <a href="#/konular" style="text-decoration:underline">Konu Anlatımları</a> sayfasına dön.</p>
    </div>
    <div class="kart">${satirlar}</div>`;
  topbar(`Konu Anlatımları · ${DERSLER[d].ad}`);
}

function viewDers(d, gun) {
  const dObj = V.dersler[d];
  if (!dObj) return (location.hash = "#/konular");
  const g = dObj.gunler.find((x) => x.gun === gun) || dObj.gunler[0];
  const sonraki = dObj.gunler.find((x) => x.gun === g.gun + 1);
  const gunlukSoru = V.sorular[d].filter((s) => s.gun === g.gun);
  const konular = [...new Set(gunlukSoru.map((s) => s.konu))];
  const okundu = V.kayit.okunan[okumaAnahtar(d, g.gun)];
  $("#view").innerHTML = `
    <div class="anlatim">
      <div class="ust-yol"><a href="#/konular">Konu Anlatımları</a> → <a href="#/konular/${d}">${DERSLER[d].ad}</a> → ${g.gun}. Modül</div>
      <span class="badge ${d}">${DERSLER[d].ad}</span>
      <h2 style="margin-top:8px">${g.gun}. ${esc(g.baslik)}</h2>
      ${g.kilit ? `<div class="kilit">🔑 ${esc(g.kilit)}</div>` : ""}
      ${paragrafla(g.giris)}
      ${Object.entries(g.bolumler).map(([ad, html]) => `<h3>${esc(ad)}</h3>${paragrafla(html)}`).join("")}
      ${Object.entries(g.yontemler).map(([ad, html]) => `<div class="yontem-kutu"><h4>🧭 ${esc(ad)}</h4>${paragrafla(html)}</div>`).join("")}
      ${g.sik_hatalar.length ? `<div class="hata"><h4>⚠️ Sık Yapılan Hatalar</h4><ul>${g.sik_hatalar.map((s) => `<li>${esc(s)}</li>`).join("")}</ul></div>` : ""}
      ${g.kart ? `<div class="kart-cep"><h4>🃏 Cebe Kart — bu cebinde dursun</h4>${paragrafla(g.kart)}</div>` : ""}
      ${g.agiz_tekrari.length ? `<h3>🗣 Ağız Tekrarı (sesli cevapla)</h3><ul>${g.agiz_tekrari.map((s) => `<li>${esc(s)}</li>`).join("")}</ul>` : ""}

      <div class="sonraki-adim">
        <h3>✅ Sıradaki adım: 10'luk Test</h3>
        <p class="meta">Okuduktan sonra testi çöz. Yanlış yaparsan konu <b>farklı anlatım</b>la tekrar anlatılır ve o konudan yeni sorular gelir.</p>
        <div class="sonuc-satir">
          <button class="btn yesil" id="okudum-btn">${okundu ? "✅ Okundu" : "📖 Okudum"}</button>
          <a class="btn" href="#/coz/test/gun/${d}/${g.gun}">✏️ 10 Soruluk Test</a>
          ${sonraki ? `<a class="btn seffaf" href="#/ders/${d}/${sonraki.gun}">Sonraki modül →</a>` : `<a class="btn seffaf" href="#/konular/${d}">← Modül listesi</a>`}
        </div>
        ${konular.length ? `<div class="konu-soru-link"><b>Konuya göre 10'luk test:</b>
          ${konular.map((k) => `<a class="chip" href="#/coz/test/konu/${d}/${encodeURIComponent(k)}">${esc(k)}</a>`).join("")}
        </div>` : ""}
      </div>
    </div>`;
  topbar(`${DERSLER[d].ad} · ${g.gun}. Modül`);
  $("#okudum-btn").onclick = () => {
    V.kayit.okunan[okumaAnahtar(d, g.gun)] = true; kaydet();
    $("#okudum-btn").textContent = "✅ Okundu";
    if (gunlukSoru.length) location.hash = `#/coz/test/gun/${d}/${g.gun}`;
  };
}

/* hızlı tur kartı */
window.konuAc = (d, btn) => {
  const konu = btn.dataset.konu;
  const key = konuAnahtar(d, konu);
  const k = V.konuYeniden[key] || {};
  V.kayit.konu_okuma[key] = true; kaydet();
  const kart = document.createElement("div");
  kart.className = "cozum";
  kart.innerHTML = `
    <h4>📖 ${esc(konu)} — Hızlı Tur</h4>
    <p>${esc(k.ozet || "Bu konunun özeti yakında eklenecek.")}</p>
    <h4>🎭 Farklı Anlatım (hikâyeyle)</h4>
    <p>${esc(k.hikaye || "")}</p>
    <h4>⚠️ Sınav Tuzağı</h4>
    <p>${esc(k.tuzak || "")}</p>
    <h4>🎯 Nasıl Sorulur?</h4>
    <p>${esc(k.nasil_sorulur || "")}</p>
    <div class="sonuc-satir">
      <a class="btn" href="#/coz/test/konu/${d}/${encodeURIComponent(konu)}">✏️ Bu Konudan 10 Soru</a>
    </div>`;
  const satir = btn.closest(".adim-satir");
  satir.classList.add("okundu");
  if (satir.nextElementSibling && satir.nextElementSibling.classList.contains("konu-kart")) {
    satir.nextElementSibling.remove();
  } else {
    kart.classList.add("konu-kart");
    satir.after(kart);
  }
};

/* =========================================================
   TEST ÇÖZ — 10'luk testler, otomatik kontrol, telafi
   ========================================================= */
function viewCozHub() {
  const dersKart = Object.keys(DERSLER).map((d) => {
    const k = V.konuListe[d];
    const usta = k.filter((x) => V.kayit.ustalik[konuAnahtar(d, x.konu)]?.usta).length;
    return `<div class="ders-kart ${d}">
      <h3>${DERSLER[d].ad} <span class="badge ${usta === k.length ? "yesil" : "gri"}">${usta}/${k.length} usta</span></h3>
      <div class="konu-ozet">${k.map((x) => {
        const key = konuAnahtar(d, x.konu);
        const u = V.kayit.ustalik[key];
        return `<a class="chip ${u?.usta ? "guclu" : u ? "zayif" : ""}" href="#/coz/test/konu/${d}/${encodeURIComponent(x.konu)}">${esc(x.konu)} (${x.adet})</a>`;
      }).join("")}</div>
      <div class="aksiyonlar">
        <a class="btn kucuk turuncu" href="#/akis/${d}">📅 Günlük Akış (${DERS_HEDEF})</a>
        <a class="btn kucuk yesil" href="#/coz/maraton/${d}/0">🚀 Maraton (10'lu)</a>
        <a class="btn kucuk turuncu" href="#/coz/telafi/${d}/0">🔁 Yanlış Telafisi</a>
        <a class="btn kucuk seffaf" href="#/coz/hata/${d}/0">🎯 Hata Atölyesi</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">✏️ TEST ÇÖZ ${gunlukRozet()}</span>
      <h1>10'ar soruluk testler — ustalana kadar</h1>
      <p>Her 10 soruda otomatik kontrol: yanlışların çözümleri ve <b>farklı anlatım</b> kartları çıkar, o konulardan <b>yeni sorular</b> gelir. Her gün yüzlerce soru; ama durumuna göre karşıına gelir, aynı soru tekrar etmez.</p>
      <div class="sayac">
        <div><b>${gunlukSayac().sayi}</b>bugün çözülen</div>
        <div><b>${Object.values(V.kayit.ustalik).filter((u) => u.usta).length}</b>usta konu</div>
        <div><b>${Object.keys(V.kayit.soru_kayit).length}</b>görülen soru</div>
      </div>
    </div>
    <div class="baslik-satir"><h2>🚀 Hızlı Başlangıç</h2></div>
    <div class="grid grid-3">
      <a class="btn blok yesil" href="#/coz/maraton/0/0">Günün Maratonu (10 soru)</a>
      <a class="btn blok turuncu" href="#/coz/telafi/0/0">Yanlış Telafisi (10 soru)</a>
      <a class="btn blok" href="#/gun/${bugunKampGunu()}">Bugünün Rehberi</a>
    </div>
    <div class="baslik-satir"><h2>🎯 Gerçek Çıkmış KPSS Soruları</h2><span class="chip chip-sm">Kaynakları etiketli · 2014–2024</span></div>
    <div class="card">
      <p class="meta">ÖSYM'nin gerçek sınav soruları; her sorunun kartında <b>kaynak yılı</b> yazar (2014-KPSS, 2016-KPSS...).</p>
      <div class="aks">
        ${["2014", "2016", "2018", "2020", "2024"].map((y) => {
          const adet = Object.values(V.tumSorular).filter((s) => s.kaynak === `${y}-KPSS`).length;
          return `<a class="btn kucuk" href="#/coz/cikmis/${y}">${y}-KPSS (${adet})</a>`;
        }).join("")}
        <a class="btn kucuk turuncu" href="#/coz/cikmis/karisik">🔀 Karışık Çıkmışlar</a>
      </div>
    </div>
    <div class="baslik-satir"><h2>📚 Konuya göre çalış</h2></div>
    <div class="grid grid-2">${dersKart}</div>`;
  topbar("Test Çöz");
}

function viewCoz(mod, ders, arg, sub) {
  {
    let liste = [], baslik = "";
    const dAd = ders && DERSLER[ders] ? DERSLER[ders].ad : null;
    if (mod === "test" && sub === "gun") {
      const gun = +arg || 0;
      const gunluk = (V.sorular[ders] || []).filter((s) => s.gun === gun);
      liste = testSeti(gunluk.length ? gunluk : (V.sorular[ders] || []), BATCH, {});
      baslik = `${dAd} ${gun}. gün — 10'luk test`;
    } else if (mod === "test" && sub === "konu") {
      liste = testSeti((V.sorular[ders] || []).filter((s) => s.konu === arg), BATCH, {});
      baslik = `${dAd} — ${arg}`;
    } else if (mod === "maraton") {
      const havuz = ders && DERSLER[ders] ? V.sorular[ders] : Object.values(V.sorular).flat();
      liste = testSeti(havuz, BATCH, { zayifOdak: true });
      baslik = `${dAd ? dAd + " " : ""}Maratonu — 10'luk tur`;
    } else if (mod === "telafi") {
      const hatalar = Object.entries(V.kayit.soru_kayit)
        .filter(([, v]) => v.y > 0)
        .map(([id]) => V.tumSorular[id])
        .filter(Boolean);
      const konular = new Set(hatalar.map((s) => konuAnahtar(s.ders, s.konu)));
      let havuz = Object.values(V.tumSorular).filter((s) => konular.has(konuAnahtar(s.ders, s.konu)));
      if (ders && DERSLER[ders]) havuz = havuz.filter((s) => s.ders === ders);
      if (!havuz.length) havuz = (ders && DERSLER[ders] ? V.sorular[ders] : Object.values(V.sorular).flat());
      liste = testSeti(havuz, BATCH, { zayifOdak: true });
      baslik = `Yanlış Telafisi — ${liste.length} soru`;
    } else if (mod === "hata") {
      const havuz = ders && DERSLER[ders] ? V.sorular[ders] : Object.values(V.sorular).flat();
      liste = testSeti(havuz, BATCH, { zayifOdak: true });
      baslik = `Hata Atölyesi — ${liste.length} soru`;
    } else if (mod === "gunluk") {
      liste = testSeti(V.sorular[ders] || [], BATCH, {});
      baslik = `${dAd} — 10'luk test`;
    } else if (mod === "karisik") {
      liste = testSeti(V.sorular[ders] || [], BATCH, {});
      baslik = `${dAd} — Karışık Test (tüm konular)`;
    } else if (mod === "odak") {
      const odaklar = new Set(Object.keys(V.kayit.odak || {}).filter((k) => V.kayit.odak[k] > 0));
      const havuz = Object.values(V.tumSorular).filter((s) => odaklar.has(konuAnahtar(s.ders, s.konu)));
      liste = testSeti(havuz.length ? havuz : Object.values(V.tumSorular), BATCH, { zayifOdak: true });
      baslik = "🎯 Deneme Odak Testi — zayıf konuların";
    } else if (mod === "cikmis") {
      const yil = ders && ders !== "karisik" ? ders : null;
      let havuz = Object.values(V.tumSorular).filter((s) => /^\d{4}-KPSS$/.test(s.kaynak || ""));
      if (yil) havuz = havuz.filter((s) => s.kaynak === `${yil}-KPSS`);
      liste = testSeti(havuz, BATCH, {});
      baslik = yil ? `🎯 ${yil}-KPSS Çıkmış Soruları` : "🎯 Çıkmış KPSS Soruları (karışık)";
    } else {
      return (location.hash = "#/coz");
    }
    if (!liste.length) return (location.hash = "#/coz");
    V.oturum = {
      mod, ders, arg, sub, baslik, sira: 0, dogru: 0, yanlis: 0,
      kuyruk: liste.map((s) => ({ s, tip: "ana" })),
      gorulen: [], bas: Date.now(),
    };
    V.oturumTecih = {};
    liste.forEach((s) => (V.oturumTecih[s.id] = 1));
  }
  renderQuiz();
}

function renderQuiz() {
  const o = V.oturum;
  if (o.sira >= o.kuyruk.length) return testKontrol();
  const { s, tip } = o.kuyruk[o.sira];
  const k = o.gorulen[o.sira];
  const ad = tip === "pekiştirme" ? "🧩 Pekiştirme (benzer soru)" : "";
  const g = gunlukSayac();
  $("#view").innerHTML = `<div class="quiz">
    <div class="quiz-ust">
      <div>
        <a class="btn kucuk seffaf" href="#/coz">← Test menüsü</a>
        <span class="badge ${o.ders}">${DERSLER[o.ders]?.ad || "Karışık"}</span>
        ${!DERSLER[o.ders] && o.baslik ? `<span class="badge turuncu">${esc(o.baslik)}</span>` : ""}
        ${ad ? `<span class="badge turuncu">${ad}</span>` : ""}
        <span class="badge gri">${esc(s.konu)}</span>
        <span class="badge gri">${["", "Kolay", "Orta", "Zor"][s.zorluk] || ""}</span>
        ${/^\d{4}-KPSS$/.test(s.kaynak || "") ? `<span class="badge turuncu" title="Gerçek ÖSYM çıkmış sorusu">🎯 ${esc(s.kaynak)}</span>` : ""}
      </div>
      <div class="quiz-sayac">Soru <b>${o.sira + 1}</b> / ${o.kuyruk.length} · ✅${o.dogru} ❌${o.yanlis} · ${gunlukRozet()}</div>
    </div>
    <div class="soru-kart">
      <div class="soru-kok">${esc(s.kok)}</div>
      ${s.siklar.map((sx, i) => {
        let cls = "sik";
        if (k) {
          cls += " kapali";
          if (i === s.dogru) cls += " dogru";
          else if (i === k.secim) cls += " yanlis";
        }
        return `<div class="${cls}" data-sik="${i}"><span class="harf">${SIK_HARF[i]}</span><span>${esc(sx)}</span></div>`;
      }).join("")}
      ${k ? cozumHtml(s, k) : ""}
      <div class="sonuc-satir" id="quiz-aks">
        ${k ? `<button class="btn" id="sonraki-btn">${o.sira + 1 >= o.kuyruk.length ? "Kontrol Et →" : "Sonraki Soru →"}</button>
              <a class="btn seffaf" href="#/ders/${s.ders}/${s.gun}">📖 Konu anlatımı</a>
              <button class="btn seffaf" onclick="isaretleGec()">İşaretle ve geç</button>`
            : `<span class="meta">Bir şıkka dokun veya klavyeden A–E ile cevapla. (Bugün ${g.sayi}/${GUNLUK_HEDEF})</span>`}
      </div>
    </div>
    <div class="benzer-not">💡 10 soru bitince <b>otomatik kontrol</b> yapılır: yanlışların çözümleri + <b>farklı anlatım</b> kartları gösterilir, o konudan yeni sorular gelir. Aynı soru bugün tekrar gelmez.</div>
  </div>`;
  $$(".sik").forEach((el) => el.onclick = () => cevapla(+el.dataset.sik));
  const sb = $("#sonraki-btn"); if (sb) sb.onclick = () => { o.sira++; renderQuiz(); };
  if (!k) {
    document.onkeydown = (e) => {
      const i = "abcde".indexOf(e.key.toLowerCase());
      if (i >= 0 && i < 5 && V.oturum && !V.oturum.gorulen[V.oturum.sira]) cevapla(i);
    };
  } else document.onkeydown = null;
}
function cozumHtml(s, k) {
  return `<div class="cozum">
    <h4>${k.dogru ? "✅ Doğru!" : "❌ Yanlış — doğrusu: " + SIK_HARF[s.dogru] + ") " + esc(s.siklar[s.dogru])}</h4>
    ${(s.cozumler || []).map((c, i) => `<div class="yontem"><b>Yöntem ${i + 1} — ${esc(c.yontem)}:</b> ${esc(c.metin)}</div>`).join("")}
    <div class="meta" style="font-size:12px">Kaynak: ${esc(s.kaynak)} · Etiketler: ${(s.etiketler || []).join(", ")}</div>
  </div>`;
}
function cevapla(i) {
  const o = V.oturum; if (!o) return;
  const { s } = o.kuyruk[o.sira];
  if (o.gorulen[o.sira]) return;
  const dogru = i === s.dogru;
  o.gorulen[o.sira] = { secim: i, dogru };
  const sk = soruKaydi(s.id); sk.son = Date.now();
  if (dogru) { sk.d++; o.dogru++; } else { sk.y++; o.yanlis++; }
  (s.etiketler || []).forEach((t) => {
    const ek = etiketKaydi(t);
    if (dogru) ek.d++; else { ek.y++; ek.tekrar++; }
  });
  ustalikGuncelle(s, dogru);
  if (dogru) {
    const ok = konuAnahtar(s.ders, s.konu);
    if (V.kayit.odak && V.kayit.odak[ok] > 0) {
      V.kayit.odak[ok]--;
      if (V.kayit.odak[ok] <= 0) delete V.kayit.odak[ok];
    }
  }
  const g = gunlukSayac();
  g.sayi++; g.ids[s.id] = 1;
  const dg = dersGunlukKaydi(s.ders); dg.sayi++; dg.ids[s.id] = 1;
  if (!dogru) {
    const ben = benzerler(s, 2, o.kuyruk.map((x) => x.s.id));
    ben.forEach((b) => { o.kuyruk.push({ s: b, tip: "pekiştirme" }); V.oturumTecih[b.id] = 1; });
  }
  kaydet();
  const cevapAdet = o.gorulen.filter(Boolean).length;
  if (cevapAdet > 0 && cevapAdet % BATCH === 0) return testKontrol();
  renderQuiz();
}
window.isaretleGec = () => { const o = V.oturum; if (o) { o.sira++; renderQuiz(); } };

/* ---------------- OTOMATİK KONTROL (checkpoint) ---------------- */
function testKontrol() {
  const o = V.oturum;
  if (!o) return (location.hash = "#/coz");
  const gorulenler = o.gorulen.map((g, i) => ({ g, i })).filter((x) => x.g);
  const batch = gorulenler.slice(-BATCH);
  const yanlislar = batch.filter((x) => !x.g.dogru).map((x) => o.kuyruk[x.i].s);
  const dogru = batch.filter((x) => x.g.dogru).length;
  const yanlis = batch.length - dogru;
  const net = (dogru - yanlis / 4).toFixed(2);
  const dk = Math.max(1, Math.round((Date.now() - o.bas) / 60000));
  V.kayit.oturumlar.push({ tarih: new Date().toISOString(), ders: o.ders, mod: o.mod, dogru, yanlis, dk });
  V.kayit.oturumlar = V.kayit.oturumlar.slice(-200);
  // konu testi bitti → günlük akışta işaretle
  if (o.mod === "test" && o.sub === "konu" && o.ders && DERSLER[o.ders]) {
    const a = dersAkisKaydi(o.ders);
    if (!a.biten.includes(o.arg)) a.biten.push(o.arg);
  }
  kaydet();

  /* yanlış konuları → farklı anlatım kartları */
  const yanliKonular = [...new Set(yanlislar.map((s) => konuAnahtar(s.ders, s.konu)))];
  const anlatimlar = yanliKonular.map((key) => {
    const k = V.konuYeniden[key] || {};
    const [d, ...rest] = key.split("|");
    const konu = rest.join("|");
    return `<div class="cozum">
      <h4>🎭 ${esc(konu)} — bu konu sana <b>farklı</b> anlatımla</h4>
      <p><b>Hızlı tur:</b> ${esc(k.ozet || "")}</p>
      <p><b>Hikâyeyle:</b> ${esc(k.hikaye || "")}</p>
      <p><b>Sınav tuzağı:</b> ${esc(k.tuzak || "")}</p>
      <div class="sonuc-satir">
        <a class="btn kucuk" href="#/coz/test/konu/${d}/${encodeURIComponent(konu)}">✏️ Bu konudan yeni 10 soru</a>
      </div>
    </div>`;
  }).join("");

  const yanlisHtml = yanlislar.map((s, i) => `<div class="soru-kart" style="margin-bottom:12px">
    <div class="quiz-ust"><span class="badge ${s.ders}">${DERSLER[s.ders].ad}</span><span class="badge gri">${esc(s.konu)}</span></div>
    <div class="soru-kok">${i + 1}. ${esc(s.kok)}</div>
    ${s.siklar.map((sx, j) => `<div class="sik ${j === s.dogru ? "dogru" : ""} kapali"><span class="harf">${SIK_HARF[j]}</span><span>${esc(sx)}</span></div>`).join("")}
    ${cozumHtml(s, { dogru: false })}
  </div>`).join("");

  const sonrakiMod = o.mod;
  const sonrakiDers = o.ders;
  const kalanVar = o.kuyruk.some((_, i) => !o.gorulen[i]);
  if (!kalanVar) { V.oturum = null; V.oturumTecih = {}; }

  $("#view").innerHTML = `<div class="quiz">
    <div class="hero">
      <span class="etiket">📋 OTOMATİK KONTROL — ${yanlis ? yanlis + " yanlış" : "HATASIZ! 🎉"}</span>
      <h1>${batch.length} soru · ${dogru} doğru, ${yanlis} yanlış</h1>
      <p>${yanlis ? "Aşağıda yanlışların çözümleri ve o konuların FARKLI ANLATIMI var. Yeni sorularla tekrar çözmeye devam et — ustalana kadar!" : "Harika! Devam edersen yeni sorular gelir; aynı soru bugün tekrar etmez."}</p>
    </div>
    <div class="net-kutu">
      <div><b style="color:var(--iyi)">${dogru}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${yanlis}</b>Yanlış</div>
      <div><b>${net}</b>Net</div>
      <div><b>${gunlukSayac().sayi}</b>Bugün</div>
    </div>
    ${yanlislar.length ? `<div class="baslik-satir"><h2>❌ Yanlışların (${yanlislar.length})</h2></div>${yanlisHtml}` : ""}
    ${anlatimlar ? `<div class="baslik-satir"><h2>🎭 Yanlış Konuların Farklı Anlatımı</h2></div>${anlatimlar}` : ""}
    <div class="sonuc-satir" style="margin:18px 0 40px">
      ${kalanVar ? `<button class="btn yesil" onclick="testDevam()">▶ Devam Et (sırada sorular var)</button>` : ""}
      ${yanliKonular.length ? `<a class="btn turuncu" href="#/coz/telafi/${sonrakiDers && DERSLER[sonrakiDers] ? sonrakiDers : "0"}/0">🔁 Bu Konulardan Yeni 10 Soru</a>` : ""}
      ${sonrakiDers && DERSLER[sonrakiDers] ? `<a class="btn turuncu" href="#/akis/${sonrakiDers}">📅 Günlük Akışa Dön</a>` : ""}
      <a class="btn yesil" href="#/coz/maraton/${sonrakiDers && DERSLER[sonrakiDers] ? sonrakiDers : "0"}/0">🚀 Karışık Devam (10 soru)</a>
      <a class="btn" href="#/gun/${bugunKampGunu()}">Günün rehberi</a>
      <a class="btn seffaf" href="#/coz">Test menüsü</a>
    </div>
    <div class="benzer-not">📊 Ustalık: ${Object.values(V.kayit.ustalik).filter((u) => u.usta).length} konuda usta · Bugün ${gunlukSayac().sayi}/${GUNLUK_HEDEF} soru${o.ders && DERSLER[o.ders] ? ` · ${DERSLER[o.ders].ad}: ${dersGunlukKaydi(o.ders).sayi}/${DERS_HEDEF}` : ""} · Aynı soru bugün tekrar gelmez.</div>
  </div>`;
  topbar("Otomatik Kontrol");
}
window.testDevam = () => {
  const o = V.oturum;
  if (!o) return (location.hash = "#/coz");
  for (let i = 0; i < o.kuyruk.length; i++) {
    if (!o.gorulen[i]) { o.sira = i; return renderQuiz(); }
  }
  return testKontrol();
};

/* =========================================================
   DENEMELER (aynı kaldı)
   ========================================================= */
function viewDenemeler() {
  const satirlar = V.denemeler.denemeler.map((d) => {
    const gecmis = V.kayit.denemeler.filter((x) => x.id === d.id).slice(-1)[0];
    return `<div class="kart" style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap">
      <div>
        <h3>${esc(d.ad)}</h3>
        <p class="meta">${d.soru_sayisi} soru · ${d.sure_dk} dk · ${d.tur === "buyuk" ? "🏆 Büyük Deneme" : "Mini deneme"} · ${d.gun}. gün</p>
      </div>
      <div style="display:flex;gap:10px;align-items:center">
        ${gecmis ? `<span class="badge yesil">Net: ${gecmis.net}</span><span class="badge gri">D${gecmis.dogru} Y${gecmis.yanlis}</span>` : `<span class="badge gri">Henüz çözülmedi</span>`}
        <a class="btn kucuk yesil" href="#/deneme/${d.id}">Aç →</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">📝 DENEMELER</span>
      <h1>Her Gün 1 Deneme — 5. ve 10. Gün Büyük Prova</h1>
      <p>Deneme sonuçların ertesi günün soru setini otomatik yönlendirir. Net = Doğru − Yanlış/4.</p></div>
    <div class="grid" style="gap:12px">${satirlar}</div>`;
  topbar("Denemeler");
}
function viewDenemeBilgi(id) {
  const d = V.denemeIdx[id]; if (!d) return (location.hash = "#/denemeler");
  $("#view").innerHTML = `<div class="quiz">
    <div class="hero"><span class="etiket">${esc(d.ad)}</span>
      <h1>${d.soru_sayisi} soru · ${d.sure_dk} dakika</h1>
      <p>${esc(d.odak)}. Gerçek sınav gibi: mola yok, telefon yok. Süre başlayınca geri sayar.</p></div>
    <div class="kart">
      <h3>Kurallar</h3>
      <ul style="margin-left:18px;font-size:14px">
        <li>Her soru 5 şıklı (A–E). Klavyeden 1–5 veya A–E ile cevap verebilirsin.</li>
        <li>Takıldığında işaretle ve geç — daha sonra geri dönersin.</li>
        <li>Bitir'de: net, konu analizi ve tüm çözümler gösterilir.</li>
        <li>Yanlışların Hata Defteri'ne işlenir; ertesi günün setinde %40 ağırlıkla gelir.</li>
      </ul>
      <div class="sonuc-satir"><a class="btn yesil" href="#/deneme-run/${id}">⏱ Süreyi Başlat</a>
      <a class="btn seffaf" href="#/gun/${d.gun}">Günün rehberine dön</a></div>
    </div>
  </div>`;
  topbar(d.ad);
}
async function viewDenemeRun(id) {
  const c = await fetch(`/api/deneme/${id}`).then((r) => r.json());
  V.denemeOturum = {
    d: c, sira: 0, cevaplar: {}, isaretli: new Set(), bas: Date.now(), sure: c.sure_dk * 60,
  };
  renderDeneme();
  clearInterval(V._sayac);
  V._sayac = setInterval(() => {
    if (!V.denemeOturum) return clearInterval(V._sayac);
    V.denemeOturum.kalan = V.denemeOturum.sure - Math.floor((Date.now() - V.denemeOturum.bas) / 1000);
    const el = $("#sure-el");
    if (el) {
      const k = Math.max(0, V.denemeOturum.kalan);
      el.textContent = `${String(Math.floor(k / 60)).padStart(2, "0")}:${String(k % 60).padStart(2, "0")}`;
      if (k <= 0) { clearInterval(V._sayac); denemeBitir(); }
    }
  }, 500);
}
function renderDeneme() {
  const o = V.denemeOturum;
  const s = o.d.soru_nesneleri[o.sira];
  const cevap = o.cevaplar[s.id];
  $("#view").innerHTML = `<div class="quiz">
    <div class="quiz-ust">
      <div><span class="badge gri">${esc(o.d.ad)}</span> <span class="badge ${s.ders}">${DERSLER[s.ders].ad}</span> <span class="badge gri">${esc(s.konu)}</span></div>
      <div style="display:flex;gap:14px;align-items:center">
        <span class="sure" id="sure-el">--:--</span>
        <button class="btn kucuk kotu" onclick="denemeBitir()">Bitir</button>
      </div>
    </div>
    <div class="deneme-grid">
      ${o.d.soru_nesneleri.map((sq, i) => {
        let cls = "deneme-hucre";
        if (i === o.sira) cls += " aktif";
        if (o.cevaplar[sq.id] != null) cls += " dolu";
        else if (o.isaretli.has(sq.id)) cls += " isaretli";
        else cls += " bos";
        return `<div class="${cls}" onclick="denemeGit(${i})">${i + 1}</div>`;
      }).join("")}
    </div>
    <div class="soru-kart">
      <div class="soru-kok">${esc(s.kok)}</div>
      ${s.siklar.map((sx, i) => `<div class="sik ${cevap === i ? "dogru" : ""}" data-sik="${i}"><span class="harf">${SIK_HARF[i]}</span><span>${esc(sx)}</span></div>`).join("")}
      <div class="sonuc-satir">
        <button class="btn seffaf" onclick="denemeGit(${o.sira - 1})" ${o.sira === 0 ? "disabled" : ""}>← Önceki</button>
        <button class="btn seffaf" onclick="denemeIsaretle()">⭐ İşaretle</button>
        ${o.sira + 1 < o.d.soru_nesneleri.length
          ? `<button class="btn" onclick="denemeGit(${o.sira + 1})">Sonraki →</button>`
          : `<button class="btn kotu" onclick="denemeBitir()">Sınavı Bitir</button>`}
      </div>
    </div>
  </div>`;
  $$(".sik").forEach((el) => el.onclick = () => {
    o.cevaplar[s.id] = +el.dataset.sik; renderDeneme();
  });
  document.onkeydown = (e) => {
    const key = e.key.toLowerCase();
    const i = "abcde12345".indexOf(key) % 5;
    if (["a","b","c","d","e","1","2","3","4","5"].includes(key) && V.denemeOturum) {
      V.denemeOturum.cevaplar[s.id] = i; renderDeneme();
    }
  };
}
window.denemeGit = (i) => { const o = V.denemeOturum; if (!o) return; o.sira = Math.max(0, Math.min(o.d.soru_nesneleri.length - 1, i)); renderDeneme(); };
window.denemeIsaretle = () => {
  const o = V.denemeOturum; const s = o.d.soru_nesneleri[o.sira];
  if (o.isaretli.has(s.id)) o.isaretli.delete(s.id); else o.isaretli.add(s.id);
  renderDeneme();
};
window.denemeBitir = function () {
  clearInterval(V._sayac);
  const o = V.denemeOturum; if (!o) return;
  let d = 0, y = 0, b = 0;
  const konular = {};
  o.d.soru_nesneleri.forEach((s) => {
    const c = o.cevaplar[s.id];
    const ek = (konular[s.ders] = konular[s.ders] || { d: 0, y: 0, b: 0 });
    const sk = soruKaydi(s.id); sk.son = Date.now();
    if (c == null) { b++; ek.b++; }
    else if (c === s.dogru) { d++; ek.d++; sk.d++; ustalikGuncelle(s, true); (s.etiketler || []).forEach((t) => etiketKaydi(t).d++); }
    else { y++; ek.y++; sk.y++; ustalikGuncelle(s, false); (s.etiketler || []).forEach((t) => { etiketKaydi(t).y++; etiketKaydi(t).tekrar++; }); }
  });
  const net = +(d - y / 4).toFixed(2);
  V.kayit.denemeler.push({ id: o.d.id, ad: o.d.ad, tarih: new Date().toISOString(), dogru: d, yanlis: y, bos: b, net, sure: Math.floor((Date.now() - o.bas) / 1000) });
  // deneme sonuçları ertesi günü yönetsin: yanlış/boşların konuları odak listesine
  V.kayit.odak = V.kayit.odak || {};
  o.d.soru_nesneleri.forEach((s) => {
    const c = o.cevaplar[s.id];
    if (c == null || c !== s.dogru) {
      const ok = konuAnahtar(s.ders, s.konu);
      V.kayit.odak[ok] = (V.kayit.odak[ok] || 0) + 1;
    }
  });
  kaydet();
  V.denemeOturum = null; document.onkeydown = null;
  const yanlislar = o.d.soru_nesneleri.filter((s) => o.cevaplar[s.id] != null && o.cevaplar[s.id] !== s.dogru);
  $("#view").innerHTML = `<div class="quiz">
    <div class="hero"><span class="etiket">🏁 DENEME BİTTİ — ${esc(o.d.ad)}</span>
      <h1>Net: ${net}</h1><p>${d} doğru, ${y} yanlış, ${b} boş. KPSS'de 4 yanlış 1 doğruyu götürür.</p></div>
    <div class="net-kutu">
      <div><b style="color:var(--iyi)">${d}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${y}</b>Yanlış</div>
      <div><b>${b}</b>Boş</div>
      <div><b>${net}</b>Net</div>
    </div>
    ${Object.keys(V.kayit.odak || {}).length ? `<div class="kart" style="border-left:4px solid var(--turuncu)"><b>🎯 Yarının Odağı (deneme sonuçlarından):</b>
      ${Object.entries(V.kayit.odak).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, n]) => {
        const [dr, ko] = k.split("|");
        return `<a class="chip chip-sm" href="#/coz/odak/0">${esc(ko)}${n > 1 ? " ×" + n : ""}</a>`;
      }).join(" ")}
      <p class="meta">Bu konular yarının planında öncelikli gelecek; doğru çözdükçe listeden silinir.</p></div>` : ""}
    <div class="baslik-satir"><h2>📊 Ders Dağılımı</h2></div>
    <div class="kart"><table><tr><th>Ders</th><th>Doğru</th><th>Yanlış</th><th>Boş</th></tr>
      ${Object.entries(konular).map(([k, v]) => `<tr><td><span class="badge ${k}">${DERSLER[k].ad}</span></td><td>${v.d}</td><td>${v.y}</td><td>${v.b}</td></tr>`).join("")}
    </table></div>
    <div class="baslik-satir"><h2>❌ Yanlışların ve Çözümleri</h2></div>
    ${yanlislar.length ? yanlislar.map((s, i) => `<div class="soru-kart" style="margin-bottom:12px">
      <div class="soru-kok">${i + 1}. ${esc(s.kok)}</div>
      ${s.siklar.map((sx, j) => `<div class="sik ${j === s.dogru ? "dogru" : ""} kapali"><span class="harf">${SIK_HARF[j]}</span><span>${esc(sx)}</span></div>`).join("")}
      ${cozumHtml(s, { dogru: false })}
    </div>`).join("") : `<div class="kart"><p>Harika! Yanlış yok 🎉</p></div>`}
    <div class="sonuc-satir" style="margin:18px 0 40px">
      <a class="btn turuncu" href="#/coz/telafi/0/0">🔁 Yanlış Telafisi (10 soru)</a>
      <a class="btn" href="#/gun/${o.d.gun}">Günün rehberine dön</a>
      <a class="btn seffaf" href="#/denemeler">Denemeler</a>
    </div>
  </div>`;
};

/* =========================================================
   HATA DEFTERİ
   ========================================================= */
function viewHata() {
  const t = Object.entries(V.kayit.etiketler).filter(([, v]) => v.y > 0)
    .sort((a, b) => b[1].y - a[1].y);
  const yanlisSorular = Object.entries(V.kayit.soru_kayit)
    .filter(([, v]) => v.y > 0)
    .sort((a, b) => (b[1].y - b[1].d) - (a[1].y - a[1].d))
    .map(([id]) => V.tumSorular[id])
    .filter(Boolean);
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">🎯 HATA DEFTERİ</span>
      <h1>Hata yaptığın yerler, kazandığın puanların fabrikası</h1>
      <p>Her yanlış için 2 benzer soru üretilir; konular farklı anlatımla tekrar edilir. Ustalana kadar tekrar!</p></div>
    <div class="baslik-satir"><h2>🔥 Zayıf Konuların</h2></div>
    <div class="kart">
      ${t.length ? t.map(([tag, v]) => `<span class="chip zayif">${esc(tag)} · ❌${v.y} ✅${v.d}</span>`).join("") : "<p class='meta'>Henüz hata yok.</p>"}
    </div>
    <div class="baslik-satir"><h2>⚔️ Saldırı — 10'luk testler</h2></div>
    <div class="grid grid-3">
      ${Object.keys(DERSLER).map((d) => `<div class="ders-kart ${d}">
        <h3>${DERSLER[d].ad}</h3>
        <p class="meta">Yanlışlarından uygun sorular</p>
        <div class="aksiyonlar"><a class="btn kucuk turuncu" href="#/coz/telafi/${d}/0">Telafi (10 soru)</a>
        <a class="btn kucuk seffaf" href="#/coz/hata/${d}/0">Atölye</a></div>
      </div>`).join("")}
    </div>
    <div class="baslik-satir"><h2>📕 Yanlış Yaptığın Sorular (${yanlisSorular.length})</h2></div>
    ${yanlisSorular.slice(0, 30).map((s, i) => {
      const k = V.kayit.soru_kayit[s.id];
      return `<div class="soru-kart" style="margin-bottom:12px">
        <div class="quiz-ust"><span class="badge ${s.ders}">${DERSLER[s.ders].ad}</span><span class="badge kirmizi">❌${k.y} ✅${k.d}</span>
        <a class="btn kucuk seffaf" href="#/ders/${s.ders}/${s.gun}">📖 Farklı anlatım</a></div>
        <div class="soru-kok">${i + 1}. ${esc(s.kok)}</div>
        <div class="meta" style="margin-top:8px">Doğru: ${SIK_HARF[s.dogru]}) ${esc(s.siklar[s.dogru])}</div>
        ${(s.cozumler || []).map((c, j) => `<div class="yontem" style="margin-top:8px"><b>Yöntem ${j + 1} — ${esc(c.yontem)}:</b> ${esc(c.metin)}</div>`).join("")}
      </div>`;
    }).join("")}`;
  topbar("Hata Defteri");
}

/* =========================================================
   İSTATİSTİK & AYARLAR
   ========================================================= */
function viewIstatistik() {
  const toplam = Object.values(V.kayit.soru_kayit);
  const d = toplam.reduce((a, x) => a + x.d, 0), y = toplam.reduce((a, x) => a + x.y, 0);
  const gunluk = {};
  Object.entries(V.kayit.soru_kayit).forEach(([id, v]) => {
    const s = V.tumSorular[id]; if (!s) return;
    const g = (gunluk[s.ders] = gunluk[s.ders] || { d: 0, y: 0 });
    g.d += v.d; g.y += v.y;
  });
  const den = V.kayit.denemeler.slice(-5);
  const okunan = Object.keys(V.kayit.okunan).length + Object.keys(V.kayit.konu_okuma).length;
  const usta = Object.values(V.kayit.ustalik).filter((u) => u.usta).length;
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">📊 İSTATİSTİK</span>
      <h1>${d + y} soru çözdün — doğruluk oranı: ${d + y ? Math.round((d / (d + y)) * 100) : 0}%</h1>
      <p>${okunan} konu okundu · ${usta} konuda ustalık · ${V.kayit.denemeler.length} deneme · Bugün ${gunlukSayac().sayi}/${GUNLUK_HEDEF} soru.</p></div>
    <div class="net-kutu">
      <div><b>${d + y}</b>Çözülen</div>
      <div><b style="color:var(--iyi)">${d}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${y}</b>Yanlış</div>
      <div><b>${usta}</b>Usta Konu</div>
    </div>
    <div class="baslik-satir"><h2>📚 Derslere Göre</h2></div>
    <div class="kart"><table><tr><th>Ders</th><th>Çözülen</th><th>Doğru</th><th>Yanlış</th><th>Başarı</th></tr>
      ${Object.keys(DERSLER).map((dd) => {
        const g = gunluk[dd] || { d: 0, y: 0 };
        const t = g.d + g.y;
        return `<tr><td><span class="badge ${dd}">${DERSLER[dd].ad}</span></td><td>${t}</td><td>${g.d}</td><td>${g.y}</td>
        <td><div class="ilerleme-cubuk"><span style="width:${t ? Math.round((g.d / t) * 100) : 0}%"></span></div></td></tr>`;
      }).join("")}
    </table></div>
    <div class="baslik-satir"><h2>🏅 Ustalık Durumu</h2></div>
    <div class="kart">${Object.entries(V.kayit.ustalik).length
      ? Object.entries(V.kayit.ustalik).map(([key, u]) => `<span class="chip ${u.usta ? "guclu" : "zayif"}">${esc(key.split("|").slice(1).join("|"))} ${u.usta ? "🎓" : "%" + ustalikOrani(key)}</span>`).join("")
      : "<p class='meta'>Henüz test çözülmedi.</p>"}</div>
    <div class="baslik-satir"><h2>📝 Son Denemeler</h2></div>
    <div class="kart"><table><tr><th>Deneme</th><th>Tarih</th><th>Net</th><th>D / Y / B</th></tr>
      ${den.length ? den.map((x) => `<tr><td>${esc(x.ad)}</td><td>${new Date(x.tarih).toLocaleDateString("tr-TR")}</td><td><b>${x.net}</b></td><td>${x.dogru} / ${x.yanlis} / ${x.bos}</td></tr>`).join("")
      : "<tr><td colspan='4' class='meta'>Henüz deneme çözülmedi.</td></tr>"}
    </table></div>`;
  topbar("İstatistik");
}

function viewAyarlar() {
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">⚙️ AYARLAR</span><h1>Veriler ve Sıfırlama</h1>
    <p>İlerlemen sunucuda (data/ilerleme/) ve tarayıcında saklanır. Sıfırdan başlamak istersen sıfırlayabilirsin.</p></div>
    <div class="kart">
      <h3>Yedekle</h3>
      <p class="meta">Tüm ilerlemeni JSON olarak indir; başka bilgisayarda geri yükle.</p>
      <div class="sonuc-satir">
        <button class="btn" onclick="disaAktar()">⬇ Dışa aktar</button>
        <label class="btn seffaf">⬆ İçe aktar<input type="file" id="yedek-dosya" style="display:none" accept="application/json"></label>
        <button class="btn kotu" onclick="sifirla()">🗑 Sıfırla</button>
      </div>
    </div>
    <div class="kart" style="margin-top:14px">
      <h3>Sınav Bilgisi</h3>
      <p class="meta">${esc(V.meta.sinav.ad)} · ${tarihTR(V.meta.sinav.tarih)}<br>${esc(V.meta.sinav.not)}</p>
    </div>`;
  topbar("Ayarlar");
  $("#yedek-dosya").onchange = (e) => {
    const f = e.target.files[0]; if (!f) return;
    const ok = new FileReader();
    ok.onload = () => {
      try {
        V.kayit = JSON.parse(ok.result);
        const b = bosKayit();
        for (const k of Object.keys(b)) if (V.kayit[k] === undefined) V.kayit[k] = b[k];
        kaydet(); alert("Yedek yüklendi!"); location.hash = "#/panel";
      } catch { alert("Geçersiz dosya"); }
    };
    ok.readAsText(f);
  };
}
window.disaAktar = () => {
  const blob = new Blob([JSON.stringify(V.kayit, null, 1)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = "kpss-kamp-yedek.json"; a.click();
};
window.sifirla = async () => {
  if (!confirm("TÜM ilerleme silinecek. Emin misin?")) return;
  await fetch(`/api/sifirla/${KULLANICI}`);
  V.kayit = bosKayit(); kaydet(); location.hash = "#/panel"; route();
};
