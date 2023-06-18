import ftplib


ftpHost = 'localhost'
ftpPort = 21
ftpUser = 'hidayat'
ftpPass = 'kelompok9'

#buat instance klien FTP, gunakan parameter batas waktu (kedua) hanya untuk koneksi lambat
ftp = ftplib.FTP_TLS(timeout=30) #.FTP / .FTP_TLS (untuk protocol dalam file zilla)

#konek dengan host dan port
ftp.connect(ftpHost, ftpPort)

#untuk masuk ke server
ftp.login(ftpUser, ftpPass)

# mengatur koneksi data yang aman & jangan gunakan selain .cwd
ftp.prot_p() #.FTP_TLS (berpasangan)

# kirim perintah keluar ke server FTP dan tutup koneksi
ftp.quit()

print('eksekusi berhasil.......')