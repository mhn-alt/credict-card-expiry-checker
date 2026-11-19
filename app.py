import os
import re
import shutil
from datetime import datetime

import cv2
import numpy as np
import pytesseract
import streamlit as st
from pytesseract import Output

st.set_page_config(page_title="Card Expiry Checker", page_icon="💳", layout="centered", initial_sidebar_state="collapsed")

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;800&display=swap');

html, body, [class*="css"], .stApp { font-family:'Sora', sans-serif; }
.stApp {
  background:
    radial-gradient(900px 500px at 85% -10%, rgba(99,102,241,.28), transparent 60%),
    radial-gradient(700px 500px at -10% 40%, rgba(20,184,166,.18), transparent 60%),
    #0B1020;
  color:#E6EAF5;
}
#MainMenu, footer, header {visibility:hidden;}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none;}

/* slow drifting glow behind everything */
.stApp::before, .stApp::after { content:""; position:fixed; z-index:0; pointer-events:none;
  width:520px; height:520px; border-radius:50%; filter:blur(90px); opacity:.35; }
.stApp::before { background:#6366F1; top:-160px; right:-120px; animation:drift1 18s ease-in-out infinite alternate; }
.stApp::after  { background:#14B8A6; bottom:-200px; left:-140px; animation:drift2 22s ease-in-out infinite alternate; }
@keyframes drift1 { to { transform:translate(-90px,70px) scale(1.15); } }
@keyframes drift2 { to { transform:translate(110px,-60px) scale(1.2); } }
@media (prefers-reduced-motion: reduce) { .stApp::before, .stApp::after { animation:none; } }
.main .block-container { position:relative; z-index:1; max-width:860px; }

.chip { display:inline-flex; align-items:center; gap:10px; padding:10px 18px; border-radius:16px;
        background:linear-gradient(135deg,rgba(99,102,241,.35),rgba(20,184,166,.25));
        border:1px solid rgba(255,255,255,.15); font-size:1.6rem; margin-bottom:14px;
        box-shadow:0 10px 30px -10px rgba(99,102,241,.6); }
.chip i { display:block; width:34px; height:6px; border-radius:3px; background:rgba(255,255,255,.55); }
[data-testid="stSidebar"] { background:#0F1630; border-right:1px solid rgba(255,255,255,.06); }
[data-testid="stSidebar"] * { color:#C9D1E8 !important; }
label, .stMarkdown, p { color:#C9D1E8; }

.hero { text-align:center; padding:28px 0 10px 0; }
.hero h1 { font-size:2.9rem; font-weight:800; margin:0; letter-spacing:-.03em;
           background:linear-gradient(90deg,#fff,#A5B4FC 60%,#5EEAD4);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { color:#8B96B8; margin-top:8px; font-weight:300; font-size:1.05rem; }

[data-testid="stFileUploaderDropzone"] {
  background:rgba(255,255,255,.04); border:1.5px dashed rgba(165,180,252,.45);
  border-radius:20px; padding:30px; transition:all .2s;
}
[data-testid="stFileUploaderDropzone"]:hover { background:rgba(165,180,252,.09); border-color:#A5B4FC; }
[data-testid="stFileUploaderDropzone"] * { color:#C9D1E8 !important; }
[data-testid="stFileUploaderDropzone"] button { background:#6366F1; color:#fff !important; border:0; border-radius:10px; }

@keyframes rise { from {opacity:0; transform:translateY(12px);} to {opacity:1; transform:none;} }
.result { animation:rise .5s ease-out; border-radius:22px; padding:26px 28px; margin-top:6px;
          background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.09);
          backdrop-filter:blur(8px); }
.result.green { box-shadow:0 0 40px -8px rgba(52,211,153,.45); }
.result.amber { box-shadow:0 0 40px -8px rgba(251,191,36,.45); }
.result.red   { box-shadow:0 0 40px -8px rgba(248,113,113,.5); }
.result.grey  { box-shadow:none; }
.badge { width:54px; height:54px; border-radius:50%; display:flex; align-items:center; justify-content:center;
         font-size:1.6rem; font-weight:800; margin-bottom:14px; border:2px solid currentColor; }
.green .badge{color:#34D399; background:rgba(52,211,153,.12)}
.red .badge{color:#F87171; background:rgba(248,113,113,.12)}
.grey .badge{color:#94A3B8; background:rgba(148,163,184,.12)}
.status { font-size:2.3rem; font-weight:800; letter-spacing:-.02em; line-height:1.1; }
.green .status{color:#34D399} .amber .status{color:#FBBF24}
.red .status{color:#F87171} .grey .status{color:#94A3B8}
.label { color:#8B96B8; font-size:.85rem; margin-top:18px; }
.date { font-size:2.4rem; font-weight:600; color:#fff; letter-spacing:.04em; }
.stImage img { border-radius:18px; border:1px solid rgba(255,255,255,.1); box-shadow:0 18px 40px -18px rgba(0,0,0,.8); }
.note { color:#8B96B8; font-size:.95rem; margin-top:2px; }
.fname { color:#8B96B8; font-size:.8rem; margin:14px 0 6px 4px; }

/* ---------- animations (visual only, no layout changes) ---------- */
.hero h1 { background-size:200% auto; animation:shimmer 6s linear infinite; }
@keyframes shimmer { to { background-position:200% center; } }

.chip { animation:floaty 4s ease-in-out infinite; }
@keyframes floaty { 50% { transform:translateY(-6px); } }

[data-testid="stFileUploaderDropzone"] { animation:borderpulse 3s ease-in-out infinite; }
@keyframes borderpulse {
  0%,100% { box-shadow:0 0 0 0 rgba(165,180,252,0); }
  50%     { box-shadow:0 0 28px -6px rgba(165,180,252,.45); }
}

.badge { animation:pop .6s cubic-bezier(.2,1.4,.4,1) .15s both; }
@keyframes pop { from { transform:scale(0); opacity:0; } to { transform:scale(1); opacity:1; } }

.result.green { animation:rise .5s ease-out, glowg 3.5s ease-in-out .6s infinite; }
.result.red   { animation:rise .5s ease-out, glowr 3.5s ease-in-out .6s infinite; }
@keyframes glowg { 50% { box-shadow:0 0 56px -6px rgba(52,211,153,.6); } }
@keyframes glowr { 50% { box-shadow:0 0 56px -6px rgba(248,113,113,.65); } }

.date, .status { animation:fadein .8s ease-out .25s both; }
@keyframes fadein { from { opacity:0; letter-spacing:.2em; } to { opacity:1; } }

/* one light sweep across the card image when it appears */
[data-testid="stImage"] { position:relative; overflow:hidden; border-radius:18px; }
[data-testid="stImage"]::after { content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(105deg, transparent 35%, rgba(255,255,255,.28) 50%, transparent 65%);
  transform:translateX(-120%); animation:sweep 1.4s ease-out .3s 1 forwards; }
@keyframes sweep { to { transform:translateX(120%); } }

@media (prefers-reduced-motion: reduce) {
  .hero h1, .chip, [data-testid="stFileUploaderDropzone"], .badge, .result, .date, .status,
  [data-testid="stImage"]::after { animation:none !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- OCR logic
DEFAULT_TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
DATE_RE = re.compile(r"(0[1-9]|1[0-2])\s*[/\-]\s*(\d{4}|\d{2})")
FIX = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1", "|": "1"})


def resolve_tesseract(path):
    return path if path and os.path.exists(path) else shutil.which("tesseract")


def ocr_lines(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scale = float(np.clip(1400 / gray.shape[1], 0.5, 3.0))
    big = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(big)
    _, otsu = cv2.threshold(big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lines = []
    for v in (big, clahe, otsu, cv2.bitwise_not(otsu)):
        for cfg in ("--psm 6", "--psm 11"):
            d = pytesseract.image_to_data(v, config=cfg, output_type=Output.DICT)
            grouped = {}
            for i, t in enumerate(d["text"]):
                t = t.strip()
                if not t or float(d["conf"][i]) < 0:
                    continue
                box = tuple(int(d[k][i] / scale) for k in ("left", "top", "width", "height"))
                key = (d["block_num"][i], d["par_num"][i], d["line_num"][i])
                grouped.setdefault(key, []).append((t, box))
            lines.extend(grouped.values())
    return lines


def union_box(chunk):
    x = min(b[0] for _, b in chunk)
    y = min(b[1] for _, b in chunk)
    xe = max(b[0] + b[2] for _, b in chunk)
    ye = max(b[1] + b[3] for _, b in chunk)
    return x, y, xe - x, ye - y


def find_expiry(lines):
    found = {}
    for line in lines:
        for n in (1, 2, 3):
            for i in range(len(line) - n + 1):
                chunk = line[i:i + n]
                txt = "".join(c[0] for c in chunk).translate(FIX).strip(".,;:")
                m = DATE_RE.fullmatch(txt)
                if not m:
                    continue
                yr = int(m.group(2))
                year = yr + 2000 if yr < 100 else yr
                if not 2000 <= year <= 2060:
                    continue
                e = found.setdefault((year, int(m.group(1))), {"count": 0, "box": union_box(chunk)})
                e["count"] += 1
    if not found:
        return None, None
    pool = [k for k, v in found.items() if v["count"] >= 2] or list(found)
    best = max(pool)  # latest date = expiry (ignores "valid from")
    return best, found[best]["box"]


@st.cache_data(show_spinner=False)
def analyze(file_bytes, tess_path):
    pytesseract.pytesseract.tesseract_cmd = tess_path
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None
    expiry, box = find_expiry(ocr_lines(img))
    return {"expiry": expiry, "box": box}


def months_left(expiry):
    t = datetime.today()
    return (expiry[0] - t.year) * 12 + expiry[1] - t.month


def status_for(expiry):
    if expiry is None:
        return "Date not found", "grey"
    if months_left(expiry) < 0:
        return "Expired", "red"
    return "Not expired", "green"


def annotate(img, box, color):
    out = img.copy()
    if box:
        bgr = {"green": (153, 211, 52), "amber": (36, 191, 251), "red": (113, 113, 248), "grey": (184, 163, 148)}[color]
        x, y, w, h = box
        cv2.rectangle(out, (x - 5, y - 5), (x + w + 5, y + h + 5), bgr, 3)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


tess_path = resolve_tesseract(DEFAULT_TESS)

# ---------------------------------------------------------------- page
st.markdown(
    """
<div class="hero">
  <div class="chip">💳<i></i></div>
  <h1>Card Expiry Checker</h1>
  <p>Upload a credit or debit card photo and see if it has expired.</p>
</div>
""",
    unsafe_allow_html=True,
)

if not tess_path:
    st.error("Tesseract OCR was not found. Install it from the UB Mannheim build, or update DEFAULT_TESS at the top of app.py.")
    st.stop()

files = st.file_uploader("Card images", type=["jpg", "jpeg", "png", "webp"],
                         accept_multiple_files=True, label_visibility="collapsed")
if not files:
    st.stop()

for idx, f in enumerate(files):
    data = f.getvalue()
    with st.spinner(f"Reading {f.name}..."):
        res = analyze(data, tess_path)

    st.markdown(f"<div class='fname'>{f.name}</div>", unsafe_allow_html=True)
    if res is None:
        st.warning("Could not open this image.")
        continue

    expiry, box = res["expiry"], res["box"]
    with st.expander("Wrong date? Correct it", expanded=False):
        manual = st.text_input("Expiry as MM/YY", key=f"m{idx}", placeholder="06/27")
    if manual.strip():
        m = DATE_RE.fullmatch(manual.strip())
        if m:
            yr = int(m.group(2))
            expiry, box = (yr + 2000 if yr < 100 else yr, int(m.group(1))), None

    status, color = status_for(expiry)
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    c1, c2 = st.columns([1.15, 1], gap="large")
    c1.image(annotate(img, box, color), use_container_width=True)

    if expiry:
        ml = months_left(expiry)
        when = ("expires this month" if ml == 0 else
                f"expired {abs(ml)} month{'s' if abs(ml) != 1 else ''} ago" if ml < 0 else
                f"{ml} month{'s' if ml != 1 else ''} left")
        date_html = f"<div class='label'>Expiry date</div><div class='date'>{expiry[1]:02d}/{expiry[0]}</div><div class='note'>{when}</div>"
    else:
        date_html = "<div class='note' style='margin-top:14px'>Try a sharper, straighter photo, or enter the date manually.</div>"

    icon = {"green": "✓", "red": "✕", "grey": "?"}[color]
    c2.markdown(f"<div class='result {color}'><div class='badge'>{icon}</div><div class='status'>{status}</div>{date_html}</div>",
                unsafe_allow_html=True)
