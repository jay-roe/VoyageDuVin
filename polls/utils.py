import os.path
from openpyxl import Workbook, load_workbook

path = "results.xlsx"
sheet = "Sheet"  # default sheet


def create_workbook():
    wb = Workbook()
    wb.save(path)


def add_score(name):
    if not (os.path.isfile(path)):
        create_workbook()

    wb = load_workbook(filename=path)
    ws = wb[sheet]
    ws['A1'] = name
    wb.save(path)
