import csv
import os
from datetime import datetime


HISTORY_FILE = "datasets/history/activity_history.csv"


def log_activity(module, source, people, status):

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "Module",
                "Source",
                "People",
                "Status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            module,
            source,
            people,
            status
        ])