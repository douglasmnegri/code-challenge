import os
import shutil
from datetime import date

# Get current date and create the correct folder structure
def organize_csv_files(destination_dir, current_date):
    source_dir = "output"

    files = [i for i in os.listdir(source_dir) if i.endswith(".csv")]

    for file in files:
        table_name = file.replace("public-", "").replace(".csv", "")

        new_dir = os.path.join(destination_dir, table_name, current_date)
        os.makedirs(new_dir, exist_ok=True)

        src_path = os.path.join(source_dir, file)
        dest_path = os.path.join(new_dir, file)
        shutil.move(src_path, dest_path)
