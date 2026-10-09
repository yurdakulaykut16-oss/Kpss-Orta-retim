/* =========================================================
   KPSS Ortaöğretim — 10 Günlük Hızlandırılmış Kamp
   Sade akış: 1) Konu anlatımını oku → 2) Soru çöz → 3) Deneme
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

const V = {
  meta: null, program: null, dersler: {}, sorular: {}, soruIdx: {},
  denemeler: null, denemeIdx: {}, kayit: null, oturum: null, denemeOturum: null,
  tumSorular: {}, etiketIdx: {}, konuListe: {},
};

/* ---------------- ilerleme ---------------- */
function bosKayit() {
  return { kullanici: KULLANICI, gorevler: {}, soru_kayit: {}, etiketler: {}, denemeler: [], oturumlar: [], okunan: {} };
}
async function kayitYukle() {
  try {
    const r = await fetch(`/api/ilerleme/${KULLANICI}`);
    V.kayit = await r.json();
    if (!V.kayit || !V.kayit.etiketler) V.kayit = bosKayit();
    if (!V.kayit.okunan) V.kayit.okunan = {};
    if (!V.kayit.gorevler) V.kayit.gorevler = {};
    if (!V.kayit.oturumlar) V.kayit.oturumlar = [];
    if (!V.kayit.denemeler) V.kayit.denemeler = [];
    if (!V.kayit.soru_kayit) V.kayit.soru_kayit = {};
  } catch {
    V.kayit = JSON.parse(localStorage.getItem("kpss-kayit") || "null") || bosKayit();
    if (!V.kayit.okunan) V.kayit.okunan = {};
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

/* ---------------- veri ---------------- */
async function veriYukle() {
  const [meta, program, denemeler] = await Promise.all([
    fetch("/api/meta").then((r) => r.json()),
    fetch("/api/program").then((r) => r.json()),
    fetch("/api/denemeler").then((r) => r.json()),
  ]);
  V.meta = meta; V.program = program; V.denemeler = denemeler;
  V.denemeIdx = {}; denemeler.denemeler.forEach((d) => (V.denemeIdx[d.id] = d));
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
    // güne göre sıralı konu listesi
    V.konuListe[d] = [...konular.entries()]
      .map(([konu, liste]) => ({ konu, adet: liste.length, gunler: [...new Set(liste.map((s) => s.gun))].sort((a, b) => a - b) }))
      .sort((a, b) => (a.gunler[0] ?? 0) - (b.gunler[0] ?? 0) || a.konu.localeCompare(b.konu, "tr"));
  }
}

/* ---------------- adaptif motor ---------------- */
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
function gorulduSirasi(id) {
  const k = V.kayit.soru_kayit[id];
  return k && k.son ? k.son : 0;
}
function gunlukSet(ders, gun, adet = 20) {
  const havuz = V.sorular[ders];
  const gunluk = havuz.filter((s) => s.gun === gun);
  const karisik = havuz.filter((s) => s.gun !== gun);
  const sirala = (a) =>
    [...a].sort((x, y) => {
      const kx = V.kayit.soru_kayit[x.id], ky = V.kayit.soru_kayit[y.id];
      const hx = kx ? kx.y - kx.d : -1, hy = ky ? ky.y - ky.d : -1;
      return hy - hx || gorulduSirasi(x.id) - gorulduSirasi(y.id);
    });
  const ana = sirala(gunluk);
  const zayif = sirala(karisik.filter((s) =>
    (s.etiketler || []).some((t) => etiketZayiflik(t) > 0)
  ));
  const kalan = sirala(karisik);
  const sec = [];
  const it = (l) => { for (const s of l) if (!sec.includes(s) && sec.length < adet) sec.push(s); };
  const gunPayi = Math.min(ana.length, Math.round(adet * 0.6));
  it(ana.slice(0, gunPayi)); it(zayif); it(kalan); it(ana);
  return sec.slice(0, adet);
}
function konuSeti(ders, konu) {
  return (V.sorular[ders] || []).filter((s) => s.konu === konu);
}
function hataSeti(ders, limit = 500) {
  const havuz = [...V.sorular[ders]];
  havuz.sort((x, y) => {
    const kx = V.kayit.soru_kayit[x.id], ky = V.kayit.soru_kayit[y.id];
    const hx = kx ? kx.y * 2 - kx.d : -0.5, hy = ky ? ky.y * 2 - ky.d : -0.5;
    return hy - hx || gorulduSirasi(x.id) - gorulduSirasi(y.id);
  });
  return havuz.slice(0, limit);
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
    case "coz": return p[1] ? viewCoz(p[1], p[2], decodeURIComponent(p[3] || "")) : viewCozHub();
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
   GÜN REHBERİ — "Bugün ne yapacağım?" (panel + gün sayfası)
   ========================================================= */
function viewGun(no) {
  const g = V.program.gunler.find((x) => x.no === no);
  if (!g) return (location.hash = "#/panel");
  const den = V.denemeler.denemeler.find((d) => d.gun === no);
  const kalan = sinavSayaci();
  $("#kalan-gun").innerHTML = `SINAVA<br><b>${kalan}</b>gün`;

  /* --- ADIM 1: konu anlatımları --- */
  const okumaSatir = g.dersler.map((d) => {
    const okundu = V.kayit.okunan[okumaAnahtar(d.ders, no)];
    return `<div class="adim-satir ${okundu ? "okundu" : ""}">
      <span class="badge ${d.ders}">${DERSLER[d.ders].ad}</span>
      <div class="adim-bilgi">
        <b>${esc(d.konular.join(" · "))}</b>
        <span>${okundu ? "✅ Okundu" : "Okuma süresi ~" + Math.round((d.sure_min || 15) * 0.45) + " dk"}</span>
      </div>
      <a class="btn kucuk" href="#/ders/${d.ders}/${no}">${okundu ? "📖 Tekrar Oku" : "📖 Konu Anlatımını Oku"}</a>
    </div>`;
  }).join("");

  /* --- ADIM 2: soru çözümü --- */
  const soruSatir = g.dersler.map((d) => {
    if (!d.soru_sayisi) return "";
    return `<div class="adim-satir">
      <span class="badge ${d.ders}">${DERSLER[d.ders].ad}</span>
      <div class="adim-bilgi">
        <b>${d.soru_sayisi} soru — ${esc(d.konular[0])} ağırlıklı</b>
        <span>Yanlışta 2 benzer soru eklenir · ~${d.sure_min} dk</span>
      </div>
      <a class="btn kucuk yesil" href="#/coz/gunluk/${d.ders}/${no}">✏️ Soruları Çöz</a>
    </div>`;
  }).join("");

  /* --- ADIM 3: deneme --- */
  const denemeBitti = V.kayit.denemeler.some((x) => x.id === den.id);

  /* gün özeti: okunan + çözülen */
  const okunanAdet = g.dersler.filter((d) => V.kayit.okunan[okumaAnahtar(d.ders, no)]).length;

  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">🎯 ${g.no}. GÜN REHBERİ · ${tarihTR(g.tarih)}</span>
      <h1>${esc(g.tema)}</h1>
      <p>${esc(g.hedef)}</p>
      <div class="sayac">
        <div><b>${kalan}</b>gün kaldı</div>
        <div><b>${g.no}/10</b>kamp günü</div>
        <div><b>${okunanAdet}/5</b>anlatım okundu</div>
        <div><b>~2 sa</b>bugün çalış</div>
      </div>
    </div>

    ${gunSecici(g.no)}

    <div class="yol-haritasi">
      <div class="adim-kart">
        <div class="adim-no">1</div>
        <div class="adim-ic">
          <h2>📖 Konu Anlatımlarını Oku</h2>
          <p class="meta">Önce anlatımları oku. Konu anlatımları sade; sadece okuyarak öğrenilecek şekilde yazıldı. Her dersin altında "Cebe Kart" ve "Ağız Tekrarı" var.</p>
          ${okumaSatir}
          <div class="adim-alt">
            <a class="btn seffaf kucuk" href="#/konular">Tüm konu anlatımları →</a>
          </div>
        </div>
      </div>

      <div class="adim-kart">
        <div class="adim-no">2</div>
        <div class="adim-ic">
          <h2>✏️ Soruları Çöz</h2>
          <p class="meta">Anlatımı okuduktan sonra o dersin sorularını çöz. Yanlış yaparsan <b>2 benzer soru</b> anında gelir; konu anlatımı da hatırlatılır.</p>
          ${soruSatir}
          <div class="adim-alt">
            <a class="btn seffaf kucuk" href="#/coz">Konuya göre soru çöz →</a>
            <a class="btn turuncu kucuk" href="#/hata">Hata Atölyesi →</a>
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
   KONU ANLATIMLARI — sadece okuma bölümü
   ========================================================= */
function viewKonular() {
  const html = Object.keys(DERSLER).map((d) => {
    const okunan = V.dersler[d].gunler.filter((gg) => V.kayit.okunan[okumaAnahtar(d, gg.gun)]).length;
    return `<a class="ders-kart ${d}" href="#/konular/${d}">
      <h3>${DERSLER[d].ad}</h3>
      <p class="meta">10 konu anlatımı · ${V.sorular[d].length} soru bankada</p>
      <div class="konu-ozet">${V.dersler[d].gunler.map((gg) => `<span class="chip">${gg.gun}. ${esc(gg.baslik.slice(0, 26))}${gg.baslik.length > 26 ? "…" : ""}</span>`).join("")}</div>
      <div class="aksiyonlar"><span class="btn kucuk">${okunan}/10 okundu →</span></div>
    </a>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">📖 KONU ANLATIMLARI</span>
      <h1>Sadece oku — 5 ders, 50 konu anlatımı</h1>
      <p>Burada sadece konu anlatımları var; soru yok, telaş yok. Bir ders seç, konu anlatımını oku, sonra "Soru Çöz" bölümünden o konunun sorularını çöz.</p>
    </div>
    <div class="grid grid-2">${html}</div>`;
  topbar("Konu Anlatımları");
}

function viewKonularDers(d) {
  const dObj = V.dersler[d];
  if (!dObj) return (location.hash = "#/konular");
  const satirlar = dObj.gunler.map((gg) => {
    const okundu = V.kayit.okunan[okumaAnahtar(d, gg.gun)];
    const konuSoru = V.sorular[d].filter((s) => s.gun === gg.gun).length;
    return `<div class="adim-satir ${okundu ? "okundu" : ""}">
      <div class="gun-no mini">${gg.gun}</div>
      <div class="adim-bilgi">
        <b>${esc(gg.baslik)}</b>
        <span>${esc((gg.konular || []).join(" · "))}${okundu ? " · ✅ Okundu" : ""}</span>
      </div>
      <div class="adim-butonlar">
        <a class="btn kucuk" href="#/ders/${d}/${gg.gun}">📖 Oku</a>
        ${konuSoru ? `<a class="btn kucuk seffaf" href="#/coz/gunluk/${d}/${gg.gun}">✏️ Soru</a>` : ""}
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">📖 KONU ANLATIMLARI · ${DERSLER[d].ad.toUpperCase()}</span>
      <h1>${DERSLER[d].ad} — 10 konu anlatımı</h1>
      <p>İstediğin konudan başla. Her konu anlatımının sonunda o konunun sorularını çözebileceğin buton var.</p>
    </div>
    <div class="kart">${satirlar}</div>
    <div class="sonuc-satir" style="margin-top:16px">
      <a class="btn seffaf" href="#/konular">← Tüm dersler</a>
      <a class="btn turuncu" href="#/coz/karma/${d}/0">✏️ ${DERSLER[d].ad} soruları</a>
    </div>`;
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
      <div class="ust-yol"><a href="#/konular">Konu Anlatımları</a> → <a href="#/konular/${d}">${DERSLER[d].ad}</a> → ${g.gun}. Konu</div>
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
        <h3>✅ Okudun mu? Sıradaki adım: Soru Çöz</h3>
        <p class="meta">Bu konu anlatımını bitirdiysen aşağıdaki sorularla pekiştir. Yanlış yaparsan 2 benzer soru eklenir.</p>
        <div class="sonuc-satir">
          <button class="btn yesil" id="okudum-btn">${okundu ? "✅ Okundu olarak işaretli" : "📖 Okudum — sorulara geç"}</button>
          ${gunlukSoru.length ? `<a class="btn" href="#/coz/gunluk/${d}/${g.gun}">✏️ Bu Günün ${gunlukSoru.length} Sorusunu Çöz</a>` : ""}
          ${sonraki ? `<a class="btn seffaf" href="#/ders/${d}/${sonraki.gun}">Sonraki konu →</a>` : `<a class="btn seffaf" href="#/konular/${d}">← Konu listesi</a>`}
        </div>
        ${konular.length ? `<div class="konu-soru-link">
          <b>Konuya göre çöz:</b>
          ${konular.map((k) => `<a class="chip" href="#/coz/konu/${d}/${encodeURIComponent(k)}">${esc(k)} (${gunlukSoru.filter((s) => s.konu === k).length} soru)</a>`).join("")}
        </div>` : ""}
      </div>
    </div>`;
  topbar(`${DERSLER[d].ad} · ${g.gun}. Konu Anlatımı`);
  const btn = $("#okudum-btn");
  btn.onclick = () => {
    V.kayit.okunan[okumaAnahtar(d, g.gun)] = true; kaydet();
    btn.textContent = "✅ Okundu olarak işaretli";
    if (gunlukSoru.length) location.hash = `#/coz/gunluk/${d}/${g.gun}`;
  };
}

/* =========================================================
   SORU ÇÖZ — önce seçim, sonra quiz
   ========================================================= */
function viewCozHub() {
  const gunler = V.program.gunler.map((g) => `
    <a class="gun-chip" href="#/gun/${g.no}">${g.no}. Gün</a>`).join("");
  const dersKart = Object.keys(DERSLER).map((d) => {
    const k = V.konuListe[d];
    return `<div class="ders-kart ${d}">
      <h3>${DERSLER[d].ad}</h3>
      <p class="meta">${k.length} konu · ${V.sorular[d].length} soru</p>
      <div class="konu-ozet">${k.slice(0, 8).map((x) => `<a class="chip" href="#/coz/konu/${d}/${encodeURIComponent(x.konu)}">${esc(x.konu)} (${x.adet})</a>`).join("")}${k.length > 8 ? `<a class="chip" href="#/konular/${d}">…tümü</a>` : ""}</div>
      <div class="aksiyonlar">
        <a class="btn kucuk" href="#/coz/konu-ders/${d}/">Karışık çöz (${V.sorular[d].length})</a>
        <a class="btn kucuk turuncu" href="#/coz/hata/${d}/0">🎯 Hata Atölyesi</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">✏️ SORU ÇÖZ</span>
      <h1>Nasıl soru çözmek istersin?</h1>
      <p>Günün soruları için "Bugünün Rehberi"ni kullan. Buradan tek bir konuya çalışabilir, konu konu veya karışık soru çözebilirsin.</p>
    </div>
    <div class="baslik-satir"><h2>📅 Günlük set için gün seç</h2></div>
    <div class="gun-secici">${gunler}</div>
    <div class="baslik-satir"><h2>📚 Derse göre — konu seç, o konunun sorularını çöz</h2></div>
    <div class="grid grid-2">${dersKart}</div>`;
  topbar("Soru Çöz");
}

function viewCoz(mod, ders, arg) {
  if (!ders || !DERSLER[ders]) return (location.hash = "#/coz");
  if (mod === "konu-ders") {
    // dersin karışık tüm soruları — konu seçim sayfası
    return viewKonuSec(ders);
  }
  if (!V.oturum || V.oturum.mod !== mod || V.oturum.ders !== ders || V.oturum.arg !== arg) {
    let liste, baslik = "";
    if (mod === "gunluk") {
      const gun = +arg || 0;
      liste = gunlukSet(ders, gun, 20);
      baslik = `${gun}. Gün — günlük set`;
    } else if (mod === "konu") {
      liste = konuSeti(ders, arg);
      baslik = `${arg} — ${liste.length} soru`;
      if (!liste.length) return (location.hash = "#/coz");
    } else if (mod === "hata") {
      liste = hataSeti(ders, 500);
      baslik = `Hata Atölyesi — ${liste.length} soru`;
    } else if (mod === "karma") {
      liste = hataSeti(ders, 60);
      baslik = `${DERSLER[ders].ad} karışık — ${liste.length} soru`;
    } else return (location.hash = "#/coz");
    V.oturum = {
      mod, ders, arg, baslik, sira: 0, dogru: 0, yanlis: 0,
      kuyruk: liste.map((s) => ({ s, tip: "ana" })),
      gorulen: [], bas: Date.now(),
    };
    V.oturumTecih = {};
    liste.forEach((s) => (V.oturumTecih[s.id] = 1));
  }
  renderQuiz();
}

function viewKonuSec(ders) {
  const k = V.konuListe[ders];
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">✏️ ${DERSLER[ders].ad.toUpperCase()} — KONU SEÇ</span>
      <h1>Bir konu seç, sadece o konunun sorularını çöz</h1>
      <p>İstersen karışık da çözebilirsin. Yanlış yaptığın konular Hata Defteri'ne eklenir.</p>
    </div>
    <div class="kart">
      ${k.map((x) => `<div class="adim-satir">
        <div class="gun-no mini">${x.gunler[0] || "-"}</div>
        <div class="adim-bilgi"><b>${esc(x.konu)}</b><span>${x.adet} soru · ${x.gunler.map((gg) => gg + ". gün").join(", ")}</span></div>
        <a class="btn kucuk" href="#/coz/konu/${ders}/${encodeURIComponent(x.konu)}">Çöz →</a>
      </div>`).join("")}
      <div class="adim-alt" style="margin-top:14px">
        <a class="btn" href="#/coz/karma/${ders}/0">🔀 Karışık çalış (${V.sorular[ders].length} soru)</a>
        <a class="btn turuncu" href="#/coz/hata/${ders}/0">🎯 Hata Atölyesi (≤500)</a>
      </div>
    </div>`;
  topbar(`${DERSLER[ders].ad} · Konu Seç`);
}

function renderQuiz() {
  const o = V.oturum;
  if (o.sira >= o.kuyruk.length) return quizBitti();
  const { s, tip } = o.kuyruk[o.sira];
  const k = o.gorulen[o.sira];
  const ad = tip === "pekiştirme" ? "🧩 Pekiştirme (benzer soru)" : tip === "tekrar" ? "🔁 Tekrar" : "";
  $("#view").innerHTML = `<div class="quiz">
    <div class="quiz-ust">
      <div>
        <a class="btn kucuk seffaf" href="#/coz">← Çözüm menüsü</a>
        <span class="badge ${o.ders}">${DERSLER[o.ders].ad}</span>
        ${ad ? `<span class="badge turuncu">${ad}</span>` : ""}
        <span class="badge gri">${esc(s.konu)}</span>
        <span class="badge gri">${["", "Kolay", "Orta", "Zor"][s.zorluk] || ""}</span>
      </div>
      <div class="quiz-sayac">Soru <b>${o.sira + 1}</b> / ${o.kuyruk.length} · ✅${o.dogru} ❌${o.yanlis}</div>
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
        ${k ? `<button class="btn" id="sonraki-btn">${o.sira + 1 >= o.kuyruk.length ? "Sonuçları Gör →" : "Sonraki Soru →"}</button>
              <a class="btn seffaf" href="#/ders/${s.ders}/${s.gun}">📖 Konu anlatımını oku</a>
              <button class="btn seffaf" onclick="isaretleGec()">İşaretle ve geç</button>`
            : `<span class="meta">Bir şıkka dokun veya klavyeden A–E ile cevapla.</span>`}
      </div>
    </div>
    <div class="benzer-not">💡 Yanlış yaparsan o konudan <b>2 benzer soru</b> kuyruğa eklenir. Aynı konuda hata birikirse konu anlatımı hatırlatılır.</div>
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
  if (!dogru) {
    const ben = benzerler(s, 2, o.kuyruk.map((x) => x.s.id));
    ben.forEach((b) => { o.kuyruk.push({ s: b, tip: "pekiştirme" }); V.oturumTecih[b.id] = 1; });
  }
  kaydet();
  renderQuiz();
}
window.isaretleGec = () => { const o = V.oturum; if (o) { o.sira++; renderQuiz(); } };

function quizBitti() {
  const o = V.oturum;
  const toplam = o.dogru + o.yanlis;
  const net = (o.dogru - o.yanlis / 4).toFixed(2);
  const dk = Math.max(1, Math.round((Date.now() - o.bas) / 60000));
  V.kayit.oturumlar.push({ tarih: new Date().toISOString(), ders: o.ders, mod: o.mod, dogru: o.dogru, yanlis: o.yanlis, dk });
  V.kayit.oturumlar = V.kayit.oturumlar.slice(-200);
  kaydet();
  const zayif = zayifEtiketler(o.ders, 8);
  const gun = (o.mod === "gunluk" ? +o.arg : (o.kuyruk[0] ? o.kuyruk[0].s.gun : 1));
  V.oturum = null; V.oturumTecih = {};
  $("#view").innerHTML = `<div class="quiz">
    <div class="hero"><span class="etiket">🎉 TEBRİKLER — TUR BİTTİ</span>
      <h1>${toplam} soruda ${o.dogru} doğru, ${o.yanlis} yanlış</h1>
      <p>${dk} dakikada tamamladın. ${o.yanlis ? "Yanlışların Hata Defteri'ne eklendi." : "Hatasız! 🎉"}</p></div>
    <div class="net-kutu">
      <div><b style="color:var(--iyi)">${o.dogru}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${o.yanlis}</b>Yanlış</div>
      <div><b>${net}</b>Net</div>
      <div><b>${dk}′</b>Süre</div>
    </div>
    <div class="sonuc-satir" style="margin-top:18px">
      <a class="btn" href="#/gun/${gun}">Günün rehberine dön</a>
      <a class="btn turuncu" href="#/hata">🎯 Hata Defteri</a>
      <a class="btn seffaf" href="#/coz">Başka soru seti</a>
      <a class="btn seffaf" href="#/ders/${o.ders}/${gun}">📖 Konu anlatımına dön</a>
    </div>
  </div>`;
}

/* =========================================================
   DENEMELER
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
    else if (c === s.dogru) { d++; ek.d++; sk.d++; (s.etiketler || []).forEach((t) => etiketKaydi(t).d++); }
    else { y++; ek.y++; sk.y++; (s.etiketler || []).forEach((t) => { etiketKaydi(t).y++; etiketKaydi(t).tekrar++; }); }
  });
  const net = +(d - y / 4).toFixed(2);
  V.kayit.denemeler.push({ id: o.d.id, ad: o.d.ad, tarih: new Date().toISOString(), dogru: d, yanlis: y, bos: b, net, sure: Math.floor((Date.now() - o.bas) / 1000) });
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
      <a class="btn" href="#/gun/${o.d.gun}">Günün rehberine dön</a>
      <a class="btn turuncu" href="#/hata">🎯 Hata Defteri'ne bak</a>
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
      <p>En çok yanlış yaptığın konular aşağıda. Her yanlış için 2 benzer soru üretilir. Ertesi günün 20 sorusunun 8'i buradan gelir.</p></div>
    <div class="baslik-satir"><h2>🔥 Zayıf Konuların</h2></div>
    <div class="kart">
      ${t.length ? t.map(([tag, v]) => `<span class="chip zayif">${esc(tag)} · ❌${v.y} ✅${v.d}</span>`).join("") : "<p class='meta'>Henüz hata yok.</p>"}
    </div>
    <div class="baslik-satir"><h2>⚔️ Zayıf Konu Atağı — soru çöz</h2></div>
    <div class="grid grid-3">
      ${Object.keys(DERSLER).map((d) => `<div class="ders-kart ${d}">
        <h3>${DERSLER[d].ad}</h3>
        <p class="meta">Zayıf konulardan ≤500 soruluk kişisel set</p>
        <div class="aksiyonlar"><a class="btn kucuk turuncu" href="#/coz/hata/${d}/0">Saldırıyı başlat</a></div>
      </div>`).join("")}
    </div>
    <div class="baslik-satir"><h2>📕 Yanlış Yaptığın Sorular (${yanlisSorular.length})</h2></div>
    ${yanlisSorular.slice(0, 30).map((s, i) => {
      const k = V.kayit.soru_kayit[s.id];
      return `<div class="soru-kart" style="margin-bottom:12px">
        <div class="quiz-ust"><span class="badge ${s.ders}">${DERSLER[s.ders].ad}</span><span class="badge kirmizi">❌${k.y} ✅${k.d}</span>
        <a class="btn kucuk seffaf" href="#/ders/${s.ders}/${s.gun}">📖 Konu anlatımı</a></div>
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
  const okunan = Object.keys(V.kayit.okunan).length;
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">📊 İSTATİSTİK</span>
      <h1>${d + y} soru çözdün — doğruluk oranı: ${d + y ? Math.round((d / (d + y)) * 100) : 0}%</h1>
      <p>${okunan}/50 konu anlatımı okundu · ${V.kayit.denemeler.length} deneme çözüldü.</p></div>
    <div class="net-kutu">
      <div><b>${d + y}</b>Çözülen</div>
      <div><b style="color:var(--iyi)">${d}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${y}</b>Yanlış</div>
      <div><b>${V.kayit.denemeler.length}</b>Deneme</div>
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
        if (!V.kayit.okunan) V.kayit.okunan = {};
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
