# Automated BI Dashboard for Zomato (Simulated)

An end-to-end simulated BI pipeline: synthetic order data is generated nightly, loaded into
PostgreSQL, transformed into an analysis-ready mart, and visualized in a Tableau dashboard
(KPI cards, monthly revenue trend, orders-by-zone map, restaurant performance scatter plot,
and a customer cohort/retention analysis).

## Architecture

```
src/generate_data.py   -> data/*.csv               (synthetic customers/restaurants/orders)
src/run_pipeline.py    -> sql/00_create_raw_tables.sql  (bootstrap schema, idempotent)
                        -> sql/01_load_raw.sql           (truncate staging tables)
                        -> COPY csv -> raw_* tables       (via psycopg2 copy_expert, client-side)
                        -> sql/02_build_mart.sql          (rebuild mart_performance)
Zomato_Db.twb           -> connects to mart_performance via Tableau Bridge, refreshes extract
```

The mart is always built from data that was *just* loaded in the same run — raw tables are
truncated and reloaded before `mart_performance` is rebuilt, never after.

## Setup

1. Install PostgreSQL and Python 3.10+.
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in your real DB credentials. `.env` is gitignored — never commit it.
4. Create the database once: `createdb zomato_db` (or via psql/pgAdmin).
5. Run the pipeline manually to verify it works end-to-end:
   ```bash
   python src/run_pipeline.py
   ```
   This generates fresh CSVs into `data/`, creates the raw tables if missing, reloads them,
   and rebuilds `mart_performance`.
6. Open `Zomato_Db.twb` in Tableau, point the data source connection at your local
   `zomato_db` / `mart_performance` table, and republish to Tableau Public if desired.

## Automating it (make it actually run on a schedule)

The pipeline is a single script (`src/run_pipeline.py`), so "automating" it just means getting
Windows to run that script on a timer, and getting Tableau to refresh after it finishes.

### 1. Schedule the data pipeline (Windows Task Scheduler)

From an **elevated** PowerShell prompt, from this project folder:

```powershell
.\register_task.ps1
```

This registers a task named `ZomatoBIPipeline` that runs `python src\run_pipeline.py` daily
at 05:00, with up to 3 retries on failure. Test it immediately without waiting for the trigger:

```powershell
Start-ScheduledTask -TaskName 'ZomatoBIPipeline'
```

Check `logs/pipeline.log` afterward to confirm it ran cleanly. You can also open
**Task Scheduler > Task Scheduler Library > ZomatoBIPipeline** to see run history and
last-run result codes.

### 2. Schedule the Tableau refresh (Tableau Bridge)

Tableau Bridge is a separate app (not part of this repo) that keeps a published Tableau
Public/Online workbook in sync with a local data source on a schedule:

1. Install **Tableau Bridge** and sign in with the account that published `Zomato_Db.twb`.
2. In Tableau Public/Online, open the workbook's data source settings and set the
   **refresh schedule** to run daily at 06:00 (one hour after the pipeline, so
   `mart_performance` is guaranteed to be fresh by the time Bridge reads it).
3. Bridge runs as a background Windows service once configured — no script needed on your
   side beyond keeping it installed and signed in.

### End-to-end automated schedule

| Time  | What runs               | Where |
|-------|--------------------------|-------|
| 05:00 | `ZomatoBIPipeline` task  | Windows Task Scheduler, this repo |
| 06:00 | Extract refresh          | Tableau Bridge (configured in Tableau, not in this repo) |

## Project layout

```
.
├── data/                 # generated CSVs (gitignored)
├── logs/                 # pipeline run logs (gitignored)
├── sql/
│   ├── 00_create_raw_tables.sql
│   ├── 01_load_raw.sql
│   └── 02_build_mart.sql
├── src/
│   ├── generate_data.py
│   └── run_pipeline.py
├── assets/               # dashboard screenshots
├── Zomato_Db.twb
├── register_task.ps1
├── .env.example
└── requirements.txt
```

## Tech stack

- **Warehouse:** PostgreSQL
- **Transformation:** SQL (joins, `COPY`)
- **Automation:** Python (pandas, Faker, psycopg2), Windows Task Scheduler
- **Visualization:** Tableau Public / Tableau Bridge
