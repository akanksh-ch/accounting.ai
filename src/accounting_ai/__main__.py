import argparse
from pathlib import Path
from accounting_ai.excel import get_items_from_workbook
from accounting_ai.build_report import build_report

def main():
    parser = argparse.ArgumentParser(description="Generate Financial statements from Trial balance")

    parser.add_argument("input", type=Path, help="Trial balance Excel file")
    parser.add_argument("output", type=Path, help="Output Excel file")

    args = parser.parse_args()

    items = get_items_from_workbook(args.input)
    build_report(items, args.output)
    
    print(f'Financial statements saved to {args.output}')

if __name__ == '__main__':
    main()
