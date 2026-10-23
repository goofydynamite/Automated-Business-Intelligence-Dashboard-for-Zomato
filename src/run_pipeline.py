import logging
import os
import subprocess
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("DATA_DIR", PROJECT_ROOT / "data"))
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("zomato_pipeline")


def get_connection():
    return psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
    )


def run_sql_file(cur, path: Path) -> None:
    log.info("Executing %s", path.name)
    cur.execute(path.read_text())


def export_mart_csv(cur, csv_path: Path) -> None:
    log.info("Exporting mart_performance to %s", csv_path)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        cur.copy_expert(
            "COPY mart_performance TO STDOUT WITH (FORMAT csv, HEADER true)", f
        )


def load_csv(cur, table: str, csv_path: Path) -> None:
    log.info("Loading %s into %s", csv_path.name, table)
    with open(csv_path, "r", encoding="utf-8") as f:
        cur.copy_expert(f"COPY {table} FROM STDIN WITH (FORMAT csv, HEADER true)", f)


def regenerate_data() -> None:
    log.info("Generating fresh synthetic data")
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "src" / "generate_data.py")],
        check=True,
    )


def run_pipeline(skip_generate: bool = False) -> None:
    if not skip_generate:
        regenerate_data()

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                run_sql_file(cur, PROJECT_ROOT / "sql" / "00_create_raw_tables.sql")
                run_sql_file(cur, PROJECT_ROOT / "sql" / "01_load_raw.sql")
                load_csv(cur, "raw_customers", DATA_DIR / "customers.csv")
                load_csv(cur, "raw_restaurants", DATA_DIR / "restaurants.csv")
                load_csv(cur, "raw_orders", DATA_DIR / "orders.csv")
                run_sql_file(cur, PROJECT_ROOT / "sql" / "02_build_mart.sql")
                export_mart_csv(cur, DATA_DIR / "zomato_mart.csv")
        log.info("Pipeline completed successfully.")
    except Exception:
        log.exception("Pipeline failed; transaction rolled back.")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline()
