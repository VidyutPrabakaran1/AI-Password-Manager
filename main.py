'''
AI Password Manager

Copyright (c) 2024 Vidyut Prabakaran

'''

'''
Release Notes (v2.0)(ClearOut)
 - APM Accounts - Introducing a new Backup & Restore system, you can now create a new APM account and backup your credentials and restore them on another computer !
 - Streamer Mode - Let's you use APM while streaming or recording your screen without your passwords being visible.
 - Background Music [FE] - Plays music in the background when using APM. [ID:1]
 - Bug Fixes

'''

# IMPORTS

from tkinter import *
from tkinter import messagebox
import webbrowser
import requests
import json
import zxcvbn
import pickle
import os
import sys
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet, InvalidToken
from PIL import Image, ImageTk
from time import sleep
from tkinter import PhotoImage
import gspread
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import base64
import cv2
import ctypes
from random import randint
import smtplib
from email.mime.text import MIMEText
import geocoder

# Globals

key_def = b''
fernet_def = Fernet(key_def)

script_dir = os.path.dirname(sys.argv[0])

json_path = '_itnrl/apm-db.json'
credentials_path = os.path.join(script_dir, json_path)

SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

# Load the credentials and specify the scope
credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet = gc.open('APM-DB').sheet1

# PATHS

dir_init = os.path.expanduser('~')
local_appdata = os.getenv('LOCALAPPDATA')
config_fl_nme = 'config.txt'
trans_fl_nme = 'trans.txt'
txtclr_fl_nme = 'txt_clr.txt'
btnclr_fl_nme = 'btn_clr.txt'
btnclr1_fl_nme = 'btn_clr1.txt'
bgclr_fl_nme = 'bg_clr.txt'
mp_fl_nme = 'mp.mp'
bg_fl_nme = 'wallpaper.jpg'
cred_fl_nme = 'credentials.pkl'

home_directory_fr_cred = os.path.expanduser('~')

usr_path_with_cnfg_fl = os.path.join(local_appdata, 'APM', config_fl_nme)
usr_path_with_trns_fl = os.path.join(local_appdata, 'APM', trans_fl_nme)
usr_path_with_txtclr_fl = os.path.join(local_appdata, 'APM', txtclr_fl_nme)
usr_path_with_btnclr_fl = os.path.join(local_appdata, 'APM', btnclr_fl_nme)
usr_path_with_btnclr1_fl = os.path.join(local_appdata, 'APM', btnclr1_fl_nme)
usr_path_with_bgclr_fl = os.path.join(local_appdata, 'APM', bgclr_fl_nme)
usr_path_with_mp_fl = os.path.join(local_appdata, 'APM', mp_fl_nme)
usr_path_with_bg_fl = os.path.join(local_appdata, 'APM', bg_fl_nme)
cred_full_path = os.path.join(home_directory_fr_cred, cred_fl_nme)

script_dir_forbg = os.path.dirname(sys.argv[0])
bg_path = os.path.join(script_dir_forbg, 'wallpaper.jpg')

cmn_pwds_path = os.path.join(script_dir_forbg, '_itnrl/10M.txt')
apm_ico_full_path = os.path.join(script_dir_forbg, '_itnrl/apm.png')
hfsconfig1 = os.path.join(script_dir_forbg, '_itnrl/hfsconfig1.txt')
fer_path = os.path.join(local_appdata, 'APM', 'fer.apm')

acc_status_filepath = os.path.join(local_appdata, 'APM','acc_stat.txt')
acc_usrnme_flpath = os.path.join(local_appdata, 'APM', 'acc_usrnme.apm')
acc_pwd_flpath = os.path.join(local_appdata, 'APM', 'acc_pwd.apm')

apm_logo_flpath = os.path.join(script_dir, '_itnrl', 'apm_logo.png')

license_flpath = os.path.join(script_dir, '_itnrl', 'LICENSE.txt')

# FUNCTIONS

def about():
    def license():
        os.system(f'notepad {license_flpath}')

    about_win = Toplevel(win)
    about_win.title("AI Password Manager - About")
    about_win.geometry('715x275')
    about_win.configure(background='black')
    about_win.resizable(False, False)

    apm_logo = PhotoImage(file=apm_logo_flpath)
    about_win.image = apm_logo

    apm_logo_lbl = Label(about_win, image=apm_logo)
    apm_logo_lbl.grid(row=0, column=0, padx=25, pady=45)

    apm_lbl = Label(about_win, text="AI Password Manager", font=('Arial', 18), fg='white', bg='black')
    apm_lbl.place(x=350, y=45)

    apm_ver = Label(about_win, text="Version: 2.0", font=('Arial', 15), fg='white', bg='black')
    apm_ver.place(x=350, y=95)

    apm_dev = Label(about_win, text="Developed by: Vidyut Prabakaran", font=('Arial', 15), fg='white', bg='black')
    apm_dev.place(x=350, y=125)

    apm_cntct = Label(about_win, text="Contact: vidyutprabakaran@gmail.com", font=('Arial', 15), fg='white', bg='black')
    apm_cntct.place(x=350, y=155)

    apm_lcnse = Button(about_win, text="  License  ", fg='black', bg='white', command=license)
    apm_lcnse.place(x=353, y=195)

def fer_chk():

    os.makedirs(os.path.dirname(fer_path), exist_ok=True)

    if os.path.exists(fer_path):
        with open(fer_path, "rb") as keyfile:
            key = keyfile.read()

    else:
        key = Fernet.generate_key()
        with open(fer_path, 'wb') as keyfile:
            keyfile.write(key)

    if not isinstance(key, bytes) or len(key) != 44:  # A valid Fernet key is 44 bytes long
        raise ValueError("Generated or loaded key is invalid.")
        #print("h")

    return key

key = fer_chk()
loaded_ferkey = Fernet(key)

def bgm_win():
    bgmwin = Toplevel(win)
    pass

def bgm():
    with open(hfsconfig1, 'r') as file:
        val1 = file.read()
        if val1 == '1':
            music_btn.place(x=20, y=530)
        else:
            pass

def add_email(email):
    col_d_values = sheet.col_values(4)  # This checks for the last filled password cell
    row_index = len(col_d_values)  # Same row as the password
    sheet.update_cell(row_index, 5, email)  # Update the email in column E

def add_ID_num():
    col_values = sheet.col_values(1)
    row_index = len(col_values) + 1

    if len(col_values) > 1:
        last_id = int(col_values[-1])
        next_id = last_id + 1
    else:
        next_id = 1

    sheet.update_cell(row_index, 1, next_id)

def chk_usrnme(usrnme):
    col_c_values = sheet.col_values(3)
    if usrnme in col_c_values:
        messagebox.showinfo("APM Accounts", f"The username '{usrnme}' already exists.")
        return "no"
    else:
        return "yes"

def add_usrnme(usrnme):
    col_c_values = sheet.col_values(3)
    row_index = len(col_c_values) + 1
    sheet.update_cell(row_index, 3, usrnme)

def add_pwd(pwd):
    col_c_values = sheet.col_values(4)
    row_index = len(col_c_values) + 1
    sheet.update_cell(row_index, 4, pwd)

def authenticate_drive():
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload_to_drive(service, file_path, new_name):
    file_metadata = {'name': new_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def create_shareable_link(service, file_id):
    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }
    service.permissions().create(fileId=file_id, body=request_body).execute()
    file = service.files().get(fileId=file_id, fields='webViewLink').execute()
    return file.get('webViewLink')

