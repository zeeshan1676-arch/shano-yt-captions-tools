from flask import Flask, request, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

HTML = """
<h2>YouTube No Captions Finder 🔍</h2>
<input id="k" placeholder="Enter keyword">
<button onclick="s()">Search</button>
<div id="r"></div>

<script>
async function s(){
 let k=document.getElementById('k').value;
 let d=await fetch('/s?k='+k);
 let j=await d.json();
 let h='';
 if(j.length==0){
   h = "<p>No results found ❌</p>";
 }
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
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as y:
        try:
            d = y.extract_info(f"ytsearch15:{k}", download=False)

            for e in d['entries']:
                try:
                    info = y.extract_info(f"https://youtube.com/watch?v={e['id']}", download=False)

                    # STRICT filter: no subtitles
                    if not info.get('subtitles') and not info.get('automatic_captions'):
                        out.append({
                            'id': e['id'],
                            'title': e['title']
                        })
                except:
                    continue
        except:
            pass

    return jsonify(out)

import os
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
