import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
let pw;
try{pw=require(process.env.VERITALEX_PLAYWRIGHT||'playwright');}
catch{pw=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));}
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const base=(process.env.VERITALEX_BASE_URL||'http://127.0.0.1:4175').replace(/\/$/,'');
let executable=process.env.VERITALEX_CHROME||pw.chromium.executablePath();
const exists=async p=>{try{await fs.access(p);return true;}catch{return false;}};
if(!await exists(executable)){
 const cache=path.join(os.homedir(),'Library/Caches/ms-playwright');
 for(const dir of (await fs.readdir(cache)).filter(x=>x.startsWith('chromium_headless_shell-')).sort().reverse()){
  const p=path.join(cache,dir,'chrome-headless-shell-mac-arm64/chrome-headless-shell');
  if(await exists(p)){executable=p;break;}
 }
}
const browser=await pw.chromium.launch({headless:true,executablePath:executable});
const page=await browser.newPage();
const errors=[];
page.on('pageerror',e=>errors.push(e.message));
const report={kind:'clarity-reference-review',results:[],errors};
const slugs=JSON.parse(await fs.readFile(path.join(root,'metadata.json'),'utf8')).stitchScreens.map(x=>x.slug);
async function inspect(slug,width,large=false){
 await page.setViewportSize({width,height:slug.startsWith('tablet-')?1024:915});
 await page.goto(base+'/designs/'+slug+'.html',{waitUntil:'networkidle'});
 await page.evaluate(()=>document.fonts.ready);
 if(large)await page.evaluate(()=>{
  const all=[...document.querySelectorAll('body *')].filter(e=>e instanceof HTMLElement&&!e.closest('[aria-hidden="true"]')&&!e.matches('.material-symbols-outlined,.material-symbols-rounded')).map(e=>({e,size:parseFloat(getComputedStyle(e).fontSize),line:parseFloat(getComputedStyle(e).lineHeight)}));
  for(const {e,size,line} of all){e.style.fontSize=size*2+'px';if(Number.isFinite(line))e.style.lineHeight=line*2+'px';}
 });
 const result=await page.evaluate(()=>{
  const active=[...document.querySelectorAll('a[href],button,summary,input,select,textarea')].filter(e=>{
   const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden';
  });
  const target=e=>(e.matches('input')?e.closest('label'):null)||e;
  const small=active.filter(e=>{const r=target(e).getBoundingClientRect();return r.width<47||r.height<47;}).map(e=>({label:e.getAttribute('aria-label')||e.textContent.trim().slice(0,60),tag:e.tagName,width:target(e).getBoundingClientRect().width,height:target(e).getBoundingClientRect().height}));
  const unnamed=active.filter(e=>e.matches('button,summary')&&!e.getAttribute('aria-label')&&!e.textContent.trim()).map(e=>e.outerHTML.slice(0,180));
  const clips=active.filter(e=>e.matches('a,button,summary')&&e.scrollHeight>e.clientHeight+2&&getComputedStyle(e).overflowY==='hidden').map(e=>e.textContent.trim().slice(0,80));
  return {title:document.title,bodyOverflow:document.documentElement.scrollWidth>innerWidth+2,small,unnamed,clips,externalResources:performance.getEntriesByType('resource').map(x=>x.name).filter(x=>/^https?:/.test(x)&&new URL(x).origin!==location.origin),links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(Boolean)};
 });
 const broken=[];
 for(const href of result.links){
  if(/^(https?:|mailto:|data:)/.test(href))continue;
  if(href==='#'){broken.push(href);continue;}
  const file=decodeURIComponent(href.split(/[?#]/)[0]);
  if(file&&!await exists(path.resolve(root,'designs',file)))broken.push(href);
 }
 delete result.links;
 report.results.push({slug,width,large,...result,broken});
}
try{
 for(const slug of slugs)for(const width of slug.startsWith('tablet-')?[800,1280]:[360,412])await inspect(slug,width);
 for(const slug of ['home','book-details','library','journal','reader-appearance','dark-home','tablet-library','tablet-journal'])await inspect(slug,slug.startsWith('tablet-')?1280:360,true);
 await page.setViewportSize({width:1280,height:1024});
 await page.goto(base+'/designs/tablet-reader.html',{waitUntil:'networkidle'});
 await page.locator('[data-panel="bookmarks-list"]').click();
 await page.getByRole('button',{name:'Remove bookmark',exact:true}).click();
 const saved=page.locator('[data-bookmark-saved]');
 if(await saved.isVisible()||await saved.locator('a').getAttribute('href')!==null||!await page.locator('[data-bookmark-empty]').isVisible())throw new Error('Removed bookmark remains visible or linked in tablet Reader.');
 await page.locator('[data-panel="contents-list"]').click();
 await page.locator('[data-panel="bookmarks-list"]').click();
 if(await saved.isVisible())throw new Error('Switching tabs recreated a removed bookmark.');
 await page.getByRole('button',{name:'Add bookmark',exact:true}).click();
 if(!await saved.isVisible()||!await saved.locator('a').getAttribute('href')||await page.locator('[data-bookmark-empty]').isVisible())throw new Error('Adding a bookmark did not restore its visible row and link.');
 report.interactions=[{name:'Tablet bookmark removal, tab switching and re-addition keep row, link and selected state consistent',passed:true}];
 await page.setViewportSize({width:1440,height:1000});
 await page.goto(base+'/revisions/clarity-v1/index.html',{waitUntil:'networkidle'});
 await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:path.join(root,'revisions/clarity-v1/comparison.png'),fullPage:true});
 report.comparison={images:await page.locator('img').count(),loaded:await page.locator('img').evaluateAll(images=>images.every(i=>i.complete&&i.naturalWidth>0))};
 report.passed=!errors.length&&report.comparison.loaded&&report.results.every(r=>!r.bodyOverflow&&!r.small.length&&!r.unnamed.length&&!r.clips.length&&!r.broken.length&&!r.externalResources.length);
 await fs.writeFile(path.join(root,'qa/clarity-references.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({passed:report.passed,cases:report.results.length,errors,failures:report.results.filter(r=>r.bodyOverflow||r.small.length||r.unnamed.length||r.clips.length||r.broken.length||r.externalResources.length)}));
 process.exitCode=report.passed?0:1;
}finally{await browser.close();}
