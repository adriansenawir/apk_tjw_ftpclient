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

targetUnduh = "456.png"
localFilePath = targetUnduh

with open (localFilePath, 'wb') as file:
    retCode = ftp.retrbinary(f"RETR {targetUnduh}", file.write)


# kirim perintah keluar ke server FTP dan tutup koneksi
ftp.quit()

if retCode.startswith("226"):
    print ("File berhasil diunggah")
else:
    print("terjadi kesalahan")
