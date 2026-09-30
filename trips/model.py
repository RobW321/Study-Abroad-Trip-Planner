from dataclasses import dataclass

@dataclass
class Trip:
    name: str
    destination: str
    start_date: str
    end_date: str
    id: int | None = None