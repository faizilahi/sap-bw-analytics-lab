"""Synthetic FI documents + FX curve with a mid-month EUR shift."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(1015)

ACCOUNTS = [("400000", "COGS"), ("410000", "Revenue"), ("500000", "Opex"), ("160000", "AR")]

def main():
    fx = []
    for d in pd.date_range("2024-10-01", "2024-10-31", freq="D"):
        rate = 1.085 if d.day < 15 else 1.062
        fx.append({"rate_date": d.strftime("%Y-%m-%d"), "from_ccy": "EUR", "to_ccy": "USD", "rate": rate})
        fx.append({"rate_date": d.strftime("%Y-%m-%d"), "from_ccy": "USD", "to_ccy": "USD", "rate": 1.0})
    fx_df = pd.DataFrame(fx)

    docs = []
    doc_num = 100000
    # Plant exact DE01 EUR amounts so break is reproducible
    # Early month DE01 EUR doc total chosen so * (1.085-1.062) = 38441.70
    # => early EUR total = 38441.70 / 0.023 = 1,671,378.2609 ≈ 1671378.26
    early_eur_target = 1671378.26
    late_eur_target = 890000.00
    us_usd_target = 1200000.00

    def add_block(company, ccy, start, end, target, n):
        nonlocal doc_num
        days = pd.date_range(start, end, freq="D")
        raw = []
        for i in range(n):
            d = days[i % len(days)]
            acct, _ = ACCOUNTS[i % len(ACCOUNTS)]
            amt = float(RNG.uniform(500, 8000))
            raw.append((d, acct, amt))
        scale = target / sum(a for _, _, a in raw)
        for d, acct, amt in raw:
            doc_num += 1
            local = round(amt * scale, 2)
            docs.append({
                "doc_number": f"FI{doc_num}",
                "company_code": company,
                "gl_account": acct,
                "posting_date": d.strftime("%Y-%m-%d"),
                "doc_currency": ccy,
                "amount_doc": local,
                "local_currency": ccy,
                "amount_local": local,
            })

    add_block("DE01", "EUR", "2024-10-01", "2024-10-14", early_eur_target, 420)
    add_block("DE01", "EUR", "2024-10-15", "2024-10-31", late_eur_target, 380)
    add_block("US01", "USD", "2024-10-01", "2024-10-31", us_usd_target, 448)

    # fix penny on last of each block via regenerate totals check
    df = pd.DataFrame(docs)
    # Adjust last early DE01 row for exact early total
    early_mask = (df.company_code == "DE01") & (df.posting_date < "2024-10-15")
    drift = round(early_eur_target - df.loc[early_mask, "amount_doc"].sum(), 2)
    idx = df.loc[early_mask].index[-1]
    df.at[idx, "amount_doc"] = round(df.at[idx, "amount_doc"] + drift, 2)
    df.at[idx, "amount_local"] = df.at[idx, "amount_doc"]

    late_mask = (df.company_code == "DE01") & (df.posting_date >= "2024-10-15")
    drift = round(late_eur_target - df.loc[late_mask, "amount_doc"].sum(), 2)
    idx = df.loc[late_mask].index[-1]
    df.at[idx, "amount_doc"] = round(df.at[idx, "amount_doc"] + drift, 2)
    df.at[idx, "amount_local"] = df.at[idx, "amount_doc"]

    us_mask = df.company_code == "US01"
    drift = round(us_usd_target - df.loc[us_mask, "amount_doc"].sum(), 2)
    idx = df.loc[us_mask].index[-1]
    df.at[idx, "amount_doc"] = round(df.at[idx, "amount_doc"] + drift, 2)
    df.at[idx, "amount_local"] = df.at[idx, "amount_doc"]

    df.to_csv(DATA / "fi_documents.csv", index=False)
    fx_df.to_csv(DATA / "fx_rates.csv", index=False)
    pd.DataFrame([
        {"company_code": "US01", "controlling_area": "CA_US", "co_ccy": "USD"},
        {"company_code": "DE01", "controlling_area": "CA_US", "co_ccy": "USD"},
    ]).to_csv(DATA / "company_code.csv", index=False)
    print("FI docs", len(df), "early EUR", df.loc[early_mask, "amount_doc"].sum())

if __name__ == "__main__":
    main()
