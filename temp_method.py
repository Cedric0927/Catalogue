import os
import re

from replace_ import replace_html, get_all_page

cata_path = r'C:\Users\Cedric.Niu\Desktop\catalog.html'
spec_path = r'C:\Users\Cedric.Niu\Desktop\catalog\@spec1'
with open(cata_path, 'r', encoding='utf-8') as f:
    html = f.read()

spec_list = []
folder = os.walk(spec_path)
for path, dir_list, file_list in folder:
    if file_list:
        spec_list.append(path)
        spec_list.append(file_list)

spec_pages = [15, 172, 254, 271, 347]
for num, each in enumerate(spec_list):
    if num % 2 == 0:
        page = spec_pages[num // 2]
        spec_folder = sorted(spec_list[num + 1], key=lambda x: int(x.split('@')[0]))
        for file in spec_folder:
            file_path = os.path.join(each, file)
            page = replace_html(file_path, '', page)
