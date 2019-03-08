import pandas as pd
from DBconnection import connection2, BankConnection, firebaseConnection

'''Firebase'''

firebase = firebaseConnection()
db = firebase.database()

ADestID = []
ADestname = []
Alocation = []
Aamount = []
Aavg = []

status, cur, db = BankConnection()

query = "SELECT clientID FROM SMI_DB.Client"
cur.execute(query)
record = list(set(list(cur.fetchall())))
for column in record:
    query2 = ("SELECT * FROM SMI_DB.transaction WHERE clientID = '%s'" % (column[0]))
    cur.execute(query2)
    record2 = cur.fetchall()
    for column2 in record2:
        ADestID.append(column2[6])  # list with client id
        Aamount.append(column2[2])  # amount
        Aavg.append(column2[11])  # AvgAmountOfTransaction
        Alocation.append(column2[12])
        ADestname.append(column2[13])  # list with names

riskFlag = 0

'''
Reading dataset

filtered_df = pd.read_csv('GeneratedDataset.csv', sep=",",header=0)
nameDests = filtered_df['nameDest'].unique()

filtered_df.head(2)


Reading sanctions list

sanction_df = pd.read_csv('Sanctions_list.csv', sep=",", header=None, encoding='utf-8', engine="python")
sanction_list = sanction_df[0].tolist()


Reading High risk locations


hrl_df = pd.read_csv('HighRiskLocation.csv', sep=",", header=None, engine='python')
risk_locations = hrl_df[0].tolist()

#risk_locations


    This method takes a client name  and it checks that name in sanction_list if it was in the sanction
    list it returns one which means rule1 is satisfied
'''

risk_countries = db.child('Rule1').child('highRiskCountries').get().val()
sanction_list = db.child('Rule4').child('blackList').get().val()
exceed_avg_tran = db.child('Rule2').child('exceedingAvgTransaction').get().val()
amount = db.child('Rule3').child('suspiciousTransaction').child('amount').get().val()


def business_rule1(client):
    if client in sanction_list:
        return 1
    return 0


'''
    This method takes a client location  and it checks that location in risk_locations if it was in the High risk 
    locations it returns one which means rule2 is satisfied
'''


def business_rule2(location):
    if location in risk_countries:
        return 1
    return 0


''' 
    loop to check the 4 rules for each client and calculate its risk
'''

for nameDest in nameDests:

    filtered_df_ = filtered_df[filtered_df['nameDest'] == nameDest].drop_duplicates(keep='first')

    # business rule 1
    ''' client_risk is a col contains 0s and 1s '''

    filtered_df_['client_risk'] = filtered_df_['clientName'].map(business_rule1)
    flag1 = filtered_df_['client_risk'].sum()
    # Normalization
    if flag1 > 0:
        flag1 = 1
    print(flag1)
    '''if nameDest in sanction_list:
        flag1 = 1
    else:
        flag1 = 0'''

    # business rule 2

    filtered_df_['location_risk'] = filtered_df_['location'].map(business_rule2)
    # print(filtered_df_['location_risk'])
    flag2 = filtered_df_['location_risk'].sum()
    # Normalization
    if flag2 > 0:
        flag2 = 1
    print(flag2)

    # business rule 3
    max_amount = filtered_df_['amount'].max()
    avg_amount = filtered_df_['amount'].mean()
    if max_amount > avg_amount * exceed_avg_tran:
        flag3 = 1
    else:
        flag3 = 0

    # business rule 4
    if max_amount > amount:
        flag4 = 1
    else:
        flag4 = 0

    sum_of_flags = flag1 + flag2 + flag3 + flag4
    print('sum of flags/4 is {} for nameDest as {}'.format(sum_of_flags / 4, filtered_df_['clientName']))



