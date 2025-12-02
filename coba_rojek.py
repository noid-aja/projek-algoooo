import psycopg2
import pandas as pd
import tabulate as tb
import pyfiglet as pf
from colorama import init, Fore, Style
import questionary as q
from datetime import date, datetime, timedelta
import traceback

# koneksi antar python dengan database
def connectDB():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "dizy1234",
            dbname = "aidb",
            port = "5432"
        )
        cur = conn.cursor()
        # print("Koneksi Berhasil") # buat ngasi kejelasan kalo db ini serius
        return conn, cur
    except Exception as e:
        print("Koneksi gagal, coba lagi")
        # v jaga2 kalo error nya di database v
        print("Detail error:", e)
        return None, None

connectDB()

# biar color berubah tanpa harus reset di setiap fungsi
init(autoreset=True)

# clear sistem buat gk rame dan lebih jelas
def bersih_terminal():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

# judul program
def header():
    bersih_terminal()
    title = pf.figlet_format("SEWA ALAT PERTANIAN", font="slant")
    print(Fore.GREEN + title)
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + Style.BRIGHT + "   SISTEM PEMINJAMAN & PENYEWAAN ALAT PERTANIAN")
    print(Fore.CYAN + "="*60)
    print()

# menu utama
def menu_utama():
    while True:
        header()
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║" + Fore.CYAN + "                    MENU UTAMA                          " + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "👤  Login sebagai Peminjam",
                "🏪  Login sebagai Owner/Pemilik",
                "📝  Registrasi Akun Peminjam",
                "❌  Keluar"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
                
        if pilihan == "👤  Login sebagai Peminjam":
            login_peminjam()
        elif pilihan == "🏪  Login sebagai Owner/Pemilik":
            login_owner()
        elif pilihan == "📝  Registrasi Akun Peminjam":
            registrasi()
        elif pilihan == "❌  Keluar":
            bersih_terminal()
            print(Fore.GREEN + Style.BRIGHT + "\n✨ Terima kasih telah menggunakan aplikasi kami! ✨\n")
            return
        else:
            print(Fore.RED + "\n❌ Pilihan tidak valid! Tekan Enter untuk kembali...")
            input()

