#!/usr/bin/env python3
"""
build_site.py — generate the interactive site from the repo's docs and lessons.

Outputs:
  index.html        a self-contained single page with every doc + lesson (libs inlined,
                    works offline from file://). This is the main thing.
  pages/*.html      one standalone HTML page per doc/lesson, sharing the vendored libs.

Re-run after editing any doc:  python build_site.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent

# (id, nav label, group, kind, path, lang)
SECTIONS = [
    ("overview",   "Overview",                 "Guide",     "md",   "README.md",                  None),
    ("setup",      "Setup",                    "Guide",     "md",   "SETUP.md",                   None),
    ("walkthrough","Teaching Guide",           "Guide",     "md",   "WALKTHROUGH.md",             None),

    ("d1-01", "01 · Hello, LLM",               "Day 1",     "code", "day1/01_hello_llm.py",       "python"),
    ("d1-02", "02 · First Tool",               "Day 1",     "code", "day1/02_first_tool.py",      "python"),
    ("d1-03", "03 · The Agent Loop",           "Day 1",     "code", "day1/03_agent_loop.py",      "python"),

    ("d2-04", "04 · ReAct Agent",              "Day 2 — Patterns", "code", "day2/04_react_agent.py",     "python"),
    ("d2-05", "05 · Reflection",               "Day 2 — Patterns", "code", "day2/05_reflection.py",      "python"),
    ("d2-06", "06 · Framework (SDK)",          "Day 2 — Patterns", "code", "day2/06_framework_agent.py", "python"),

    ("ops-07",     "07 · Tracing",             "Day 2 — Ops", "code", "day2_ops/07_tracing.py",     "python"),
    ("ops-08",     "08 · Eval Harness",        "Day 2 — Ops", "code", "day2_ops/08_eval_harness.py","python"),
    ("ops-09",     "09 · Guardrails",          "Day 2 — Ops", "code", "day2_ops/09_guardrails.py",  "python"),
    ("ops-docker", "Dockerfile",               "Day 2 — Ops", "code", "day2_ops/Dockerfile",        "dockerfile"),
    ("ops-run",    "Running in Production",    "Day 2 — Ops", "md",   "day2_ops/run.md",            None),

    ("capstone",   "Capstone",                 "Capstone",  "md",   "capstone/README.md",         None),

    ("glossary",   "Glossary",                 "Reference", "md",   "glossary.md",                None),
    ("resources",  "Resources",                "Reference", "md",   "resources.md",               None),
    ("career",     "Career Roadmap",           "Reference", "md",   "CAREER.md",                  None),
    ("style",      "Writing Style",            "Reference", "md",   "STYLE.md",                   None),
]

manifest = []
embeds = []
for sid, label, group, kind, path, lang in SECTIONS:
    raw = (ROOT / path).read_text(encoding="utf-8")
    assert "</script" not in raw.lower(), f"{path} contains </script — would break embedding"
    embeds.append(f'<script type="text/plain" id="src-{sid}">{raw}</script>')
    # A code section may have a prose walkthrough at lessons/<id>.md. If so, the site
    # renders the walkthrough first and collapses the source beneath it.
    lesson_path = ROOT / "lessons" / f"{sid}.md"
    has_lesson = kind == "code" and lesson_path.exists()
    if has_lesson:
        lraw = lesson_path.read_text(encoding="utf-8")
        assert "</script" not in lraw.lower(), f"{lesson_path} contains </script"
        embeds.append(f'<script type="text/plain" id="lesson-{sid}">{lraw}</script>')
    manifest.append({"id": sid, "label": label, "group": group, "kind": kind,
                     "path": path, "dir": str(Path(path).parent).replace(".", ""),
                     "lang": lang or "plaintext", "lesson": has_lesson})

EMBEDS = "\n".join(embeds)
MANIFEST = json.dumps(manifest, separators=(",", ":"))

# Vendored libraries
MARKED_JS  = (ROOT / "vendor/marked.min.js").read_text(encoding="utf-8")
HLJS_JS    = (ROOT / "vendor/hljs.min.js").read_text(encoding="utf-8")
HLJS_DARK  = (ROOT / "vendor/hljs-dark.css").read_text(encoding="utf-8")
HLJS_LIGHT = (ROOT / "vendor/hljs-light.css").read_text(encoding="utf-8")
for blob, name in [(MARKED_JS, "marked.min.js"), (HLJS_JS, "hljs.min.js")]:
    assert "</script" not in blob.lower(), f"{name} contains </script"

CSS = r"""
:root{
  --bg:#0d1117; --panel:#11161d; --panel-2:#161c25; --border:#222b36;
  --text:#d7dee8; --muted:#8b97a7; --heading:#f0f4f9;
  --accent:#5eead8; --accent-2:#7c9bff; --accent-soft:rgba(94,234,216,.12);
  --code-bg:#0b0f15; --shadow:0 10px 30px rgba(0,0,0,.35);
}
html[data-theme="light"]{
  --bg:#f6f8fb; --panel:#ffffff; --panel-2:#f0f3f8; --border:#e1e7ef;
  --text:#283340; --muted:#5d6b7d; --heading:#0f1722;
  --accent:#0d9488; --accent-2:#3b5bdb; --accent-soft:rgba(13,148,136,.10);
  --code-bg:#f3f5f9; --shadow:0 10px 28px rgba(20,40,80,.10);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
  font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
code,pre,kbd{font-family:"SF Mono",SFMono-Regular,ui-monospace,Menlo,Consolas,monospace}
#progress-top{position:fixed;top:0;left:0;height:3px;width:0;z-index:60;
  background:linear-gradient(90deg,var(--accent),var(--accent-2));transition:width .1s linear}
