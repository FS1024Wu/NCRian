import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="ncr"
)
print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)
sql = """select * from posts"""
mycursor.execute(sql)
res = mycursor.fetchall()

inner = []
for i in range (len(res)):
    for ii in range (len(res[i])):
        try:
            inner.append(res[i][ii])
        except IndexError:
            break
        
print(inner, len(inner))

##mycursor.execute("""select email,password from user where id='sheng11' and email='fangshion@gmail.com';""")
##res=mycursor.fetchall()
##print(res)
##print(res[0][0],res[0][1])

##for x in mycursor:
##    print(x)
##if(len(res)==1):
##    print(x)
    
