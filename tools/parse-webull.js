const OCC=/^([A-Z.]{1,6})(\d{2})(\d{2})(\d{2})([CP])(\d{8})$/;
function parseCSV(text){
  const rows=[];let row=[],field='',q=false;
  for(let i=0;i<text.length;i++){const c=text[i];
    if(q){ if(c==='"'){ if(text[i+1]==='"'){field+='"';i++;} else q=false; } else field+=c; }
    else if(c==='"')q=true; else if(c===','){row.push(field);field='';}
    else if(c==='\n'||c==='\r'){ if(c==='\r'&&text[i+1]==='\n')i++; row.push(field);rows.push(row);row=[];field=''; }
    else field+=c;}
  if(field||row.length){row.push(field);rows.push(row);}
  return rows.filter(r=>r.length>1||r[0]);
}
function parseTime(s){ // "09/16/2026 15:57:55 EDT" -> "2026-09-16T15:57:55" (ET wall clock)
  if(!s)return null;const m=s.trim().match(/^(\d{2})\/(\d{2})\/(\d{4})\s+(\d{2}):(\d{2})(?::(\d{2}))?/);
  if(m)return `${m[3]}-${m[1]}-${m[2]}T${m[4]}:${m[5]}:${m[6]||'00'}`;
  const m2=s.trim().match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})/);
  return m2?`${m2[1]}-${m2[2]}-${m2[3]}T${m2[4]}:${m2[5]}:${m2[6]}`:null;
}
function parsePrice(s){ if(s==null)return null;const v=parseFloat(String(s).trim().replace(/^@/,'').replace(/,/g,''));return isNaN(v)?null:v; }
function parseWebull(text){
  const rows=parseCSV(text.replace(/^﻿/,''));if(rows.length<2)throw new Error('Empty file');
  const hdr=rows[0].map(h=>h.trim().toLowerCase());
  const col=(...names)=>{for(const n of names){const i=hdr.indexOf(n);if(i>=0)return i;}return -1;};
  const cSym=col('symbol','name'),cSide=col('side','action'),cFilled=col('filled','filled qty','quantity'),
        cAvg=col('avg price','avg. price','average price'),cPrice=col('price'),cT=col('filled time','filled at','time'),
        cTif=col('time-in-force','tif'),cStatus=col('status'),cP=col('placed time');
  if(cSym<0||cSide<0||cFilled<0||cT<0)throw new Error('Not a Webull orders export (columns found: '+rows[0].join(', ')+')');
  const fills=[];
  rows.slice(1).forEach((r,idx)=>{
    const status=cStatus>=0?(r[cStatus]||'').trim().toLowerCase():'filled';
    if(status&&!/^(filled|partially filled|partial)$/.test(status))return;
    const qty=Math.round(parseFloat(r[cFilled]||'0'));if(!(qty>0))return;
    const sd=(r[cSide]||'').trim().toUpperCase();const side=sd.startsWith('BUY')?'BUY':(sd.startsWith('SELL')||sd.startsWith('SHORT'))?'SELL':null;if(!side)return;
    let price=cAvg>=0?parsePrice(r[cAvg]):null;if(price==null&&cPrice>=0)price=parsePrice(r[cPrice]);if(price==null)return;
    const t=parseTime(r[cT]);if(!t)return;
    const symbol=(r[cSym]||'').trim().toUpperCase();const pt=cP>=0?(parseTime(r[cP])||''):'';
    // two distinct orders can fill in the same second at the same price, so the placed time is part of the identity
    fills.push(hydrate({k:`${symbol}|${side}|${qty}|${price.toFixed(6)}|${t}|${pt}`,sym:symbol,side,qty,price,t,p:pt,tif:cTif>=0?(r[cTif]||'').trim():'',row:idx+2}));
  });
  return fills;
}
function hydrate(f){ // derive contract fields from the symbol (not stored, to keep documents small)
  if(f.und)return f;const m=f.sym.match(OCC);
  if(m){f.und=m[1];f.type='option';f.mult=100;f.exp=`20${m[2]}-${m[3]}-${m[4]}`;f.right=m[5];f.strike=parseInt(m[6],10)/1000;}
  else{f.und=f.sym;f.type='stock';f.mult=1;}
  if(f.row==null)f.row=0;return f;
}
function compact(f){return {k:f.k,sym:f.sym,side:f.side,qty:f.qty,price:f.price,t:f.t,p:f.p||'',tif:f.tif||''};}
function shardOf(t){const d=+t.slice(8,10);return t.slice(0,7)+(d<=10?'a':d<=20?'b':'c');} // ten-day documents stay well under the 256 KiB cap
function hash(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}let h2=5381;for(let i=0;i<s.length;i++)h2=((h2*33)^s.charCodeAt(i))>>>0;return h.toString(16).padStart(8,'0')+h2.toString(16).padStart(8,'0');}
function secs(a,b){return Math.round((Date.parse(b+'Z')-Date.parse(a+'Z'))/1000);}
function buildTrades(fills,opts){
  const feeC=opts.feeC||0,feeS=opts.feeS||0,longOnly=opts.longOnly!==false;
  const bySym={};[...fills].sort((a,b)=>a.t<b.t?-1:a.t>b.t?1:(a.p||'')<(b.p||'')?-1:(a.p||'')>(b.p||'')?1:b.row-a.row).forEach(f=>(bySym[f.sym]=bySym[f.sym]||[]).push(f));
  const trades=[];
  const mk=(f,dir)=>({dir,fills:[],eq:0,ec:0,xq:0,xc:0,first:f,last:null,flags:[]});
  const fin=(o,unknown)=>{
    const f0=o.first,mult=f0.mult,fee=f0.type==='option'?feeC:feeS;
    const base={sym:f0.sym,und:f0.und,type:f0.type,mult,exp:f0.exp||null,strike:f0.strike||null,right:f0.right||null,entry:f0.t,fills:o.fills.map(x=>({side:x.side,qty:x.qty,price:x.price,t:x.t,tif:x.tif})),flags:o.flags};
    if(unknown){const ax=o.xc/o.xq;return Object.assign(base,{key:hash(`${f0.sym}|UNKNOWN|${f0.t}`),dir:'LONG',exit:o.last.t,eq:0,xq:o.xq,avgIn:null,avgOut:ax,gross:null,fees:+(fee*o.xq).toFixed(2),net:null,status:'CLOSED',result:'UNKNOWN',hold:null});}
    const ai=o.ec/o.eq,ax=o.xq?o.xc/o.xq:null,sign=o.dir==='LONG'?1:-1;
    const gross=o.xq?(ax-ai)*o.xq*mult*sign:0,fees=fee*(o.eq+o.xq),net=gross-fees,closed=o.eq===o.xq;
    const result=!closed?'OPEN':net>0.005?'WIN':net<-0.005?'LOSS':'SCRATCH';
    const exit=closed&&o.last?o.last.t:null;
    return Object.assign(base,{key:hash(`${f0.sym}|${o.dir}|${f0.t}`),dir:o.dir,exit,eq:o.eq,xq:o.xq,avgIn:+ai.toFixed(6),avgOut:ax==null?null:+ax.toFixed(6),gross:+gross.toFixed(2),fees:+fees.toFixed(2),net:+net.toFixed(2),status:closed?'CLOSED':'OPEN',result,hold:exit?secs(f0.t,exit):null});
  };
  for(const sym in bySym){
    let pos=0,cur=null,orphan=null;
    const flush=()=>{if(orphan){trades.push(fin(orphan,true));orphan=null;}};
    for(const f of bySym[sym]){
      let rem=f.qty;if(f.side==='BUY')flush();
      while(rem>0){
        if(pos===0){
          if(f.side==='SELL'&&f.type==='option'&&longOnly){ if(!orphan){orphan=mk(f,'LONG');orphan.flags.push('PRE_WINDOW_ENTRY');} orphan.xq+=rem;orphan.xc+=rem*f.price;orphan.fills.push(f);orphan.last=f;rem=0;continue; }
          const dir=f.side==='BUY'?'LONG':'SHORT';cur=mk(f,dir);if(dir==='SHORT'&&f.type==='option')cur.flags.push('ORPHAN_SELL_OPEN');
          cur.eq+=rem;cur.ec+=rem*f.price;cur.fills.push(f);pos=dir==='LONG'?rem:-rem;rem=0;
        }else if((pos>0)===(f.side==='BUY')){ cur.eq+=rem;cur.ec+=rem*f.price;cur.fills.push(f);pos+=pos>0?rem:-rem;rem=0; }
        else{ const c=Math.min(rem,Math.abs(pos));cur.xq+=c;cur.xc+=c*f.price;cur.fills.push(f);cur.last=f;pos+=pos>0?-c:c;rem-=c; if(pos===0){trades.push(fin(cur,false));cur=null;} }
      }
    }
    flush();if(cur)trades.push(fin(cur,false));
  }
  trades.forEach(t=>{t.date=(t.exit||t.entry).slice(0,10);});
  return trades.sort((a,b)=>a.entry<b.entry?-1:1);
}


/* Lifted verbatim from section 1 of the Webull Trade Journal page so the repo
   no longer has to scrape it out of an HTML file on Drive. Do not "tidy" it:
   the page and this file must parse identically, or the mirror and the page
   disagree about what a fill is. */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { OCC, parseCSV, parseWebull, hydrate, compact, shardOf, hash, secs, buildTrades };
}
