// ── All 255 municipalities with coordinates ────────────────────────────────────
const MUNI_COORDS = {
  "Rottenmann":[47.52,14.37],"Pinggau":[47.51,15.92],"Bad Mitterndorf":[47.56,13.93],
  "Stainz":[46.88,15.27],"Birkfeld":[47.38,15.68],"Gratwein-Straßengel":[47.13,15.33],
  "Sankt Peter am Ottersbach":[46.82,15.87],"Sankt Stefan im Rosental":[46.85,15.80],
  "Hitzendorf":[47.02,15.23],"Feldbach":[46.94,15.88],"Judenburg":[47.20,14.67],
  "Altaussee":[47.63,13.77],"Ilz":[47.05,15.69],"Gnas":[46.88,15.82],
  "Eggersdorf bei Graz":[47.12,15.43],"Burgau":[46.99,15.33],"Fehring":[46.93,16.07],
  "Obdach":[47.07,14.68],"Knittelfeld":[47.22,14.83],"Sankt Veit in der Südsteiermark":[46.78,14.73],
  "Neumarkt in der Steiermark":[47.08,14.42],"Kapfenberg":[47.44,15.29],
  "Hengsberg":[46.85,15.33],"Rohrbach an der Lafnitz":[47.13,15.96],
  "Sankt Marein bei Graz":[47.07,15.43],"Lieboch":[46.99,15.29],
  "Ilztal":[47.10,15.70],"Sankt Johann in der Haide":[47.16,16.05],
  "Spielberg":[47.22,15.13],"Paldau":[46.93,15.84],"Haus":[47.49,14.05],
  "Deutschlandsberg":[46.82,15.22],"Passail":[47.20,15.60],
  "Frauental an der Laßnitz":[46.90,15.12],"Anger":[47.12,15.57],
  "Pischelsdorf am Kulm":[47.17,15.73],"Graz":[47.07,15.44],
  "Zeltweg":[47.19,14.75],"Markt Hartmannsdorf":[47.17,15.87],"Öblarn":[47.51,13.68],
  "Hausmannstätten":[47.00,15.46],"Dobl-Zwaring":[46.97,15.39],
  "Sankt Marein-Feistritz":[47.17,15.20],"Tillmitsch":[46.85,15.30],
  "Eichkögl":[47.15,15.63],"Weiz":[47.22,15.62],"Ardning":[47.51,14.44],
  "Weinitzen":[47.13,15.47],"Hart bei Graz":[47.07,15.41],"Liezen":[47.57,14.23],
  "Gleisdorf":[47.10,15.72],"Söding-Sankt Johann":[46.95,15.07],
  "Bad Aussee":[47.61,13.77],"Gutenberg":[47.22,15.41],"Fischbach":[47.42,15.84],
  "Vorau":[47.27,15.93],"Waldbach-Mönichwald":[47.26,15.41],"Trofaiach":[47.38,15.00],
  "Wundschuh":[47.00,15.34],"Stubenberg":[47.22,15.66],"Gralla":[46.87,15.38],
  "Seiersberg-Pirka":[47.01,15.37],"Bad Schwanberg":[46.97,15.15],
  "Stallhofen":[46.96,15.34],"Wagna":[46.71,15.54],"Nestelbach bei Graz":[47.01,15.45],
  "Sankt Stefan ob Stainz":[46.90,15.18],"Gössendorf":[46.98,15.42],
  "Ligist":[47.06,15.17],"Deutschfeistritz":[47.13,15.34],
  "Groß Sankt Florian":[46.93,15.27],"Bruck an der Mur":[47.41,15.27],
  "Arnfels":[46.89,15.06],"Leibnitz":[46.78,15.54],
  "Sankt Martin im Sulmtal":[46.97,15.04],"Oberwölz":[47.11,14.33],
  "Frohnleiten":[47.38,15.23],"Gratkorn":[47.13,15.33],"Mureck":[46.72,15.76],
  "Stattegg":[47.08,15.28],"Haselsdorf-Tobelbad":[46.81,15.34],
  "Voitsberg":[47.05,15.12],"Gleinstätten":[46.85,15.38],
  "Straß in Steiermark":[46.85,15.54],"Premstätten":[46.96,15.38],
  "Wildon":[46.88,15.52],"Sankt Radegund bei Graz":[47.14,15.58],
  "Laßnitzhöhe":[47.08,15.59],"Hartl":[47.06,15.41],
  "Weißkirchen in Steiermark":[47.20,14.27],"Hartberg":[47.28,15.97],
  "Raaba-Grambach":[47.01,15.47],"Sankt Stefan ob Leoben":[47.44,15.02],
  "Pöllauberg":[47.34,15.88],"Sankt Bartholomä":[46.96,15.62],
  "Aich":[47.45,14.32],"Grafendorf bei Hartberg":[47.32,15.89],
  "Sankt Georgen ob Judenburg":[47.12,14.66],"Feldkirchen bei Graz":[47.06,15.35],
  "Sinabelkirchen":[47.00,15.80],"Kirchberg an der Raab":[47.08,15.80],
  "Leoben":[47.38,15.09],"Halbenrain":[46.83,15.90],
  "Edelsbach bei Feldbach":[47.08,15.82],"Wies":[46.82,15.16],
  "Sankt Jakob im Walde":[47.23,15.76],"Naas":[47.62,15.52],
  "Köflach":[47.07,15.08],"Neuberg an der Mürz":[47.52,15.59],
  "Thörl":[47.59,15.19],"Mürzzuschlag":[47.60,15.67],"Bärnbach":[47.20,15.13],
  "Aflenz":[47.46,15.23],"Friedberg":[47.43,16.06],"Eibiswald":[46.68,15.25],
  "Hartberg Umgebung":[47.30,16.00],"Ragnitz":[46.89,15.42],"Straden":[46.84,15.85],
  "Semriach":[47.22,15.40],"Krottendorf-Gaisfeld":[47.05,15.18],
  "Tieschen":[46.79,15.92],"Sankt Ruprecht an der Raab":[47.19,15.76],
  "Fürstenfeld":[47.05,16.08],"Leutschach an der Weinstraße":[46.68,15.47],
  "Klöch":[46.77,16.00],"Kaindorf":[47.22,15.88],"Lannach":[46.93,15.33],
  "Stanz im Mürztal":[47.55,15.41],"Riegersburg":[47.00,15.93],
  "Werndorf":[46.93,15.47],"Scheifling":[47.16,14.42],"Krieglach":[47.55,15.56],
  "Kirchbach-Zerlach":[46.96,15.85],"Sankt Georgen am Kreischberg":[47.10,14.43],
  "Allerheiligen bei Wildon":[46.87,15.53],"Landl":[47.73,14.72],
  "Vasoldsberg":[47.04,15.57],"Pöllau":[47.30,15.83],
  "Bad Waltersdorf":[47.15,16.00],"Sankt Lorenzen am Wechsel":[47.55,16.02],
  "Seckau":[47.27,14.78],"Mitterdorf an der Raab":[47.14,15.72],
  "Großsteinbach":[47.12,15.85],"Kumberg":[47.15,15.55],"Bad Blumau":[47.19,16.09],
  "Maria Lankowitz":[47.07,15.07],"Kapfenstein":[46.89,15.98],
  "Langenwang":[47.57,15.61],"Lang":[46.85,15.49],"Übelbach":[47.22,15.24],
  "Admont":[47.58,14.46],"Thal":[47.09,15.33],"Sankt Andrä-Höch":[46.87,15.63],
  "Thannhausen":[47.08,15.87],"Kammern im Liesingtal":[47.38,14.83],
  "Großklein":[46.76,15.43],"Kalsdorf bei Graz":[46.95,15.49],
  "Schladming":[47.39,13.69],"Sankt Anna am Aigen":[46.81,15.94],
  "Stainach-Pürgg":[47.53,14.11],"Heiligenkreuz am Waasen":[46.85,15.58],
  "Fladnitz an der Teichalm":[47.28,15.53],"Preding":[46.87,15.29],
  "Proleb":[47.40,15.07],"Sankt Barbara im Mürztal":[47.54,15.38],
  "Sankt Oswald bei Plankenwarth":[47.05,15.23],"Dechantskirchen":[47.38,16.03],
  "Lebring-Sankt Margarethen":[46.79,15.49],"Sankt Lorenzen im Mürztal":[47.52,15.44],
  "Edelschrott":[47.10,15.13],"Eisenerz":[47.54,14.89],"Mooskirchen":[47.00,15.18],
  "Sankt Martin am Wöllmißberg":[47.07,15.26],"Fernitz-Mellach":[46.94,15.47],
  "Greinbach":[47.28,16.00],"Heimschuh":[46.79,15.41],"Kindberg":[47.50,15.45],
  "St. Margarethen an der Raab":[47.10,15.73],"Mortantsch":[47.18,15.67],
  "Kainbach bei Graz":[47.10,15.55],"Pöls-Oberkurzheim":[47.23,14.61],
  "Ebersdorf":[46.95,15.82],"Großwilfersdorf":[47.12,16.05],
  "Albersdorf-Prebuch":[47.05,15.88],"Sankt Georgen an der Stiefing":[46.82,15.48],
  "Lafnitz":[47.40,16.02],"Feistritztal":[47.38,15.64],"Floing":[47.35,15.87],
  "Bad Radkersburg":[46.69,15.99],"Sankt Nikolai im Sausal":[46.77,15.41],
  "Sölk":[47.37,14.05],"Niklasdorf":[47.40,15.13],"Stadl-Predlitz":[47.08,14.17],
  "Lobmingtal":[47.21,14.85],"Kainach bei Voitsberg":[47.06,15.09],
  "Stiwoll":[47.08,15.22],"Aigen im Ennstal":[47.53,14.13],
  "Mettersdorf am Saßbach":[46.87,15.76],"Unzmarkt-Frauenburg":[47.18,14.48],
  "Pernegg an der Mur":[47.38,15.22],"Bad Loipersdorf":[46.94,16.06],
  "Murau":[47.11,14.17],"Pirching am Traubenberg":[47.02,15.67],
  "Wettmannstätten":[46.90,15.33],"Kobenz":[47.23,14.79],
  "Sankt Margarethen bei Knittelfeld":[47.20,14.82],"Fohnsdorf":[47.19,14.69],
  "Bad Gleichenberg":[46.87,15.90],"Peggau":[47.20,15.35],"Turnau":[47.55,15.47],
  "Gamlitz":[46.71,15.57],"Pölfing-Brunn":[46.84,15.15],"Ranten":[47.12,14.28],
  "Mariazell":[47.77,15.32],"Ottendorf an der Rittschein":[47.17,15.92],
  "Rohr bei Hartberg":[47.28,15.85],"Irdning-Donnersbachtal":[47.50,14.10],
  "Kraubath an der Mur":[47.30,14.96],"Söchau":[47.12,16.04],
  "Kitzeck im Sausal":[46.76,15.44],"Spital am Semmering":[47.59,15.76],
  "Rettenegg":[47.48,15.74],"Strallegg":[47.37,15.55],
  "Sankt Josef (Weststeiermark)":[46.87,15.21],
  "Gersdorf an der Feistritz":[47.16,15.72],
  "Sankt Johann im Saggautal":[46.82,15.39],"Schäffern":[47.46,16.00],
  "Sankt Peter im Sulmtal":[46.87,15.05],"Sankt Peter-Freienstein":[47.40,15.07],
  "Ratten":[47.47,15.72],"Mühlen":[46.94,14.48],"Pölstal":[47.22,14.62],
  "Altenmarkt bei Sankt Gallen":[47.70,14.65],"Niederwölz":[47.14,14.38],
  "Wildalpen":[47.66,14.98],"Gaal":[47.27,14.67],"Deutsch Goritz":[46.83,15.96],
  "Wörschach":[47.56,14.15],"Sankt Gallen":[47.70,14.63],
  "Breitenau am Hochlantsch":[47.35,15.35],"Schwarzautal":[46.78,15.36],
  "Wenigzell":[47.41,15.83],"Gaishorn am See":[47.52,14.56],
  "Sankt Michael in Obersteiermark":[47.33,15.01],
  "Sankt Peter ob Judenburg":[47.17,14.60],"Trieben":[47.49,14.49],
  "Empersdorf":[47.08,15.75],"Michaelerberg-Pruggern":[47.51,13.88],
  "Buch-St. Magdalena":[47.24,15.75],"Gabersdorf":[46.83,15.44],
  "Oberhaag":[46.71,15.40],"Puch bei Weiz":[47.26,15.67],
  "Schöder":[47.16,14.09],"Selzthal":[47.55,14.32],
  "Sankt Kathrein am Offenegg":[47.35,15.52]
};

