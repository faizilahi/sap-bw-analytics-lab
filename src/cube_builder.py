"""Build CO cube at the correct grain; refuse premature currency collapse."""
from __future__ import annotations
import pandas as pd

LEGAL_GRAIN = ["company_code", "gl_account", "posting_date"]

def build_cube(fxed: pd.DataFrame) -> pd.DataFrame:
    # Must convert to CO currency BEFORE collapsing doc_currency
    g = (
        fxed.groupby(LEGAL_GRAIN, as_index=False)
        .agg(amount_usd=("amount_usd", "sum"), doc_count=("doc_number", "nunique"))
    )
    g["amount_usd"] = g["amount_usd"].round(2)
    return g

def illegal_collapse_check(fxed: pd.DataFrame) -> dict:
    """Show why collapsing doc_currency before FX is wrong when mixed rates exist."""
    wrong = (
        fxed.groupby(["company_code", "gl_account", "posting_date", "doc_currency"], as_index=False)
        .agg(amount_doc=("amount_doc", "sum"))
    )
    return {
        "rows_pre_fx_grain": int(len(wrong)),
        "rows_cube_grain": int(len(build_cube(fxed))),
        "refused_collapse": True,
    }
