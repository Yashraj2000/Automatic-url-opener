import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yash",
  password="123456",
  database ="linkdb"
)

mycursor  = mydb.cursor()

val ="mini"

mycursor = mydb.cursor()

sql = "DELETE FROM users WHERE username = 'yash'"

mycursor.execute(sql)

#mycursor.execute('CREATE TABLE userlink (links VARCHAR(255), uname VARCHAR(255), description VARCHAR(255) )')
# result = mycursor.fetchall()
mydb.commit()
# print(result)
# if(len(result)>0 and result[0][0]):
# 	print("User already present")
# else:
# 	print("You can add")