const STATE_COLOR = { ADOPTED:'#00E5A0', AWARE:'#FFB930', UNAWARE:'#FF4D6D' };
const GROUP_LABEL = { 1:'Transition Leader',2:'CO₂ Reducer',3:'Energy Saver',4:'Tech Adopter',5:'New Builder',6:'No Actions' };

// ── Populate select ───────────────────────────────────────────────────────────
const sel = document.getElementById('municipality');
Object.keys(MUNI_COORDS).sort().forEach(name => {
  const opt = document.createElement('option');
  opt.value = name;
  opt.textContent = name;
  if (name === 'Stainz') opt.selected = true;
  sel.appendChild(opt);
});

// ── Slider bindings ───────────────────────────────────────────────────────────
[['numSteps','numStepsVal',0],['pUnaware','pUnawareVal',3],['pAware','pAwareVal',3],
 ['alpha','alphaVal',2],['beta','betaVal',2],['gamma','gammaVal',2]].forEach(([id,vid,dec]) => {
  document.getElementById(id).addEventListener('input', e => {
    document.getElementById(vid).textContent = parseFloat(e.target.value).toFixed(dec);
  });
});

// ── Map init ──────────────────────────────────────────────────────────────────
const map = L.map('map', { center:[47.07,15.44], zoom:13, zoomControl:true, attributionControl:false });
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom:19 }).addTo(map);

