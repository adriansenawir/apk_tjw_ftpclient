from ftplib import FTP
from tkinter import Tk, Label, Button, filedialog, Listbox

# Konfigurasi FTP
ftp_host = '127.0.0.1'
ftp_user = 'hidayat'
ftp_password = 'kelompok9'

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            ftp = FTP(ftp_host)
            ftp.login(user=ftp_user, passwd=ftp_password)
            ftp.storbinary(f'STOR {file_path}', file)
            ftp.quit()

def download_file():
    file_name = file_listbox.get(file_listbox.curselection())
    if file_name:
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        with open(file_name, 'wb') as file:
            ftp.retrbinary(f'RETR {file_name}', file.write)
        ftp.quit()

def get_file_list():
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_password)
    file_list = ftp.nlst()
    ftp.quit()
    return file_list

def main():
    root = Tk()
    root.title('Aplikasi FTP')

    label = Label(root, text='Daftar File di Server FTP')
    label.pack()

    file_listbox = Listbox(root)
    file_listbox.pack()

    def refresh_file_list():
        file_list = get_file_list()
        file_listbox.delete(0, 'end')
        for file_name in file_list:
            file_listbox.insert('end', file_name)

    upload_button = Button(root, text='Unggah File', command=upload_file)
    upload_button.pack()

    download_button = Button(root, text='Unduh File', command=download_file)
    download_button.pack()

    refresh_button = Button(root, text='Perbarui Daftar File', command=refresh_file_list)
    refresh_button.pack()

    refresh_file_list()

    root.mainloop()

if __name__ == '__main__':
    main()
