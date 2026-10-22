"""Tiny web UI + JSON API.   python app.py  ->  http://127.0.0.1:5000
POST /predict  {"query": "..."}  ->  {"category":..., "confidence":..., "top":[...]}"""
from flask import Flask, request, jsonify, render_template_string
from predict import predict

app = Flask(__name__)
PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><title>Campus Query Classifier</title>
<style>body{font-family:system-ui;max-width:640px;margin:40px auto;padding:0 16px}input{width:100%;padding:12px;font-size:16px;box-sizing:border-box}
.bar{background:#e5e7eb;border-radius:4px;height:10px}.bar>div{background:#2563eb;height:10px;border-radius:4px}#out{margin-top:20px}</style>
<h2>Campus Query Classifier</h2><input id=q placeholder="e.g. when does the next college bus leave?" autofocus>
<div id=out></div>
<script>
const q=document.getElementById('q'),out=document.getElementById('out');
q.addEventListener('keydown',async e=>{if(e.key!=='Enter'||!q.value.trim())return;
 const r=await (await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query:q.value})})).json();
 out.innerHTML='<h3>'+r.category+' <small>('+(r.confidence*100).toFixed(0)+'% confident)</small></h3>'+
 r.top.map(t=>'<div>'+t.category+' '+(t.prob*100).toFixed(0)+'%</div><div class=bar><div style="width:'+t.prob*100+'%"></div></div>').join('');});
</script>"""

@app.get("/")
def index(): return render_template_string(PAGE)

@app.post("/predict")
def api():
    q = (request.get_json(silent=True) or {}).get("query", "").strip()
    if not q: return jsonify(error="send JSON like {\"query\": \"...\"}"), 400
    return jsonify(predict(q))

if __name__ == "__main__": app.run(port=5000)