// ── State ─────────────────────────────────────────────────────────────────────
let apiData = null;
let sessionId = null;
let selectedAgentId = null;
let agentHistoryCache = {}; // id -> history data
let edgeLines = [];
let agentMarkers = {};
let agentStepStates = {};
let currentStep = 0;
let isPlaying = false, playTimer = null;

// ── Seeded random ─────────────────────────────────────────────────────────────
function seededRand(seed) {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => {
    s = s * 16807 % 2147483647;
    return (s - 1) / 2147483646;
  };
}

// ── API fetch ─────────────────────────────────────────────────────────────────
async function runSimulation() {
  const btn = document.getElementById('runBtn');
  const msg = document.getElementById('errMsg');
  msg.className = 'msg';
  btn.disabled = true;
  btn.textContent = '⏳ Loading...';

  const base  = document.getElementById('apiBase').value.replace(/\/$/,'');
  const muni  = document.getElementById('municipality').value;
  const steps = document.getElementById('numSteps').value;
  const pu    = document.getElementById('pUnaware').value;
  const pa    = document.getElementById('pAware').value;
  const al    = document.getElementById('alpha').value;
  const be    = document.getElementById('beta').value;
  const ga    = document.getElementById('gamma').value;

  const url = `${base}/simulation/steps?municipality=${encodeURIComponent(muni)}&num_steps=${steps}&p_unaware=${pu}&p_aware=${pa}&alpha=${al}&beta=${be}&gamma=${ga}`;

  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(30000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    apiData = await r.json();
    sessionId = apiData.session_id || null;
    msg.textContent = `✓ ${apiData.agents.length} agents · ${apiData.edges.length} edges`;
    msg.className = 'msg ok';
  } catch(e) {
    msg.textContent = `✗ ${e.message} — using demo data`;
    msg.className = 'msg err';
    apiData = demoData();
    sessionId = null;
  }

  // Reset agent history panel
  selectedAgentId = null;
  document.getElementById('agentInfo').innerHTML = 'Click an agent to see details.';
  document.getElementById('agentHistory').innerHTML = '';

  renderGraph();
  btn.disabled = false;
  btn.textContent = '▶ RUN SIMULATION';
}

