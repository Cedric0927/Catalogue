import os
import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QListWidgetItem, QTreeWidgetItem, QFileSystemModel

from UI import Ui_MainWindow
from getdate import GetDate
from replace_ import replace_html


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.select_folder_path = ''
        self.spec_files = {}

        self.slot()

    def slot(self):
        self.ui.pushButton.clicked.connect(self.import_file)

    def import_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Open',
                                                       r"C:\Users\Cedric.Niu\Desktop\before\catalog\@spec")
        if not folder_path:
            return
        self.select_folder_path = folder_path
        folder = os.walk(folder_path)
        for path, dir_list, file_list in folder:
            if path and file_list:
                folder_name = os.path.basename(path)
                file_list = [each for each in file_list if each.endswith('.html')]
                self.spec_files[folder_name] = file_list

        model = QFileSystemModel()
        model.setRootPath(self.select_folder_path)
        self.ui.treeView.setModel(model)
        self.ui.treeView.setRootIndex(model.index(self.select_folder_path))

    def create_table(self):
        start_page = self.ui.lineEdit.text()
        for folder, files in self.spec_files.items():
            for each_file in files:
                data = get_spec_data(each_file)

    def replace_html(self):
        replace_html()


def get_spec_data(file):
    data = {
        'Port': '',
        'Antenna Type': '',
        'Frequency': '',
        'Gain': '',
        'Hbw': '',
        'Dimension': '',
        'Page': ''
    }
    get_data = GetDate(file)
    base_info = get_data.get_heading()
    data['Name'] = base_info[0]
    data['Port'] = base_info[1]
    data['Antenna Type'] = base_info[2]
    mechanical = get_data.mechanical()
    for num, each in enumerate(mechanical):
        if each == 'Antenna Dimensions (H x W x D)':
            antenna_dimensions = mechanical[num + 1][:-3]
            data['Dimension'] = antenna_dimensions
    all_value, all_value_tag, all_fre, fre = get_data.electrical_base()
    data['Frequency'] = [f'{each[0]} x {each[1]}' for each in all_fre]
    gain_mid, gain_all, gain_ry_temp = get_data.gain()
    max_gain_list = []
    for num, each_fre in enumerate(all_fre):
        gain_list = gain_all[:int(each_fre[0])]
        gain_format = []
        for gain in gain_list:
            if '±' in gain:
                gain_format.append(float(gain.split('±')[0]))
            else:
                gain_format.append(float(gain))
        max_gain = max(gain_format)
        max_gain_list.append(max_gain)
        del gain_all[:int(each_fre[0])]
    max_gain_list = [str(max_gain) for max_gain in max_gain_list]
    max_gain_str = '<br/>'.join(max_gain_list)
    data['Gain'] = max_gain_str
    hbw = []
    for each in all_value:
        if 'Azimuth' in each or 'Horizontal' in each[0]:
            for each_value in each[1:]:
                if '±' in each_value:
                    each_value = each_value.split('±')[0]
                if 60 < int(each_value) < 70:
                    hbw.append('65')
                elif 15 < int(each_value) < 25:
                    hbw.append('22')
                elif 30 < int(each_value) < 40:
                    hbw.append('33')
                elif 85 < int(each_value) < 95:
                    hbw.append('90')
                elif 95 < int(each_value) < 105:
                    hbw.append('100')
                elif 350 < int(each_value) < 361:
                    hbw.append('360')
            break
    hbw = set(hbw) if hbw else ['']
    hbw_str = '-'.join(hbw)
    data['Hbw'] = hbw_str
    return data


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # my_app = App()
    # my_app.show()
    # sys.exit(app.exec())
    # my_app.spec_files = [
    #     r'C:\Users\Cedric.Niu\Desktop\before\catalog\@spec\1@Single-MultiBand Antenna Spec\1@GC-21_A.html']
    # my_app.create_table()
    get_spec_data(
        r'C:\Users\Cedric.Niu\Desktop\before\catalog\@spec\1@Single-MultiBand Antenna Spec\1@GC-21_A.html'
    )
