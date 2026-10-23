import base64
import re
import subprocess
import sys
import tempfile
import os

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

HTML = """<!doctype html><html><head><meta charset="utf-8"></head>
<body style="margin:0">
<img id="src" src="data:image/png;base64,__DATA__">
<pre id="out" style="white-space:pre-wrap;word-break:break-all;"></pre>
<script>
const img = document.getElementById('src');
function run() {{
  const c = document.createElement('canvas');
  c.width = img.naturalWidth;
  c.height = img.naturalHeight;
  const ctx = c.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const url = c.toDataURL('image/webp', __QUALITY__);
  document.getElementById('out').textContent = url;
  document.title = 'DONE';
}}
if (img.complete) run(); else img.onload = run;
</script>
</body></html>
"""

def convert(src_png, dst_webp, quality=0.85):
    with open(src_png, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    html = HTML.replace("__DATA__", b64).replace("__QUALITY__", str(quality))
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tf:
        tf.write(html.encode("utf-8"))
        html_path = tf.name
    dump_path = html_path + ".dump"
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--virtual-time-budget=4000",
            f"--dump-dom",
            f"file://{html_path}",
        ],
        stdout=open(dump_path, "w"),
        stderr=subprocess.DEVNULL,
        check=True,
    )
    with open(dump_path, "r") as f:
        dom = f.read()
    m = re.search(r'<pre id="out"[^>]*>(.*?)</pre>', dom, re.S)
    if not m or "data:image/webp;base64," not in m.group(1):
        raise RuntimeError(f"webp conversion failed for {src_png}; dom snippet: {dom[:500]}")
    data_url = m.group(1).strip()
    b64_payload = data_url.split("base64,", 1)[1]
    with open(dst_webp, "wb") as f:
        f.write(base64.b64decode(b64_payload))
    os.unlink(html_path)
    os.unlink(dump_path)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.85)
    print(f"wrote {sys.argv[2]}")
