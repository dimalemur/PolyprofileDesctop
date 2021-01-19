import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(toaddr, topic, scode, time, username='', ):
    L = 'dim4ik120899@gmail.com'
    P = 'lazurik36'
    To = toaddr
    T = topic
    M = 'Здравствуйте ' + username + '. Ваш код подтвеждения: ' + scode \
        + '. \n Не показывайте никому данный код!' + '\n Время отправки письма: ' + time
    try:
        msg = MIMEMultipart()
        msg['Subject'] = T
        msg['From'] = L
        body = M
        msg.attach(MIMEText(body, 'plain'))

        server = root.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(L, P)

        server.sendmail(L, To, msg.as_string())
        server.sendmail(L, To, M)
        server.quit()

        return 'Success email sent!'

    except:
        return 'Email failed to send'
