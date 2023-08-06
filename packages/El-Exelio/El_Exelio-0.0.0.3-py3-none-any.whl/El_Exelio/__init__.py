import openpyxl
from openpyxl.styles import Font


class Workbook:
    def __init__(self, file_name: str, title: str):
        self._file_name = file_name
        self.workbook = openpyxl.Workbook()  # Создание рабочей книги
        self.sheet = self.workbook.active  # Создание листа с именем title
        self.sheet.title = title

    def create_list(self, name: str):
        return self.workbook.create_sheet(name)

    def add_header(self, sheet=None, head: str = "Sheet", head_bold: bool = False, head_justify: str = "center"):
        if sheet is None:
            sheet = self.sheet
        sheet.append(head)  # Добавляем заголовок

        for cell in sheet["1:1"]:
            cell.font = Font(bold=head_bold)
            cell.alignment = cell.alignment.copy(horizontal=head_justify, vertical='center')

    def append(self, sheet=None, data: tuple | list = None, data_bold: bool = False, data_justify: str = "center"):
        if sheet is None:
            sheet = self.sheet

        sheet.append(data)

        k = 0
        for row in sheet.rows:
            if k == 0:
                continue
            k += 1
            for cell in row:
                cell.font = Font(bold=data_bold)
                alignment_obj = cell.alignment.copy(horizontal=data_justify, vertical='center')
                cell.alignment = alignment_obj

    def save(self):
        self.workbook.save(self._file_name + ".xlsx")
        self.workbook.close()
