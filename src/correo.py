import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(user_name, user_surname, user_tel, user_email, selected_option, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'deko4kplay@gmail.com'
    smtp_password = 'correoIturritek'

    subject = 'Nuevo formulario enviado'
    email_body = f'Nuevo formulario enviado con los siguientes datos:\n\nNombre: {user_name}\nApellidos: {user_surname}\nTeléfono: {user_tel}\nEmail: {user_email}\nServicio: {selected_option}\nMensaje: {message}'

    sender = smtp_user
    recipients = ['destinatario@ejemplo.com']

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



