#importing

import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from email.mime.text import MIMEText
import os
import zipfile


#define a function

def mrMailer(smtp_server, smtp_port, fileToAttach):

    #check whether the file is exists or not

    if os.path.exists(fileToAttach):

        zipfilename = fileToAttach

        # checking whether this file has an extension or not

        if "." in zipfilename:

            zipfilename = fileToAttach.split(".")[0]

        else:
            # or you can do nothing as out file name already stored in zipfilename
            zipfilename = fileToAttach

    else:
        #"return error if file not exist"
        return "'ERROR': File Not Exist\nPlease enter the valid name of the file"

    #compress the file in ".zip" format

    zipping = zipfile.ZipFile(zipfilename+".zip", "w", zipfile.ZIP_DEFLATED)

    # write the file
    zipping.write(fileToAttach)

    #close the new zipped file
    zipping.close()

    # add sender and reciever email address

    sender = "your_email"
    senderPassword = "your_password"

    reciever = "reciever's_email"


    # create a variable to store the instance of MIMEMultipart

    mail = MIMEMultipart()

    # store the sender's email address and sender's name

    mail['from'] = formataddr((str(Header("your_name", "utf-8")), sender))

    #store the reciever's email address

    mail['To'] = reciever

    # store the subject of the mail

    mail['Subject'] = "SUBJECT_OF_THE_EMAIL"

    # body of the email
    # edit the sentence in single quote to change

    body = """<!DOCTYPE html>
     <html>
     <head>
     </head>
     <body>"""+'BODY_OF_THE_EMAIL'+ """</body>
     </html>"""

    # now attaching the body with mail instance we created

    mail.attach(MIMEText(body, 'html'))

    zipfilename = zipfilename +'.zip'
    attachment = open(zipfilename, "rb")

    # create a variable to store the instance of MIMEBase

    base = MIMEBase('application', 'octet-stream')

    #set the payload in

    base.set_payload((attachment).read())

    # encode it into base64

    encoders.encode_base64(base)

    base.add_header("Content-Disposition", "attachment; filename = %s" %zipfilename)

    # attach the MIMEMultipart instance (mail) to MIMEBase instance(base)

    mail.attach(base)
    print("Connecting... Please Wait\n")
    # start the session
    session = smtplib.SMTP(smtp_server, smtp_port)

    #start with tls 

    session.starttls()

    #Add crendentials to authenticate

    session.login(sender, senderPassword)
    print("Connected")

    #change the mail instance to string

    text = mail.as_string()

    #finally send the email
    print("Your email is being sent\n")
    session.sendmail(sender, reciever, text)


    print("Email Sent Successfully")
    #after sending close the session

    session.quit()



#fileToAttach

file = input("Please enter the file to attach: ")

# enter the smtp_server (for gmail it is 'smtp.gmail.com')
smtp_server = input("Enter the smtp server: ")

#enter the port for the smtp_server (for gmail you can use 587)
smtp_port = int(input("Enter the port no for smtp server: "))

#call the function
mrMailer(smtp_server, smtp_port, file)