// ── Render ────────────────────────────────────────────────────────────────────
function renderGraph() {
  if (!apiData) return;

  // Clear old layers
  edgeLines.forEach(l => map.removeLayer(l));
  edgeLines = [];
  Object.values(agentMarkers).forEach(m => map.removeLayer(m.marker));
  agentMarkers = {};
  agentHistoryCache = {};

  const muni   = apiData.municipality || document.getElementById('municipality').value;
  const center = MUNI_COORDS[muni] || [47.07, 15.44];
  const agents = apiData.agents;
  const edges  = apiData.edges;
  const steps  = apiData.steps;

  // Generate reproducible random positions around city center
  const rand   = seededRand(agents.length * 7919);
  const radius = Math.max(0.007, Math.min(0.022, 0.0025 * Math.sqrt(agents.length)));

  const positions = {};
  agents.forEach(a => {
    const angle = rand() * Math.PI * 2;
    const dist  = Math.sqrt(rand()) * radius;
    positions[a.id] = [
      center[0] + dist * Math.cos(angle),
      center[1] + dist * Math.sin(angle) * 1.5,
    ];
  });

  // ── Draw edges as L.polyline (reliable, always visible) ──────────────────
  edges.forEach(edge => {
    const a = positions[edge.source];
    const b = positions[edge.target];
    if (!a || !b) return;

    const w = edge.weight || 0.5;
    const line = L.polyline([a, b], {
      color:   '#3b82f6',
      weight:  Math.max(0.5, w * 2),
      opacity: Math.max(0.08, w * 0.45),
    }).addTo(map);
    edgeLines.push(line);
  });

  // ── Build per-agent state timeline ────────────────────────────────────────
  agentStepStates = buildTimeline(agents, steps);

  // ── Draw agent markers ────────────────────────────────────────────────────
  agents.forEach(a => {
    const pos   = positions[a.id];
    const state = a.state;
    const marker = makeMarker(pos, state, 13)
      .addTo(map)
      .on('click', () => showInfo(a));
    agentMarkers[a.id] = { marker };
  });

  // Setup slider
  const maxStep = steps.length - 1;
  const slider  = document.getElementById('stepSlider');
  slider.max    = maxStep;
  slider.value  = 0;
  document.getElementById('stepLbl').textContent = `/ ${maxStep} steps`;

  map.setView(center, 14);
  currentStep = 0;
  applyStep(0);
}

