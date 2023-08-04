import os
import re

import openpyxl

from catalog import analysis_col, table_end, HTML, create_new_table
from replace_ import replace_html, get_all_page

html = ""

# 总目录
# with open('all_cata.html', 'r', encoding='utf-8') as f:
#     html += f.read()
# html += r"""<iframe id="all_catalog" src="D:\PythonProject\Practise\catalog\all_cata.html" frameborder="0" width="100%" height="1122.520px" scrolling="no"></iframe>"""
html += HTML
# 分目录循环
excel_path = r'C:\Users\Cedric.Niu\Desktop\网站规格书列表转目录用---0822.xlsx'
result_html = r'C:\Users\Cedric.Niu\Desktop\result.html'
spec_path = r'C:\Users\Cedric.Niu\Desktop\catalog\@spec1'
folder = os.walk(spec_path)
spec_list = []
for path, dir_list, file_list in folder:
    if path == spec_path or not file_list:
        continue
    spec_list.append(path)
    spec_list.append(file_list)
wb = openpyxl.load_workbook(excel_path)
all_table = wb.sheetnames
page_2 = False
for num, table in enumerate(all_table):
    html += create_new_table(table, page_2)
    html += analysis_col(wb[table])
    html += table_end()

    # 规格书
    for num1, each in enumerate(sorted(spec_list[num * 2 + 1], key=lambda x: int(x.split('@')[0]))):
        path = os.path.join(spec_list[num * 2], each)
        pattern = r"""<td><a.href="#%s">(\d{1,3})</a></td>""" % (each.split('_')[0].split('@')[1])
        page = re.findall(pattern, html, re.S)
        height = get_all_page(path) * 29.7
        replace_html(path, '', int(page[0]))
        html += r"""
        <iframe id="{}" src="{}" frameborder="0" width="100%" style="height:{}cm" scrolling="no"></iframe>
        """.format(each.split('_')[0].split('@')[1], path, height)
    page_2 = True

    # print(html)
with open(result_html, 'w', encoding='utf-8') as f:
    f.write(html)
    os.popen(result_html)
