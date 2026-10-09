#!/usr/bin/env node
// Capture actual local screen states. Screenshot review stays an explicit human/agent step.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{createRequire}=require('module');
async function main(){
 const args=process.argv.slice(2),inputArg=args.find(x=>!x.startsWith('--'));if(!inputArg)throw Error('Usage: node capture_screens.cjs scenarios.json [--overwrite]');
 const input=path.resolve(inputArg),base=path.dirname(input),data=JSON.parse(fs.readFileSync(input,'utf8')),overwrite=args.includes('--overwrite');
 const getModule=createRequire(path.join(process.cwd(),'package.json'));
 const {chromium}=getModule(process.env.PLAYWRIGHT_MODULE||'playwright');
 const viewport={width:1600,height:1000,device_scale_factor:2};
 const within=p=>{const r=path.relative(base,p);return r!==''&&!r.startsWith('..'+path.sep)&&r!=='..'&&!path.isAbsolute(r)};
 const targets=[];
 for(const scene of data.scenes){
  if(!/^[A-Za-z][A-Za-z0-9_-]*$/.test(scene.id))throw Error('Invalid scenario ID');
  const demo=path.resolve(base,scene.demo);if(!within(demo)||!fs.existsSync(demo)||!demo.endsWith('.html'))throw Error('Scenario HTML does not exist or escapes the delivery directory');
  for(const phase of ['before','after',...(scene.result_required?['result']:[])])targets.push(path.join(base,'images',scene.id+'-'+phase+'.png'));
 }
 const reportPath=path.join(base,'capture-report.json');
 if(!overwrite&&[...targets,reportPath].some(p=>fs.existsSync(p)))throw Error('Captures or receipt already exist; inspect before using --overwrite or a new directory');
 fs.mkdirSync(path.join(base,'images'),{recursive:true});
 const browser=await chromium.launch({headless:true});const records=[],errors=[];
 try{
  for(const scene of data.scenes){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},deviceScaleFactor:viewport.device_scale_factor});
   const runtimeErrors=[],network=[];page.on('pageerror',e=>runtimeErrors.push(e.message));
   await page.route('**/*',route=>{if(/^https?:/.test(route.request().url())){network.push(route.request().url());return route.abort()}return route.continue()});
   let afterText='';
   for(const phase of ['before','after',...(scene.result_required?['result']:[])]){
    try{
     if(phase!=='result'){
      const url=pathToFileURL(path.resolve(base,scene.demo));url.searchParams.set('state',phase);await page.goto(url.href);await page.locator('body[data-state="'+phase+'"]').waitFor();
     }else{
      await page.locator('[data-primary]').click();await page.locator('body[data-state="result"]').waitFor();
     }
     await page.evaluate(()=>document.fonts.ready);
     const root=page.locator('[data-capture-root]');await root.waitFor();
     const stateText=await page.locator('#blocks').innerText();
     if(phase==='after')afterText=stateText;
     if(phase==='result'&&stateText===afterText)throw Error('Action result has the same content as the before-action state');
     if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw Error('Horizontal page overflow');
     if(runtimeErrors.length||network.length)throw Error('Page script error or attempted external request: '+[...runtimeErrors,...network].join('; '));
     const file='images/'+scene.id+'-'+phase+'.png';await root.screenshot({path:path.join(base,file)});
     records.push({scene_id:scene.id,phase,status:'captured',file,page:scene.demo,viewport,checked:false,caption:scene.title+' · '+({before:'Before',after:'After',result:'Action result'}[phase]),provenance:'Local HTML/CSS simulation captured through actual browser rendering; not a production screenshot',interaction:phase==='result'?'Captured after clicking the primary action':'Captured from the specified page state'});
    }catch(error){const reason=String(error.message);records.push({scene_id:scene.id,phase,status:'failed',reason,caption:scene.title,provenance:'Browser capture incomplete'});errors.push({scene_id:scene.id,phase,reason});break}
   }
   await page.close();
  }
 }finally{await browser.close()}
 fs.writeFileSync(reportPath,JSON.stringify({created_at:new Date().toISOString(),method:'local_html_browser_capture',records,errors},null,2)+'\n');
 console.log(JSON.stringify({screenshots:records.filter(r=>r.status==='captured').length,errors,review:'Inspect screenshots before setting checked:true',report:'capture-report.json'}));
 return errors.length?2:0;
}
main().then(code=>process.exitCode=code).catch(e=>{console.error(e.message);process.exitCode=1});
