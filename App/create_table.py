import os
import re


from replace_ import get_all_page

excel_path = r'C:\Users\Cedric.Niu\Desktop\网站规格书列表转目录用---0822.xlsx'
result_html = r'C:\Users\Cedric.Niu\Desktop\catalog.html'


PAGE = 15
PAGE2 = 13
HTML = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
	</head>
	<style>
        * {
			margin: 0;
			font-family:arial;
			border-spacing: 0;
			box-sizing: border-box;
		}
		a{
		text-decoration: none;
		color: black;
		}
        body {
			margin: 0 auto;
			padding: 0;
			background: rgb(204, 204, 204);
			display: flex;
			flex-direction: column;
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
			margin: 0.5cm auto;
			box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
			background: white;
        }
        @media print {
        	.page {
        		margin: 0;
        		overflow: hidden;
        	}
        }
        @page {
			size: A4;
			margin: 0;
		}
		.catalog{
		    width: 94%;
		    border-collapse: collapse;
			margin: 0 3% 0 3%;
			page-break-before: always;
		}

		.catalog caption{
		    font-size: 20px;
		    color: rgb(50, 138, 202);
		    margin: 1em 0;
			text-align: left;
		}

		.catalog th,td{
		    border: 1px solid #999;
		    text-align: center;
		    padding: 14px 0;
		    font-size: 10px;
            border: none;
			border-bottom: 0.5px solid ;
		}

		.catalog thead tr{
		    background-color: rgb(24, 57, 95);
		    color: #fff;
		}

		.catalog tbody tr:nth-child(odd){
		    /* background-color: #eee; */
		}

		.catalog tbody tr:hover{
		    background-color: #ccc;
		}

		.catalog tbody tr td:first-child{
		    /* color: #f40; */
		}
		.catalog tbody tr td:nth-child(4){

		}
		.catalog tfoot tr td{
		    text-align: right;
		    padding-right: 20px;
		}
		.catalog_page {
			padding-left: 25%;
			font: 15px Arial;
			color: black;
			padding-bottom: 13px;
			opacity: 80%;
		}
        .all-footer {
            position: absolute;
            bottom: 0;
            width: 95%;       
        }
        iframe {
        page-break-before: always;
        }
		.b2 {
			background-image: url("C:/Users/Cedric.Niu/Desktop/catalog/photo/Product Category.svg");
			height: 59px;
			width: 77px;
			background-repeat: no-repeat;
            margin-bottom: -17px;
			margin-left: 74px;
		}
          .footer_table td{
			border: none;
		}
	</style>
		<body>
"""


def create_new_table(caption, current_page):
    content = """<div class="page">"""
    content += """

    <div class="all-footer">
        <table class="footer_table">
            <tr>
                <td width="80%"><p class="catalog_page">{}</p></td>
                <td><a href="#product_category"><div class="b2"></div></a></td>
            </tr>
        </table>
    </div>
    """.format(PAGE_2)
    content += "<table class ='catalog' >"
    content += "<caption>{}</caption>".format(caption)
    content += """
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Port</th>
                    <th>Antenna Type</th>
                    <th>Frequency(MHz)</th>
                    <th>Gain(dBi)</th>
                    <th>3dB HBW</th>
                    <th>L x W x D(mm)</th>
                    <th>Page</th>
                </tr>
            </thead>
            <tbody>"""
    return content


def analysis_col(ws):
    global PAGE
    row, count = 0, 1
    content = ""
    for col in range(2, 100):
        pn = ws['{}2'.format(get_column_letter(col))].value
        if not pn:
            break
        pn_list = pn.split('\n')
        port = ws['{}3'.format(get_column_letter(col))].value.replace(' port', '')
        description = ws['{}4'.format(get_column_letter(col))].value
        frequency = ws['{}5'.format(get_column_letter(col))].value
        frequency_str = frequency.replace('\n', '<br>')
        gain = ws['{}6'.format(get_column_letter(col))].value
        gain_list = str(gain).split('\n')
        hbw = ws['{}7'.format(get_column_letter(col))].value
        size = ws['{}8'.format(get_column_letter(col))].value
        size_list = size.split('\n')
        for num, pn in enumerate(pn_list):
            if len(gain_list) == 1:
                gain = gain_list[0]
            else:
                gain = gain_list[num]
            if len(size_list) == 1:
                size = size_list[0]
            else:
                size = size_list[num]
            content += """

            <tr>
            <td><a href="#{}">{}</a></td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td><a href="#{}">{}</a></td>
            </tr>
            """.format(pn.strip(), pn.strip(), port, description, frequency_str, gain, hbw, size, pn.strip(), PAGE)
            PAGE += get_all_page(os.path.join(
                r'C:\Users\Cedric.Niu\Desktop\catalog\spec',
                ws.title,
                pn.strip() + '.html'
            ))
            # count += 1
            row += 1
            if row == 18:
                content += table_end()
                content += create_new_table('', False)
                row = 0
    PAGE += 1

    return content

def table_end():
    content = """
    </tbody>
    </table>
    </div>
    """

    return content


def html_end():
    content = """
    </body>
    </html>
    """
    return content


if __name__ == '__main__':
    catalog_pages = [[12, 13, 14], [170, 171], [253], [270], [346]]
    spec_pages = [15, 172, 254, 271, 347]
    index = 3
    for index in range(0, 5):
        temp = HTML
        result_html = r'C:\Users\Cedric.Niu\Desktop\catalog\res\catalog{}.html'.format(index)
        PAGE_2 = catalog_pages[index][0]
        PAGE = spec_pages[index]
        for num, table in enumerate(all_table):
            if num == index:
                temp += create_new_table(table, PAGE_2)
                temp += analysis_col(wb[table])
                temp += table_end()
        temp += html_end()
        with open(result_html, 'w', encoding='utf-8') as f:
            f.write(temp)