def overwrite_file_on_drive(service, file_name, file_path):
    # Search for the file by name
    results = service.files().list(q=f"name='{file_name}'", fields="files(id, name)").execute()
    items = results.get('files', [])

    if items:
        # If the file exists, delete it
        for item in items:
            service.files().delete(fileId=item['id']).execute()
    # Upload the new file
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def get_row_index():
    with open(acc_usrnme_flpath, 'r') as f:
        usrnme = f.read()
    usernames = sheet.col_values(3)
    return usernames.index(usrnme) + 1

def apm_func():
    def chk_acc_status():
        try:
            with open(acc_status_filepath, 'r') as file:
                val = file.read()
                return val
            
        except(FileNotFoundError):
            with open(acc_status_filepath, 'w') as file:
                file.write("0")
            with open(acc_status_filepath, 'r') as file:
                val = file.read()
                return val
            
    stat = chk_acc_status()
    #print(stat)

    if stat == "1":
        def logout():
            with open (acc_status_filepath, 'w') as file:
                file.write("0")
            
            os.remove(acc_usrnme_flpath)
            os.remove(acc_pwd_flpath)

            messagebox.showinfo("APM Accounts", "Logged out.")
            signedin_apmpanel.destroy()

        def backup():
            with open (acc_usrnme_flpath, 'r') as file:
                usrnme = file.read()
            usernames = sheet.col_values(3)
            row_index = get_row_index()

            account_id = sheet.cell(row_index, 1).value
            new_name = f"credentials{account_id}.pkl"
            new_cred_path = os.path.join(home_directory_fr_cred, new_name)
            os.rename(cred_full_path, new_cred_path)

            messagebox.showinfo("APM Accounts", "Backing up... Do not exit APM.")

            service = authenticate_drive()
            file_id = overwrite_file_on_drive(service, new_name, new_cred_path)
            drive_link = create_shareable_link(service, file_id)
            sheet.update_cell(row_index, 2, drive_link)

            os.rename(new_cred_path, cred_full_path)

            fer_path = os.path.join(local_appdata, 'APM', 'fer.apm')
            if os.path.exists(fer_path):
                new_ferkey_name = f"fer{account_id}.apm"
                new_ferkey_path = os.path.join(local_appdata, 'APM', new_ferkey_name)
                os.rename(fer_path, new_ferkey_path)
                #print("\nBacking up ferkey.apm...")

                ferkey_file_id = overwrite_file_on_drive(service, new_ferkey_name, new_ferkey_path)
                ferkey_drive_link = create_shareable_link(service, ferkey_file_id)
                sheet.update_cell(row_index, 6, ferkey_drive_link)
                os.rename(new_ferkey_path, fer_path)
                #print("\nBackup complete for fer.apm!")
                messagebox.showinfo("APM Accounts", "Backup complete !")

            else:
                #print("fer.apm not found. Skipping backup for this file.")
                pass

        def restore():
            row_index = get_row_index()
            drive_link = sheet.cell(row_index, 2).value
            if not drive_link:
                #print("No backup link found for this account.")
                return

            file_id = drive_link.split('/')[-2]
            home_dir1 = os.path.expanduser('~')
            file_path = os.path.join(home_dir1, "credentials.pkl")
            service1 = authenticate_drive()
            request = service1.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            ferkey_drive_link = sheet.cell(row_index, 6).value
            if not ferkey_drive_link:
                return

            ferkey_file_id = ferkey_drive_link.split('/')[-2]
            ferkey_file_path = os.path.join(os.path.expanduser('~'), "fer.apm")
            ferkey_request = service1.files().get_media(fileId=ferkey_file_id)
            ferkey_fh = io.FileIO(ferkey_file_path, 'wb')
            ferkey_downloader = MediaIoBaseDownload(ferkey_fh, ferkey_request)

            done = False
            while not done:
                status, done = ferkey_downloader.next_chunk()

            messagebox.showinfo("APM Accounts", "Restore complete !")
            messagebox.showinfo("APM Accounts", "Restart the program to apply the changes.")
            quit()

        with open (acc_usrnme_flpath, 'r') as file:
            signedin_usrnme = file.read()

        signedin_apmpanel = Toplevel(win)
        signedin_apmpanel.title(f"APM Accounts - {signedin_usrnme}")
        signedin_apmpanel.geometry('500x300')
        signedin_apmpanel.configure(background='black')
        signedin_apmpanel.resizable(False, False)

        apm_lbl1 = Label(signedin_apmpanel, text="APM Accounts", font=('Arial', 18), fg='white', bg='black')
        apm_lbl1.pack(side=LEFT, padx=20)

        backup_btn = Button(signedin_apmpanel, text="          Backup          ", fg='black', bg='white', command=backup)
        backup_btn.pack(side=TOP, pady=(115, 10))

        restore_btn = Button (signedin_apmpanel, text="          Restore          ", fg='black', bg='white', command=restore)
        restore_btn.pack(side=TOP, pady=(10, 0))

        logout_btn = Button (signedin_apmpanel, text="Logout", fg='black', bg='white', command=logout)
        logout_btn.place(x=440, y=260)

    elif stat == "0":
        def apm_signin_acc():
            script_dir = os.path.dirname(sys.argv[0])
            json_path = '_itnrl/apm-db.json'
            json_fullpath = os.path.join(script_dir, json_path)

            SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file(json_fullpath, scopes=SCOPES)
            gc = gspread.authorize(credentials)
            sheet = gc.open('APM-DB').sheet1

            def send_verification_email(email_addr, code):
                ip = geocoder.ip("me")

                sender_email = "apm.officialnoreply@gmail.com"  # Replace with your email
                sender_password = ""      # Replace with your email password or app-specific password
                subject = "AI Password Manager - Verification Code"
                body = f"Your APM verification code is : {code} . Sign In requested from {ip.city}, {ip.state}, {ip.country}. Do not share this code to anyone. If you didn't request this, someone may have your password."

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = email_addr

                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, email_addr, msg.as_string())
                    messagebox.showinfo("Verification", "Verification email sent.")
                except Exception as e:
                    messagebox.showerror("Verification", f"Failed to send verification email: {e}")


            def sign_in():
                usrnme = apm_usrnme_entry1.get()
                pwd = apm_pwd_entry1.get()
                usernames = sheet.col_values(3)
                if usrnme in usernames:
                    row_index = usernames.index(usrnme) + 1
                    hashed_pwd = sheet.cell(row_index, 4).value

                    pwd_bytes = base64.urlsafe_b64decode(hashed_pwd.encode('utf-8'))
                    pwd_decrypted = fernet_def.decrypt(pwd_bytes)
                    pwd_decrypted_str = pwd_decrypted.decode()

                    if pwd_decrypted_str == pwd:
                        email_addr = sheet.cell(row_index, 5).value
                        #messagebox.showinfo("APM Accounts", f"Logged in to : {usrnme}")
                        apm_pwd_entry1.delete(0, END)
                        apm_usrnme_entry1.delete(0, END)
                        
                        verification_code = randint(100000, 999999)
                        send_verification_email(email_addr, verification_code)
                        #print(verification_code)

                        apmswin.destroy()

                        def chk_vrfc_code():
                            entrd_code = vrfc_entry.get()
                            #print(entrd_code)

                            if int(entrd_code) == verification_code :
                                with open (acc_usrnme_flpath, 'w') as file:
                                    file.write(usrnme)

                                encrypted_acc_pwd = fernet_def.encrypt(pwd.encode())
                                with open (acc_pwd_flpath, 'wb') as file:
                                    file.write(encrypted_acc_pwd)

                                with open (acc_status_filepath, 'w') as file:
                                    file.write("1")

                                messagebox.showinfo("APM Accounts", f"Successfully logged in to: {usrnme}.")
                                apm_vrfc_win.destroy()

                            else:
                                messagebox.showerror("Verification Code", "Incorrect verification code. Try again.")
                    
                        apm_vrfc_win = Toplevel(win)
                        apm_vrfc_win.title("APM Accounts - Verification Code")
                        apm_vrfc_win.geometry('350x150')
                        apm_vrfc_win.configure(background='black')
                        apm_vrfc_win.resizable(False, False)

                        vrfc_lbl = Label (apm_vrfc_win, text="APM Verification Code", font=('Arial', 18), fg='white', bg='black')
                        vrfc_lbl.pack(pady=10)

                        vrfc_entry = Entry(apm_vrfc_win, width=30)
                        vrfc_entry.pack(pady=10)

                        vrfc_btn = Button(apm_vrfc_win, text="Verify", fg='black', bg='white', command=chk_vrfc_code)
                        vrfc_btn.pack(pady=10)
                    else:
                        messagebox.showerror("APM - Accounts", "Incorrect password.")

                else:
                    messagebox.showerror("APM - Accounts", "Username not found.")

            apm_win.destroy()

            apmswin = Toplevel(win)
            apmswin.title("APM Accounts - Sign In")
            apmswin.geometry('500x300')
            apmswin.configure(background='black')
            apmswin.resizable(False, False)

            apm_lbl1 = Label(apmswin, text="APM Accounts", font=('Arial', 18), fg='white', bg='black')
            apm_lbl1.pack(side=LEFT, padx=20)

            apm_usrnme_entry1 = Entry(apmswin , width=30)
            apm_usrnme_entry1.place(x=260, y=130)
            apm_usrnme_entry1.insert(0, "Enter your username")

            apm_pwd_entry1 = Entry(apmswin, width=30)
            apm_pwd_entry1.place(x=260, y=160)
            apm_pwd_entry1.insert(0, "Enter your password")

            apm_signin_acc_btn = Button(apmswin, text="  Sign In  ", fg='black', bg='white', command=sign_in)
            apm_signin_acc_btn.place(x=320, y=200)


        def apm_crte_acc():
            messagebox.showinfo("APM Accounts", "Creating your account, this may take a while. Please wait.")

            script_dir = os.path.dirname(sys.argv[0])
            json_path = '_itnrl/apm-db.json'
            json_fullpath = os.path.join(script_dir, json_path)

            SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file(json_fullpath, scopes=SCOPES)
            gc = gspread.authorize(credentials)
            sheet = gc.open('APM-DB').sheet1

            def add_email(email):
                col_d_values = sheet.col_values(4)  # This checks for the last filled password cell
                row_index = len(col_d_values)  # Same row as the password
                sheet.update_cell(row_index, 5, email) 

            def add_pwd(pwd):
                col_c_values = sheet.col_values(4)
                row_index = len(col_c_values) + 1
                sheet.update_cell(row_index, 4, pwd)

            def add_usrnme(usrnme):
                col_c_values = sheet.col_values(3)
                row_index = len(col_c_values) + 1
                sheet.update_cell(row_index, 3, usrnme)

            def add_ID_num():
                col_values = sheet.col_values(1)
                row_index = len(col_values) + 1

                if len(col_values) > 1:
                    last_id = int(col_values[-1])
                    next_id = last_id + 1
                else:
                    next_id = 1

                sheet.update_cell(row_index, 1, next_id)

            def chk_usrnme(usrnme):
                col_c_values = sheet.col_values(3)
                if usrnme in col_c_values:
                    messagebox.showerror("APM Accounts", f"The username '{usrnme}' already exists.")
                    return "no"
                
                elif usrnme == "Enter a username":
                    messagebox.showerror("APM Accounts", "Enter a valid username.")
                    return "no"
                
                elif usrnme == "":
                    messagebox.showerror("APM Accounts", "Enter a valid username.")
                    return "no"

                else:
                    return "yes"

            pwd_get = apm_pwd_entry.get() # raw password
            pwd_encrypted = fernet_def.encrypt(pwd_get.encode()) # encrypt it
            pwd = base64.urlsafe_b64encode(pwd_encrypted).decode('utf-8') # convert to string

            usrnme = apm_usrnme_entry.get()

            if chk_usrnme(usrnme) == "no":
                pass
            elif chk_usrnme(usrnme) == "yes":
                email = apm_crte_acc_email.get()
                if email == "Enter your email":
                    messagebox.showerror("APM Accounts", "Enter your email address.")
                    pass
                else:
                    add_ID_num()
                    add_usrnme(usrnme)
                    add_pwd(pwd)
                    add_email(email)

                    messagebox.showinfo("APM Accounts", "Account created successfully.")
                    apm_win.destroy()

                    apm_signin_acc()

            else:
                messagebox.showerror("Error", "Unable to create account.")

        apm_win = Toplevel(win)
        apm_win.title("APM Accounts")
        apm_win.geometry('500x300')
        apm_win.configure(background='black')
        apm_win.resizable(False, False)

        apm_lbl = Label(apm_win, text="APM Accounts", font=('Arial', 18), fg='white', bg='black')
        apm_lbl.pack(side=LEFT, padx=20)

        apm_usrnme_entry = Entry(apm_win , width=30)
        apm_usrnme_entry.place(x=260, y=100)
        apm_usrnme_entry.insert(0, "Enter a username")

        apm_pwd_entry = Entry(apm_win, width=30)
        apm_pwd_entry.place(x=260, y=130)
        apm_pwd_entry.insert(0, "Enter a password")

        apm_crte_acc_email = Entry(apm_win, width=30)
        apm_crte_acc_email.place(x=260, y=160)
        apm_crte_acc_email.insert(0, "Enter your email")

        apm_crte_acc_btn = Button(apm_win, text="Create Account", fg='black', bg='white', command=apm_crte_acc)
        apm_crte_acc_btn.place(x=305, y=200)

        apm_signin_btn = Button(apm_win, text="Sign In", fg='black', bg='white', command=apm_signin_acc)
        apm_signin_btn.place(x=445, y=265)

    else:
        #print("smth off")
        pass

