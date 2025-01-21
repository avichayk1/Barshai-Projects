import os
from openpyxl import load_workbook
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

from_email_password = config.EMAIL_PASSWORD
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import datetime
def send_email(subject, body, to_email, from_email):


    if from_email_password is None:
        raise ValueError("Email password not set in environment variables")

    # Create the email
    msg = MIMEText(body)
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg['Subject'] = subject


    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp_server:
        smtp_server.login(from_email,from_email_password)
        smtp_server.sendmail(from_email,to_email,msg.as_string())
    print('messege sent!')


directory = r'C:\Users\AvichayKadosh\ברשאי\טכנולוגיה - Documents\שירותים\בקרות שטח\בקרות מסע לקוח\03- בדיקות\תוצאות בדיקה'
stpos_file_path = r'C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\gtfs\israel-public-transportation\stops.txt'
output_file_path=r'C:\Users\AvichayKadosh\ברשאי\טכנולוגיה - Documents\שירותים\בקרות שטח\בקרות מסע לקוח\03- בדיקות\תוצאות בדיקה'
# subject = "Test Email"
# body = "This is a test email from Python."
# to_email = "avichayk@barshai.co.il"
# from_email = "avichayk1@gmail.com"
# from_email_password = from_email_password
# smtp_server = "smtp.gmail.com"  # e.g., smtp.gmail.com for Gmail
# smtp_port = 587    # SSL port for Gmail
#
# send_email(subject, body, to_email, from_email)

def sort_digits(number):
    return ''.join(sorted(str(number)))
for filename in os.listdir(directory):
    if filename.endswith(".xlsx") and (filename == 'ריכוז שלטים.xlsx'  or filename == 'ריכוז מסופים.xlsx' or filename =="ריכוז נסיעות ברכב.xlsx"):  # Skip the output file
        # Read each Excel file into a DataFrame
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path, index_col=None)
        if(filename=="ריכוז נסיעות ברכב.xlsx"):
            df.rename(columns={'מקט תחנת עלייה': 'מק"ט תחנה'}, inplace=True)
        df = df.sort_values(by='מק"ט תחנה')
        for key, group in df.groupby('מק"ט תחנה'):
        # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                # print(key,"   ",row['מק"ט תחנה'])
                if(row['מק"ט תחנה']==23451 and key==32451):
                    s=5
                order_row=sort_digits(row['מק"ט תחנה'])
                order_key=sort_digits(key)
                if(key!=row['מק"ט תחנה'] and order_row== order_key):
                    s=row['מק"ט תחנה']
                    print(f"The wrong makat is: {s}")

                    # # Example usage
                    # subject = "Test Email"
                    # body = "This is a test email from Python."
                    # to_email = "avichayk@barshai.co.il"
                    # from_email = "avichayk@barshai.co.il"
                    # from_email_password = from_email_password
                    # smtp_server = "smtp-mail.outlook.com"  # e.g., smtp.gmail.com for Gmail
                    # smtp_port = 587  # SSL port for Gmail
                    #
                    # send_email(subject, body, to_email, from_email, from_email_password, smtp_server, smtp_port)

