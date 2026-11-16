from dataclasses import dataclass


@dataclass
class Expense:
    trip_id: int
    description: str
    amount: float
    category: str
    id: int | None = None