def reset():
    def yes():
        try:
            def check_mp():
                entry_mp_get = entry_mp.get()
                if mp_fl_cntnts == entry_mp.get():
                    try:
                        os.remove(usr_path_with_cnfg_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_trns_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_txtclr_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_btnclr_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_btnclr1_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_bgclr_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(usr_path_with_bg_fl)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.remove(cred_full_path)
                    except(FileNotFoundError):
                        pass

                    try:
                        os.rename(fer_path, 'fer_deleted.apm')
                    except(FileExistsError):
                        os.rename('fer_deleted.apm', 'fer_deleted1.apm')
                    except(FileNotFoundError):
                        pass

                    messagebox.showinfo("Restart", "APM has been sucessfully reset, please restart the program.")

                    reset_win.destroy()
                    mp_fl_fnd.destroy()
                    #sys.exit()
                    quit()
                else:
                    messagebox.showerror("Master Password", "Incorrect Master Password.")

            with open (usr_path_with_mp_fl, 'r') as mp_fl:
                mp_fl_cntnts = mp_fl.read()
            mp_fl_fnd = Toplevel(win)
            mp_fl_fnd.title("Master Password Required")
            mp_fl_fnd.geometry('350x160')
            mp_fl_fnd.resizable(False, False)
            mp_fl_fnd.configure(background='black')

            dropdown_menu.place_forget()
            pwd_hide_btn.place_forget()
            pwd_show_btn.place_forget()
            delete_cred_btn.place_forget()
            pwd_entry.place_forget()

            title_mp = Label(mp_fl_fnd, text="Master Password Required", font=('Arial', 16), fg='white', bg='black')
            title_mp.pack(pady=20)

            entry_mp = Entry(mp_fl_fnd, width=40, show='*')
            entry_mp.pack(pady=5)

            enter_btn = Button(mp_fl_fnd, text="        Enter      ", fg='black', bg='white', command=check_mp)
            enter_btn.pack(pady=10)
        
        except FileNotFoundError:
            def set_mp():
                entry_mp_cntnts = entry_mp.get()
                with open(usr_path_with_mp_fl, 'w') as mp:
                    mp.write(entry_mp_cntnts)
                messagebox.showinfo("Master Password", "Master Password set successfully.")
                mp_nt_fnd.destroy()

            mp_nt_fnd = Toplevel(win)
            mp_nt_fnd.title("Master Password Creation")
            mp_nt_fnd.geometry('350x160')
            mp_nt_fnd.resizable(False, False)
            mp_nt_fnd.configure(background='black')

            title_mp = Label(mp_nt_fnd, text="Master Password Creation", font=('Arial', 16), fg='white', bg='black')
            title_mp.pack(pady=20)

            entry_mp = Entry(mp_nt_fnd, width=40)
            entry_mp.pack(pady=5)

            enter_btn = Button(mp_nt_fnd, text="        Set      ", fg='black', bg='white', command=set_mp)
            enter_btn.pack(pady=10)

    def no():
        reset_win.destroy()

    reset_win = Toplevel(win)
    reset_win.title("Reset")
    reset_win.geometry('500x350')
    reset_win.configure(background='red')
    reset_win.resizable(False, False)

    warning_txt = Label(reset_win, text="WARNING", font=('Arial', 16), fg='white', bg='red')
    warning_txt.pack(pady=15)

    warning_txt = Label(reset_win, text=" - This will DELETE all YOUR CREDENTIALS !!", font=('Arial', 16), fg='white', bg='red')
    warning_txt.pack(pady=15)

    warning_txt1 = Label(reset_win, text=" - This will reset your customizations.", font=('Arial', 16), fg='white', bg='red')
    warning_txt1.pack(pady=20)

    warning_txt2 = Label(reset_win, text="Do you wish to continue ?", font=('Arial', 16), fg='white', bg='red')
    warning_txt2.pack(pady=25)

    yes_btn = Button(reset_win, text="      Yes       ", command=yes)
    yes_btn.pack(side=BOTTOM, pady=5)

    no_btn = Button(reset_win, text="      No      ", command=no)
    no_btn.pack(pady=5)

def chk_lclapdt_fldr():
    target_folder_path = os.path.join(local_appdata, 'APM')
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)
    else:
        pass

