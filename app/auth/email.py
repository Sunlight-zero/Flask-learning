from flask import render_template, current_app
from app import app
from app.email import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    # print(user, user.email)
    send_email(
        subject='[Paper Warehouse]重置密码',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.jinja',
                                  user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                  user=user, token=token)
    )