import psycopg2
import pandas as pd
import tabulate as tb
import pyfiglet as pf
from colorama import init, Fore, Style
import questionary as q
from datetime import date, datetime, timedelta

# koneksi antar python dengan database
def connectDB():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "NOIDAJA",
            dbname = "Databaseminjam",
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
                global peminjam_id
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
                global owner_id_skrg
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
                    continue

                if not no_hp.startswith("08"):
                    print(Fore.RED + "❌ No. HP harus diawali '08' (contoh: 08xxxxxxxxxx)!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang No. HP...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi ulang data (No. HP salah).")
                    print(Fore.WHITE + f"Username : {username}")
                    continue

                if not (10 <= len(no_hp) <= 13):
                    print(Fore.RED + "❌ No. HP harus 10–13 digit!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang No. HP...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi ulang data (No. HP salah).")
                    print(Fore.WHITE + f"Username : {username}")
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
                    input(Fore.WHITE + "Tekan Enter untuk ulang Tanggal Lahir...")
                    bersih_terminal()
                    header()
                    print(Fore.YELLOW + "Silakan isi data lagi (Tanggal Lahir salah).")
                    print()
                    print(Fore.WHITE + f"Username : {username}")
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
                "🔍  Lihat dan Ajukan Alat Tersedia",
                "📋  Riwayat Peminjaman Saya",
                "↩   Kembalikan Alat",
                "❌  Logout"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
        
        if pilihan == "🔍  Lihat dan Ajukan Alat Tersedia":
            lihat_alat_tersedia()

        elif pilihan == "❌  Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")

# lihat alat tersedia
def lihat_alat_tersedia():
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  ALAT YANG TERSEDIA                    " + Fore.GREEN + "║")
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
            
        else:
            print(Fore.YELLOW + "\n⚠ Tidak ada alat pertanian yang tersedia saat ini.")

        input(Fore.WHITE + "\nTekan Enter untuk kembali...")
        menu_peminjam()
        bersih_terminal()

    except Exception as e:
        print(Fore.RED + f"\n❌ Terjadi kesalahan saat mengambil data: {e}")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ajukan persetujuan peminjaman
def proses_ajukan_peminjaman(cur, id_peminjam, rows):
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  AJUKAN PERSETUJUAN PEMINJAMAN                    " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    # pilih alat
    df = pd.DataFrame(rows, columns=['ID', 'Nama Alat', 'Harga', 'Deskripsi', 'Diskon', 'Kondisi', 'Status Alat'])
    print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

    print()
    idalat = int(input(Fore.CYAN + "Masukkan ID alat yang ingin disewa: " + Fore.WHITE))

    # input lama peminjaman
    lama_hari = int(input(Fore.CYAN + "Lama peminjaman (hari): " + Fore.WHITE))
    today = date.today()
    tenggat = today + timedelta(days=lama_hari)

    # ambil harga & diskon
    cur.execute("SELECT hargaalat, diskonalat FROM AlatPertanian WHERE idalat = %s", (idalat,))
    alat = cur.fetchone()
    if not alat:
        raise ValueError("ID alat tidak ditemukan")

    harga_alat, diskon_alat = alat
    harga_setelah_diskon = harga_alat - (diskon_alat or 0)
    dp = int(0.2 * harga_setelah_diskon) 

    # insert ke Peminjaman
    insert_peminjaman = """
        INSERT INTO Peminjaman (tanggalpeminjaman, tenggatpeminjaman, dp, deskripsi, idstatuspeminjaman)
        VALUES ( %s, %s, %s, %s, %s)
        RETURNING idpeminjaman;
    """
    deskripsi = f"Peminjaman alat ID {idalat}"
    idstatus = 1  # Pending (sesuaikan dengan DB-mu)

    cur.execute(insert_peminjaman, (id_peminjam, today, tenggat, dp, deskripsi, idstatus))
    id_peminjaman_baru = cur.fetchone()[0]

    # insert ke DetailPeminjaman
    insert_detail = """
        INSERT INTO DetailPeminjaman (idpeminjaman, idalat, harga, diskon)
        VALUES (%s, %s, %s, %s);
    """
    cur.execute(insert_detail, (id_peminjaman_baru, idalat, harga_alat, diskon_alat))

    # update status alat → Diajukan
    cur.execute("SELECT idstatusalat FROM StatusAlat WHERE status = 'Diajukan'")
    row_status = cur.fetchone()
    if row_status:
        id_status_diajukan = row_status[0]
        cur.execute(
            "UPDATE AlatPertanian SET idstatusalat = %s WHERE idalat = %s",
            (id_status_diajukan, idalat)
        )

    return id_peminjaman_baru