def cmn_pwds_chk():
    try:
        with open (cmn_pwds_path, 'r') as file:
            cmn_pwds = file.read()
            
            usr_cmn_pwd = cmn_pwds_chk_etry.get()
            
            if usr_cmn_pwd in cmn_pwds:
                cmn_pwds_result_text.set("Frequently Used. Unsafe Password.")
            elif usr_cmn_pwd == "":
                cmn_pwds_result_text.set("Please enter a password to check.")
            else:
                cmn_pwds_result_text.set("Not Frequently Used. Safe Password.")

    except Exception as e:
        messagebox.showerror(f"Error", "Unable to check password.")
        #print(e)

def scrn_sz_chk():
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    if screen_width < 1280 or screen_height < 720:
        messagebox.showwarning("Low Resolution Warning", f"Your screen resolution is {screen_width}x{screen_height}, For comfortable usage, please use a resolution of atleast 1280x720.")
    else:
        pass

def m_pwd_win_func():
    try:
        def check_mp():
            entry_mp_get = entry_mp.get()
            if mp_fl_cntnts == entry_mp.get():
                dropdown_menu.place(x=460, y=150)
                pwd_hide_btn.place(x=555, y=215)
                pwd_show_btn.place(x=460, y=215)
                delete_cred_btn.place(x=646, y=215)
                pwd_entry.place(x=460, y=190)
                mp_fl_fnd.destroy()
            else:
                messagebox.showerror("Master Password", "Incorrect Master Password.")

        with open (usr_path_with_mp_fl, 'r') as mp_fl:
            mp_fl_cntnts = mp_fl.read()
        mp_fl_fnd = Toplevel(win)
        mp_fl_fnd.title("Master Password Required")
        mp_fl_fnd.geometry('350x160')
        mp_fl_fnd.resizable(False, False)
        mp_fl_fnd.configure(background='black')

        dropdown_menu.place_forget()
        pwd_hide_btn.place_forget()
        pwd_show_btn.place_forget()
        delete_cred_btn.place_forget()
        pwd_entry.place_forget()

        title_mp = Label(mp_fl_fnd, text="Master Password Required", font=('Arial', 16), fg='white', bg='black')
        title_mp.pack(pady=20)

        entry_mp = Entry(mp_fl_fnd, width=40, show='*')
        entry_mp.pack(pady=5)

        enter_btn = Button(mp_fl_fnd, text="        Enter      ", fg='black', bg='white', command=check_mp)
        enter_btn.pack(pady=10)
    
    except FileNotFoundError:
        def set_mp():
            entry_mp_cntnts = entry_mp.get()
            with open(usr_path_with_mp_fl, 'w') as mp:
                mp.write(entry_mp_cntnts)
            messagebox.showinfo("Master Password", "Master Password set successfully.")
            mp_nt_fnd.destroy()

        mp_nt_fnd = Toplevel(win)
        mp_nt_fnd.title("Master Password Creation")
        mp_nt_fnd.geometry('350x160')
        mp_nt_fnd.resizable(False, False)
        mp_nt_fnd.configure(background='black')

        title_mp = Label(mp_nt_fnd, text="Master Password Creation", font=('Arial', 16), fg='white', bg='black')
        title_mp.pack(pady=20)

        entry_mp = Entry(mp_nt_fnd, width=40)
        entry_mp.pack(pady=5)

        enter_btn = Button(mp_nt_fnd, text="        Set      ", fg='black', bg='white', command=set_mp)
        enter_btn.pack(pady=10)

def check_updts():
    version_url = "https://apm-version.tiiny.site"
    version = requests.get(version_url)
    if version.status_code == 200:
        soup = BeautifulSoup(version.content, 'html.parser')
        version_no = soup.find('h1')
        if version_no:
            final_version = version_no.text.strip()
            if final_version == "v2.0" :
                messagebox.showinfo("Updates", "No new updates available.")
            else:
                messagebox.showinfo("Updates", f"A new release is available : {final_version} . Click Ok to view the releases page.")
                webbrowser.open("https://github.com/VidyutPrabakaran1/AI-Password-Manager/releases")
        else:
            messagebox.showerror("Updates", "Unable to check for updates.")

    else:
        messagebox.showerror("Updates", "Unable to check for updates.")

def trans_check():
    try:
        with open (usr_path_with_trns_fl, 'r') as file:
            trans_cmd = file.read().strip()
            try:
                trans_val = int(trans_cmd)
                return trans_val
            except ValueError:
                return 0
    except FileNotFoundError:
        with open (usr_path_with_trns_fl, 'w') as file:
            file.write('0')
    
def trans_aply_fr():
    trans_val_agn = trans_check()
    if trans_val_agn == 1:
        win.attributes('-alpha', 0.7)
    else:
        win.attributes('-alpha', 1)

def trans_act():
    trans_val_chk_agn = trans_check()
    if trans_val_chk_agn == 1:
        with open(usr_path_with_trns_fl, 'w') as file:
            file.write('0')
        messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
        sys.exit()

    elif trans_val_chk_agn == 0:
        with open(usr_path_with_trns_fl, 'w') as file:
            file.write('1')
        messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
        sys.exit()
    else:
        with open(usr_path_with_trns_fl, 'w') as file:
            file.write('1')
        messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
        sys.exit()

