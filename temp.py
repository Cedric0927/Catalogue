import os
from PyPDF2 import PdfFileMerger

index = 5
target_path = r'C:\Users\Cedric.Niu\Desktop\catalog\total'  ## pdf目录文件
# target_path = r'C:\Users\Cedric.Niu\Desktop\catalog\BRACKET'  ## pdf目录文件

pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
# pdf_lst = sorted(pdf_lst, key=lambda x: int(x.split('@')[0]))
# pdf_lst = sorted(pdf_lst, key=lambda x: int(x.split('.')[0]))
pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]


file_merger = PdfFileMerger()
for pdf in pdf_lst:
    file_merger.append(pdf,import_bookmarks=False)     # 合并pdf文件


file_merger.write(r'C:\Users\Cedric.Niu\Desktop\catalog\total\total.pdf')
# file_merger.write(r'C:\Users\Cedric.Niu\Desktop\catalog\BRACKET\BRACKET.pdf')
