# nventory

```
                      _                   
                     | |                  
 _ ____   _____ _ __ | |_ ___  _ __ _   _ 
| '_ \ \ / / _ \ '_ \| __/ _ \| '__| | | |
| | | \ V /  __/ | | | || (_) | |  | |_| |
|_| |_|\_/ \___|_| |_|\__\___/|_|   \__, |
                                     __/ |
                                    |___/ 
```

A light-weight NMAP wrapper based on https://github.com/argp/nmapdb.

![alt text](https://i.imgur.com/BhtEOMg.png "nventory!")

### Dependencies:
1. Linux, MacOSX
1. python2
2. libsqlite3-dev
3. pysqlite (https://pypi.python.org/pypi/pysqlite)

### Installation:

1. cd to `$ nventory-master/installer`
2. `$ sudo python2 install.py`
3. You're done!

### Usage:

`$ nventory`

### What's next?

Everything else from this point is straight-forward. 

You can use list files (-iL) for inventorying multiple hosts.

You can explicitly type specific single hosts for inventory as well.

All working elements of this software are located at `/opt/nventory`.

Actual database location: `/opt/nventory/database/database.db`.

Feel free to fork it / break it / bop it.

# FUTURE PLANS

- Create a man page
- Create DEB and RPM packages
- Release v1.0

# nmapdb

nmapdb parses nmap's XML output files and inserts them into an SQLite database.

I coded this a while back (mid 2009) and have been using it since.  Some
people I have shared nmapdb with have found it useful, so I am releasing it
publicly.

Example usage:

```
$ sudo nmap -A -oX scanme.xml scanme.nmap.org

Starting Nmap ...

$ ls scanme.xml
scanme.xml
$ ./nmapdb.py -h
usage: ./nmapdb.py [options] <nmap output XML file(s)>
options:
     (-h) --help         this message
     (-v) --verbose      verbose output
     (-c) --create       specify input SQL file to create SQLite DB
     (-d) --database     specify output SQLite DB file
     (-f) --frequency    list most frequent open ports from specified DB
     (-n) --nodb         do not perform any DB operations (i.e. dry run)
     (-V) --version      output version number and exit
```

Use -c to create a database from the schema on the first run:
```
$ ./nmapdb.py -c nmapdb.sql -d myscan.db scanme.xml
$ file myscan.db
myscan.db: SQLite 3.x database
$ sqlite3 myscan.db
SQLite version 3.7.7 ...
sqlite> select * from hosts;
74.207.244.221||scanme.nmap.org|ipv4|Linux 2.6.18|Linux|85|2.6.X|1316681984|up|
sqlite> select * from ports;
74.207.244.221|22|tcp|ssh|open|
74.207.244.221|80|tcp|http|open|
```

Subsequent scans can be entered into the same database:

```
$ ./nmapdb.py -d myscan.db bar.xml foo.xml host1.xml host2.xml \
    host3.xml host4.xml meh.xml (or simply *.xml)
$ sqlite3 myscan.db
SQLite version 3.7.7 ...
sqlite> select * from ports where ports.port='22';
aa.bb.244.221|22|tcp|ssh|open|
204.cc.ddd.250|22|tcp|ssh|open|
bbb.242.aa.180|22|tcp|ssh|open|
aa.bb.121.21|22|tcp|ssh|open|
sqlite> select * from ports where ports.port='23';
192.168.1.254|23|tcp|telnet|open|
sqlite> select * from hosts inner join ports on hosts.ip=ports.ip where hosts.ip='192.168.1.254' and ports.state='open';
192.168.1.254|00:00:C5:CF:86:30|modem|ipv4||||||up|Farallon Computing/netopia|192.168.1.254|23|tcp|telnet|open|
192.168.1.254|00:00:C5:CF:86:30|modem|ipv4||||||up|Farallon Computing/netopia|192.168.1.254|80|tcp|http|open|
sqlite> select * from hosts inner join ports on hosts.ip=ports.ip where hosts.os_name like '%bsd%' and ports.port=22;
aa.bb.91.25||foo.bar.org|ipv4|FreeBSD 7.0-STABLE|FreeBSD|95|7.X|1231841556|up||aa.bb.91.25|22|tcp|ssh|open|
```

Feel free to fork, submit patches, whatever.

Thanks to antonat and thomas for providing feedback.

argp, Mon Apr 30 14:49:21 EEST 2012


