from pydantic import BaseModel 
from typing import Optional
from enum import Enum

class EntrySide(str, Enum):
    credit = 'credit'
    debit = 'debit'
    
class AccountType(str, Enum):
    asset = 'asset'
    liability = 'liability'
    capital = 'capital'
    revenue = 'revenue'
    expenses = 'expenses'

class LedgerItem(BaseModel):
    name: str
    entry_side: EntrySide
    account_type: Optional[AccountType] = None