def thm_crt_win():
    win1=Toplevel(win)
    win1.geometry('460x250')
    win1.title("Theme Creator")
    win1.resizable(False, False)
    win1.configure(background='black')
    txt_clr_lbl=Label(win1, text="Text Colour :", font=("arial", 16), fg='white', bg='black')
    txt_clr_lbl.place(x=50, y=30)
    txt_clr_ety=Entry(win1, width=20)
    txt_clr_ety.place(x=180, y=35)
    btn_clr_lbl=Label(win1, text="Button :", font=("arial", 16), fg='white', bg='black')
    btn_clr_lbl.place(x=50, y=58)
    btn_clr_ety=Entry(win1, width=20)
    btn_clr_ety.insert(0, "Button Text Colour")
    btn_clr_ety.place(x=180, y=63)
    btn_clr1_ety=Entry(win1, width=20)
    btn_clr1_ety.insert(0, "Button Colour")
    btn_clr1_ety.place(x=180, y=93)
    bg_clr_lbl=Label(win1, text="Background :", font=("arial", 16), fg='white', bg='black')
    bg_clr_lbl.place(x=50, y=115)
    bg_clr_ety=Entry(win1, width=20)
    bg_clr_ety.insert(0, "Solid Colour")
    bg_clr_ety.place(x=180, y=123)
    gclrs=Label(win1, text="General Colours : red, orange, yellow, green, blue,", font=("arial", 12), fg='white', bg='black')
    gclrs.place(x=50, y=160)
    gclrs1=Label(win1, text="black, gray, white, etc.", font=("arial", 12), fg='white', bg='black')
    gclrs1.place(x=50, y=183)
    gclrs2=Label(win1, text="(LOWERCASE ONLY)", font=("arial", 12), fg='white', bg='black')
    gclrs2.place(x=50, y=213)

    def aply_chngs():
        with open (usr_path_with_cnfg_fl, 'w') as file:
            file.write('6')

        txt_clr_fl=txt_clr_ety.get()
        with open (usr_path_with_txtclr_fl, 'w') as file:
            file.write(txt_clr_fl)

        btn_clr_fl=btn_clr_ety.get()
        with open (usr_path_with_btnclr_fl, 'w') as file:
            file.write(btn_clr_fl)

        btn_clr1_fl=btn_clr1_ety.get()
        with open (usr_path_with_btnclr1_fl, 'w') as file:
            file.write(btn_clr1_fl)

        bg_clr_fl=bg_clr_ety.get()
        with open (usr_path_with_bgclr_fl, 'w') as file:
            file.write(bg_clr_fl)

        messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
        sys.exit()
    
    aply_btn=Button(win1, text="Apply Changes", fg='black', bg='white', command=aply_chngs)
    aply_btn.place(x=340, y=74)

def fdbk():
    url = 'https://forms.gle/gAvLGKMQPSQe3NyJ8'
    webbrowser.open(url)

def usrnme_gen():
    api_url1 = 'https://api.api-ninjas.com/v1/randomuser'
    response1 = requests.get(api_url1, headers={'X-Api-Key': ''})
    if response1.status_code == requests.codes.ok:
        data1 = json.loads(response1.text)
        random_usrnme = data1.get('username', '')
        usrnme_gen_entry.delete(0, END)
        usrnme_gen_entry.insert(0, random_usrnme)
    else:
        usrnme_gen_entry.delete(0, END)
        usrnme_gen_entry.insert(0, "Failed to generate username.")

def usrnme_clear():
    usrnme_gen_entry.delete(0, END)

def mode_dark():
    with open (usr_path_with_cnfg_fl, 'w') as file:
        file.write('1')
    messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
    sys.exit()

def mode_light():
    with open (usr_path_with_cnfg_fl, 'w') as file:
        file.write('2')
    messagebox.showinfo("Restart", "Restart the program for the changes to take effect.")
    sys.exit()

def estr_init(event):
    if pwd_gen.get() == 'the first Sunday after the full Moon that occurs on or after the spring equinox':
        with open (usr_path_with_cnfg_fl, 'w') as file:
            file.write('3')
        messagebox.showinfo("You Found The Secret !", "Restart the program to see the secret theme !")
        sys.exit()
    else:
        pass

def mode_grab():
    try:
        with open (usr_path_with_cnfg_fl, 'r') as file:
            mode_val=file.read().strip()
            try:
                val_cnv = int(mode_val)
                return val_cnv
            except ValueError:
                return 1
    except FileNotFoundError:
        with open (usr_path_with_cnfg_fl, 'w') as file:
            file.write('1')

