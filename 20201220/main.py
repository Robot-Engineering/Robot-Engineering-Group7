import xlrd
import xlwt
from xlutils.copy import copy
import os
import view


def read_excel():
    try:
        workbook = xlrd.open_workbook('testdat/students.xlsx')
        sheet1 = workbook.sheets()[0]
        sheet = copy(workbook)
        sheet2 = sheet.get_sheet(0)

        for i in range(1, sheet1.nrows):
            element = sheet1.cell(i, 1).value
            photo_data = list(os.walk('testdat/' + str(int(element))))[0][2:]
            print(photo_data[0])
            if not photo_data[0]:
                color = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
                sheet2.write(i, 1, sheet1.cell(i, 1).value, color)
                sheet.save('testdat/students.xlsx')
            elif '.jpg' in photo_data[0][0]:
                sheet2.write(i, 2, 'testdat/' + str(int(element)))
                sheet.save('testdat/students.xlsx')
        else:
            a = os.listdir('testdat/')
            for _ in a:
                if '.xlsx' in _:
                    os.rename('testdat/students.xlsx', 'testdat/students.xls')
    except Exception as e:
        print(e)


def return_dict():
    workbook = xlrd.open_workbook('testdat/students.xls')
    sheet1 = workbook.sheets()[0]
    data_list = sheet1.__dict__['_cell_values']
    data_list.pop(0)
    data_dict_list = []
    for _ in data_list:
        data_dict_list.append({'name': _[0], 'image': _[2]})
    # print(data_list, data_dict_list, sep='\n')
    return data_dict_list


if __name__ == '__main__':
    read_excel()
    view = view.View(return_dict())
    view.c_box.bind("<<ComboboxSelected>>", view.show)
    view.root.mainloop()
