"""Month-by-month tests for manager.py (run: python test_manager.py).
Works on a temporary copy of readings.csv, so your real CSV is never changed."""
import os
import shutil
import tempfile

import matplotlib
matplotlib.use("Agg")            # no chart windows while testing
import pandas as pd

from manager import ElectricityManager
from generate_data import MONTHS

failed = []


def check(name, condition):
    print(f"   {'PASS' if condition else 'FAIL'}  {name}")
    if not condition:
        failed.append(name)


def expected_total(u):
    """Independent bill formula (does NOT use billing.py)."""
    energy = (min(u, 100) * 3 + max(0, min(u, 200) - 100) * 5
              + max(0, min(u, 300) - 200) * 7 + max(0, u - 300) * 9)
    return round(energy + 50 + round(energy * 0.05, 2), 2)


tmp = tempfile.mkdtemp()
csv = os.path.join(tmp, "readings.csv")
shutil.copy("readings.csv", csv)
raw = pd.read_csv("readings.csv")
mgr = ElectricityManager(csv_path=csv, chart_dir=os.path.join(tmp, "charts"))

for month in MONTHS:
    print(f"\n=== {month} ===")
    sub = raw[raw["month"] == month]

    # 1. data loaded for this month
    check("20 readings loaded", len(mgr.df[mgr.df["month"] == month]) == 20)

    # 2. monthly_trend total and average
    t = mgr.monthly_trend()
    check("trend total matches CSV", int(t.loc[month, "total"]) == int(sub["units"].sum()))
    check("trend average matches CSV", abs(t.loc[month, "average"] - round(sub["units"].mean(), 1)) < 0.01)

    # 3. bill for every house (independent formula vs billing.py via manager)
    ok = all(abs(mgr.bill_for(r.house_id, month)["total"] - expected_total(int(r.units))) < 0.01
             for r in sub.itertuples())
    check("bill correct for all 20 houses", ok)

    # 4. month text is case-insensitive / accepts full name (uses first 3 letters)
    check("lookup works with lower-case and full month name",
          mgr.get_units("h01", month.lower()) == mgr.get_units("H01", month) ==
          mgr.get_units("H01", {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
                                "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
                                "Sep": "September", "Oct": "October", "Nov": "November",
                                "Dec": "December"}[month]))

    # 5. add a new reading in this month, then reject the duplicate
    mgr.add_reading("H21", "test", month, 250)
    check("add H21 -> bill Rs1257.50", mgr.bill_for("H21", month)["total"] == 1257.50)
    check("trend now has 21 readings in month", int(mgr.df[mgr.df["month"] == month].shape[0]) == 21)
    try:
        mgr.add_reading("H21", "test", month, 250)
        check("duplicate reading rejected", False)
    except ValueError:
        check("duplicate reading rejected", True)
    check("new reading saved to CSV file",
          ((pd.read_csv(csv)["house_id"] == "H21") & (pd.read_csv(csv)["month"] == month)).any())

    # 6. insights still work when the file holds ONLY this month (the original crash case)
    only_csv = os.path.join(tmp, f"only_{month}.csv")
    raw[raw["month"] == month].to_csv(only_csv, index=False)
    only = ElectricityManager(csv_path=only_csv, chart_dir=os.path.join(tmp, "charts"))
    try:
        lines = only.insights()
        check("insights() runs on single-month data (5 lines)", len(lines) == 5)
    except Exception as e:
        check(f"insights() runs on single-month data ({type(e).__name__}: {e})", False)

print("\n=== All months together ===")
full = ElectricityManager(csv_path=csv, chart_dir=os.path.join(tmp, "charts"))
full.df = full.df[full.df["house_id"] != "H21"].reset_index(drop=True)
lines = full.insights()
check("insights() gives 5 lines", len(lines) == 5)
check("peak Jun, lowest Feb", lines[0].startswith("Peak month is Jun") and "lowest is Feb" in lines[0])
check("summer 314 vs winter 187, 68%", "314" in lines[1] and "187" in lines[1] and "68%" in lines[1])
check("top 5 = 32.7%, H19 Tiwari 4067", "32.7%" in lines[2] and "H19 (Tiwari)" in lines[2] and "4067" in lines[2])
check("12 months in trend, Jan-Dec order", list(full.monthly_trend().index.astype(str)) == MONTHS)
check("line chart (H01, 12 months) saved", os.path.exists(full.line_chart("H01", show=False)))
check("line chart (all-house average) saved", os.path.exists(full.line_chart(None, show=False)))
check("bar chart saved", os.path.exists(full.bar_chart(10, show=False)))

print("\n=== Error handling ===")
for label, call, exc in [
    ("invalid month 'abc'", lambda: mgr.add_reading("H22", "x", "abc", 100), ValueError),
    ("negative units", lambda: mgr.add_reading("H22", "x", "Jan", -5), ValueError),
    ("unknown house H99", lambda: mgr.get_units("H99", "Jan"), KeyError),
]:
    try:
        call()
        check(label, False)
    except exc:
        check(label, True)

shutil.rmtree(tmp)
print("\n" + ("ALL TESTS PASSED" if not failed else f"{len(failed)} TEST(S) FAILED: {failed}"))
