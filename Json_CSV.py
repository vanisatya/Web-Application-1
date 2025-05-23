import json
import csv
import pandas as pd
from datetime import datetime

# Paths
input_file = "apm_metrics.log"
output_file = "apm_metrics.csv"

# Define all possible fields
fieldnames = [
    "type", "timestamp", "path", "method", "status_code", "duration_ms",
    "event_name", "page", "client_ip", "logged_at"
]

# Step 1: Convert JSON to CSV
with open(input_file, "r") as infile, open(output_file, "w", newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in infile:
        data = json.loads(line)
        row = {key: data.get(key, "") for key in fieldnames}
        writer.writerow(row)

print(f"✅ CSV file saved: {output_file}")

# Step 2: Load CSV for analysis
df = pd.read_csv(output_file)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Filter request events
reqs = df[df["type"] == "request"]
valid_reqs = reqs[reqs["duration_ms"].notna()]

# ➤ 1. Request/Response Time (Latency)
avg_response = valid_reqs["duration_ms"].mean()

# ➤ 2. Error Rate
total = valid_reqs.shape[0]
errors = valid_reqs[valid_reqs["status_code"] >= 400].shape[0]
error_rate = (errors / total) * 100 if total > 0 else 0

# ➤ 3. Throughput (Requests per minute)
throughput_series = valid_reqs.set_index("timestamp").resample("1Min").size()
peak_throughput = throughput_series.max()
avg_throughput = throughput_series.mean()

# ➤ 4. Availability (based on /health)
health = valid_reqs[valid_reqs["path"] == "/health"]
available = health[health["status_code"] == 200].shape[0]
uptime_rate = (available / health.shape[0]) * 100 if health.shape[0] > 0 else 0

# Step 3: Print APM Summary
print("\n🔍 Web APM Summary:")
print(f"• Avg Request/Response Time: {round(avg_response, 2)} ms")
print(f"• Error Rate: {round(error_rate, 2)}%")
print(f"• Avg Throughput: {round(avg_throughput, 2)} requests/min")
print(f"• Peak Throughput: {peak_throughput} requests/min")
print(f"• Availability (via /health): {round(uptime_rate, 2)}%")