def app_mode():
    if mode_state==1:
        win.configure(background='black')
        title.configure(fg='white', bg='black')
        pwd_gen_text.configure(fg='white', bg='black')
        pwd_gen_btn.configure(fg='black', bg='white')
        pwd_gen_clear.configure(fg='black', bg='white')
        pwd_check_text.configure(fg='white', bg='black')
        pwd_check_btn.configure(fg='black', bg='white')
        creds_txt.configure(fg='white', bg='black')
        dropdown_menu.configure(fg='white', bg='black')
        pwd_show_btn.configure(fg='black', bg='white')
        pwd_hide_btn.configure(fg='black', bg='white')
        new_pwd_text.configure(fg='white', bg='black')
        add_cred_btn.configure(fg='black', bg='white')
        delete_cred_btn.configure(fg='black', bg='white')
        dark_mode_btn.configure(fg='black', bg='white')
        light_mode_btn.configure(fg='black', bg='white')
        usrnme_gen_txt.configure(fg='white', bg='black')
        usrnme_gen_btn.configure(fg='black', bg='white')
        usrnme_clear_btn.configure(fg='black', bg='white')
        app_mode_txt.configure(fg='white', bg='black')
        pwd_gen_l_12.configure(fg='black', bg='white')
        pwd_gen_l_16.configure(fg='black', bg='white')
        fdbk_btn.configure(fg='black', bg='white')
        thm_crtr_btn.configure(fg='black', bg='white')
        trans_btn.configure(fg='black', bg='white')
        updt_btn.configure(fg='black', bg='white')
        cmn_pwds_chk_txt.configure(fg='white', bg='black')
        cmn_pwds_chk_btn.configure(fg='black', bg='white')
        reset_btn.configure(fg='black', bg='white')
        apm_accs_btn.configure(fg='black', bg='white')
    elif mode_state == 2:
        win.configure(background='white')
        title.configure(fg='black', bg='white')
        pwd_gen_text.configure(fg='black', bg='white')
        pwd_gen_btn.configure(fg='white', bg='black')
        pwd_gen_clear.configure(fg='white', bg='black')
        pwd_check_text.configure(fg='black', bg='white')
        pwd_check_btn.configure(fg='white', bg='black')
        creds_txt.configure(fg='black', bg='white')
        dropdown_menu.configure(fg='black', bg='white')
        pwd_show_btn.configure(fg='white', bg='black')
        pwd_hide_btn.configure(fg='white', bg='black')
        new_pwd_text.configure(fg='black', bg='white')
        add_cred_btn.configure(fg='white', bg='black')
        delete_cred_btn.configure(fg='white', bg='black')
        dark_mode_btn.configure(fg='white', bg='black')
        light_mode_btn.configure(fg='white', bg='black')
        usrnme_gen_txt.configure(fg='black', bg='white')
        usrnme_gen_btn.configure(fg='white', bg='black')
        usrnme_clear_btn.configure(fg='white', bg='black')
        app_mode_txt.configure(fg='black', bg='white')
        pwd_gen_l_12.configure(fg='white', bg='black')
        pwd_gen_l_16.configure(fg='white', bg='black')
        fdbk_btn.configure(fg='white', bg='black')
        thm_crtr_btn.configure(fg='white', bg='black')
        trans_btn.configure(fg='white', bg='black')
        updt_btn.configure(fg='white', bg='black')
        cmn_pwds_chk_txt.configure(fg='black', bg='white')
        cmn_pwds_chk_btn.configure(fg='white', bg='black')
        reset_btn.configure(fg='white', bg='black')
        apm_accs_btn.configure(fg='white', bg='black')
    elif mode_state == 3:
        win.configure(background='grey')
        title.configure(fg='black', bg='grey')
        pwd_gen_text.configure(fg='black', bg='grey')
        pwd_gen_btn.configure(fg='white', bg='black')
        pwd_gen_clear.configure(fg='white', bg='black')
        pwd_check_text.configure(fg='black', bg='grey')
        pwd_check_btn.configure(fg='white', bg='black')
        creds_txt.configure(fg='black', bg='grey')
        dropdown_menu.configure(fg='black', bg='white')
        pwd_show_btn.configure(fg='white', bg='black')
        pwd_hide_btn.configure(fg='white', bg='black')
        new_pwd_text.configure(fg='black', bg='grey')
        add_cred_btn.configure(fg='white', bg='black')
        delete_cred_btn.configure(fg='white', bg='black')
        dark_mode_btn.configure(fg='white', bg='black')
        light_mode_btn.configure(fg='white', bg='black')
        usrnme_gen_txt.configure(fg='black', bg='grey')
        usrnme_gen_btn.configure(fg='white', bg='black')
        usrnme_clear_btn.configure(fg='white', bg='black')
        app_mode_txt.configure(fg='black', bg='grey')
        pwd_gen_l_12.configure(fg='white', bg='black')
        pwd_gen_l_16.configure(fg='white', bg='black')
        def sprg_mode():
            with open (usr_path_with_cnfg_fl, 'w') as file:
                file.write('4')
            messagebox.showinfo("Restart", "Restart the program to see the changes.")
            sys.exit()
        estr_thm=Button(win, text="Spring Mode", fg='white', bg='black', command=sprg_mode)
        estr_thm.place(x=660, y=460)
        fdbk_btn.configure(fg='white', bg='black')
        thm_crtr_btn.configure(fg='white', bg='black')
        trans_btn.configure(fg='white', bg='black')
        updt_btn.configure(fg='white', bg='black')
        cmn_pwds_chk_txt.configure(fg='black', bg='grey')
        cmn_pwds_chk_btn.configure(fg='white', bg='black')
        reset_btn.configure(fg='white', bg='black')
        apm_accs_btn.configure(fg='white', bg='black')
    elif mode_state == 4:
        win.configure(background='light blue')
        title.configure(fg='purple', bg='light blue')
        pwd_gen_text.configure(fg='purple', bg='light blue')
        pwd_gen_btn.configure(fg='black', bg='orange')
        pwd_gen_clear.configure(fg='black', bg='orange')
        pwd_check_text.configure(fg='purple', bg='light blue')
        pwd_check_btn.configure(fg='black', bg='orange')
        creds_txt.configure(fg='purple', bg='light blue')
        dropdown_menu.configure(fg='black', bg='orange')
        pwd_show_btn.configure(fg='black', bg='orange')
        pwd_hide_btn.configure(fg='black', bg='orange')
        new_pwd_text.configure(fg='purple', bg='light blue')
        add_cred_btn.configure(fg='black', bg='orange')
        delete_cred_btn.configure(fg='black', bg='orange')
        dark_mode_btn.configure(fg='black', bg='orange')
        light_mode_btn.configure(fg='black', bg='orange')
        usrnme_gen_txt.configure(fg='purple', bg='light blue')
        usrnme_gen_btn.configure(fg='black', bg='orange')
        usrnme_clear_btn.configure(fg='black', bg='orange')
        app_mode_txt.configure(fg='purple', bg='light blue')
        pwd_gen_l_12.configure(fg='black', bg='orange')
        pwd_gen_l_16.configure(fg='black', bg='orange')
        fdbk_btn.configure(fg='black', bg='orange')
        thm_crtr_btn.configure(fg='black', bg='orange')
        trans_btn.configure(fg='black', bg='orange')
        updt_btn.configure(fg='black', bg='orange')
        cmn_pwds_chk_txt.configure(fg='purple', bg='light blue')
        cmn_pwds_chk_btn.configure(fg='black', bg='orange')
        reset_btn.configure(fg='black', bg='orange')
        apm_accs_btn.configure(fg='black', bg='orange')

    elif mode_state == 6:
        try :
            with open(usr_path_with_txtclr_fl, 'r') as file:
                txt_clr_ld = file.read()
            with open(usr_path_with_btnclr_fl, 'r') as file:
                btn_clr_ld = file.read()
            with open(usr_path_with_btnclr1_fl, 'r') as file:
                btn_clr1_ld = file.read()
            with open(usr_path_with_bgclr_fl, 'r') as file:
                bg_clr_ld = file.read()

            win.configure(background=bg_clr_ld)
            title.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            pwd_gen_text.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            pwd_gen_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            pwd_gen_clear.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            pwd_check_text.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            pwd_check_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            creds_txt.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            dropdown_menu.configure(fg=btn_clr1_ld, bg=btn_clr_ld)
            pwd_show_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            pwd_hide_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            new_pwd_text.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            add_cred_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            delete_cred_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            dark_mode_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            light_mode_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            usrnme_gen_txt.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            usrnme_gen_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            usrnme_clear_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            app_mode_txt.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            pwd_gen_l_12.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            pwd_gen_l_16.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            fdbk_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            thm_crtr_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            trans_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            updt_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            cmn_pwds_chk_txt.configure(fg=txt_clr_ld, bg=bg_clr_ld)
            cmn_pwds_chk_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            reset_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)
            apm_accs_btn.configure(fg=btn_clr_ld, bg=btn_clr1_ld)

        except Exception as e:
            messagebox.showerror("Error", "Your custom theme has errors. Reverting to the default theme.")
            with open (usr_path_with_cnfg_fl, 'w') as file:
                file.write('1')
            pass

    elif mode_state == 7:
        title.configure(fg='white')
        pwd_gen_text.configure(fg='white')
        pwd_gen_btn.configure(fg='black', bg='white')
        pwd_gen_clear.configure(fg='black', bg='white')
        pwd_check_text.configure(fg='white')
        pwd_check_btn.configure(fg='black', bg='white')
        creds_txt.configure(fg='white')
        dropdown_menu.configure(fg='white', bg='black')
        pwd_show_btn.configure(fg='black', bg='white')
        pwd_hide_btn.configure(fg='black', bg='white')
        new_pwd_text.configure(fg='white')
        add_cred_btn.configure(fg='black', bg='white')
        delete_cred_btn.configure(fg='black', bg='white')
        dark_mode_btn.configure(fg='black', bg='white')
        light_mode_btn.configure(fg='black', bg='white')
        usrnme_gen_txt.configure(fg='white')
        usrnme_gen_btn.configure(fg='black', bg='white')
        usrnme_clear_btn.configure(fg='black', bg='white')
        app_mode_txt.configure(fg='white')
        pwd_gen_l_12.configure(fg='black', bg='white')
        pwd_gen_l_16.configure(fg='black', bg='white')
        fdbk_btn.configure(fg='black', bg='white')
        thm_crtr_btn.configure(fg='black', bg='white')
        trans_btn.configure(fg='black', bg='white')
        updt_btn.configure(fg='black', bg='white')
        cmn_pwds_chk_txt.configure(fg='white')
        cmn_pwds_chk_btn.configure(fg='black', bg='white')
        reset_btn.configure(fg='black', bg='white')
        apm_accs_btn.configure(fg='black', bg='white')

    elif mode_state == 8:
        pass

    else:
        win.configure(background='black')
        title.configure(fg='white', bg='black')
        pwd_gen_text.configure(fg='white', bg='black')
        pwd_gen_btn.configure(fg='black', bg='white')
        pwd_gen_clear.configure(fg='black', bg='white')
        pwd_check_text.configure(fg='white', bg='black')
        pwd_check_btn.configure(fg='black', bg='white')
        creds_txt.configure(fg='white', bg='black')
        dropdown_menu.configure(fg='white', bg='black')
        pwd_show_btn.configure(fg='black', bg='white')
        pwd_hide_btn.configure(fg='black', bg='white')
        new_pwd_text.configure(fg='white', bg='black')
        add_cred_btn.configure(fg='black', bg='white')
        delete_cred_btn.configure(fg='black', bg='white')
        dark_mode_btn.configure(fg='black', bg='white')
        light_mode_btn.configure(fg='black', bg='white')
        usrnme_gen_txt.configure(fg='white', bg='black')
        usrnme_gen_btn.configure(fg='black', bg='white')
        usrnme_clear_btn.configure(fg='black', bg='white')
        app_mode_txt.configure(fg='white', bg='black')
        pwd_gen_l_12.configure(fg='black', bg='white')
        pwd_gen_l_16.configure(fg='black', bg='white')
        fdbk_btn.configure(fg='black', bg='white')
        thm_crtr_btn.configure(fg='black', bg='white')
        trans_btn.configure(fg='black', bg='white')
        updt_btn.configure(fg='black', bg='white')
        cmn_pwds_chk_txt.configure(fg='white', bg='black')
        cmn_pwds_chk_btn.configure(fg='black', bg='white')
        reset_btn.configure(fg='black', bg='white')
        apm_accs_btn.configure(fg='black', bg='white')

