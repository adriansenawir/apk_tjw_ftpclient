import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import simpledialog
from ftplib import FTP
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import customtkinter

# Konfigurasi FTP
ftp_host = '127.0.0.1'
ftp_port = 21

import tkinter as tk
from ftplib import FTP
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('800x700')

        image = Image.open('background7.jpg')
        image = image.resize((800, 700), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = ttk.Label(root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        label_username = tk.Label(root, text='Username:', font=('roboto', 12), bd=0, bg='#95aeee', fg='black')
        label_username.place(relx=0.8, rely=0.43, anchor="center")

        self.entry_username = tk.Entry(root, font=('roboto', 12), cursor="ibeam")
        self.entry_username.place(relx=0.8, rely=0.46, anchor="center")

        label_password = tk.Label(root, text='Password:', font=('roboto', 12), bd=0, bg='#95aeee', fg='black')
        label_password.place(relx=0.8, rely=0.5, anchor="center")

        self.entry_password = tk.Entry(root, show='*', font=('roboto', 12), cursor="ibeam")
        self.entry_password.place(relx=0.8, rely=0.54, anchor="center")

        self.login_button = tk.Button(root, text='Login', command=self.login, font=('roboto', 12, "bold"), fg="white",relief="raised",background="#5380DE", bd=5, state=tk.DISABLED)
        self.login_button.place(relx=0.8, rely=0.6, anchor="center")

        self.entry_username.bind("<KeyRelease>", self.check_input)
        self.entry_password.bind("<KeyRelease>", self.check_input)

    def check_input(self, event):
        if self.entry_username.get() and self.entry_password.get():
            self.login_button.config(state=tk.NORMAL)
        else:
            self.login_button.config(state=tk.DISABLED)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        ftp = FTP()
        try:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(user=username, passwd=password)
            self.root.destroy()
            FTPClientApp(ftp)
        except:
            messagebox.showerror('Login Failed', 'Failed to connect to the FTP server.')


class FTPClientApp:
    def __init__(self, ftp):
        self.ftp = ftp


        self.root = tk.Tk()
        self.root.configure(bg="#95AEEE")
        self.root.title('File Directory')
        self.root.geometry('800x700')

        frame_label = tk.Frame(self.root,bg='#987eff', borderwidth=15, relief="raised" )
        frame_label.pack()

        frame_tabel = tk.Frame(self.root, bg='#987eff', borderwidth=15, relief="raised")
        frame_tabel.pack()

        frame_button = tk.Frame(self.root, bg = "#9747ff", highlightbackground="white", highlightcolor="white", highlightthickness=10, relief="solid" )
        frame_button.pack(pady=10, ipadx=20,ipady=10)

        label = tk.Label(frame_label, text='List of Files in Server', font=('roboto', 32, "bold"))
        label.pack()

        self.treeview = ttk.Treeview(frame_tabel, columns=('Name', 'Size'), show='headings', height=20)
        self.treeview.heading('Name', text='Name', anchor="center")
        self.treeview.heading('Size', text='Size', anchor="center")
        self.treeview.pack()
        self.treeview.column('Name', width=500, anchor="center")
        self.treeview.column('Size', width=200, anchor="center")


        upload_button = tk.Button(frame_button, text='Upload File', command=self.upload_file, font=('roboto', 12,"bold"), bd=5, bg='#5380DE', fg='white',relief="raised")
        upload_button.pack(side='left',expand=True)

        download_button = tk.Button(frame_button, text='Download File', command=self.download_file, font=('roboto', 12,"bold"), bd=5, bg='#5380DE', fg='white', relief="raised")
        download_button.pack(side='left',expand=True)

        delete_button = tk.Button(frame_button, text='Delete File', command=self.delete_file, font=('roboto', 12,"bold"), bd=5, bg='#5380DE', fg='white',relief="raised")
        delete_button.pack(side='left',expand=True)

        rename_button = tk.Button(frame_button, text='Rename File', command=self.rename_file, font=('roboto', 12,"bold"), bd=5, bg='#5380DE', fg='white',relief="raised")
        rename_button.pack(side='left',expand=True)

        back_button = tk.Button(frame_button, text='Logout', command=self.back_to_login, font=('roboto', 12,"bold"), bd=5, bg='#5380DE', fg='white')
        back_button.pack(side='left',expand=True)
        

        self.refresh_file_list()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_name = file_path.split('/')[-1]
                self.ftp.storbinary(f'STOR {file_name}', file)
                self.refresh_file_list()

    def download_file(self):
        download_dir = filedialog.askdirectory()
        selected_item = self.treeview.selection()
        if selected_item and download_dir:
            file_name = self.treeview.item(selected_item)['values'][0]
            with open(f"{download_dir}/{file_name}", 'wb') as file:
                self.ftp.retrbinary(f'RETR {file_name}', file.write)

    def delete_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item)['values'][0]
            self.ftp.delete(file_name)
            self.refresh_file_list()

    def rename_file(self):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item)['values'][0]
            new_name = simpledialog.askstring('Rename File', f'Enter new name for {file_name}:')
            if new_name:
                self.ftp.rename(file_name, new_name)
                self.refresh_file_list()

    def refresh_file_list(self):
        file_list = self.ftp.nlst()
        self.treeview.delete(*self.treeview.get_children())
        for file_name in file_list:
            file_size = self.get_file_size(file_name)
            self.treeview.insert('', 'end', values=(file_name, file_size))

    def get_file_size(self, file_name):
        try:
            file_size = self.ftp.size(file_name)
            if file_size is not None:
                size_units = ['B', 'KB', 'MB', 'GB']
                unit_index = 0
                while file_size >= 1024 and unit_index < len(size_units) - 1:
                    file_size /= 1024
                    unit_index += 1
                return f"{file_size:.2f} {size_units[unit_index]}"
        except:
            pass
        return 'Unknown'

    def back_to_login(self):
        self.ftp.quit()
        self.root.destroy()
        root = tk.Tk()
        login_window = LoginWindow(root)
        root.mainloop()

    def close_app(self):
        self.ftp.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
