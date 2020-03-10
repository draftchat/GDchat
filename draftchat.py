#Written by: Ozkan Mustafa AkkuS ( @ehakkus )
# -*- coding: utf-8 -*-
import pickle,os.path,re,sys,colorama,random,string
import base64,mimetypes,os,cursor,time, dbanner
from base64 import *
from colorama import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto import Random
from email.mime.text import MIMEText
# File upload feature can be added to drafts in the next version
# The following will be used when attachment feature is added to drafts
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

init(autoreset=True)
dbanner.bnr()
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
base64pad = lambda s: s + '=' * (4 - len(s) % 4)
base64unpad = lambda s: s.rstrip("=")

def encrypt(key, msg):
  iv = Random.new().read(BS)
  cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
  encrypted_msg = cipher.encrypt(pad(str(msg)))
  return base64unpad(urlsafe_b64encode(iv + encrypted_msg))

def decrypt(key, msg):
  decoded_msg = urlsafe_b64decode(base64pad(msg))
  iv = decoded_msg[:BS]
  encrypted_msg = decoded_msg[BS:] 
  cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
  return unpad(cipher.decrypt(encrypted_msg))

def CreateMessage(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  fmessage = base64.urlsafe_b64encode(message.as_string())
  return {'raw': fmessage}

def CreateDraft(service, user_id, message_body, deskey, aeskey):
  try:
    draft = service.users().drafts().create(userId=user_id, body=message_body).execute()
    did = draft['id']
    print(Fore.GREEN + "[+] Draft(" + did + ") created successfully")
    GetDraft(service, 'me', did, deskey, aeskey)
    return draft

  except errors.HttpError, error:
    print('An error occurred: %s') % error
    return none

def GetDraft(service, user_id, draft_id, deskey, aeskey):
  try:
    draft = service.users().drafts().get(userId=user_id, id=draft_id, format='full').execute()
    lmessage = draft['message']['payload']['body']['data']   
    des = DES.new(deskey)
    msg = des.decrypt(urlsafe_b64decode(b64decode(str(lmessage))))
    aes = decrypt(aeskey, msg)
    return aes,draft_id

  except errors.HttpError, error:
    print('An error occurred: %s') % error
    return none

def UpDraft(service, user_id, draft_id, message):
    service.users().drafts().update(userId=user_id, id=draft_id, body=message).execute()
    

def pad2(s):
  return s + (DES.block_size - len(s) % DES.block_size) * \
        chr(DES.block_size - len(s) % DES.block_size)

def randomString(stringLength=10):
  letters = string.ascii_letters
  return ''.join(random.choice(letters) for i in range(stringLength))

def descrypto(string, deskey):
  des = DES.new(deskey)
  crstr = urlsafe_b64encode(des.encrypt(pad2(string)))
  return base64pad(crstr)

def is_number_check(s):
  if s == 1 or 2:
    return True
  else:
    return False

def start(deskey, ctype, aeskey):
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except IOError:
                print(Fore.RED + "[?] You need to create a new Cloud Platform project and automatically enable the Gmail API.")   
                print(Fore.YELLOW + "    After enable the Gmail API, in resulting dialog click DOWNLOAD CLIENT CONFIGURATION and")
                print("    save the file credentials.json to your working directory.")
                print(Fore.GREEN + "[+] If you have confusion, follow the steps at https://github.com/draftchat")
                exit()

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    frm = randomString(10) + "@gmail.com" 
    to = randomString(10) + "@gmail.com"
    if str(ctype) == "2": 
      enaes = encrypt(aeskey, 'ImServer') 
      cryptom = descrypto(enaes, deskey) 
      firstm = CreateMessage(frm, to, randomString(7), cryptom) 
      message = {'message': firstm}
      cdraft = CreateDraft(service, 'me', message, deskey, aeskey)
      i = 0
      while(True):
        check_client = GetDraft(service, 'me', cdraft['id'], deskey, aeskey)[0] 
        if str(check_client) == 'ImClient':
          cursor.show()
          print(Fore.GREEN + "\r[+] Client found. Chatting possible.")
          chat(service, cdraft['id'], deskey, frm, to, aeskey) 
        else: 
          cursor.hide()
          msg = "\r[?] Waiting for partner" + ("." * i) + "   "
          sys.stdout.write("\r {:<70}".format(msg))
          sys.stdout.flush()
          i = (i + 1) % 4 
          time.sleep(1)       
      
    if str(ctype) == "1": 
      respon = service.users().drafts().list(userId='me').execute()
      did = respon.get('drafts')[0]['id']
      print(Fore.GREEN + "[+] Last draft(" + did + ") found successfully")
      check_server = GetDraft(service, 'me', did, deskey, aeskey)[0]
      if len(str(check_server)) == 8:
        print(Fore.GREEN + "[+] Server found. Checking AES and DES keys...")
        if str(check_server) == 'ImServer':
          print(Fore.GREEN + "[+] Keys correct! Chatting possible.")
          enaes = encrypt(aeskey, 'ImClient')
          cmessage = descrypto(enaes, deskey)
          limessage = CreateMessage(frm, to, did, cmessage)   
          upmessage = {'message': limessage}
          UpDraft(service, 'me', did, upmessage)
          i = 0
          while(True):
            check_client = GetDraft(service, 'me', did, deskey, aeskey)[0] 
            if str(check_client) != 'ImClient':
              cursor.show()
              print("\r" + "[+] The first message received successfully from " + check_client)
              chat(service, did, deskey, frm, to, aeskey) 
            else: 
              cursor.hide()
              msg = "\r[?] Waiting for the first message from your partner" + ("." * i) + "   "
              sys.stdout.write("\r {:<80}".format(msg))
              sys.stdout.flush()
              i = (i + 1) % 4 
              time.sleep(1)          
        else:
          print(Fore.RED + "[!] Keys not correct! Please get the right keys from your partner.")
          exit()
      else:
        print(Fore.RED + "[!] Server not found. Make sure your partner is a server!")
        exit()
def chat(service, draft_id, deskey, frm, to, aeskey):
    print(Fore.YELLOW + "-" * 69)
    while(True):
      umessage = str(raw_input(nickname + " : " ))
      lastmsg = str(nickname) + " : " + str(umessage)
      enaes = encrypt(aeskey, lastmsg)
      cmessage = descrypto(enaes, deskey)
      limessage = CreateMessage(frm, to, randomString(7), cmessage)   
      upmessage = {'message': limessage}
      UpDraft(service, 'me', draft_id, upmessage)
      i = 0
      while(True):
        rm = GetDraft(service, 'me', draft_id, deskey, aeskey)[0] 
        if rm == lastmsg:
          cursor.hide()
          msg = "\rChecking" + ("." * i) + "   "
          sys.stdout.write("\r {:<70}".format(msg))
          sys.stdout.flush()
          i = (i + 1) % 4 
          time.sleep(1)
        else: 
          cursor.show()
          print("\r" + rm)
          break

def chatctrl(service, user_id, draft_id, deskey, lastmsg):
  GetDraft(service, 'me', draft_id, deskey)

def client_based(ctype):
  print(Fore.YELLOW + "-" * 69)
  print(Fore.YELLOW + "[!] The DES algorithm key is FIRST special key that you need to get ")
  print(Fore.YELLOW + "    from your partner. With this key, your messages are encrypted and")
  print(Fore.YELLOW + "    your partner's messages are decrypted") 
  print(Fore.YELLOW + "-" * 69)
  while(True):
    print(Fore.WHITE + " │")
    deskey = str(raw_input(Fore.WHITE + " └──=> DES Key (Must consist of 8 digits) : ")) 
    if re.match("^[a-zA-Z0-9_]*$", deskey) and len(deskey) == 8:
      print(Fore.YELLOW + "-" * 69)
      print(Fore.YELLOW + "[!] The AES algorithm key is SECOND special key that you need to get ")
      print(Fore.YELLOW + "    from your partner. With this key, the message encrypted with DES ")
      print(Fore.YELLOW + "    is encrypted again ")  
      print(Fore.YELLOW + "-" * 69)
      print(Fore.RED + "[?] Make sure to get the right keys from your partner! ")
      print(Fore.YELLOW + "-" * 69)
      while(True):
        print(Fore.GREEN + " │")
        aeskey = str(raw_input(Fore.GREEN + " └──=> Your AES KEY (Must consist of 16 digits) : "))
        if re.match("^[a-zA-Z0-9_]*$", aeskey) and len(aeskey) == 16:
          print(Fore.YELLOW + "-" * 69)
          start(deskey, ctype, aeskey)
        else:
          print(Fore.RED + "[!] Error! Only letters a-zA-Z0-9 allowed and AES Key should be consist of 16 digits!")
    else:
      print(Fore.RED + "[!] Error! Only letters a-zA-Z0-9 allowed and DES Key should be consist of 8 digits!")

def server_based(ctype):
  print(Fore.YELLOW + "-" * 69)
  print(Fore.YELLOW + "[!] The DES algorithm key is a special key that you will determine.")
  print(Fore.YELLOW + "    With this key, your messages are encrypted.") 
  print(Fore.YELLOW + "-" * 69)
  print(Fore.RED + "[?] You should forward this key to the person you wanna messaging.")
  print(Fore.YELLOW + "-" * 69)
  while(True):
    print(Fore.WHITE + " │")
    deskey = str(raw_input(Fore.WHITE + " └──=> DES Key (Must consist of 8 digits) : "))
    if re.match("^[a-zA-Z0-9_]*$", deskey) and len(deskey) == 8:
      print("  ")
      print("       Your DES Key : " + deskey)
      print(Fore.YELLOW + "-" * 69)
      print(Fore.YELLOW + "[!] The AES algorithm key is a special key that you will use.")
      print(Fore.YELLOW + "    With this key, the message encrypted with DES is encrypted again ") 
      print(Fore.YELLOW + "    with the AES algorithm. We have created a random AES key for you.") 
      print(Fore.WHITE + "    You should share this key with the person you are chatting with.")
      print(Fore.YELLOW + "-" * 69)
      print(Fore.RED + "[?] Don't forget to share DES and AES keys with your partner! ")
      print(Fore.RED + "    Your partner should choose the 'client' option.")
      print(Fore.YELLOW + "-" * 69)
      aeskey = randomString(16)
      print(Fore.GREEN + " │")
      print(Fore.GREEN + " └──=> Your AES KEY : " + aeskey)
      print(Fore.YELLOW + "-" * 69)
      start(deskey, ctype, aeskey)
    else:
      print(Fore.RED + "[!] Error! Only letters a-zA-Z0-9 allowed and DES Key should be consist of 8 digits!")

def ctype():
  ctype = str(raw_input(Style.BRIGHT + Fore.BLUE + ">>>" +  Style.RESET_ALL + " Are you client[1] or server[2] ? : "))
  while is_number_check(ctype) == True:
    if str(ctype) == "1": 
      client_based(ctype)
    elif str(ctype) == "2":
      server_based(ctype)
    else:
      print("Your choice should be 1 or 2 !")
      ctype = str(raw_input("Are you client[1] or server[2] ? : "))

while(True):
  nickname = str(raw_input(Style.BRIGHT + Fore.BLUE + ">>>" +  Style.RESET_ALL + " Nickname: ")) 
  if re.match("^[a-zA-Z0-9_]*$", nickname) and len(nickname) < 15:
    ctype()
  else:
    print(Fore.RED + "[!] Error! Only letters a-zA-Z0-9 allowed and username should not be longer than 15 digits!")
