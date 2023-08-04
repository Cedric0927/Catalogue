import base64
import os.path
import re

path = r'C:\Users\Cedric.Niu\Desktop\catalog\@spec1\1@Single-MultiBand Antenna Spec\1@GC-21_A.html'


def get_all_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    res = re.findall('<td rowspan="2">.*?\d/(\d).*?</td>', content)

    # print(res[0])
    return int(res[0])


def replace_html(file_path, target, page):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r"""<div\sclass="all-footer">"""
    res = re.findall(pattern, content)
    # print(res)

    new_footer = """
                <div class="all-footer">
                    <table>
                        <tr>
                            <td width="80%"><a href="#{}"><p class="catalog_page">catalog_page_num</p></a></td>
                            <td><a href="#catalog_list_{}"><div class="b1"></div></a></td>
                            <td><a href="#product_category"><div class="b2"></div></a></td>
                        </tr>
                    </table>
                </div>
                """.format(os.path.basename(file_path)[:-5], target)
    pattern = r"""<div\sclass="all-footer">.*?</div>"""
    content = re.sub(pattern, new_footer, content, flags=re.S)
    for each in range(len(res)):
        content = content.replace('catalog_page_num', f'{page + each}', 1)
    content = re.sub(r'alert.*?\)', '', content, flags=re.S)
    # print(content)
    new_css = """
		.catalog_page {
			padding-left: 62%;
			font: 15px Arial;
			color: black;
			padding-bottom: 30px;
			opacity: 80%;
		}

		.b1 {
			background-image: url("C:/Users/Cedric.Niu/Desktop/catalog/photo/Product List.svg");
			height: 59px;
			width: 79px;
			background-repeat: no-repeat;
			margin-right: 6.5px;
			margin-bottom: -2px;
		}	
		.b2 {
			background-image: url("C:/Users/Cedric.Niu/Desktop/catalog/photo/Product Category.svg");
			height: 59px;
			width: 77px;
			background-repeat: no-repeat;
			margin-bottom: -2px;
		}
        </style>
    """
    content = content.replace('</style>', new_css)
    new_css_page = """
        * {
            box-sizing: border-box;
        }
        body {
			margin: 0 auto;
			padding: 0;
			background: rgb(204, 204, 204);
			display: flex;
			flex-direction: column;
		}
        @page {
			size: A4;
			margin: 0;
		}
        .page {
            padding-left: 20px;
            padding-right: 20px;
            padding-top: 15px;
			display: inline-block;
			position: relative;
			height: 297mm;
			width: 210mm;
			font-size: 12pt;
			box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
			background: white;
        }
        @media print {
        	.page {
        		margin: 0;
        		overflow: hidden;
        	}
        
    """
    content = re.sub(r'\.page.*?always;', new_css_page, content, flags=re.S)
    content = content.replace('color: rebeccapurple;', 'background-size:  100% 100%;', 1)
    # photo_base64(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return page + len(res)


def photo_base64(html):
    pattern_1 = r'url\((.*?)\)'
    photos_1 = re.findall(pattern_1, html)

    def to_base64(path):
        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data

    for photo in photos_1:
        if "otf" in photo:
            continue
        try:
            photo_base64 = to_base64(photo)
            new_photo = "data:image/svg+xml;base64,{}".format(str(photo_base64, encoding="utf-8"))
            html = html.replace(photo, new_photo, 1)
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("File not found")
    return html


if __name__ == '__main__':
    replace_html(path, '', 123)
    # print(get_all_page(r'C:\Users\Cedric.Niu\Desktop\catalog\@spec\1@Single-MultiBand Antenna Spec\9@GWF-21_A.html'))
