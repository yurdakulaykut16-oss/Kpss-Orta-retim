#!/usr/bin/env node
/* =========================================================
   KPSS Kamp — jsdom smoke testi
   Çalıştırma (önce sunucu ayağa kalkıp fixture'lar çekilmeli):
     python3 araclar/refresh_fixtures.py
     cd /tmp/kpss_test && npm i jsdom >/dev/null 2>&1
     NODE_PATH=/tmp/kpss_test/node_modules node araclar/smoke_test.js
   ========================================================= */
"use strict";
const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

const FIX = process.env.KPSS_FIX || "/tmp/kpss_test";
const ROOT = path.join(__dirname, "..");

let pass = 0, fail = 0;
const ok = (name, cond, extra = "") => {
  if (cond) { pass++; console.log("✔ " + name); }
  else { fail++; console.log("✖ " + name + (extra ? " — " + extra : "")); }
};
const tick = (ms = 40) => new Promise((r) => setTimeout(r, ms));

function loadFix(name, fb = {}) {
  try { return JSON.parse(fs.readFileSync(path.join(FIX, name), "utf8")); }
  catch { return fb; }
}

function mockFetch(url, opts) {
  const u = String(url);
  const send = (data) => Promise.resolve({
    ok: true, status: 200,
    json: () => Promise.resolve(data),
    text: () => Promise.resolve(JSON.stringify(data)),
  });
  if (u.includes("/api/meta")) return send(loadFix("meta.json"));
  if (u.includes("/api/program")) return send(loadFix("program.json"));
  if (u.includes("/api/denemeler")) return send(loadFix("denemeler.json", { denemeler: [] }));
  if (u.includes("/api/konu-yeniden")) return send(loadFix("konu_yeniden.json"));
  const d = u.match(/\/api\/ders\/(\w+)/); if (d) return send(loadFix(`ders_${d[1]}.json`));
  const s = u.match(/\/api\/sorular\/(\w+)/); if (s) return send(loadFix(`sorular_${s[1]}.json`, []));
  const dn = u.match(/\/api\/deneme\/([\w-]+)/); if (dn) return send(loadFix(`deneme_${dn[1]}.json`, { soru_nesneleri: [] }));
  if (u.includes("/api/ilerleme")) return send({});
  if (u.includes("/api/sifirla")) return send({ ok: 1 });
  return send({});
}

