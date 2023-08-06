pip install easy_excel, xlwt


Example

    from python_easy_excel import Excel, Column


    class A:
        def __init__(self, a='Nothing', b='Все хорошо', c=43):
            self.a, self.b, self.c = a, b, c


    excel_example = Excel()

    columns = [Column('a'), Column('b', lambda x: x.b), Column('Thi is C', lambda x: x.c)]
    excel_example.add_sheet('New sheet', columns=columns, objects=[A(), A(b=354), A(423,12)])
    excel_example.add_sheet('double', columns=columns, objects=[A(b='4233'), A(12, 12)])
    excel_example.add_sheet('third', columns=columns, objects=[A(), A(b=354), A(423,12)])

    excel_example.save(file_name='Новый файл', dir='/home/nicking/')

