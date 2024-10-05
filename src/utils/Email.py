import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from db.repositories.AuthRepo import create_and_save_token
from utils.Celery import celery
import asyncio
from jinja2 import Environment, FileSystemLoader


@celery.task
def send_confirmation_email(user: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email_async(user))


def render_html(confirmation_code: int):
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("email.html")
    context = {"confirmation_code": confirmation_code}
    return template.render(context)


async def send_email_async(user: dict):
    sender_email = settings.EMAIL_SENDER
    password = settings.GOOGLE_PASSWORD
    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтверждение регистрации"
    message["From"] = sender_email
    message["To"] = user["email"]
    code = await create_and_save_token(user["id"])
    part2 = MIMEText(render_html(code), "html")
    message.attach(part2)
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=465,
        username=sender_email,
        password=password,
        use_tls=True,
    )
