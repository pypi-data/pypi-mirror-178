import json
import os
from datetime import datetime
import math
import time
import pandas as pd
import qrcode
import qrcode.image.svg
from vialactea.feed import Notifications
from vialactea.bifrost import __bifrost, bifrost_import, bifrost_export



notif = Notifications()

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class report:
    def __init__(self):
        self._path = os.path.join(__bifrost.vialactea_log, 'log.txt')

        if os.path.exists(self._path):
            pass
        else:
            with open(self._path, 'w', encoding='utf-8') as f:
                f.write('Sirius Tech. Studio, 2022\n')
                f.write(f'{"="*100}\n')
                f.write(f'[{datetime.now():%d/%m/%Y %H:%M:%S}];NOTIFICATION;Log file created\n')
        with open(self._path, 'r', encoding='utf-8') as f:
            self.file = f.read()

    def reload(self):
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(self.file)
        with open(self._path, 'r', encoding='utf-8') as f:
            self.file = f.read()

    def set_value(self, text):
        self.file += f'{"=" * 100}\n'
        self.file += f'[{datetime.now():%d/%m/%Y %H:%M:%S}];{text}\n'
        self.reload()

    @staticmethod
    def describe_dir(target_dir):
        """
        Generates report with Name, Date, Type and Size
        :param target_dir:
        :return:
        """
        report_headers = ['File Name', 'Last Date Modified', 'Extension', 'Size']
        report_content = []
        file__name_tosave = ''.join(
            [
                __bifrost.vialactea_export,
                target_dir.split('/')[-2].upper(),
                '_DESCRIPTION_REPORT.csv'
            ]
        )

        if os.path.isdir(target_dir):
            list_dir = os.listdir(target_dir)

            for file in list_dir:
                file_path = f'{target_dir}/{file}'
                _ = list()
                _.append(file)
                _.append(time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.path.getctime(file_path)))))
                _.append(file.split('.')[-1])
                _.append(convert_size(os.path.getsize(file_path)))
                report_content.append(_)

            df = pd.DataFrame(data=report_content, columns=report_headers)
            df.to_csv(file__name_tosave, index=False, sep=';')


