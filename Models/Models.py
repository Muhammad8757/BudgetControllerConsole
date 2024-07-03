from dataclasses import dataclass
import datetime

@dataclass(frozen=True)
class user:
    name: str
    phone_number: int
    password: str

@dataclass(frozen=True)
class transaction:
    amount: float
    date: datetime
    category: int 

@dataclass(frozen=True)
class category:
    name: str

@dataclass(frozen=True)
class transaction_details:
    amount: float
    date: datetime
    description: str
    category_id: int