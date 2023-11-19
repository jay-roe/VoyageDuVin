import os.path
from openpyxl import Workbook, load_workbook

path = "results.xlsx"
sheet = "Sheet"  # default sheet


def create_workbook():
    wb = Workbook()
    ws = wb[sheet]
    ws['A1'] = "Name"
    # TODO update this to match the desired session
    for i in range(1, 7):
        ws[f'{chr(65+i)}1'] = f'Vin {i}'

    wb.save(path)


def add_score(data):
    if not (os.path.isfile(path)):
        create_workbook()

    wb = load_workbook(filename=path)
    ws = wb[sheet]
    ws.append(data)
    wb.save(path)
