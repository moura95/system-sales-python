import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from midas_sales.config import settings

app = Celery("tasks", broker=settings.celery_broker_url,
             backend=settings.celery_backend_url)


@app.task
def process_task(param):
    # Coloque aqui a lógica de processamento da tarefa
    return f"Task processed with parameter: {param}"


@app.task
def process_send_email(to: str, subject: str, template: str):
    with open(f"templates/{template}.html", "r") as arquivo:
        body_html = arquivo.read()
    receiver_email = to
    sender_email = "nao-responder@midasgestor.com.br"
    message = MIMEMultipart()

    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = subject

    # BODY-- Adjuste for include TEMPLATES
    body_content = MIMEText(body_html, 'html')
    message.attach(body_content)

    # Settings SMTP

    server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
    server.starttls()
    server.login(sender_email, settings.smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
