import pandas as pd
from DBconnection import connection2 ,firebaseConnection
from pandas import DataFrame
import mysql.connector


class MultiCriteria:


    def __init__(self):

        '''database'''
        self.cur, self.db,self.engine = connection2()

        self.ADestID = []
        '''
        self.ADestname = []
        self.Alocation = []
        self.Aamount = []
        self.Aavg = []
        self.AtrnID = []
        self.suspiciousTransactions2= []
        '''

        query2 = ("SELECT * FROM bank_db.transaction")
        self.cur.execute(query2)
        record2 = self.cur.fetchall()
        self.df = DataFrame(record2)
        self.df.columns = self.cur.column_names

        for column2 in record2:
            self.ADestID.append(column2[7])  # list with client id
        '''
            self.AtrnID.append(column2[0])
            self.Aamount.append(column2[3])  # amount
            self.Aavg.append(column2[12])  # AvgAmountOfTransaction
            self.Alocation.append(column2[13])
            self.ADestname.append(column2[14])  # list with names
        '''
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
    def multi_criteria(self,nameDest,risk_countries,sanction_list,exceed_avg_tran,amount): #will be sent from detect later on
        self.risk_countries=risk_countries
        self.sanction_list=sanction_list
        if nameDest in self.ADestID:
            self.s=''
            filtered_df_ = self.df[self.df['clientID'] == nameDest].drop_duplicates(keep='first')

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
            self.max_amount = filtered_df_['amount'].max()
            self.avg_amount = filtered_df_['amount'].mean()
            if self.max_amount > (self.avg_amount*exceed_avg_tran):
                flag3 = 1
                self.suspiciousTransactions2 = filtered_df_.loc[(filtered_df_['amount'] == self.max_amount)]
                self.savingTransaction()
                #print(self.suspiciousTransactions2['transactionID'],"***transactionID***")
            else:
                flag3 = 0

            #business rule 4
            if self.max_amount > amount:
                flag4 = 1
                if flag3 == 0:
                    self.suspiciousTransactions2 = filtered_df_.loc[(filtered_df_['amount'] == self.max_amount)]
                    self.savingTransaction()
                #print(self.suspiciousTransactions2['transactionID'],"***transactionID***")
            else:
                flag4 = 0

            sum_of_flags = (flag1 + flag2 + flag3 + flag4)/4
            self.s=str(flag1)+str(flag2)+str(flag3)+str(flag4)
            self.cur.execute("UPDATE SMI_DB.Client SET BR='%s' where clientID='%s'" % (self.s,nameDest))
            self.db.commit()
            #print(self.s)
            return sum_of_flags
            #print('sum of flags/4 is {} for nameDest as {}'.format(sum_of_flags, nameDest))

    def savingTransaction(self):
            '''database'''
            self.cur, self.db,self.engine = connection2()

            query1 = ("SELECT * FROM SMI_DB.SuspiciousTransaction WHERE transactionID=  '%s'" % (self.suspiciousTransactions2['transactionID']))  # pre suspiciousTransactions2
            self.cur.execute(query1)
            record = self.cur.fetchall()
            #print(record, "****record***")
            if not record:  # Dosen't exisit
                LOACTION = self.df['location']
                NAMES = self.df['clientName']
                transactionID = self.df['transactionID']
                del self.df['location']
                del self.df['clientName']
                del self.df['transactionID']
                self.df = self.df.rename(columns={'clientID': 'nameDest'})
                self.df['isFruad_result'] = 1
                self.df['location'] = LOACTION
                self.df['clientName'] = NAMES
                self.df['transactionID'] = transactionID
                self.df = self.df.rename(columns={'nameDest': 'clientID'})

                ### Save results  ####
                self.df.to_csv('predictionsResults.csv', encoding='utf-8', index=False)

                self.suspiciousTransactions2 = self.df.loc[(self.df.amount == self.max_amount)]  # reding form csv file
                self.suspiciousTransactions2.to_csv('suspiciousTransactions.csv', encoding='utf-8', index=False)
                self.suspiciousTransactions2.to_sql(name='SuspiciousTransaction', con=self.engine, if_exists='append', index=False)
                #print("*****ADDDEDDD****")
                self.db.commit()

