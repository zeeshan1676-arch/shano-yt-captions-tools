from flask import Flask, request, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

HTML = """
<h2>YouTube No Captions Finder ??</h2>
<input id="k" placeholder="Enter keyword">
<button onclick="s()">Search</button>
<div id="r"></div>

<script>
async function s(){
 let k=document.getElementById('k').value;
 let d=await fetch('/s?k='+k);
 let j=await d.json();
 let h='';
 j.forEach(v=>{
  h+=`<p><a target='_blank' href='https://youtube.com/watch?v=${v.id}'>${v.title}</a></p>`;
 });
 document.getElementById('r').innerHTML=h;
}
</script>
"""

@app.route('/')
def home():
    return HTML

@app.route('/s')
def s():
    k=request.args.get('k')
    out=[]
    with yt_dlp.YoutubeDL({'quiet':True}) as y:
        d=y.extract_info(f"ytsearch10:{k}",download=False)
        for e in d['entries']:
            try:
                i=y.extract_info(f"https://youtube.com/watch?v={e['id']}",download=False)
                if not i.get('subtitles'):
                    out.append({'id':e['id'],'title':e['title']})
            except:
                pass
    return jsonify(out)

import os
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
