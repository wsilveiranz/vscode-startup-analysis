#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('baseline'); ap.add_argument('customer'); ap.add_argument('--output',required=True); a=ap.parse_args()
b=json.loads(Path(a.baseline).read_text()); c=json.loads(Path(a.customer).read_text())
bm={x['extension']:x for x in b['extensions']}; cm={x['extension']:x for x in c['extensions']}
ids=sorted(set(bm)|set(cm),key=lambda e:(cm.get(e,{}).get('load_code_ms') or 0),reverse=True)
lines=['# VS Code startup comparison','',f"Baseline: `{b['label']}`  ",f"Customer: `{c['label']}`",'', '| Extension | Baseline load code | Customer load code | Ratio |','|---|---:|---:|---:|']
for e in ids:
    bv=bm.get(e,{}).get('load_code_ms'); cv=cm.get(e,{}).get('load_code_ms')
    ratio=f"{cv/bv:.2f}x" if bv and cv is not None else 'n/a'
    lines.append(f"| {e} | {bv if bv is not None else 'n/a'} ms | {cv if cv is not None else 'n/a'} ms | {ratio} |")
lines += ['','## Interpretation guardrails','', '- Verify VS Code and extension version comparability.', '- Treat ratios as observations, not root-cause proof.', '- Use controlled tests and profiles to validate the critical path.']
Path(a.output).write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(a.output)
