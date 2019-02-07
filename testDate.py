from datetime import datetime

from DBconnection import connection2

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

print(formatted_date)

cur, db =connection2()

query = 'INSERT INTO generalSearch (searchDate, searchContent) VALUES(%s, %s)'