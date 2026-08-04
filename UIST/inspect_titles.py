from pathlib import Path

import pypdf


ROOT = Path(r"D:\1Study\论文\CCF-A-Short-Paper\UIST")
DIRS = ["2021—UIST—Demo Session", "2022—UIST—Doctoral Symposium", "2021—UIST—Poster Session"]

files = []
for d in DIRS:
    files += sorted((ROOT / d).glob("*.pdf"))[:4]

for f in files:
    try:
        reader = pypdf.PdfReader(str(f))
        meta_title = (reader.metadata.title or "").strip()
        first = reader.pages[0].extract_text() or ""
        print("FILE:", f.name)
        print("META:", repr(meta_title[:200]))
        print("TEXT:", repr(first[:800]))
        print("---")
    except Exception as e:
        print("ERR", f.name, type(e).__name__, e)
