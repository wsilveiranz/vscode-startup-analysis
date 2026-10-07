#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

def num(v):
    v=v.strip().replace(',','')
    return None if v in ('','-') else int(float(v))

def parse(path, label):
    text=Path(path).read_text(encoding='utf-8-sig', errors='replace')
    result={'label':label,'source':Path(path).name,'system':{},'core':{},'extensions':[],'raw_ext_host_loads':[]}
    for key in ['Code','OS','CPUs','Memory(System)','Memory(Process)','Initial Startup','Empty Workspace']:
        m=re.search(r'^\\?\*\s*'+re.escape(key)+r':\s*(.+)$',text,re.M)
        if m: result['system'][key]=m.group(1).strip()
    core_names=['workbench ready','renderer ready','extensions registered','register extensions & spawn extension host','overall workbench load']
    for line in text.splitlines():
        cells=[c.strip().replace('\\','') for c in line.strip().strip('|').split('|')]
        if len(cells)>=2 and cells[0] in core_names:
            try: result['core'][cells[0]]=num(cells[1])
            except: pass
    in_stats=False
    for line in text.splitlines():
        if '## Extension Activation Stats' in line: in_stats=True; continue
        if in_stats and line.startswith('## '): break
        if not in_stats or '|' not in line: continue
        cells=[c.strip().replace('\\','') for c in line.strip().strip('|').split('|')]
        if len(cells)<7 or cells[0] in ('Extension','---') or set(cells[0])=={'-'}: continue
        try:
            result['extensions'].append({'extension':cells[0],'eager':cells[1].lower()=='true','load_code_ms':num(cells[2]),'call_activate_ms':num(cells[3]),'finish_activate_ms':num(cells[4]),'event':cells[5],'by':cells[6]})
        except: continue
    starts={}
    for m in re.finditer(r'^code/extHost/(will|did)LoadExtensionCode/([^\t\r\n]+)\t([0-9.]+)', text, re.M):
        kind,ext,ts=m.group(1),m.group(2),float(m.group(3))
        if kind=='will': starts[ext]=ts
        elif ext in starts: result['raw_ext_host_loads'].append({'extension':ext,'duration_ms':round(ts-starts[ext],3)})
    result['extensions'].sort(key=lambda x:(x['load_code_ms'] or 0), reverse=True)
    result['raw_ext_host_loads'].sort(key=lambda x:x['duration_ms'], reverse=True)
    return result

ap=argparse.ArgumentParser()
ap.add_argument('report')
ap.add_argument('--label',default='capture')
ap.add_argument('--output',required=True)
a=ap.parse_args()
out=parse(a.report,a.label)
Path(a.output).write_text(json.dumps(out,indent=2),encoding='utf-8')
print(a.output)
