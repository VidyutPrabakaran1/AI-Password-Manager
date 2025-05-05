'''
AI Password Manager - MIT License

Copyright (c) 2025 Vidyut Prabakaran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

# Release Notes (v2.3)(Temporary):
# - Change default colour theme to Dark Blue.
# - Added in-built updater for APM.
# - Password Generator : Now uses more faster & secure on-device model to generate secure passwords even when offline.
# - Username Generator : Now uses an instantaneous on-device rule-based model to generate usernames even when offline.
# - Fixed the issue where Password Strength wouldn't display properly when strength is 4 (Strong).
# - Bug fixes.

# Libraries

import customtkinter as ctk
import platform
import os
import sys
#import requests
#import json
#import zxcvbn
#import pickle
from tkinter import messagebox
#import webbrowser
#from bs4 import BeautifulSoup
from cryptography.fernet import Fernet, InvalidToken
import gspread
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
#import io
#import base64
#import ctypes
#from random import randint
#import random
#import smtplib
#from email.mime.text import MIMEText
#import geocoder
#import subprocess
#import time

def main():
    # Globals

    if getattr(sys, 'frozen', False):  # Check if running as compiled EXE
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    key_def = b''
    fernet_def = Fernet(key_def)

    #script_dir = os.path.dirname(os.path.abspath(__file__))  # Works on all OS

    json_path = '_itnrl/misc', ''
    credentials_path = os.path.join(script_dir, *json_path)

    SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

    # Load the credentials and specify the scope
    credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    sheet = gc.open('APM-DB').sheet1

    # Paths

    #script_dir = os.path.dirname(os.path.abspath(__file__))

    passdir_init = os.path.expanduser('~')

    if sys.platform == "win32":
        local_appdata = os.getenv('LOCALAPPDATA')  # Windows
    elif sys.platform == "darwin":
        local_appdata = os.path.expanduser('~/Library/Application Support')  # macOS
    else:
        local_appdata = os.path.expanduser('~/.config')  # Linux

    config_fl_nme = 'config.txt'
    trans_fl_nme = 'trans.txt'
    mp_fl_nme = 'mp.mp'
    cred_fl_nme = 'credentials.pkl'

    home_directory_fr_cred = os.path.expanduser('~')

    usr_path_with_cnfg_fl = os.path.join(local_appdata, 'APM', config_fl_nme)
    usr_path_with_trns_fl = os.path.join(local_appdata, 'APM', trans_fl_nme)
    usr_path_with_mp_fl = os.path.join(local_appdata, 'APM', mp_fl_nme)
    cred_full_path = os.path.join(home_directory_fr_cred, cred_fl_nme)
    cred_json_path = os.path.join(home_directory_fr_cred, 'credentials.json')

    cred_file_name = 'credentials.json'
    cred_file_path = os.path.join(os.path.expanduser('~'), cred_file_name)

    cmn_pwds_path = os.path.join(script_dir, '_itnrl/misc', '10M.txt')
    apm_ico_full_path = os.path.join(script_dir, '_itnrl/icons', 'apm.png')
    fer_path = os.path.join(local_appdata, 'APM', 'fer.apm')

    acc_status_filepath = os.path.join(local_appdata, 'APM','acc_stat.txt')
    acc_usrnme_flpath = os.path.join(local_appdata, 'APM', 'acc_usrnme.apm')
    acc_pwd_flpath = os.path.join(local_appdata, 'APM', 'acc_pwd.apm')

    apm_logo_flpath = os.path.join(script_dir, '_itnrl/icons', 'apm_logo.png')

    license_flpath = os.path.join(script_dir, '_itnrl/docs', 'LICENSE.txt')
    credits_flpath = os.path.join(script_dir, '_itnrl/docs', 'CREDITS.txt')

    red_theme = os.path.join(os.path.dirname(__file__), "_itnrl/themes", "red_theme.json")
    orange_theme = os.path.join(os.path.dirname(__file__), "_itnrl/themes", "orange_theme.json")
    green_theme = os.path.join(os.path.dirname(__file__), "_itnrl/themes", "green_theme.json")
    blue_theme = os.path.join(os.path.dirname(__file__), "_itnrl/themes", "blue_theme.json")
    violet_theme = os.path.join(os.path.dirname(__file__), "_itnrl/themes", "violet_theme.json")

    pwd_model = os.path.join(script_dir, '_itnrl/models', 'pwd_model.json')
    usrnme_model = os.path.join(script_dir, '_itnrl/models', 'usernames.txt')

    # Functions

    def about():
        def license():
            system_name = platform.system()
        
            if system_name == "Windows":
                os.system(f'notepad "{license_flpath}"')
            elif system_name == "Darwin":  # macOS
                os.system(f'open -a TextEdit "{license_flpath}"')
            elif system_name == "Linux":
                os.system(f'xdg-open "{license_flpath}"')
            else:
                messagebox.showerror("Error", "Unable to open license file.")

        def credits():
            system_name = platform.system()

            if system_name == "Windows":
                os.system(f'notepad "{credits_flpath}"')
            elif system_name == "Darwin":  # macOS
                os.system(f'open -a TextEdit "{credits_flpath}"')
            elif system_name == "Linux":
                os.system(f'xdg-open "{credits_flpath}"')
            else:
                messagebox.showerror("Error", "Unable to open credits file.")

        about_win = ctk.CTkToplevel(win)
        about_win.title("AI Password Manager - About")
        about_win.geometry("370x270")
        about_win.resizable(False, False)
        about_win.lift()
        about_win.attributes("-topmost", True)
        if platform.system() == "Windows":
            about_win.iconbitmap(apm_ico_full_path)
        elif platform.system() == "Linux":
            from tkinter import PhotoImage
            icon_image = PhotoImage(file=apm_logo_flpath)
            about_win.iconphoto(False, icon_image)

        apm_lbl = ctk.CTkLabel(about_win, text="AI Password Manager", font=("Arial", 25, "bold"))
        apm_lbl.pack(pady=10, padx=40, anchor="nw")

        apm_ver_lbl = ctk.CTkLabel(about_win, text="Version 2.2", font=("Arial", 15))
        apm_ver_lbl.pack(pady=10, padx=40, anchor="nw")

        apm_dev_lbl = ctk.CTkLabel(about_win, text="Developed by Vidyut Prabakaran", font=("Arial", 15))
        apm_dev_lbl.pack(pady=10, padx=40, anchor="nw")

        apm_cnct = ctk.CTkLabel(about_win, text="Contact: vidyutprabakaran@gmail.com")
        apm_cnct.pack(pady=10, padx=40, anchor="nw")

        apm_btn_frame = ctk.CTkFrame(about_win)
        apm_btn_frame.pack(pady=10, padx=40, anchor="nw")

        apm_lcnse = ctk.CTkButton(apm_btn_frame, text="License", command=license, width=100, font=("Arial", 15))
        apm_lcnse.pack(side="left", padx=(0, 10))

        apm_crdts = ctk.CTkButton(apm_btn_frame, text="Credits", command=credits, width=100, font=("Arial", 15))
        apm_crdts.pack(side="left")

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
                    #print("\nBacking up ferkey.apm...")/g

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
                import io
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

            signedin_apmpanel = ctk.CTkToplevel(win)
            signedin_apmpanel.title(f"APM Accounts - {signedin_usrnme}")
            signedin_apmpanel.geometry('500x300')
            signedin_apmpanel.resizable(False, False)
            signedin_apmpanel.lift()
            signedin_apmpanel.attributes("-topmost", True)

            apm_lbl1 = ctk.CTkLabel(signedin_apmpanel, text="APM Accounts", font=('Arial', 18, "bold"))
            apm_lbl1.pack(side="left", padx=20)

            backup_btn = ctk.CTkButton(signedin_apmpanel, text="          Backup          ", command=backup)
            backup_btn.pack(side="top", pady=(115, 10))

            restore_btn = ctk.CTkButton(signedin_apmpanel, text="        Restore        ", command=restore)
            restore_btn.pack(side="top", pady=(10, 0))

            logout_btn = ctk.CTkButton(signedin_apmpanel, text="Logout", command=logout)
            logout_btn.place(x=350, y=260)

        elif stat == "0":
            def apm_signin_acc():
                json_path = '_itnrl/misc/'
                json_fullpath = os.path.join(script_dir, json_path)

                SCOPES = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]

                credentials = Credentials.from_service_account_file(json_fullpath, scopes=SCOPES)
                gc = gspread.authorize(credentials)
                sheet = gc.open('APM-DB').sheet1

                def send_verification_email(email_addr, code):
                    import geocoder
                    ip = geocoder.ip("me")

                    sender_email = "apm.officialnoreply@gmail.com"  # Replace with your email
                    sender_password = ""      # Replace with your email password or app-specific password
                    subject = "AI Password Manager - Verification Code"
                    body = f"Your APM verification code is : {code} . Sign In requested from {ip.city}, {ip.state}, {ip.country}. Do not share this code to anyone. If you didn't request this, someone may have your password."

                    from email.mime.text import MIMEText
                    msg = MIMEText(body)
                    msg['Subject'] = subject
                    msg['From'] = sender_email
                    msg['To'] = email_addr

                    try:
                        import smtplib
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

                        import base64
                        pwd_bytes = base64.urlsafe_b64decode(hashed_pwd.encode('utf-8'))
                        pwd_decrypted = fernet_def.decrypt(pwd_bytes)
                        pwd_decrypted_str = pwd_decrypted.decode()

                        if pwd_decrypted_str == pwd:
                            email_addr = sheet.cell(row_index, 5).value
                            #messagebox.showinfo("APM Accounts", f"Logged in to : {usrnme}")
                            apm_pwd_entry1.delete(0, "end")
                            apm_usrnme_entry1.delete(0, "end")
                            
                            from random import randint
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
                        
                            apm_vrfc_win = ctk.CTkToplevel(win)
                            apm_vrfc_win.title("APM Accounts - Verification Code")
                            apm_vrfc_win.geometry('350x150')
                            apm_vrfc_win.resizable(False, False)
                            apm_vrfc_win.lift()
                            apm_vrfc_win.attributes("-topmost", True)

                            vrfc_lbl = ctk.CTkLabel(apm_vrfc_win, text="Enter the verification code sent to your email:", font=('Arial', 15))
                            vrfc_lbl.pack(pady=10)

                            vrfc_entry = ctk.CTkEntry(apm_vrfc_win, width=200)
                            vrfc_entry.pack(pady=10)

                            vrfc_btn = ctk.CTkButton(apm_vrfc_win, text="Verify", command=chk_vrfc_code)
                            vrfc_btn.pack(pady=10)
                        else:
                            messagebox.showerror("APM - Accounts", "Incorrect password.")

                    else:
                        messagebox.showerror("APM - Accounts", "Username not found.")

                apm_win.destroy()

                apmswin = ctk.CTkToplevel(win)
                apmswin.title("APM Accounts - Sign In")
                apmswin.geometry('500x300')
                apmswin.resizable(False, False)
                apmswin.lift()
                apmswin.attributes("-topmost", True)

                apm_lbl1 = ctk.CTkLabel(apmswin, text="APM Accounts", font=('Arial', 18, "bold"))
                apm_lbl1.pack(side="left", padx=20)

                apm_usrnme_entry1 = ctk.CTkEntry(apmswin, placeholder_text="Enter your Username", width=200)
                apm_usrnme_entry1.place(x=260, y=130)

                apm_pwd_entry1 = ctk.CTkEntry(apmswin, placeholder_text="Enter your Password", width=200)
                apm_pwd_entry1.place(x=260, y=160)

                apm_signin_acc_btn = ctk.CTkButton(apmswin, text="Sign In", command=sign_in)
                apm_signin_acc_btn.place(x=290, y=200)


            def apm_crte_acc():
                messagebox.showinfo("APM Accounts", "Creating your account, this may take a while. Please wait.")

                script_dir = os.path.dirname(sys.argv[0])
                json_path = '_itnrl/misc/'
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
                import base64
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

            apm_win = ctk.CTkToplevel(win)
            apm_win.title("APM Accounts")
            apm_win.geometry('500x300')
            apm_win.resizable(False, False)
            apm_win.lift()
            apm_win.attributes("-topmost", True)

            apm_lbl = ctk.CTkLabel(apm_win, text="APM Accounts", font=('Arial', 18, "bold"))
            apm_lbl.pack(side="left", padx=20)

            apm_usrnme_entry = ctk.CTkEntry(apm_win, placeholder_text="Enter a Username", width=200)
            apm_usrnme_entry.place(x=260, y=100)

            apm_pwd_entry = ctk.CTkEntry(apm_win, placeholder_text="Enter a Password", width=200)
            apm_pwd_entry.place(x=260, y=130)

            apm_crte_acc_email = ctk.CTkEntry(apm_win, placeholder_text="Enter your email", width=200)
            apm_crte_acc_email.place(x=260, y=160)

            apm_crte_acc_btn = ctk.CTkButton(apm_win, text="Create Account", command=apm_crte_acc)
            apm_crte_acc_btn.place(x=290, y=200)

            apm_signin_btn = ctk.CTkButton(apm_win, text="Sign In", command=apm_signin_acc)
            apm_signin_btn.place(x=350, y=265)

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

                mp_fl_fnd = ctk.CTkToplevel(win)
                mp_fl_fnd.title("Master Password Required")
                mp_fl_fnd.geometry('350x160')
                mp_fl_fnd.resizable(False, False)

                mp_fl_fnd.lift()
                mp_fl_fnd.attributes("-topmost", True)

                dropdown_menu.place_forget()
                pwd_sh_btn.place_forget()
                pwd_copy_btn.place_forget()
                delete_cred_btn.place_forget()
                pwd_entry.place_forget()

                title_mp = ctk.CTkLabel(mp_fl_fnd, text="Master Password Required", font=('Arial', 16, "bold"))
                title_mp.pack(pady=20)

                entry_mp = ctk.CTkEntry(mp_fl_fnd, width=200, placeholder_text="Enter Master Password", show="*")
                entry_mp.pack(pady=5)

                enter_btn = ctk.CTkButton(mp_fl_fnd, text="        Enter      ", command=check_mp)
                enter_btn.pack(pady=10)
            
            except FileNotFoundError:
                def set_mp():
                    entry_mp_cntnts = entry_mp.get()
                    with open(usr_path_with_mp_fl, 'w') as mp:
                        mp.write(entry_mp_cntnts)
                    messagebox.showinfo("Master Password", "Master Password set successfully.")
                    mp_nt_fnd.destroy()

                mp_nt_fnd = ctk.CTkToplevel(win)
                mp_nt_fnd.title("Master Password Creation")
                mp_nt_fnd.geometry('350x160')
                mp_nt_fnd.resizable(False, False)
                mp_nt_fnd.configure(background='black')

                mp_nt_fnd.lift()
                mp_nt_fnd.attributes("-topmost", True)

                title_mp = ctk.CTkLabel(mp_nt_fnd, text="Set Master Password", font=('Arial', 16, "bold"))
                title_mp.pack(pady=20)

                entry_mp = ctk.CTkEntry(mp_nt_fnd, width=200, placeholder_text="Enter a Master Password")
                entry_mp.pack(pady=5)

                enter_btn = ctk.CTkButton(mp_nt_fnd, text="        Set        ", command=set_mp)
                enter_btn.pack(pady=10)

        def no():
            reset_win.destroy()

        reset_win = ctk.CTkToplevel(win)
        reset_win.title("Reset APM")

        reset_win.geometry('350x160')
        reset_win.resizable(False, False)

        reset_win.lift()
        reset_win.attributes("-topmost", True)

        title = ctk.CTkLabel(reset_win, text="Are you sure you want to reset APM?", font=('Arial', 16, "bold"))
        title.pack(pady=20)
        
        no_btn = ctk.CTkButton(reset_win, text="No", command=no)
        no_btn.pack(side="left", padx=(50, 10), pady=10)

        yes_btn = ctk.CTkButton(reset_win, text="Yes", command=yes)
        yes_btn.pack(side="right", padx=(10, 50), pady=10)

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
                    cmn_pwds_result_text.configure(text="Frequently Used. Unsafe Password.")
                elif usr_cmn_pwd == "":
                    cmn_pwds_result_text.configure(text="Please enter a password to check.")
                else:
                    cmn_pwds_result_text.configure(text="Not Frequently Used. Safe Password.")

        except Exception as e:
            messagebox.showerror(f"Error", "Unable to check password.")
            print(e)

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
                if mp_fl_cntnts == entry_mp_get:
                    # Re-place the credential-related widgets in their original positions
                    dropdown_menu.place(x=450, y=150)
                    pwd_entry.place(x=450, y=200)
                    pwd_copy_btn.place(x=450, y=250)
                    pwd_sh_btn.place(x=575, y=250)
                    delete_cred_btn.place(x=702, y=250)
                    mp_fl_fnd.destroy()
                else:
                    messagebox.showerror("Master Password", "Incorrect Master Password.")

            with open(usr_path_with_mp_fl, 'r') as mp_fl:
                mp_fl_cntnts = mp_fl.read()

            # Temporarily hide the credential-related widgets BEFORE creating the master password prompt
            dropdown_menu.place_forget()
            pwd_entry.place_forget()
            pwd_copy_btn.place_forget()
            pwd_sh_btn.place_forget()
            delete_cred_btn.place_forget()

            # Create the master password prompt window
            mp_fl_fnd = ctk.CTkToplevel(win)
            mp_fl_fnd.title("Master Password Required")
            mp_fl_fnd.geometry('350x160')
            mp_fl_fnd.resizable(False, False)

            mp_fl_fnd.lift()
            mp_fl_fnd.attributes("-topmost", True)

            # Add widgets to the master password prompt
            title_mp = ctk.CTkLabel(mp_fl_fnd, text="Master Password Required", font=('Arial', 16, "bold"))
            title_mp.pack(pady=20)

            entry_mp = ctk.CTkEntry(mp_fl_fnd, width=200, placeholder_text="Enter Master Password", show="*")
            entry_mp.pack(pady=5)

            enter_btn = ctk.CTkButton(mp_fl_fnd, text="Enter", command=check_mp)
            enter_btn.pack(pady=10)

        except FileNotFoundError:
            def set_mp():
                entry_mp_cntnts = entry_mp.get()
                with open(usr_path_with_mp_fl, 'w') as mp:
                    mp.write(entry_mp_cntnts)
                messagebox.showinfo("Master Password", "Master Password set successfully.")
                mp_nt_fnd.destroy()

            # Create the master password setup window
            mp_nt_fnd = ctk.CTkToplevel(win)
            mp_nt_fnd.title("Master Password Creation")
            mp_nt_fnd.geometry('350x160')
            mp_nt_fnd.resizable(False, False)

            mp_nt_fnd.lift()
            mp_nt_fnd.attributes("-topmost", True)

            title_mp = ctk.CTkLabel(mp_nt_fnd, text="Set Master Password", font=('Arial', 16, "bold"))
            title_mp.pack(pady=20)

            entry_mp = ctk.CTkEntry(mp_nt_fnd, width=200, placeholder_text="Enter a Master Password")
            entry_mp.pack(pady=5)

            enter_btn = ctk.CTkButton(mp_nt_fnd, text="Set", command=set_mp)
            enter_btn.pack(pady=10)

    def windows_update():
        def update_apm():
            import subprocess

            updater_path = os.path.join(script_dir, 'apm_updater.exe')
            subprocess.Popen([updater_path])
            sys.exit(0)

        def changelog():
            import webbrowser
            webbrowser.open("https://github.com/VidyutPrabakaran1/AI-Password-Manager/releases")

        wupdate = ctk.CTkToplevel(win)
        wupdate.title("APM Update")
        wupdate.geometry('350x160')
        wupdate.resizable(False, False)
        wupdate.lift()
        wupdate.attributes("-topmost", True)

        import requests
        version_url = "https://apm-version.tiiny.site"
        version = requests.get(version_url)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(version.content, 'html.parser')
        version_no = soup.find('h1')

        wupdate_lbl = ctk.CTkLabel(wupdate, text=f"Update Available : {version_no}", font=('Arial', 16, "bold"))
        wupdate_lbl.pack(pady=20)

        # Update, Cancel, Changelog buttons
        update_btn = ctk.CTkButton(wupdate, text="Update", command=update_apm)
        update_btn.pack(side="left", padx=(50, 10), pady=10)

        cancel_btn = ctk.CTkButton(wupdate, text="Cancel", command=wupdate.destroy)
        cancel_btn.pack(side="right", padx=(10, 50), pady=10)

        changelog_btn = ctk.CTkButton(wupdate, text="Changelog", command=changelog)
        changelog_btn.pack(side="top", pady=(10, 0))

    def check_updts():
        version_url = "https://apm-version.tiiny.site"
        import requests
        version = requests.get(version_url)
        if version.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(version.content, 'html.parser')
            version_no = soup.find('h1')
            if version_no:
                final_version = version_no.text.strip()
                if final_version == "v2.3" :
                    messagebox.showinfo("Updates", "No new updates available.")
                elif final_version == "[SERVER SIDE FAILURE - FALLBACK]":
                    if platform.system() == "Windows":
                        import webbrowser
                        messagebox.showinfo("Updates", "Unable to update APM. Click Ok to view to view the releases page to update manually.")
                        webbrowser.open("https://github.com/VidyutPrabakaran1/AI-Password-Manager/releases")
                    elif platform.system() == "Linux":
                        import webbrowser
                        messagebox.showinfo("Updates", f"A new release is available . Click Ok to view the releases page.")
                        webbrowser.open("https://github.com/VidyutPrabakaran1/AI-Password-Manager/releases")

                else:
                    if platform.system() == "Linux":
                        import webbrowser
                        messagebox.showinfo("Updates", f"A new release is available : {final_version} . Click Ok to view the releases page.")
                        webbrowser.open("https://github.com/VidyutPrabakaran1/AI-Password-Manager/releases")
                    elif platform.system() == "Windows":
                        pass
                    else:
                        import webbrowser
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

    def fdbk():
        url = 'https://forms.gle/gAvLGKMQPSQe3NyJ8'
        import webbrowser
        webbrowser.open(url)

    def usrnme_gen():
        import random

        with open (usrnme_model, 'r') as file:
            words = file.read().splitlines()

        def generate_usrnme():
            return random.choice(words) + str(random.randint(100, 9999))
        
        usrnme_gen_entry.delete(0, "end")
        usrnme_gen_entry.insert(0, generate_usrnme())

    def usrnme_clear():
        usrnme_gen_entry.delete(0, "end")

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

    # Ensure mode_grab() retrieves the mode state correctly
    def mode_grab():
        try:
            with open(usr_path_with_cnfg_fl, 'r') as file:
                mode_val = file.read().strip()
                try:
                    val_cnv = int(mode_val)
                    return val_cnv
                except ValueError:
                    return 1  # Default to dark mode if the value is invalid
        except FileNotFoundError:
            with open(usr_path_with_cnfg_fl, 'w') as file:
                file.write('1')  # Default to dark mode
            return 1

    # Apply the appearance mode based on the mode state
    def app_mode():
        if mode_state == 1:
            ctk.set_appearance_mode("dark")
        elif mode_state == 2:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")  # Default to dark mode

    # Call mode_grab() and app_mode() during initialization
    mode_state = mode_grab()
    app_mode()

    def internet_check():
        import requests
        try:
            check = requests.get("https://www.example.com", timeout = 5)
            if check.status_code == 200:
                pass
            else:
                messagebox.showwarning("Internet Connection", "You're not connected to the internet. Some features will not work.")

        except requests.ConnectionError:
            messagebox.showerror("Internet Connection", "Failed to connect to the internet. Restart the program to try again. Without internet some features won't work.")

    def update_dropdown():
        """Update the dropdown menu with the latest credentials."""
        dropdown_menu.configure(values=pwd_options)  # Update the dropdown options
        dropdown_var.set("")  # Reset the selected value to empty

    def delete_cred():
        """Delete the selected credential."""
        selected_option = dropdown_var.get()
        if selected_option:
            del pwd_pwd[selected_option]  # Remove the credential from the dictionary
            pwd_options.remove(selected_option)  # Remove it from the options list
            dropdown_var.set("")  # Reset the dropdown selection
            pwd_entry.delete(0, ctk.END)  # Clear the password entry field
            save_credentials()  # Save the updated credentials
            update_dropdown()  # Update the dropdown menu
        else:
            messagebox.showerror("Error", "Please select a credential to delete.")

    def add_cred():
        """Add a new credential."""
        new_cred = new_cred_entry.get()
        new_cred1_prehash = new_cred_entry1.get()
        new_cred1 = loaded_ferkey.encrypt(new_cred1_prehash.encode())

        if new_cred in pwd_pwd:
            messagebox.showerror("Error", "This Credential already exists.")
            return

        if new_cred and new_cred1:
            pwd_options.append(new_cred)  # Add the new credential to the options list
            pwd_pwd[new_cred] = new_cred1  # Add the encrypted password to the dictionary
            save_credentials()  # Save the updated credentials
            update_dropdown()  # Update the dropdown menu
            new_cred_entry.delete(0, ctk.END)  # Clear the input fields
            new_cred_entry1.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Please enter both Account ID and Password.")


    def save_credentials():
        home_directory = os.path.expanduser('~')
        file_name = 'credentials.pkl'
        file_path = os.path.join(home_directory, file_name)
        try:
            with open(file_path, "wb") as f:
                import pickle
                pickle.dump(pwd_pwd, f)
        except Exception as e:
            messagebox.showerror("AI Password Manager", f"Error saving credentials:{e}")

    def load_credentials():
        home_directory = os.path.expanduser('~')
        file_name = 'credentials.pkl'
        file_path = os.path.join(home_directory, file_name)
        try:
            with open(file_path, "rb") as f:
                import pickle
                return pickle.load(f)
        except FileNotFoundError:
            return {}
        except EOFError:
            return {}
        except Exception as e:
            messagebox.showerror("AI Password Manager", f"Error loading credentials: {e}")
            return {}

    '''
    def save_credentials():
        import json
        try:
            json_data = {k: v.decode() for k, v in pwd_pwd.items()}
            with open(cred_file_path, 'w') as f:
                json.dump(json_data, f)
        except Exception as e:
            messagebox.showerror("AI Password Manager", f"Error saving credentials: {e}")

    def load_credentials():
        import json
        try:
            if os.path.exists(cred_file_path):  # JSON already exists
                with open(cred_file_path, 'r') as f:
                    data = json.load(f)
                return {k: v.encode() for k, v in data.items()}

            elif os.path.exists(cred_full_path):  # Migrate from .pkl
                with open(cred_full_path, 'rb') as f:
                    import pickle
                    data = pickle.load(f)

                # Save as JSON
                try:
                    json_data = {k: v.decode() for k, v in data.items()}
                    with open(cred_file_path, 'w') as f:
                        json.dump(json_data, f)
                    os.remove(cred_full_path)  # only delete if save worked
                except Exception as save_error:
                    messagebox.showerror("APM", f"Failed to migrate credentials to JSON: {save_error}")
                    return data  # fallback to in-memory usage

                return data

            else:
                return {}

        except Exception as e:
            messagebox.showerror("AI Password Manager", f"Error loading credentials: {e}")
            return {}
    '''

    is_shown = 0  

    def pwd_hide():
        global is_shown  # Access the global variable
        pwd_entry.delete(0, 'end')
        is_shown = 0

    def pwd_show():
        global is_shown  # Access the global variable
        selected_option = dropdown_var.get()
        
        if selected_option in pwd_pwd:
            pwd_entry.delete(0, 'end')  # Clear the entry field before inserting the decrypted password

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
                is_shown = 1
            elif encryption_status == "default_key":
                pwd_decrypted = fernet_def.decrypt(pwd_pwd[selected_option]).decode()
                pwd_entry.insert(0, pwd_decrypted)
                is_shown = 1
                messagebox.showwarning(
                    "Encryption",
                    "This credential is using an older encryption method. To switch to the newer encryption method, delete and re-add this credential."
                )
            elif encryption_status == "not_encrypted":
                pwd_entry.insert(0, pwd_pwd[selected_option])
                is_shown = 1
                messagebox.showwarning(
                    "Encryption",
                    "This credential is using an older encryption method. To switch to the newer encryption method, delete and re-add this credential."
                )
        else:
            messagebox.showerror("Error", "No password found for the selected credential.")

    def pwd_sh_clicked():
        global is_shown  # Access the global variable
        if is_shown == 0:
            pwd_show()
            pwd_sh_btn.configure(text=" Hide Password")
        else:
            pwd_hide()
            pwd_sh_btn.configure(text="Show Password")

    def pwd_copy_clicked():
        selected_option = dropdown_var.get()
        if selected_option in pwd_pwd:
            win.clipboard_clear()

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
            elif encryption_status == "default_key":
                pwd_decrypted = fernet_def.decrypt(pwd_pwd[selected_option]).decode()
            elif encryption_status == "not_encrypted":
                pwd_decrypted = pwd_pwd[selected_option]
            else:
                messagebox.showerror("Error", "Could not decrypt the password.")
                return  # Stop function if decryption fails

            # Copy the decrypted password to the clipboard
            win.clipboard_append(pwd_decrypted)
            win.update()
            messagebox.showinfo("AI Password Manager", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "No password found for the selected credential.")

    def pwd_check_clicked():
        password=pwd_check.get()
        if password == "":
            pwd_check_result_text.configure(text="Please enter a password to check.")
        else:
            def get_password_strength(password):
                import zxcvbn
                result = zxcvbn.zxcvbn(password)
                return result['score']
            strength_score = get_password_strength(password)
            if strength_score == 4:
                pwd_check_result_text.configure(text=f"Strength : Strong | Score : {strength_score}/4")
            elif strength_score == 3 :
                pwd_check_result_text.configure(text=f"Strength : Moderate | Score : {strength_score}/4")
            elif strength_score == 2 :
                pwd_check_result_text.configure(text=f"Strength : Ok | Score : {strength_score}/4")
            elif strength_score == 1 :
                pwd_check_result_text.configure(text=f"Strength : Low | Score : {strength_score}/4")
            elif strength_score == 0 :
                pwd_check_result_text.configure(text=f"Strength : Very Low | Score : {strength_score}/4")
            else:
                pwd_check_result_text.configure(text="Unable to obtain score.")

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

    def gen_l12():
        try:
            import json
            import random

            with open(pwd_model) as f:
                model = json.load(f)

            def generate_password(length=12, n=3):
                prefix = random.choice(list(model.keys()))
                result = prefix
                while len(result) < length:
                    next_chars = model.get(prefix)
                    if not next_chars:
                        prefix = random.choice(list(model.keys()))
                        continue
                    next_char = random.choice(next_chars)
                    result += next_char
                    prefix = result[-n:]
                return result
            
            pwd_gen.delete(0, 'end')
            pwd_gen.insert(0, generate_password(length=12, n=3))
        except FileNotFoundError:
            pwd_gen.delete(0, 'end')
            pwd_gen.insert(0, "Unable to generate password. Try again.")

    def gen_l16():
        try:
            import json
            import random

            with open(pwd_model) as f:
                model = json.load(f)

            def generate_password(length=16, n=3):
                prefix = random.choice(list(model.keys()))
                result = prefix
                while len(result) < length:
                    next_chars = model.get(prefix)
                    if not next_chars:
                        prefix = random.choice(list(model.keys()))
                        continue
                    next_char = random.choice(next_chars)
                    result += next_char
                    prefix = result[-n:]
                return result
            
            pwd_gen.delete(0, 'end')
            pwd_gen.insert(0, generate_password(length=16, n=3))
        except FileNotFoundError:
            pwd_gen.delete(0, 'end')
            pwd_gen.insert(0, "Unable to generate password. Try again.")

    def pwd_gen_clicked():
        global length
        if length == 12:
            gen_l12()
        elif length == 16:
            gen_l16()
        else:
            gen_l12()
            
    def pwd_gen_clear():
        pwd_gen.delete(0, 'end')

    # UI

    win = ctk.CTk()
    win.title("AI Password Manager")

    # Theme Mode

    usr_path_with_thm_fl = os.path.join(local_appdata, 'APM', 'theme_mode.txt')

    def theme_mode_val():
        try:
            with open (usr_path_with_thm_fl, 'r') as file:
                thmfl_cmd = file.read().strip()
                try:
                    thm_val = int(thmfl_cmd)
                    return thm_val
                except ValueError:
                    with  open (usr_path_with_thm_fl, 'w') as file:
                        file.write('0')
                    return 0
        except FileNotFoundError:
            with open (usr_path_with_thm_fl, 'w') as file:
                file.write('0')
            return 0
        
    def theme_apply():
        thm_val_agn = theme_mode_val()
        if thm_val_agn == 0:
            ctk.set_default_color_theme("dark-blue")
        elif thm_val_agn == 1:
            pass # Theme Creator
        else:
            messagebox.showerror("Theme Mode", "Unable to apply theme mode. Reverting to default.")
            ctk.set_default_color_theme("dark-blue")

    # Center the window manually
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    window_width = 1290
    window_height = 620
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    win.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    win.resizable(False, False)

    # Set the icon

    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            base_path = sys._MEIPASS  # This is used in the PyInstaller bundle
        except AttributeError:
            base_path = os.path.abspath(os.path.dirname(__file__))

        return os.path.join(base_path, relative_path)

    icon_path_ico = resource_path("_itnrl/icons/apm.ico")
    icon_path_png = resource_path("_itnrl/icons/apm.png")

    if platform.system() == "Windows":
        win.iconbitmap(icon_path_ico)
    elif platform.system() == "Linux":
        from tkinter import PhotoImage
        icon_image = PhotoImage(file=icon_path_png)
        win.iconphoto(False, icon_image)
    else:
        pass


    chk_lclapdt_fldr()

    theme_apply()

    mode_change_init = 1

    internet_check()

    trans_aply_fr()

    scrn_sz_chk()


    title = ctk.CTkLabel(win, text="AI Password Manager", font=("Arial", 25, "bold"))
    title.pack(pady=30, padx=40, anchor="nw")

    # Password Manager Frame

    pwd_gen_text = ctk.CTkLabel(win, text="Password Generator :", font=("Arial", 20, "bold"))
    pwd_gen_text.pack(pady=10, padx=40, anchor="nw")

    pwd_gen = ctk.CTkEntry(win, placeholder_text="Default password length is 12.", width=310, font=("Arial", 15))
    pwd_gen.pack(pady=10, padx=40, anchor="nw")

    pwd_gen_frame = ctk.CTkFrame(win)
    pwd_gen_frame.pack(pady=10, padx=40, anchor="nw")

    pwd_gen_btn = ctk.CTkButton(pwd_gen_frame, text="Generate Password", command=pwd_gen_clicked, width=150, font=("Arial", 15))
    pwd_gen_btn.pack(side="left", padx=(0, 10))

    pwd_gen_clear = ctk.CTkButton(pwd_gen_frame, text="Clear", command=pwd_gen_clear, width=60, font=("Arial", 15))
    pwd_gen_clear.pack(side="left", padx=(0, 10))

    pwd_gen_l_12 = ctk.CTkButton(pwd_gen_frame, text="12", command=l_12, width=20, font=("Arial", 15))
    pwd_gen_l_12.pack(side="left", padx=(0, 10))

    pwd_gen_l_16 = ctk.CTkButton(pwd_gen_frame, text="16", command=l_16, width=20, font=("Arial", 15))
    pwd_gen_l_16.pack(side="left")

    # Password Strength Checker Frame

    pwd_check_text = ctk.CTkLabel(win, text="Password Strength Checker :", font=("Arial", 20, "bold"))
    pwd_check_text.pack(pady=10, padx=40, anchor="nw")

    pwd_check = ctk.CTkEntry(win, placeholder_text="Enter password to check strength.", width=310, font=("Arial", 15))
    pwd_check.pack(pady=10, padx=40, anchor="nw")

    pwd_check_frame = ctk.CTkFrame(win)
    pwd_check_frame.pack(pady=10, padx=40, anchor="nw")

    pwd_check_result_text = ctk.CTkLabel(pwd_check_frame, text="Password strength will be displayed here.", width=290, font=("Arial", 15))
    pwd_check_result_text.pack(pady=0, padx=10)

    pwd_check_btn = ctk.CTkButton(win, text="Check Password", command=pwd_check_clicked, width=150, font=("Arial", 15))
    pwd_check_btn.pack(pady=10, padx=40, anchor="nw")

    # Username Generator Frame

    usrnme_gen_text = ctk.CTkLabel(win, text="Username Generator :", font=("Arial", 20, "bold"))
    usrnme_gen_text.pack(pady=10, padx=40, anchor="nw")

    usrnme_gen_entry = ctk.CTkEntry(win, placeholder_text="Generated Username will appear here.", width=310, font=("Arial", 15))
    usrnme_gen_entry.pack(pady=10, padx=40, anchor="nw")

    usrnme_gen_btn = ctk.CTkButton(win, text="Generate Username", command=usrnme_gen, width=150, font=("Arial", 15))
    usrnme_gen_btn.pack(side="left", pady=10, padx=(40, 10), anchor="nw")

    usrnme_gen_clear = ctk.CTkButton(win, text="Clear", command=usrnme_clear, width=60, font=("Arial", 15))
    usrnme_gen_clear.pack(side="left", pady=10, padx=(0, 40), anchor="nw")

    # Your Credentials Dropdown Frame

    creds_txt = ctk.CTkLabel(win, text="Your Credentials :", font=("Arial", 20, "bold"))
    creds_txt.place(x=450, y=99)

    # Load credentials from file
    pwd_pwd = load_credentials()  # Dictionary to hold credentials (loaded from file)
    #print("Loaded credentials:", pwd_pwd) 

    # Populate the dropdown options from the loaded credentials
    pwd_options = list(pwd_pwd.keys())  # Extract the keys (account names) from the dictionary

    # Initialize the dropdown menu
    dropdown_var = ctk.StringVar(value="Select a Credential")  # Variable to hold the selected dropdown value
    dropdown_menu = ctk.CTkOptionMenu(win, variable=dropdown_var, values=pwd_options, width=382, font=("Arial", 15),command=None)
    dropdown_menu.place(x=450, y=150)

    pwd_entry = ctk.CTkEntry(win, placeholder_text="Password will appear here.", width=382, font=("Arial", 15))
    pwd_entry.place(x=450, y=200)

    pwd_copy_btn = ctk.CTkButton(win, text="Copy Password", command=pwd_copy_clicked, width=100, font=("Arial", 15))
    pwd_copy_btn.place(x=450, y=250)

    pwd_sh_btn = ctk.CTkButton(win, text="Show Password", command=pwd_sh_clicked, width=100, font=("Arial", 15))
    pwd_sh_btn.place(x=575, y=250)

    delete_cred_btn = ctk.CTkButton(win, text="Delete Credential", command=delete_cred, width=100, font=("Arial", 15))
    delete_cred_btn.place(x=702, y=250)

    # Add Credentials Frame

    new_pwd_txt = ctk.CTkLabel(win, text="Add New Credentials :", font=("Arial", 20, "bold"))
    new_pwd_txt.place(x=450, y=320)

    new_cred_entry = ctk.CTkEntry(win, placeholder_text="Enter Your Account ID/Name/Username", width=382, font=("Arial", 15))
    new_cred_entry.place(x=450, y=370)

    new_cred_entry1 = ctk.CTkEntry(win, placeholder_text="Enter Your Password", width=382, font=("Arial", 15))
    new_cred_entry1.place(x=450, y=420)

    add_cred_btn = ctk.CTkButton(win, text="Add Credential", command=add_cred, width=150, font=("Arial", 15))
    add_cred_btn.place(x=450, y=470)

    # Common Passwords Checker Frame

    cmn_pwds_chk_txt = ctk.CTkLabel(win, text="Common Passwords Checker :", font=("Arial", 20, "bold"))
    cmn_pwds_chk_txt.place(x=930, y=99)

    cmn_pwds_chk_etry = ctk.CTkEntry(win, placeholder_text="Enter password to check.", width=290, font=("Arial", 15))
    cmn_pwds_chk_etry.place(x=930, y=150)

    cmn_pwds_result_text_frame = ctk.CTkFrame(win)
    cmn_pwds_result_text_frame.place(x=930, y=200)

    cmn_pwds_result_text = ctk.CTkLabel(cmn_pwds_result_text_frame, text="Password strength will be displayed here.", width=290, font=("Arial", 15))
    cmn_pwds_result_text.pack(pady=0, padx=10)

    cmn_pwds_chk_btn = ctk.CTkButton(win, text="Check Password", command=cmn_pwds_chk, width=150, font=("Arial", 15))
    cmn_pwds_chk_btn.place(x=930, y=250)

    # App Mode

    app_mode_txt = ctk.CTkLabel(win, text="App Mode :", font=("Arial", 20, "bold"))
    app_mode_txt.place(x=930, y=320)

    light_mode_btn = ctk.CTkButton(win, text="Light Mode", command=mode_light, width=100, font=("Arial", 15))
    light_mode_btn.place(x=930, y=370)

    dark_mode_btn = ctk.CTkButton(win, text="Dark Mode", command=mode_dark, width=100, font=("Arial", 15))
    dark_mode_btn.place(x=1050, y=370)

    if sys.platform == "win32":
        trans_btn = ctk.CTkButton(win, text="Transparency Mode", command=trans_act, width=150, font=("Arial", 15))
        trans_btn.place(x=930, y=420)
    else:
        trans_btn = ctk.CTkButton(win, text="Transparency Mode", command=None, width=150, font=("Arial", 15))

    # Bottom Bar Buttons

    about_btn = ctk.CTkButton(win, text="About", command=about, width=50, font=("Arial", 15))
    about_btn.place(x=1220, y=580)

    fdbk_btn = ctk.CTkButton(win, text="Feedback", command=fdbk, width=50, font=("Arial", 15))
    fdbk_btn.place(x=1135, y=580)

    updt_btn = ctk.CTkButton(win, text="Update", command=check_updts, width=50, font=("Arial", 15))
    updt_btn.place(x=1070, y=580)

    reset_btn = ctk.CTkButton(win, text="Reset", command=reset, width=50, font=("Arial", 15))
    reset_btn.place(x=1013, y=580)

    apm_accs_btn = ctk.CTkButton(win, text="APM Accounts", command=apm_func, width=50, font=("Arial", 15))
    apm_accs_btn.place(x=890, y=580)

    m_pwd_win_func()
    app_mode()
    update_dropdown()
    win.mainloop()

def splash_screen():
    from PIL import Image
    import time

    if getattr(sys, 'frozen', False):  # Check if running as compiled EXE
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    splash_png = os.path.join(script_dir, "_itnrl/icons/splash_screen.png")

    splash = Image.open(splash_png)


if __name__ == "__main__":
    #splash_screen()
    main()