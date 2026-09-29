"""Apply posting-date vs period-end FX and quantify the break."""
from __future__ import annotations
import pandas as pd

def apply_fx(docs: pd.DataFrame, fx: pd.DataFrame, mode: str) -> pd.DataFrame:
    rates = fx.rename(columns={"rate_date": "posting_date", "from_ccy": "doc_currency"})
    if mode == "period_end":
        # use last rate in month per currency pair
        last = (
            fx.sort_values("rate_date")
            .groupby(["from_ccy", "to_ccy"], as_index=False)
            .tail(1)
            .rename(columns={"from_ccy": "doc_currency"})
        )
        merged = docs.merge(last[["doc_currency", "to_ccy", "rate"]], on="doc_currency", how="left")
    else:
        merged = docs.merge(
            rates[["posting_date", "doc_currency", "to_ccy", "rate"]],
            on=["posting_date", "doc_currency"],
            how="left",
        )
    merged["amount_usd"] = (merged["amount_doc"] * merged["rate"]).round(2)
    merged["fx_mode"] = mode
    return merged

def fx_break(posting: pd.DataFrame, period_end: pd.DataFrame) -> dict:
    a = round(float(posting["amount_usd"].sum()), 2)
    b = round(float(period_end["amount_usd"].sum()), 2)
    return {
        "posting_date_usd_total": a,
        "period_end_usd_total": b,
        "break_usd": round(a - b, 2),
    }