# login peminjam
def login_peminjam():
    global peminjam_id

    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "              LOGIN SEBAGAI PEMINJAM                    " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    while True:
        username = input(Fore.CYAN + "Username: " + Fore.WHITE)
        password = input(Fore.CYAN + "Password: " + Fore.WHITE)
        
        print()
        print(Fore.YELLOW + "⏳ Memproses login...")
        
        try:
            conn, cursor = connectDB()

            query = "SELECT * FROM peminjam WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))

            result = cursor.fetchone()

            if result:
                peminjam_id = result[0]
                print(Fore.GREEN + "✅ Login berhasil!")
                print(Fore.CYAN + f"Selamat datang, {username}!")
                break
            else:
                print(Fore.RED + "❌ Username atau password salah. Silakan coba lagi.")

        except psycopg2.Error as e:
            print(Fore.RED + f"Error database: {e}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    input(Fore.WHITE + "\nTekan Enter untuk melanjutkan...")
    menu_peminjam()

# login owner
def login_owner():
    global owner_id_skrg


    header()
    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + "           LOGIN SEBAGAI OWNER/PEMILIK                  " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    while True:
        username = input(Fore.CYAN + "Username: " + Fore.WHITE)
        password = input(Fore.CYAN + "Password: " + Fore.WHITE)

        print()

        try:
            conn, cursor = connectDB()

            query = "SELECT * FROM owners WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))

            result = cursor.fetchone()

            if result:
                owner_id_skrg = result[0]
                print(Fore.GREEN + "✅ Login berhasil!")
                print(Fore.CYAN + f"Selamat datang, {username}!")
                break
            else:
                print(Fore.RED + "❌ Username atau password salah. Silakan coba lagi.")

        except psycopg2.Error as e:
            print(Fore.RED + f"Error database: {e}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    input(Fore.WHITE + "\nTekan Enter untuk melanjutkan...")
    menu_owner()

# registrasi akun peminjam
def registrasi():
    header()
    print(Fore.BLUE + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.BLUE + Style.BRIGHT + "║" + Fore.WHITE + " REGISTRASI AKUN PEMINJAM " + Fore.BLUE + "║")
    print(Fore.BLUE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    while True:
        conn = None
        cursor = None
        try:
            username = input(Fore.CYAN + "Username baru: " + Fore.WHITE)
            password = input(Fore.CYAN + "Password     : " + Fore.WHITE)

            # NO HP: harus mulai 08, digit semua, panjang 10–13
            while True:
                no_hp = input(Fore.CYAN + "No. HP (wajib mulai 08, 10-13 digit): " + Fore.WHITE)

                if not no_hp.isdigit():
                    print(Fore.RED + "❌ No. HP harus angka semua!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang No. HP...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi ulang data (No. HP salah).")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    continue


                if not no_hp.startswith("08"):
                    print(Fore.RED + "❌ No. HP harus diawali '08' (contoh: 08xxxxxxxxxx)!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang No. HP...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi ulang data (No. HP salah).")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    continue


                if not (10 <= len(no_hp) <= 13):
                    print(Fore.RED + "❌ No. HP harus 10–13 digit!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang No. HP...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi ulang data (No. HP salah).")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    continue
                break

            # NIK wajib 16 digit
            while True:
                nik = input(Fore.CYAN + "NIK (16 digit): " + Fore.WHITE)
                if not nik.isdigit():
                    print(Fore.RED + "❌ NIK harus angka!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang NIK...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi data lagi (NIK salah).")
                    print()
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}")
                    continue
                if len(nik) != 16:
                    print(Fore.RED + "❌ NIK harus tepat 16 digit!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang NIK...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi data lagi (NIK salah).")
                    print()
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}")
                    continue
                break

            # Tanggal lahir wajib format YYYY-MM-DD

            while True:
                tanggal_lahir_str = input(Fore.CYAN + "Tanggal Lahir (YYYY-MM-DD) Contoh: 2000-01-31: " + Fore.WHITE)
                try:
                    tanggal_lahir = datetime.strptime(tanggal_lahir_str, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print(Fore.RED + "❌ Format tanggal salah!")
                    input(Fore.WHITE + "Tekan Enter untuk ulangi input...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi data lagi (Tanggal Lahir salah).")
                    print()
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}")
                    print(Fore.WHITE + f"NIK      : {nik}")
                    continue


            # Alamat
            jalan = input(Fore.CYAN + "Nama Jalan (contoh: Jl. Mawar No. 10): " + Fore.WHITE)
            nama_desa = input(Fore.CYAN + "Desa                     : " + Fore.WHITE)
            nama_kecamatan = input(Fore.CYAN + "Kecamatan                : " + Fore.WHITE)


            # Verifikasi lagi
            bersih_terminal()
            header()
            print(Fore.GREEN + Style.BRIGHT + "⚙️ VERIFIKASI DATA REGISTRASI")
            print(Fore.CYAN + "-" * 60)
            print(Fore.WHITE + f"Username       : {username}")
            print(Fore.WHITE + f"No. HP         : {no_hp}")
            print(Fore.WHITE + f"NIK            : {nik}")
            print(Fore.WHITE + f"Tanggal Lahir  : {tanggal_lahir}")
            print(Fore.WHITE + f"Jalan          : {jalan}")
            print(Fore.WHITE + f"Desa           : {nama_desa}")
            print(Fore.WHITE + f"Kecamatan      : {nama_kecamatan}")
            print(Fore.CYAN + "-" * 60)


            konfirmasi = input(Fore.YELLOW + "Apakah data sudah benar? (y/n): " + Fore.WHITE).lower()
            if konfirmasi != "y":
                print(Fore.YELLOW + "🔁 Data dibatalkan, silakan input ulang.")
                input(Fore.WHITE + "Tekan Enter untuk mulai dari awal...")
                bersih_terminal()
                header()
                continue  # ulang dari awal, layar sudah bersih


            print(Fore.YELLOW + "⏳ Memproses registrasi...")


            # ---------- SIMPAN KE DATABASE ----------
            conn, cursor = connectDB()
            if conn is None:
                print(Fore.RED + "❌ Gagal terhubung ke database")
                input()
                bersih_terminal()
                break


            # Desa
            cursor.execute("SELECT iddesa FROM Desa WHERE desa = %s", (nama_desa,))
            row_desa = cursor.fetchone()
            if row_desa:
                iddesa = row_desa
            else:
                cursor.execute("INSERT INTO Desa (desa) VALUES (%s) RETURNING iddesa", (nama_desa,))
                iddesa = cursor.fetchone()


            # Kecamatan
            cursor.execute(
                "SELECT idkecamatan FROM Kecamatan WHERE kecamatan = %s AND iddesa = %s",
                (nama_kecamatan, iddesa)
            )
            row_kec = cursor.fetchone()
            if row_kec:
                idkecamatan = row_kec
            else:
                cursor.execute(
                    "INSERT INTO Kecamatan (kecamatan, iddesa) VALUES (%s, %s) RETURNING idkecamatan",
                    (nama_kecamatan, iddesa)
                )
                idkecamatan = cursor.fetchone()


            # Alamat
            cursor.execute(
                "INSERT INTO Alamat (jalan, idkecamatan) VALUES (%s, %s) RETURNING idalamat",
                (jalan, idkecamatan)
            )
            idalamat = cursor.fetchone()


            # Peminjam
            query_peminjam = """
                INSERT INTO Peminjam 
                    (username, password, nohp, nik, tanggallahir, idalamat) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query_peminjam,
                (username, password, no_hp, nik, tanggal_lahir, idalamat)
            )
            conn.commit()


            bersih_terminal()
            header()
            print(Fore.GREEN + "✅ Registrasi berhasil!")
            print(Fore.CYAN + "Silakan login dengan akun Anda.")
            input(Fore.WHITE + "\nTekan Enter untuk kembali...")
            break  # keluar dari while True registrasi


        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            bersih_terminal()
            header()
            print(Fore.RED + f"❌ Gagal registrasi: {e}")
            input(Fore.WHITE + "Tekan Enter untuk coba lagi...")
            bersih_terminal()
            header()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


# menu peminjam
def menu_peminjam():
    while True:
        header()
        print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  MENU PEMINJAM                         " + Fore.GREEN + "║")
        print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                # "🔍  Lihat Alat Tersedia",
                "📮  Pinjam Alat",
                "📋  Riwayat Peminjaman Saya",
                "↩   Kembalikan Alat",
                "❌  Logout"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
        
        # if pilihan == "🔍  Lihat Alat Tersedia":
            # lihat_alat_tersedia()

        if pilihan == "📮  Pinjam Alat":
            conn, cur = connectDB()
            ajukan_peminjaman_alat(conn, cur, peminjam_id, [])

        elif pilihan == "📋  Riwayat Peminjaman Saya":
            lihat_riwayat_peminjaman()

        elif pilihan == "↩   Kembalikan Alat":
            kembalikan_alat()

        elif pilihan == "❌  Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")


# lihat alat tersedia
def ajukan_peminjaman_alat(conn, cur, id_peminjam, rows):
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                 PINJAM ALAT                     " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    conn, cur = connectDB()
    
    if conn is None or cur is None:
        print(Fore.RED + "\n❌ Gagal terhubung ke database.")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return


    try:
        query = """
        SELECT 
        a.idalat AS ID, a.namaalat AS Nama_Alat,
        'RP. ' || a.hargaalat AS Harga,
        a.deskripsialat AS Deskripsi,
        a.diskonalat || '%' AS Diskon,
        k.kondisi AS Nama_Kondisi,
        s.status AS Status_Alat
        FROM AlatPertanian a
        JOIN KondisiAlat k USING (idkondisialat)
        JOIN StatusAlat s USING (idstatusalat)
        WHERE s.status = 'Tersedia'
        """
        cur.execute(query)
        rows = cur.fetchall()


        if rows:
            # Buat DataFrame dengan kolom yang spesifik
            df = pd.DataFrame(rows, columns=['ID', 'Nama Alat', 'Harga', 'Deskripsi', 'Diskon', 'Kondisi', 'Status Alat'])
            
            # Tampilkan tabel dengan format yang lebih baik
            print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
            print()

            # Input dari user
            idalat = int(input(Fore.CYAN + "Masukkan ID alat yang ingin disewa: " + Fore.WHITE))
            lama_hari = int(input(Fore.CYAN + "Lama peminjaman (hari): " + Fore.WHITE))

            # Hitung tanggal
            today = date.today()
            tenggat = today + timedelta(days=lama_hari)

            # Ambil harga & diskon dari database
            cur.execute("SELECT hargaalat, diskonalat FROM AlatPertanian WHERE idalat = %s", (idalat,))
            alat = cur.fetchone()
            
            if not alat:
                raise ValueError(f"❌ ID alat {idalat} tidak ditemukan")

            harga_alat, diskon_alat = alat
            harga_setelah_diskon = harga_alat - (diskon_alat or 0)
            dp = int(0.2 * harga_setelah_diskon)  # DP 20%

            # ✅ INSERT ke Peminjaman - SESUAI STRUKTUR TABEL
            insert_peminjaman = """
                INSERT INTO Peminjaman (
                    idpeminjam,
                    tanggalpeminjaman,
                    tenggatpeminjaman,
                    dp,
                    deskripsi,
                    idstatuspeminjaman
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING idpeminjaman;
            """
            deskripsi = f"Peminjaman alat ID {idalat}"
            idstatus = 1  # Status: Pending

            cur.execute(insert_peminjaman, (id_peminjam, today, tenggat, dp, deskripsi, idstatus))
            id_peminjaman_baru = cur.fetchone()[0]
            print(Fore.GREEN + f"\n✅ Peminjaman dibuat dengan ID: {id_peminjaman_baru}")

            insert_detail = """
                INSERT INTO DetailPeminjaman (idpeminjaman, idalat, harga, diskon)
                VALUES (%s, %s, %s, %s);
            """
            cur.execute(insert_detail, (id_peminjaman_baru, idalat, harga_alat, diskon_alat))
            print(Fore.GREEN + "✅ Detail peminjaman ditambahkan")

            conn.commit()
            print(Fore.GREEN + "\n✅✅✅ Peminjaman berhasil diajukan!")
            print(Fore.YELLOW + f"Status Peminjaman: Pending (Menunggu Persetujuan Owner)")
            print(Fore.YELLOW + f"DP yang harus dibayar: RP {dp:,}")
            input(Fore.WHITE + "\nTekan Enter untuk kembali...")
            return id_peminjaman_baru
        else:
            print(Fore.YELLOW + "\n⚠ Tidak ada alat pertanian yang tersedia saat ini.")
            input(Fore.WHITE + "\nTekan Enter untuk kembali...")
            return None
                
    except ValueError as e:
        # Error validasi (alat tidak ditemukan, dll)
        print(Fore.RED + f"\n❌ Error Validasi: {e}")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None
        
    except Exception as e:
        # Error lainnya (database, dll)
        conn.rollback()  # ✅ ROLLBACK jika error
        print(Fore.RED + f"\n❌ Terjadi kesalahan: {type(e).__name__}")
        print(Fore.RED + f"📝 Pesan: {e}")
        print(Fore.RED + "\n🐛 Detail error untuk debugging:")
        traceback.print_exc()
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None


def lihat_riwayat_peminjaman():
    global peminjam_id
    header()
    print(Fore.CYAN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + "             RIWAYAT PEMINJAMAN SAYA                    " + Fore.CYAN + "║")
    print(Fore.CYAN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return

        # Query history peminjaman (semua status, bukan hanya yang selesai)
        query = """
        SELECT 
            p.idpeminjaman,
            a.namaalat as Nama_Alat,
            'RP ' || dp.harga::TEXT as Harga_Satuan,
            'RP ' || dp.diskon::TEXT as Diskon,
            p.tanggalpeminjaman as Tgl_Pinjam,
            p.tenggatpeminjaman as Tgl_Tenggat,
            sp.statuspeminjaman as Status,
            COALESCE(pr.tanggalpengembalian::TEXT, '-') as Tgl_Kembali
        FROM Peminjaman p
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        LEFT JOIN Pengembalian pr ON p.idpeminjaman = pr.idpeminjaman
        WHERE p.idpeminjam = %s
        ORDER BY p.idpeminjaman DESC
        """
        cur.execute(query, (peminjam_id,))
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "⚠️ Anda belum memiliki riwayat peminjaman.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
        
        df = pd.DataFrame(rows, columns=['ID Peminjaman', 'Nama Alat', 'Harga', 'Diskon', 'Tgl Pinjam', 'Tgl Tenggat', 'Status', 'Tgl Kembali'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()
        
        # Statistik
        total_peminjaman = len(rows)
        selesai = sum(1 for row in rows if row[6] == 'Dikembalikan')
        pending = sum(1 for row in rows if row[6] == 'Pending')
        disetujui = sum(1 for row in rows if row[6] == 'Disetujui')
        
        print(Fore.YELLOW + f"\n📊 Statistik:")
        print(Fore.WHITE + f"   Total Peminjaman: {total_peminjaman}")
        print(Fore.GREEN + f"   ✅ Selesai (Dikembalikan): {selesai}")
        print(Fore.YELLOW + f"   ⏳ Disetujui: {disetujui}")
        print(Fore.CYAN + f"   ⏰ Pending: {pending}")
        
        input(Fore.WHITE + "\nTekan Enter untuk kembali...")

    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input()
    finally:
        if conn:
            cur.close()
            conn.close()

def kembalikan_alat():
    global peminjam_id
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  ALAT YANG TERSEDIA                    " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    try:
        conn, cur = connectDB()
        if conn is None or cur is None:
            print(Fore.RED + "\n❌ Gagal terhubung ke database.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
    
        # Tampilkan peminjaman aktif
        query = """
        SELECT p.idpeminjaman, a.namaalat, p.tanggalpeminjaman, 
               p.tenggatpeminjaman, sp.statuspeminjaman
        FROM Peminjaman p
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        WHERE p.idpeminjam = %s AND sp.statuspeminjaman = 'Sedang Disewakan'
        """
        
        cur.execute(query, (peminjam_id,))
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada peminjaman aktif.")
            input()
            return

        df = pd.DataFrame(rows, columns=['ID Pinjam', 'Alat', 'Tgl Pinjam', 'Tenggat', 'Status'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()

        idpeminjaman = int(input(Fore.CYAN + "Masukkan ID peminjaman yang ingin dikembalikan: " + Fore.WHITE))
        
        # Cek apakah peminjaman ada
        cur.execute("SELECT tenggatpeminjaman FROM Peminjaman WHERE idpeminjaman = %s AND idpeminjam = %s", 
                   (idpeminjaman, peminjam_id))
        result = cur.fetchone()

        if not result:
            print(Fore.RED + "❌ ID peminjaman tidak ditemukan atau bukan milik Anda!")
            input()
            return

        tenggat = result[0]
        today = date.today()
        iddenda = None

        # Cek denda jika terlambat
        if today > tenggat:
            hari_telat = (today - tenggat).days
            print(Fore.RED + f"⚠️ Anda terlambat {hari_telat} hari!")
            
            # Insert denda
            query_denda = """
            INSERT INTO Denda (jenispelanggaran, biayadenda)
            VALUES (%s, %s)
            RETURNING iddenda
            """
            cur.execute(query_denda, (f"Keterlambatan {hari_telat} hari", 50000 * hari_telat))
            iddenda = cur.fetchone()[0]
            print(Fore.YELLOW + f"💰 Denda: RP. {50000 * hari_telat}")

        # Insert pengembalian
        query_pengembalian = """
        INSERT INTO Pengembalian (tanggalpengembalian, idpeminjaman, idstatuspengembalian, iddenda)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query_pengembalian, (today, idpeminjaman, 1, iddenda))

        # Update status peminjaman
        cur.execute("UPDATE Peminjaman SET idstatuspeminjaman = 5 WHERE idpeminjaman = %s", (idpeminjaman,))

        # Update status alat
        cur.execute("SELECT idalat FROM DetailPeminjaman WHERE idpeminjaman = %s", (idpeminjaman,))
        idalat = cur.fetchone()[0]
        cur.execute("SELECT idstatusalat FROM StatusAlat WHERE status = 'Tersedia'")
        idstatus_tersedia = cur.fetchone()[0]
        cur.execute("UPDATE AlatPertanian SET idstatusalat = %s WHERE idalat = %s", (idstatus_tersedia, idalat))

        conn.commit()

        print()
        print(Fore.GREEN + "✅ Pengembalian berhasil diproses!")
        input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")

    except ValueError:
        print(Fore.RED + "❌ Input tidak valid!")
        input()
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input()
    finally:
        if conn:
            cur.close()
            conn.close()

# ajukan persetujuan peminjaman
def ajukan_peminjaman(conn, cur, id_peminjam, rows):
    """
    Fungsi untuk mengajukan peminjaman alat
    
    Parameters:
    - conn: Connection object dari connectDB()
    - cur: Cursor object dari connectDB()
    - id_peminjam: ID peminjam yang login
    - rows: Data alat dari query sebelumnya
    """
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  AJUKAN PERSETUJUAN PEMINJAMAN                    " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    try:
        # Validasi connection
        if conn is None or cur is None:
            print(Fore.RED + "\n❌ Gagal terhubung ke database.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return None

        # Tampilkan daftar alat tersedia
        df = pd.DataFrame(rows, columns=['ID', 'Nama Alat', 'Harga', 'Deskripsi', 'Diskon', 'Kondisi', 'Status Alat'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()

        # Input dari user
        idalat = int(input(Fore.CYAN + "Masukkan ID alat yang ingin disewa: " + Fore.WHITE))
        lama_hari = int(input(Fore.CYAN + "Lama peminjaman (hari): " + Fore.WHITE))

        # Hitung tanggal
        today = date.today()
        tenggat = today + timedelta(days=lama_hari)

        # Ambil harga & diskon dari database
        cur.execute("SELECT hargaalat, diskonalat FROM AlatPertanian WHERE idalat = %s", (idalat,))
        alat = cur.fetchone()
        
        if not alat:
            raise ValueError(f"❌ ID alat {idalat} tidak ditemukan")

        harga_alat, diskon_alat = alat
        harga_setelah_diskon = harga_alat - (diskon_alat or 0)
        dp = int(0.2 * harga_setelah_diskon)  # DP 20%

        # ✅ INSERT ke Peminjaman - SESUAI STRUKTUR TABEL
        insert_peminjaman = """
            INSERT INTO Peminjaman (
                idpeminjam,
                tanggalpeminjaman,
                tenggatpeminjaman,
                dp,
                deskripsi,
                idstatuspeminjaman
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING idpeminjaman;
        """
        deskripsi = f"Peminjaman alat ID {idalat}"
        idstatus = 1  # Status: Pending

        cur.execute(insert_peminjaman, (id_peminjam, today, tenggat, dp, deskripsi, idstatus))
        id_peminjaman_baru = cur.fetchone()[0]
        print(Fore.GREEN + f"\n✅ Peminjaman dibuat dengan ID: {id_peminjaman_baru}")

        insert_detail = """
            INSERT INTO DetailPeminjaman (idpeminjaman, idalat, harga, diskon)
            VALUES (%s, %s, %s, %s);
        """
        cur.execute(insert_detail, (id_peminjaman_baru, idalat, harga_alat, diskon_alat))
        print(Fore.GREEN + "✅ Detail peminjaman ditambahkan")

        conn.commit()
        print(Fore.GREEN + "\n✅✅✅ Peminjaman berhasil diajukan!")
        print(Fore.YELLOW + f"Status: Menunggu Persetujuan Owner")
        print(Fore.YELLOW + f"DP yang harus dibayar: RP {dp:,}")
        input(Fore.WHITE + "\nTekan Enter untuk kembali...")
        return id_peminjaman_baru

    except ValueError as e:
        # Error validasi (alat tidak ditemukan, dll)
        print(Fore.RED + f"\n❌ Error Validasi: {e}")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None
    
    except Exception as e:
        # Error lainnya (database, dll)
        conn.rollback()  # ✅ ROLLBACK jika error
        print(Fore.RED + f"\n❌ Terjadi kesalahan: {type(e).__name__}")
        print(Fore.RED + f"📝 Pesan: {e}")
        print(Fore.RED + "\n🐛 Detail error untuk debugging:")
        traceback.print_exc()
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None
        


# menu owner
def menu_owner():
    global owner_id_skrg
    while True:
        header()
        print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + "                    MENU OWNER                          " + Fore.YELLOW + "║")
        print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        pilihan = q.select(
                    "Pilih menu:",
                    choices=[
                        "🚜  Kelola Alat Pertanian",
                        "📊  Lihat Peminjaman Aktif",
                        "📋  Konfirmasi Persetujuan Peminjaman",
                        "✅  Konfirmasi Pengembalian",
                        "📜  Riwayat Peminjaman",
                        "❌  Logout"
                    ]
                ).ask()

        print(Fore.CYAN + "─" * 60)
        
        if pilihan == "🚜  Kelola Alat Pertanian":
            kelola_alat_pertanian()

        elif pilihan == "📊  Lihat Peminjaman Aktif":
            lihat_peminjaman_aktif()

        elif pilihan == "📋  Konfirmasi Persetujuan Peminjaman":
            konfirmasi_persetujuan_peminjaman()

        elif pilihan == "✅  Konfirmasi Pengembalian":
            konfirmasi_pengembalian()
        
        elif pilihan == "📜  Riwayat Peminjaman":
            lihat_riwayat_peminjaman_owner()
            
        elif pilihan == "❌  Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")


def kelola_alat_pertanian():
    global owner_id_skrg
    while True:
        header()
        print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "               KELOLA ALAT PERTANIAN OWNER              " + Fore.GREEN + "║")
        print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()


        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "➕ Tambah alat pertanian",
                "📊 Ubah status alat",
                "🔧 Ubah kondisi alat",
                "💸 Ubah diskon alat",
                "📋 Lihat daftar alat",
                "❌ Keluar"
            ]
        ).ask()

        print(Fore.CYAN + "─" * 60)

        conn, cur = connectDB()
        if conn is None or cur is None:
            print(Fore.RED + "\n❌ Gagal terhubung ke database.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            continue

        try:
            # 1. TAMBAH ALAT
            if pilihan == "➕ Tambah alat pertanian":
                try:
                    nama = q.text("Nama alat (ESC untuk batal): ").ask()
                    if nama is None:  # ESC ditekan
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    
                    harga_str = q.text("Harga alat (ESC untuk batal): ").ask()
                    if harga_str is None:  # ESC ditekan
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    harga = int(harga_str)
                    
                    desk = q.text("Deskripsi (ESC untuk batal): ").ask()
                    if desk is None:  # ESC ditekan
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    
                    diskon_str = q.text("Diskon (ESC untuk batal): ").ask()
                    if diskon_str is None:  # ESC ditekan
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    diskon = int(diskon_str)
                    
                    kondisi_str = q.text("ID Kondisi 1=Sangat baik, 2=Cukup (ESC untuk batal): ").ask()
                    if kondisi_str is None:  # ESC ditekan
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    kondisi = int(kondisi_str)

                    cur.execute("""
                        INSERT INTO AlatPertanian
                        (namaalat, hargaalat, deskripsialat, diskonalat, idowner, idstatusalat, idkondisialat)
                        VALUES (%s, %s, %s, %s, %s, 1, %s)
                    """, (nama, harga, desk, diskon, owner_id_skrg, kondisi))
                    conn.commit()

                    print(Fore.GREEN + "\n✔ Alat berhasil ditambahkan!")
                    input("Tekan Enter untuk lanjut...")
                except ValueError:
                    print(Fore.RED + "❌ Input tidak valid (harus angka untuk harga/diskon/kondisi)!")
                    input("Tekan Enter untuk lanjut...")

            # 2. UBAH STATUS ALAT
            elif pilihan == "📊 Ubah status alat":

                print(Fore.WHITE + "\nDaftar alat Anda:\n")
                cur.execute("""
                    SELECT a.idalat, a.namaalat, a.hargaalat, s.status AS status_alat, k.kondisi AS kondisi_alat
                    FROM AlatPertanian a
                    JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
                    JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
                    WHERE a.idowner = %s
                    ORDER BY a.idalat
                    """, (owner_id_skrg,))
                rows = cur.fetchall()


                if not rows:
                    print(Fore.YELLOW + "⚠ Tidak ada alat terdaftar.")
                    input("Enter...")
                    continue
                
                df = pd.DataFrame(rows, columns=["ID", "Nama Alat", "Harga", "Status", "Kondisi"])
                print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))


                print("\nPilih alat yang mau diubah statusnya.")
                idalat = input("Masukkan ID alat: ")


                print("\nStatus Baru:")
                print("1 = Tersedia")
                print("2 = Dipesan")
                print("3 = Dipinjam")
                print("4 = Tidak Aktif")


                status_baru = int(input("Pilih status baru: "))


                cur.execute("""
                    UPDATE AlatPertanian
                    SET idstatusalat = %s
                    WHERE idalat = %s AND idowner = %s
                """, (status_baru, idalat, owner_id_skrg))
                conn.commit()


                print(Fore.GREEN + "\n✔ Status alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")


            # 3. UBAH KONDISI ALAT
            elif pilihan == "🔧 Ubah kondisi alat":


                print(Fore.WHITE + "\nDaftar alat Anda:\n")
                cur.execute("""
                    SELECT a.idalat, a.namaalat, a.hargaalat, s.status AS status_alat, k.kondisi AS kondisi_alat
                    FROM AlatPertanian a
                    JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
                    JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
                    WHERE a.idowner = %s
                    ORDER BY a.idalat
                    """, (owner_id_skrg,))
                rows = cur.fetchall()


                if not rows:
                    print(Fore.YELLOW + "⚠ Tidak ada alat terdaftar.")
                    input("Enter...")
                    continue
                
                df = pd.DataFrame(rows, columns=["ID", "Nama Alat", "Harga", "Status", "Kondisi"])
                print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))


                print("\nPilih alat yang mau diubah kondisinya.")
                idalat = input("Masukkan ID alat: ")


                print("\nKondisi Baru:")
                print("1 = Baik")
                print("2 = Rusak")


                kondisi_baru = int(input("Pilih kondisi baru: "))


                cur.execute("""
                    UPDATE AlatPertanian
                    SET idkondisialat = %s
                    WHERE idalat = %s AND idowner = %s
                """, (kondisi_baru, idalat, owner_id_skrg))
                conn.commit()


                print(Fore.GREEN + "\n✔ Kondisi alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")


            elif pilihan == "💸 Ubah diskon alat":


                # 1) Tampilkan daftar alat milik owner yang akan diubah diskonnya
                print(Fore.WHITE + "\nDaftar alat Anda:\n")
                cur.execute("""
                SELECT 
                    a.idalat,
                    a.namaalat,
                    'RP ' || a.hargaalat::TEXT as harga,
                    a.diskonalat,
                    o.username as owner,
                    s.status,
                    k.kondisi
                FROM AlatPertanian a
                JOIN Owners o ON a.idowner = o.idowners
                JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
                JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
                WHERE a.idowner = %s
                ORDER BY a.idalat;
                """, (owner_id_skrg,))
                rows = cur.fetchall()

                if not rows:
                    print(Fore.YELLOW + "⚠ Tidak ada alat terdaftar.")
                    input("Tekan Enter...")
                    continue

                df = pd.DataFrame(rows, columns=["ID", "Nama Alat", "Harga", "Diskon", "Username", "Status", "Kondisi"])
                print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))


                print("\nPilih alat yang mau diubah diskonnya.")
                idalat = input("Masukkan ID alat: ")


                # input diskon baru
                diskon_baru = int(input("Masukkan diskon baru (angka rupiah): "))


                # update ke database
                cur.execute("""
                    UPDATE AlatPertanian
                    SET diskonalat = %s
                    WHERE idalat = %s AND idowner = %s
                """, (diskon_baru, idalat, owner_id_skrg))
                conn.commit()


                print(Fore.GREEN + "\n✔ Diskon alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")


            # 4. LIHAT SEMUA ALAT
            elif pilihan == "📋 Lihat daftar alat":
                print(Fore.WHITE + "\nDaftar alat milik Anda:\n")


                cur.execute("""
                    SELECT idalat, namaalat, hargaalat, idstatusalat, idkondisialat
                    FROM AlatPertanian
                    WHERE idowner = %s
                """, (owner_id_skrg,))
                rows = cur.fetchall()

                if rows:
                    df = pd.DataFrame(rows, columns=["ID", "Nama Alat", "Harga", "Status ID", "Kondisi ID"])
                    print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
                else:
                    print(Fore.YELLOW + "⚠ Tidak ada alat terdaftar.")

                input("\nTekan Enter untuk kembali...")


            # 5. KELUAR
            elif pilihan == "❌ Keluar":
                break

            if conn:
                cur.close()
                conn.close()
    
        except ValueError:
            print(Fore.RED + "❌ Input tidak valid!")
            input("Tekan Enter untuk coba lagi...")
        except psycopg2.Error as e:
            print(Fore.RED + f"❌ Error database: {e}")
            input("Tekan Enter untuk coba lagi...")
        finally:
            if conn:
                cur.close()
                conn.close()

