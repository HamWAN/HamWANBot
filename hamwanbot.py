import socket
import shlex
import math
import json
from subprocess import Popen, PIPE, STDOUT
        
server = "chat.freenode.net"       #settings
channel = "#hamwan"
botnick = "HamWANBot"

def get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]
 
def get_ping_time(host):
    host = host.split(':')[0]
    cmd = "fping {host} -C 3 -q".format(host=host)
    res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
    if len(res) > 0:
        return round(sum(res) / len(res) * 10)/10
    else:
        return None
def google(search):
    cmd = """curl -s --get --data-urlencode "q="""+search+"""" http://ajax.googleapis.com/ajax/services/search/web?v=1.0"""
    result = get_simple_cmd_output(cmd).strip()
    result = json.loads(result)
    
    return result

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print "connecting to:"+server
irc.connect((server, 6667))                                                         #connects to the server
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
irc.send("JOIN "+ channel +"\n")        #join the chan

while 1:    #puts it in a loop
    text=irc.recv(2040)  #receive the text
    t = ''
    print text   #print text to console

    if text.find('PING') != -1:                          #check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
    if text.find(':!hi') !=-1: #you can change !hi to whatever you want
        t = text.split(':!hi') #you can change t and to :)
        to = t[1].strip() #this code is for getting the first word after !hi
        irc.send('PRIVMSG '+channel+' :Hello '+str(to)+'! \r\n')
    if text.find(':!ping') !=-1:
        t = text.split(':!ping') #you can change t and to :)
        address = t[1].strip() #this code is for getting the first word after !hi
        ping = get_ping_time(address)
        if ping is not None:
            irc.send('PRIVMSG '+channel+' :Ping to '+str(address)+': '+str(ping)+' ms. \r\n')
        else:
            irc.send('PRIVMSG '+channel+' :'+str(address)+' is not responding to ping. \r\n')
    if text.find(':!google') !=-1: #you can change !hi to whatever you want
        t = text.split(':!google') #you can change t and to :)
        term = t[1].strip() #this code is for getting the first word after !hi
        url = 'test'
        result = google(term)
        searchResults = result.get('responseData').get('results')
        if len(searchResults) > 1:
            irc.send('PRIVMSG '+channel+' :First result on Google: "' + str(searchResults[0].get('titleNoFormatting')) + '" '+str(searchResults[0].get('url'))+'. \r\n')
        else:
            irc.send('PRIVMSG '+channel+' :No results on Google for "' + term +'". \r\n')
