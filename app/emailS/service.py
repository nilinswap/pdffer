import smtplib

from os import environ as env

import ssl
from email.message import EmailMessage
from emailS.errors import EmailVerificationError

email_sender = env['GOOGLE_EMAIL_ADDRESS']

# email_password = input(f"Enter your email password for {email_sender}:")


def send_mail(fromaddr, toaddr, subject, message):
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
    print('toaddr', toaddr)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            email_password = env['GOOGLE_EMAIL_PASSWORD']
            smtp.login(fromaddr, email_password)
            smtp.sendmail(fromaddr, toaddr, em.as_string())
    except Exception as e:
        raise EmailVerificationError(toaddr, str(e))


def send_verification_email(email, verification_link):
    """
    Send the verification email to the user.
    :param email:
    :param verification_link:
    :return:
    """
    subject = 'Verify your email'
    message = 'Please verify your email by clicking the link below:\n\n' + verification_link
    send_mail(email_sender, email, subject, message)


if __name__ == '__main__':
    _d = 'A mail from you from Python test'
    _f = 'So happy to hear from you!'
    _e = '<b>A mail from you from Python</b><br><br>' + _f
    send_mail(email_sender, 'nilinswap@gmail.com', _d, _e)
    send_verification_email('nilinswap@gmail.com', 'http://www.google.com')
