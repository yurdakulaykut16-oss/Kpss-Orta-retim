/* Saf seçim kuralları: gün değişse de tekrar yok; şık sırası kökü değiştirmez. */
(function (root) {
  "use strict";
  const kok = (s) => `${s.kok.normalize("NFKC").toLocaleLowerCase("tr-TR")
    .replace(/[.,;:!?…“”"'’]/g, "").replace(/\s+/g, " ").trim()}`;
  const keys = (o) => Object.keys(o && typeof o === "object" && !Array.isArray(o) ? o : {});
  function gecmis(kayit, index) {
    const ids = new Set(keys(kayit.ayrilan_sorular));
    for (const [id, k] of Object.entries(kayit.soru_kayit || {})) {
      if (k && (k.son || k.d > 0 || k.y > 0)) ids.add(id);
    }
    keys(kayit.gunluk?.ids).forEach((id) => ids.add(id));
    Object.values(kayit.ders_gunluk || {}).forEach((g) => keys(g?.ids).forEach((id) => ids.add(id)));
    for (const d of (Array.isArray(kayit.denemeler) ? kayit.denemeler : [])) {
      if (Array.isArray(d.sorular)) d.sorular.forEach((id) => ids.add(id));
    }
    const roots = new Set(keys(kayit.ayrilan_kokler));
    ids.forEach((id) => { if (index[id]) roots.add(kok(index[id])); });
    return {ids, roots};
  }
  function ayrilan(denemeler, index, haric) {
    const ids = new Set(), roots = new Set();
    for (const d of denemeler) {
      if (d.id === haric) continue;
      for (const id of d.sorular) {
        ids.add(id); if (index[id]) roots.add(kok(index[id]));
      }
    }
    return {ids, roots};
  }
  function yeni(havuz, history, reserved = {ids:new Set(), roots:new Set()}) {
    const ids = new Set(), roots = new Set();
    return havuz.filter((s) => {
      const k = kok(s);
      if (ids.has(s.id) || roots.has(k) || history.ids.has(s.id) || history.roots.has(k)
          || reserved.ids.has(s.id) || reserved.roots.has(k)) return false;
      ids.add(s.id); roots.add(k); return true;
    });
  }
  function deneme(template, bank, exams, history) {
    const index = Object.fromEntries(bank.map((s) => [s.id,s]));
    const reserved = ayrilan(exams,index,template.id);
    if (!Array.isArray(template.soru_nesneleri) || template.soru_nesneleri.length !== template.soru_sayisi)
      throw new Error("Denemenin soru sayısı doğrulanamadı; oturum başlatılmadı.");
    // Önce geçerli özgün soruları koru; bir değiştirme sonraki özgün soruyu tüketmesin.
    const originals = new Set(template.soru_nesneleri.map((s) => s.id));
    const selected = [], seen = {ids:new Set(history.ids), roots:new Set(history.roots)};
    for (const original of template.soru_nesneleri) {
      const preferred = index[original.id];
      let s = preferred && yeni([preferred],seen,reserved)[0];
      if (!s) s = yeni(bank.filter((s) => s.ders === original.ders && !originals.has(s.id)),seen,reserved)
        .sort((a,b) => a.id.localeCompare(b.id,"en"))[0];
      if (!s) throw new Error(`${original.ders}: deneme dağılımını koruyacak yeterli yeni soru kalmadı. Aynı sorularla doldurulmadı.`);
      selected.push(s); seen.ids.add(s.id); seen.roots.add(kok(s));
    }
    return {...template, sorular:selected.map((s) => s.id), soru_nesneleri:selected};
  }
  const api = {kok, gecmis, ayrilan, yeni, deneme};
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SoruSecimi = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
