# 添加依赖
import os
import time
import shutil
import subprocess
import webbrowser
# from PyQt5.QtWidgets import QWidget
# import Diconfig
import Diconfig
import wmi
import winreg
import pythoncom
from tqdm import tqdm




class xboxServers():
    # -----手动-----
    # 通过服务显示名称进行启用
    def stat_xbox_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for service in c.Win32_Service():
            if service.DisplayName == display_name:
                if service.State == "Stopped":
                    service.StartService()
                    print(f"已启用服务：{display_name}")
                else:
                    print(f"服务 {display_name} 已启用或不存在。")
                break
        else:
            print(f"未找到名称为 {display_name} 的服务。")
        pythoncom.CoUninitialize()
    # 设置为手动
    def start_and_set_manual_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for service in c.Win32_Service():
            if service.DisplayName == display_name:
                if service.State!= "Running":
                    service.StartService()
                    # print(f"已启动服务：{display_name}")
                # 设置服务启动类型为手动
                service.ChangeStartMode("Manual")
                print(f"已将服务 {display_name} 设置为手动启动状态。")
                break
        else:
            print(f"未找到名称为 {display_name} 的服务。")
        pythoncom.CoUninitialize()

    # -----自动-----
    def start_and_set_auto_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for service in c.Win32_Service():
            if service.DisplayName == display_name:
                if service.State!= "Running":
                    service.StartService()
                    print(f"已启动服务：{display_name}")
                # 设置服务启动类型为自动
                service.ChangeStartMode("Automatic")
                print(f"已将服务 {display_name} 设置为自动启动状态。")
                break
        else:
            print(f"未找到名称为 {display_name} 的服务。")
        pythoncom.CoUninitialize()


