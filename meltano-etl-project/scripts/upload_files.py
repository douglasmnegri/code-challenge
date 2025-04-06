import sys
from pathlib import Path
import subprocess
import json

def run_csv_pipeline(project_path: str, date_str: str):
    csv_path_order_details = Path(project_path) / "../data" / "csv" / date_str / "order_details.csv"
    csv_path_orders = Path(project_path) / "../data" / "postgres" / "orders" / date_str / "public-orders.csv"

    if not csv_path_order_details.exists():
        print(f"Could not find order details table in the current path: {csv_path_order_details}")
        print("Error: Files were NOT uploaded", file=sys.stderr)
        return

    if not csv_path_orders.exists():
        print(f"Could not find orders table in the current path : {csv_path_orders}")
        print("Error: Files were NOT uploaded", file=sys.stderr)
        return

    files_config = [
        {
            "entity": "order_details",
            "path": csv_path_order_details.as_posix(),
            "keys": ["order_id"],
            "delimiter": ","
        },
        {
            "entity": "orders",
            "path": csv_path_orders.as_posix(),
            "keys": ["order_id"],
            "delimiter": ","
        }
    ]

    config_json = json.dumps(files_config)
    commands = [
        f"meltano config tap-csv set files '{config_json}'",
        "meltano run tap-csv target-postgres"
    ]

    for cmd in commands:
        subprocess.run(f"cd {project_path} && {cmd}", shell=True, check=True, executable="/bin/bash")

    print("Success! Orders and Orders Details were loaded into the database.")

if __name__ == "__main__":
    project_path, date_str = sys.argv[1], sys.argv[2]
    run_csv_pipeline(project_path, date_str)