def internet_check():
    try:
        check = requests.get("https://www.example.com", timeout = 5)
        if check.status_code == 200:
            pass
        else:
            messagebox.showwarning("Internet Connection", "You're not connected to the internet. Some features will not work.")

    except requests.ConnectionError:
        messagebox.showerror("Internet Connection", "Failed to connect to the internet. Restart the program to try again. Without internet some features won't work.")

def delete_cred():
    selected_option = dropdown_var.get()
    if selected_option:
        del pwd_pwd[selected_option]
        pwd_options.remove(selected_option)
        dropdown_var.set("")
        pwd_entry.delete(0, END)
        save_credentials()
        update_dropdown()
    else:
        messagebox.showerror("Error", "Please select a credential to delete.")

#def add_cred():
#    new_cred = new_cred_entry.get()
#    new_cred1_prehash = new_cred_entry1.get()
#    new_cred1 = fernet.encrypt(new_cred1_prehash.encode())
#    if new_cred and new_cred1:
#        pwd_options.append(new_cred)
#        pwd_pwd[new_cred] = new_cred1
#        save_credentials()
#        update_dropdown()
#        new_cred_entry.delete(0, END)
#        new_cred_entry1.delete(0, END)
#    else:
#        messagebox.showerror("Error", "Please enter both Account ID and Password.")

def add_cred():

    new_cred = new_cred_entry.get()
    new_cred1_prehash = new_cred_entry1.get()
    new_cred1 = loaded_ferkey.encrypt(new_cred1_prehash.encode())
    
    if new_cred in pwd_pwd:
        # Check if the encrypted password is the same
        if pwd_pwd[new_cred] == new_cred1:
            messagebox.showerror("Error", "This Credential already exists.")
            return
        else:
            messagebox.showerror("Error", "This Credential already exists.")
            return
    
    if new_cred and new_cred1:
        pwd_options.append(new_cred)
        pwd_pwd[new_cred] = new_cred1
        save_credentials()
        update_dropdown()
        new_cred_entry.delete(0, END)
        new_cred_entry1.delete(0, END)
    else:
        messagebox.showerror("Error", "Please enter both Account ID and Password.")

def save_credentials():
    home_directory = os.path.expanduser('~')
    file_name = 'credentials.pkl'
    file_path = os.path.join(home_directory, file_name)
    try:
        with open(file_path, "wb") as f:
            pickle.dump(pwd_pwd, f)
    except Exception as e:
        messagebox.showerror("AI Password Manager", f"Error saving credentials:{e}")

def load_credentials():
    home_directory = os.path.expanduser('~')
    file_name = 'credentials.pkl'
    file_path = os.path.join(home_directory, file_name)
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}
    except EOFError:
        return {}
    except Exception as e:
        messagebox.showerror("AI Password Manager", f"Error loading credentials: {e}")
        return {}

def update_dropdown():
    dropdown_menu['menu'].delete(0, 'end')
    for option in pwd_options:
        dropdown_menu['menu'].add_command(label=option, command=lambda value=option: dropdown_var.set(value))

def pwd_hide():
    pwd_entry.delete(0, END)

def pwd_show():
    selected_option = dropdown_var.get()
    
    if selected_option in pwd_pwd:
        pwd_entry.delete(0, END)

        def check_if_encrypted():
            try:
                # Attempt to decrypt with the main key
                loaded_ferkey.decrypt(pwd_pwd[selected_option])
                return "main_key"
            except InvalidToken:
                # Try to decrypt with the default key
                try:
                    fernet_def.decrypt(pwd_pwd[selected_option])
                    return "default_key"
                except InvalidToken:
                    return "not_encrypted"

        # Check the encryption status
        encryption_status = check_if_encrypted()

        if encryption_status == "main_key":
            pwd_decrypted = loaded_ferkey.decrypt(pwd_pwd[selected_option]).decode()
            pwd_entry.insert(0, pwd_decrypted)
        elif encryption_status == "default_key":
            pwd_decrypted = fernet_def.decrypt(pwd_pwd[selected_option]).decode()
            pwd_entry.insert(0, pwd_decrypted)
            messagebox.showwarning(
                "Encryption",
                "This credential is using an older encryption method. To switch to the newer encryption method, delete and re-add this credential."
            )
        elif encryption_status == "not_encrypted":
            pwd_entry.insert(0, pwd_pwd[selected_option])
            messagebox.showwarning(
                "Encryption",
                "This credential is using an older encryption method. To switch to the newer encryption method, delete and re-add this credential."
            )
    else:
        messagebox.showerror("Error", "No password found for the selected credential.")

    
def pwd_check_clicked():
    password=pwd_check.get()
    if password == "":
        pwd_check_result_text.set("Please enter a password to check.")
    else:
        def get_password_strength(password):
            result = zxcvbn.zxcvbn(password)
            return result['score']
        strength_score = get_password_strength(password)
        if strength_score == 4:
            pwd_check_result_text.set(f"Strength : Strong | Score : {strength_score}/4")
        elif strength_score == 3 :
            pwd_check_result_text.set(f"Strength : Moderate | Score : {strength_score}/4")
        elif strength_score == 2 :
            pwd_check_result_text.set(f"Strength : Ok | Score : {strength_score}/4")
        elif strength_score == 1 :
            pwd_check_result_text.set(f"Strength : Low | Score : {strength_score}/4")
        elif strength_score == 0 :
            pwd_check_result_text.set(f"Strength : Very Low | Score : {strength_score}/4")
        else:
            pwd_check_result_text.set("Unable to obtain score.")

length = 12

def l_12():
    global length
    length = 12
    btn_12 = 12
    temp_var = length
    length = btn_12

def l_16():
    global length
    length = 12
    btn_16 = 16
    temp_var_2 = length
    length = btn_16

def pwd_gen_clicked():
    global length
    api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
    response = requests.get(api_url, headers={'X-Api-Key': ''})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        random_password = data.get('random_password', '')
        pwd_gen.delete(0, END)
        pwd_gen.insert(0, random_password)
    else:
        pwd_gen.delete(0, END)
        pwd_gen.insert(0, "Failed to generate password. Try Again")

