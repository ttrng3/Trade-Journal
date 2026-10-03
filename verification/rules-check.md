# Verification: the rules check

## Promise

The Rules card in Reports, the rule badges and the "Rule breaks only" filter in the trade log, and the over-cap line agree exactly with an independent recount of the same definitions from `data/`. The definitions are in `work/261003-rules-check/spec.md`, Requirements 1–2. Setting R changes nothing in `data/`, and R is never written to the repo.

## Clean state

```bash
cd ~/Projects/Trade-Journal && git checkout <branch under test> && git pull --ff-only   # main after the merge
```
Run on the Mac. You need `node` and Playwright (`npm i playwright` in a scratch folder, never in this repo). Use a fresh browser profile, which is Playwright's default. Never clear `localStorage` in Ty's own browser: it holds his settings, including R.

## Steps

1. **Recount.** From the scratch folder, run `node recount.js ~/Projects/Trade-Journal 2024-12-10 2026-10-02 100` (script below). It prints the count and net per rule, "No rule broken", the over-cap days and their net, and the size of the filtered trade log.
2. **Page.** Serve the page with `python3 -m http.server 8765` in the repo, or use https://ttrng3.github.io/Trade-Journal/ after a merge. Then run `node page.js <url> 100 2024-12-10 2026-10-02 <out-dir>` (script below). In a fresh profile it does the following:
   - reads the over-cap line before R is set;
   - sets R = 100 in Settings and saves;
   - sets the custom range;
   - reads the Rules card;
   - turns on "Rule breaks only" and reads the trade-log count;
   - saves two screenshots.
3. **Data untouched.** `node tools/sync.js --csv-dir <empty dir> --check`.
4. **R not in the repo.** `git grep -nE '"R"[[:space:]]*:[[:space:]]*[0-9]' | wc -l` over the whole tree (an R key holding a number; the spec's own wording of this check doesn't match), and check `'R' in meta` of `data/index.json`.
5. **The journal protocol.** `verification/journal.md` step 1.

## Invariants

All of these must hold:

- `capLineBeforeR` reads "Daily cap: set R in Settings to check it."
- For every Rules row (add-down, early 0DTE, late 0DTE, long hold, SPXW, No rule broken, Over-cap days), the page's Trades and Net P&L equal the recount's `n` and `net` (rounded to whole dollars).
- The over-cap line's day count and net, and the Over-cap days row's trades and net, equal the recount's `capDays` (`days`, `n`, `net`).
- The trade-log title shows `<filtered> of <total>`, where `<filtered>` equals the recount's `filtered`.
- `addDownBadgeSample` (the add-down trade entered 2026-09-08 in `SPY260909C00768000`) is at least 1.
- The boundary fixture: in both the recount and the page, `at97` is true (3.00 then 2.91 is an add-down) and `above97` is false (3.00 then 2.92 is not).
- `errors` holds nothing except the 404 for `data/journal.json`, which the page probes on purpose and falls back from (`.pages-allow` notes it).
- Step 3 prints `"changedFiles": []`.
- Step 4 prints `0` and `False`.
- Step 5 prints `"pass": true` after the merge. On the branch, `served_equals_main` is false by design (Pages still serves `main`) and every other verdict must be true.

Measured on 2026-10-03 on branch `work/rules-check` (local server): 322 / −$6,309, 28 / −$529, 32 / −$1,598, 144 / −$3,523, 87 / −$3,450, 118 / +$1,962; 16 over-cap days (130 trades), −$11,136; 411 of 532. These pass only as long as the data is unchanged. New fills inside the range move them, so compare the page against the recount, never against these figures.

