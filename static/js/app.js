/* =========================================================
   KPSS Ortaöğretim — 10 Günlük Hızlandırılmış Kamp
   Uygulama motoru: adaptif soru seçimi, hata defteri, deneme
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
};

/* ---------------- ilerleme ---------------- */
function bosKayit() {
  return { kullanici: KULLANICI, gorevler: {}, soru_kayit: {}, etiketler: {}, denemeler: [], oturumlar: [] };
}
async function kayitYukle() {
  try {
    const r = await fetch(`/api/ilerleme/${KULLANICI}`);
    V.kayit = await r.json();
    if (!V.kayit || !V.kayit.etiketler) V.kayit = bosKayit();
  } catch {
    V.kayit = JSON.parse(localStorage.getItem("kpss-kayit") || "null") || bosKayit();
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
  // her sorunun dersine göre genel index
  V.tumSorular = {}; V.etiketIdx = {};
  for (const d of Object.keys(DERSLER))
    for (const s of V.sorular[d]) {
      V.tumSorular[s.id] = s;
      (s.etiketler || []).forEach((t) => {
        (V.etiketIdx[t] = V.etiketIdx[t] || []).push(s.id);
      });
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
  // önce görülmemişler, sonra eskiler
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
  const gun = Math.max(0, Math.ceil((sinav - simdi) / 86400000));
  return gun;
}
function bugunKampGunu() {
  const iso = new Date().toISOString().slice(0, 10);
  const g = V.program.gunler.find((x) => x.tarih === iso);
  if (g) return g.no;
  // sınavdan geriye say: 24 Ekim = 10. gün
  const sinav = new Date(V.meta.sinav.tarih + "T12:00:00");
  const simdi = new Date();
  const fark = Math.round((sinav - simdi) / 86400000); // 25 ekim -> 0
  const no = 10 - fark + 1; // 24 ekim (fark=1) -> 10
  return Math.min(10, Math.max(1, no));
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
  $$(".nav a").forEach((a) => a.classList.toggle("aktif", a.dataset.r === p[0]));
  $(".sidebar").classList.remove("acik");
  window.scrollTo(0, 0);
  const v = $("#view");
  if (V.oturum && p[0] !== "coz") V.oturum = null;
  if (V.denemeOturum && p[0] !== "deneme-run") V.denemeOturum = null;
  switch (p[0]) {
    case "panel": return viewPanel();
    case "takvim": return viewTakvim();
    case "gun": return viewGun(+p[1]);
    case "kitaplik": return viewKitaplik();
    case "ders": return viewDers(p[1], +p[2]);
    case "coz": return viewCoz(p[1], p[2], +p[3]);
    case "denemeler": return viewDenemeler();
    case "deneme": return viewDenemeBilgi(p[1]);
    case "deneme-run": return viewDenemeRun(p[1]);
    case "hata": return viewHata();
    case "istatistik": return viewIstatistik();
    case "ayarlar": return viewAyarlar();
    default: v.innerHTML = "<p>Sayfa bulunamadı.</p>";
  }
}

/* ---------------- PANEL ---------------- */
function viewPanel() {
  const gun = bugunKampGunu();
  const g = V.program.gunler.find((x) => x.no === gun);
  const kalan = sinavSayaci();
  $("#kalan-gun").innerHTML = `SINAVA<br><b>${kalan}</b>gün`;
  const gorevler = g.plan.filter((x) => x.tip !== "kapanis" || true);
  let dk = 0;
  const planHtml = g.plan.map((x, i) => {
    const anahtar = `g${g.no}-p${i}`;
    const d = V.kayit.gorevler[anahtar] ? "dolu" : "";
    const sure = x.tip === "deneme" || x.tip === "deneme-buyuk" ? x.dk || (x.tip === "deneme-buyuk" ? 40 : 12) : x.dk;
    const etiket = sure ? `${sure} dk` : "5 dk";
    return `<li>
      <input class="tik ${d}" type="checkbox" data-gorev="${anahtar}" ${d ? "checked" : ""}>
      <div class="dk">${etiket}</div>
      <div class="gorev"><b>${esc(x.baslik)}</b><span>${esc(x.aciklama)}</span></div>
    </li>`;
  }).join("");

  const dersHtml = g.dersler.map((d) => {
    const info = DERSLER[d.ders];
    const bitti = V.kayit.gorevler[`g${g.no}-d-${d.ders}`];
    return `<div class="ders-kart ${d.ders}">
      <span class="badge ${d.ders}">${info.ad}</span>
      <h3>${d.konular[0]}</h3>
      <div class="konular">${d.konular.map(esc).join(" · ")}${d.soru_sayisi ? `<br><b>${d.soru_sayisi} soru</b> · ~${d.sure_min} dk` : "<br>Özet tekrar"}</div>
      <div class="aksiyonlar">
        <a class="btn kucuk seffaf" href="#/ders/${d.ders}/${g.no}">📖 Anlatım</a>
        ${d.soru_sayisi ? `<a class="btn kucuk" href="#/coz/gunluk/${d.ders}/${g.no}">✏️ ${d.soru_sayisi} Soru</a>` : ""}
        <button class="btn kucuk turuncu" onclick="hataAtolyesi('${d.ders}')">🎯 Hata Atölyesi</button>
      </div>
    </div>`;
  }).join("");

  const zayif = zayifEtiketler("tarih", 3).concat(zayifEtiketler("cografya", 2), zayifEtiketler("vatandaslik", 2), zayifEtiketler("turkce", 2), zayifEtiketler("guncel", 1));
  const zayifHtml = zayif.length
    ? zayif.map((t) => {
        const k = V.kayit.etiketler[t];
        return `<span class="chip ${k && k.y > 0 ? "zayif" : ""}">${esc(t)}${k ? ` · ${k.y} yanlış` : ""}</span>`;
      }).join("")
    : `<span class="meta">Henüz hata kaydı yok — soru çözdükçe burası dolacak.</span>`;

  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">🚀 HIZLANDIRILMIŞ KAMP · ${g.no}. GÜN</span>
      <h1>${esc(g.tema)}</h1>
      <p>${esc(g.hedef)}</p>
      <div class="sayac">
        <div><b>${kalan}</b>gün kaldı</div>
        <div><b>${g.no}/10</b>kamp günü</div>
        <div><b>2 sa</b>bugünkü plan</div>
        <div><b>${g.dersler.length}</b>ders bugün</div>
      </div>
    </div>

    <div class="baslik-satir"><h2>📋 Bugünün Dakika Dakika Planı</h2>
      <a class="btn kucuk turuncu" href="#/gun/${g.no}">Gün sayfası →</a></div>
    <div class="kart"><ul class="zaman" id="plan-liste">${planHtml}</ul></div>

    <div class="baslik-satir"><h2>📚 Bugünün Dersleri</h2></div>
    <div class="grid grid-2">${dersHtml}</div>

    <div class="baslik-satir"><h2>✍️ Gün Sonu Denemesi</h2></div>
    <div class="kart">
      <h3>${esc(g.deneme.ad)} — ${g.deneme.soru_sayisi} soru / ${g.deneme.sure_dk} dk</h3>
      <p class="meta">${esc(g.deneme.odak)}. 4 yanlış 1 doğruyu götürür; net = D − Y/4.</p>
      <div style="margin-top:12px"><a class="btn yesil" href="#/deneme/${V.denemeler.denemeler.find(d=>d.gun===g.no).id}">Denemeye Başla →</a></div>
    </div>

    <div class="baslik-satir"><h2>🎯 Zayıf Konuların (Hata Defteri)</h2><a class="btn kucuk seffaf" href="#/hata">Tümü</a></div>
    <div class="kart">${zayifHtml}</div>

    <div class="baslik-satir"><h2>💬 Günün Motivasyonu</h2></div>
    <div class="kart"><p class="meta">${esc(g.motivasyon)}</p></div>
  `;
  $$("#plan-liste .tik").forEach((t) =>
    t.onchange = () => {
      V.kayit.gorevler[t.dataset.gorev] = t.checked;
      t.classList.toggle("dolu", t.checked);
      kaydet();
    }
  );
  topbar(`${g.no}. Gün — ${g.tema.split("—")[0]}`);
}

function topbar(b) { $("#topbar-baslik").textContent = b; }

/* ---------------- TAKVİM ---------------- */
function viewTakvim() {
  const kartlar = V.program.gunler.map((g) => {
    const bitenler = g.plan.filter((_, i) => V.kayit.gorevler[`g${g.no}-p${i}`]).length;
    const oran = Math.round((bitenler / g.plan.length) * 100);
    return `<a class="gun-kart ${oran === 100 ? "bitti" : ""}" href="#/gun/${g.no}">
      <div class="gun-no">${g.no}</div>
      <div class="govde">
        <h3>${esc(g.tema)}</h3>
        <div class="meta">${tarihTR(g.tarih)} · ${g.dersler.map((d) => DERSLER[d.ders].ad).join(", ")}</div>
        <div class="ilerleme-cubuk" style="margin-top:8px"><span style="width:${oran}%"></span></div>
      </div>
      <span class="badge ${oran === 100 ? "yesil" : oran > 0 ? "turuncu" : "gri"}">${oran}%</span>
    </a>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">🗓 10 GÜNLÜK KAMP TAKVİMİ</span>
      <h1>15–24 Ekim 2026 · Sınav: 25 Ekim Pazar</h1>
      <p>Her gün 5 ders sırayla: Tarih → Coğrafya → Vatandaşlık → Türkçe → Güncel. Sonunda gün sonu denemesi. Hataların ertesi güne miras kalır!</p>
    </div>
    <div class="grid" style="gap:12px">${kartlar}</div>
    <div class="baslik-satir"><h2>📌 Temel Kurallar</h2></div>
    <div class="kart"><ul style="margin-left:18px">${V.program.temel_kurallar.map((k) => `<li style="margin-bottom:6px;font-size:14px">${esc(k)}</li>`).join("")}</ul></div>`;
  topbar("10 Günlük Kamp Takvimi");
}

/* ---------------- GÜN SAYFASI ---------------- */
function viewGun(no) {
  const g = V.program.gunler.find((x) => x.no === no);
  if (!g) return (location.hash = "#/takvim");
  const den = V.denemeler.denemeler.find((d) => d.gun === no);
  $("#view").innerHTML = `
    <div class="hero">
      <span class="etiket">${g.no}. GÜN · ${tarihTR(g.tarih)}</span>
      <h1>${esc(g.tema)}</h1>
      <p>${esc(g.hedef)}</p>
    </div>
    <div class="baslik-satir"><h2>⏱ 2 Saatlik Çekirdek Plan</h2></div>
    <div class="kart"><ul class="zaman">${g.plan.map((x) => `
      <li><div class="dk">${x.dk ? x.dk + " dk" : "5 dk"}</div>
      <div class="gorev"><b>${esc(x.baslik)}</b><span>${esc(x.aciklama)}</span></div></li>`).join("")}
    </ul></div>

    <div class="baslik-satir"><h2>📚 Ders Blokları</h2></div>
    <div class="grid grid-2">
      ${g.dersler.map((d) => `<div class="ders-kart ${d.ders}">
        <span class="badge ${d.ders}">${DERSLER[d.ders].ad}</span>
        <h3>${esc(d.konular[0])}</h3>
        <div class="konular">${d.konular.map(esc).join(" · ")}</div>
        <div class="aksiyonlar">
          <a class="btn kucuk seffaf" href="#/ders/${d.ders}/${no}">📖 Anlatım</a>
          ${d.soru_sayisi ? `<a class="btn kucuk" href="#/coz/gunluk/${d.ders}/${no}">✏️ 20 Soru</a>` : ""}
          <button class="btn kucuk turuncu" onclick="hataAtolyesi('${d.ders}')">🎯 Hata Atölyesi (≤500)</button>
        </div></div>`).join("")}
    </div>

    <div class="baslik-satir"><h2>✍️ Gün Sonu Denemesi</h2></div>
    <div class="kart">
      <h3>${esc(g.deneme.ad)}</h3>
      <p class="meta">${g.deneme.soru_sayisi} soru · ${g.deneme.sure_dk} dakika · ${esc(g.deneme.odak)}</p>
      <div style="margin-top:12px"><a class="btn yesil" href="#/deneme/${den.id}">Denemeyi Aç →</a></div>
    </div>

    <div class="baslik-satir"><h2>🚀 Genişletilmiş Bloklar (istediğin kadar)</h2></div>
    <div class="grid grid-2">
      ${g.genisletilmis.map((x) => `<div class="kart"><h3>${esc(x.baslik)}</h3>
        <p class="meta">${esc(x.aciklama)}</p>
        ${x.max_soru ? `<p class="meta" style="margin-top:6px"><b>Tavan: ${x.max_soru} soru</b></p>` : x.sure_dk ? `<p class="meta" style="margin-top:6px"><b>~${x.sure_dk} dk</b></p>` : ""}
      </div>`).join("")}
    </div>

    <div class="baslik-satir"><h2>💬 Motivasyon</h2></div>
    <div class="kart"><p class="meta">${esc(g.motivasyon)}</p></div>`;
  topbar(`${no}. Gün`);
}

/* ---------------- KİTAPLIK & DERS ---------------- */
function viewKitaplik() {
  const html = Object.keys(DERSLER).map((d) => {
    const gunler = V.dersler[d].gunler.map((gg) => `
      <a class="chip" href="#/ders/${d}/${gg.gun}">${gg.gun}. ${esc(gg.baslik.slice(0, 28))}${gg.baslik.length > 28 ? "…" : ""}</a>`).join("");
    const n = V.sorular[d].length;
    return `<div class="ders-kart ${d}">
      <h3>${DERSLER[d].ad}</h3>
      <p class="meta">10 konu modülü · ${n} soru bankada</p>
      <div style="margin:10px 0">${gunler}</div>
      <div class="aksiyonlar">
        <button class="btn kucuk turuncu" onclick="hataAtolyesi('${d}')">🎯 Hata Atölyesi</button>
        <a class="btn kucuk seffaf" href="#/coz/hata/${d}/0">Karışık çalış</a>
      </div>
    </div>`;
  }).join("");
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">📖 DERS KÜTÜPHANESİ</span>
    <h1>5 Ders · 50 Konu Modülü · ${Object.values(V.sorular).reduce((a, b) => a + b.length, 0)} Soru</h1>
    <p>Konu anlatımları meslek lisesi seviyesinde, sade ve sınav odaklı. Her modülde 2 farklı soru çözüm yöntemi + sık yapılan hatalar + cebe kart özet var.</p></div>
    <div class="grid grid-2">${html}</div>`;
  topbar("Ders Kütüphanesi");
}

function viewDers(d, gun) {
  const dObj = V.dersler[d];
  if (!dObj) return (location.hash = "#/kitaplik");
  const g = dObj.gunler.find((x) => x.gun === gun) || dObj.gunler[0];
  const sonraki = dObj.gunler.find((x) => x.gun === g.gun + 1);
  $("#view").innerHTML = `
    <div class="anlatim">
      <span class="badge ${d}">${DERSLER[d].ad}</span>
      <h2 style="margin-top:8px">${g.gun}. ${esc(g.baslik)}</h2>
      ${g.kilit ? `<div class="kilit">🔑 ${esc(g.kilit)}</div>` : ""}
      ${paragrafla(g.giris)}
      ${g.bolumler.map((b) => `<h3>${esc(b.baslik)}</h3>${paragrafla(b.html)}`).join("")}
      ${g.yontemler.map((y) => `<div class="yontem-kutu"><h4>🧭 ${esc(y.ad)}</h4>${paragrafla(y.html)}</div>`).join("")}
      ${g.sik_hatalar.length ? `<div class="hata"><h4>⚠️ Sık Yapılan Hatalar</h4><ul>${g.sik_hatalar.map((s) => `<li>${esc(s)}</li>`).join("")}</ul></div>` : ""}
      ${g.kart ? `<div class="kart-cep"><h4>🃏 Cebe Kart — bu cebinde dursun</h4>${paragrafla(g.kart)}</div>` : ""}
      ${g.agiz_tekrari.length ? `<h3>🗣 Ağız Tekrarı (sesli cevapla)</h3><ul>${g.agiz_tekrari.map((s) => `<li>${esc(s)}</li>`).join("")}</ul>` : ""}
      <div class="sonuc-satir">
        <a class="btn" href="#/coz/gunluk/${d}/${g.gun}">✏️ Bu Konudan 20 Soru Çöz</a>
        <button class="btn turuncu" onclick="hataAtolyesi('${d}')">🎯 Hata Atölyesi</button>
        ${sonraki ? `<a class="btn seffaf" href="#/ders/${d}/${sonraki.gun}">Sonraki Modül →</a>` : `<a class="btn seffaf" href="#/kitaplik">← Kütüphane</a>`}
      </div>
    </div>`;
  topbar(`${DERSLER[d].ad} · ${g.gun}. Modül`);
}

/* ---------------- SORU ÇÖZME (QUİZ) ---------------- */
function viewCoz(mod, ders, gun) {
  if (!V.oturum || V.oturum.mod !== mod || V.oturum.ders !== ders || V.oturum.gun !== gun) {
    let liste;
    if (mod === "gunluk") liste = gunlukSet(ders, gun, gun ? 20 : 20);
    else if (mod === "hata") liste = hataSeti(ders, 500);
    else if (mod === "etiket") liste = (V.etiketIdx[ders] || []).map((id) => V.tumSorular[id]);
    else liste = hataSeti(ders, 50);
    V.oturum = {
      mod, ders, gun, sira: 0, dogru: 0, yanlis: 0, kuyruk: liste.map((s) => ({ s, tip: "ana" })),
      gorulen: [], bas: Date.now(), bitis: false,
    };
    V.oturumTecih = {};
    liste.forEach((s) => (V.oturumTecih[s.id] = 1));
  }
  renderQuiz();
}
function renderQuiz() {
  const o = V.oturum;
  if (o.sira >= o.kuyruk.length) return quizBitti();
  const { s, tip } = o.kuyruk[o.sira];
  const k = o.gorulen[o.sira];
  const ad = tip === "pekiştirme" ? "🧩 Pekiştirme sorusu (benzer)" : tip === "tekrar" ? "🔁 Tekrar sorusu" : "";
  $("#view").innerHTML = `<div class="quiz">
    <div class="quiz-ust">
      <div>
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
              <button class="btn seffaf" onclick="konuTekrari(${JSON.stringify(s.ders).replace(/"/g, "&quot;")},${s.gun})">📖 Konu anlatımına dön</button>
              <button class="btn seffaf" onclick="isaretleGec()">İşaretle ve geç</button>`
            : `<span class="meta">Klavyeden A–E ile de cevap verebilirsin. Bir şıkka dokun.</span>`}
      </div>
    </div>
    <div class="benzer-not">💡 <b>Nasıl çalışır?</b> Yanlış yaparsan o konudan <b>2 benzer soru</b> anında kuyruğa girer; konudaki yanlışların 2'yi geçerse konu anlatımı tekrar hatırlatılır. Hataların ertesi günün setinde %40 ağırlıkla geri gelir.</div>
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
    const etY = (s.etiketler || []).map((t) => V.kayit.etiketler[t]).filter(Boolean);
    if (etY.some((e) => e.y >= 2)) {
      // konu tekrarı kartı: anlatımı hatırlat
      o.kuyruk.splice(o.sira + 1, 0, { s, tip: "tekrar-tekrar", konuHatirlat: true });
    }
  }
  kaydet();
  renderQuiz();
}
function isaretleGec() { const o = V.oturum; if (o) { o.sira++; renderQuiz(); } }
function konuTekrari(ders, gun) {
  const g = (V.oturum && V.oturum.gun) || gun || 1;
  location.hash = `#/ders/${ders}/${g}`;
}
function hataAtolyesi(ders) { location.hash = `#/coz/hata/${ders}/0`; }
window.hataAtolyesi = hataAtolyesi; window.konuTekrari = konuTekrari; window.isaretleGec = isaretleGec;