def pwd_gen_clear():
    pwd_gen.delete(0, END)

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f'{width}x{height}+{x}+{y}')

def splash_screen():
    messagebox.showinfo("AI Password Manager", "Welcome to AI Password Manager !")

# MAIN

win = Tk()
win.title("AI Password Manager")
win.geometry('1230x570')    # 1280x720 (MIN)
center_window(win, 1230, 570)
win.resizable(False, False)
win.configure(background='black')

#win.wm_attributes('-transparentcolor','black')

script_dir = os.path.dirname(sys.argv[0])
icon_path = os.path.join(script_dir, '_itnrl/apm.png')
icon_path_ico = os.path.join(script_dir, '_itnrl/apm.ico')
icon = PhotoImage(file=icon_path)
win.iconphoto(False, icon)
win.iconbitmap(icon_path_ico)

chk_lclapdt_fldr()

mode_change_init = 1

mode_state = mode_grab()

internet_check()

trans_aply_fr()

scrn_sz_chk()

title = Label(win, text="AI Password Manager", font=('Arial', 16), fg='white', bg='black')
title.place(x=50, y=40)
#title = canvas.create_text(50, 40, text="AI Password Manager", font=('Arial', 16), fill='white', anchor='nw')

pwd_gen_text=Label(win, text="Password Generator :", font=('Arial', 15), fg='white', bg='black')
pwd_gen_text.place(x=50, y=100)

pwd_gen=Entry(win, width=40)
pwd_gen.place(x=50, y=150)
pwd_gen.insert(0, "Default Password Length is 12.")

pwd_gen_l_12 = Button(win, text="12", fg='black', bg='white', command=l_12)
pwd_gen_l_12.place(x=220, y=180)

pwd_gen_l_16 = Button(win, text="16", fg='black', bg='white', command=l_16)
pwd_gen_l_16.place(x=245, y=180)

pwd_gen_btn=Button(win, text="Generate Password", fg='black', bg='white', command=pwd_gen_clicked)
pwd_gen_btn.place(x=50, y=180)

pwd_gen_clear=Button(win, text="Clear", fg='black', bg='white', command=pwd_gen_clear)
pwd_gen_clear.place(x=163, y=180)

pwd_check_text=Label(win, text="Password Strength Checker :", font=('Arial', 15), fg='white', bg='black')
pwd_check_text.place(x=50, y=240)

pwd_check=Entry(win, width=40)
pwd_check.place(x=50, y=285)

pwd_check_result_text = StringVar(win)
pwd_check_result=Entry(win, width=35, state='readonly', textvariable=pwd_check_result_text)
pwd_check_result_text.set("Result will appear here.")
pwd_check_result.place(x=50, y=310)

pwd_check_btn=Button(win, text="Check Password", fg='black', bg='white', command=pwd_check_clicked)
pwd_check_btn.place(x=50, y=340)

pwd_pwd = load_credentials()
pwd_options = list(pwd_pwd.keys())
dropdown_var = StringVar(win)
dropdown_var.set("")

creds_txt=Label(win, text="Your Credentials :", fg='white', bg='black', font=('Arial', 12))
creds_txt.place(x=460, y=120)

dropdown_menu = OptionMenu(win, dropdown_var, "")
dropdown_menu.configure(fg='white', bg='black', width=40)
dropdown_menu.place(x=460, y=150)

pwd_entry=Entry(win, width=47)
pwd_entry.place(x=460, y=190)

pwd_show_btn=Button(win, text="Show Password", fg='black', bg='white', command=pwd_show)
pwd_show_btn.place(x=460, y=215)

pwd_hide_btn=Button(win, text="Hide Password", fg='black', bg='white', command=pwd_hide)
pwd_hide_btn.place(x=555, y=215)

pwd_gen.bind('<Return>', estr_init)

new_pwd_text=Label(win, text="Add Credentials :", font=('Arial', 12), fg='white', bg='black')
new_pwd_text.place(x=460, y=250)

new_cred_entry=Entry(win, width = 47)
new_cred_entry.insert(0, "Enter Your Account ID/Name/Username")
new_cred_entry.place(x=460, y=280)

new_cred_entry1=Entry(win, width = 47)
new_cred_entry1.insert(0, "Enter Your Password")
new_cred_entry1.place(x=460, y=305)

add_cred_btn=Button(win, text="Add Credentials", fg='black', bg='white', command=add_cred)
add_cred_btn.place(x=460, y=330)

delete_cred_btn = Button(win, text="Delete Credential", fg='black', bg='white', command=delete_cred)
delete_cred_btn.place(x=646, y=215)

app_mode_txt=Label(win, text="App Mode :", font=('Arial', 12), fg='white', bg='black')
app_mode_txt.place(x=460, y=400)

dark_mode_btn=Button(win, text="Dark Mode", fg='black', bg='white', command=mode_dark)
dark_mode_btn.place(x=560, y=460)

light_mode_btn=Button(win, text="Light Mode", fg='black', bg='white', command=mode_light)
light_mode_btn.place(x=460, y=460)

usrnme_gen_txt=Label(win, text="Generate Username :", font=('Arials', 15), fg='white', bg='black')
usrnme_gen_txt.place(x=50, y=390)

usrnme_gen_entry=Entry(win, width=40)
usrnme_gen_entry.place(x=50, y=435)

usrnme_gen_btn=Button(win, text="Generate Username", fg='black', bg='white', command=usrnme_gen)
usrnme_gen_btn.place(x=50, y=465)

usrnme_clear_btn=Button(win, text="Clear", fg='black', bg='white', command=usrnme_clear)
usrnme_clear_btn.place(x=166, y=465)

fdbk_btn=Button(win, text="Feedback", fg='black', bg='white', command=fdbk)
fdbk_btn.place(x=1150, y=530)

thm_crtr_btn=Button(win, text="Theme Creator", fg='black', bg='white', command=thm_crt_win)
thm_crtr_btn.place(x=1050, y=530)

trans_btn = Button(win, text="Transparency Mode", fg='black', bg='white', command=trans_act)
trans_btn.place(x=660, y=460)

updt_btn = Button(win, text="Updates", fg='black', bg='white', command=check_updts)
updt_btn.place(x=987, y=530)

cmn_pwds_chk_txt=Label(win, text="Common Passwords Checker :", font=('Arial', 15), fg='white', bg='black')
cmn_pwds_chk_txt.place(x=850, y=200)

cmn_pwds_chk_etry=Entry(win, width=40)
cmn_pwds_chk_etry.place(x=853, y=240)

cmn_pwds_result_text = StringVar(win)
cmn_pwds_result=Entry(win, width=35, state='readonly', textvariable=cmn_pwds_result_text)
cmn_pwds_result_text.set("Result will appear here.")
cmn_pwds_result.place(x=853, y=265)

cmn_pwds_chk_btn = Button(win, text="Check Password", fg='black', bg='white', command=cmn_pwds_chk)
cmn_pwds_chk_btn.place(x=853, y=295)

reset_btn = Button(win, text="Reset ", fg='black', bg='white', command=reset)
reset_btn.place(x=935, y=530)

apm_accs_btn = Button(win, text="APM Accounts", fg='black', bg='white', command=apm_func)
apm_accs_btn.place(x=835, y=530)

music_btn = Button(win, text="Music", command=bgm_win)

about_btn = Button(win, text="About", fg='black', bg='white', command=about)
about_btn.place(x=15, y=530)    #665x275

# MAIN END

#apm_func()
#bgm()
#splash_screen()
m_pwd_win_func()
app_mode()
update_dropdown()
win.mainloop()
