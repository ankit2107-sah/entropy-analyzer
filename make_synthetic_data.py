import csv
import random
import sys
from datetime import date, timedelta

# Usage: python make_synthetic_data.py [rows]
# Default 500000 rows, roughly 50-60 MB.
ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
OUT = "samples/synthetic_egov_large.csv"

random.seed(42)  # same output every run

STATES = ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana",
          "Maharashtra", "Gujarat", "Rajasthan", "Uttar Pradesh", "Bihar",
          "West Bengal", "Odisha", "Punjab", "Haryana", "Madhya Pradesh"]
SERVICES = ["Birth Certificate", "Income Certificate", "Land Record",
            "Ration Card", "Pension Scheme", "Water Connection",
            "Road Complaint", "Health Camp", "Scholarship", "Driving Licence"]
STATUS = ["Approved", "Pending", "Rejected", "Under Review"]
FIRST = ["Asha", "Ravi", "Meena", "Arjun", "Lakshmi", "Imran", "Priya", "Sunil"]
LAST = ["Kumar", "Devi", "Singh", "Rao", "Khan", "Nair", "Patel", "Sharma"]

start = date(2019, 1, 1)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", "state", "district_code", "service", "applicant_name",
                "email", "phone", "application_date", "status", "amount_inr", "remarks"])
    for i in range(1, ROWS + 1):
        name = f"{random.choice(FIRST)} {random.choice(LAST)}"
        email = f"user{i}@example.com"                     # reserved test domain
        phone = f"+91-1{random.randint(10**8, 10**9 - 1)}"   # starts with 1, not a real mobile range
        d = start + timedelta(days=random.randint(0, 2500))
        w.writerow([
            f"EG{i:08d}",
            random.choice(STATES),
            random.randint(101, 799),
            random.choice(SERVICES),
            name,
            email,
            phone,
            d.isoformat(),
            random.choice(STATUS),
            random.randint(0, 50000),
            random.choice(["", "Document verified", "Field visit done", "Resubmitted"]),
        ])

print(f"Wrote {ROWS} rows to {OUT}")