# def lihat_peminjaman_aktif():
def lihat_peminjaman_aktif():
    header()


    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + " PEMINJAMAN AKTIF ALATKU " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()


    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            return


        query = """
        SELECT p.idpeminjaman, pm.username, a.namaalat, p.tanggalpeminjaman, 
               p.tenggatpeminjaman, sp.statuspeminjaman
        FROM Peminjaman p
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        WHERE a.idowner = %s AND sp.statuspeminjaman IN ('Pending', 'Disetujui')
        """
        
        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()


        if rows:
            df = pd.DataFrame(rows, columns=['ID', 'Peminjam', 'Alat', 'Tgl Pinjam', 'Tenggat', 'Status'])
            print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        else:
            print(Fore.YELLOW + "⚠️ Tidak ada peminjaman aktif.")


        input(Fore.WHITE + "\nTekan Enter untuk kembali...")


    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input()
    finally:
        if conn:
            cur.close()
            conn.close()


def konfirmasi_persetujuan_peminjaman():
    header()
    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + " KONFIRMASI PERSETUJUAN ALAT " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return

        query = """
        SELECT 
            p.idpeminjaman,
            pm.username as peminjam,
            COUNT(dp.idalat) as jumlah_alat,
            'RP ' || SUM(dp.harga)::TEXT as total_harga,
            'RP ' || p.dp::TEXT as dp,
            p.tenggatpeminjaman
        FROM Peminjaman p
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        WHERE p.idstatuspeminjaman = 1 AND a.idowner = %s
        GROUP BY p.idpeminjaman, pm.username, p.dp, p.tenggatpeminjaman
        ORDER BY p.idpeminjaman;
        """
        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada peminjaman baru untuk dikonfirmasi.")
            input()
            return
        
        # Kumpulkan ID valid
        valid_ids = {r[0] for r in rows}

        # Loop sampai input valid
        while True:
            # Tampilkan tabel setiap kali loop (biar fresh)
            header()
            print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
            print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + " KONFIRMASI PERSETUJUAN ALAT " + Fore.YELLOW + "║")
            print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
            print()
            
            df = pd.DataFrame(rows, columns=['ID Pinjam', 'Peminjam', 'Jumlah Alat', 'Total Harga', 'DP', 'Tenggat'])
            print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
            print()

            id_input = input(Fore.CYAN + "Masukkan ID peminjaman yang ingin dikonfirmasi: " + Fore.WHITE)

            if not id_input.isdigit():
                print(Fore.RED + "❌ ID harus berupa angka!")
                input(Fore.YELLOW + "Tekan Enter untuk coba lagi...")
                continue

            idpeminjaman = int(id_input)

            if idpeminjaman not in valid_ids:
                print(Fore.RED + "❌ ID tidak ada di daftar di atas!")
                input(Fore.YELLOW + "Tekan Enter untuk coba lagi...")
                continue

            # Kalau lolos semua, break
            break
        
        # Konfirmasi persetujuan
        cur.execute(
            "UPDATE Peminjaman SET idstatuspeminjaman = 2 WHERE idpeminjaman = %s",
            (idpeminjaman,)
        )
        
        # Update status alat menjadi 'Tidak Tersedia' atau 'Dipinjam'
        cur.execute(
            """
            SELECT DISTINCT dp.idalat FROM DetailPeminjaman dp
            WHERE dp.idpeminjaman = %s
            """,
            (idpeminjaman,)
        )
        alat_list = cur.fetchall()
        
        # Cari atau buat status 'Tidak Tersedia' untuk alat yang dipinjam
        cur.execute("SELECT idstatusalat FROM StatusAlat WHERE status = 'Tidak Tersedia'")
        status_row = cur.fetchone()
        
        if status_row:
            id_status_tidak_tersedia = status_row[0]
        else:
            cur.execute("INSERT INTO StatusAlat (status) VALUES ('Tidak Tersedia') RETURNING idstatusalat")
            id_status_tidak_tersedia = cur.fetchone()[0]
        
        # Update status setiap alat
        for alat in alat_list:
            idalat = alat[0]
            cur.execute(
                "UPDATE AlatPertanian SET idstatusalat = %s WHERE idalat = %s",
                (id_status_tidak_tersedia, idalat)
            )
        
        conn.commit()
        
        header()
        print(Fore.GREEN + "✅ Peminjaman telah dikonfirmasi!")
        print(Fore.GREEN + "✅ Status alat diubah menjadi 'Tidak Tersedia'")
        input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")

    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input()
    finally:
        if conn:
            cur.close()
            conn.close()

