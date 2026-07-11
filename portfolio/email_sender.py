import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

# ── Load credentials from .env ──────────────────────────────────
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("EMAIL_PASSWORD")
reciever_email = os.getenv("RECIEVER_EMAIL")

# ── Connect and log in to Gmail ─────────────────────────────────
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(sender_email, app_password)

# ── Build the email ──────────────────────────────────────────────
msg = EmailMessage()
msg["Subject"] = "Cleaned Data Report"
msg["From"] = sender_email
msg["To"] = reciever_email
msg.set_content("Hey Mahmoud, here's your cleaned data file attached.")

# ── Attach the cleaned Excel file ───────────────────────────────
with open("cleaned_result.xlsx", "rb") as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(
    file_data,
    maintype="application",
    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    filename=file_name
)

# ── Send and close ───────────────────────────────────────────────
server.send_message(msg)
server.quit()
