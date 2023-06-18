import ftplib

ftpHost = '127.0.0.1'
ftpPort = 21
ftpUser = input("User : ") #'hidayat'
ftpPass = input("Password : ")#'kelompok9'

#buat instance klien FTP, gunakan parameter batas waktu (kedua) hanya untuk koneksi lambat
ftp = ftplib.FTP(timeout=30) #.FTP / .FTP_TLS (untuk protocol dalam file zilla)

#konek dengan host dan port
ftp.connect(ftpHost, ftpPort)

#untuk masuk ke server
ftp.login(ftpUser, ftpPass)


#///kerjanya aplikasi

#.cwd untuk mengindentifikasi alamat dari file nya (folderBaru/abcd)
ftp.cwd("folderBaru") #lokasi ynag mau dibaca

#.nlst untuk mendapatkan daftar nama file
cekisi = ftp.nlst()
print(cekisi)



# kirim perintah keluar ke server FTP dan tutup koneksi
ftp.quit()

print('eksekusi berhasil.......')