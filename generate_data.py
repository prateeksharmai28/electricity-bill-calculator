"""Creates the self-made dataset: 20 houses x 12 months of meter readings."""
import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Seasonal factor: summer (AC/cooler) and monsoon humidity push usage up
SEASON = [0.80, 0.80, 0.90, 1.10, 1.35, 1.50, 1.40, 1.30, 1.15, 0.95, 0.85, 0.85]
OWNERS = ["Sharma", "Verma", "Singh", "Gupta", "Yadav", "Khan", "Mehta", "Jain",
          "Kumar", "Patel", "Reddy", "Nair", "Joshi", "Bansal", "Malik", "Chopra",
          "Saxena", "Mishra", "Tiwari", "Arora"]


def generate(path="readings.csv", seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for i, owner in enumerate(OWNERS, start=1):
        base = rng.integers(120, 320)  # house's base monthly usage
        for month, factor in zip(MONTHS, SEASON):
            units = int(base * factor * rng.uniform(0.9, 1.1))
            rows.append({"house_id": f"H{i:02d}", "owner": owner,
                         "month": month, "units": units})
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Created {path} with {len(rows)} readings.")


if __name__ == "__main__":
    generate()
