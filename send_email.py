import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import Diconfig


# 登录发送邮件
class login_send_email():
    def __init__(self):
        super().__init__()
        self.path = os.getcwd()

        self.send_email(
            "发件人",
            "收件人",
            "授权码",
            '用户登录',
            f'有用户登陆了地平线修复工具 {Diconfig.Version} 版本'
        )
    

    # 发送邮件
        # 发件人   收件人  授权码  标题  内容
    def send_email(self, sender, to, email_password, title, meg):
        # 发件人邮箱地址和授权码
        sender_email = sender
        password = email_password

        # 收件人邮箱地址
        receiver_email = to

        # 设置邮件主题、发件人、收件人
        subject = title
        message = meg

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 添加邮件正文内容
        msg.attach(MIMEText(message, 'plain'))

        # 使用QQ邮箱的SMTP服务器发送邮件
        try:
            server = smtplib.SMTP('smtp.qq.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败：{e}")
