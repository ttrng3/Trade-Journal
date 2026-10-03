const fs=require('fs'),R=require('path').resolve(__dirname,'../..')+'/';
const P=require(R+'tools/parse-webull.js');
const idx=JSON.parse(fs.readFileSync(R+'data/index.json'));
let fills=[];for(const s of idx.shards){const d=JSON.parse(fs.readFileSync(R+`data/fills/${s}.json`));fills.push(...Object.values(d).map(f=>P.hydrate({...f})));}
const trades=P.buildTrades(fills,{feeC:0,feeS:0,longOnly:true});
const today='2026-10-03';
const day=t=>t.slice(0,10),dd=(a,b)=>Math.round((Date.parse(b)-Date.parse(a))/864e5);
const rows=[];let unk=0;
for(const t of trades){
 if(t.type!=='option'||t.dir!=='LONG'){continue}
 if(t.result==='UNKNOWN'){unk++;continue}
 let net=t.net,expired=false;
 if(t.status==='OPEN'){ if(t.exp<today){ // held to expiry: assume worthless on the open qty
   net=t.gross-(t.eq-t.xq)*t.avgIn*100; expired=true;} else continue; }
 const buys=t.fills.filter(f=>f.side==='BUY');const p0=buys[0].price;
 const avgDown=buys.slice(1).some(f=>f.price<p0*0.97);
 const hm=t.entry.slice(11,16);
 rows.push({d:day(t.entry),y:t.entry.slice(0,4),und:t.und,dte:dd(day(t.entry),t.exp),hm,net,risk:t.avgIn*t.eq*100,hold:t.hold,expired,avgDown,qty:t.eq});
}
function stats(a){if(!a.length)return null;const w=a.filter(r=>r.net>0),l=a.filter(r=>r.net<0);const sum=x=>x.reduce((s,r)=>s+r.net,0);
 const aw=w.length?sum(w)/w.length:0,al=l.length?sum(l)/l.length:0;
 return {n:a.length,net:Math.round(sum(a)),win:+(w.length/a.length*100).toFixed(1),avgW:Math.round(aw),avgL:Math.round(al),payoff:al?+(aw/-al).toFixed(2):null,exp:Math.round(sum(a)/a.length),pf:l.length?+(sum(w)/-sum(l)).toFixed(2):null};}
const by=(a,f)=>{const m={};a.forEach(r=>{const k=f(r);(m[k]=m[k]||[]).push(r)});return Object.fromEntries(Object.entries(m).sort().map(([k,v])=>[k,stats(v)]))};
const recent=rows.filter(r=>r.d>='2024-12-01'),old=rows.filter(r=>r.d<'2024-12-01');
const bucket=hm=>hm<'09:30'?'pre':hm<'10:00'?'09:30-10:00':hm<'11:30'?'10:00-11:30':hm<'14:00'?'11:30-14:00':hm<'15:00'?'14:00-15:00':hm<'16:00'?'15:00-16:00':'post';
const dteB=r=>r.dte<=0?'0DTE':r.dte<=2?'1-2DTE':r.dte<=7?'3-7DTE':'8+DTE';
function daily(a){const m={};a.forEach(r=>m[r.d]=(m[r.d]||0)+r.net);const v=Object.entries(m).sort();const nets=v.map(x=>x[1]);
 let peak=0,cum=0,mdd=0,streak=0,maxStreak=0;for(const x of nets){cum+=x;peak=Math.max(peak,cum);mdd=Math.min(mdd,cum-peak);streak=x<0?streak+1:0;maxStreak=Math.max(maxStreak,streak)}
 const s=[...nets].sort((a,b)=>a-b);const q=p=>Math.round(s[Math.floor(p*(s.length-1))]);
 return {days:nets.length,green:+(nets.filter(x=>x>0).length/nets.length*100).toFixed(1),worst5:s.slice(0,5).map(Math.round),best5:s.slice(-5).map(Math.round),p10:q(.1),median:q(.5),p90:q(.9),maxDD:Math.round(mdd),maxLosingStreakDays:maxStreak,worstDays:v.filter(x=>x[1]<=s[4]).map(x=>x[0]+' '+Math.round(x[1]))};}
