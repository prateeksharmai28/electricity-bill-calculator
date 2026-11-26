# Household Electricity Consumption & Bill Calculator

**Live website:** https://prateeksharmai28.github.io/electricity-bill-calculator/

A Python capstone project that stores monthly meter readings of 20 houses, calculates slab-wise electricity bills, and analyses the data with tables, charts and automatic insights. It comes in two versions that use the same data and give the same results:

1. **Python program** (terminal menu): `main.py`
2. **Website** (runs in any browser): `index.html`

Team: Prateek Sharma, Meet Yadav, Abhishek, Sukhjot, Chetan. KR Mangalam University, B.Tech CSE (AI & ML), Semester I.

---

## What it does

- Holds **240 meter readings**: 20 houses (H01 to H20) x 12 months (Jan to Dec).
- Calculates a **bill** for any house and month, with a slab-wise breakdown, a fixed charge and 5% duty.
- Shows **month-wise consumption** (total and average per house).
- Ranks the **highest-consuming houses**.
- Draws a **line chart** (consumption over months) and a **bar chart** (top houses).
- Writes **5 data-driven insights** automatically.
- Lets you **add a new reading**, with checks for a wrong month, negative units and duplicate entries.

---

## How the bill is calculated

The more units a house uses, the higher the rate per unit. Each slab is charged only for the units that fall inside it.

| Units | Rate per unit |
|---|---|
| First 100 (1-100) | Rs 3 |
| Next 100 (101-200) | Rs 5 |
| Next 100 (201-300) | Rs 7 |
| Above 300 | Rs 9 |

On top of the energy charge: a **fixed charge of Rs 50** per month and **5% duty** on the energy charge.

**Example, 250 units:**

| Step | Working | Amount |
|---|---|---|
| Slab 1 | 100 x 3 | Rs 300 |
| Slab 2 | 100 x 5 | Rs 500 |
| Slab 3 | 50 x 7 | Rs 350 |
| Energy charge | | Rs 1150 |
| Duty (5%) | 5% of 1150 | Rs 57.50 |
| Fixed charge | | Rs 50 |
| **Total payable** | | **Rs 1257.50** |

---

## How it works (Python version)

### Files

| File | Purpose |
|---|---|
| `generate_data.py` | Creates `readings.csv` (seasonal usage pattern using NumPy random numbers). Also defines the `MONTHS` list. |
| `billing.py` | Pure functions: `calculate_bill()` does the slab maths, `format_bill()` makes the printable bill. |
| `manager.py` | `ElectricityManager` class: loads and cleans the CSV, adds readings, runs Pandas analysis, draws Matplotlib charts, builds insights. |
| `main.py` | The menu. It only takes input and prints output. |
| `readings.csv` | The stored data (`house_id, owner, month, units`). |
| `index.html` | The website version (see below). |
| `requirements.txt` | Libraries needed: pandas, numpy, matplotlib. |

### Data flow for one house (example: H05, Jun)

```
User types H05, Jun
   |
main.py          show_bill() takes the input
   |
manager.py       bill_for() finds the row in the DataFrame, gets units (e.g. 250)
   |
billing.py       calculate_bill(250) -> slab breakdown + duty + total
   |
main.py          format_bill() prints the bill on screen
```

Each file has one job and data moves in one direction: user, menu, manager, billing, and back.

### What happens at start-up

`ElectricityManager` loads `readings.csv` once, removes empty rows, duplicates and bad numbers, and keeps everything in a Pandas DataFrame. If `readings.csv` is missing, `generate_data.py` creates it automatically.

### Menu options

| Option | What it does |
|---|---|
| 1 | Add a new meter reading (saved to the CSV) and show its bill |
| 2 | Calculate the bill for a house and month |
| 3 | Month-wise consumption trend (total and average) |
| 4 | Highest-consuming houses |
| 5 | Line chart (one house or all-house average), saved in `charts/` |
| 6 | Bar chart of top houses, saved in `charts/` |
| 7 | Show the 5 insights |
| 0 | Exit |

### Run it

```
pip install -r requirements.txt
python main.py
```

`readings.csv` is generated automatically if it is missing.

---

## How it works (website version)

Open the live website: https://prateeksharmai28.github.io/electricity-bill-calculator/

`index.html` is a single file (HTML, CSS and JavaScript, with Chart.js for charts). It contains the same 240 readings and the same tariff, so every number matches the Python program.

| Section on the page | What to do | What happens |
|---|---|---|
| **Bill calculator** | Pick a house and month, or type any units, or move the slider | The stored reading is loaded and the bill updates instantly, with a coloured slab bar and a full breakdown |
| **Month-wise consumption** | Choose "All houses (average)" or one house | A line chart and a month table (total and average) |
| **Highest-consuming houses** | Choose 5, 10 or 20 houses | A bar chart of yearly units, with the owner's name on hover |
| **Key insights** | Read the list | The same 5 findings as option 7 in the Python program |
| **Add a meter reading** | Enter house ID, owner, month and units, then Save | The reading is checked, added, and the bill, charts and insights update |

Notes:

- New readings added on the website stay **in that browser tab only**. Press **Download readings.csv** to keep them.
- The website needs no installation and no server. It is hosted free on GitHub Pages.

---

## The 5 insights

Generated from the data (option 7 in Python, "Key insights" on the website):

1. Peak month and lowest month (June has the highest total, February the lowest).
2. Summer (Apr-Jul) average usage vs winter (Dec-Feb): about **68% higher** in summer.
3. Share of all electricity used by the top 5 houses: about **32.7%**, with H19 (Tiwari) the highest at 4067 units a year.
4. Share of house-months that fall in the costliest slab (above 300 units): about **27.9%**.
5. Average monthly bill (about Rs 1341) and the highest single bill (about Rs 3298).

---

## Error handling

| Situation | Result |
|---|---|
| Reading for the same house and month already exists | Error: reading already exists |
| Month is not Jan to Dec | Error: month must be one of Jan to Dec |
| Units are negative | Error: units cannot be negative |
| Units are not a whole number | Asks again for a whole number |
| House or month has no reading | Error: no reading found |
| Invalid menu choice | "Invalid choice" message |
| `readings.csv` missing or empty | Regenerated automatically / handled safely |

---

## Quick test of the bill logic

```python
from billing import calculate_bill

print(calculate_bill(250)["total"])   # 1257.5
print(calculate_bill(100)["total"])   # 365.0  (300 + 50 + 15)
print(calculate_bill(0)["total"])     # 50.0   (fixed charge only)
```

---

## Project marking rubric mapping

| Rubric area | Where it is covered |
|---|---|
| Problem understanding and design | Billing (functions), data and analysis (class), and user interface (menu) are separate files |
| Python implementation | Functions, loops, OOP, file handling, try/except |
| Data processing | Pandas groupby, data cleaning, NumPy statistics |
| Visualization and insights | Line chart and bar chart with titles and labels; 5 automatic insights |
| Report and demo | Project report (`Project_Report.pdf`) and the live website |



## Technologies

Python 3, Pandas, NumPy, Matplotlib, CSV, HTML, CSS, JavaScript, Chart.js, Git, GitHub Pages.

## Limitations and future scope

- The data is simulated, not from real meters.
- One fixed tariff is used for all houses.
- Future ideas: real smart-meter data, multiple tariffs, PDF bills, usage prediction with machine learning, a database instead of a CSV file.
