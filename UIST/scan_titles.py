import json
from pathlib import Path

import pypdf


ROOT = Path(r"D:\1Study\论文\CCF-A-Short-Paper\UIST")
OUT = ROOT / "titles_scan.json"

pdfs = sorted(ROOT.rglob("*.pdf"))
results = []

for pdf in pdfs:
    meta = ""
    text_preview = ""
    error = ""
    try:
        reader = pypdf.PdfReader(str(pdf))
        meta = (reader.metadata.title or "").strip()
        try:
            text_preview = (reader.pages[0].extract_text() or "")[:400]
        except Exception as e:
            text_preview = ""
            error = f"text: {type(e).__name__}: {e}"
    except Exception as e:
        error = f"pdf: {type(e).__name__}: {e}"
    results.append(
        {
            "path": str(pdf),
            "dir": pdf.parent.name,
            "old_name": pdf.name,
            "meta_title": meta,
            "text_preview": text_preview,
            "error": error,
        }
    )

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

no_meta = [r for r in results if not r["meta_title"]]
generic = [
    r
    for r in results
    if r["meta_title"]
    and r["meta_title"].lower() in {"untitled", "no title", "untitled document", "microsoft word - document"}
]
print(f"total={len(results)} no_meta={len(no_meta)} generic={len(generic)}")
for r in no_meta + generic:
    print(r["path"], "|", r["meta_title"], "|", r["error"])
