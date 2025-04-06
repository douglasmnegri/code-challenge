import os
import shutil
import sys

def organize_files(project_root, execution_date):
    csv_source_dir = os.path.join(project_root, "../data/csv")
    postgres_source_dir = os.path.join(project_root, "../data/postgres")

    csv_source = os.path.join(csv_source_dir, "order_details.csv")
    if os.path.exists(csv_source):
        csv_dest_dir = os.path.join(csv_source_dir, execution_date)
        os.makedirs(csv_dest_dir, exist_ok=True)
        shutil.move(csv_source, os.path.join(csv_dest_dir, "order_details.csv"))

    for filename in os.listdir(postgres_source_dir):
        if filename.endswith(".csv"):
            table_name = filename.replace("public-", "").replace(".csv", "")
            dest_dir = os.path.join(
                project_root,
                "../data/postgres",
                table_name,
                execution_date
            )
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(
                os.path.join(postgres_source_dir, filename),
                os.path.join(dest_dir, filename)
            )

if __name__ == "__main__":
    project_root = sys.argv[1]
    execution_date = sys.argv[2]
    organize_files(project_root, execution_date)