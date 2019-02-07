from DBconnection import connection, connection2

from datetime import datetime




now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

print(formatted_date)

'''try:
    cursor, conn = connection()
    #cursor.execute("ALTER TABLE generalSearch CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")




    fh = open('searchFiles/"حجاج العجمي".txt', 'r')
    #fh = open('searchFiles/"حجاج العجمي".txt', mode='r', encoding='UTF-8', errors='strict', buffering=1)
        #fh.encode('UTF-8')
        #fh = io.open('searchFiles/"حجاج العجمي".txt', mode="r", encoding="utf-8")
    while True:
        i=0
        line = fh.readline()
        print(line)
            # check if line is not empty
        if not line:
            break

            query = 'INSERT INTO generalSearch (searchID, searchDate, searchContent) VALUES(%s, %s, %s)'
            val = (i, formatted_date, line)
            cursor.execute(query,val)
    fh.close()
    cursor.close()
except Exception as e:
    print(str(e))'''

'''try:
    cursor, conn = connection()
    q = 'INSERT INTO KeyWord(wordID,word) VALUES (%s, %s)'
    val = (84, 'test')
    cursor.execute(q, val)
    cursor.close()
except Exception as e:
    print(str(e))'''


cur, db =connection2()

fh = open('searchFiles/"حجاج العجمي".txt', 'r')


while True:
        i=0
        line = fh.readline()
        print(line)
            # check if line is not empty
        if not line:
            break

        query = 'INSERT INTO generalSearch (searchDate, searchContent) VALUES(%s, %s)'
        val = (formatted_date, line)
        cur.execute(query,val)
fh.close()

#q = "insert into generalSearch(searchID,searchDate,searchContent) values(20, '2019-02-05 22:53:04', 'WORK')"
#v = {20, '2019-02-05 22:53:04', "WORK"}

#cur.execute(q) #runs the query
db.commit() #ensures that its saved
cur.close() #closes the cursor
db.close() #closes the connection

'''try:
    cursor, conn = connection()

    query = "SELECT * from KeyWord"
    cursor.execute(query)

    data = cursor.fetchall()

    for i in range(len(data)):
        print(data[i][1])

    cursor.close()
except Exception as e:
    print(str(e))'''
