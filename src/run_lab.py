from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT/"data", ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
gl = pd.read_csv(DATA/"adso_fi_gl.csv", parse_dates=["posting_date"])
co = pd.read_csv(DATA/"infoobject_company.csv")
fx = pd.read_csv(DATA/"fx_rates.csv", parse_dates=["fx_date"])
gl["posting_date"]=pd.to_datetime(gl["posting_date"]); fx["fx_date"]=pd.to_datetime(fx["fx_date"])
m = gl.merge(co[["company_code","company_name"]], on="company_code")
m = m.merge(fx, left_on=["posting_date","currency"], right_on=["fx_date","currency"], how="left")
m["amount_usd"]=(m["amount_lc"]*m["to_usd"]).round(2)
summary = m.groupby(["company_code","company_name"], as_index=False).agg(amount_usd=("amount_usd","sum"), lines=("doc_id","count"))
summary.to_csv(OUT/"summary.csv", index=False)
pd.DataFrame([{"metric":"unmatched_fx","value":int(m["to_usd"].isna().sum())}]).to_csv(OUT/"control_totals.csv", index=False)
print(summary)

