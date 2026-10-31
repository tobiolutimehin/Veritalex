import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
let playwright;
try{playwright=require(process.env.VERITALEX_PLAYWRIGHT||'playwright');}
catch{playwright=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));}
const {chromium}=playwright;
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const mode=process.argv[2]||'boards';
const baseUrl=(process.env.VERITALEX_BASE_URL||'http://127.0.0.1:4175').replace(/\/$/,'');
const exists=async p=>{try{await fs.access(p);return true;}catch{return false;}};
let executable=process.env.VERITALEX_CHROME||chromium.executablePath();
if(!await exists(executable)){
 const cache=path.join(os.homedir(),'Library/Caches/ms-playwright');
 const builds=await fs.readdir(cache).catch(()=>[]);
 const candidates=builds.filter(x=>x.startsWith('chromium_headless_shell-')).sort().reverse().map(x=>path.join(cache,x,'chrome-headless-shell-mac-arm64/chrome-headless-shell'));
 candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
 for(const candidate of candidates){if(await exists(candidate)){executable=candidate;break;}}
}
if(!await exists(executable))throw new Error('Install Playwright Chromium or set VERITALEX_CHROME to a browser executable.');
const browser=await chromium.launch({headless:true,executablePath:executable});
const context=await browser.newContext({viewport:{width:1440,height:1080},deviceScaleFactor:mode==='references'?2:1});
const page=await context.newPage();
const errors=[];
page.on('pageerror',error=>errors.push(error.message));
const report={mode,baseUrl,executable,errors,results:[]};
try{
 if(mode==='boards'){
  for(const folder of ['boards','polished-boards']){
   for(const file of (await fs.readdir(path.join(root,folder))).filter(x=>x.endsWith('.html')).sort()){
    await page.goto(baseUrl+'/'+folder+'/'+file,{waitUntil:'networkidle'});
    await page.evaluate(()=>document.fonts.ready);
    const dimensions=await page.evaluate(()=>({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight}));
    await page.setViewportSize({width:dimensions.width,height:Math.min(dimensions.height,2200)});
    await page.screenshot({path:path.join(root,folder,file.replace('.html','.png')),fullPage:true});
    report.results.push({file:folder+'/'+file,...dimensions});
   }
  }
 }else if(mode==='audit'){
  const manifest=JSON.parse(await fs.readFile(path.join(root,'screens.json'),'utf8'));
  for(const width of [360,412]){
   await page.setViewportSize({width,height:915});
   for(const screen of manifest.screens){
    await page.goto(baseUrl+'/polished/'+screen.id+'.html?embed=1',{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    const result=await page.evaluate(()=>{
     const phone=document.querySelector('.phone');
     const rect=phone.getBoundingClientRect();
     const overflow=[...phone.querySelectorAll('.topbar,.app-main,.bottomnav,.dialog-body')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({element:e.className,client:e.clientWidth,scroll:e.scrollWidth}));
     const smallTargets=[...phone.querySelectorAll('a[data-to],button,input,select')].filter(e=>{
      const label=e.matches('input')?e.closest('label'):null;
      const r=(label||e).getBoundingClientRect();return r.width>0&&r.height>0&&(r.height<47||r.width<47)&&!e.closest('.modal-background');
     }).map(e=>({label:e.getAttribute('aria-label')||e.textContent.trim(),width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}));
     return {phoneWidth:rect.width,viewport:innerWidth,bodyOverflow:document.documentElement.scrollWidth>innerWidth+2,overflow,smallTargets};
    });
    report.results.push({id:screen.id,width,...result});
   }
  }
 }else if(mode==='references'){
  await page.setViewportSize({width:390,height:915});
  const refinements=JSON.parse(await fs.readFile(path.join(root,'raw/reference-refinements.json'),'utf8'));
  for(const slug of Object.keys(refinements)){
   const tablet=slug.startsWith('tablet-');
   await page.setViewportSize(tablet?{width:1280,height:1024}:{width:390,height:915});
   await page.goto(baseUrl+'/designs/'+slug+'.html',{waitUntil:'networkidle'});
   await page.evaluate(()=>document.fonts.ready);
   if(!tablet){
    const height=await page.evaluate(()=>Math.max(915,document.documentElement.scrollHeight));
    await page.setViewportSize({width:390,height});
   }
   const styles=await page.evaluate(()=>[...document.styleSheets].flatMap(sheet=>{try{return [...sheet.cssRules].map(rule=>rule.cssText);}catch{return [];}}).join('\n'));
   if(styles.length<10000)throw new Error('Reference stylesheet did not finish loading: '+slug);
   await page.screenshot({path:path.join(root,'designs/'+slug+'.png'),fullPage:true});
   report.results.push({slug,stylesLength:styles.length,title:await page.title()});
  }
 }else if(mode==='large-text'){
  await page.setViewportSize({width:360,height:915});
  for(const id of ['home-returning','library-books','reader-scroll','reader-appearance','journal-create','shelf-create','account-signout-pending','settings-main']){
   await page.goto(baseUrl+'/polished/'+id+'.html?embed=1',{waitUntil:'load'});
   await page.evaluate(()=>document.fonts.ready);
   await page.evaluate(()=>{
    const items=[...document.querySelectorAll('.phone *')].filter(e=>e instanceof HTMLElement).map(e=>({e,size:parseFloat(getComputedStyle(e).fontSize),line:parseFloat(getComputedStyle(e).lineHeight)}));
    for(const {e,size,line} of items){e.style.fontSize=size*2+'px';if(Number.isFinite(line))e.style.lineHeight=line*2+'px';}
   });
   const result=await page.evaluate(()=>({bodyOverflow:document.documentElement.scrollWidth>innerWidth+2,overflow:[...document.querySelectorAll('.topbar,.app-main,.bottomnav,.dialog-body')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({element:e.className,client:e.clientWidth,scroll:e.scrollWidth}))}));
   await fs.mkdir(path.join(root,'qa/large-text'),{recursive:true});
   await page.screenshot({path:path.join(root,'qa/large-text',id+'.png')});
   report.results.push({id,...result});
  }
 }else if(mode==='flows'){
  const frame=()=>page.frameLocator('#prototype-frame');
  const ready=async()=>{await frame().locator('.phone').waitFor();};
  const jump=async id=>{await page.selectOption('#screen-select',id);await page.waitForURL(u=>u.hash==='#'+id);await ready();};
  const act=async id=>{await frame().locator('[data-action="'+id+'"]').first().click();await ready();};
  const check=(name,pass)=>{if(!pass)throw new Error(name);report.results.push({name,passed:true});};
  await fs.mkdir(path.join(root,'qa'),{recursive:true});
  await page.goto(baseUrl+'/prototype.html',{waitUntil:'networkidle'});
  await page.locator('[data-mode="styled"]').click();await ready();
  await frame().getByRole('link',{name:'Continue as guest',exact:true}).click();
  await page.waitForURL(u=>u.hash==='#home-first');await ready();
  await frame().getByRole('link',{name:/Pride and Prejudice Jane Austen/}).first().click();
  await page.waitForURL(u=>u.hash==='#book-new');await ready();
  await frame().getByRole('link',{name:'Want to read',exact:true}).click();
  await page.waitForURL(u=>u.hash==='#book-saved');
  await frame().getByText('In your library',{exact:true}).waitFor();
  check('Guest discovery and save updates the local library',true);
  await jump('journal-all');await act('new');
  await page.waitForURL(u=>u.hash==='#journal-book-picker');await ready();
  await act('book-1342');await page.waitForURL(u=>u.hash==='#journal-create');
  await frame().getByLabel('Title',{exact:true}).fill('A quiet observation');
  await frame().getByLabel('Your thought',{exact:true}).fill('First impressions deserve a second reading.');
  await act('save');await page.waitForURL(u=>u.hash==='#journal-view');
  await frame().getByText('First impressions deserve a second reading.',{exact:true}).waitFor();
  check('Journal book selection and actual saved form values',true);
  await act('edit');await page.waitForURL(u=>u.hash==='#journal-edit');
  await frame().getByLabel('Your thought',{exact:true}).fill('Keep this unfinished thought.');
  await act('back');await page.waitForURL(u=>u.hash==='#journal-discard');
  await frame().getByRole('link',{name:'Keep editing',exact:true}).click();await ready();
  await page.waitForFunction(expected=>document.querySelector('#prototype-frame')?.contentDocument?.querySelector('textarea')?.value===expected,'Keep this unfinished thought.',{timeout:5000});
  check('Cancelling discard preserves the actual journal draft',(await frame().getByLabel('Your thought',{exact:true}).inputValue())==='Keep this unfinished thought.');
  await frame().locator('.phone').screenshot({path:path.join(root,'qa/prototype-journal.png')});
  await jump('reader-appearance');
  await frame().getByRole('button',{name:'Paged',exact:true}).click();
  await frame().getByRole('button',{name:'Wide',exact:true}).click();
  await act('done');await page.waitForURL(u=>u.hash==='#reader-paged');await ready();
  check('Reader page mode and appearance preserve reading position',(await frame().locator('.phone').innerText()).includes('28%'));
  await frame().locator('.phone').screenshot({path:path.join(root,'qa/prototype-reader.png')});
  await jump('sync-conflict');
  await frame().getByRole('radio',{name:/Account/}).check();await act('use');await ready();
  await frame().getByText(/31%/).first().waitFor();
  check('Chosen other-device position is rendered in the reader',(await frame().locator('.phone').innerText()).includes('Chapter 19'));
  await frame().locator('.phone').screenshot({path:path.join(root,'qa/prototype-position.png')});
 }else if(mode==='overview'){
  await page.setViewportSize({width:1280,height:980});
  await page.goto(baseUrl+'/overview.html',{waitUntil:'networkidle'});
  await page.screenshot({path:path.join(root,'overview.png'),fullPage:true});
  report.results.push({title:await page.title()});
 }else if(mode==='gallery'){
  await page.goto(baseUrl+'/index.html',{waitUntil:'networkidle'});
  await page.screenshot({path:path.join(root,'gallery.png'),fullPage:false});
  report.results.push({title:await page.title(),cards:await page.locator('.screen-card').count()});
 }
 const failed=errors.length>0||report.results.some(x=>x.bodyOverflow||x.overflow?.length||x.smallTargets?.length);
 report.passed=!failed;
 process.exitCode=failed?1:0;
 await fs.mkdir(path.join(root,'qa'),{recursive:true});
 await fs.writeFile(path.join(root,'qa',mode+'.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({mode,pages:report.results.length,errors,overflow:report.results.filter(x=>x.bodyOverflow||x.overflow?.length).map(x=>({id:x.id,width:x.width,overflow:x.overflow})),smallTargets:report.results.filter(x=>x.smallTargets?.length).map(x=>({id:x.id,width:x.width,targets:x.smallTargets}))}));
}finally{await browser.close();}
