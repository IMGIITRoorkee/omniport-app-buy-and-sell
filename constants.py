"""
The type of periodicity
"""

DAILY = "day"
WEEKLY = "week"
MONTHLY = "month"
YEARLY = "year"
LIFESPAN = "lfs"

PERIODICITY = (
    (DAILY, "Daily"),
    (WEEKLY, "Weekly"),
    (MONTHLY, "Monthly"),
    (YEARLY, "Yearly"),
    (LIFESPAN, "Lifespan"),
)

PERIODICITY_MAP = {
    'Daily': DAILY,
    'Weekly': WEEKLY,
    'Monthly': MONTHLY,
    'Yearly': YEARLY,
    'Lifespan': LIFESPAN,
}