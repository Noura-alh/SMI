from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import secrets
from DBconnection import connection2


class passwordRecovery:

    def __init__(self, clientEmail):
        self.clientEmail = clientEmail
        self.newPass = secrets.token_hex(16)
        self.senEmail(self.clientEmail,self.newPass)




    def senEmail(self,Email, password):
        msg = MIMEMultipart()
        msg['From'] = "smi.ksu2019@gmail.com"

        msg['To'] = "nourahnasser2@gmail.com"
        msg['Subject'] = "Password Recovery"

        body = "Hello this is test for password recovery request - Sent from SMI python"
        msg.attach(MIMEText(body, 'html'))
        print(msg)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'],'SMIHMWN19')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def updatePassword(self, Email, password):
        cur, db = connection2()
        query = "SELECT * FROM SMI_DB.AMLOfficer WHERE email ='" + form.email.data + "'"
        cur.execute(query)
        data1 = cur.fetchone()

