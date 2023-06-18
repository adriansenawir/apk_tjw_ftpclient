import ftplib


ftpHost = 'localhost'
ftpPort = 21
ftpUser = 'hidayat'
ftpPass = 'kelompok9'

#buat instance klien FTP, gunakan parameter batas waktu (kedua) hanya untuk koneksi lambat
ftp = ftplib.FTP(timeout=30) #.FTP / .FTP_TLS (untuk protocol dalam file zilla)

#konek dengan host dan port
ftp.connect(ftpHost, ftpPort)

#untuk masuk ke server
ftp.login(ftpUser, ftpPass)

#.cwd untuk mengindentifikasi alamat dari file nya (folderBaru/abcd)
ftp.cwd("folderBaru")

targetUnduh = "kontol.txt"

ftp.rename(targetUnduh, "ilahi.txt")

# kirim perintah keluar ke server FTP dan tutup koneksi
ftp.quit()
print ("File berhasil dieksekusi......")
