const fs = require('fs');
let c = fs.readFileSync('index.html', 'utf8');

// Fix: ,'like') -> ,'like') needs the + operator
// The problem: in the string concat, we have:
// JSON.stringify(r.userId) + ','like') 
// should be:
// JSON.stringify(r.userId) + ',\'like\')'
// meaning the JS string should have: ,'like') as HTML onclick arg

// Current (broken): + JSON.stringify(r.userId) + ','like')"
// Correct:          + JSON.stringify(r.userId) + ",'like')"

// The bad strings:
const bad1 = "JSON.stringify(r.userId) + ','like')\\\"";
const good1 = "JSON.stringify(r.userId) + \",'like')\\\"";

const bad2 = "JSON.stringify(r.userId) + ','dislike')\\\"";
const good2 = "JSON.stringify(r.userId) + \",'dislike')\\\"";

let fixed = 0;
if (c.includes(bad1)) {
  c = c.replace(bad1, good1);
  console.log('Fixed like quote');
  fixed++;
} else {
  console.log('bad1 not found - searching for context...');
  // Find toggleReaction in string concat context
  const idx = c.indexOf("toggleReaction(' + JSON.stringify(tKey) + ',' + JSON.stringify(r.userId)");
  if (idx >= 0) {
    console.log('Found toggleReaction call at:', idx);
    console.log('Context:', JSON.stringify(c.substring(idx, idx+150)));
  }
}

if (c.includes(bad2)) {
  c = c.replace(bad2, good2);
  console.log('Fixed dislike quote');
  fixed++;
} else {
  console.log('bad2 not found');
}

if (fixed > 0) {
  fs.writeFileSync('index.html', c, 'utf8');
  console.log('Saved', fixed, 'fixes');
} else {
  // Find the actual bad pattern
  const m1 = c.match(/JSON\.stringify\(r\.userId\) \+ ','like'\)/);
  const m2 = c.match(/JSON\.stringify\(r\.userId\) \+ ','dislike'\)/);
  console.log('Pattern match 1:', m1 ? JSON.stringify(m1[0]) : 'not found');
  console.log('Pattern match 2:', m2 ? JSON.stringify(m2[0]) : 'not found');
  
  // Try regex replacement
  let c2 = c.replace(/\+ ','like'\)/g, '+ ",'+"'"+'like'+"'"+')")');
  if (c2 !== c) { console.log('regex fix 1 worked'); c = c2; fixed++; }
  c2 = c.replace(/\+ ','dislike'\)/g, '+ ",\'dislike\')')');
  if (c2 !== c) { console.log('regex fix 2 worked'); c = c2; fixed++; }
  if (fixed > 0) fs.writeFileSync('index.html', c, 'utf8');
}