### recount.js
```js
const fs=require('fs'),R=process.argv[2],P=require(R+'/tools/parse-webull.js');
const [from,to,riskR]=[process.argv[3],process.argv[4],+process.argv[5]];
const idx=JSON.parse(fs.readFileSync(R+'/data/index.json'));let fills=[];
for(const s of idx.shards)fills.push(...Object.values(JSON.parse(fs.readFileSync(`${R}/data/fills/${s}.json`))).map(f=>P.hydrate({...f})));
const all=P.buildTrades(fills,{feeC:0,feeS:0,longOnly:true});
const closed=all.filter(t=>t.net!=null&&t.result!=='OPEN'&&t.result!=='UNKNOWN');
const rules=t=>{if(t.type!=='option')return[];const r=[],b=t.fills.filter(f=>f.side==='BUY'),hm=t.entry.slice(11,16),z=t.exp===t.entry.slice(0,10);
 if(t.dir==='LONG'&&b.slice(1).some(f=>Math.round(f.price*1e6)*100<=Math.round(b[0].price*1e6)*97))r.push('add-down');if(z&&hm<'10:00')r.push('early 0DTE');if(z&&hm>='14:00'&&hm<'15:00')r.push('late 0DTE');if(z&&t.hold>600)r.push('long hold');if(t.und==='SPXW')r.push('SPXW');return r;};
const day={};closed.forEach(t=>day[t.date]=(day[t.date]||0)+t.net);const cap=new Set(Object.keys(day).filter(d=>day[d]<-3*riskR));
const inR=closed.filter(t=>t.date>=from&&t.date<=to);const sum=a=>Math.round(a.reduce((x,t)=>x+t.net,0));
const out={};['add-down','early 0DTE','late 0DTE','long hold','SPXW'].forEach(k=>{const a=inR.filter(t=>rules(t).includes(k));out[k]={n:a.length,net:sum(a)}});
const clean=inR.filter(t=>t.type==='option'&&!rules(t).length&&!cap.has(t.date));out['No rule broken']={n:clean.length,net:sum(clean)};
const capT=inR.filter(t=>cap.has(t.date));out.capDays={days:new Set(capT.map(t=>t.date)).size,n:capT.length,net:sum(capT)};
out.filtered=inR.filter(t=>rules(t).length||cap.has(t.date)).length;
const fx=(p2)=>rules({type:'option',dir:'LONG',und:'SPY',entry:'2026-09-08T11:00:00',exp:'2026-09-09',hold:60,fills:[{side:'BUY',price:3},{side:'BUY',price:p2}]}).includes('add-down');
out.fixture={at97:fx(2.91),above97:fx(2.92)};
console.log(JSON.stringify(out));
```

### page.js
```js
const {chromium}=require('playwright');
(async()=>{
 const [url,R,from,to,shots]=process.argv.slice(2);
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1000}});const errs=[];
 p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto(url);await p.waitForFunction(()=>/snapshot/.test(document.body.innerText),null,{timeout:30000});
 const res={};
 await p.click('[data-view="reports"]');res.capLineBeforeR=await p.textContent('#capLine');
 await p.click('[data-view="settings"]');await p.fill('#riskR',R);await p.click('#saveSettings');await p.waitForTimeout(500);
 await p.selectOption('#rangePreset','custom');
 await p.fill('#rangeFrom',from);await p.dispatchEvent('#rangeFrom','change');await p.fill('#rangeTo',to);await p.dispatchEvent('#rangeTo','change');
 await p.click('[data-view="reports"]');await p.waitForTimeout(300);
 const card=p.locator('.card',{has:p.locator('h3',{hasText:/^Rules$/})});
 res.rows=await card.locator('tbody tr').evaluateAll(trs=>trs.map(tr=>[...tr.children].map(td=>td.textContent.trim())));
 res.capLine=await p.textContent('#capLine');
 await card.screenshot({path:shots+'/rules-card.png'});
 await p.click('[data-view="trades"]');await p.click('#frules');await p.waitForTimeout(300);
 res.tradeLogTitle=await p.textContent('#view-trades h3');
 res.addDownBadgeSample=await p.$$eval('#tt tr.row',rs=>rs.filter(r=>/2026-09-08/.test(r.innerText)&&/SPY260909C00768000/.test(r.innerText)&&/add-down/.test(r.innerText)).length);
 await p.screenshot({path:shots+'/trade-log-filtered.png'});
 res.fixture=await p.evaluate(()=>{const fx=p2=>ruleFlags({type:'option',net:1,result:'WIN',dir:'LONG',und:'SPY',entry:'2026-09-08T11:00:00',exp:'2026-09-09',hold:60,fills:[{side:'BUY',price:3},{side:'BUY',price:p2}]}).includes('adddown');return {at97:fx(2.91),above97:fx(2.92)};});
 res.errors=errs;console.log(JSON.stringify(res,null,1));await b.close();
})();
```

## Adversary

- **The page and the recount share a bug.** They don't share code: the recount re-implements the five rules and the cap from the spec's words, and writes the add-down threshold in integer millionths of a dollar (147 fills carry sub-cent prices) where the page uses a float with a tolerance. Review #12 found the first version used the same float expression on both sides, which missed fills at exactly 97%. The boundary fixture now tests both. The only shared code is `buildTrades`, which `verification/journal.md` already covers.
- **R leaks into the public repo.** Step 4. R is saved by `store.saveMeta`, which on Pages writes to `localStorage` and in the preview writes to the preview's private database. The nightly sync writes `data/` only.
- **A rule badge without the rule.** Step 2 checks one known add-down trade. The filtered count catches any rule or cap mismatch, because the filter's set equals the recount's.

## Sanctioned substitutes

- The R value used is 100, a test value. Ty's real R stays in his browser and is never read by this protocol.
- The badges are checked through one known trade and the filter's total, not trade by trade.

## Evidence

- The JSON from steps 1 and 2.
- `rules-card.png` and `trade-log-filtered.png`.
- The outputs of steps 3–5.

## Not covered

- Whether the rules are good trading rules. That's the paper-trading gate, not this page.
- Whether the Cowork preview's copy behaves the same. Its R is stored in its own database, and the preview is rebuilt from the same `index.html` in the ship turn.
