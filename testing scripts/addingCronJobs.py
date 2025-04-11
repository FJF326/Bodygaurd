import subprocess

# Define the cron jobs you want to add
cron_jobs = [
    '0 9 * * * evilScript.py',
    '0 17 * * * echo "Good evening!"',
]

# Read current crontab (if any)
result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    current_cron = result.stdout.splitlines()
else:
    current_cron = []

# Append new jobs if they don't already exist
for job in cron_jobs:
    if job not in current_cron:
        current_cron.append(job)

# Combine the cron jobs into one string
updated_cron = "\n".join(current_cron).strip() + "\n"

# Write the updated crontab
proc = subprocess.run(['crontab', '-'], input=updated_cron, text=True)

if proc.returncode == 0:
    print("Cron jobs added successfully.")
else:
    print("Failed to update crontab.")