const out={unknownSkipped:unk,
 all:stats(rows),old:stats(old),recent:stats(recent),
 recentRange:[recent.map(r=>r.d).sort()[0],recent.map(r=>r.d).sort().pop()],
 byYear:by(rows,r=>r.y),
 recentByDTE:by(recent,dteB),
 recent0DTEByTime:by(recent.filter(r=>r.dte<=0),r=>bucket(r.hm)),
 recentByTime:by(recent,r=>bucket(r.hm)),
 recentByUnd:Object.fromEntries(Object.entries(by(recent,r=>r.und)).sort((a,b)=>b[1].n-a[1].n).slice(0,8)),
 recentAvgDown:{yes:stats(recent.filter(r=>r.avgDown)),no:stats(recent.filter(r=>!r.avgDown))},
 recentExpired:stats(recent.filter(r=>r.expired)),
 recentHold:by(recent,r=>r.hold==null?'expired':r.hold<120?'<2m':r.hold<600?'2-10m':r.hold<1800?'10-30m':r.hold<7200?'30m-2h':'2h+'),
 recentRisk:(()=>{const s=recent.map(r=>r.risk).sort((a,b)=>a-b);const q=p=>Math.round(s[Math.floor(p*(s.length-1))]);return{p50:q(.5),p90:q(.9),max:Math.round(s.pop())}})(),
 recentDaily:daily(recent),
 recentTradesPerDay:(()=>{const m={};recent.forEach(r=>m[r.d]=(m[r.d]||0)+1);const v=Object.values(m).sort((a,b)=>a-b);return{median:v[Math.floor(v.length/2)],max:v.pop()}})(),
 recentByTradeCountDay:(()=>{const m={};recent.forEach(r=>{(m[r.d]=m[r.d]||[]).push(r)});const g={};Object.values(m).forEach(a=>{const k=a.length<=3?'1-3':a.length<=8?'4-8':'9+';(g[k]=g[k]||[]).push(a.reduce((s,r)=>s+r.net,0))});return Object.fromEntries(Object.entries(g).map(([k,v])=>[k,{days:v.length,avgDay:Math.round(v.reduce((a,b)=>a+b,0)/v.length),green:+(v.filter(x=>x>0).length/v.length*100).toFixed(0)}]))})(),
 // after first N losing trades in a day, how do the rest of that day's trades do?
 afterTwoLosses:(()=>{const m={};recent.forEach(r=>(m[r.d]=m[r.d]||[]).push(r));const pre=[],post=[];Object.values(m).forEach(a=>{let L=0;a.forEach(r=>{(L>=2?post:pre).push(r);if(r.net<0)L++})});return{before:stats(pre),after:stats(post)}})()
};
console.log(JSON.stringify(out));const f1=recent.filter(r=>!(r.hm>="14:00"&&r.hm<"15:00")),f2=f1.filter(r=>r.und!=="SPXW"),f3=f2.filter(r=>!(r.dte<=0&&r.hm<"10:00"));console.log(JSON.stringify({base:stats(recent),no14:stats(f1),no14noSPX:stats(f2),plusNo0DTEbefore10:stats(f3),dailyF3:daily(f3),avgDownShare:+(recent.filter(r=>r.avgDown).length/recent.length*100).toFixed(0),riskAvgDown:Math.round(recent.filter(r=>r.avgDown).reduce((s,r)=>s+r.risk,0)/recent.filter(r=>r.avgDown).length),riskNo:Math.round(recent.filter(r=>!r.avgDown).reduce((s,r)=>s+r.risk,0)/recent.filter(r=>!r.avgDown).length)}));
