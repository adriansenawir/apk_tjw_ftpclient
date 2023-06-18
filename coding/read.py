import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import simpledialog
from ftplib import FTP
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk

# Konfigurasi FTP
ftp_host = '127.0.0.1'
ftp_port = 21

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('700x500')

        background_image = Image.open('background.jpg')  # Ganti dengan path gambar latar belakang Anda
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label_username = tk.Label(root, text='Username', font=('Arial', 12))
        label_username.place(x=100, y=100)

        self.entry_username = tk.Entry(root, font=('Arial', 12))
        self.entry_username.place(x=200, y=100)

        label_password = tk.Label(root, text='Password', font=('Arial', 12))
        label_password.place(x=100, y=150)

        self.entry_password = tk.Entry(root, show='*', font=('Arial', 12))
        self.entry_password.place(x=200, y=150)

        login_button = tk.Button(root, text='Login', command=self.login, font=('Arial', 12))
        login_button.place(x=250, y=200)

        background_label.image = background_photo

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
        self.root.title('Aplikasi FTP')
        self.root.geometry('700x500')

        background_image = Image.open('background.jpg')  # Ganti dengan path gambar latar belakang Anda
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self.root, text='Daftar File di Server FTP', font=('Arial', 17))
        label.place(x=10, y=10)

        self.treeview = ttk.Treeview(self.root, columns=('Name', 'Size'), show='headings', height=15)
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Size', text='Size')
        self.treeview.place(x=10, y=50)

        self.treeview.column('Name', width=300)
        self.treeview.column('Size', width=100)

        upload_button = tk.Button(self.root, text='Unggah File', command=self.upload_file, font=('Arial', 12))
        upload_button.place(x=450, y=100)

        download_button = tk.Button(self.root, text='Unduh File', command=self.download_file, font=('Arial', 12))
        download_button.place(x=450, y=150)

        delete_button = tk.Button(self.root, text='Hapus File', command=self.delete_file, font=('Arial', 12))
        delete_button.place(x=450, y=200)

        rename_button = tk.Button(self.root, text='Rename File', command=self.rename_file, font=('Arial', 12))
        rename_button.place(x=450, y=250)

        back_button = tk.Button(self.root, text='LogOut', command=self.back_to_login, font=('Arial', 12))
        back_button.place(x=10, y=400)  # Mengatur posisi tombol "Kembali" di sudut kiri atas

        background_label.image = background_photo

        self.refresh_file_list()

        self.root.mainloop()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_name = file_path.split('/')[-1]  # Mengambil nama file dari path
                self.ftp.storbinary(f'STOR {file_name}', file)  # Menggunakan nama file
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
                # Konversi ukuran file menjadi format yang lebih mudah dibaca
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

def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
