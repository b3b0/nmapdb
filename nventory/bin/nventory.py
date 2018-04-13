#Copyright (C) 2018 Dustin Davis (b3b0)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()
oss = os.system

oss("clear")

if os.path.isfile("/opt/nventory/database/database.db-journal"):
    locked = True
    while locked == True:
        if os.path.isfile("/opt/nventory/database/database.db-journal"):
            oss("clear")
            print("ERROR:")
            raw_input("The audit database is LOCKED! Press ENTER to continue after changes are applied and database is unlocked.")
        else:
            print("The audit database is now unlocked. Proceeding with AB5K.")
            locked = False

checking = True

while checking == True:
    print("""
                      _                   
                     | |                  
 _ ____   _____ _ __ | |_ ___  _ __ _   _ 
| '_ \ \ / / _ \ '_ \| __/ _ \| '__| | | |
| | | \ V /  __/ | | | || (_) | |  | |_| |
|_| |_|\_/ \___|_| |_|\__\___/|_|   \__, |
                                     __/ |
                                    |___/ 

                  v 0.2
""")
    print("")
    iplist = raw_input("Are you using an IP list file today? [y/n]: ")
    if iplist == "n":
        target = raw_input("Specify host or host range (no CIDR): ")
        action = ("sudo nmap -v --osscan-guess -O " + target +  " -oX /opt/nventory/xml/" + target + ".xml --open")
        checking == False
        break
    if iplist == "y":
	print("Select your IP list file!:")
	target = tkFileDialog.askopenfilename()
        if os.path.isfile(target):
            scanname = raw_input("Give this scan a unique name. (example: usersubnet, servers, etc...): ")
            if os.path.isfile("/opt/nventory/xml/" + scanname + ".xml"):
                print("Please provide a unique filename. /opt/nventory/xml/" + scanname + ".xml exists.")
            if not os.path.isfile("/opt/nventory/xml/" + scanname + ".xml"):
                action = ("sudo nmap -v --osscan-guess -O -iL " + target + " -oX /opt/nventory//xml/" + scanname + ".xml --open")
                checking == False
                break
        if not os.path.isfile(target):
            print("Cannot find " + target + ".")
    else:
        oss("clear")
        print("You have two choices. This isn't hard bro.")

interface = raw_input("Will you use a specific interface? [y/n]: ")

if interface == "y":
    oss("ifconfig")
    whichint = raw_input("Which interface will you use?: ")
    action = action + " -e " + whichint

print("")

actiontype = raw_input("""
Choose which type of scan:
--------------------------
pn  = host discovery      (Disable host discovery. Port scan only.)
sv  = service versioning  (Attempts to determine the version of the service running on port)
a   = aggressive          (not recommended for ranges larger than 10 hosts)
ss  = TCP/SYN connect     (TCP SYN port scan (Default))

If none selected, a plain nmap scan will commence.

Choose [pn/sv/sn/a/ss/ps/stu]: """)

if actiontype == "pn":
    action = action + " -Pn"
if actiontype == "sv":
    action = action + " -sV"
if actiontype == "sn":
    action = action + " -sN"
if actiontype == "a":
    action = action + " -A"
if actiontype == "ss":
    action = action + " -sS"

print("")

portchoose = raw_input("Will you use a standard port scan or custom? [s/c] (default = s): ")

if portchoose == "c":
    customizer = raw_input("Enter individual ports separated by commas, or a range. (Ex:22,23,24,135-139): ")
    action = action + " -p " + customizer
else:
    print("Standard ports will be used. According to which nmap scan you have invoked.")

print("")
print("..................................")
print("    PRESS ENTER TO EXECUTE:       ")
print(action)
print("..................................")
raw_input("")

oss(action)

print ("")
print("..................................")
print("    ADD RESULTS TO DATABASE?      ")
print("..................................")
databaser = raw_input("[y/n]: ")

if iplist != "y":
    xml = "/opt/nventory/xml/" + target + ".xml"
if iplist == "y":
    xml = "/opt/nventory/xml/" + scanname + ".xml"

if databaser == "y":
    oss("python2 /opt/nventory/bin/nmapdb.py -d /opt/nventory/database/database.db " + xml)
    print("IT IS DONE!")
    print("~-~-~-~-~-~-")
if databaser != "y":
    print("YOU HAVE CHOSEN NOT TO ADD TO DATABASE")

print("")

print("That was a nice round of auditing! Great job!")