class Zaxiang():

    def __init__(self):
        super().__init__()
        # 获取自己的软件路径
        self.Apppath = os.getcwd()
        self.path = fr'{self.Apppath}\plugins\app'

    # 自动修复
    def Zidong(self):
        # 1. 重置hosts文件
        self.host_file()
        # 2. 把xbox服务启用
        self.strat_xbox_ser()
        # 3. 修改注册表并赋值
        for i in Diconfig.para:
            self.set_or_create_dword(Diconfig.path, i, 0)
        # 4.关闭防火墙
        self.disable_firewall()
        # 5. 禁用所有仿真电路软件(禁用冲突服务)
        for i in Diconfig.disName:
            self.stop_service_by_display_name(i)

    # 重置hosts文件
    def host_file(self):
        print("正在重置中， 请稍候...")

        try:
            file1_path = fr'{self.path}\host\hosts'  # 1 文件的路径
            file2_path = 'C:\Windows\System32\drivers\etc\hosts'  # 2 文件的路径

            #    先删除目标文件（如果存在）
            try:
                import os
                os.remove(file2_path)

            except FileNotFoundError:
                pass

            #    将源文件移动到目标路径，实现替换
            shutil.copy(file1_path, file2_path)

            time.sleep(0.4)
            # return "重置host文件成功"
            # 刷新缓存
            self.flush_dns_windows()
            return True
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
    # 重置hosts文件附属项
    def flush_dns_windows(self):
       try:
           # 执行刷新DNS缓存的命令
           command = 'ipconfig /flushdns'
           subprocess.run(command, shell=True)
           print("Windows系统DNS缓存已刷新。")
       except subprocess.CalledProcessError as e:
           print(f"刷新DNS缓存出现错误: {e}")

    # 重置网络
    def reset_winsock(self):
        print("稍等，正在重置网络...")
        print("提示重置成功后，请重启电脑生效")

        try:
            # "netsh", "winsock", "reset"
            result = subprocess.run(
                ["netsh", "winsock", "reset"], capture_output=True, text=True)
            print(result.stdout)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        
    # 通过服务显示名称进行完全禁用
    def stop_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        c = wmi.WMI()

        try:
            for service in c.Win32_Service():
                if service.DisplayName == display_name:
                    if service.State == "Running":
                        service.StopService()
                        print(f"已停止服务：{display_name}")

                        # return 'stop', display_name
                    else:
                        print(f"服务 {display_name} 已停止或不存在。")

                        # return 'stoped', display_name
                    # 设置服务启动类型为禁用
                    service.ChangeStartMode("Disabled")
                    print(f"已将服务 {display_name} 设置为禁用状态。")
                    return 'disable', display_name
                    break
            else:
                print(f"未找到名称为 {display_name} 的服务。")
                return 'not found', display_name
        finally:
            pythoncom.CoUninitialize()
        

    # 通过服务显示名称进行启用
    def stat_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        # 完成性能释放1
        c = wmi.WMI()
        for service in c.Win32_Service():
            if service.DisplayName == display_name:
                if service.State == "Stopped":
                    service.StartService()
                    print(f"已启用服务：{display_name}")
                else:
                    print(f"服务 {display_name} 已启用或不存在。")
                break
        else:
            print(f"未找到名称为 {display_name} 的服务。")
        pythoncom.CoUninitialize()

    # xbox服务
    # 自动
    # 将xbox某些服务设置为自动启动
    def start_and_set_auto_service_by_display_name(self, display_name):
        pythoncom.CoInitialize()
        # 完成性能释放1
        c = wmi.WMI()
        for service in c.Win32_Service():
            if service.DisplayName == display_name:
                if service.State!= "Running":
                    service.StartService()
                    print(f"已启动服务：{display_name}")
                # 设置服务启动类型为自动
                service.ChangeStartMode("Automatic")
                print(f"已将服务 {display_name} 设置为自动启动状态。")
                break
        else:
            print(f"未找到名称为 {display_name} 的服务。")
        pythoncom.CoUninitialize()

    # 再次查询类型
    def seach_tendo(self):
        try:
            result = subprocess.run('netsh int teredo show state', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                print(result.stdout)
                return result.stdout
            else:
                print("没有输出内容。")
        except subprocess.CalledProcessError as e:
            print(f"执行命令时出现错误：{e}")

    # 开启xbox服务
    def strat_xbox_ser(self):
        # 手动
        for i in Diconfig.man_safe:
            xboxServers().stat_xbox_service_by_display_name(i)
            xboxServers().start_and_set_manual_service_by_display_name(i)
        # 自动
        for i in Diconfig.auto_safe:
            xboxServers().start_and_set_auto_service_by_display_name(i)

    # 跳转到查询是否封禁的网站
    def ban_html(self):
        url = "https://forza.net/myforza/banhistory"  # 将这里替换为你想要打开的链接
        webbrowser.open(url)

    # 修改注册表并赋值
    def set_or_create_dword(self, key_path, value_name, value):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            try:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
                # print(f"Value {value_name} updated successfully.")
                print(f"创建并赋值 {value_name} 成功")
            except FileNotFoundError:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
                print(f"Value {value_name} created successfully.")
            finally:
                winreg.CloseKey(key)
        except PermissionError:
            print("Permission denied. Run as administrator.")
        except Exception as e:
            print(f"Error handling value {value_name}: {e}")

    # 关闭防火墙
    def disable_firewall(self):
        try:
            # 关闭 Windows 防火墙
            subprocess.run('netsh advfirewall set allprofiles state off', shell=True, check=True)
            # print("防火墙已关闭。")

            return True
        except subprocess.CalledProcessError as e:
            # print(f"关闭防火墙时出现错误：{e}")

            return False

    # 开启防火墙
    def check_and_enable_windows_firewall(self):
        try:
            # 检查域配置文件防火墙状态
            domain_check_command = 'netsh advfirewall show domainprofile | findstr "State"'
            domain_result = subprocess.run(domain_check_command, shell=True, capture_output=True, text=True)
            domain_status = "on" in domain_result.stdout.lower()

            # 检查专用配置文件防火墙状态
            private_check_command = 'netsh advfirewall show privateprofile | findstr "State"'
            private_result = subprocess.run(private_check_command, shell=True, capture_output=True, text=True)
            private_status = "on" in private_result.stdout.lower()

            # 检查公用配置文件防火墙状态
            public_check_command = 'netsh advfirewall show publicprofile | findstr "State"'
            public_result = subprocess.run(public_check_command, shell=True, capture_output=True, text=True)
            public_status = "on" in public_result.stdout.lower()

            if domain_status and private_status and public_status:
                return True
            else:
                # 开启域配置文件防火墙（如果未开启）
                domain_command = 'netsh advfirewall set domainprofile state on'
                subprocess.run(domain_command, shell=True)
                # 开启专用配置文件防火墙（如果未开启）
                private_command = 'netsh advfirewall set privateprofile state on'
                subprocess.run(private_command, shell=True)
                # 开启公用配置文件防火墙（如果未开启）
                public_command = 'netsh advfirewall set publicprofile state on'
                subprocess.run(public_command, shell=True)
                return True
        except subprocess.CalledProcessError as e:
            return False

    # 寻找延迟最低的服务器
    def ping_server(self, server):
        try:
            result = subprocess.run(["ping", "-n", "4", server], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if "平均 = " in line:
                    latency = line.split("平均 = ")[1].split("ms")[0].strip()
                    return float(latency)
            return None
        except Exception as e:
            return None

    # # 寻找延迟最低服务器
    # def ping_xbox_servers(self):
    #         print('正在寻找ping列表中延迟最低的一项')
    #         lowest_latency = float('inf')
    #         low = None
    #         with tqdm(total=len(config.teredo_servers), desc="正在寻找延迟最低的一个地址") as pbar:
    #             for server in config.teredo_servers:
    #                 latency = self.ping_server(server)
    #                 if latency is not None and latency < lowest_latency:
    #                     lowest_latency = latency
    #                     low = server
    #                 pbar.update(1)
    #         script_directory = os.path.dirname(os.path.abspath(__file__))
    #         file_path = os.path.join('', 'result.txt')
    #         try:
    #             with open('result.txt', 'w') as f:
    #                 f.write(f"{low}")
    #             print(f"延迟最低的服务器是：{low}，延迟为：{lowest_latency}ms")
    #             print(f"结果已写入 {file_path} 文件。")
    #         except Exception as e:
    #             print(f"写入文件时出现错误：{e}")

    def send_reg_command(self):
        try:
            # 构建要执行的命令
            command = 'reg add HKLM\\System\\CurrentControlSet\\Services\\Tcpip6\\Parameters /v DisabledComponents /t REG_DWORD /d 0x0'
            # 使用subprocess.Popen来启动命令，以便后续能进行输入交互
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 等待2秒
            time.sleep(2)
            # 向命令的标准输入写入 'y' 并添加换行符（模拟按下回车键）
            process.stdin.write(b'y\n')
            process.stdin.flush()

            # 获取命令执行的标准输出和标准错误输出内容
            stdout, stderr = process.communicate()

            # 打印标准输出内容
            print("标准输出：")
            print(stdout.decode('GBK'))
            return True

        except subprocess.CalledProcessError as e:
            print(f"命令执行出现错误: {e}")
            return False
    # Apppath = os.getcwd()
# path = fr'{Apppath}\plugins\app'
# file1_name = fr'{path}\host\hosts'