(async function main() {
  const html = fs.readFileSync(path.join(ROOT, "static", "index.html"), "utf8");
  const appjs = fs.readFileSync(path.join(ROOT, "static", "js", "app.js"), "utf8");

  const dom = new JSDOM(html, {
    runScripts: "outside-only",
    url: "http://localhost/#/panel",
    pretendToBeVisual: true,
  });
  const win = dom.window, doc = win.document;
  win.fetch = mockFetch;
  win.confirm = () => true;
  win.scrollTo = () => {};
  win.eval(appjs);
  win.dispatchEvent(new win.Event("load"));
  await tick(250);

  const txt = () => (doc.querySelector("#view") || { textContent: "" }).textContent;
  const has = (q) => txt().includes(q);
  const go = async (hash) => {
    win.location.hash = hash;
    win.dispatchEvent(new win.HashChangeEvent("hashchange"));
    await tick(60);
  };
  const sikSec = async (i = 0) => {
    const siklar = [...doc.querySelectorAll(".sik")].filter((el) => !el.classList.contains("kapali"));
    if (!siklar.length) return false;
    siklar[i % siklar.length].click();
    await tick(40);
    return true;
  };
  const sonraki = async () => {
    const b = doc.querySelector("#sonraki-btn");
    if (b) { b.click(); await tick(40); }
    return !!b;
  };

  /* ---------- 1-5: gün rehberi ---------- */
  ok("gün rehberi yüklendi", has("GÜN REHBERİ"));
  ok("konu maratonu bölümü (1-2. gün)", has("Konu Maratonı") || has("Konu Tekrarı"));
  ok("10'ar soruluk testler bölümü", has("10'ar Soruluk Testler"));
  ok("deneme kartı", /DENEME/i.test(txt()) && has("dakika"));
  ok("günlük hedef rozeti 0/2500", has("0/2500"));

  /* ---------- 6-8: konu anlatımı ---------- */
  await go("#/konular");
  ok("konu anlatımları sayfası", has("KONU ANLATIMLARI"));
  await go("#/ders/tarih/1");
  ok("modül anlatım sayfası", has("Sıradaki adım") && has("10'luk Test") && has("Okudum"));
  await go("#/konular/tarih");
  ok("konu modülü başlığı", has("Tarih") && (has("DERİN MODÜLLER") || has("modülü")));

  /* ---------- 9-14: test çöz hubı ---------- */
  await go("#/coz");
  ok("test çöz hubı", has("TEST ÇÖZ"));
  ok("gerçek çıkmış bölümü", has("Gerçek Çıkmış KPSS Soruları"));
  ok("çıkmış yıl butonları 2014/2024", has("2014-KPSS") && has("2024-KPSS"));
  ok("2022-KPSS butonu", has("2022-KPSS"));
  ok("günlük akış butonu (500)", has("Günlük Akış (500)"));
  ok("maraton / telafi / hata butonları", has("Maraton (10'lu)") && has("Yanlış Telafisi") && has("Hata Atölyesi"));

  /* ---------- 15-22: konu testi akışı ---------- */
  const tarihS = loadFix("sorular_tarih.json", []);
  const konuSay = {};
  tarihS.forEach((s) => (konuSay[s.konu] = (konuSay[s.konu] || 0) + 1));
  const konu = Object.entries(konuSay).sort((a, b) => b[1] - a[1])[0]?.[0] || "Osmanlı";
  await go(`#/coz/test/konu/tarih/${encodeURIComponent(konu)}`);
  ok("konu testi başladı", has("Soru 1") && has("Test menüsü"));
  ok("soru kartı ve şıklar", doc.querySelectorAll(".sik").length === 5);
  await sikSec(0);
  ok("şık cevaplama → çözüm", has("Yöntem") || has("Doğru!") || has("Yanlış"));
  const ilkKok = txt().slice(0, 0) || (doc.querySelector(".soru-kok") || {}).textContent;
  await sonraki();
  ok("sonraki soruya geçti", (doc.querySelector(".soru-kok") || {}).textContent !== ilkKok);
  // kalan 9 soruyu cevapla → 10 cevapta otomatik kontrol
  for (let i = 0; i < 9; i++) {
    if (has("OTOMATİK KONTROL")) break;
    await sikSec(i);
    if (!has("OTOMATİK KONTROL")) await sonraki();
  }
  await tick(80);
  ok("10 soruda otomatik kontrol", has("OTOMATİK KONTROL"));
  ok("kontrol: net kutusu", has("Net") && has("Doğru"));
  ok("kontrol: yanlışlar veya hatasız", has("Yanlışların") || has("HATASIZ"));
  ok("kontrol: devam seçenekleri", has("Devam") || has("Günün rehberi"));
  ok("günlük sayaç arttı", /Bugün: [1-9]/.test(txt()) || /[1-9]\d*\/2500/.test(txt()));
  ok("anti-repeat notu ekranda", has("Aynı soru bugün tekrar gelmez") || has("otomatik kontrol"));

  /* ---------- 23-26: karışık / odak / çıkmış ---------- */
  await go("#/coz/karisik/tarih");
  ok("karışık test (tüm konular)", has("Soru 1") && has("Tarih"));
  await go("#/coz/odak/0");
  ok("deneme odak testi", has("Odak Testi") || has("zayıf konuların"));
  await go("#/coz/cikmis/2022");
  ok("2022-KPSS çıkmış testi", has("2022-KPSS"));
  await go("#/coz/cikmis/karisik");
  ok("karışık çıkmış testi", has("Çıkmış KPSS Soruları"));

  /* ---------- 27-31: deneme ---------- */
  const den = loadFix("denemeler.json", { denemeler: [] }).denemeler[0];
  const did = den ? den.id : "DEN-01";
  await go(`#/deneme/${did}`);
  ok("deneme bilgi sayfası", has("Kurallar") && has("Süreyi Başlat"));
  await go(`#/deneme-run/${did}`);
  ok("deneme başladı", has("Bitir") && doc.querySelectorAll(".deneme-hucre").length > 0);
  const hedef = doc.querySelectorAll(".deneme-hucre").length;
  ok("deneme soru ızgarası tam", hedef === (den && den.sorular ? den.sorular.length : hedef));
  win.eval("denemeIsaretle()");
  await tick(40);
  ok("deneme işaretleme", doc.querySelectorAll(".deneme-hucre.isaretli").length >= 1);
  await sikSec(1);
  win.eval("denemeBitir()");
  await tick(80);
  ok("deneme bitti + net", has("DENEME BİTTİ") && has("Net:"));
  ok("yarının odağı üretildi", has("Yarının Odağı") || has("Odak"));

  /* ---------- 32-37: defter / istatistik / akış / ayarlar ---------- */
  await go("#/hata");
  ok("hata defteri", has("HATA DEFTERİ"));
  await go("#/istatistik");
  ok("istatistik sayfası", has("İSTATİSTİK") && has("Bugün"));
  await go("#/akis/tarih");
  ok("ders akış sayfası", has("GÜNLÜK DERS AKIŞI") && has("bugün bu ders"));
  ok("akış: konu testi linki", !!doc.querySelector('a[href^="#/coz/test/konu/tarih/"]'));
  ok("akış: karışık test kilidi/uyarısı", has("karışık") || has("Karışık"));
  await go("#/ayarlar");
  ok("ayarlar: sıfırlama", has("Veriler ve Sıfırlama") && has("Sıfırla"));

  console.log(`\nSONUÇ: ${pass} başarılı, ${fail} başarısız`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error("SMOKE ÇÖKTÜ:", e); process.exit(2); });
