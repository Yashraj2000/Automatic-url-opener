import webbrowser 
import random
import datetime
import time as t
import schedule
from datetime import timedelta
import mysql.connector
from dateutil import parser

#Database connections
mydb = mysql.connector.connect(
  host="localhost",
  user="yash",
  password="123456",
  database ="linkdb"
)

mycursor  = mydb.cursor()

print("Hello welcome to the alarm clock \n")
print("You will be Prompted for username which will be used as unique key to identify you\n")


#Function Declaration 
def take_time():
	while True:
		try:
			user_time = input("Enter the date and time you want to play the video in 24hrs format(y-m-d hr:min:sec) \n")
			date,time = user_time.split(" ")
			if date.count('-') != 2:
				raise Exception
			if time.count(':') != 2:
				raise Exception
			yr,mn,dy = date.split('-')
			hr,mins,sec = time.split(':')
			b = datetime.datetime(int(yr),int(mn),int(dy),int(hr),int(mins),int(sec))
			break
		except Exception as e:
			print(e)
			print("Please Enter in described format")
	return b

# Query the db every sec to check if current_time matches the time to visit the link
def search_every_sec():
	t.sleep(1)
	cur_time = datetime.datetime.now()
	cur_time = cur_time.strftime("%Y-%m-%d, %H:%M:%S")
	sql = 'SELECT links FROM userlink WHERE (uname = %s AND played_at = %s)'
	temp = (username,cur_time)
	mycursor.execute(sql,temp)
	result = mycursor.fetchall()
	for x in result:
		print(f'{x[0]} is being visited at {cur_time}\n')
		webbrowser.open(x[0])

#Clearing the file whenever programme runs
with open("links.txt",'w'):
	pass


#Taking user-input
username = input("Please Enter your username to proceed\n")

sql = 'SELECT username FROM users WHERE username = %s'
mycursor.execute(sql,(username,))
result = mycursor.fetchall()
if(len(result)>0):
	#checking if user is already there in db 
	print(f"Welcome back {username}\n")
	print("Please check the link.txt file to find the history of all the links visit by You\n")
	sql = 'SELECT links,played_at FROM userlink WHERE uname = %s'
	mycursor.execute(sql,(username,))
	result = mycursor.fetchall()
	for i in range(len(result)):
		with open("links.txt",'a') as link:
			link.write(result[i][0]+'   ')
			link.write("Played at "+ str(result[i][1])+'\n')
else:
	sql = 'INSERT INTO users(Username) VALUES (%s)'
	mycursor.execute(sql,(username,))
	mydb.commit()
	print("You are successfully registered\n")

#This is current system time
cur_time = datetime.datetime.now()
cur_time = cur_time.strftime("%Y-%m-%d, %H:%M:%S")
print(f'This is Your current system time {cur_time}\n')


# storing the link in the database
while True:
	try:
		while True:
			ytube = input("Enter the link(s) you want to open\n")
			#Checkinf if its a valid link or not 
			if ytube.find("https://")!=-1 or ytube.find("http://")!=-1:
				desc = input("Please enter a description\n")
				time = take_time()
				sql = 'INSERT INTO userlink(links,uname,description,played_at) VALUES (%s,%s,%s,%s)'
				temp = (ytube,username,desc,time)
				mycursor.execute(sql,temp)
				mydb.commit()
			else:
				raise Exception("Sorry, Please enter a valid link\n")
			more = input("Want to enter more links?y/n")
			if(more.lower()=='n'):
				break
		if(more.lower()=='n'):
			break
	except Exception as e:
		print(e)

# Time to visit the last link in db
sql = 'SELECT MAX(played_at) FROM userlink WHERE uname = %s'
temp = (username,)
mycursor.execute(sql,temp)
result = mycursor.fetchall()
max_time = result[0][0]
print(f'Time to visit the last link {result[0][0]}\n')

print("Please wait ... link will be automatically visited")

# if current time is greater than max time break
while True:
	cur_time = datetime.datetime.now()
	if cur_time > max_time:
		break
	search_every_sec()

print("Thanks For using the app , Please do come back")

# s1 = cur_time.time().strftime("%H:%M:%S")
# s2 = user_time
# FMT = "%H:%M:%S"
# tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)
# if tdelta.days < 0:
# 	tdelta = timedelta(days=0,seconds=tdelta.seconds)
# print(f"Time left to open the link is {tdelta}")
