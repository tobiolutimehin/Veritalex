import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createRequire} from 'node:module';

const require=createRequire(import.meta.url);
let playwright;
try{playwright=require(process.env.VERITALEX_PLAYWRIGHT||'playwright');}
catch{playwright=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));}
const {chromium}=playwright;
const exists=async file=>{try{await fs.access(file);return true;}catch{return false;}};
let executable=process.env.VERITALEX_CHROME||chromium.executablePath();
if(!await exists(executable)){
  const cache=path.join(os.homedir(),'Library/Caches/ms-playwright');
  const builds=await fs.readdir(cache).catch(()=>[]);
  const candidates=builds.filter(x=>x.startsWith('chromium_headless_shell-')).sort().reverse().map(x=>path.join(cache,x,'chrome-headless-shell-mac-arm64/chrome-headless-shell'));
  candidates.push('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');
  for(const candidate of candidates)if(await exists(candidate)){executable=candidate;break;}
}
const browser=await chromium.launch({headless:true,executablePath:executable});
const page=await browser.newPage({viewport:{width:1400,height:1080}});
const errors=[];
page.on('pageerror',error=>errors.push(error.message));
const base=(process.env.VERITALEX_BASE_URL||'http://127.0.0.1:4175').replace(/\/$/,'');
const frame=()=>page.frameLocator('#prototype-frame');
const ready=async id=>frame().locator('.phone[data-screen-id="'+id+'"]').waitFor();
const jump=async id=>{await page.selectOption('#screen-select',id);await ready(id);};
const act=async(id,target)=>{await frame().locator('[data-action="'+id+'"]:visible').first().click();await ready(target);};
try{
  await page.goto(base+'/prototype.html',{waitUntil:'networkidle'});
  await jump('shelf-detail');
  const summary=frame().getByLabel('Shelf options',{exact:true});
  await summary.focus();
  await page.keyboard.press('Enter');
  assert.equal(await frame().locator('.overflow').getAttribute('open'),'');
  await page.keyboard.press('Escape');
  assert.equal(await frame().locator('.overflow').getAttribute('open'),null);
  assert(await summary.evaluate(el=>el===document.activeElement));
  await summary.click();
  await act('rename','shelf-rename');
  await frame().getByLabel('Shelf name',{exact:true}).fill('Revisited classics');
  await act('save','shelf-detail');
  await frame().locator('.topbar h1').filter({hasText:'Revisited classics'}).waitFor();
  const booksBefore=await page.evaluate(()=>window.__veritalexPrototype.getState().guest.books.join(','));
  await frame().getByLabel('Shelf options',{exact:true}).click();
  await act('delete','shelf-delete');
  assert((await frame().locator('.dialog-body').innerText()).includes('Library'));
  await act('delete','shelves-after-delete');
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().guest.books.join(',')),booksBefore);

  await jump('reader-scroll');
  await frame().locator('[data-bookmark-control][aria-pressed="false"]').waitFor();
  await frame().getByRole('button',{name:'Add bookmark',exact:true}).click();
  await ready('reader-bookmark');
  await frame().locator('[data-bookmark-control][aria-pressed="true"][aria-label="Remove bookmark"]').waitFor();
  await act('back','reader-scroll');
  await frame().locator('[data-bookmark-control][aria-pressed="true"]').waitFor();
  await frame().getByRole('button',{name:'Remove bookmark',exact:true}).click();
  await ready('reader-scroll');
  await frame().locator('[data-bookmark-control][aria-pressed="false"][aria-label="Add bookmark"]').waitFor();
  assert.deepEqual(await frame().locator('.reader-actions .reader-tool span').allTextContents(),['Contents','Appearance','Search','Journal']);
  await act('journal','journal-book');
  await act('back','reader-scroll');

  await jump('journal-all');
  assert.equal(await frame().locator('.phone [data-action="new"]').count(),1);
  assert.equal(await frame().locator('.phone [data-action="passage"]').count(),0);
  await act('entry','journal-view');
  await frame().getByRole('link',{name:'Return to passage',exact:true}).waitFor();
  await jump('journal-all');
  await act('new','journal-book-picker');
  await act('book-84','journal-create');
  await frame().getByLabel('Title',{exact:true}).fill('A thought without a passage');
  await frame().getByLabel('Your thought',{exact:true}).fill('Keep this personal writing.');
  await act('save','journal-view');
  await frame().getByRole('heading',{name:'A thought without a passage',exact:true}).waitFor();
  assert.equal(await frame().locator('.phone [data-action="passage"]').count(),0);

  await page.setViewportSize({width:392,height:960});
  await jump('reader-appearance');
  await frame().locator('.phone').evaluate(el=>{
    const sizes=[...el.querySelectorAll('*')].map(child=>{const style=getComputedStyle(child);return {child,size:parseFloat(style.fontSize),line:parseFloat(style.lineHeight)};});
    for(const {child,size,line} of sizes){child.style.fontSize=size*2+'px';if(Number.isFinite(line))child.style.lineHeight=line*2+'px';}
  });
  const controls=frame().locator('.dialog-body button,.dialog-body input[type="range"],.dialog-body [data-action="done"]');
  for(let i=0;i<await controls.count();i++){
    const control=controls.nth(i);
    await control.scrollIntoViewIfNeeded();
    assert(await control.evaluate(el=>{const r=el.getBoundingClientRect(),d=el.closest('dialog').getBoundingClientRect();return r.width>=47&&r.height>=47&&r.top>=d.top&&r.bottom<=d.bottom;}));
  }
  await page.goto(base+'/prototype.html?book=1342#book-new',{waitUntil:'networkidle'});
  await ready('book-new');
  await act('save','book-saved');
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().guest.statuses['1342']),'Want to read');
  await page.goto(base+'/prototype.html?book=84#book-new',{waitUntil:'networkidle'});
  await ready('book-saved');
  await frame().getByRole('heading',{name:'Frankenstein',exact:true}).waitFor();
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().guest.books.join(',')),'1342,84,11');
  await page.goto(base+'/prototype.html?shelf=reading-next#shelf-delete',{waitUntil:'networkidle'});
  await ready('shelf-delete');
  await frame().locator('.dialog-body h2').filter({hasText:'Reading next'}).waitFor();
  assert.equal(await frame().locator('.modal-background .topbar h1').innerText(),'Reading next');
  await page.goto(base+'/prototype.html?book=1342&position=account#reader-scroll',{waitUntil:'networkidle'});
  await ready('reader-scroll');
  await frame().locator('.reader-content h2').filter({hasText:'Chapter 19'}).waitFor();
  await page.goto(base+'/prototype.html?subject=Gothic%20fiction#explore-results',{waitUntil:'networkidle'});
  await ready('explore-results');
  await frame().locator('[data-live-books] .book').last().waitFor();
  assert.deepEqual(await frame().locator('[data-live-books] .book h2').allTextContents(),['Frankenstein','Jane Eyre']);
  await page.goto(base+'/prototype.html?workspace=account#home-returning',{waitUntil:'networkidle'});
  await ready('home-returning');
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().workspace),'account');
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().guest.entries.length),1);
  assert.equal(await page.evaluate(()=>window.__veritalexPrototype.getState().account.entries.length),1);
  await page.goto(base+'/prototype.html?workspace=account&book=1342#book-reading',{waitUntil:'networkidle'});
  await ready('book-reading');
  await frame().locator('[role="progressbar"][aria-valuenow="31"]').waitFor();
  assert.deepEqual(errors,[]);
  const verificationSummary='Shelf overflow keyboard/focus, rename/delete scope, bookmark action/selected state, Journal passage gating, enlarged-text appearance reachability and validated reference contexts.';
  await fs.writeFile(new URL('../qa/clarity-state-regression.json',import.meta.url),JSON.stringify({passed:true,summary:verificationSummary,errors},null,2));
  console.log('PASS: '+verificationSummary);
}catch(error){
  await fs.writeFile(new URL('../qa/clarity-state-regression.json',import.meta.url),JSON.stringify({passed:false,error:error.message,errors},null,2));
  throw error;
}finally{await browser.close();}
