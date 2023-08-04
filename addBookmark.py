import os

from PyPDF2 import PdfReader as Reader, PdfWriter as Writer


pdf_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test2.pdf'

pdf_in = Reader(pdf_path)
pdf_out = Writer()
pageCount = pdf_in.getNumPages()
for each in range(pageCount):
    pdf_out.addPage(pdf_in.getPage(each))

catalog_pages = [11, 12, 170, 253, 270, 346, 359, 366, 375]
name = [
    'Product Category',
    'Single-MultiBand Antennas',
    'Multi-Beam Hybrid Antennas',
    'TDD Beamforming Antennas',
    'FDD+TDD Hybrid Antennas',
    'Small Cell Antennas',
    'AISG',
    'RET system',
    'Bracket & Installation Guide'
]
for num, page in enumerate(catalog_pages):
    pdf_out.addBookmark(name[num], page, parent=None)

out_path = r'C:\Users\Cedric.Niu\Desktop\catalog\test3.pdf'

with open(out_path, 'wb') as f:
    pdf_out.write(f)

os.popen(out_path)