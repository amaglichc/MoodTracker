import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from db.repositories.AuthRepo import create_and_save_token
from utils.Celery import celery
import asyncio


@celery.task
def send_confirmation_email(user: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email_async(user))


async def send_email_async(user: dict):
    sender_email = settings.EMAIL_SENDER
    password = settings.GOOGLE_PASSWORD
    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтверждение регистрации"
    message["From"] = sender_email
    message["To"] = user["email"]
    token = await create_and_save_token(user["id"])

    confirmation_link = f"http://localhost:8000/confirm-email/{token}"
    html = f"<html><body><a href='{confirmation_link}'>Подтвердите email</a><h2>ВАШ КОД = {token}</h2></body></html>"

    part2 = MIMEText(html, "html")
    message.attach(part2)

    # Асинхронная отправка через SMTP
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=465,
        username=sender_email,
        password=password,
        use_tls=True,
    )