def lihat_riwayat_peminjaman_owner():
    global owner_id_skrg
    header()
    print(Fore.MAGENTA + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.MAGENTA + Style.BRIGHT + "║" + Fore.WHITE + "        RIWAYAT PEMINJAMAN ALAT SAYA (OWNER)             " + Fore.MAGENTA + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return

        # Query riwayat peminjaman untuk alat milik owner ini
        query = """
        SELECT 
            p.idpeminjaman,
            pm.username as Peminjam,
            a.namaalat as Nama_Alat,
            'RP ' || dp.harga::TEXT as Harga,
            p.tanggalpeminjaman as Tgl_Pinjam,
            p.tenggatpeminjaman as Tgl_Tenggat,
            sp.statuspeminjaman as Status_Peminjaman,
            COALESCE(pr.tanggalpengembalian::TEXT, '-') as Tgl_Kembali
        FROM Peminjaman p
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        LEFT JOIN Pengembalian pr ON p.idpeminjaman = pr.idpeminjaman
        WHERE a.idowner = %s
        ORDER BY p.idpeminjaman DESC
        """
        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada riwayat peminjaman untuk alat Anda.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
        
        df = pd.DataFrame(rows, columns=['ID Peminjaman', 'Peminjam', 'Nama Alat', 'Harga', 'Tgl Pinjam', 'Tgl Tenggat', 'Status', 'Tgl Kembali'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()
        
        # Statistik
        total_peminjaman = len(rows)
        selesai = sum(1 for row in rows if row[6] == 'Dikembalikan')
        pending = sum(1 for row in rows if row[6] == 'Pending')
        disetujui = sum(1 for row in rows if row[6] == 'Disetujui')
        ditolak = sum(1 for row in rows if row[6] == 'Ditolak')
        
        print(Fore.YELLOW + f"\n📊 Statistik:")
        print(Fore.WHITE + f"   Total Peminjaman: {total_peminjaman}")
        print(Fore.GREEN + f"   ✅ Selesai (Dikembalikan): {selesai}")
        print(Fore.YELLOW + f"   ⏳ Disetujui: {disetujui}")
        print(Fore.CYAN + f"   ⏰ Pending: {pending}")
        print(Fore.RED + f"   ❌ Ditolak: {ditolak}")
        
        input(Fore.WHITE + "\nTekan Enter untuk kembali...")

    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        traceback.print_exc()
        input()
    finally:
        if conn:
            cur.close()
            conn.close()

def konfirmasi_pengembalian():
    header()
    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + " KONFIRMASI PENGEMBALIAN ALAT " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()


    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return

        # Tampilkan pengembalian pending
        query = """
        SELECT pen.idpengembalian, pm.username, a.namaalat, pen.tanggalpengembalian, 
               pen.idpeminjaman, d.biayadenda
        FROM Pengembalian pen
        JOIN Peminjaman p ON pen.idpeminjaman = p.idpeminjaman
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        LEFT JOIN Denda d ON pen.iddenda = d.iddenda
        WHERE a.idowner = %s AND pen.idstatuspengembalian = 1
        """

        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada pengembalian baru untuk dikonfirmasi.")
            input()
            return

        df = pd.DataFrame(rows, columns=['ID Return', 'Peminjam', 'Alat', 'Tgl Return', 'ID Pinjam', 'Denda'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()

        idpengembalian = int(input(Fore.CYAN + "Masukkan ID pengembalian yang ingin dikonfirmasi: " + Fore.WHITE))
        
        # Konfirmasi pengembalian
        cur.execute("UPDATE Pengembalian SET idstatuspengembalian = 2 WHERE idpengembalian = %s", (idpengembalian,))
        conn.commit()

        print()
        print(Fore.GREEN + "✅ Pengembalian telah dikonfirmasi!")
        input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")

    except ValueError:
        print(Fore.RED + "❌ Input tidak valid!")
        input()
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input()
    finally:
        if conn:
            cur.close()
            conn.close()


# Jalanin Main program
if __name__ == "__main__":
    try:
        menu_utama()
    except KeyboardInterrupt:
        bersih_terminal()
        print(Fore.RED + "\n\n❌ Program dihentikan oleh user.\n")
    except Exception:
        print(Fore.RED + f"\n❌ Error: {Exception}\n")