import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(user_name, user_surname, user_tel, user_email, selected_option, message):
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_user = 'iturritek.correo@hotmail.com'
    smtp_password = 'correoIturritek'

    subject = 'Nueva peticion desde iturritek'
    email_body = f'Nuevo formulario enviado con los siguientes datos:\n\n'
    email_body += f'Nombre: {user_name}\n'
    email_body += f'Apellidos: {user_surname}\n'
    email_body += f'Teléfono: {user_tel}\n'
    email_body += f'Email: {user_email}\n'
    email_body += f'Servicio seleccionado: {selected_option}\n'
    email_body += f'Mensaje: {message}\n'

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



