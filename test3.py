from DBconnection import connection2

cur, db, enginec = connection2()

cur.execute("SELECT * FROM SMI_DB.ClientCase ")
cases = cur.fetchall()
countCases = len(cases)
print("Cases",cases[0][5])