class Studio:
    def __init__(self):
        self._path = __bifrost.vialactea_dir

    class tools:
        def __init__(self):
            pass

        @staticmethod
        def validate_path(target_dir):

            if os.path.isdir(target_dir):
                return {'type': 'dir', 'content': target_dir}
            elif os.path.isfile(target_dir):
                return {'type': 'file', 'content': target_dir}
            else:
                return {'type': 'unknown', 'content': target_dir}

        def dir_handler(self, target_dir):
            if self.validate_path(target_dir)['type'] == 'dir':
                return {'type': 'handler', 'path': target_dir, 'content': os.listdir(target_dir)}
            else:
                print(f'Error {target_dir} is not a dir.')

        @staticmethod
        def list_textfilter(target_list: list, inFilter=' ', outFilter=' '):
            """
            Filter a list using in and out arguments.
            inFilter is for include the param
            outFilter is when you want to exclude the param from the current list
            IMPORTANT! This does not cover all regex structures
            :param target_list:
            :param inFilter:
            :param outFilter:
            :return:
            """
            # todo COLOCAR O UPPER E CHECAR DE FOI PASSADO ''
            
            print(notif.FUNC_UNDER_MAINTENANCE)

            out_target_list = []
            in_target_list = []

            for out_list_item in target_list:
                if outFilter in out_list_item:
                    pass
                else:
                    out_target_list.append(out_list_item)

            for _list_item in out_target_list:
                if inFilter in _list_item:
                    in_target_list.append(_list_item)
                else:
                    pass

            return in_target_list


    class qr(qrcode.QRCode):

        import_default_file = 'qr_src.txt'
        _IMPORT_SRC_ = os.path.join(bifrost_import, import_default_file)
        _EXPORT_SRC_ = 'downloads\\siriusqr\\'
        _IMG_TYPE_FACTORY_ = qrcode.image.svg.SvgImage
        _IMG_TYPE_EXTENSION = 'svg'

        def __init__(self):
            super().__init__()
            self.import_src = self._IMPORT_SRC_
            self.export_src = os.path.join(os.path.expanduser('~'), self._EXPORT_SRC_)
            self.version = 4
            self.error_correction = qrcode.constants.ERROR_CORRECT_M
            self.box_size = 50
            self.border = 3
            self.current_data = ''

            if os.path.isdir(self.export_src):
                pass
            else:
                os.makedirs(self.export_src)

        def set_version(self, version_value):

            if isinstance(version_value, int):
                if version_value >= 1 <= 44:
                    self.version = version_value
                else:
                    self.version = 4
                    print(
                        'You tried to set an version param that is out of its bounds.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')
            elif isinstance(version_value, float):
                if int(version_value) >= 1 <= 44:
                    self.version = int(version_value)
                    print(
                        'Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
                else:
                    self.version = 4
                    print(
                        'You tried to set an version param that is out of its bounds.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')
            else:
                self.version = 4
                print(
                    'You tried to set an non-numeric argument.\nYou should try an integer value between 1 till 44.\nLimit was set to application default (4)')

        def get_version(self):
            return self.version

        def set_error_c(self, acc_lvl: str):
            """
            Accuracy error treatment  you can set low, medium, quarter or high if anything different from the known arguments is passed, bifrost will set medium acc_error lvl as default
            :param acc_lvl:
            :return:
            """
            match acc_lvl:
                case 'low':
                    self.error_correction = qrcode.constants.ERROR_CORRECT_L
                case 'medium':
                    self.error_correction = qrcode.constants.ERROR_CORRECT_M
                case 'quarter':
                    self.error_correction = qrcode.constants.ERROR_CORRECT_Q
                case 'high':
                    self.error_correction = qrcode.constants.ERROR_CORRECT_H
                case _:
                    self.error_correction = qrcode.constants.ERROR_CORRECT_M
                    raise KeyError(
                        'The argument for accuracy error does not match with any option supported.\n In that case, error accuracy was set to medium (default) level')

        def get_error_c(self):
            return self.error_correction

        def set_box_size(self, pixels=10):
            """
            The box_size parameter controls how many pixels each “box” of the QR code is
            :param pixels:
            :return:
            """
            if isinstance(pixels, int):
                self.box_size = pixels
            elif isinstance(pixels, float):
                self.box_size = int(pixels)
                raise Warning(
                    'Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
            else:
                self.box_size = 10
                raise TypeError(
                    f'Bifrost could not apply {pixels} value because is not an numeric type. Box_size was set do default value (10)')

        def get_box_size(self):
            return self.box_size

        def set_border(self, boxes):
            box_warning = 'Boxes default is 4, according to specs.\nYou should work with that value'
            if isinstance(boxes, int):
                self.border = boxes
                raise Warning(box_warning)
            elif isinstance(boxes, float):
                self.border = int(boxes)
                print(
                    'Float type was catch in pixels param and should not be used.\npixels param was applied using int method')
                raise Warning(box_warning)
            else:
                self.border = 4
                raise TypeError(
                    f'Bifrost could not apply {boxes} value because is not an numeric type. border was set do default value (4)')

        def get_border(self):
            return self.border

        def read_import(self):
            return open(self.import_src, 'r').readlines()

        def set_data(self, text_value: str):
            self.current_data = text_value
            self.add_data(text_value)

        def reset_data(self):
            self.clear()
            self.current_data = ''

        def create(self):
            """Create an QR Code according to current_data content"""
            img = self.make_image(image_factory=self._IMG_TYPE_FACTORY_)
            if self.current_data == '' or None:
                self.current_data = str(datetime.now().strftime('%d%m%Y%I%M%S%p'))
            img.save(f'{self.export_src}{self.current_data}.{self._IMG_TYPE_EXTENSION}')

        def set_importsrc(self, path_to_importsrc):
            """
            The paths must be a valid .txt file
            :param path_to_importsrc:
            :return:
            """
            if os.path.isfile(path_to_importsrc):
                if path_to_importsrc.lower().endswith('.txt'):
                    self.import_src = path_to_importsrc
                else:
                    print(f'{path_to_importsrc} could not be assigned as import src')

        def create_from_import(self):
            lines = self.read_import()

            for line in lines:
                print('Save as')
                file_name = input('Name: ')
                self.set_data(text_value=line.rstrip())
                img = self.make_image(image_factory=self._IMG_TYPE_FACTORY_)

                if self.current_data == '' or None:
                    self.current_data = str(datetime.now().strftime('%d%m%Y%I%M%S%p'))
                img.save(f'{self.export_src}{file_name}{self.get_version()}V.{self._IMG_TYPE_EXTENSION}')
                self.reset_data()
