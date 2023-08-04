import os


def catalog():
    path = r'C:\Users\Cedric.Niu\Desktop\catalog\@spec'

    folder = os.walk(path)
    for path, dir_list, file_list in folder:
        for each in file_list:
            if '#' in each:
                new_name = each.replace('#', '@')
                old_file_path = os.path.join(path, each)
                new_file_path = os.path.join(path, new_name)
                os.rename(old_file_path, new_file_path)


def german():
    path = r'D:\german\8FW8FW-65-8D-64K-11F-OD'
    folder = os.walk(path)
    for path, dir_list, file_list in folder:
        for each in file_list:
            new_name = each.replace('msi', 'txt')
            old_file_path = os.path.join(path, each)
            new_file_path = os.path.join(path, new_name)
            os.rename(old_file_path, new_file_path)


catalog()
