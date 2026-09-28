import argparse
from pathlib import Path
from accounting_ai.excel import get_items_from_workbook

def main():
    parser = argparse.ArgumentParser(description="Generate Financial statements from Trial balance")

    parser.add_argument("input", type=Path, help="Trial balance Excel file")
    parser.add_argument("output", type=Path, help="Output Excel file")

    args = parser.parse_args()

    print(get_items_from_workbook(args.input)) 

if __name__ == '__main__':
    main()
