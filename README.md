# SAP BW/4HANA Analytics Lab (Synthetic Extracts)

**Author:** [Faiz Elahi](https://github.com/faizilahi) (`faizilahi`) · **Type:** EDUCATIONAL LAB · **Synthetic data only**

---

## Educational disclaimer

This is an **educational portfolio lab**. Datasets are **synthetic**. It does **not** claim employment at a customer, hospital, bank, SAP shop, or Oracle estate. No real PHI/PII. No live cloud spend. No API keys required.

---

## Problem statement

Analytics engineers inherit SAP BW extract files (aDSO/InfoCube-shaped) and must land them into a modern mart with clear InfoObject-like keys, currency, and company-code control totals.

**Domain focus:** Finance / industrial controlling

---

## Why this tool (SAP BW/4HANA-style InfoProvider extracts (local))

| Opaque BW dumps | Documented extract → mart pipeline |
|---|---|
| Mixed currencies | Explicit FX teaching table |
| No audit grain | Company-code control totals |

---

## Architecture

```mermaid
flowchart LR
  GEN[generate_synthetic_data.py]
  DATA[data/*.csv]
  RUN[run_lab.py]
  OUT[output/*.csv]
  CHART[generate_charts.py]
  IMG[docs/images/*.png]
  GEN --> DATA --> RUN --> OUT
  OUT --> CHART --> IMG
```

See [`docs/architecture.md`](docs/architecture.md).

---

## Dataset dictionary

| File | Grain | Notes |
|------|-------|-------|
| `adso_fi_gl.csv` | Doc line | Company code, account, amount LC |
| `infoobject_company.csv` | Company | Currency |
| `fx_rates.csv` | Day×currency | To USD teaching |
| `output/summary.csv` | Company | USD totals |

---

## Prerequisites

- Python 3.10+
- Packages in `requirements.txt`

---

## How to run

```powershell
cd "sap-bw/4hana-analytics-lab-"
python -m venv .venv
.\\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_lab.py
python scripts/generate_charts.py
```

Inspect `output/summary.csv` and `docs/images/primary_metric.png`.

---

## Local vs cloud (honest)

**No SAP BW/4HANA or Datasphere tenant.** CSV extracts mimic aDSO open-hub / flat-file interfaces. Transforms run in pandas. Do not claim live SAP connectivity.

---

## Results interpretation

Open `output/` CSVs and the PNGs under `docs/images/`. Numbers are synthetic teaching fixtures — use them to explain grain, filters, and control totals, not as real business KPIs.

---

## Limitations

- Stand-in engines (DuckDB/SQLite/pandas) replace paid MPP/warehouses where noted.
- Simplified schemas vs production SAP/Oracle/Hive estates.
- Charts are matplotlib teaching visuals, not vendor BI embeds.

---

## Exercises

1. Add a cost-center InfoObject and slice margin.
2. Break FX coverage for one day and detect with a test.
3. Write a BW→Snowflake naming map in docs.

---

## License / attribution

Educational portfolio content by Faiz Elahi. Synthetic data for teaching only.

