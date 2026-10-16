#!/usr/bin/env node
/* node --test araclar/test_soru_secimi.js */
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
const S = require('../static/js/soru_secimi.js');
const q = (id,ders='guncel',kok=`Soru ${id}?`) => ({id,ders,kok,siklar:['a','b','c','d','e'],dogru:0});
const empty = () => ({ids:new Set(),roots:new Set()});
const hist = (rows) => ({ids:new Set(rows.map(s=>s.id)),roots:new Set(rows.map(S.kok))});
const exam = (id,rows) => ({id,soru_sayisi:rows.length,sorular:rows.map(s=>s.id),soru_nesneleri:rows});

test('boş geçmiş yeni soruları engellemez',()=>assert.equal(S.yeni([q('a')],empty()).length,1));
test('aynı id farklı metinle geri gelemez',()=>assert.equal(S.yeni([q('a','guncel','Yeni metin')],hist([q('a')])).length,0));
test('aynı kök farklı id ve şık sırasıyla geri gelemez',()=>{
  const a=q('a'),b={...q('b','guncel',a.kok),siklar:['e','d','c','b','a'],dogru:4};
  assert.equal(S.yeni([b],hist([a])).length,0);
});
test('noktalama ve boşluk varyantı yeni soru değildir',()=>assert.equal(S.kok(q('a','turkce','  IŞIK,  ve İZ! ')),S.kok(q('b','turkce','ışık ve iz'))));
test('ders değiştirmek aynı kökü yeni soru yapmaz',()=>assert.equal(S.yeni([q('b','tarih','Soru a?')],hist([q('a')])).length,0));
test('aynı havuzdaki yinelenen id tek kez seçilir',()=>assert.equal(S.yeni([q('a'),q('a')],empty()).length,1));
test('aynı havuzdaki farklı idli aynı kök tek kez seçilir',()=>assert.equal(S.yeni([q('a'),q('b','guncel','Soru a?')],empty()).length,1));
test('eski doğru cevap geçmişi korunur',()=>assert(S.gecmis({soru_kayit:{a:{d:1}}},{a:q('a')}).ids.has('a')));
test('eski yanlış cevap geçmişi korunur',()=>assert(S.gecmis({soru_kayit:{a:{y:1}}},{a:q('a')}).ids.has('a')));
test('eski boş deneme son görülme kaydı korunur',()=>assert(S.gecmis({soru_kayit:{a:{son:123,d:0,y:0}}},{a:q('a')}).ids.has('a')));
test('yalnız boş sayaç nesnesi görülmüş sayılmaz',()=>assert(!S.gecmis({soru_kayit:{a:{son:null,d:0,y:0}}},{a:q('a')}).ids.has('a')));
test('eski günlük ve derslik idler taşınır',()=>{
 const h=S.gecmis({gunluk:{ids:{a:1}},ders_gunluk:{guncel:{ids:{b:1}}}},{});
 assert.deepEqual([...h.ids].sort(),['a','b']);
});
test('tarih değişince kalıcı rezerv kaydı silinmez',()=>assert(S.gecmis({gunluk:{tarih:'2099-01-01',ids:{}},ayrilan_sorular:{a:{tur:'test'}}},{}).ids.has('a')));
test('artık bankada olmayan kaydın saklanmış kökü engellenir',()=>assert.equal(S.yeni([q('b','guncel','Eski soru')],S.gecmis({ayrilan_kokler:{[S.kok(q('a','guncel','Eski soru'))]:true}},{})).length,0));
test('denemeye ayrılan soru testte seçilemez',()=>{
 const a=q('a'),b=q('b');assert.deepEqual(S.yeni([a,b],empty(),S.ayrilan([exam('D',[a])],{a,b})).map(s=>s.id),['b']);
});
test('deneme rezervinin başka idli aynı kökü de testten çıkar',()=>{
 const a=q('a'),b=q('b','guncel',a.kok);assert.equal(S.yeni([b],empty(),S.ayrilan([exam('D',[a])],{a})).length,0);
});
test('kullanılmamış deneme özgün seçimlerini korur',()=>{
 const rows=[q('a'),q('b','tarih')],d=exam('D',rows);
 assert.deepEqual(S.deneme(d,rows,[d],empty()).sorular,['a','b']);
});
test('testte kullanılan deneme sorusu aynı dersten yenisiyle değişir',()=>{
 const a=q('a'),b=q('b'),c=q('c','tarih'),d=exam('D',[a,c]);
 const out=S.deneme(d,[a,b,c],[d],hist([a]));assert.deepEqual(out.sorular,['b','c']);
});
test('başka denemenin rezervi yerine kullanılamaz',()=>{
 const a=q('a'),b=q('b'),c=q('c'),d=exam('D',[a]);
 assert.deepEqual(S.deneme(d,[a,b,c],[d,exam('E',[b])],hist([a])).sorular,['c']);
});
test('denemeyi yeniden açınca önceki oturumla çakışmaz',()=>{
 const rows=['a','b','c','d'].map(id=>q(id)),d=exam('D',rows.slice(0,2));
 const first=S.deneme(d,rows,[d],empty());
 const next=S.deneme(d,rows,[d],hist(first.soru_nesneleri));
 assert.deepEqual(next.sorular,['c','d']);
});
test('yetersiz aynı ders havuzunda başka dersle veya eski soruyla doldurulmaz',()=>{
 const a=q('a'),d=exam('D',[a]),before=JSON.stringify(d);
 assert.throws(()=>S.deneme(d,[a,q('b','tarih')],[d],hist([a])),/yeterli yeni soru/);
 assert.equal(JSON.stringify(d),before);
});
test('eksik deneme nesneleriyle süre başlatılamaz',()=>assert.throws(()=>S.deneme({...exam('D',[q('a')]),soru_sayisi:2},[q('a')],[],empty()),/doğrulanamadı/));
test('kayıtlı gerçek deneme idleri de geçmişe taşınır',()=>assert(S.gecmis({denemeler:[{sorular:['a']}]},{}).ids.has('a')));
test('gerçek bankada tüm test havuzu tüketilse de 10 deneme ayrı kalır',()=>{
 const root=path.join(__dirname,'..');
 const raw=execFileSync('python3',['-c',"import json,app; c=app.her_seyi_yukle(); print(json.dumps({'bank':[s for rows in c['sorular'].values() for s in rows], 'exams':[{**d,'soru_nesneleri':[next(s for rows in c['sorular'].values() for s in rows if s['id']==sid) for sid in d['sorular']]} for d in c['denemeler']['denemeler']]}))"],{cwd:root,maxBuffer:256*1024*1024});
 const {bank,exams}=JSON.parse(raw),index=Object.fromEntries(bank.map(s=>[s.id,s]));
 const tests=S.yeni(bank,empty(),S.ayrilan(exams,index));
 const h=hist(tests),all=[];
 for(const d of exams){
  const out=S.deneme(d,bank,exams,h);
  assert.equal(out.soru_nesneleri.length,d.soru_sayisi);
  const mix=rows=>rows.reduce((o,s)=>(o[s.ders]=(o[s.ders]||0)+1,o),{});
  assert.deepEqual(mix(out.soru_nesneleri),mix(d.soru_nesneleri));
  for(const s of out.soru_nesneleri){assert(!h.ids.has(s.id));assert(!h.roots.has(S.kok(s)));h.ids.add(s.id);h.roots.add(S.kok(s));all.push(s.id);}
 }
 assert.equal(all.length,220);assert.equal(new Set(all).size,220);
});
