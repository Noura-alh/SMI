
import pprint
client_BR ='0100'
Br_flag = True
print('Br', client_BR)
Br_dic = {}
if client_BR == '0000':
    Br_flag = False
else:
    if client_BR[0] == '1':
        Br_dic['Rule#1'] = 'Client Name is in sanction list'
    if client_BR[1] == '1':
        Br_dic['Rule#2'] = 'Client location in risk contries'
    if client_BR[2] == '1':
        Br_dic['Rule#3'] = 'Client exceeded avg amount of transactions'
    if client_BR[3] == '1':
        Br_dic['Rule#4'] = 'Client exceeded max amount of transaction'



if Br_flag == False:
    print('No bussinse rules violations')
else:
    for keys, values in Br_dic.items():
        print(keys)
        print(values)
        print('***************')