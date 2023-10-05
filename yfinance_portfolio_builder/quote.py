from dataclasses import dataclass
from datetime import datetime


@dataclass
class Quote:
    date: datetime
    price: float


