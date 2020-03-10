
```
                _____________________________________________________________________
               |_____________________________|DRAFTCHAT|_____________________________|
                ___________                          ___________
               ||         ||   If Privacy Matters   ||         || > Via single account      
               || SERVER  ||         ________       || CLIENT  || > Via single draft
               ||         ||        | ---- | \     _||         || > With AES and DES 
               ||         ||        | ---- |__\   / ||_________|| > %100 private chat
               |  + + + +  |        | -- -- - |  /  |  + + + +  |
                   _|_|_   \AES     | -DRAFT- | /AES    _|_|_
                  (_____)   \DES   _|_ - CHAT |/DES    (_____)
                             \    / |,\ ----- |
                      _______ \__|- ' -|______|
                     |       |/   \_,_/                   ~ Author : AkkuS @ehakkus
                     | TOKEN |    /    |_________|        ~ github.com / draftchat
                     |_______|   /      GMAIL API         ~ https://pentest.com.tr
                          \_____/
                                                               Version 1.0.0 (Stable)
               _____________________________________________________________________

```

<p align="center">
<img src="https://img.shields.io/badge/Python-2-yellow.svg"></a>
<a href="#"><img src="https://www.pentest.com.tr/images/Blackhat/blackhatUSA2020p.svg"></a>
<a href="#"><img src="https://www.pentest.com.tr/images/Defcon/defcon28p.svg"></a>
<a href="#"><img src="https://www.pentest.com.tr/projects/images/release.svg"></a>
</p>

## Purpose

**DRAFTCHAT** allows persons to chat through a single gmail account in the gmail that does not record drafts.
It encrypts the sent messages first with DES and then with the AES algorithm and writes them to the created draft.
The messages of the persons are written in encrypted form on the same draft. Messages can only be read with the correct keys to be determined.
In this way, a completely hidden chat room is created with a single gmail account.
Therefore, draftchat makes 100% private communication opportunity by turning a non-your mail server into a chat server.

GD (Gmail Draft) Chat is the first module. Modules will be added for other mail systems.(Yandex,Hotmail,Outlook,MailEnable etc.)

## Installation

Set up a common gmail account to chat with your patern.
Remember, you will only perform these operations once. You will not have to do these configurations every time you chat.

Complete the steps described in the rest of installation part to use DRAFTCHAT that makes requests to the Gmail API.

#### Prerequisites

To run GDchat, you'll need: 

+ Python 2.6 or greater
+ The pip package management tool
+ A Google account with Gmail enabled (Determined with your partner)

#### Step 1: Turn on the Gmail API

First of all, because we used Python Quickstart, **CLICK LINK BELOW**
+ https://developers.google.com/gmail/api/quickstart/python

+ Go to **Step 1** on the page.
+ Click on the **Enable the Gmail API** button.
+ In resulting dialog click **DOWNLOAD CLIENT CONFIGURATION** and save the file **credentials.json** to your DRAFTCHAT directory. 

#### Step 2: Install the Google Client Library

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### Step 3: Run DRAFTCHAT and Create Token

```
python draftchat.py
```

+ DRAFTCHAT will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser.
  If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

+ Click the **Accept** button.

+ The DRAFTCHAT will proceed automatically, and you may close the window/tab. **token.pickle** will be created on your DRAFTCHAT directory.

The **token.pickle** will hold your authentication processes and you will not need to repeat the above processes unless you delete this file.
You can share this file directly with your partner. Therefore, your partner does not need to do the same processes.

## Usage

After running Draftchat, it will first ask you for your nickname. 

<p align="center">
<img src="https://www.pentest.com.tr/projects/images/usage1.png" height="%70" width="70%">
</p>

Once you have determined your nickname, you must determine whether you want to be a **server** or a **client**.
Client-Server relationship logic is very simple. If you want to be a server, the DES and AES keys that you determine will be used.
If you choose to be a client, you have to get the keys for these algorithms from your server partner.
+ Let's say you choose the server option.

<p align="center">
<img src="https://www.pentest.com.tr/projects/images/usage2.png" height="%70" width="70%">
</p>

After determined an 8-digit DES key, draftchat generates a 16-digit random AES key for you.
And a new draft is created for the chat room. Then your client partner is expected. So you need to pass these keys over to your partner.

+ Let's take a look at the client option. 

Necessary keys are taken and entered from the server partner. If the keys are wrong or there is no server waiting for the client, the program will give an error.

<p align="center">
<img src="https://www.pentest.com.tr/projects/images/usage3.png" height="%70" width="70%">
</p>

The taken keys were entered and the information was verified. You can then communicate with your partner in peace of mind.

<p align="center">
<img src="https://www.pentest.com.tr/projects/images/usage4.png" height="%70" width="70%">
</p>

#### DRAFTCHAT GDchat module - Introduction and Usage (Youtube)

[![DRAFTCHAT GDchat module - Introduction and Usage](https://www.pentest.com.tr/projects/images/usage5.png)](https://www.youtube.com/watch?v=TxmNtgga5Io "DRAFTCHAT GDchat module - Introduction and Usage")

## About the Responsibilities

The fact that you are offered a private chat room does not mean that the communication you provide while using this tool may be **illegal**.
Remember that all the responsibility belongs to you.
