# 新修复连接不到线上
import os
import subprocess
import wmi
import ctypes
import winreg

from PySide6.QtWidgets import *

from view.log_maker import *

# from log_maker import *

import Diconfig

log = log_maker()

# 新自动修复
class new_xiufu():
    def __init__(self, parent=None):
        self.path = os.getcwd()

        self.main_window = parent
        # 计数器
        self.num = 0
        # 一共有多少个修复过程
        self.max_num = 11

    def main(self):
        # 1. 设置windows时间同步
        self.set_windows_time_sync()
        log.info("1. 设置windows时间同步成功")
        self.num += 1
        # 2. 同步windows时间
        self.sync_windows_time()
        log.info("2. 同步windows时间成功")
        self.num += 1
        # 3. 禁用非微软服务 设想
        # self.disable_non_microsoft_services()
        # 4. 获取所有的适配器名称
        net_list = self.print_network_adapter_aliases()
        log.info("4. 获取所有的适配器名称成功")
        self.num += 1
        # 5. 循环将网络改为公用网络
        for i in net_list:
            self.run_Public(i)
        log.info("5. 循环将网络改为公用网络成功")
        self.num += 1
        # 6. 打开SSL3.0和TLS1.0，1.1，1.2，1.3
        self.set_ssl_tls_registry()
        log.info("6. 打开SSL3.0和TLS1.0，1.1，1.2，1.3成功")
        self.num += 1
        # 7. 将所有适配器禁用ipv6
        for i in net_list:
            self.enable_disable_ipv6_by_name(i)
        log.info("7. 将所有适配器禁用ipv6成功")
        self.num += 1
        # 8. 清除微软商店缓存
        self.run_Wsreset()
        log.info("8. 清除微软商店缓存成功")
        self.num += 1
        # 9. 关闭windows defender定期扫描
        self.run_shut_win()
        log.info("9. 关闭windows defender定期扫描成功")
        self.num += 1
        # 10. 禁用开发模式
        self.run_dis_kaifa()
        log.info("10. 禁用开发模式成功")
        self.num += 1
        # 11. 删除xboxLive凭据
        self.clear_xbox_credentials()
        log.info("11. 删除xboxLive凭据成功")
        self.num += 1
        # 12. 打开凭据管理器，指引用户把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除
        # QMessageBox.information(self.main_window, "提示", "12. 打开凭据管理器，指引用户把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除", QMessageBox.Ok)
        self.open_credential_manager()
        log.info("12. 打开凭据管理器，指引用户把Xbl|开头的选项，举例：Xbl|Devicekey，全部统统删除成功")
        self.num += 1

        return 1
    
    # 设置windows时间同步
    def set_windows_time_sync(self):
        try:
            # 打开自动设置时间（修改注册表）
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\TimeProviders\\NtpClient" /v SpecialPollInterval /t REG_DWORD /d 900 /f')
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\TimeProviders\\NtpClient" /v Enabled /t REG_DWORD /d 1 /f')
            # 设置时区为 UTC+8:00 北京时间（修改注册表）
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation" /v TimeZoneKeyName /t REG_SZ /d "China Standard Time" /f')
            # 与微软时间服务器 time.windows.com 同步时间（修改注册表）
            os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters" /v NtpServer /t REG_SZ /d "time.windows.com,0x9" /f')
            # 重启 Windows 时间服务以使时间同步设置生效
            os.system('net stop w32time && net start w32time')
            # 刷新时区设置
            os.system('tzutil /s "China Standard Time"')
            log.info("设置windows时间同步成功")
        except Exception as e:
            print(f"出现错误: {e}")
            log.error(f"设置windows时间同步出现错误: {e}")

    # 同步windows时间
    def sync_windows_time(self):
        try:
            os.system('w32tm /resync')
            log.info("同步windows时间成功")
        except Exception as e:
            print(f"出现错误: {e}")
            log.error(f"同步windows时间出现错误: {e}")

    # 禁用指定服务
    def disable_service(self, service_name):
        try:
            # 构建禁用服务的命令
            command = f'sc config "{service_name}" start= disabled'
            # 执行命令
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            # 检查执行结果
            if result.returncode == 0:
                print(f'Service "{service_name}" has been disabled successfully.')
            else:
                print(f'Failed to disable service "{service_name}": {result.stderr}')
        except Exception as e:
            print(f'Error occurred: {str(e)}')

    # 获取非微软服务
    def get_non_microsoft_service_names(self):
        """
        获取除微软服务之外的所有服务名称列表
        """
        service_names = []
        try:
            # 获取所有服务的信息
            output = subprocess.check_output(['wmic', 'service', 'get', 'name,displayname', '/format:list'])
            service_info_list = output.decode('utf-8', errors='replace').split('\r\n')
            for info in service_info_list:
                if info:
                    parts = info.split('=')
                    if len(parts) == 2:
                        service_name = parts[0] if parts[0].lower() == 'name' else parts[1]
                        service_names.append(service_name)
            # 筛选出非微软服务
            non_microsoft_service_names = []
            for service_name in service_names:
                try:
                    display_name_output = subprocess.check_output(['sc', 'qc', service_name], capture_output=True, text=True, shell=True).strip()
                    display_name = display_name_output.splitlines()[4].split(':')[1].strip()
                    if not display_name.lower().startswith('microsoft'):
                        non_microsoft_service_names.append(service_name)
                except subprocess.CalledProcessError:
                    continue
            return non_microsoft_service_names
        except Exception as e:
            print(f"获取服务名称时出错: {e}")
            return []

    # 禁用非微软服务 设想
    def disable_non_microsoft_services(self):
        # 初始化 COM 环境
        # # pythoncom.CoInitialize()

        # wmiobj = wmi.WMI()

        # services = wmiobj.Win32_Service()

        # # 创建一个空列表用于存储服务的名称和显示名称
        # service_info = []
        # Name = []
        # DisplayName = []

        # # 遍历服务，将服务的名称和显示名称添加到列表中，排除 Diconfig.Microsoft_server 列表中的服务
        # for i in services:
        #     if i.Name not in Diconfig.Microsoft_display_service:
        #         print(i.Name, i.DisplayName)
        #         service_info.append((i.Name, i.DisplayName))
        #         Name.append(i.Name)
        #         DisplayName.append(i.DisplayName)


        # # 打印服务的名称和显示名称列表
        # for name, display_name in service_info:
        #     print(f"Name: {name}, Display Name: {display_name}")


        # print("服务名称列表：", Name)
        # print("服务显示名称列表：", DisplayName)

        # # 筛选出非微软服务
        # for i in DisplayName:
        #     # print(i)
        #     for j in Diconfig.Microsoft_display_service:
        #         if i == j and i in DisplayName:
        #             DisplayName.remove(i)
        #             print(f"从列表中移出了{i}")
        #             # continue

        # for i in DisplayName:
        #     for j in my_services:
        #         if i == j:
        #             DisplayName.remove(i)
        #             print(f"从列表中移出了{i}")
        #             # continue

        # # 筛选出非微软服务
        # for i in DisplayName:
        #     # print(i)
        #     for j in Diconfig.Microsoft_display_service:
        #         if i == j and i in DisplayName:
        #             DisplayName.remove(i)
        #             print(f"从列表中移出了{i}")
        #             # continue


        # print("服务显示名称列表：", DisplayName)
        # # print(Diconfig.Microsoft_display_service)


        # # 清理 COM 环境
        # # pythoncom.CoUninitialize()

        pass

    # 获取所有的适配器名称
    def print_network_adapter_aliases(self):
        """
        获取所有的适配器名称

        :return: 适配器名称列表
        """
        # pythoncom.CoInitialize()
        net_work = []
        w = wmi.WMI()
        network_adapters = w.Win32_NetworkAdapter()
        for adapter in network_adapters:
            # print(adapter.NetConnectionID)
            if adapter.NetConnectionID:
                net_work.append(adapter.NetConnectionID)
        # print(net_work)

        # 清理 COM 环境
        # pythoncom.CoUninitialize()
        return net_work

    # 将网络改为专用网络
    def run_powershell_command(self):
        command = 'Get-NetConnectionProfile -InterfaceAlias "InterfaceName" | Set-NetConnectionProfile -NetworkCategory Private'
        try:
            # 使用 runas 命令以管理员身份运行 PowerShell 并执行命令
            full_command = f'powershell Start-Process powershell -Verb runas -ArgumentList "-Command \"& {command}\"'
            subprocess.run(full_command, check=True, shell=True)
            print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")

    # 通过PowerShell运行命令, 更改网络为专用网络
    def run_Private(self, network_adapter_name):
        command = f'Get-NetConnectionProfile -InterfaceAlias "{network_adapter_name}" | Set-NetConnectionProfile -NetworkCategory Private'
        # 使用 Windows API 中的 ShellExecuteW 函数
        shell32 = ctypes.windll.shell32
        params = f'-Command "{command}"'
        result = shell32.ShellExecuteW(None, "runas", "powershell", params, None, 1)
        if result > 32:
            print("PowerShell command is running with admin privileges.")
        else:
            print("Failed to run PowerShell command with admin privileges.")

    # 通过PowerShell运行命令, 更改网络为公用网络
    def run_Public(self, network_adapter_name):
        command = f'Get-NetConnectionProfile -InterfaceAlias "{network_adapter_name}" | Set-NetConnectionProfile -NetworkCategory Public'
        # 使用 Windows API 中的 ShellExecuteW 函数
        shell32 = ctypes.windll.shell32
        params = f'-Command "{command}"'
        result = shell32.ShellExecuteW(None, "runas", "powershell", params, None, 1)
        if result > 32:
            print("PowerShell command is running with admin privileges.")
        else:
            print("Failed to run PowerShell command with admin privileges.")

    # 打开SSL3.0和TLS1.0，1.1，1.2，1.3
    def set_ssl_tls_registry(self):
        # 定义需要操作的注册表项和值
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings"
        protocols = {
            "SSL 3.0": "SecureProtocols",
            "TLS 1.0": "SecureProtocols",
            "TLS 1.1": "SecureProtocols",
            "TLS 1.2": "SecureProtocols",
            "TLS 1.3": "SecureProtocols"
        }
        protocol_values = {
            "SSL 3.0": 0x00000020,
            "TLS 1.0": 0x00000080,
            "TLS 1.1": 0x00000200,
            "TLS 1.2": 0x00000800,
            "TLS 1.3": 0x00002000
        }

        try:
            # 打开 Internet Settings 注册表键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "SecureProtocols")[0]
            new_value = current_value
            for protocol, value_name in protocols.items():
                if protocol == "SSL 3.0":
                    new_value |= protocol_values[protocol]
                else:
                    new_value |= protocol_values[protocol]
            # 设置 SecureProtocols 的值
            winreg.SetValueEx(key, "SecureProtocols", 0, winreg.REG_DWORD, new_value)
            winreg.CloseKey(key)
            # print("SSL and TLS 启用成功")
            log.info("SSL and TLS 启用成功")
        except Exception as e:
            # print(f"Failed to set SSL/TLS protocols: {e}")
            log.error(f"Failed to set SSL/TLS protocols: {e}")

    # 将适配器禁用ipv6
    def get_interface_index(self, interface_name):
        try:
            # 执行 netsh 命令列出所有接口
            result = subprocess.run(
                ["netsh", "interface", "ipv6", "show", "interfaces"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout
            # 按行分割输出
            lines = output.splitlines()
            for line in lines:
                # print(line)
                if interface_name in line:
                    parts = line.split()
                    # print(parts)
                    if len(parts) >= 4:
                        # print(parts[3])
                        return parts[0]  # 通常接口索引是第 4 个元素
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.stderr}")
            return None
    # 将适配器禁用ipv6 附属函数
    def enable_disable_ipv6_by_name(self, interface_name, enableAndDisable=False):
        """
        根据接口名称禁用 IPv6

        :param interface_name: 接口名称
        enableAndDisable: True 启用 IPv6, False 禁用 IPv6 默认禁用
        """
        result = ['enable', 'disable']
        if enableAndDisable:
            result_eb = result[0]
        else:
            result_eb = result[1]
        interface_index = self.get_interface_index(interface_name)
        if interface_index:
            try:
                # 执行 netsh 命令禁用 IPv6
                result = subprocess.run(
                    ["netsh", "interface", "ipv6", "set", "interface", interface_index, result_eb],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # print(f"IPv6 for interface {interface_name} has been {result_eb}.")
                log.info(f"IPv6 for interface {interface_name} has been {result_eb}.")
                # print(result.stdout)
            except subprocess.CalledProcessError as e:
                # print(f"Error occurred when disabling IPv6: {e.stderr}")
                log.error(f"Error occurred when {result_eb}ing IPv6: {e.stderr}")
        else:
            # print(f"Interface {interface_name} not found.")
            log.error(f"Interface {interface_name} not found.")

    # 清除微软商店缓存
    def run_Wsreset(self):
        command = 'Wsreset'
        # 使用 Windows API 中的 ShellExecuteW 函数
        shell32 = ctypes.windll.shell32
        params = f'-Command "{command}"'
        result = shell32.ShellExecuteW(None, "runas", "powershell", params, None, 1)
        if result > 32:
            # print("PowerShell command is running with admin privileges.")
            log.info("清除微软商店缓存成功")
        else:
            # print("Failed to run PowerShell command with admin privileges.")
            log.error("Failed to run PowerShell command with admin privileges.")

    # 关闭windows defender定期扫描
    def run_shut_win(self):
        command = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableScanningSchedule /t REG_DWORD /d 1 /f'
        # 使用 Windows API 中的 ShellExecuteW 函数
        shell32 = ctypes.windll.shell32
        params = f'-Command "{command}"'
        result = shell32.ShellExecuteW(None, "runas", "powershell", params, None, 1)
        if result > 32:
            print("PowerShell command is running with admin privileges.")
        else:
            print("Failed to run PowerShell command with admin privileges.")
    
    # 禁用开发模式
    def run_dis_kaifa(self):
        command = 'Get-AppXPackage | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}'
        try:
            # 打开一个新的 PowerShell 窗口并执行命令
            powershell_process = subprocess.Popen(
                ['powershell.exe', '-Command', command],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print("已在新的 PowerShell 窗口中开始执行命令。")
            # 等待命令执行完成
            powershell_process.wait()
            print("命令执行完成，正在关闭 PowerShell 窗口。")
            # 使用 taskkill 命令关闭该 PowerShell 窗口
            subprocess.run(['taskkill', '/F', '/PID', str(powershell_process.pid)], check=True)
            print("PowerShell 窗口已关闭。")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred when running taskkill: {e.stderr}")
        except Exception as e:
            print(f"Error occurred: {e}")

    # 删除xboxLive凭据
    def clear_xbox_credentials(self):
        try:
            # 删除 Xbox Live 相关的凭据
            subprocess.run(["cmdkey", "/delete:XboxLive"], check=True)
            print("Xbox Live 登录凭据已删除。")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.stderr}")

    # 打开凭据管理器，让用户把Xbl开头的选项，举例：Xbl|Devicekey，都删除
    def open_credential_manager(self):
        try:
            # 使用 rundll32 打开凭据管理器
            subprocess.run(["rundll32.exe", "keymgr.dll", "KRShowKeyMgr"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while opening Credential Manager: {e.stderr}")

# if __name__ == "__main__":
#     test = new_xiufu()
#     test.set_ssl_tls_registry()
