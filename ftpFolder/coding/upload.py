import ftplib


ftpHost = 'localhost'
ftpPort = 21
ftpUser = 'aco'
ftpPass = 'kelompok9'

#buat instance klien FTP, gunakan parameter batas waktu (kedua) hanya untuk koneksi lambat
ftp = ftplib.FTP(timeout=30) #.FTP / .FTP_TLS (untuk protocol dalam file zilla)

#konek dengan host dan port
ftp.connect(ftpHost, ftpPort)

#untuk masuk ke server
ftp.login(ftpUser, ftpPass)

#///kerjanya aplikasi

# upload file
ftp.cwd("folderBaru")
localFilePath = "unduh.py"
with open(localFilePath, 'rb') as file :
    retCode = ftp.storbinary("STOR coding", file, blocksize=1024*1024)


# kirim perintah keluar ke server FTP dan tutup koneksi
ftp.quit()

if retCode.startswith("226"):
    print("File berhasil diunggah")
else:
    print("gagal")