# menu owner
def menu_owner():
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
                        "❌  Logout"
                    ]
                ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
        
        pilihan = input(Fore.WHITE + "Pilih menu: " + Fore.YELLOW)
        if pilihan == "🚜  Kelola Alat Pertanian":
            kelola_alat_pertanian()

        elif pilihan == "📊  Lihat Peminjaman Aktif":
            lihat_peminjaman_aktif()

        #elif pilihan == "📋  Konfirmasi Persetujuan Peminjaman":
        #    konfirmasi_persetujuan_peminjaman()

        elif pilihan == "✅  Konfirmasi Pengembalian":
            konfirmasi_pengembalian()
            
        elif pilihan == "❌  Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")

def kelola_alat_pertanian():
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

        # 1. TAMBAH ALAT
        if pilihan == "➕ Tambah alat pertanian":
            nama = input("Nama alat: ")
            harga = int(input("Harga alat: "))
            desk = input("Deskripsi: ")
            diskon = int(input("Diskon: "))
            kondisi = int(input("ID Kondisi (1=Sangat baik, 2=Cukup): "))

            cur.execute("""
                INSERT INTO AlatPertanian
                (namaalat, hargaalat, deskripsialat, diskonalat, idowner, idstatusalat, idkondisialat)
                VALUES (%s, %s, %s, %s, %s, 1, %s)
            """, (nama, harga, desk, diskon, owner_id_skrg, kondisi))
            conn.commit()

            print(Fore.GREEN + "\n✔ Alat berhasil ditambahkan!")
            input("Tekan Enter untuk lanjut...")

        # 2. UBAH STATUS ALAT
        elif pilihan == "📊 Ubah status alat":

            print(Fore.WHITE + "\nDaftar alat Anda:\n")
            cur.execute("""
                SELECT idalat, namaalat, hargaalat, status, kondisi
                FROM AlatPertanian join StatusAlat using(idstatusalat)
                join KondisiAlat using(idkondisialat)
                WHERE idowner = %s
            """, (owner_id_skrg,))
            rows = cur.fetchall()

            for r in rows:
                print(f"ID {r[0]} | {r[1]} | Harga: {r[2]} | Status: {r[3]} | Kondisi: {r[4]}")

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
                SELECT idalat, namaalat, hargaalat, idstatusalat, idkondisialat
                FROM AlatPertanian join StatusAlat using(idstatusalat)
                join KondisiAlat using(idkondisialat)
                WHERE idowner = %s
            """, (owner_id_skrg,))
            rows = cur.fetchall()

            for r in rows:
                print(f"ID {r[0]} | {r[1]} | Harga: {r[2]} | Status: {r[3]} | Kondisi: {r[4]}")

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

            # 1) Tampilkan daftar alat milik owner
            print(Fore.WHITE + "\nDaftar alat Anda:\n")
            cur.execute("""
                SELECT idalat, namaalat, hargaalat, diskonalat
                FROM AlatPertanian
                WHERE idowner = %s
            """, (owner_id_skrg,))
            rows = cur.fetchall()

            for r in rows:
                print(f"ID {r[0]} | {r[1]} | Harga: {r[2]} | Diskon: {r[3]}")

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

            for r in rows:
                print(f"ID {r[0]} | {r[1]} | Harga: {r[2]} | Status: {r[3]} | Kondisi: {r[4]}")

            input("\nTekan Enter untuk kembali...")

        # 5. KELUAR
        elif pilihan == "❌ Keluar":
            break

# def lihat_peminjaman_aktif():
def lihat_peminjaman_aktif(idowners):
    header()
    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + " PEMINJAMAN AKTIF ALATKU " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
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
        
        cur.execute(query, (idowners,))
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

# def konfirmasi_persetujuan_peminjaman():

def konfirmasi_pengembalian(idowners):
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
        
        cur.execute(query, (idowners,))
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