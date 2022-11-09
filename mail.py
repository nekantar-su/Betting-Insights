import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mail_message import html
import config

sender_email = config.sender_email  # Enter your address
receiver_email = config.receiver_email  # Enter receiver address
password = config.password

message = MIMEMultipart("alternative")
message["Subject"] = "NFL SUNDAY ANALYSIS"
message["From"] = sender_email
message["To"] = receiver_email

# Turn these into plain/html MIMEText objects

text = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first

message.attach(text)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

