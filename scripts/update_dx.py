#!/usr/bin/env python3
"""Refresh local expedition JSON from NG3K ADXO public calendar."""
import json, re, datetime, pathlib, urllib.request
from html.parser import HTMLParser
BASE=pathlib.Path(__file__).resolve().parents[1]
URL='https://www.ng3k.com/Misc/adxoc.html'
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None;self.table=0
 def handle_starttag(self,t,a):
  if t=='tr':self.row=[]
  elif t in ('td','th') and self.row is not None:self.cell=[]
 def handle_data(self,s):
  if self.cell is not None:self.cell.append(s)
 def handle_endtag(self,t):
  if t in ('td','th') and self.cell is not None and self.row is not None:self.row.append(' '.join(' '.join(self.cell).split()));self.cell=None
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None

def parse_date(s):
 m=re.search(r'(20\d{2})\s*([A-Za-z]{3})\s*(\d{1,2})',s)
 if not m:return None
 try:return datetime.datetime.strptime(' '.join(m.groups()),'%Y %b %d').date().isoformat()
 except ValueError:return None

def run():
 req=urllib.request.Request(URL,headers={'User-Agent':'DXClock/0.2 amateur radio calendar reader (GitHub Actions)'})
 with urllib.request.urlopen(req,timeout=35) as r:content=r.read().decode('utf-8','replace')
 p=Extract();p.feed(content)
 entries=[]
 for cells in p.rows:
  if len(cells)<4:continue
  # NG3K tables generally use Call | DXCC | Start | End | QSL | Source | Info
  opts=[(0,1,2,3),(3,2,0,1)]
  chosen=None
  for ci,ei,si,fi in opts:
   if max(ci,ei,si,fi)>=len(cells):continue
   start,end=parse_date(cells[si]),parse_date(cells[fi]);call=cells[ci].split()[0]
   if start and end and re.fullmatch(r'[A-Za-z0-9/\-]{2,22}',call):chosen=(call,cells[ei],start,end);break
  if not chosen:continue
  call,entity,start,end=chosen
  details=' '.join(cells[4:])
  modes=' / '.join(m for m in ('CW','SSB','FT8','FT4','RTTY') if re.search(r'\b'+m+r'\b',details,re.I))
  entries.append({'call':call.upper(),'entity':entity,'start':start,'end':end,'modes':modes or 'No especificado'})
 if len(entries)<8:raise RuntimeError(f'NG3K structure not understood: {len(entries)} entries; keeping previous data')
 uniq={ (x['call'],x['start'],x['end']):x for x in entries}
 data={'source':URL,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entries':list(uniq.values())}
 (BASE/'dxpeditions.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Updated',len(uniq),'expeditions')
if __name__=='__main__':run()