function makeMarker(pos, state, size) {
  const color = STATE_COLOR[state] || '#888';
  const icon  = L.divIcon({
    className: '',
    html: `<div class="agent-marker" style="width:${size}px;height:${size}px;background:${color};box-shadow:0 0 8px ${color}88"></div>`,
    iconSize:   [size, size],
    iconAnchor: [size/2, size/2],
  });
  return L.marker(pos, { icon, zIndexOffset: 600 });
}

function buildTimeline(agents, steps) {
  const result = {};
  agents.forEach(a => { result[a.id] = { 0: a.state }; });

  for (let t = 1; t < steps.length; t++) {
    const prev = steps[t-1].state_distribution;
    const curr = steps[t].state_distribution;

    const dAdopted = (curr.ADOPTED||0) - (prev.ADOPTED||0);
    const dAware   = (curr.AWARE||0)   - (prev.AWARE||0);

    // copy previous step
    agents.forEach(a => { result[a.id][t] = result[a.id][t-1]; });

    // AWARE -> ADOPTED
    let toAdopt = Math.max(0, dAdopted + Math.max(0, -dAware));
    if (toAdopt > 0) {
      agents.filter(a => result[a.id][t] === 'AWARE')
        .slice(0, toAdopt)
        .forEach(a => { result[a.id][t] = 'ADOPTED'; });
    }

    // UNAWARE -> AWARE
    let toAware = Math.max(0, dAware);
    if (toAware > 0) {
      agents.filter(a => result[a.id][t] === 'UNAWARE')
        .slice(0, toAware)
        .forEach(a => { result[a.id][t] = 'AWARE'; });
    }
  }
  return result;
}

function applyStep(step) {
  currentStep = step;
  document.getElementById('stepDisp').textContent = step;
  document.getElementById('stepSlider').value = step;

  if (!apiData) return;
  const sd   = apiData.steps[step].state_distribution;
  const rate = apiData.steps[step].adopted_rate;

  document.getElementById('sAdopted').textContent = sd.ADOPTED || 0;
  document.getElementById('sAware').textContent   = sd.AWARE   || 0;
  document.getElementById('sUnaware').textContent = sd.UNAWARE || 0;
  document.getElementById('sRate').textContent    = `${(rate*100).toFixed(1)}%`;
  document.getElementById('pfill').style.width    = `${rate*100}%`;

  // Update marker colors
  apiData.agents.forEach(a => {
    const info  = agentMarkers[a.id];
    if (!info) return;
    const state = (agentStepStates[a.id] || {})[step] || a.state;
    const color = STATE_COLOR[state] || '#888';
    const size  = 13;
    const icon  = L.divIcon({
      className: '',
      html: `<div class="agent-marker" style="width:${size}px;height:${size}px;background:${color};box-shadow:0 0 8px ${color}88"></div>`,
      iconSize:   [size, size],
      iconAnchor: [size/2, size/2],
    });
    info.marker.setIcon(icon);
  });
}

