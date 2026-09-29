from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from extractor import extract, extractor_controls
from currency_shift import apply_fx, fx_break
from cube_builder import build_cube, illegal_collapse_check

DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    staged = extract(DATA)
    staged.to_csv(OUT / "staging_fi.csv", index=False)
    fx = pd.read_csv(DATA / "fx_rates.csv")
    posting = apply_fx(staged, fx, "posting_date")
    period = apply_fx(staged, fx, "period_end")
    br = fx_break(posting, period)
    cube = build_cube(posting)
    cube.to_csv(OUT / "cube_fico_usd.csv", index=False)
    grain = illegal_collapse_check(posting)
    pd.DataFrame([br | grain | extractor_controls(staged) | {"cube_rows": len(cube)}]).to_csv(
        OUT / "fx_break.csv", index=False
    )
    print(json.dumps(br | grain | {"cube_rows": len(cube)}, indent=2))

if __name__ == "__main__":
    main()
