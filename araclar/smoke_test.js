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
  const send = (data, status=200) => Promise.resolve({
    ok: status===200, status,
    json: () => Promise.resolve(data),
    text: () => Promise.resolve(JSON.stringify(data)),
  });
  if (u.includes("/api/soru-ayir/")) {
    const payload=JSON.parse(opts.body);
    return send({ok:true,ayrilan_sorular:Object.fromEntries(payload.ids.map((id) => [id,{tur:payload.tur}]))});
  }
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
  // Strict eval içindeki V dışarı sızmaz. Yalnız test ortamında, aynı
  // leksik kapsamda bir render yardımcısı kur; üretim JS'sini değiştirme.
  win.eval(fs.readFileSync(path.join(ROOT,"static/js/soru_secimi.js"),"utf8"));
  win.eval(appjs + `\nwindow.__smokeRenderQuestion = (ders, sid) => {
    V.oturum = {uid:"smoke-"+sid,mod:"test", ders, baslik:"İçerik kontrolü", sira:0,
      dogru:0, yanlis:0, kuyruk:[{s:V.tumSorular[sid],tip:"ana"}],
      gorulen:[], bas:Date.now()}; V.oturumTecih = {}; renderQuiz();
  };
  window.__smokeQueueIds = () => V.oturum?.kuyruk.map((x) => x.s.id) || [];
  window.__smokeExamIds = () => V.denemeOturum?.d.sorular || [];
  window.__smokeExhaust = () => {
    Object.values(V.tumSorular).forEach((s) => { V.kayit.ayrilan_sorular[s.id]={tur:"test"}; }); kaydet();
  };
  window.__smokeReload = async () => { await kayitYukle(); };
  window.__smokeSeedOldTopics = () => {
    const a = dersAkisKaydi("guncel");
    a.biten = Array.from({length:30}, (_,i) => "Kapsam dışı eski konu " + i);
  };`);
  win.dispatchEvent(new win.Event("load"));
  await tick(250);

  const txt = () => (doc.querySelector("#view") || { textContent: "" }).textContent;
  const has = (q) => txt().includes(q);
  const go = async (hash) => {
    // jsdom gerçek hash değişiminde olayı zaten gönderir; ikinci yapay olay
    // yeni bir oturum açıp kullanılmamış seti haksız yere tüketmemelidir.
    if (win.location.hash === hash) win.dispatchEvent(new win.HashChangeEvent("hashchange"));
    else win.location.hash = hash;
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
  ok("geçmiş KPSS konu filtresi görünür", has("Geçmiş KPSS konu filtresi açık"));
  ok("Güncel 3000 hedefi gerçek sayıyla karıştırılmaz", has("3000 farklı soru") && has("Şu an 364 aktif") && has("2636 soru kaldı"));
  ok("Güncel havuzunun 500 farklı soruya yetmediği açık", has("364 farklı aktif soru") && has("kapsam dışı soru eklenmez"));
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
  ok("anti-repeat notu ekranda", has("Aynı soru yeni test veya denemede tekrar verilmez") || has("otomatik kontrol"));

  /* ---------- 23-26: karışık / odak / çıkmış ---------- */
  await go("#/coz/karisik/tarih");
  ok("karışık test (tüm konular)", has("Soru 1") && has("Tarih"));
  await go("#/coz/odak/0");
  ok("deneme odak testi", has("Odak Testi") || has("zayıf konuların"));
  await go("#/coz/cikmis/2022");
  ok("2022-KPSS çıkmış testi", has("2022-KPSS"));
  await go("#/coz/cikmis/karisik");
  ok("karışık çıkmış testi", has("Çıkmış KPSS Soruları"));

  await go("#/coz/karisik/cografya");
  const firstSet=win.__smokeQueueIds();
  await go("#/coz");
  await go("#/coz/karisik/cografya");
  const secondSet=win.__smokeQueueIds();
  ok("cevaplanmadan bırakılan set yeni testte geri gelmez",firstSet.length===10 && secondSet.length===10 && secondSet.every((id) => !firstSet.includes(id)));
  const examReserve=new Set(loadFix("denemeler.json").denemeler.flatMap((d) => d.sorular));
  ok("test seti denemelere ayrılan sorulardan seçilmez",[...firstSet,...secondSet].every((id) => !examReserve.has(id)));

  /* ---------- 27-31: deneme ---------- */
  const den = loadFix("denemeler.json", { denemeler: [] }).denemeler[0];
  const did = den ? den.id : "DEN-01";
  await go(`#/deneme/${did}`);
  ok("deneme bilgi sayfası", has("Kurallar") && has("Süreyi Başlat"));
  await go(`#/deneme-run/${did}`);
  ok("deneme başladı", has("Bitir") && doc.querySelectorAll(".deneme-hucre").length > 0);
  ok("deneme seti önceki test setleriyle çakışmaz",win.__smokeExamIds().every((id) => ![...firstSet,...secondSet].includes(id)));
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

  /* ---------- 1500'lük parti: her derste iki yargı biçiminin gerçek kaydı ---------- */
  const plan1500 = JSON.parse(fs.readFileSync(path.join(ROOT, "data/kaynaklar/parti_1500_plan.json"), "utf8"));
  for (const ders of ["tarih", "cografya", "vatandaslik", "turkce", "guncel"]) {
    const bank = loadFix(`sorular_${ders}.json`, []);
    const targets = new Set(plan1500.targets.filter((t) => t.ders === ders).map((t) => t.id));
    for (const [bicim, prefix] of [["üç öncül", "I. "], ["beş yargı", "1. "]]) {
      const s = bank.find((s) => targets.has(s.id) && s.kok.startsWith(prefix));
      if (!s) { ok(`${ders} ${bicim}: güncel API kaydı`, false); continue; }
      // İzole bir test oturumu; mevcut rota/akış testlerinden bağımsız olarak
      // gerçek API kaydının render ve cevap/çözüm eşleşmesini denetler.
      win.__smokeRenderQuestion(ders, s.id);
      ok(`${ders} ${bicim}: kök ve satır sonları`, doc.querySelector(".soru-kok")?.textContent === s.kok);
      ok(`${ders} ${bicim}: 5 şık ve özgün kaynak`, doc.querySelectorAll(".sik").length === 5 && has("Kaynak: KPSS formatında"));
      await sikSec(s.dogru);
      ok(`${ders} ${bicim}: doğru şık eşleşmesi`, doc.querySelector(".sik.dogru")?.getAttribute("data-sik") === String(s.dogru));
      ok(`${ders} ${bicim}: gerekçeli çözüm`, has(s.cozumler[0].metin.slice(0, 60)));
      ok(`${ders} ${bicim}: konu dayanağı ve özgün/çıkmış ayrımı`, !!doc.querySelector(".kapsam-notu") && has("Konu örnekleri:") && has("o sınavda çıktığı anlamına gelmez"));
    }
  }

  const quality=JSON.parse(fs.readFileSync(path.join(ROOT,"data/kaynaklar/kalite_01_inceleme.json"),"utf8")).questions;
  for (const sid of Object.keys(quality)) {
    const ders=quality[sid].before.ders;
    const s=loadFix(`sorular_${ders}.json`).find((s) => s.id===sid);
    win.__smokeRenderQuestion(ders,sid);
    ok(`${sid} kalite: yeni kök ve beş seçenek`,doc.querySelector(".soru-kok")?.textContent===s.kok && doc.querySelectorAll(".sik").length===5);
    await sikSec(s.dogru);
    ok(`${sid} kalite: cevap ve açıklama`,doc.querySelector(".sik.dogru")?.getAttribute("data-sik")===String(s.dogru) && has(s.cozumler[0].metin));
    ok(`${sid} kalite: özgün kaynak ve geçmiş konu ayrımı`,has("Kaynak: KPSS formatında") && !!doc.querySelector(".kapsam-notu") && has("o sınavda çıktığı anlamına gelmez"));
  }

  const kapsam = loadFix("kapsam.json");
  const activeQuestions = ["tarih", "cografya", "vatandaslik", "turkce", "guncel"].flatMap((d) => loadFix(`sorular_${d}.json`, []));
  ok("bütün API fixture soruları konu kapsamı taşır", activeQuestions.length === kapsam.aktif && activeQuestions.every((s) => s.kpss_kapsam?.konular?.length));
  ok("bekleyen sorular hiçbir ders fixture'ında yok", activeQuestions.every((s) => !kapsam.bekleyen_kayitlar[s.id]));
  win.__smokeSeedOldTopics();
  await go("#/akis/guncel");
  ok("Güncel günlük akışında aktif havuz sınırı görünür", has("364 farklı aktif soru") && has("500 farklı soruya yetmiyor"));
  ok("kapsam dışı eski konular karışık test kilidini açmaz", has("Önce konu testlerini bitir") && !!doc.querySelector("button[disabled]"));

  win.__smokeExhaust();
  await win.__smokeReload();
  await go("#/coz/karisik/guncel");
  ok("yeniden yükleme kalıcı kullanım kaydını silmez",has("Yeni soru havuzu yetersiz"));
  ok("tükenen havuz eski soruyla doldurulmaz",doc.querySelectorAll(".sik").length===0 && has("Eski soru yeniden verilmez"));

  console.log(`\nSONUÇ: ${pass} başarılı, ${fail} başarısız`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error("SMOKE ÇÖKTÜ:", e); process.exit(2); });
