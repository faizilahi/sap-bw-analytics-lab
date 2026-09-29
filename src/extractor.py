"""0FI_GL_14-style extractor into staging."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def extract(data_dir: Path) -> pd.DataFrame:
    docs = pd.read_csv(data_dir / "fi_documents.csv")
    cc = pd.read_csv(data_dir / "company_code.csv")
    out = docs.merge(cc, on="company_code", how="left")
    out["extractor"] = "0FI_GL_14_SIM"
    out["load_ts"] = "2024-11-01T02:15:00Z"
    return out

def extractor_controls(df: pd.DataFrame) -> dict:
    return {
        "document_count": int(len(df)),
        "company_codes": sorted(df["company_code"].unique().tolist()),
        "amount_doc_sum": round(float(df["amount_doc"].sum()), 2),
        "grain": "doc_number x gl_account x posting_date",
    }
