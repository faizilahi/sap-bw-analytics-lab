import numpy as np, pandas as pd
from pathlib import Path
RNG = np.random.default_rng(19)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
cos = pd.DataFrame({"company_code":["1000","2000","3000"],"company_name":["North Am Ops","EU Ops","APAC Ops"],"currency":["USD","EUR","JPY"]})
fx = []
for d in pd.date_range("2024-01-01","2024-01-31",freq="D"):
  fx += [{"fx_date":d.date(),"currency":"USD","to_usd":1.0},
         {"fx_date":d.date(),"currency":"EUR","to_usd":round(float(RNG.uniform(1.05,1.12)),4)},
         {"fx_date":d.date(),"currency":"JPY","to_usd":round(float(RNG.uniform(0.0065,0.0072)),6)}]
rows=[]
accts=["400000","500000","600000"]
for i in range(800):
  c=cos.sample(1,random_state=int(RNG.integers(0,1e9))).iloc[0]
  d=pd.Timestamp("2024-01-01")+pd.Timedelta(days=int(RNG.integers(0,31)))
  rows.append({"doc_id":f"D{i+1:05d}","posting_date":d.date(),"company_code":c.company_code,
    "gl_account":RNG.choice(accts),"amount_lc":round(float(RNG.normal(5000,2000)),2),"currency":c.currency})
cos.to_csv(DATA/"infoobject_company.csv",index=False)
pd.DataFrame(fx).to_csv(DATA/"fx_rates.csv",index=False)
pd.DataFrame(rows).to_csv(DATA/"adso_fi_gl.csv",index=False)
print("Wrote SAP BW synthetic extracts")

