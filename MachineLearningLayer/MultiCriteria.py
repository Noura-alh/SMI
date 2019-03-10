import pandas as pd
from DBconnection import connection2 ,firebaseConnection
import mysql.connector


class MultiCriteria:

    def __init__(self):

        '''Firebase'''
        firebase = firebaseConnection()
        db = firebase.database()

        self.risk_countries = db.child('Rule1').child('highRiskCountries').get().val()
        self.sanction_list = db.child('Rule4').child('blackList').get().val()
        self.exceed_avg_tran = db.child('Rule2').child('exceedingAvgTransaction').get().val()
        self.amount = db.child('Rule3').child('suspiciousTransaction').child('amount').get().val()

        '''database'''
        self.cur, self.db,self.engine = connection2()

        self.ADestID = []
        self.ADestname = []
        self.Alocation = []
        self.Aamount = []
        self.Aavg = []
        self.suspiciousTransactions2= []

        self.cur.execute('SELECT clientID FROM bank_db.transaction')
        record = list(set(list(self.cur.fetchall())))
        for column in record:
            query2 = ("SELECT * FROM bank_db.transaction WHERE clientID = '%s'" % (column[0]))
            self.cur.execute(query2)
            record2 = self.cur.fetchall()
            for column2 in record2:
                self.ADestID.append(column2[6])  # list with client id
                self.Aamount.append(column2[2])  # amount
                self.Aavg.append(column2[11])  # AvgAmountOfTransaction
                self.Alocation.append(column2[12])
                self.ADestname.append(column2[13])  # list with names

    '''
        This method takes a client name  and it checks that name in sanction_list if it was in the sanction
        list it returns one which means rule1 is satisfied
    '''
    def business_rule1(self,client):
        if client in self.sanction_list:
            return 1
        return 0

    '''
            This method takes a client location  and it checks that location in risk_locations if it was in the High risk 
            locations it returns one which means rule2 is satisfied
    '''
    def business_rule2(self,location):
        if location in self.risk_countries:
            return 1
        return 0

    ''' 
            loop to check the 4 rules for each client and calculate its risk
    '''
    def multi_criteria(self,nameDest): #will be sent from detect later on
        if nameDest in self.ADestID:
            i = self.ADestID.index(nameDest)  # finding the location of the id will give us the location of the name.
            filtered_df_ = pd.DataFrame({"nameDest": self.ADestID,"clientName": self.ADestname,
                                         "location": self.Alocation, "amount": self.Aamount})
           # filtered_df_ = pd.read_csv(filtered_df_, delimiter=',', encoding="utf-8")
            filtered_df_ = filtered_df_[filtered_df_['nameDest'] == nameDest].drop_duplicates(keep='first')

            # business rule 1
            ''' client_risk is a col contains 0s and 1s '''
            filtered_df_['client_risk'] = filtered_df_['clientName'].map(self.business_rule1)
            flag1 = filtered_df_['client_risk'].sum()
            # Normalization
            if flag1 > 0:
                flag1 = 1

            # business rule 2
            filtered_df_['location_risk'] = filtered_df_['location'].map(self.business_rule2)
            flag2 = filtered_df_['location_risk'].sum()
            # Normalization
            if flag2 > 0:
                flag2 = 1

            # business rule 3
            max_amount = filtered_df_['amount'].max()
            avg_amount = filtered_df_['amount'].mean()
            if max_amount > avg_amount*self.exceed_avg_tran:
                flag3 = 1
                self.suspiciousTransactions2 = filtered_df_.loc[(filtered_df_['amount'] == max_amount)]
                self.cur.execute("SELECT * FROM SMI_DB.SuspiciousTransaction WHERE transactionID = %s;",filtered_df_['transactionID'])
                record = self.cur.fetchall()
                if (record is None): # Dosen't exisit
                    #query = "INSERT INTO SMI_DB.SuspiciousTransaction (userName, email, fullname, password, bank_id ) VALUES(%s,%s,%s,%s,%s)"
                    #val = (form.username.data, form.email.data, form.fullName.data, form.password.data, 1)
                    #cur.execute(query, val)



            else:
                flag3 = 0

            #business rule 4
            if max_amount > self.amount:
                flag4 = 1
            else:
                flag4 = 0

            sum_of_flags = (flag1 + flag2 + flag3 + flag4)/4
           # print('sum of flags/4 is {} for nameDest as {}'.format(sum_of_flags, nameDest))
            return sum_of_flags
