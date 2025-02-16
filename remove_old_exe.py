from pathlib import Path
import os
import Diconfig


class remove_old_exe:

    '''
    
    移除旧版本的exe文件
    
    
    '''

    def find_files(self, directory):
        found_files = []
        path = Path(directory)
        for item in path.glob("*.exe"):
            if "地平线修复工具" in item.name:
                found_files.append(str(item))
        return found_files

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
        path = os.getcwd()
        directory = f"{path}"  # 替换为你要搜索的目录路径
        result = self.find_files(directory)
        print(result)
        # 寻找当前版本,并将当前版本从列表中移除
        for i in result:
            if Diconfig.Version in i:
                print("存在, 开始移除")
                result.remove(i)
                # print("移除成功")
        # print(result)

        for i in result:
            self.remove_file(i)
            # print("移除成功")
        return True


if __name__ == '__main__':
    remove_old_exe().main()