function onStep(val) {
  if (!apiData) return;
  applyStep(parseInt(val));
  // Refresh history highlight for selected agent
  if (selectedAgentId && agentHistoryCache[selectedAgentId]) {
    renderHistory(agentHistoryCache[selectedAgentId]);
  }
}

function showInfo(agent) {
  const state = (agentStepStates[agent.id] || {})[currentStep] || agent.state;
  const color = STATE_COLOR[state] || '#888';
  const age   = agent.age ? 2023 - agent.age : '—';
  const infoPas = ['None','1–2','3–5','>5'][agent.info_pas] || '—';
  document.getElementById('agentInfo').innerHTML =
    `<div style="color:${color};font-weight:700;margin-bottom:3px">Agent #${agent.id} — ${state}</div>` +
    `Group: <span>${agent.group} · ${GROUP_LABEL[agent.group]||'—'}</span><br>` +
    `Age: <span>${age}</span> &nbsp; Income: <span>${agent.income||'—'}</span><br>` +
    `Build age cat: <span>${agent.build_age||'—'}</span> &nbsp; Energy std: <span>${agent.energy_std||'—'}</span><br>` +
    `Subsidy: <span>${agent.subsidy===1?'Yes':agent.subsidy===0?'No':'—'}</span><br>` +
    `Network: <span>${infoPas}</span> known renovators`;

  selectedAgentId = agent.id;
  fetchAgentHistory(agent.id);
}

