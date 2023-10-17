import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo():
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_user = 'iturritek.correo@hotmail.com'
    smtp_password = 'correoIturritek'

    subject = 'Nuevo formulario enviado'
    email_body = f'Mensaje de prueba para correo'

    sender = smtp_user
    recipients = ['iturritek.correo@hotmail.com']

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        return False



