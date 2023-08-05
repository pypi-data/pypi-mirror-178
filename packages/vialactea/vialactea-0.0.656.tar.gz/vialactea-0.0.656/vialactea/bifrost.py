import os
import winshell
import shutil


class Bifrost:
    c_user = os.environ['userprofile']
    local_appdata = os.environ['localappdata']
    tmp = os.environ['tmp']
    desktop = winshell.desktop()
    vialactea_in_dir = os.path.dirname(__file__)

    vialactea_dir = os.path.join(local_appdata, 'vialactea')
    vialactea_import = os.path.join(vialactea_dir, 'import')
    vialactea_export = os.path.join(vialactea_dir, 'export')
    vialactea_log = os.path.join(vialactea_dir, 'log')

    nav_dir = os.path.join(desktop, 'ViaLactea Navigation')

    PERSIST_DIRECTORIES = [
        nav_dir,
        vialactea_dir,
        vialactea_import,
        vialactea_export,
        vialactea_log
    ]

    NAV_DIR_LINKS = [
        vialactea_dir,
        vialactea_import,
        vialactea_export,
        vialactea_log
    ]

    def persist(self):
        
        try:

            for persist_dir in self.PERSIST_DIRECTORIES:
                if os.path.exists(persist_dir):
                    pass
                else:
                    os.makedirs(persist_dir)

            
            for dest in self.NAV_DIR_LINKS:
                link_filepath = os.path.join(self.nav_dir, f'{os.path.basename(dest)}.lnk')
                with winshell.shortcut(link_filepath) as link:
                    link.path = dest
        
        except Exception as e:
            print('Something went wrong ', e)


__bifrost: Bifrost = Bifrost()
