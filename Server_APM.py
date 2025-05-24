import psutil
import json
import os
import time
from datetime import datetime

# Define log directory and file
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "server_metrics.log")

# Function to track and log server metrics
def log_metrics():
    while True:
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")
        time.sleep(10)  # log every 10 seconds

if __name__ == "__main__":
    log_metrics()
