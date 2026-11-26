"""Slab-wise electricity bill calculation (pure functions)."""

# (units in this slab, rate per unit in Rs). None = no upper limit.
SLABS = [(100, 3.0), (100, 5.0), (100, 7.0), (None, 9.0)]
FIXED_CHARGE = 50.0   # Rs per month
TAX_RATE = 0.05       # 5% electricity duty on energy charges


def calculate_bill(units):
    """Return a dict with slab-wise breakdown and the final payable amount."""
    if units < 0:
        raise ValueError("Units consumed cannot be negative.")

    remaining = units
    breakdown = []
    energy_charge = 0.0
    start = 0
    for limit, rate in SLABS:
        if remaining <= 0:
            break
        used = remaining if limit is None else min(remaining, limit)
        cost = used * rate
        end = start + used
        breakdown.append({"slab": f"{start + 1}-{end}", "units": used,
                          "rate": rate, "amount": cost})
        energy_charge += cost
        remaining -= used
        start = end

    tax = round(energy_charge * TAX_RATE, 2)
    total = round(energy_charge + FIXED_CHARGE + tax, 2)
    return {"units": units, "breakdown": breakdown,
            "energy_charge": energy_charge, "fixed_charge": FIXED_CHARGE,
            "tax": tax, "total": total}


def format_bill(bill, house_id="", month=""):
    """Return a printable bill string."""
    lines = ["=" * 44, f" ELECTRICITY BILL  {house_id} {month}".rstrip(), "=" * 44]
    for row in bill["breakdown"]:
        lines.append(f" {row['slab']:>9} units: {row['units']:>4} x Rs{row['rate']:<4} = Rs{row['amount']:>8.2f}")
    lines += ["-" * 44,
              f" Energy charge : Rs{bill['energy_charge']:>10.2f}",
              f" Fixed charge  : Rs{bill['fixed_charge']:>10.2f}",
              f" Duty (5%)     : Rs{bill['tax']:>10.2f}",
              f" TOTAL PAYABLE : Rs{bill['total']:>10.2f}", "=" * 44]
    return "\n".join(lines)
