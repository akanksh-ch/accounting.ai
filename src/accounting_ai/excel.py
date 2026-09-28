import openpyxl
from pathlib import Path
from accounting_ai.types.ledger import LedgerItem
from accounting_ai.classify import classify_account


def get_items_from_workbook(workbook_file: Path) -> list[LedgerItem]:
    """Read the first worksheet's account amounts and classify each account name."""
    wb = openpyxl.load_workbook(filename=workbook_file)
    ws = wb.worksheets[0]
    
    items = []
    
    for account_name, debit, credit in ws.iter_rows(min_row=2, max_col=3, values_only=True):
        if debit in (None, '', 'None'):  # i.e. it's a credit
            entry_side = 'credit'
            value = credit
        else:
            entry_side = 'debit'
            value = debit
            
        account_type = classify_account(account_name)

        item = LedgerItem(name=account_name, entry_side=entry_side, account_type=account_type, value=float(value))
    
        items.append(item)

    return items
