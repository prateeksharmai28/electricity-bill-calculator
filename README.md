# Household Electricity Consumption & Bill Calculator

Python project: 20 houses x 12 months of self-created meter readings (CSV).

## Run
    pip install -r requirements.txt
    python main.py          # readings.csv is auto-generated if missing

## Files
| File | Purpose |
|---|---|
| generate_data.py | Builds readings.csv (seasonal usage pattern, NumPy random) |
| billing.py | Slab-wise bill functions |
| manager.py | `ElectricityManager` class: CSV I/O, Pandas analysis, charts |
| main.py | Menu-driven interface |

## Tariff (slabs)
| Units | Rate |
|---|---|
| 1-100 | Rs3 |
| 101-200 | Rs5 |
| 201-300 | Rs7 |
| 300+ | Rs9 |
Plus Rs50 fixed charge and 5% duty on energy charge.

## Rubric mapping
- Problem design: billing (functions) / data + analysis (class) / UI (menu) separated
- Python quality: functions, loops, OOP, file handling, try/except
- Data processing: Pandas groupby, cleaning, NumPy stats
- Visualization: line chart (trend) and bar chart (top houses), titled and labelled
- Insights: option 7 gives 5 data-driven findings

## Sample insights
1. Peak month is June, lowest is February.
2. Summer average usage is ~67% higher than winter.
3. Top 5 houses consume ~32% of all electricity.
