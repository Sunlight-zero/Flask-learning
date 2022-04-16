from flask_mail import Message
from app import app, mail
from flask import render_template
from threading import Thread

# 异步发送邮件
# 因为Flask借助context来避免某些参数传送，
# 创建新线程时需手动传入app实例
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
