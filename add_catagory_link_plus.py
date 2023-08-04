import os

import pdfplumber
from PyPDF2 import PdfReader as Reader, PdfWriter as Writer
from PyPDF2.generic import RectangleObject

pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test1.pdf'
pdf = pdfplumber.open(pdf_path)
page = pdf.pages[0]
# print(words)

pdf_in = Reader(pdf_path)
pdf_out = Writer()

pageCount = pdf_in.getNumPages()
page_one = pdf_in.getPage(1)
page_one.extract_text()
print(1)
for each in range(pageCount):
    pdf_out.addPage(pdf_in.getPage(each))

height = page.height
catalog_pages = [12, 13, 14, 170, 171, 253, 270, 346]
antenna_appendix = [359, 366, 375]
tolerance = 10
for num in range(pageCount):
    if num in catalog_pages:
        page = pdf.pages[num]
        original_words = page.extract_words()
        words = [each for each in original_words if int(each.get('x0')) > 535]
        words = [each for each in words if each.get('text').isdigit()]
        spec_words = [each for each in original_words if int(each.get('x0')) < 80 and int(each.get('top')) > 70]
        for num_1, word in enumerate(words):
            pdf_out.addLink(num, int(word.get('text')), RectangleObject(
                (word.get('x0') - tolerance,
                 height - word.get('bottom') - tolerance,
                 word.get('x1') + tolerance,
                 height - word.get('top') + tolerance)))
            pdf_out.addLink(num, int(word.get('text')), RectangleObject(
                (spec_words[num_1].get('x0') - tolerance,
                 height - spec_words[num_1].get('bottom') - tolerance,
                 spec_words[num_1].get('x1') + tolerance,
                 height - spec_words[num_1].get('top') + tolerance)))
    elif num == 11:
        page = pdf.pages[num]
        words = page.extract_words()
        words = [each for each in words if int(each.get('x0')) > 480]
        for word in words:
            pdf_out.addLink(num, int(word.get('text')), RectangleObject(
                (word.get('x0') - tolerance * 2,
                 height - word.get('bottom') - tolerance,
                 word.get('x1') + tolerance * 2,
                 height - word.get('top') + tolerance)))
    elif num in antenna_appendix:
        page = pdf.pages[num]
        original_words = page.extract_words()
        words = [each for each in original_words if int(each.get('x0')) > 400]
        words = [each for each in words if each.get('text').isdigit()]
        spec_words = [each for each in original_words if int(each.get('x0')) < 80 and int(each.get('top')) > 70]
        for num_1, word in enumerate(words):
            pdf_out.addLink(num, int(word.get('text')), RectangleObject(
                (word.get('x0') - tolerance,
                 height - word.get('bottom') - tolerance,
                 word.get('x1') + tolerance,
                 height - word.get('top') + tolerance)))
            pdf_out.addLink(num, int(word.get('text')), RectangleObject(
                (spec_words[num_1].get('x0') - tolerance,
                 height - spec_words[num_1].get('bottom') - tolerance,
                 spec_words[num_1].get('x1') + tolerance,
                 height - spec_words[num_1].get('top') + tolerance)))

out_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test2.pdf'

with open(out_path, 'wb') as f:
    pdf_out.write(f)

os.popen(out_path)
