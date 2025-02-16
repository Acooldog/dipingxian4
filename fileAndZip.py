import requests, zipfile
import os

class FileDownloader:
    def __init__(self, url, save_path, show_progress=False):
        """
        初始化文件下载器

        参数:
        url: 要下载文件的URL地址
        save_path: 文件在本地保存的路径，包含文件名及扩展名，若路径中的目录不存在会自动创建
        show_progress: 是否显示下载进度，默认为False（不显示）
        """
        self.url = url
        self.save_path = save_path
        self.show_progress = show_progress
        self.file_size = 0  # 用于记录文件总大小（字节数）
        self.downloaded_size = 0  # 用于记录已下载的大小（字节数）

    def download(self):
        """
        执行文件下载操作
        """
        try:
            self._create_local_directory()
            response = requests.get(self.url, stream=True)
            if response.status_code == 200:
                self.file_size = int(response.headers.get('Content-Length', 0))
                with open(self.save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            self.downloaded_size += len(chunk)
                            if self.show_progress:
                                self._show_progress()
                print(f"文件已成功下载到 {self.save_path}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"下载出错: {e}")

    def _create_local_directory(self):
        """
        创建本地保存文件的目录（如果不存在的话）
        """
        directory = os.path.dirname(self.save_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _show_progress(self):
        """
        显示下载进度
        """
        progress = self.downloaded_size / self.file_size * 100
        print(f"\r下载进度: {progress:.2f}%", end='')

    def uncompress_archive(self, source_archive_path, destination_path):
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
        
        print("解压完成")
        # 解压完成删除压缩包
        self.remove_file(source_archive_path)

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


def main():
    # 要下载文件的URL
    file_url = "你的服务器网址"
    # 本地保存文件的路径（包含文件名和扩展名），可以根据实际情况调整为绝对路径或相对路径
    local_path = f"{os.getcwd()}/plugins/unlock.zip"

    # 实例化FileDownloader类并调用download方法进行下载
    downloader = FileDownloader(file_url, local_path)
    downloader.download()

    # zip压缩包的实际路径，例如："C:/files/my_zip.zip"，可根据情况替换
    zip_file_path = local_path
    # 想要解压到的指定文件夹路径，比如："C:/files/extracted_folder"，可按需修改
    extract_to_path = rf"{os.getcwd()}\plugins\unlock"
    downloader.uncompress_archive(zip_file_path, extract_to_path)