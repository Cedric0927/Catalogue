# 导入读写pdf模块
from PyPDF2 import PdfFileReader, PdfFileWriter

'''
注意：
页数从0开始索引
range()是左闭右开区间
'''


def split_pdf(file_name, start_page, end_page, output_pdf):
    '''
    :param file_name:待分割的pdf文件名
    :param start_page: 执行分割的开始页数
    :param end_page: 执行分割的结束位页数
    :param output_pdf: 保存切割后的文件名
    '''
    # 读取待分割的pdf文件
    input_file = PdfFileReader(open(file_name, 'rb'))
    # 实例一个 PDF文件编写器
    output_file = PdfFileWriter()
    # 把分割的文件添加在一起
    for i in range(start_page, end_page):
        output_file.addPage(input_file.getPage(i))
    # 将分割的文件输出保存
    with open(output_pdf, 'wb') as f:
        output_file.write(f)


if __name__ == '__main__':
    # 分割pdf
    split_pdf(
        r"C:\Users\Cedric.Niu\Desktop\catalog\参考材料\2022-Huawei-Antenna-Products-Catalogue.pdf",
        161, 163,
        r"C:\Users\Cedric.Niu\Desktop\catalog\参考材料\result.pdf")

