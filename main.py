"""Household Electricity Consumption & Bill Calculator - menu-driven app."""
from manager import ElectricityManager
from billing import format_bill
from generate_data import MONTHS


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a whole number.")


def add_reading(mgr):
    hid = input("House ID (e.g. H05): ")
    owner = input("Owner name: ")
    month = input(f"Month ({', '.join(MONTHS)}): ")
    units = ask_int("Units consumed: ")
    try:
        mgr.add_reading(hid, owner, month, units)
        print("  Saved to CSV.")
        print(format_bill(mgr.bill_for(hid, month), hid.upper(), month.capitalize()[:3]))
    except ValueError as e:
        print("  Error:", e)


def show_bill(mgr):
    hid, month = input("House ID: "), input("Month: ")
    try:
        print(format_bill(mgr.bill_for(hid, month), hid.upper(), month.capitalize()[:3]))
    except KeyError as e:
        print("  Error:", e.args[0])


def show_trend(mgr):
    print("\nMonth-wise consumption (all houses):")
    print(mgr.monthly_trend().to_string())


def show_top(mgr):
    n = ask_int("How many houses? ")
    print(mgr.top_houses(n).to_string(index=False))


def line_chart(mgr):
    hid = input("House ID (blank = all houses average): ").strip() or None
    try:
        print("  Saved:", mgr.line_chart(hid))
    except KeyError as e:
        print("  Error:", e.args[0])


def bar_chart(mgr):
    print("  Saved:", mgr.bar_chart(ask_int("Top how many houses? ")))


def show_insights(mgr):
    print("\nKey insights:")
    for i, text in enumerate(mgr.insights(), 1):
        print(f" {i}. {text}")


MENU = {
    "1": ("Add a new meter reading", add_reading),
    "2": ("Calculate bill for a house/month", show_bill),
    "3": ("Month-wise consumption trend", show_trend),
    "4": ("Highest-consuming houses", show_top),
    "5": ("Line chart (trend)", line_chart),
    "6": ("Bar chart (top houses)", bar_chart),
    "7": ("Show insights", show_insights),
    "0": ("Exit", None),
}


def main():
    mgr = ElectricityManager()
    while True:
        print("\n===== ELECTRICITY BILL CALCULATOR =====")
        for key, (label, _) in MENU.items():
            print(f" {key}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice in MENU:
            MENU[choice][1](mgr)
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
