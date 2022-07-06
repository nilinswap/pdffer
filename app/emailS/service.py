import smtplib

from os import environ as env

import ssl
from email.message import EmailMessage

email_password = env['GOOGLE_EMAIL_PASSWORD']
email_sender = env['GOOGLE_EMAIL_ADDRESS']


def send_mail_(fromaddr, toaddr, subject, message):
    """
    The main function that sends the mail.
    :param fromaddr:
    :param toaddr:
    :param subject:
    :param message:
    :return:
    """

    em = EmailMessage()
    em['From'] = fromaddr
    em['To'] = toaddr
    em['Subject'] = subject
    em.set_content(message)

    context = ssl.create_default_context()

    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(fromaddr, email_password)
        smtp.sendmail(fromaddr, toaddr, em.as_string())


if __name__ == '__main__':
    _d = 'A mail from you from Python test'
    _f = 'So happy to hear from you!'
    _e = '<b>A mail from you from Python</b><br><br>' + _f
    send_mail_(email_sender, 'nilinswap@gmail.com', _d, _e)
