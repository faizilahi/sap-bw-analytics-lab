# FI/CO Extract: Currency Shift Before the Cube

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A BW-style extract of FI documents into an analytic cube disagreed with Controlling
after a mid-month EUR→USD rate change. Company code `US01` posted in USD; `DE01`
posted in EUR. The extractor kept document currency; the cube expected controlling
area currency (USD) at the **posting-date** rate, not the **period-end** rate the
first load used.

## The extractor

`src/extractor.py` mimics 0FI_GL_14-style lines: document number, company code,
account, amount in doc currency, local currency, posting date. Seed data plants
**1,248** documents across October 2024.

## The currency shift

On `2024-10-15` the synthetic ECB-style rate moves from **1.085** to **1.062**
USD per EUR. Loading with period-end (1.062) understates USD COGS for early-month
DE01 postings by **$38,441.69** versus posting-date conversion.

## The cube grain

Grain is `(company_code, gl_account, posting_date, doc_currency)` before FX, then
`(company_code, gl_account, posting_date)` in controlling USD after FX. Collapsing
currency too early double-counts cross-rate docs — `src/cube_builder.py` refuses
that collapse and emits the break in `output/fx_break.csv`.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_bw_extract.py
```

Worked result: posting-date USD total **$3,958,625.54**, period-end USD total
**$3,920,183.85**, break **$38,441.69**, cube rows at correct grain **220**.
