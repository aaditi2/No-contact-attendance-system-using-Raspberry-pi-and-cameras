import face_recognition
import os
import time
import cv2
import datetime
import csv
import numpy as np
import os
from matplotlib import pyplot as plt

import email, smtplib,ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Encoding the dataset")
encode_lst=[]
attendance_lst=[]
#path of the stored images(dataset folder)
pathOut = r"path/to/your/folder/of/images"
dir_list= os.listdir(pathOut)
#traversing through each of the image
for f in dir_list:
    image_path = os.path.abspath(os.path.join(pathOut, f))
    image1=face_recognition.load_image_file(image_path)
        
    faceLocTest = face_recognition.face_locations(image1)[0]
    encodeTest = face_recognition.face_encodings(image1)[0]
    encode_lst.append(encodeTest)
print("Done with encodings..")
print("Marking the attendance")
#for class of 2 students
for click in range(2):
    print("Next student....")
    print("Student:" +str(click +1))
    print("Adjust your face properly in front of the camera")
    print("Image will get captured in 15 secs")
    time.sleep(15)
    os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/No_contact_attendance/sample_photo/image.jpg') # uses Fswebcam to take picture
    print("Image captured successfully")

    print("Face recognition process is going on")
    #path of the captured image by the camera
    student= face_recognition.load_image_file(r"/path/image.jpg") #image gets loaded
    #convert the colour image to RGB
    student= cv2.cvtColor(student, cv2.COLOR_BGR2RGB)
    
    #finds faces in the image
    #as the image contains only one face index 0 is used.
    faceLoc = face_recognition.face_locations(student)[0]
    #features are encoded-->128 measurements
    encode_student = face_recognition.face_encodings(student)[0]
  

    #compares all 128 measurements and finds out the difference
    results = face_recognition.compare_faces(encode_lst, encode_student)

    print(results)
    count=0
    for r in range(len(results)):
        if results[r]==True:
            x = datetime.datetime.now()#time,date
            s= z+"  "+ x.strftime("%c")#concatinating name and time
            attendance_lst.append(s)#appending it in the present student list
        else:
            count= count+1
    if count==len(results):
        print("Unknown face is detected, attendance not marked.")


    
    
#opens the csv file in append mode        
w= open("attendance.csv","a",newline="")
c=csv.writer(w)
#csv file is appended with the present student list

c.writerow(attendance_lst)

w.close()
print(attendance_lst)
print("Attendance updated on the sheet")

ans= input("Do you want to mail the attendance sheet?[y/n]")
if ans=="y":
    #sending an email
    subject = "Attendance" + datetime.datetime.now().strftime
    body = "PFA csv file of today's attendance"
    sender_email = "sender@gmail.com"
    receiver_email = "receiver@gmail.com"
    password = input("Type your password and press enter:") //the sender has to set up a password on his/her gmail acc. 

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Attendance"] = subject
    message["BCC"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "attendance.csv"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
