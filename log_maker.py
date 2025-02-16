import os
import logging

# 日志生成器
class log_maker():
    def __init__(self):

        '''
        
        日志生成器
        
        日志类型:
            1. info: 普通日志
            2. error: 错误日志
            3. warning: 警告日志
            4. debug: 调试日志
            5. critical: 严重错误日志

        '''

        path = os.getcwd()
        # 获取今天日期
        today = self.get_today()

        log_file_path = f"{path}\\log\\log_{today}.log"
        # 获取日志文件所在目录的路径（去掉文件名部分）
        log_dir = os.path.dirname(log_file_path)
        # 判断目录是否存在，如果不存在则创建
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 先配置基本的日志记录到文件，设置为追加模式（filemode='a'）
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='a', encoding='utf-8')

        # 获取根日志记录器
        self.logger = logging.getLogger()
        # 创建一个StreamHandler用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # 将StreamHandler添加到根日志记录器
        self.logger.addHandler(console_handler)
    
    # 获取今天日期
    def get_today(self):
        from datetime import date

        # 获取今天的日期
        today = date.today()
        # print("今天的日期是:", today)
        return today
    
    # 普通日志
    def info(self, msg):
        self.logger.info(msg)

    # 错误日志
    def error(self, msg):
        self.logger.error(msg)

    # 警告日志
    def warning(self, msg):
        self.logger.warning(msg)

    # 调试日志
    def debug(self, msg):
        self.logger.debug(msg)

    # 严重错误日志
    def critical(self, msg):
        self.logger.critical(msg)


