from fastapi import BackgroundTasks
import smtplib

def send_email(subject, body, to):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("abc@gmail.com", "password")
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail("abc@gmail.com", to, message)
    server.quit()
