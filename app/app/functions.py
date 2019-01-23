import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta, date


from django.conf import settings


def send_email(number_of_project, add_date, email_to, file):
    #  отправка email
    error = ""
    del_date = date.today() + timedelta(days=3)

    fromaddr = "oa@fort-telecom.ru"
    pswd = "BQpE4pNb"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = email_to
    msg['Subject'] = "Проект № {}, зарегистрированный ООО Форт-Телеком, актуален?".format(number_of_project)

    html = """
    <html>
      <head></head>
      <body>
      <p>Добрый день!</p>
        <p>
        Напоминаем, что истек срок регистрации Вашего проекта <strong>рег.№ {0} от {1}</strong>.
        Проект будет автоматически <strong>удален из базы {2}</strong>.
        Если данный проект актуален - просьба сообщить об этом в ответном письме.
        </p>
        <hr/>
        <p>С уважением,<br/>
        Оксана Абрамова<br/>       
        Корпоративный менеджер отдела продаж Fort Telecom<br/>      
        614107, г. Пермь, ул. Хрустальная, 8а<br/>   
        Тел.: (342) 260-20-30, 215-59-89 доб.102<br/>         
        ICQ: 624 423 170<br/>      
        E-mail: oa@fort-telecom.ru<br/>
        skype: oa@fort-telecom.ru<br/>        
      </body>
    </html>
    """.format(number_of_project, add_date.strftime("%d.%m.%Y"), del_date.strftime("%d.%m.%Y"))

    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # Прикрепление файла
    filename = "Project.pdf"
    try:

        file_path = settings.MEDIA_ROOT + "/" + file.name

        attachment = open(file_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    except FileNotFoundError as err:
        error += str(err)
        error += "\n"
    except TypeError as err:
        error += str(err)
        error += "\n"

    server = smtplib.SMTP('smtp.mastermail.ru', 25)
    server.starttls()
    try:
        server.login(fromaddr, pswd)
        text = msg.as_string()
        server.sendmail(fromaddr, email_to, text)
    except smtplib.SMTPAuthenticationError as err:
        error += str(err)
        error += "\n"
    except smtplib.SMTPSenderRefused as err:
        error += str(err)
        error += "\n"
    except smtplib.SMTPRecipientsRefused as err:
        error += str(err)
        error += "\n"
    finally:
        server.quit()

    # print("Отправлен Email")
    return error
