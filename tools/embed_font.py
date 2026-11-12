# usage: embed_font.py file.html  -> (re)embeds a WenKai subset covering the file's characters
import sys,re,base64,subprocess
from fontTools.ttLib import TTFont
import os;FD=os.path.dirname(os.path.abspath(__file__))+'/'
P=sys.argv[1];s=open(P,encoding='utf-8').read()
s=re.sub(r'/\* 标签字体[^\n]*\n@font-face\{font-family:"LXGW WenKai"[^\n]*\n','',s)
chars=set(chr(c) for c in range(0x20,0x7f))|set(ch for ch in s if ord(ch)>0x7f)|set('0123456789%：；，。、（）“”…·—')
open(FD+'chars.txt','w',encoding='utf-8').write(''.join(sorted(chars)))
subprocess.run(['pyftsubset',FD+'LXGWWenKai-Medium.ttf','--text-file='+FD+'chars.txt','--flavor=woff2','--output-file='+FD+'wk-m.woff2','--layout-features=*','--no-hinting','--desubroutinize'],check=True)
b=open(FD+'wk-m.woff2','rb').read();cm=TTFont(FD+'wk-m.woff2').getBestCmap()
print(len(chars),'chars, woff2',len(b),'missing',''.join(c for c in sorted(chars) if ord(c)>0x7f and ord(c) not in cm))
face='/* 标签字体：霞鹜文楷 LXGW WenKai Medium（SIL OFL 1.1），只嵌入本页用到的字 */\n@font-face{font-family:"LXGW WenKai";font-weight:400 900;font-display:swap;src:url(data:font/woff2;base64,'+base64.b64encode(b).decode()+') format("woff2")}\n'
assert s.count('<style>\n')==1;s=s.replace('<style>\n','<style>\n'+face)
open(P,'w',encoding='utf-8').write(s)
