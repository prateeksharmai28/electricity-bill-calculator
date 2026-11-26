"""ElectricityManager: CSV storage, Pandas analysis and charts."""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from billing import calculate_bill
from generate_data import MONTHS, generate

COLUMNS = ["house_id", "owner", "month", "units"]


class ElectricityManager:
    def __init__(self, csv_path="readings.csv", chart_dir="charts"):
        self.csv_path = csv_path
        self.chart_dir = chart_dir
        os.makedirs(chart_dir, exist_ok=True)
        self.df = self._load()

    # ---------- file handling ----------
    def _load(self):
        try:
            df = pd.read_csv(self.csv_path)
        except FileNotFoundError:
            print("readings.csv not found - generating sample data...")
            generate(self.csv_path)
            df = pd.read_csv(self.csv_path)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=COLUMNS)
        # cleaning
        df = df.dropna().drop_duplicates(subset=["house_id", "month"], keep="last")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")
        df = df.dropna(subset=["units"])
        df["month"] = pd.Categorical(df["month"], categories=MONTHS, ordered=True)
        return df.reset_index(drop=True)

    def save(self):
        out = self.df.copy()
        out["month"] = out["month"].astype(str)
        out.to_csv(self.csv_path, index=False)

    # ---------- add / lookup ----------
    def add_reading(self, house_id, owner, month, units):
        house_id, month = house_id.strip().upper(), month.strip().capitalize()[:3]
        if month not in MONTHS:
            raise ValueError(f"Month must be one of {', '.join(MONTHS)}")
        if units < 0:
            raise ValueError("Units cannot be negative.")
        exists = ((self.df["house_id"] == house_id) & (self.df["month"] == month)).any()
        if exists:
            raise ValueError(f"Reading for {house_id} / {month} already exists.")
        new = pd.DataFrame([{"house_id": house_id, "owner": owner.strip().title(),
                             "month": month, "units": int(units)}])
        new["month"] = pd.Categorical(new["month"], categories=MONTHS, ordered=True)
        self.df = pd.concat([self.df, new], ignore_index=True)
        self.save()

    def house_ids(self):
        return sorted(self.df["house_id"].unique())

    def get_units(self, house_id, month):
        row = self.df[(self.df["house_id"] == house_id.upper()) &
                      (self.df["month"] == month.capitalize()[:3])]
        if row.empty:
            raise KeyError("No reading found for that house and month.")
        return int(row["units"].iloc[0])

    def bill_for(self, house_id, month):
        return calculate_bill(self.get_units(house_id, month))

    # ---------- analysis (Pandas / NumPy) ----------
    def monthly_trend(self):
        g = self.df.groupby("month", observed=True)["units"]
        return pd.DataFrame({"total": g.sum(), "average": g.mean().round(1)})

    def house_totals(self):
        return (self.df.groupby(["house_id", "owner"])["units"].sum()
                .sort_values(ascending=False).reset_index())

    def top_houses(self, n=5):
        return self.house_totals().head(n)

    def all_bills(self):
        d = self.df.copy()
        d["bill"] = d["units"].apply(lambda u: calculate_bill(u)["total"])
        return d

    def insights(self):
        if self.df.empty:
            return ["No data yet. Add readings with option 1 first."]
        trend = self.monthly_trend()
        totals = self.house_totals()
        bills = self.all_bills()
        peak, low = trend["total"].idxmax(), trend["total"].idxmin()
        # reindex() gives NaN for months that have no readings (loc[] would crash)
        summer = trend["average"].reindex(["Apr", "May", "Jun", "Jul"]).mean()
        winter = trend["average"].reindex(["Dec", "Jan", "Feb"]).mean()
        top5_share = totals["units"].head(5).sum() / totals["units"].sum() * 100
        slab4 = (self.df["units"] > 300).mean() * 100
        if pd.isna(summer) or pd.isna(winter) or winter == 0:
            season_line = ("Summer vs winter comparison needs readings for both "
                           "Apr-Jul and Dec-Feb - not enough data yet.")
        else:
            season_line = (f"Summer (Apr-Jul) average per house is {summer:.0f} units vs "
                           f"{winter:.0f} in winter (Dec-Feb): "
                           f"{(summer / winter - 1) * 100:.0f}% higher.")
        return [
            f"Peak month is {peak} ({int(trend.loc[peak, 'total'])} units); "
            f"lowest is {low} ({int(trend.loc[low, 'total'])} units).",
            season_line,
            f"Top 5 houses use {top5_share:.1f}% of all electricity; "
            f"highest is {totals.iloc[0]['house_id']} ({totals.iloc[0]['owner']}) "
            f"with {int(totals.iloc[0]['units'])} units/year.",
            f"{slab4:.1f}% of house-months fall in the costliest slab (>300 units).",
            f"Average monthly bill is Rs{np.mean(bills['bill']):.0f}; "
            f"highest single bill is Rs{bills['bill'].max():.0f}.",
        ]

    # ---------- charts ----------
    def line_chart(self, house_id=None, show=True):
        fig, ax = plt.subplots(figsize=(9, 5))
        if house_id:
            d = self.df[self.df["house_id"] == house_id.upper()].sort_values("month")
            if d.empty:
                plt.close(fig)
                raise KeyError("No data for that house.")
            ax.plot(d["month"].astype(str), d["units"], marker="o", color="tab:green")
            ax.set_title(f"Monthly Consumption - {house_id.upper()}")
            name = f"line_{house_id.upper()}.png"
        else:
            t = self.monthly_trend()
            ax.plot(t.index.astype(str), t["average"], marker="o", color="tab:blue")
            ax.set_title("Average Monthly Consumption per House")
            name = "line_monthly_trend.png"
        ax.set_xlabel("Month"); ax.set_ylabel("Units (kWh)"); ax.grid(alpha=.3)
        return self._finish(fig, name, show)

    def bar_chart(self, n=10, show=True):
        top = self.top_houses(n)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(top["house_id"], top["units"], color="tab:orange")
        for x, y in zip(top["house_id"], top["units"]):
            ax.text(x, y, str(int(y)), ha="center", va="bottom", fontsize=8)
        ax.set_title(f"Top {n} Highest-Consuming Houses (Yearly)")
        ax.set_xlabel("House ID"); ax.set_ylabel("Total Units (kWh)")
        return self._finish(fig, "bar_top_houses.png", show)

    def _finish(self, fig, name, show):
        path = os.path.join(self.chart_dir, name)
        fig.tight_layout(); fig.savefig(path, dpi=120)
        if show:
            plt.show()
        plt.close(fig)
        return path
