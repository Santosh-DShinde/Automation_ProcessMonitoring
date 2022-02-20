""" Design automation script which accept directory name and mail id from user and create log file in that directory,
which contains information of running processes as its name, PID, Username. After creating log file send that log file
to the specified mail.A """

import os.path
import psutil
import schedule
import smtplib
import time
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import *
from urllib.request import urlopen


def is_connected():
    try:
        urlopen("https://www.google.co.in/", timeout=1)
        return True
    except Exception as obj:
        return False


def Create_Files(DirName):
    global AbsPath, fd
    File_Name = "LogFile" + datetime.now().strftime("%H-%M-%S") + ".txt"
    if not os.path.exists(DirName):
        os.mkdir(DirName)
    for root, dir, file in os.walk("."):
        for dirnames in dir:
            AbsPath = os.path.join(os.getcwd(), DirName, File_Name)
            if not os.path.exists(AbsPath):
                fd = open(AbsPath, "a")
                Heading = "=" * 80
                fd.write(Heading)
                fd.write(f"\nRecord Of Running Process On This Machine \n")
                fd.write(Heading)
                fd.write("\n")

    Process_Monitoring()
    mail_Sending(File_Name)


def Process_Monitoring():
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            fd.write("\n")
            fd.write(str(pinfo))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    fd.close()


def mail_Sending(File_Name):
    try:
        Sender = "shindesan3047@gmail.com"
        Receiver = argv[2]
        password = "Darshan@1889"
        msg = MIMEMultipart()
        msg['From'] = Sender
        msg['To'] = Receiver
        Subject = """
    Process log generated at : %s """ % (datetime.now().strftime("%H-%M-%S"))
        msg['Subject'] = Subject
        body = """
    Hello %s,  
    Please find attached document which contains Log of Running  Process
    Log file is created at : %s 
        
    This is auto generated mail.
                       \n\n\n\n 
                                        Thank & Regards,
                                        Santosh  Shinde
        """ % (Receiver, datetime.now().strftime("%H_%M_%S"))

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(AbsPath, "rb")

        p = MIMEBase('application', 'octet-stream')

        p.set_payload(attachment.read())
        encoders.encode_base64(p)

        p.add_header('content -Disposition', "attachment;  filename= %s " % File_Name)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(Sender, password)

        text = msg.as_string()

        s.sendmail(Sender, Receiver, text)

        s.quit()

        print("Log File sent through mail")

    except Exception as obj:
        print("Exception Occurred : ", obj)


def main():
    print("--------Automation Script by : Santosh Shinde ---------\n")
    print(f"Application Name is :", argv[0].split(".")[0], "\n")
    if len(argv) < 2 or len(argv) > 3:
        print('''Error : Argument error
For help  : -h or -H
For Usage : -u or -U''')

    if len(argv) == 2:

        if argv[1] == "-h" or argv[1] == "-H":
            print("""Help : 
This Application accepts two commandline arguments 
first argument is Directory name
second argument is mail id of receiver
Expected syntax : Application_Name.py  Directory_Name  Receiver_Mail_ID""")

        elif argv[1] == "-u" or argv[1] == "-U":
            print("""Usage : the use of this application is gets the records of running processes of our computer and 
write into logFile and after writing record into file send that LogFile through Gmail""")

    if len(argv) == 3:

        if is_connected():
            print("Processing....🔍")
            try:
                schedule.every(15).seconds.do(Create_Files, argv[1])
                # schedule.every().minute.at(":01").do(Create_Files, argv[1])
                # schedule.every().hour.at(":01").do(Create_Files, argv[1])
                # schedule.every().day.at("10:30").do(Create_Files, argv[1])
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except Exception:
                print("""Error : Invalid Arguments
Check your arguments or contact to developer""")
        else:
            print("Error : Connection failed, Please check your internet connection")


if __name__ == "__main__":
    main()