function quizBitti() {
  const o = V.oturum;
  const toplam = o.dogru + o.yanlis;
  const net = (o.dogru - o.yanlis / 4).toFixed(2);
  const dk = Math.max(1, Math.round((Date.now() - o.bas) / 60000));
  // oturum kaydı
  V.kayit.oturumlar.push({ tarih: new Date().toISOString(), ders: o.ders, mod: o.mod, dogru: o.dogru, yanlis: o.yanlis, dk });
  V.kayit.oturumlar = V.kayit.oturumlar.slice(-200);
  kaydet();
  const zayif = zayifEtiketler(o.ders, 8);
  V.oturum = null; V.oturumTecih = {};
  $("#view").innerHTML = `<div class="quiz">
    <div class="hero"><span class="etiket">🎉 OTURUM BİTTİ</span><h1>${toplam} soruda ${o.dogru} doğru, ${o.yanlis} yanlış</h1>
    <p>${dk} dakikada tamamladın. Hata yaptığın konular Hata Defteri'ne eklendi; yarının setinde öncelikle onlar gelecek.</p></div>
    <div class="net-kutu">
      <div><b style="color:var(--iyi)">${o.dogru}</b>Doğru</div>
      <div><b style="color:var(--kotu)">${o.yanlis}</b>Yanlış</div>
      <div><b>${net}</b>Net</div>
      <div><b>${dk}′</b>Süre</div>
    </div>
    <div class="baslik-satir"><h2>🎯 Zayıf konuların (bu ders)</h2><a class="btn kucuk seffaf" href="#/hata">Hata Defteri</a></div>
    <div class="kart">${zayif.map((t) => {
      const k = V.kayit.etiketler[t];
      return `<span class="chip ${k && k.y > 0 ? "zayif" : ""}">${esc(t)} · ❌${k.y} ✅${k.d}</span>`;
    }).join("")}</div>
    <div class="sonuc-satir" style="margin-top:18px">
      <a class="btn" href="#/panel">Bugünkü plana dön</a>
      <button class="btn turuncu" onclick="hataAtolyesi('${o.ders}')">Hata Atölyesi ile devam</button>
    </div>
  </div>`;
}

