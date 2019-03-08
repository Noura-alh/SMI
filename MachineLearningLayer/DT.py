import pandas as pd
from pandas import DataFrame
import numpy as np
#matplotlib inline
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import average_precision_score, confusion_matrix
from xgboost.sklearn import XGBClassifier
from xgboost import plot_importance, to_graphviz
import warnings
import pickle



class DecisionTree:


    def DecisionTreeClassifier(self):

        warnings.filterwarnings("ignore", category=DeprecationWarning)
        from DBconnection import BankConnection, SMI_engine, connection2
        status, cur, db, engine = BankConnection()
        cur.execute('SELECT * FROM Bank_DB.transaction')
        testX = DataFrame(cur.fetchall())
        testX.columns = cur.column_names


        #print(testX.head())
        #print(testX.isnull().values.any())

        LOACTION = testX['location']
        NAMES = testX['clientName']
        del testX['location']
        del testX['clientName']
        testX = testX.rename(columns={'clientID': 'nameDest'})



                                #testX = pd.read_csv('testingRecordes.csv')


        ######## SAVE THE MODEL  ###########
        '''fileName = 'SMI_MODEL.sav'
        pickle.dump(clf, open(fileName,'wb'))'''


        ######## LOAD THE MODEL  ###########

        loaded_model = pickle.load(open('SMI_MODEL.sav', 'rb'))
        predict = loaded_model.predict(testX)
        testX['isFruad_result'] = predict
        testX['location'] = LOACTION
        testX['clientName'] = NAMES
        testX = testX.rename(columns={'nameDest': 'clientID'})

        ### Save predictions results  ####
        testX.to_csv('predictionsResults.csv', encoding='utf-8', index=False)


        ### Saving Suspicious Transactions in the testing dataset  ####

        suspiciousTransactions = testX.loc[(testX.isFruad_result == 1)]
        suspiciousTransactions.to_csv('suspiciousTransactions.csv', encoding='utf-8', index=False)

        engine2 = SMI_engine()
        cur1, db1 = connection2()
        cur1.execute('DROP TABLE `SMI_DB`.`SuspiciousTransaction`')

        db1.commit()
        cur1.close()
        db1.close()

        suspiciousTransactions.to_sql(name='SuspiciousTransaction', con=engine2, if_exists='append',
                                         index=False)
        db.commit()
        cur.close()
        db.close()
















