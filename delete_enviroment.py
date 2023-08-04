import os

orc_str = ' For environmental information, please refer to <a href="https://www.rosenbergertechnologies.com/Company.html?id=16">https://www.rosenbergertechnologies.com/Company.html?id=16</a>'

folder = os.walk(r"C:\Users\Cedric.Niu\Desktop\catalog\@spec1")
for path, dir_list, file_list in folder:
    for each in file_list:
        file_path = os.path.join(path, each)
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            if orc_str in html:
                html = html.replace(orc_str, '')
            else:
                print(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)