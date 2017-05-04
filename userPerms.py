#!/usr/bin/python
""" This is a smiple Python script that will take DB user, host and password from the user to query MySQL database
    and obtain a list of it's users. It then checks the permissions on those users given the that information.
    Script WILL install mysql-devel and gcc as well as termcolor and MySQL-python via pip if not present.
    Should be run as root user and the db user should have at least select on ALL databases """

from itertools import chain
import itertools
import subprocess
import time
import os
import sys

#determine the distro
rhel_based= ['amazon', 'centos', 'redhat']
debian_based = ['ubuntu', 'debian']


with open("/etc/issue") as f:
    distro = f.read().lower().split()[0]
    if distro in rhel_based:
        pkg_mgr = "yum"
    elif distro in debian_based:
        pkg_mgr = "apt-get"
    else:
        print colored('ERROR!', 'red') + " Unsupported Distribution!"
        sys.exit()


#Function for installing packages
def install(name):
    subprocess.call(['pip', 'install', name])

#Make sure MySQLdb is installed
try:
    import MySQLdb
except ImportError:
    cmd = "sudo %s install gcc mysql-devel" % pkg_mgr
    os.system(cmd)
    install('MySQL-python')
    import MySQLdb

#Make sure termcolor is installed so we can use 'colored'
try:
    from termcolor import colored
except ImportError:
     install('termcolor')
     from termcolor import colored


# Create a class for 'bold' text
class color:
    BOLD = '\033[1m'
    END = '\033[0m'


#Notice
print "*** NOTE: Please ensure that the user you use is either root or has super user privileges ***\n"

#Take user input as variables for db connection
db_host = raw_input("Database Host:") or 'localhost'
db_user = raw_input("Databse User:") or 'root'
db_pass = raw_input("Database Password:")

#Stip whitespace from user input
db_host = "".join(db_host.split())
db_user = "".join(db_user.split())
db_pass = "".join(db_pass.split())

#Let user know we are about to do things
print "\n Thank you. Querying database...\n"
time.sleep(2)

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

#Set up permissions heading
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
