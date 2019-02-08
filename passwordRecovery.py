from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

msg = MIMEMultipart()
msg['From'] = "smi.ksu2019@gmail.com"
recipients = [ "nourahnasser2@gmail.com","AitchEmm98@gmail.com","m305maha@gmail.com","wejdanqt@gmail.com"]
msg['To'] = ", ".join(recipients)
msg['Subject'] = "Password Recovery"

body = "Hello this is test for password recovery request - Sent from SMI python"
msg.attach(MIMEText(body, 'html'))
print(msg)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(msg['From'],'SMIHMWN19')
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()
