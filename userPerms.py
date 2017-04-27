#!/usr/bin/python
from itertools import chain
import itertools
import MySQLdb
import subprocess
import time

#Notice
print "*** NOTE: Please ensure that the user you use is either root or has super user privileges ***\n"

#Take user input as variables for db connection
db_host = raw_input("Database Host:") or 'localhost'
db_user = raw_input("Databse User:") or 'root'
db_pass = raw_input("Database Password:")


db_host = "".join(db_host.split())
db_user = "".join(db_user.split())
db_pass = "".join(db_pass.split())


print "\n Thank you. Querying database...\n"
time.sleep(2)

# Create a class for 'bold' text
class color:
    BOLD = '\033[1m'
    END = '\033[0m'

#Function for installing packages
def install(name):
    subprocess.call(['pip', 'install', name])

#Make sure termcolor is installed so we can use 'colored'
try:
 from termcolor import colored 
except ImportError:
  install('termcolor')
  from termcolor import colored

#Set Connection Parameters
connection = MySQLdb.connect(
                host = db_host,
                user = db_user,
                passwd = db_pass,
                )

#Establish connection
cursor = connection.cursor()

#Execute Queries
cursor.execute("USE mysql;")
cursor.execute("SELECT user,host from user")

#Grab all results from last query
results = cursor.fetchall()

#Create empty list
mylist = []

#Populate list with each item from query results 
for item in results:
    mylist.append(item)

#Convert list of Tuples to regular List
mylist = list(chain.from_iterable(mylist))

#Convert list to Dictionary key being user and value being host value
user_host = dict(itertools.izip_longest(*[iter(mylist)] *2, fillvalue=""))

#Line break to make it look a little cleaner and set up our table heading
space = " "
print "-------------------------------"
print color.BOLD + 'MySQL users:'+ color.END
print "-------------------------------"

print colored("USER", 'green') + space*21 + colored('HOST', 'red')
print "====" + space*21 + "===="

time.sleep(2)

#Loop through Dict to print out user and host
for user, host in user_host.iteritems():
    user = user
    host = host
    print user.ljust(25)[:25] + host


print "\n"
print "-------------------------------"
print color.BOLD + 'Permissions on each user:' + color.END
print "-------------------------------"

time.sleep(2)

for user, host in user_host.iteritems():
    user = user
    host = host

    print colored("Permissions", 'yellow') + " for " + colored(user, 'green') + "@" + colored(host, 'red') + ":"

    cursor.execute("SHOW GRANTS FOR '%s'@'%s'" % (user,host))
    perm_result = cursor.fetchone()
    result = "".join(perm_result)

    print result
    print "\n"
