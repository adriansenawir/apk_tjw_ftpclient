import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import simpledialog
from ftplib import FTP
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_appearance_mode("DARK")
customtkinter.set_default_color_theme("dark-blue")

# Konfigurasi FTP
ftp_host = '127.0.0.1'
ftp_port = 21

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('700x500')

        frame = tk.Frame(root, bg='#636363', borderwidth=15, relief="raised", takefocus=True)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        label_title = tk.Label(self.root, text="RUKONT FTP CLIENT", font=("georgia", 32, "bold"), bg="#636363", fg="white")
        label_title.place(relx=0.5, rely=0.3, anchor="center")

        label_username = tk.Label(frame, text='Username:', font=('roboto', 12), bd=0, bg='#636363', fg='white')
        label_username.grid(row=0, column=0, padx=5, pady=5)

        self.entry_username = tk.Entry(frame, font=('roboto', 12), cursor="ibeam")
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        label_password = tk.Label(frame, text='Password:', font=('roboto', 12), bd=0, bg='#636363', fg='white')
        label_password.grid(row=1, column=0, padx=5, pady=5)

        self.entry_password = tk.Entry(frame, show='*', font=('roboto', 12), cursor="ibeam")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(frame, text='Login', command=self.login, font=('roboto', 12), relief="raised", background="grey")
        login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

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


        self.root = customtkinter.CTk()
        self.root.title('File Directory')
        self.root.geometry('700x500')

        # frame = tk.Frame(self.root, bg='#636363', borderwidth=15, relief="raised", height=20, width=50)
        # frame.place(relx=0.5, rely=0.5, anchor='center')

        label = tk.Label(self.root, text='List of Files in Server', font=('roboto', 32))
        # label.grid(row=0, column=1, sticky=tk.N)

        self.treeview = ttk.Treeview(self.root, columns=('Name', 'Size'), show='headings', height=20)
        self.treeview.heading('Name', text='Name', anchor="center")
        self.treeview.heading('Size', text='Size', anchor="center")
        self.treeview.pack(expand=True)
        self.treeview.column('Name', width=500, anchor="center")
        self.treeview.column('Size', width=200, anchor="center")

        upload_button = tk.Button(self.root, text='Upload File', command=self.upload_file, font=('roboto', 12), bd=0, bg='#1F6E8C', fg='white')
        upload_button.place(relx=0.5)
        upload_button.pack(expand=True)

        # download_button = tk.Button(self.root, text='Download File', command=self.download_file, font=('roboto', 12), bd=0, bg='#1F6E8C', fg='white')
        # download_button.place(x=450, y=150)

        # delete_button = tk.Button(self.root, text='Delete File', command=self.delete_file, font=('roboto', 12), bd=0, bg='#1F6E8C', fg='white')
        # delete_button.place(x=450, y=200)

        # rename_button = tk.Button(self.root, text='Rename File', command=self.rename_file, font=('roboto', 12), bd=0, bg='#1F6E8C', fg='white')
        # rename_button.place(x=450, y=250)

        # back_button = tk.Button(self.root, text='Logout', command=self.back_to_login, font=('roboto', 12), bd=0, bg='#1F6E8C', fg='white')
        # back_button.place(x=10, y=430)

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
        root = customtkinter.CTk()
        login_window = LoginWindow(root)
        root.mainloop()

    def close_app(self):
        self.ftp.quit()
        self.root.destroy()

def main():
    root = customtkinter.CTk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