/* ---------------- DENEMELER ---------------- */
function viewDenemeler() {
  const satirlar = V.denemeler.denemeler.map((d) => {
    const gecmis = V.kayit.denemeler.filter((x) => x.id === d.id).slice(-1)[0];
    return `<div class="kart" style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap">
      <div>
        <h3>${esc(d.ad)}</h3>
        <p class="meta">${d.soru_sayisi} soru · ${d.sure_dk} dk · ${d.tur === "buyuk" ? "🏆 Büyük Deneme" : "Mini deneme"}</p>
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
  const g = V.program.gunler.find((x) => x.no === d.gun);
  $("#view").innerHTML = `<div class="quiz">
    <div class="hero"><span class="etiket">${esc(d.ad)}</span>
      <h1>${d.soru_sayisi} soru · ${d.sure_dk} dakika</h1>
      <p>${esc(d.odak)}. Gerçek sınav gibi: mola yok, telefon yok. Süre başlayınca geri sayar.</p></div>
    <div class="kart">
      <h3>Kurallar</h3>
      <ul style="margin-left:18px;font-size:14px">
        <li>Her soru 5 şıklı (A–E). Klavyeden 1–5 veya A–E ile cevap verebilirsin.</li>
        <li>Takıldığında işaretle ve geç — 3. turda geri dönersin.</li>
        <li>Bitir'de: net, konu analizi ve tüm çözümler gösterilir.</li>
        <li>Yanlışların Hata Defteri'ne işlenir; yarının setinde %40 ağırlıkla gelir.</li>
      </ul>
      <div class="sonuc-satir"><a class="btn yesil" href="#/deneme-run/${id}">⏱ Süreyi Başlat</a>
      <a class="btn seffaf" href="#/gun/${d.gun}">Gün sayfasına dön</a></div>
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
    const i = "abcde12345".indexOf(e.key.toLowerCase()) % 5;
    if (["a","b","c","d","e","1","2","3","4","5"].includes(e.key.toLowerCase()) && V.denemeOturum) {
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
      <a class="btn" href="#/panel">Bugünkü plana dön</a>
      <a class="btn turuncu" href="#/hata">Hata Defteri'ne bak</a>
      <a class="btn seffaf" href="#/denemeler">Denemeler</a>
    </div>
  </div>`;
};

/* ---------------- HATA DEFTERİ ---------------- */
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
      <p>En çok yanlış yaptığın konular yukarıda. Sistem her yanlış için 2 benzer soru üretir; aynı konu 2 kez yanlışlanırsa konu anlatımı tekrar hatırlatılır. Ertesi günün 20 sorusunun 8'i buradan gelir.</p></div>
    <div class="baslik-satir"><h2>🔥 Zayıf Konu Sıralaması</h2></div>
    <div class="kart">
      ${t.length ? t.map(([tag, v]) => `<span class="chip zayif">${esc(tag)} · ❌${v.y} ✅${v.d}</span>`).join("") : "<p class='meta'>Henüz hata yok.</p>"}
    </div>
    <div class="baslik-satir"><h2>⚔️ Zayıf Konu Atağı</h2></div>
    <div class="grid grid-3">
      ${Object.keys(DERSLER).map((d) => `<div class="ders-kart ${d}">
        <h3>${DERSLER[d].ad}</h3>
        <p class="meta">Zayıf konulardan ≤500 soruluk kişisel set</p>
        <div class="aksiyonlar"><button class="btn kucuk turuncu" onclick="hataAtolyesi('${d}')">Saldırıyı başlat</button></div>
      </div>`).join("")}
    </div>
    <div class="baslik-satir"><h2>📕 Yanlış Yaptığın Sorular (${yanlisSorular.length})</h2></div>
    ${yanlisSorular.slice(0, 30).map((s, i) => {
      const k = V.kayit.soru_kayit[s.id];
      return `<div class="soru-kart" style="margin-bottom:12px">
        <div class="quiz-ust"><span class="badge ${s.ders}">${DERSLER[s.ders].ad}</span><span class="badge kirmizi">❌${k.y} ✅${k.d}</span></div>
        <div class="soru-kok">${i + 1}. ${esc(s.kok)}</div>
        <div class="meta" style="margin-top:8px">Doğru: ${SIK_HARF[s.dogru]}) ${esc(s.siklar[s.dogru])}</div>
        ${(s.cozumler || []).map((c, j) => `<div class="yontem" style="margin-top:8px"><b>Yöntem ${j + 1} — ${esc(c.yontem)}:</b> ${esc(c.metin)}</div>`).join("")}
      </div>`;
    }).join("")}`;
  topbar("Hata Defteri");
}

/* ---------------- İSTATİSTİK ---------------- */
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
  $("#view").innerHTML = `
    <div class="hero"><span class="etiket">📊 İSTATİSTİK</span>
      <h1>${d + y} soru çözdün — net doğruluk oranı: ${d + y ? Math.round((d / (d + y)) * 100) : 0}%</h1>
      <p>Rakamlar yalan söylemez: nerede güçlüsün, nerede takılıyorsun?</p></div>
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

/* ---------------- AYARLAR ---------------- */
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
      try { V.kayit = JSON.parse(ok.result); kaydet(); alert("Yedek yüklendi!"); location.hash = "#/panel"; }
      catch { alert("Geçersiz dosya"); }
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
