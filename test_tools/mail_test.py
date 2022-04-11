import logging
from logging.handlers import SMTPHandler
import sys


logger = logging.getLogger('test-smtphandler')
# 2. logger的日志级别默认是WARNING
logger.setLevel(logging.INFO)
# 对于163邮箱：fromaddr和邮箱账号必须一致，否则发送失败
mail_handler = SMTPHandler(
    mailhost=('smtp.163.com', 25),
    fromaddr='xxx@163.com',
    toaddrs=['xxx@163.com'],
    subject='EMAIL ERROR TEST',
    credentials=('xxx@163.com', 'password'))
mail_handler.setLevel(logging.ERROR)
logger.addHandler(mail_handler)

# 故意出错，触发邮件系统
try:
    x = 1 / 0
except Exception:
    logger.error('Calculation error', exc_info=sys.exc_info())