header{position:fixed;top:0;left:0;right:0;height:58px;z-index:50;display:flex;align-items:center;gap:14px;
  padding:0 18px;background:color-mix(in srgb,var(--panel) 88%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
header .brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--heading)}
header .brand .dot{width:11px;height:11px;border-radius:50%;background:var(--accent);box-shadow:0 0 12px var(--accent)}
header .spacer{flex:1}
header .meta{color:var(--muted);font-size:13px}
.iconbtn{cursor:pointer;border:1px solid var(--border);background:var(--panel-2);color:var(--text);
  border-radius:9px;height:34px;min-width:34px;padding:0 10px;display:inline-flex;align-items:center;gap:7px;font-size:13px}
.iconbtn:hover{border-color:var(--accent);color:var(--heading)}
#menu-btn{display:none}
.ring{display:flex;align-items:center;gap:8px}
.ring svg{transform:rotate(-90deg)}
.ring .bg{stroke:var(--border)}
.ring .fg{stroke:var(--accent);stroke-linecap:round;transition:stroke-dashoffset .4s ease}
.ring .pct{font-size:12px;color:var(--muted);min-width:34px;text-align:right}
.layout{display:flex;padding-top:58px}
nav#side{position:fixed;top:58px;bottom:0;width:286px;overflow-y:auto;border-right:1px solid var(--border);
  background:var(--panel);padding:16px 10px 60px}
nav#side .search{width:100%;margin:0 0 12px;padding:9px 11px;border-radius:9px;border:1px solid var(--border);
  background:var(--panel-2);color:var(--text);font-size:13px}
