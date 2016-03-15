#!/usr/bin/python
# coding: utf-8

"""
NoeYe by KibodWapon
Reference(s):
        http://code.activestate.com/recipes/491264-mini-fake-dns-server/
        https://code.google.com/p/marlon-tools/source/browse/tools/dnsproxy/dnsproxy.py
"""

import os
import re
import socket
import threading
import time
import MySQLdb
import traceback


#db config
host="localhost"
user="root"
password="3531887"
database="noeye"
db=None
domainname="noeye.com"

def esc(s):
    return MySQLdb.escape_string(s)

#insert or update
def sqlquery(sql):
    print sql
    #replace single quote
    global  db
    global host
    global  user
    global  password
    global  database

    try:
        db = MySQLdb.connect(host=host,user=user,passwd=password,db=database,charset='utf8' )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 使用execute方法执行SQL语句
        cursor.execute(sql)
        ret=db.commit()
        db.close()
        return True
    except Exception,ee:
        '''
        发现连接错误，重新处理
        Can't connect to MySQL server on
        '''
        print "===="
        print ee
        traceback.print_stack()
        try:
            db.rollback()
            db.close()
        except Exception,eee:
            print ee
        if "Can't connect to MySQL server on" in  str(ee):
            print "sleep"
            time.sleep(10)
            return  sqlquery(sql)
        return False


'''
insert one dns record
root@localhost.A26AD089D4B88BFEDFD06DF26165AC94.yourdomain.com
data            userkey                          domain




param prefixdata looks like root@localhost.A26AD089D4B88BFEDFD06DF26165AC94.
'''
def insertdnsquery(prefixdata):
    try:
        p=prefixdata.rstrip(".")
        print p

        a=p.split(".")
        if len(p)==1:
            print "data format error"
            return False
        k=a[-1:][0]
        print k
        if len(k)!=32:
            print "we are using 32 bits user key"
            return False
        d=".".join(a[:-1])
        sql="insert into dns_query(prefixdata,user_key) values('%s','%s')"%(esc(d),esc(k))
        return  sqlquery(sql)
    except:
        pass
class DNSQuery(object):
    """
    Used for making fake DNS resolution responses based on received
    raw request

    Reference(s):
        http://code.activestate.com/recipes/491264-mini-fake-dns-server/
        https://code.google.com/p/marlon-tools/source/browse/tools/dnsproxy/dnsproxy.py
    """

    def __init__(self, raw):
        self._raw = raw
        self._query = ""

        type_ = (ord(raw[2]) >> 3) & 15                 # Opcode bits

        if type_ == 0:                                  # Standard query
            i = 12
            j = ord(raw[i])

            while j != 0:
                self._query += raw[i + 1:i + j + 1] + '.'
                i = i + j + 1
                j = ord(raw[i])

    def response(self, resolution):
        """
        Crafts raw DNS resolution response packet
        """

        retVal = ""

        if self._query:
            retVal += self._raw[:2]                                             # Transaction ID
            retVal += "\x85\x80"                                                # Flags (Standard query response, No error)
            retVal += self._raw[4:6] + self._raw[4:6] + "\x00\x00\x00\x00"      # Questions and Answers Counts
            retVal += self._raw[12:(12 + self._raw[12:].find("\x00") + 5)]      # Original Domain Name Query
            retVal += "\xc0\x0c"                                                # Pointer to domain name
            retVal += "\x00\x01"                                                # Type A
            retVal += "\x00\x01"                                                # Class IN
            retVal += "\x00\x00\x00\x20"                                        # TTL (32 seconds)
            retVal += "\x00\x04"                                                # Data length
            retVal += "".join(chr(int(_)) for _ in resolution.split('.'))       # 4 bytes of IP

        return retVal

class DNSServer(object):
    def __init__(self):
        self._requests = []
        self._lock = threading.Lock()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("", 53))
        self._running = False
        self._initialized = False

    def pop(self, prefix=None, suffix=None):
        """
        Returns received DNS resolution request (if any) that has given
        prefix/suffix combination (e.g. prefix.<query result>.suffix.domain)
        """

        retVal = None

        with self._lock:
            for _ in self._requests:
                if prefix is None and suffix is None or re.search("%s\..+\.%s" % (prefix, suffix), _, re.I):
                    retVal = _
                    self._requests.remove(_)
                    break

        return retVal

    def run(self):
        """
        Runs a DNSServer instance as a daemon thread (killed by program exit)
        """

        def _():
            try:
                self._running = True
                self._initialized = True

                while True:
                    data, addr = self._socket.recvfrom(1024)
                    _ = DNSQuery(data)
                    self._socket.sendto(_.response("127.0.0.1"), addr)

                    with self._lock:
                        self._requests.append(_._query)

            except KeyboardInterrupt:
                raise

            finally:
                self._running = False

        thread = threading.Thread(target=_)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    server = None
    try:
        server = DNSServer()
        server.run()

        while not server._initialized:
            time.sleep(0.1)

        while server._running:
            while True:
                _ = server.pop()

                if _ is None:
                    break
                else:
                    #print "[i] %s" % _
                    if not _.endswith("in-addr.arpa."):
                        print _[0:-1]
                        insertdnsquery(_[0:-(len(domainname)+1)])

            time.sleep(1)

    except socket.error, ex:
        if 'Permission' in str(ex):
            print "[x] Please run with sudo/Administrator privileges"
        else:
            raise
    except KeyboardInterrupt:
        os._exit(0)
    finally:
        if server:
            server._running = False