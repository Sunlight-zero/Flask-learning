from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print(user, user.email)
    send_email(
        subject='[Paper Warehouse]重置密码',
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.jinja',
                                  user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                  user=user, token=token)
    )
