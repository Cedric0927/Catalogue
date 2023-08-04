import os

from PyPDF2 import PdfReader as Reader, PdfWriter as Writer
from PyPDF2.generic import RectangleObject
import pdfplumber

# pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test.pdf'
# pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\res\all.pdf'
pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\total\total.pdf'

pdf_in = Reader(pdf_path)
pdf_out = Writer()

pageCount = pdf_in.getNumPages()
page_one = pdf_in.getPage(1)
# page_one_text = page_one.extractText()
# txt_split = page_one_text.split('\n')
# print(txt_split)
#
for each in range(pageCount):
    pdf_out.addPage(pdf_in.getPage(each))

catalog_page_list = []
catalog_page = 0
spec_page = 0
# for page in range(1, pageCount):
#     content = pdf_in.getPage(page).extract_text()
#     if 'Product Number' in content or 'Gain(dBi)' in content:
#         catalog_page = page
#         if catalog_page_list and page - catalog_page_list[-1][0] < 5:
#             catalog_page_list[-1].append(page)
#         else:
#             catalog_page_list.append([page])
# else:
#     pdf_out.addLink(0, 1, RectangleObject((455, 0, 515, 44.5)))
#     pdf_out.addLink(0, 2, RectangleObject((521, 0, 579, 44.5)))
#     spec_page += 1
#     if spec_page

catalog_pages = [12, 13, 14, 170, 171, 253, 270, 346]
spec_pages = [69, 123, 172, 229, 254, 271, 347, 400]
for page in range(1, pageCount):
    if page + 11 in catalog_pages:
        pdf_out.addLink(page, 0, RectangleObject((521, 0, 579, 44.5)))

    else:
        for num, each in enumerate(spec_pages):
            if page + 11 < each:
                link_page = catalog_pages[num]
                break
        pdf_out.addLink(page, link_page - 11, RectangleObject((455, 0, 515, 44.5)))
        pdf_out.addLink(page, 0, RectangleObject((521, 0, 579, 44.5)))
out_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test1.pdf'

with open(out_path, 'wb') as f:
    pdf_out.write(f)

os.popen(out_path)

# path = r'C:\Users\Cedric.Niu\Desktop\catalog\res\all.pdf'
# p = pdfplumber.open(path)
#
# a = p.pages[0].extract_words()
# print()
