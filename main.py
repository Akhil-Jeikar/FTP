from InquirerPy import inquirer
from InquirerPy.base import Choice

import Server
import Client

version='1.0.0.0'

if __name__ =="__main__":
    print(f"FTP\nFTPversion:{version}")
    mode=inquirer.select(message="Select the mode",
                         choices=   ["Sender","Receiver",
                                    Choice(value=None,name="Exit"),],
                                    default=None
                                    ).execute()
    if mode=="Sender":
        Server.start()
        
    if mode=="Receiver":
        Client.start()

