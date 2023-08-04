import os

from PyPDF2 import PdfReader as Reader, PdfWriter as Writer
from PyPDF2.generic import RectangleObject

pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test.pdf'
pdf_in = Reader(pdf_path)
pdf_out = Writer()

pageCount = pdf_in.getNumPages()
for each in range(pageCount):
    pdf_out.addPage(pdf_in.getPage(each))

pdf_out.addLink(0, 1, RectangleObject((455, 0, 515, 44.5)))
pdf_out.addLink(0, 2, RectangleObject((521, 0, 579, 44.5)))

out_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test1.pdf'

with open(out_path, 'wb') as f:
    pdf_out.write(f)

os.popen(out_path)