from MachineLearningLayer.DT import DecisionTree
from DBconnection import BankConnection ,firebaseConnection
from DBconnection import connection2
from datetime import datetime
from MachineLearningLayer.GeneralSearch import GeneralSearch
from MachineLearningLayer.MultiCriteria import MultiCriteria


class Detection:

    def Detect(self):

        cur1, db1, engine1 = connection2() #SMI_DB

        status, cur2, db2, engine2 = BankConnection() #bank_DB

        '''Firebase'''
        firebase = firebaseConnection()
        db = firebase.database()

        self.risk_countries = db.child('Rule1').child('highRiskCountries').get().val()
        self.sanction_list = db.child('Rule4').child('blackList').get().val()
        self.exceed_avg_tran = db.child('Rule2').child('exceedingAvgTransaction').get().val()
        self.amount = db.child('Rule3').child('suspiciousTransaction').child('amount').get().val()

        '''df = pd.read_csv('GeneratedDataset.csv')
        df.to_sql(name='transaction', con=engine2, if_exists='append',
                                      index=False)'''

        classifier = DecisionTree()
        classifier.DecisionTreeClassifier()


        #MULTI CERTIREA

        #Create profiles
        cur2.execute('SELECT clientID, clientName FROM bank_db.transaction')
        result = list(set(list(cur2.fetchall())))
        cur2.close()
        db2.close()

        #get client how flagged suspious transactions
        cur1.execute('SELECT clientName FROM SMI_DB.SuspiciousTransaction')
        suspsuoiusClient = list(set(list(cur1.fetchall())))



        i = 1
        numOFclean = 0
        numOFLow = 0
        numOfHigh =0
        numOFMeduim = 0
        for id, name in result:
            dt_class = 0
            mc_class = 0
            transaction_class =0
            profile_score = 0
            profile_class = 'clean'
            GeneralSearch_result=0
            GeneralSearch_class =0
            NumberOfRecord = 0
            weightTree = 0.5
            mc = MultiCriteria()
            mc_class = mc.multi_criteria(id,self.risk_countries,self.sanction_list,self.exceed_avg_tran,self.amount)

            # If the client has any suspsuoius transaction run general search
            if any(name in s for s in suspsuoiusClient):
                dt_class = 1
                search = GeneralSearch('"' + name + '"', id)
                #search.twitter_search()
                #GeneralSearch_result, GeneralSearch_class = search.google_search()

            if (name in s for s in suspsuoiusClient):#counter for the number of suspsuoius transactions
                NumberOfRecord = NumberOfRecord+1

            if NumberOfRecord < 1:
                weightTree = 0.75

            try:
                transaction_class = ((weightTree * dt_class)+((1-weightTree)*mc_class)/2)
            except ZeroDivisionError:
                transaction_class = 0


            profile_score = (0.5 * transaction_class) + (0.5 * GeneralSearch_result)

            if 0.7 < profile_score <= 1:
                profile_class = 'High'
                numOfHigh = numOfHigh +1
            elif 0.33 < profile_score <= 0.7:
                profile_class = 'Medium'
                numOFMeduim = numOFMeduim + 1
            elif 0 < profile_score <= 0.33:
                profile_class = 'Low'
                numOFLow = numOFLow +1
            else:
                profile_class = 'Clean'
                numOFclean = numOFclean + 1

            print('client ID: ', id)
            print('client Name: ', name)
            print('Multi Criteria Score: ',mc_class)
            print('Before IF statment', profile_class)
            print('search_result: ', GeneralSearch_result)
            print('transaction_class: ', transaction_class)
            print('GeneralSearch_class: ', GeneralSearch_class)
            print('profile class: ', profile_class)
            print('***********************')


            if (profile_class == 'High') or (profile_class == 'Medium') :
                date_now = datetime.now()
                formatted_date = date_now.strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO ClientCase (caseClassification, date, clientID) VALUES(%s,%s, %s)"
                val = (profile_class, formatted_date, id)
                cur1.execute(query, val)

            cur1.execute("UPDATE SMI_DB.Client SET profileClassification= '%s'WHERE clientID='%s' " % (profile_class, id))

        cur1.close()
        db1.close()


        print('Summary:')
        print('************')
        print('Total Number of clients', len(result))
        print('Number of clean clients:', numOFclean)
        print('Number of Low clients:', numOFLow)
        print('Number of Meduim clients:', numOFMeduim)
        print('Number of High clients:', numOfHigh)

