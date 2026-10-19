// Execute the actual embedded dashboard JS with a minimal DOM; check every interaction.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path');
const html=fs.readFileSync(path.join(__dirname,'outputs/dashboard.html'),'utf8');
const script=html.match(/<script>([\s\S]*)<\/script>/)[1];
const elements={};const rowObjects=Array.from({length:10},()=>({}));
const get=s=>elements[s]??=(s==='#case'?{value:'base'}:s==='#statement'?{value:'income_statement'}:{});
const context={document:{querySelector:get,querySelectorAll:s=>rowObjects}};
vm.createContext(context);vm.runInContext(script,context,{timeout:3000});
assert(get('#cards').innerHTML.includes('WATCH / DEFER'));
assert(get('#bridge').innerHTML.includes('less_pending_acquisition_cash_pv'));
get('#case').value='low';get('#case').onchange();
assert(get('#cards').innerHTML.includes('DO NOT INITIATE'));
get('#case').value='high';get('#case').onchange();assert(get('#story').textContent.includes('Sustained'));
get('#statement').value='cash_flow';get('#statement').onchange();assert(get('#statements').innerHTML.includes('acquisition_cash'));
get('#statement').value='balance_sheet';get('#statement').onchange();assert(get('#statements').innerHTML.includes('total_assets'));
rowObjects[1].onclick();assert(get('#picked').textContent.includes('Selected value'));
get('#case').value='base';get('#case').onchange();assert(get('#reverse').textContent.includes('additional percentage points'));
console.log('PASS: base/low/high case, income/BS/CF selectors, bridge, sensitivity click and reverse DCF');
