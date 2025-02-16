import ctypes
import requests

from PySide6.QtCore import *

# from check_up.log_maker import *

from log_maker import *
import Diconfig

log = log_maker()

# 检测是否能够开启软件
class check_update():
    def __init__(self):
        # 定义后端服务器的地址，这里假设Flask应用运行在本地，你可以根据实际情况修改IP地址
        self.url = "http://127.0.0.1:5000"
    
    # 检测是否为管理员方式启动应用
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    # 查询最后一行，获得最后一行输出
    def check_app_version(self):

        # 定义后端服务器的地址，这里假设Flask应用运行在本地，你可以根据实际情况修改IP地址
        # self.url = "http://127.0.0.1:5000/check_last"

        url = f"{self.url}/check_last"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()  # 正确使用.json()方法解析JSON数据
                result = data.get("result")  # 使用.get()方法获取"result"键对应的值，避免键不存在时报错
                if isinstance(result, list):
                    # 在这里可以对获取到的列表数据进行进一步的操作处理
                    print(result)
                    return result
                else:
                    print("获取到的数据中'result'键对应的值不是列表类型，请检查Flask应用返回的数据格式。")
            except ValueError as e:
                print(f"解析JSON数据出现错误: {e}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    
    # 查询字符串数据
    def check_close(self, string):
        
        '''
        这个方法可以检查某一列是否存在一个值，如果存在则以列表形式返回整个行，如果不存在返回 error字符串
        要检查的字符串 "string"
        
        '''

        url = f"{self.url}/check_lock"
        headers = {'Content-Type': 'application/json'}
        data = {'string': string}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            # print(result['result'])
            return result['result']
        else:
            print(f"Error: {response.status_code}, {response.text}")

    # 若需要更新，则更新地址为
    def update_url(self):
        pass

    def main(self):
        
        '''
        
        没用管理员方式启动则返回 -1 ->
        版本被作者关闭则返回 0 ->
        版本被作者关闭，并且启动自毁程序则返回 66 ->
        版本号不一致且需要强制更新返回11 ->
        需要更新则返回 1
        
        '''

        # 判断是否为管理员方式启动
        if not self.is_admin():
            # 记录在日志
            log.error("此程序需要以管理员身份运行。请重新以管理员身份启动程序。----->用户没用管理员方式启动")
            return -1
        else:
            # 记录在日志
            log.info("用户以管理员方式启动")

        # 获取版本号
        get_v = check_update()
        result = get_v.check_app_version()
        # 获取当前版本是否被作者关闭
        open_and_close = self.check_close(Diconfig.Version)
        open_and_close = open_and_close[3]
        # 获取是否需要强制更新
        must_up = result[4]
        # 获取版本号
        now_version = result[1]
        
        # 检查是否被作者关闭
        if open_and_close == 1:
            # 记录在日志
            log.error("此版本被作者关闭")
            return 0
        elif open_and_close == 2:
            # 记录在日志
            log.error("版本被作者关闭，并且启动自毁程序")
            return 66
        log.info("版本未被作者关闭")
        # 记录在日志
        log.info(f"获取到的服务器最新的版本号为：{now_version}")

        # 对比版本号
        if now_version == Diconfig.Version:
            # 记录在日志
            log.info("版本号一致，无需更新")
        else:
            # 记录在日志
            log.info("版本号不一致，需要更新但不需要强制更新")
            
            # 版本号不一致且需要强制更新
            if must_up == 1:
                # 记录在日志
                log.info("版本号不一致且需要强制更新")
                return 11

            return 1
        
start = check_update()
start.main()
# result = start.send_string_to_flask("V1.0")
# if result != "没有找到":
#     print(result[1])
# else:
#     print("没有找到")
# start.test()
                

