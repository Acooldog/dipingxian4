from typing import Optional
import configparser
import sys, os
import zipfile
import shutil

from log_maker import *

log = log_maker()

class ini_maker():

    def __init__(self) -> None:
        self.path = os.getcwd()

    def set_ini_value(self, file_name, title, key, new_value) -> None:
        
        '''
        有参无返
        更改配置文件内容
        参数：
            file_name：相对路径
            title：标题
            key：键
            new_value：新值
        '''

        config = configparser.ConfigParser()
        # 文件名称
        config.read(f'{self.path}\{file_name}')

        # 如果没有这个值，就创建
        if not config.has_section(title):
            config.add_section(title)

        config.set(title, key, new_value)

        with open(f'{file_name}', 'w', encoding='utf-8') as configfile:
            config.write(configfile)


    # 获取配置项内容
            # 文件名, 标题, 键
    def get_ini_value(self, file_name, title, key) -> str:
        
        '''
        有参有返
        读取配置文件内容
        参数：
            file_name：相对路径
            title：标题
            key：键
        '''

        config = configparser.ConfigParser()
        config.read(f'{self.path}\{file_name}', encoding='utf-8')

        value = config.get(title, key)
        return value


# 下载文件
class download_zip:
    def __init__(self) -> None:
        pass


# 查看配置文件清单是否与压缩包解压出的文件夹里面的文件一致, 一致就移动
class find_file_and_move_file:

    # 移动文件
    def move_file(self, source_file, destination_path) -> None:
        '''
        有参无返
        移动文件
        参数：
            source_file：相对路径
            destination_path：相对路径
        '''
        if not os.path.exists(source_file):
            print(f"Source file {source_file} does not exist. ---> 源文件不存在")
            return
        # 检查目标目录是否存在，如果不存在则创建
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            try:
                os.makedirs(destination_dir)
                print(f"Destination directory {destination_dir} has been created. ---> 创建成功")
            except Exception as e:
                print(f"Failed to create destination directory: {e} ---> 创建失败")
                return
        
        try:
            # shutil.move(source_file, destination_path)
            shutil.copy(source_file, destination_path)
            print(f"File {source_file} has been moved to {destination_path} successfully. ---> 移动成功")
        except PermissionError:
            print(f"Permission denied when moving file {source_file} to {destination_path}. ---> 移动失败")
        except Exception as e:
            print(f"An error occurred: {e} ---> 移动失败")

    # 找出PATH标头下所有的键，并整合为列表
    def find_all_path(self, file_path) -> Optional[list[str]]:

        '''
        
        有参有返
        找出PATH标头下所有的键，并整合为列表

        参数：
            file_path：相对路径

        返回：
            key_list：整合后的列表
        
        '''

        config = configparser.ConfigParser()
        config.read(file_path)
        if 'PATH' in config:
            path_section = config['PATH']
            key_list = []
            for key in path_section:
                key_list.append(key)
            return key_list
        else:
            return None

    # python遍历一个指定的文件夹，将它里面的所有元素: 文件夹和文件都整合为一个列表
    def list_directory_elements(self, directory) -> list[str]:

        '''
        
        有参有返
        python遍历一个指定的文件夹，将它里面的所有元素: 文件夹和文件都整合为一个列表

        参数：
            directory：指定的文件夹

        返回：
            elements：整合后的列表
        
        '''

        elements = []
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                elements.append(os.path.join(root, dir_name))
            for file_name in files:
                elements.append(os.path.join(root, file_name))
        return elements

    # 解压压缩包至指定文件夹
    def uncompress_archive(self, source_archive_path, destination_path) -> None:

        '''
        
        有参无返
        解压压缩包

        参数：
            source_archive_path：压缩包路径
            destination_path：解压路径
        
        '''

        # 确保目标路径存在
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        with zipfile.ZipFile(source_archive_path, 'r') as zip_ref:
            for name in zip_ref.namelist():
                try:
                    decoded_name = name.encode('cp437').decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        decoded_name = name.encode('cp437').decode('gbk')
                    except UnicodeDecodeError:
                        decoded_name = name
                extract_path = os.path.join(destination_path, decoded_name)
                zip_ref.extract(name, destination_path)
                if name!= decoded_name:
                    old_path = os.path.join(destination_path, name)
                    # 如果目标文件已存在，进行覆盖
                    if os.path.exists(extract_path):
                        os.remove(extract_path)
                    os.rename(old_path, extract_path)

    # 删除文件夹
    def delete_folder(self, folder_path) -> None:

        '''
        
        有参无返
        删除文件夹
        参数：
            folder_path：文件夹路径
        
        
        '''

        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist. ---> 文件夹不存在")
            return
        try:
            shutil.rmtree(folder_path)
            print(f"Folder {folder_path} has been deleted successfully. ---> 删除成功")
        except PermissionError:
            print(f"Permission denied when deleting folder {folder_path}. ---> 删除失败")
        except Exception as e:
            print(f"An error occurred: {e } ---> 删除失败")

    # 删除文件
    def remove_file(self, file_path):
        # 指定要删除的文件路径，可以是绝对路径或者相对路径
        # file_path = "example.txt"

        try:
            os.remove(file_path)
            print(f"文件 {file_path} 已成功删除")
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在，无法删除")
        except PermissionError:
            print(f"没有权限删除文件 {file_path}")
        except Exception as e:
            print(f"删除文件时出现其他错误: {e}")

    def main(self):

        '''
        
        无参有返
        主函数
        返回：
            True：成功
            False：失败
        
        '''

        path = os.getcwd()
        ini = ini_maker()

        # 解压压缩包
        self.uncompress_archive(f"{path}/up.zip", f"{path}/update")
        log.info("解压完成")

        # 获得指定文件夹下全部的文件夹名和文件名
        elements = self.list_directory_elements(f"{path}/update")
        # print(elements)
        
        # 获取所有的键, 并整合为列表
        path_list = self.find_all_path(f"{path}/update/test.ini")
        if path_list == None:
            log.error("未找到PATH标头")
            return None
        # print(path_list)

        # 用于存放配置文件路径分割的值
        key_path_list_sp = []
        # 用于存放配置文件路径的值
        key_path_list = []
        # 用于存放相同的值
        result_list = []
        # 用于存放源和目标的字典
        result_dict = {}

        # 获取全部的值
        for key in path_list:
            value = ini.get_ini_value("update/test.ini", 'PATH', key)
            key_path_list.append(value)
            # 获取文件夹或者文件名
            value_sp = value.split('/')
            # print(value_sp)
            value_sp = value_sp[-1]
            # print(value_sp)
            key_path_list_sp.append(value_sp)

            # print(key)
            for j in elements:
                # print(key)
                # result = j.split('\\')
                # result = result[-1]
                if value_sp in j:
                    # print(value)
                    # print(j)
                    result_list.append(j)
                    result_dict[value] = j
        
        # 比较是否相同
        print(key_path_list)
        print(result_list)
        print(result_dict)
        if len(key_path_list_sp) != len(result_list):
            log.error(f"出错, 不相同, 配置文件中路径数为: {len(key_path_list_sp)} 条路径, 与实际解压缩文件夹中相同的文件/文件夹仅为: {len(result_list)} 条路径. 请检测是否丢包或者路径填写错误! ")
            return False, 'error'

        log.info("全部路径相同, 开始移动")
        # 使用 items() 方法遍历字典
        for key, value in result_dict.items():
            # print(f"键: {key}, 值: {value}")
            yuan_path = value
            mubiao_path = f"{path}/{key}"
            # print(yuan_path, mubiao_path)
            self.move_file(yuan_path, mubiao_path)
            # shutil.move(yuan_path, mubiao_path)
        log.info("移动完成")
        self.delete_folder(f"{path}/update")
        log.info("删除文件夹完成")

        # 删除压缩包
        self.remove_file(f"{path}/up.zip")

        # exe文件路径
        exe_path = f"{path}/{key_path_list[-1]}"

        return True, exe_path


if __name__ == "__main__":

    find_file_and_move_file().main()