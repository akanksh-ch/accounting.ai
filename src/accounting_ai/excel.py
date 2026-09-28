import openpyxl
from pathlib import Path
from accounting_ai.types.ledger import LedgerItem


def get_items_from_workbook(workbook_file: Path) -> List[LedgerItem]:
    wb = openpyxl.load_workbook(filename=workbook_file)
    ws = wb.worksheets[0]
    
    items = []
    
    for row in ws.iter_rows(min_row=2):
        account_name = row[0].internal_value
        entry_side = ''
        if row[1].internal_value == 'None': # i.e. it's a credit
            entry_side = 'credit'
        else:
            entry_side = 'debit'

        item = LedgerItem(name=account_name, entry_side=entry_side, account_type=None)
    
        items.append(item)

    return items