async function fetchAgentHistory(agentId) {
  const histEl = document.getElementById('agentHistory');
  histEl.innerHTML = '<div style="color:var(--muted);font-size:11px">Loading history...</div>';

  // Use cache if available
  if (agentHistoryCache[agentId]) {
    renderHistory(agentHistoryCache[agentId]);
    return;
  }

  if (!sessionId) {
    renderHistoryDemo(agentId);
    return;
  }

  const base = document.getElementById('apiBase').value.replace(/\/$/,'');
  try {
    const r = await fetch(`${base}/simulation/agent/${agentId}?session_id=${sessionId}`,
                          { signal: AbortSignal.timeout(10000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    agentHistoryCache[agentId] = data;
    renderHistory(data);
  } catch(e) {
    histEl.innerHTML = `<div style="color:var(--unaware);font-size:11px">✗ ${e.message}</div>`;
  }
}

function renderHistory(data) {
  const histEl = document.getElementById('agentHistory');
  if (!data || !data.steps) { histEl.innerHTML = ''; return; }

  const rows = data.steps.map(s => {
    const color  = STATE_COLOR[s.state] || '#888';
    const icon   = s.changed ? '⚡' : '·';
    const prob   = (s.adoption_probability * 100).toFixed(1);
    const active = s.step === currentStep
      ? 'background:#1e2d47;border-radius:5px;'
      : '';

    // Top influencers (adopted neighbors sorted by contribution)
    const topN = (s.neighbors || [])
      .filter(n => n.state === 'ADOPTED')
      .sort((a, b) => b.contribution - a.contribution)
      .slice(0, 3);

    const neighborHtml = topN.length
      ? topN.map(n =>
          `<span style="color:var(--muted)">  #${n.id} w=${n.weight.toFixed(2)} +${(n.contribution*100).toFixed(1)}%</span>`
        ).join('<br>')
      : `<span style="color:var(--muted)">  no active neighbors</span>`;

    // Reason text
    let reason = '';
    if (s.state === 'ADOPTED' && s.changed) {
      reason = `<span style="color:var(--adopted)">→ Adopted! prob ${prob}% triggered transition</span>`;
    } else if (s.state === 'ADOPTED' && !s.changed) {
      reason = `<span style="color:var(--muted)">Already adopted</span>`;
    } else if (s.changed) {
      reason = `<span style="color:var(--aware)">→ Became AWARE, prob ${prob}%</span>`;
    } else if (s.adoption_probability > 0) {
      reason = `<span style="color:var(--muted)">prob ${prob}% — not enough to change</span>`;
    } else {
      reason = `<span style="color:var(--muted)">No adopted neighbors yet</span>`;
    }

    return `
      <div style="padding:7px 8px;border-bottom:1px solid var(--border);${active}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px">
          <span style="font-family:var(--mono);font-size:11px;color:var(--muted)">step ${s.step}</span>
          <span style="font-size:11px;color:${color};font-weight:700">${icon} ${s.state}</span>
        </div>
        <div style="font-size:11px;margin-bottom:2px">${reason}</div>
        ${topN.length ? `<div style="font-size:10px;line-height:1.7">${neighborHtml}</div>` : ''}
      </div>`;
  }).join('');

  histEl.innerHTML = rows;

  // Scroll to current step
  const stepEls = histEl.querySelectorAll('[style*="border-bottom"]');
  if (stepEls[currentStep]) {
    stepEls[currentStep].scrollIntoView({ block: 'nearest' });
  }
}

function renderHistoryDemo(agentId) {
  document.getElementById('agentHistory').innerHTML =
    `<div style="color:var(--muted);font-size:11px;padding:6px">
      Run a real simulation to see step-by-step history for agent #${agentId}.
    </div>`;
}

function togglePlay() {
  if (!apiData) return;
  isPlaying = !isPlaying;
  document.getElementById('playBtn').textContent = isPlaying ? '⏸ Pause' : '▶ Play';
  if (isPlaying) {
    const max = apiData.steps.length - 1;
    if (currentStep >= max) applyStep(0);
    playTimer = setInterval(() => {
      if (currentStep >= max) {
        isPlaying = false;
        document.getElementById('playBtn').textContent = '▶ Play';
        clearInterval(playTimer);
        return;
      }
      applyStep(currentStep + 1);
    }, 900);
  } else {
    clearInterval(playTimer);
  }
}

// ── Demo data ─────────────────────────────────────────────────────────────────
function demoData() {
  return {
    municipality: "Stainz",
    agents: [
      {id:4,   group:1,income:3, age:1959,building_type:"1",build_age:4, energy_std:"3",subsidy:1,info_pas:1,state:"ADOPTED"},
      {id:16,  group:1,income:2, age:1972,building_type:"1",build_age:1, energy_std:"6",subsidy:1,info_pas:1,state:"ADOPTED"},
      {id:28,  group:6,income:3, age:1972,building_type:"1",build_age:1, energy_std:"6",subsidy:1,info_pas:2,state:"UNAWARE"},
      {id:183, group:1,income:null,age:1953,building_type:"1",build_age:5,energy_std:"4",subsidy:1,info_pas:1,state:"ADOPTED"},
      {id:235, group:2,income:3, age:1968,building_type:"1",build_age:7, energy_std:"4",subsidy:1,info_pas:2,state:"ADOPTED"},
      {id:238, group:2,income:5, age:1961,building_type:"1",build_age:7, energy_std:"4",subsidy:1,info_pas:2,state:"ADOPTED"},
      {id:262, group:6,income:3, age:1981,building_type:"1",build_age:9, energy_std:"2",subsidy:1,info_pas:2,state:"UNAWARE"},
      {id:342, group:6,income:2, age:1955,building_type:"1",build_age:4, energy_std:"4",subsidy:null,info_pas:null,state:"UNAWARE"},
      {id:401, group:6,income:1, age:1957,building_type:"1",build_age:6, energy_std:"6",subsidy:null,info_pas:null,state:"UNAWARE"},
      {id:406, group:5,income:3, age:1987,building_type:"1",build_age:9, energy_std:"4",subsidy:1,info_pas:3,state:"AWARE"},
      {id:411, group:6,income:2, age:1985,building_type:"1",build_age:6, energy_std:"6",subsidy:0,info_pas:1,state:"UNAWARE"},
      {id:431, group:1,income:4, age:1946,building_type:"1",build_age:6, energy_std:"4",subsidy:1,info_pas:2,state:"ADOPTED"},
      {id:700, group:1,income:2, age:1951,building_type:"1",build_age:1, energy_std:"6",subsidy:1,info_pas:2,state:"ADOPTED"},
      {id:718, group:1,income:null,age:1963,building_type:"1",build_age:7,energy_std:"3",subsidy:1,info_pas:3,state:"ADOPTED"},
      {id:760, group:2,income:4, age:1970,building_type:"1",build_age:3, energy_std:"5",subsidy:0,info_pas:1,state:"ADOPTED"},
      {id:942, group:1,income:3, age:1957,building_type:"1",build_age:4, energy_std:"5",subsidy:1,info_pas:1,state:"ADOPTED"},
      {id:944, group:6,income:3, age:1976,building_type:"1",build_age:9, energy_std:"3",subsidy:null,info_pas:null,state:"UNAWARE"},
      {id:1058,group:2,income:5, age:1988,building_type:"1",build_age:9, energy_std:"2",subsidy:1,info_pas:2,state:"ADOPTED"},
      {id:1273,group:4,income:null,age:null,building_type:"1",build_age:1,energy_std:"4",subsidy:0,info_pas:3,state:"AWARE"},
      {id:1343,group:1,income:3, age:1966,building_type:"2",build_age:7, energy_std:"6",subsidy:0,info_pas:0,state:"ADOPTED"},
    ],
    edges: [
      {source:4,  target:16,  weight:0.905},{source:4,  target:28,  weight:0.756},
      {source:4,  target:235, weight:0.912},{source:4,  target:238, weight:0.922},
      {source:4,  target:942, weight:0.997},{source:4,  target:431, weight:0.905},
      {source:4,  target:700, weight:0.913},{source:4,  target:718, weight:0.882},
      {source:4,  target:183, weight:0.879},{source:4,  target:760, weight:0.908},
      {source:16, target:700, weight:0.969},{source:16, target:235, weight:0.919},
      {source:16, target:238, weight:0.908},{source:16, target:760, weight:0.922},
      {source:16, target:942, weight:0.902},{source:16, target:431, weight:0.886},
      {source:235,target:238, weight:0.989},{source:235,target:760, weight:0.922},
      {source:235,target:718, weight:0.955},{source:238,target:760, weight:0.911},
      {source:238,target:718, weight:0.960},{source:942,target:431, weight:0.908},
      {source:942,target:235, weight:0.909},{source:942,target:700, weight:0.916},
      {source:700,target:238, weight:0.910},{source:718,target:700, weight:0.869},
      {source:1058,target:406,weight:0.908},{source:1058,target:235,weight:0.895},
      {source:1058,target:942,weight:0.878},{source:262,target:406, weight:0.751},
      {source:28, target:700, weight:0.818},{source:411,target:431, weight:0.791},
      {source:401,target:431, weight:0.833},{source:342,target:235, weight:0.755},
      {source:1343,target:235,weight:0.922},{source:1343,target:718,weight:0.883},
      {source:1273,target:16, weight:0.850},{source:1273,target:235,weight:0.775},
      {source:406,target:28,  weight:0.663},{source:944,target:262, weight:0.693},
    ],
    steps: [
      {step:0,adopted_count:13,total_agents:20,adopted_rate:0.65,state_distribution:{ADOPTED:13,UNAWARE:6,AWARE:1}},
      {step:1,adopted_count:14,total_agents:20,adopted_rate:0.70,state_distribution:{ADOPTED:14,UNAWARE:6}},
      {step:2,adopted_count:14,total_agents:20,adopted_rate:0.70,state_distribution:{ADOPTED:14,UNAWARE:6}},
      {step:3,adopted_count:14,total_agents:20,adopted_rate:0.70,state_distribution:{ADOPTED:14,UNAWARE:6}},
      {step:4,adopted_count:14,total_agents:20,adopted_rate:0.70,state_distribution:{ADOPTED:14,UNAWARE:6}},
      {step:5,adopted_count:14,total_agents:20,adopted_rate:0.70,state_distribution:{ADOPTED:14,UNAWARE:5,AWARE:1}},
      {step:6,adopted_count:15,total_agents:20,adopted_rate:0.75,state_distribution:{ADOPTED:15,UNAWARE:5}},
      {step:7,adopted_count:15,total_agents:20,adopted_rate:0.75,state_distribution:{ADOPTED:15,UNAWARE:5}},
      {step:8,adopted_count:15,total_agents:20,adopted_rate:0.75,state_distribution:{ADOPTED:15,UNAWARE:3,AWARE:2}},
      {step:9,adopted_count:16,total_agents:20,adopted_rate:0.80,state_distribution:{ADOPTED:16,UNAWARE:3,AWARE:1}},
    ]
  };
}

// ── Init ──────────────────────────────────────────────────────────────────────
window.addEventListener('load', () => {
  apiData = demoData();
  renderGraph();
});