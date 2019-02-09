from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import secrets
from DBconnection import connection2


class passwordRecovery:

    def __init__(self, clientEmail):
        self.clientEmail = clientEmail
        self.newPass = secrets.token_hex(16)
        self.sendEmail()





    def sendEmail(self):
        msg = MIMEMultipart()
        msg['From'] = "smi.ksu2019@gmail.com"

        msg['To'] =  self.clientEmail
        msg['Subject'] = "SMI | Password Recovery"

        body = '<html><head> <body style="background-color:#d8d6d6;"> <div style="background-color:#ffffff; text-align: center;"> <h4>Hello '+ self.clientEmail+'! </h4> <p>We have just received a password recovery request for <b>'+ self.clientEmail+'</b><br> This is your new password <b>'+ self.newPass +'</b> <br> You can change it later from your account settings.<br> Thank you,<br> SMI Technical Support</p></div> </body </head></html>'
        msg.attach(MIMEText(body, 'html'))
        print(msg)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'],'SMIHMWN19')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        self.updatePassword()


    def updatePassword(self):
        cur, db = connection2()
        query = "UPDATE SMI_DB.AMLOfficer SET password ='" + self.newPass  + "' WHERE email = '" + self.clientEmail + "'"
        cur.execute(query)
        db.commit()
        cur.close()
        db.close()

