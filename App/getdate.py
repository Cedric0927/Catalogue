"""
@Time: 2021/1/5 9:14
@Author: Cedric
"""
import base64
import json
import os

from bs4 import BeautifulSoup
import re


class GetDate:
    def __init__(self, fn):
        self.fn = fn

        with open(fn, encoding='utf-8') as f:
            try:
                self.html = f.read()
            except UnicodeDecodeError:
                raise Exception('文件无法读取')

        self.soup = BeautifulSoup(self.html, 'lxml')
        self.initial_treatment()
        self.language = 'English'

        # 导入网页分割
        self.segmentation_html = {
            'fdd': '',
            'tdd': '',
            'nr': '',
        }
        segmentation_html_list = self.soup.find_all(attrs={'class': 'page'})
        for each_page in segmentation_html_list:
            each_page = str(each_page)
            if 'Horizontal Pattern' in each_page or '水平面方向图' in each_page:
                self.segmentation_html['fdd'] += each_page
            elif '5G NR Electrical Properties' in each_page:
                self.segmentation_html['nr'] += each_page
            elif 'tdd_table' in each_page or '单元波束' in each_page:
                self.segmentation_html['tdd'] += each_page
            elif 'Mechanical Data' in each_page:
                break

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def initial_treatment(self):
        self.html = self.html.replace('<br>', '')
        # 解决Polarization新旧规格书的单位导入问题
        self.html = self.html.replace('<td class="unit">°</td>', '<td class="unit" rowspan="1">°</td>')

    def get_heading(self):
        other_info = {
            'length_unit': 'm',
            'language': 'English',
            'usa': False
        }
        antenna_port = self.soup.find(attrs={'class': 'Antenna-port'}).get_text()
        # 中文无port
        if 'Antenna' in antenna_port:
            antenna_port = antenna_port.strip().split(' ')[0]

        antenna_name = self.soup.find(attrs={'class': 'Antenna-name'}).get_text()
        # print(antenna_port)
        # print(antenna_name)
        antenna_lh = self.soup.find(attrs={'class': 'Antenna-model'}).get_text().split('/')[0].strip()
        antenna_length = self.soup.find(attrs={'class': 'Antenna-model'}).get_text().split('/')[1].strip()
        if antenna_length.endswith('m'):
            antenna_length = antenna_length[:-1]
        elif antenna_length.endswith('ft'):
            antenna_length = antenna_length[:-2]
            other_info['length_unit'] = 'ft'

        # print(antenna_lh)
        # print(antenna_length)
        antenna_temp, antenna_list = [], []
        for each in self.soup.select('ul li'):
            antenna_temp.append(each.string)
        if None not in antenna_temp:
            for num, each in enumerate(antenna_temp):
                if each == antenna_temp[0] and num != 0:
                    break
                else:
                    each = each.replace('\n', ' ')
                    antenna_list.append(each)
            # print(antenna_list)

        # 版本
        pattern_list = [r'V\s{0,1}([A-Z]{0,1}\d.\d)</td>',
                        r'<td>V\s{0,1}([A-Z])</td>',
                        r'<td>\d\d\d\d.*?V\s{0,1}(.*?)</td>',
                        r'<span class="spec_version">(.*?)</span>']
        version = '0.0'
        for each_pattern in pattern_list:
            version = re.findall(each_pattern, self.html)
            if version:
                version = version[0]
                break

        # print(version)
        preliminary = False
        if '(Preliminary)' in self.html:
            preliminary = True

        if '1-888-840-4066' in self.html:
            other_info['usa'] = True

        if '辐射参数' in self.html:
            other_info['language'] = 'Chinese'
            self.language = 'Chinese'

        return [antenna_name, antenna_port, antenna_lh, antenna_length, antenna_list, version, preliminary, other_info]

    def check_fdd_tdd(self):
        fdd_state = False
        if 'Horizontal Pattern' in self.html or '水平面方向图' in self.html:
            fdd_state = True
        tdd_state = False
        nr_state = False
        if 'tdd_table' in self.html or '单元波束' in self.html:
            tdd_state = True
        if '5G NR Electrical Properties' in self.html:
            nr_state = True
        return fdd_state, tdd_state

    def electrical_base(self):
        fdd_html = self.segmentation_html['fdd']
        fdd_soup = BeautifulSoup(fdd_html, 'lxml')
        all_value, all_value_tag = [], []

        attributes = []
        find_attributes = self.soup.select('#ED-1 .Attributes')
        for each in find_attributes:
            attributes.append(each.get_text())

        for each in attributes[2:]:
            single_value, single_tag = [each], [each]
            each = each.replace('\n', ' ')
            each = each.replace(' ', '-')
            each = each.capitalize()
            if "Maximum-effective-power" in each:
                each = "Maximum-effective-power"
                temp_find = fdd_soup.findAll(attrs={'class': '{}'.format(each)})
                if not temp_find:
                    each = "Maximum-effective-power-per-port"
            temp_find = fdd_soup.findAll(attrs={'class': '{}'.format(each)})
            for each_1 in temp_find:
                single_value.append(each_1.get_text().strip())
                single_tag.append([each_1['colspan'], each_1.get_text().strip()])
            all_value.append(single_value)
            all_value_tag.append(single_tag)

        all_fre_pattern = r'<td class="fre\d" colspan="(\d)">(.*?)</td>'
        all_fre = re.findall(all_fre_pattern, fdd_html)
        # print(all_fre)
        fre_pattern = r'<td>(\d{3,4}-\d{3,4})</td>'
        fre = re.findall(fre_pattern, fdd_html)
        # print(fre)
        return all_value, all_value_tag, all_fre, fre

    def electrical_format(self):
        all_value_dict = {}
        _, electrical, all_fre, fre = self.electrical_base()
        for each_row in electrical:
            all_value_dict[each_row[0]] = []
            for each in each_row[1:]:
                for each_value in range(int(each[0])):
                    all_value_dict[each_row[0]].append(each[1])
        return all_value_dict

    def gain(self):
        fdd_html = self.segmentation_html['fdd']
        # gain
        gain_mid = []
        for each in range(1, 4):
            gain_temp = self.soup.select(f'.Gain-Mid-Tilt-{each}')
            for each_1 in gain_temp:
                gain_mid.append(each_1.get_text())
        gain_all = self.soup.select('.Over-All-Tilt')
        # gain_mid = [each.get_text() for each in gain_mid]
        gain_all = [each.get_text() for each in gain_all]

        gain_ry_pattern = r'<td class="Gain-Attributes" rowspan="\d">(.*?)</td>'
        gain_ry = re.findall(gain_ry_pattern, fdd_html)
        gain_ry_temp = []
        [gain_ry_temp.append(each.replace('<br/>', '')) for each in gain_ry]
        gain_ry = []
        for each in gain_ry_temp:
            if each not in gain_ry:
                gain_ry.append(each)
        gain_ry_temp = gain_ry

        # print(gain_ry_temp)
        return gain_mid, gain_all, gain_ry_temp

    def electrical(self):
        all_value, all_value_tag, all_fre, fre = self.electrical_base()
        # polarization
        polarization = all_value_tag[0]
        all_value.pop(0)
        all_value_tag.pop(0)
        gain_mid, gain_all, gain_ry_temp = self.gain()
        # fre_num
        fdd_fre_count = sum([int(each[0]) for each in all_fre])

        unit = []
        unit_pattern = r'<td\sclass="unit"\srowspan="(\d{1,2})">(.*?)</td>'
        find_unit = re.findall(unit_pattern, self.html)
        for each in find_unit:
            for num in range(int(each[0])):
                unit.append(each[1])

        if not gain_mid:
            gain_mid = ['' for each in gain_all]
            unit.insert(0, 'dBi')

        whole_power = self.get_whole_power()

        return all_fre, fre, fdd_fre_count, all_value, all_value_tag, unit, \
               [gain_mid, gain_all, gain_ry_temp], whole_power, polarization

    def get_whole_power(self):
        whole_power_pattern = '— Maximum Effective Power Whole Antenna: (.*)? W.'
        whole_power = re.findall(whole_power_pattern, self.html)
        return whole_power

    def tdd(self):
        tdd_value = []
        tdd_number = 0
        for each in range(1, 4):
            tdd_all_value = self.soup.select(f'#ED-{each} td')
            for each_value in tdd_all_value:
                tdd_value.append(each_value.get_text().strip())
            if 'Single column beam' in tdd_value:
                tdd_number = each
                break
            else:
                tdd_value = []
        # print(tdd_value)
        tdd_html = self.segmentation_html['tdd']
        tdd_soup = BeautifulSoup(tdd_html, 'lxml')

        tdd_pattern = r'<td class="fre\d" colspan="(\d)">(.*?)</td>'
        tdd_fre = re.findall(tdd_pattern, tdd_html)
        # print(tdd_fre)
        tdd_fre_count = sum([int(each[0]) for each in tdd_fre])
        # print(tdd_fre_count)
        fre_pattern = r'<td>(\d{3,4}-\d{3,4})</td>'
        fre = re.findall(fre_pattern, tdd_html)
        if not fre:
            fre = tdd_soup.select('.tdd_fre')
            fre = [each.get_text() for each in fre]
        attributes_html = tdd_soup.select('.Attributes')
        attributes = []
        all_value = []
        for each in attributes_html:
            attributes.append(each.get_text())
        for each in attributes[1:]:
            single_value = [each]
            each = each.replace(' ', '-')
            each = each.replace('\n', ' ')
            each = each.capitalize()
            temp_find = tdd_soup.findAll(attrs={'class': '{}'.format(each)})
            for each_1 in temp_find:
                single_value.append(each_1.get_text().strip())
            all_value.append(single_value)
        # print(all_value)
        unit = []
        unit_pattern = r'<td\sclass="unit"\srowspan="(\d)">(.*?)</td>'
        find_unit = re.findall(unit_pattern, tdd_html)
        for each in find_unit:
            for num in range(int(each[0])):
                unit.append(each[1])
        # print(unit)
        for num, each in enumerate(all_value):
            each.insert(1, unit[num])
        # print(all_value)

        repeat_value = {}
        for num, each in enumerate(all_value):
            if len(each) > tdd_fre_count + 2:
                if each[0] not in repeat_value.keys():
                    repeat_value[each[0]] = each[2:]
                all_value[num] = all_value[num][:2] + repeat_value[each[0]][:tdd_fre_count]
                for each_tdd in range(tdd_fre_count):
                    repeat_value[each[0]].pop(0)

        for num, each in enumerate(all_value):
            if num == 0 or each[2][0] not in ['>', '<']:
                all_value[num].insert(2, '/')
            else:
                # all_value[num + 1] = each[:-1] + [each[-1][2:]]
                all_value[num].insert(2, each[2][0])
        # print(all_value)
        whole_power_pattern = '— Maximum Effective Power Whole Antenna: (.*)? W.'
        whole_power = re.findall(whole_power_pattern, self.html)

        return tdd_fre, tdd_fre_count, fre, all_value, whole_power

    def gradient(self):
        gradient_html = self.soup.select('.segmentation')
        gradient_html_date = []
        for each in gradient_html:
            gradient_html_date.append(each.get_text())
        fdd_data, tdd_data = [], []
        if gradient_html_date:
            if 'VSWR' in gradient_html_date:
                vswr_index = gradient_html_date.index('VSWR')
                if len(gradient_html_date) > vswr_index + 1 and 'VSWR' in gradient_html_date[vswr_index + 1]:
                    vswr_index = gradient_html_date[vswr_index + 1:].index('VSWR') + vswr_index + 1
            elif '电压驻波比' in gradient_html_date:
                vswr_index = gradient_html_date.index('电压驻波比')
            else:
                vswr_index = -1
            # 应对用户改vswr
            temp = [each for each in gradient_html_date if '电压驻波比' in each]
            if temp and vswr_index == -1:
                vswr_index = gradient_html_date.index(temp[0])

            for num, each in enumerate(gradient_html_date):
                if num <= vswr_index:
                    fdd_data.append(each)
                else:
                    tdd_data.append(each)
        return fdd_data, tdd_data

    def nr(self):
        nr_info = {
            'state': False,
            'data': [],
            'all_fre': None,
            'sub_fre': []
        }
        if '5G NR Electrical Properties' in self.html:
            nr_info['state'] = True
            nr_pattern = r'<td class="nr-fre.*?" colspan="(\d)">(.*?)</td>'
            nr_fre = re.findall(nr_pattern, self.html)
            nr_info['all_fre'] = nr_fre
            nr_sub_fre = self.soup.select('.nr_sub_fre')
            for each in nr_sub_fre:
                nr_info['sub_fre'].append(each.get_text())

            nr_html = self.soup.select('#nr-table td')
            for each in nr_html:
                nr_info['data'].append(each.get_text())
        return nr_info

    def mechanical(self):
        mechanical_date_html = self.soup.select('#MD td')
        mechanical_date = []
        for each in mechanical_date_html:
            mechanical_date.append(each.get_text())
        # print(mechanical_date)
        return mechanical_date

    def mechanical_to_dict(self):
        md = self.mechanical()
        md_dict = {}
        for each in range(len(md)):
            if each % 3 == 0:
                md_dict[md[each]] = md[each + 1]
        return md_dict

    def layout(self):
        layout_data = {
            'data': [],
            'fix-tilt': False,
        }
        if '#layout-table' in self.html:
            layout_date_html = self.soup.select('#layout-table td')
            for each in layout_date_html:
                layout_data['data'].append(each.get_text())
            if self.soup.select('#layout-table') and self.soup.select('#layout-table')[0].get('class'):
                layout_data['fix-tilt'] = True
        return layout_data

    def accessories(self):
        accessories_html = self.soup.select('#Accessories-table td')
        accessories = []
        for each in accessories_html:
            accessories.append(each.get_text())
        # print(accessories)
        return accessories

    def pattern(self):
        pattern_td = self.soup.select('#Pattern td')
        pattern_fre = []
        for each in pattern_td:
            every_fre = each.get_text()
            if every_fre:
                every_fre = every_fre.split('-')
                pattern_fre.append(every_fre)
        return pattern_fre

    def tdd_pattern(self):
        tdd_info = {
            'state': False,
            'data': {},
            'model': []
        }
        if 'tdd_pattern_table' in self.html:
            tdd_info['state'] = True
            tdd_fre1 = self.soup.select('.tdd_pattern_1')
            for each in tdd_fre1:
                tdd_info['data']['fre1'] = each.get_text()
            tdd_fre2 = self.soup.select('.tdd_pattern_2')
            for each in tdd_fre2:
                tdd_info['data']['fre2'] = each.get_text()
            # if 'tdd_model1' in self.html:
            for each in range(self.html.count('tdd_model1')):
                tdd_info['model'].append(1)
            for each in range(self.html.count('tdd_model2')):
                tdd_info['model'].append(2)
        return tdd_info

    def ret(self):
        ret_info = {
            'state': False,
            'data': []
        }
        if 'id="RET"' in self.html:
            ret_info['state'] = True
            ret_html = self.soup.select('#RET td')
            for each in ret_html:
                ret_info['data'].append(each.get_text())
        return ret_info

    def decode(self):
        with open(self.fn, 'r', encoding='utf-8') as f:
            txt = f.read()
        soup = BeautifulSoup(txt, 'lxml')
        img_id = {
            'antenna_photo': '',
            'end_cap_photo': '',
            'array_diagram_photo': '',
            'appendix-photo': '',
        }

        # default_path = '../../photo_resource/Antenna_photo/antenna.jpg'
        default_path = os.path.join(
            os.path.abspath(os.path.join(os.getcwd(), "../../")), "photo_resource/Antenna_photo/antenna.jpg")

        with open(default_path, 'rb') as df:
            default_antenna_photo_base64 = str(base64.b64encode(df.read()), encoding='utf-8')
        for each in img_id:
            photo = soup.find(attrs={'id': each})
            if photo:
                photo_base64 = photo.get('src')
                if photo_base64 == 'data:image/png;base64,' + default_antenna_photo_base64:
                    continue
                photo_base64 = photo_base64.split(',')[1]
                img = base64.b64decode(photo_base64)
                img_id[each] = img
            else:
                continue
        return img_id

    def decode_pattern(self):
        with open(self.fn, 'r', encoding='utf-8') as f:
            txt = f.read()
        soup = BeautifulSoup(txt, 'lxml')

        photos = soup.findAll(attrs={'class': 'pattern_photo'})
        pattern_list = []
        for photo in photos:
            if photo and ('data' in str(photo)):
                photo_base64 = photo.get('src')
                photo_base64 = photo_base64.split(',')[1]
                img = base64.b64decode(photo_base64)
                pattern_list.append(img)
            else:
                continue
        return pattern_list

    def archive(self):
        item_info = {
            'state': False,
            'item': ''
        }
        if 'class="item"' in self.html:
            item_info['state'] = True
            all_item = self.soup.select('.item')
            for each in all_item:
                item_info['item'] = each.get_text()
                break
        return item_info

    def spec_info(self):
        pattern = r"alert.*?Author:\s(.*?).V.*?Remarks:.(.*?)['?]P?"
        result = re.findall(pattern, self.html)
        if result:
            result = [each.replace('\\', '') for each in result[0]]
            author, remark = result
        else:
            return ''
        pattern = r"alert.*?Previous.authors:\s(.*;)[']"
        previous_info = re.findall(pattern, self.html)
        if not previous_info:
            new_precious_author = '1 ' + author + ': ' + remark + ';'
        else:
            author_count = previous_info[0].count(';')
            new_precious_author = previous_info[0] + ' ' + str(author_count + 1) + '.' + author + ': ' + remark + ';'

        return new_precious_author

    def get_spec_info(self):
        pattern = r'alert\(.*?Author:\s(.*?)\\n.*Remarks:\s(.*?)\'\)'
        result = re.findall(pattern, self.html)
        return result

    def get_appendix(self):
        title = self.soup.select('#appendix-title')
        if title:
            title = title[0].get_text()
        else:
            return ''
        return title

    def get_gain_max(self):
        state = self.soup.select('.gain-max')
        if state:
            return True
        else:
            return False

    def get_logo(self):
        if 'heading-list-prose' in self.html:
            return True
        else:
            return False

    def get_layout_size(self):
        if 'float-l adjust-size' in self.html:
            return True
        else:
            return False

    def get_spec_alert(self):
        pattern = r"alert\('.*PN:\s(.*?)\\nA.*?Verify\sauthor:\s(.*?)\\nTime:\s(.*?)\\nVersion:\s(.*?)\\n.*?ks:\s(.*?)'\)"

        result = re.findall(pattern, self.html)
        if result:
            result = result[0]
            spec_alert = {
                'PN': result[0],
                'Version': result[3],
                'VerifyAuthor': result[1],
                'Time': result[2],
                'Remark': result[4]
            }
            return spec_alert
        else:
            return False

    def get_all_page(self):
        pattern = r'\d/(\d)</td>'
        result = re.findall(pattern, self.html)[0]
        return result

    def get_uid(self):
        result = re.findall(r'<!--UID:(\d{1,6})-->', self.html)[0]
        return result

    def get_vid(self):
        result = re.findall(r'<!--VID:(\d{1,6})-->', self.html)[0]
        return result

    def get_filename_de(self):
        de = re.findall(r'(_DE.?)\.', self.fn)
        if de:
            return de[0]
        else:
            return False

    def get_db_need_info(self):
        pn, port, description, length, heading_list, version, _, _ = self.get_heading()
        gain_mid, gain_all, gain_ry_temp = self.gain()
        gain = {
            'gain_mid': gain_mid,
            'gain_all': gain_all,
            'gain_ry_temp': gain_ry_temp,
        }
        all_value, all_value_tag, all_fre, fre = self.electrical_base()
        all_value_dict = {
            each[0].replace('\n', '').strip(): each[1:] for each in all_value
        }
        for key, value in all_value_dict.items():
            all_value_dict[key] = [each.strip() for each in value]
        info = {
            'spec_pn': pn,
            'spec_version': version,
            'spec_description': description,
            'spec_port': port,
            'spec_length': length,
            'spec_heading_list': json.dumps(heading_list),
            'spec_file_name': os.path.basename(self.fn),
            'spec_gain': json.dumps(gain),
            'spec_electrical': json.dumps(all_value_dict),
            'spec_mechanical': json.dumps(self.mechanical_to_dict()),
        }
        return info


if __name__ == '__main__':
    getdate = GetDate(r'D:/PythonProject/MagicalSpec3/spec/html/2G2J8XBD-27_A.html')
    getdate.nr()
