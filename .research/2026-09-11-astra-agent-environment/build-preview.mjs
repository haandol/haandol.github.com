import fs from 'node:fs';
import path from 'node:path';
import { marked } from '/Users/dongkyl/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';

const root = '/Users/dongkyl/git/haandol.github.com';
const target = path.join(root, '_drafts/2026-09-11-astra-agent-tools-and-environment.md');
const out = path.join(root, '.research/2026-09-11-astra-agent-environment/preview.html');
const input = fs.readFileSync(target, 'utf8');
const [, front, original] = input.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
const title = front.match(/^title: "(.*)"$/m)[1];
const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const notes = [];
let body = original.replace(/^\[\^(\d+)\]: (.+)$/gm, (_, id, text) => {
  notes.push({ id, text });
  return '';
});
body = body.replace(/^{% (?:end)?raw %}\n/gm, '');
body = body.replace(/```mermaid\n([\s\S]*?)\n```/g, (_, source) =>
  `<figure class="diagram"><div class="mermaid">${escape(source)}</div><details><summary>도식 원문</summary><pre>${escape(source)}</pre></details></figure>`);
const refs = {};
body = body.replace(/\[\^(\d+)\]/g, (_, id) => {
  refs[id] = (refs[id] || 0) + 1;
  return `<sup id="fnref-${id}-${refs[id]}"><a href="#fn-${id}" aria-label="출처 ${id}">${id}</a></sup>`;
});
let rendered = marked.parse(body);
rendered = rendered.replace(/href="(\/20[^"]+)"/g, 'href="https://haandol.github.io$1"');
const footnotes = notes.map(({ id, text }) => {
  const html = marked.parseInline(text).replace(/href="(\/20[^"]+)"/g, 'href="https://haandol.github.io$1"');
  return `<li id="fn-${id}">${html} <a href="#fnref-${id}-1" aria-label="본문으로 돌아가기">↩</a></li>`;
}).join('\n');
fs.writeFileSync(out, `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escape(title)}</title>
<style>
:root{color-scheme:light;--ink:#222b32;--muted:#687179;--line:#dce2e6;--accent:#225d68}
*{box-sizing:border-box}
body{margin:0;background:#fbfaf7;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
main{max-width:800px;margin:0 auto;padding:64px 32px 80px}
header{padding-bottom:36px;border-bottom:1px solid var(--line);margin-bottom:40px}
.meta{font-size:14px;color:var(--muted);letter-spacing:.04em}
h1{font-size:36px;line-height:1.45;letter-spacing:-.045em;word-break:keep-all;margin:16px 0}
.subtitle{font-size:16px;color:var(--muted)}
article{font-size:18px;line-height:1.95;word-break:keep-all;overflow-wrap:break-word}
h2{font-size:25px;line-height:1.5;letter-spacing:-.035em;margin:58px 0 22px;scroll-margin-top:24px}
p{margin:0 0 23px}
li{margin-bottom:9px}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
sup{font-size:12px;line-height:0;margin-left:2px}
sup a{text-decoration:none}
strong{font-weight:700}
hr{border:0;border-top:1px solid var(--line);margin:44px 0}
.diagram{margin:30px 0;padding:22px 18px;background:#fff;border:1px solid var(--line);border-radius:12px}
.mermaid{display:flex;justify-content:center;min-width:0}
.mermaid svg{max-width:100%;height:auto}
details{border-top:1px solid var(--line);margin-top:18px;padding-top:12px;font-size:13px;color:var(--muted)}
summary{cursor:pointer}
pre{font:12px/1.65 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
.footnotes{font-size:14px;line-height:1.8;word-break:normal;overflow-wrap:anywhere}
.footnotes h2{font-size:19px}
.footnotes li{padding-left:4px;margin-bottom:14px}
@media(max-width:600px){main{padding:32px 22px 56px}h1{font-size:29px}article{font-size:17px;line-height:1.9}h2{font-size:23px;margin-top:42px}.diagram{padding:16px 8px}}
</style>
</head>
<body><main>
<header><div class="meta">HAANDOL · 2026.09.11 · 미발행 초안</div>
<h1>${escape(title)}</h1>
<div class="subtitle">Giving agents the tools to finish the whole job</div></header>
<article>${rendered}</article>
<section class="footnotes" aria-label="출처"><h2>출처</h2><ol>${footnotes}</ol></section>
</main>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:false,theme:'base',themeVariables:{fontFamily:'-apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, sans-serif',fontSize:'16px',primaryColor:'#edf4f5',primaryTextColor:'#22343a',primaryBorderColor:'#8eaaaf',lineColor:'#647f84',secondaryColor:'#f3f1e9',tertiaryColor:'#ffffff'},flowchart:{htmlLabels:true,curve:'linear',nodeSpacing:28,rankSpacing:34}});
try { await mermaid.run({querySelector:'.mermaid'}); document.documentElement.dataset.diagram='ready'; }
catch(error) { document.documentElement.dataset.diagram='error'; console.error(error); }
</script>
</body></html>`);
console.log(out);
