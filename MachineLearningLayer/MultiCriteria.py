import pandas as pd
from DBconnection import connection2, firebaseConnection
from pandas import DataFrame
import mysql.connector


class MultiCriteria:

    def __init__(self):

        '''
        self.ADestID = []

        self.ADestname = []
        self.Alocation = []
        self.Aamount = []
        '''

    def rules_mapping(self, Firstoperand, nameDest):
        self.nameDest = nameDest
        self.Firstoperand = Firstoperand
        ValueOfTheAtt = pd.DataFrame()
        print(self.nameDest)

        '''database'''
        self.cur, self.db, self.engine = connection2()
        query2 = ("SELECT * FROM bank_db.transaction WHERE clientID=  '%s'" % (
            self.nameDest))  # list all transaction for this id
        self.cur.execute(query2)
        record2 = self.cur.fetchall()
        self.df = DataFrame(record2)
        self.df.columns = self.cur.column_names

        if Firstoperand in self.df.columns:  # need to check if Firstoperand exist in the database
            ValueOfTheAtt = self.df[Firstoperand]
        else:
            print("ERROR The column dosen't exist in the database")

        return ValueOfTheAtt

    def business_rules(self, rulsDataFrame, nameDest):
        self.flag = 0
        print("*******business_rules******")
        self.rulsDataFrame = rulsDataFrame
        for rules in range(len(rulsDataFrame.columns)):  # number of rules currently 2
            # for rule in range(rulsDataFrame.shape[0]):#number of argments inside each rules currently 3
            Rule = rulsDataFrame['Rule' + str(rules + 1)]  # coulnm2 row 0
            Firstoperand = Rule.values[0]
            operator = Rule.values[1]  # coulnm2 row 1
            Secondoperand = Rule.values[2]  # coulnm2 row 2
            print(Firstoperand)
            print(operator)
            print(Secondoperand)

            Firstoperand = self.rules_mapping(Firstoperand, nameDest)  # mapping the rule to the database
            # print(Firstoperand)
            if operator == ">":  # mapping the operator
                # print("BINGO > ")
                Firstoperand = Firstoperand.loc[Firstoperand.values > Secondoperand]
                if not Firstoperand.empty:
                    print("greater")
                    self.flag = self.flag + 1
                else:
                    print("No condition is satisfied")

            if operator == "<":  # mapping the operator
                # print("BINGO < ")
                Firstoperand = Firstoperand.loc[Firstoperand.values < Secondoperand]
                if not Firstoperand.empty:
                    print("less")
                    self.flag = self.flag + 1
                else:
                    print("No condition is satisfied")

            if operator == "=":  # mapping the operator
                # print("BINGO = ")
                Firstoperand = Firstoperand.loc[Firstoperand.values == Secondoperand]
                if not Firstoperand.empty:
                    print("equls")
                    self.flag = self.flag + 1
                else:
                    print("No condition is satisfied")
        print(rules + 1, "NUMBER OF RULES")
        return self.flag / (rules + 1)
        # print(rulsDataFrame)

    def savingTransaction(self):
        '''database'''
        self.cur, self.db, self.engine = connection2()

        query1 = ("SELECT * FROM SMI_DB.SuspiciousTransaction WHERE transactionID=  '%s'" % (
        self.suspiciousTransactions2['transactionID']))  # pre suspiciousTransactions2
        self.cur.execute(query1)
        record = self.cur.fetchall()
        # print(record, "****record***")
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
            self.suspiciousTransactions2.to_sql(name='SuspiciousTransaction', con=self.engine, if_exists='append',
                                                index=False)
            # print("*****ADDDEDDD****")
            self.db.commit()


mc = MultiCriteria()

firebase = firebaseConnection()
db = firebase.database()


values = db.child('Rules').get()
data = pd.DataFrame(values.val())

cur2, db2, engine2 = connection2()  # bank_DB
cur2.execute('SELECT clientID FROM bank_db.transaction')  # extract clients id
result = list(set(list(cur2.fetchall())))
for id in result:
    # mc_class = mc.multi_criteria(id)
    flags = mc.business_rules(data, id)
    print(flags, "***flagsResultWithDivsion**")

'''        

                query3 = ("SELECT '%s'" % (self.Firstoperand)+"FROM bank_db.transaction WHERE clientID=  '%s'" % (self.nameDest))#list all transaction for this id
        self.cur.execute(query3)
        record3 = self.cur.fetchall()
        self.df = DataFrame(record3)
'''

'''
self.risk_countries=risk_countries
self.sanction_list=sanction_list
if nameDest in self.ADestID:
    self.s=''
    filtered_df_ = self.df[self.df['clientID'] == nameDest].drop_duplicates(keep='first')

    # business rule 1
    client_risk is a col contains 0s and 1s
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
'''