nav#side .search:focus{outline:none;border-color:var(--accent)}
.navgroup{margin:14px 4px 4px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.navlink{display:flex;align-items:center;gap:9px;padding:7px 10px;border-radius:8px;color:var(--text);
  text-decoration:none;font-size:14px;cursor:pointer;border:1px solid transparent}
.navlink:hover{background:var(--panel-2)}
.navlink.active{background:var(--accent-soft);border-color:color-mix(in srgb,var(--accent) 40%,transparent);color:var(--heading);font-weight:600}
.navlink .chk{appearance:none;width:15px;height:15px;border:1.5px solid var(--border);border-radius:5px;cursor:pointer;flex:none;position:relative}
.navlink .chk:checked{background:var(--accent);border-color:var(--accent)}
.navlink .chk:checked::after{content:"";position:absolute;left:4px;top:1px;width:4px;height:8px;border:solid #04221e;border-width:0 2px 2px 0;transform:rotate(45deg)}
.navlink .lbl{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.navlink.kind-code .lbl::before{content:"›_ ";color:var(--accent);font-family:monospace}
main{margin-left:286px;flex:1;min-width:0;padding:34px 7vw 140px}
.doc-section{max-width:880px;margin:0 auto 56px;scroll-margin-top:78px}
.doc-section+.doc-section{border-top:1px solid var(--border);padding-top:46px}
.doc-section h1{font-size:31px;line-height:1.2;color:var(--heading);margin:.2em 0 .5em;letter-spacing:-.01em}
.doc-section h2{font-size:22px;color:var(--heading);margin:1.6em 0 .5em;padding-bottom:.3em;border-bottom:1px solid var(--border)}
.doc-section h3{font-size:17px;color:var(--heading);margin:1.4em 0 .4em}
.doc-section p{margin:.75em 0}
.doc-section a{color:var(--accent-2);text-decoration:none;border-bottom:1px solid transparent}
.doc-section a:hover{border-bottom-color:var(--accent-2)}
.doc-section blockquote{margin:1em 0;padding:.6em 1em;border-left:3px solid var(--accent);
  background:var(--accent-soft);border-radius:0 8px 8px 0}
.doc-section ul,.doc-section ol{padding-left:1.4em}
.doc-section li{margin:.3em 0}
.doc-section img{max-width:100%;height:auto;border-radius:14px;margin:1.2em 0;display:block;
  border:1px solid var(--border);box-shadow:var(--shadow)}
.doc-section img[src$=".svg"]{box-shadow:none;border:none;background:none}
.doc-section :not(pre)>code{background:var(--panel-2);border:1px solid var(--border);padding:.12em .42em;
  border-radius:6px;font-size:.88em;color:var(--accent)}
.doc-section table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:14px;display:block;overflow-x:auto}
.doc-section th,.doc-section td{border:1px solid var(--border);padding:9px 12px;text-align:left;vertical-align:top}
.doc-section th{background:var(--panel-2);color:var(--heading);font-weight:600}
.doc-section tr:nth-child(even) td{background:color-mix(in srgb,var(--panel-2) 50%,transparent)}
.doc-section hr{border:none;border-top:1px solid var(--border);margin:2em 0}
.code-path{margin:-.2em 0 1em;color:var(--muted);font-size:13px}
pre{position:relative;background:var(--code-bg)!important;border:1px solid var(--border);border-radius:12px;
  padding:16px;overflow:auto;margin:1.1em 0;box-shadow:var(--shadow)}
pre code{background:none!important;padding:0;font-size:13.5px;line-height:1.6}
.copy-btn{position:absolute;top:9px;right:9px;border:1px solid var(--border);background:var(--panel);
  color:var(--muted);border-radius:7px;padding:4px 9px;font-size:11.5px;cursor:pointer;opacity:0;transition:.15s}
pre:hover .copy-btn{opacity:1}
.copy-btn:hover{color:var(--heading);border-color:var(--accent)}
.copy-btn.done{color:var(--accent);border-color:var(--accent)}
details.codewrap{margin:1.1em 0}
details.codewrap>summary{cursor:pointer;color:var(--accent-2);font-size:13px;margin-bottom:6px;list-style:none}
details.codewrap>summary::-webkit-details-marker{display:none}
details.codewrap>summary::before{content:"▸ "}
details.codewrap[open]>summary::before{content:"▾ "}
#top-btn{position:fixed;right:22px;bottom:22px;z-index:40;width:44px;height:44px;border-radius:50%;
  border:1px solid var(--border);background:var(--panel);color:var(--text);cursor:pointer;font-size:18px;
  box-shadow:var(--shadow);opacity:0;pointer-events:none;transition:.2s}
#top-btn.show{opacity:1;pointer-events:auto}
.pagenav{max-width:880px;margin:0 auto;display:flex;justify-content:space-between;gap:12px;padding-top:30px;border-top:1px solid var(--border)}
.pagenav a{color:var(--accent-2);text-decoration:none;font-size:14px;border:1px solid var(--border);border-radius:9px;padding:10px 14px;max-width:48%}
.pagenav a:hover{border-color:var(--accent)}
.pagenav .dir{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.1em}
@media(max-width:920px){
  #menu-btn{display:inline-flex}
  nav#side{transform:translateX(-100%);transition:transform .25s;z-index:45;width:80%;max-width:320px;box-shadow:var(--shadow)}
  body.nav-open nav#side{transform:none}
  main{margin-left:0;padding:24px 20px 120px}
  .scrim{display:none;position:fixed;inset:58px 0 0;background:rgba(0,0,0,.4);z-index:44}
  body.nav-open .scrim{display:block}
}
"""

# Shared JS helpers used by both single-page and per-doc pages.
SHARED_JS = r"""
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const LS_THEME="agentic.theme";
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
function normPath(dir,src){
  if(/^https?:|^#|^data:/.test(src)) return src;
  const parts=(dir?dir.split("/"):[]).concat(src.split("/")); const out=[];
  for(const p of parts){ if(p===""||p===".") continue; if(p==="..") out.pop(); else out.push(p); }
  return out.join("/");
}
// rewrite <img src> and inter-doc .md links inside a rendered section
function fixLinks(el, dir, mode, byBase){
  $$("img",el).forEach(img=>{
    const root=normPath(dir, img.getAttribute("src")||"");
    img.src = (mode==="page"?"../":"") + root;
    img.loading="lazy";
  });
  $$("a",el).forEach(a=>{
    let href=a.getAttribute("href")||"";
    if(/^https?:|^mailto:/.test(href)) { a.target="_blank"; a.rel="noopener"; return; }
    const hashOnly = href.startsWith("#");
    if(hashOnly) return;
    const m = href.replace(/#.*$/,"");
    const base = m.split("/").pop();
    const id = byBase[base];
    if(id){ a.setAttribute("href", mode==="single" ? "#sec-"+id : id+".html"); }
  });
}
function applyTheme(t){
  document.documentElement.dataset.theme=t;
  const tb=$("#theme-btn"); if(tb) tb.textContent = t==="dark"?"🌙":"☀️";
  const sd=$("#hljs-dark"), sl=$("#hljs-light");
  if(sd&&sd.sheet) sd.sheet.disabled = t!=="dark";
  if(sl&&sl.sheet) sl.sheet.disabled = t==="dark";
}
function initTheme(){
  applyTheme(localStorage.getItem(LS_THEME)||"dark");
  const tb=$("#theme-btn");
  if(tb) tb.addEventListener("click",()=>{
    const t=document.documentElement.dataset.theme==="dark"?"light":"dark";
    localStorage.setItem(LS_THEME,t); applyTheme(t);
  });
}
function addCopyButtons(scope=document){
  $$("pre",scope).forEach(pre=>{
    if(pre.querySelector(".copy-btn")) return;
    const b=document.createElement("button"); b.className="copy-btn"; b.textContent="Copy";
    b.addEventListener("click",()=>{const c=pre.querySelector("code");
      navigator.clipboard.writeText(c?c.innerText:pre.innerText);
      b.textContent="Copied!"; b.classList.add("done");
      setTimeout(()=>{b.textContent="Copy"; b.classList.remove("done")},1400);});
    pre.appendChild(b);
  });
}
function renderCode(it, raw, lessonMd){
  var head, openAttr, summary;
  if(lessonMd && window.marked){
    head = marked.parse(lessonMd) + '<p class="code-path">Full source: <code>'+it.path+'</code></p>';
    openAttr = '';                                   // collapsed: read first, expand to see code
    summary = 'Show the full file';
  } else {
    head = '<h1>'+it.label+'</h1><p class="code-path"><code>'+it.path+'</code></p>';
    openAttr = ' open';
    summary = 'source';
  }
  return head +
    '<details class="codewrap"'+openAttr+'><summary>'+summary+'</summary>'+
    '<pre><code class="language-'+it.lang+'">'+esc(raw)+'</code></pre></details>';
}
"""

SINGLE_PAGE = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agentic Engineering — Weekend Intensive</title>
<style id="hljs-dark">__HLJS_DARK__</style>
<style id="hljs-light">__HLJS_LIGHT__</style>
<style>__CSS__</style>
</head>
<body>
<div id="progress-top"></div>
<header>
  <button class="iconbtn" id="menu-btn" title="Menu">☰</button>
  <div class="brand"><span class="dot"></span><span>Agentic Engineering</span></div>
  <span class="meta">· a weekend</span>
  <div class="spacer"></div>
  <div class="ring" title="Your progress">
    <svg width="30" height="30" viewBox="0 0 30 30">
      <circle class="bg" cx="15" cy="15" r="12" fill="none" stroke-width="3"></circle>
      <circle class="fg" id="ring-fg" cx="15" cy="15" r="12" fill="none" stroke-width="3"
              stroke-dasharray="75.4" stroke-dashoffset="75.4"></circle>
    </svg><span class="pct" id="ring-pct">0%</span>
  </div>
  <button class="iconbtn" id="reset-btn" title="Reset progress">Reset</button>
  <button class="iconbtn" id="theme-btn" title="Toggle theme">🌙</button>
</header>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <nav id="side"><input class="search" id="search" placeholder="Filter sections…" autocomplete="off"><div id="navlist"></div></nav>
  <main id="content"></main>
</div>
<button id="top-btn" title="Back to top">↑</button>
__EMBEDS__
<script>__MARKED__</script>
<script>__HLJS__</script>
<script>
const MANIFEST=__MANIFEST__;
__SHARED__
const LS_PROG="agentic.progress";
const raw=id=>{const e=document.getElementById("src-"+id);return e?e.textContent:"";};
const lessonMd=id=>{const e=document.getElementById("lesson-"+id);return e?e.textContent:null;};
const prog=()=>{try{return JSON.parse(localStorage.getItem(LS_PROG))||{}}catch(e){return{}}};
const saveProg=p=>localStorage.setItem(LS_PROG,JSON.stringify(p));
const byBase={}; MANIFEST.forEach(it=>byBase[it.path.split("/").pop()]=it.id);
if(window.marked) marked.setOptions({gfm:true});
function renderAll(){
  const c=$("#content");
  for(const it of MANIFEST){
    const sec=document.createElement("section"); sec.className="doc-section"; sec.id="sec-"+it.id;
    sec.innerHTML = it.kind==="md" ? (window.marked?marked.parse(raw(it.id)):"<pre>"+esc(raw(it.id))+"</pre>")
                                   : renderCode(it, raw(it.id), lessonMd(it.id));
    fixLinks(sec, it.dir, "single", byBase);
    c.appendChild(sec);
  }
  if(window.hljs) $$("pre code").forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
  addCopyButtons();
}
function buildNav(){
  const list=$("#navlist"); const p=prog(); let group="";
  for(const it of MANIFEST){
    if(it.group!==group){group=it.group;const g=document.createElement("div");g.className="navgroup";g.textContent=group;list.appendChild(g);}
    const a=document.createElement("a"); a.className="navlink kind-"+it.kind; a.href="#sec-"+it.id; a.dataset.id=it.id;
    a.innerHTML='<input class="chk" type="checkbox"'+(p[it.id]?" checked":"")+'><span class="lbl">'+it.label+'</span>';
    const chk=a.querySelector(".chk");
    chk.addEventListener("click",e=>e.stopPropagation());
    chk.addEventListener("change",()=>{const pp=prog();pp[it.id]=chk.checked;saveProg(pp);updateRing();});
    a.addEventListener("click",()=>{if(window.innerWidth<=920)document.body.classList.remove("nav-open");});
    list.appendChild(a);
  }
}
function updateRing(){
  const p=prog(); const done=MANIFEST.filter(it=>p[it.id]).length, total=MANIFEST.length, C=2*Math.PI*12;
  $("#ring-fg").style.strokeDashoffset=C*(1-done/total); $("#ring-pct").textContent=Math.round(done/total*100)+"%";
}
function spy(){
  const links=new Map($$(".navlink").map(a=>[a.dataset.id,a]));
  const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){
    links.forEach(a=>a.classList.remove("active"));
    const a=links.get(e.target.id.replace("sec-","")); if(a){a.classList.add("active");a.scrollIntoView({block:"nearest"});}
  }});},{rootMargin:"-64px 0px -70% 0px",threshold:0});
  $$(".doc-section").forEach(s=>obs.observe(s));
}
function chrome(){
  const bar=$("#progress-top"), top=$("#top-btn");
  addEventListener("scroll",()=>{const h=document.documentElement,max=h.scrollHeight-h.clientHeight;
    bar.style.width=(max>0?h.scrollTop/max*100:0)+"%"; top.classList.toggle("show",h.scrollTop>600);});
  top.addEventListener("click",()=>scrollTo({top:0,behavior:"smooth"}));
  $("#menu-btn").addEventListener("click",()=>document.body.classList.toggle("nav-open"));
  $("#scrim").addEventListener("click",()=>document.body.classList.remove("nav-open"));
  $("#search").addEventListener("input",e=>{const q=e.target.value.toLowerCase();
    $$(".navlink").forEach(a=>a.style.display=a.textContent.toLowerCase().includes(q)?"":"none");});
  $("#reset-btn").addEventListener("click",()=>{if(confirm("Reset your progress checkmarks?")){
    localStorage.removeItem(LS_PROG);$$(".chk").forEach(c=>c.checked=false);updateRing();}});
}
renderAll(); buildNav(); updateRing(); spy(); initTheme(); chrome();
</script>
</body>
</html>
"""

PAGE = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · Agentic Engineering</title>
<link id="hljs-dark" rel="stylesheet" href="../vendor/hljs-dark.css">
<link id="hljs-light" rel="stylesheet" href="../vendor/hljs-light.css" disabled>
<style>__CSS__</style>
</head>
<body>
<header>
  <button class="iconbtn" id="menu-btn" title="Menu">☰</button>
  <div class="brand"><span class="dot"></span><a href="../index.html" style="color:inherit;text-decoration:none">Agentic Engineering</a></div>
  <span class="meta">· __GROUP__</span>
  <div class="spacer"></div>
  <a class="iconbtn" href="../index.html" title="Single-page view">Single page</a>
  <button class="iconbtn" id="theme-btn" title="Toggle theme">🌙</button>
</header>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <nav id="side"><div id="navlist">__NAV__</div></nav>
  <main id="content"><section class="doc-section" id="thedoc"></section>
    <div class="pagenav">__PAGENAV__</div>
  </main>
</div>
<button id="top-btn" title="Back to top">↑</button>
<script type="text/plain" id="src-doc">__RAWDOC__</script>
<script type="text/plain" id="lesson-doc">__LESSONDOC__</script>
<script src="../vendor/marked.min.js"></script>
<script src="../vendor/hljs.min.js"></script>
<script>
const IT=__IT__, BYBASE=__BYBASE__;
__SHARED__
if(window.marked) marked.setOptions({gfm:true});
const sec=$("#thedoc");
const raw=document.getElementById("src-doc").textContent;
const lessonEl=document.getElementById("lesson-doc");
const lessonMd=(lessonEl && lessonEl.textContent.trim())?lessonEl.textContent:null;
sec.innerHTML = IT.kind==="md" ? (window.marked?marked.parse(raw):"<pre>"+esc(raw)+"</pre>") : renderCode(IT, raw, lessonMd);
fixLinks(sec, IT.dir, "page", BYBASE);
if(window.hljs) $$("pre code").forEach(b=>{try{hljs.highlightElement(b)}catch(e){}});
addCopyButtons(); initTheme();
$("#menu-btn").addEventListener("click",()=>document.body.classList.toggle("nav-open"));
$("#scrim").addEventListener("click",()=>document.body.classList.remove("nav-open"));
const topBtn=$("#top-btn");
addEventListener("scroll",()=>topBtn.classList.toggle("show",document.documentElement.scrollTop>600));
topBtn.addEventListener("click",()=>scrollTo({top:0,behavior:"smooth"}));
</script>
</body>
</html>
"""

bybase = {it["path"].split("/")[-1]: it["id"] for it in manifest}
BYBASE_JSON = json.dumps(bybase, separators=(",", ":"))

# --- single page ---
single = (SINGLE_PAGE
          .replace("__HLJS_DARK__", HLJS_DARK).replace("__HLJS_LIGHT__", HLJS_LIGHT)
          .replace("__CSS__", CSS).replace("__EMBEDS__", EMBEDS)
          .replace("__MARKED__", MARKED_JS).replace("__HLJS__", HLJS_JS)
          .replace("__MANIFEST__", MANIFEST).replace("__SHARED__", SHARED_JS))
(ROOT / "index.html").write_text(single, encoding="utf-8")

# --- per-doc pages ---
pages_dir = ROOT / "pages"
pages_dir.mkdir(exist_ok=True)
# shared sidebar nav (links to sibling pages)
nav_html = ""
group = None
for it in manifest:
    if it["group"] != group:
        group = it["group"]
        nav_html += f'<div class="navgroup">{group}</div>'
    cls = "navlink kind-" + it["kind"]
    nav_html += f'<a class="{cls}" href="{it["id"]}.html"><span class="lbl">{it["label"]}</span></a>'

for i, it in enumerate(manifest):
    raw = (ROOT / it["path"]).read_text(encoding="utf-8")
    lesson_md = ""
    if it.get("lesson"):
        lesson_md = (ROOT / "lessons" / f'{it["id"]}.md').read_text(encoding="utf-8")
    prev_a = (f'<a href="{manifest[i-1]["id"]}.html"><span class="dir">← previous</span>{manifest[i-1]["label"]}</a>'
              if i > 0 else "<span></span>")
    next_a = (f'<a href="{manifest[i+1]["id"]}.html" style="text-align:right"><span class="dir">next →</span>{manifest[i+1]["label"]}</a>'
              if i < len(manifest) - 1 else "<span></span>")
    page = (PAGE
            .replace("__TITLE__", it["label"]).replace("__GROUP__", it["group"])
            .replace("__CSS__", CSS).replace("__NAV__", nav_html)
            .replace("__PAGENAV__", prev_a + next_a)
            .replace("__RAWDOC__", raw)
            .replace("__LESSONDOC__", lesson_md)
            .replace("__IT__", json.dumps(it, separators=(",", ":")))
            .replace("__BYBASE__", BYBASE_JSON).replace("__SHARED__", SHARED_JS))
    (pages_dir / f'{it["id"]}.html').write_text(page, encoding="utf-8")

print(f"Wrote index.html ({len(single):,} bytes) + {len(manifest)} pages/ "
      f"(libs inlined in index; shared in pages; images + diagrams rendered).")
