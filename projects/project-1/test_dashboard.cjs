// Exercise the exact generated viewer script without external browser dependencies.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, 'outputs/dashboard.html'), 'utf8');
const script = html.match(/<script>([\s\S]+)<\/script>/)[1];
const elements = new Map();
const document = { getElementById(id) {
  if (!elements.has(id)) elements.set(id, {value:id==='case'?'base':'',innerHTML:'',textContent:'',
    addEventListener(name, fn) {this[name]=fn;}});
  return elements.get(id);
}};
vm.runInNewContext(script, {document, Number, JSON}, {timeout:3000});
for (const name of ['base','low','high','churn_and_collections','ai_hosting_cost','cash_acquisitions_no_benefit']) {
  document.getElementById('case').value=name;
  document.getElementById('case').change();
  const decision=document.getElementById('decision').innerHTML;
  assert(decision.includes(name==='low'||name==='churn_and_collections'?'do not initiate':'watch/defer'));
  assert(document.getElementById('statements').innerHTML.includes('2031-07-31'));
  assert(document.getElementById('statements').innerHTML.includes('Cash tie error'));
  assert(!document.getElementById('statements').innerHTML.includes('NaN'));
}
console.log('PASS: exact generated dashboard script, all six selections, actions, five-year columns and checks');
