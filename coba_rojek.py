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
            dbname = "basdadb",
            port = "5432"
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print("Koneksi gagal, coba lagi")
        return None, None

connectDB()

# fungsi untuk format nama (Title Case)
def proper_case(text):
    """Convert text ke format Title Case (Proper Case)"""
    if not text or text is None:
        return None
    return text.strip().title()

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
    print(Fore.YELLOW + Style.BRIGHT + "        SISTEM PEMINJAMAN & PENYEWAAN ALAT PERTANIAN")
    print(Fore.CYAN + "="*60)
    print()

# buat judul per fungsi biar gk ribet asli no fek
def buat_judul(warna, text):
    panjang_text = len(text)
    panjang_box = 56  # panjang total box adalah 60 karakter, minus 4 untuk border
    
    # Hitung spasi kiri dan kanan
    total_spasi = panjang_box - panjang_text
    spasi_kiri = total_spasi // 2
    spasi_kanan = total_spasi - spasi_kiri
    
    # Print box
    print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.WHITE + Style.BRIGHT + "║" + warna + " " * spasi_kiri + text + " " * spasi_kanan + Fore.WHITE + "║")
    print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

# menu utama
def menu_utama():
    while True:
        header()
        buat_judul(Fore.CYAN, "MENU UTAMA")
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "👤 Login sebagai Peminjam",
                "🏪 Login sebagai Owner/Pemilik",
                "📝 Registrasi Akun Peminjam",
                "❌ Keluar"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)

        if pilihan == "👤 Login sebagai Peminjam":
            login_peminjam()

        elif pilihan == "🏪 Login sebagai Owner/Pemilik":
            login_owner()

        elif pilihan == "📝 Registrasi Akun Peminjam":
            registrasi()

        elif pilihan == "❌ Keluar":
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
    buat_judul(Fore.GREEN, "LOGIN SEBAGAI PEMINJAM")
    while True:
        username = q.text("Username (ctrl+c untuk batal): ").ask()
        if username is None:
            print(Fore.YELLOW + "\n⬅️ Kembali ke menu utama\n")
            return
        password = q.password("Password (ctrl+c untuk batal): ").ask()
        if password is None:
            print(Fore.YELLOW + "\n⬅️ Kembali ke menu utama\n")
            return
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
                input(Fore.WHITE + "Tekan Enter untuk ulang...")
                header()
                buat_judul(Fore.GREEN, "LOGIN SEBAGAI PEMINJAM")
        except psycopg2.Error as e:
            print(Fore.RED + f"Error database: {e}")
            input(Fore.WHITE + "Tekan Enter untuk ulang...")
        except Exception as e:
            print(Fore.RED + f"Error tak terduga: {e}")
            input(Fore.WHITE + "Tekan Enter untuk ulang...")
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
    buat_judul(Fore.YELLOW, "LOGIN SEBAGAI OWNER/PEMILIK")
    while True:
        username = q.text("Username (ctrl+c untuk batal): ").ask()
        if username is None:
            print(Fore.YELLOW + "\n⬅️ Kembali ke menu utama\n")
            return
        password = q.password("Password (ctrl+c untuk batal): ").ask()
        if password is None:
            print(Fore.YELLOW + "\n⬅️ Kembali ke menu utama\n")
            return
        print()
        print(Fore.YELLOW + "⏳ Memproses login...")
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
                input(Fore.WHITE + "Tekan Enter untuk ulang...")
                header()
                buat_judul(Fore.YELLOW, "LOGIN SEBAGAI OWNER/PEMILIK")

        except psycopg2.Error as e:
            print(Fore.RED + f"Error database: {e}")
            input(Fore.WHITE + "Tekan Enter untuk ulang...")
        
        finally:
            if conn:
                cursor.close()
                conn.close()
    input(Fore.WHITE + "\nTekan Enter untuk melanjutkan...")
    menu_owner()

# registrasi akun peminjam
def registrasi():
    conn, cursor = None, None
    while True:
        bersih_terminal()
        header()
        buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
        try:
            # ========== INPUT USERNAME ==========
            username = q.text("Username baru (ctrl+c untuk batal): ").ask()
            validasi_username(username)
            
            # ========== INPUT PASSWORD ==========
            password = q.password("Password (ctrl+c untuk batal): ").ask()
            if password is None:
                print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                return
            
            # ========== INPUT NO HP (VALIDASI) ==========
            while True:
                no_hp = q.text("No. HP (08..., 10-13 digit, ctrl+c untuk batal): ").ask()
                if no_hp is None:
                    print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                    return
                
                if not no_hp.isdigit():
                    print(Fore.RED + "❌ No. HP harus angka semua!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}\n")
                    continue
                
                if not no_hp.startswith("08"):
                    print(Fore.RED + "❌ No. HP harus diawali '08'!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}\n")
                    continue
                
                if not (10 <= len(no_hp) <= 13):
                    print(Fore.RED + "❌ No. HP harus 10–13 digit!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}\n")
                    continue
                # cek apakah no_hp sudah terdaftar
                try:
                    conn_check, cur_check = connectDB()
                    if conn_check is None:
                        print(Fore.YELLOW + "⚠️ Tidak dapat memverifikasi No. HP saat ini (koneksi DB gagal).")
                    else:
                        cur_check.execute("SELECT username FROM Peminjam WHERE nohp = %s", (no_hp,))
                        row_dup = cur_check.fetchone()
                        cur_check.close()
                        conn_check.close()
                        if row_dup:
                            print(Fore.RED + f"❌ No. HP {no_hp} sudah terdaftar. Silakan gunakan nomor lain.")
                            input(Fore.WHITE + "Tekan Enter untuk ulang...")
                            bersih_terminal()
                            header()
                            buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                            print(Fore.YELLOW + "Data yang sudah diisi:")
                            print(Fore.WHITE + f"Username : {username}")
                            print(Fore.WHITE + f"Password : {'*' * len(password)}\n")
                            continue
                except Exception:
                    # jika pengecekan gagal, jangan blokir pendaftaran; lanjutkan dan periksa lagi nanti
                    try:
                        if cur_check:
                            cur_check.close()
                    except Exception:
                        pass
                    try:
                        if conn_check:
                            conn_check.close()
                    except Exception:
                        pass
                break
            
            # ========== INPUT NIK (VALIDASI) ==========
            while True:
                nik = q.text("NIK (16 digit, ctrl+c untuk batal): ").ask()
                if nik is None:
                    print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                    return
                
                if not nik.isdigit():
                    print(Fore.RED + "❌ NIK harus angka!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}\n")
                    continue
                
                if len(nik) != 16:
                    print(Fore.RED + "❌ NIK harus tepat 16 digit!")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}\n")
                    continue
                # cek apakah NIK sudah terdaftar
                try:
                    conn_check, cur_check = connectDB()
                    if conn_check is None:
                        print(Fore.YELLOW + "⚠️ Tidak dapat memverifikasi NIK saat ini (koneksi DB gagal).")
                    else:
                        cur_check.execute("SELECT username FROM Peminjam WHERE nik = %s", (nik,))
                        row_dup = cur_check.fetchone()
                        cur_check.close()
                        conn_check.close()
                        if row_dup:
                            print(Fore.RED + f"❌ NIK {nik} sudah terdaftar. Silakan gunakan NIK lain.")
                            input(Fore.WHITE + "Tekan Enter untuk ulang...")
                            bersih_terminal()
                            header()
                            buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                            print(Fore.YELLOW + "Data yang sudah diisi:")
                            print(Fore.WHITE + f"Username : {username}")
                            print(Fore.WHITE + f"Password : {'*' * len(password)}")
                            print(Fore.WHITE + f"No. HP   : {no_hp}\n")
                            continue
                except Exception:
                    try:
                        if cur_check:
                            cur_check.close()
                    except Exception:
                        pass
                    try:
                        if conn_check:
                            conn_check.close()
                    except Exception:
                        pass

                break
            
            # ========== INPUT TANGGAL LAHIR (VALIDASI) ==========
            while True:
                tanggal_lahir_str = q.text("Tanggal Lahir (YYYY-MM-DD, ctrl+c untuk batal): ").ask()
                if tanggal_lahir_str is None:
                    print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                    return
                
                try:
                    tanggal_lahir = datetime.strptime(tanggal_lahir_str, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print(Fore.RED + "❌ Format tanggal salah! Gunakan YYYY-MM-DD")
                    input(Fore.WHITE + "Tekan Enter untuk ulang...")
                    bersih_terminal()
                    header()
                    buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                    print(Fore.YELLOW + "Data yang sudah diisi:")
                    print(Fore.WHITE + f"Username : {username}")
                    print(Fore.WHITE + f"Password : {'*' * len(password)}")
                    print(Fore.WHITE + f"No. HP   : {no_hp}")
                    print(Fore.WHITE + f"NIK      : {nik}\n")
                    continue
            
            # ========== INPUT ALAMAT ==========
            jalan = q.text("Nama Jalan (ctrl+c untuk batal): ").ask()
            if jalan is None:
                print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                return
            
            # ========== SELECT KECAMATAN FROM DATABASE ==========
            conn_temp, cursor_temp = connectDB()
            if conn_temp is None:
                print(Fore.RED + "❌ Gagal terhubung ke database untuk memuat kecamatan")
                input()
                continue
            
            try:
                cursor_temp.execute("SELECT idkecamatan, kecamatan FROM Kecamatan ORDER BY kecamatan")
                kecamatan_rows = cursor_temp.fetchall()
            except Exception as e:
                print(Fore.RED + f"❌ Error saat memuat kecamatan: {e}")
                input()
                cursor_temp.close()
                conn_temp.close()
                continue
            
            kecamatan_dict = {k[1]: k[0] for k in kecamatan_rows}
            kecamatan_list = [k[1] for k in kecamatan_rows]
            kecamatan_list.append("➕ Tambah Kecamatan Baru")
            
            pilihan_kecamatan = q.select(
                "Pilih Kecamatan (atau tambah baru):",
                choices=kecamatan_list
            ).ask()
            
            if pilihan_kecamatan == "➕ Tambah Kecamatan Baru":
                while True:
                    nama_kecamatan = q.text("Masukkan nama Kecamatan baru (ctrl+c untuk batal): ").ask()
                    if nama_kecamatan is None:
                        print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                        cursor_temp.close()
                        conn_temp.close()
                        return
                    
                    # Validasi: tidak boleh kosong
                    if not nama_kecamatan.strip():
                        print(Fore.RED + "❌ Nama Kecamatan tidak boleh kosong!")
                        input(Fore.WHITE + "Tekan Enter untuk ulang...")
                        bersih_terminal()
                        header()
                        buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                        continue
                    
                    # Format dengan proper_case
                    nama_kecamatan = proper_case(nama_kecamatan)
                    
                    # Cek apakah kecamatan sudah ada (case-insensitive)
                    if nama_kecamatan.lower() in [k.lower() for k in kecamatan_list if k != "➕ Tambah Kecamatan Baru"]:
                        print(Fore.RED + f"❌ Kecamatan '{nama_kecamatan}' sudah ada di sistem!")
                        input(Fore.WHITE + "Tekan Enter untuk ulang...")
                        bersih_terminal()
                        header()
                        buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                        continue
                    break
            else:
                nama_kecamatan = pilihan_kecamatan
            
            # ========== SELECT DESA FROM DATABASE (BERDASARKAN KECAMATAN) ==========
            try:
                # Query langsung ke database untuk mencari ID kecamatan berdasarkan nama
                cursor_temp.execute(
                    "SELECT idkecamatan FROM Kecamatan WHERE kecamatan = %s",
                    (nama_kecamatan,)
                )
                row_kec = cursor_temp.fetchone()
                
                if row_kec:
                    idkecamatan = row_kec[0]
                    # Query desa dari kecamatan yang ditemukan
                    cursor_temp.execute(
                        "SELECT iddesa, namadesa FROM Desa WHERE idkecamatan = %s ORDER BY namadesa",
                        (idkecamatan,)
                    )
                    desa_rows = cursor_temp.fetchall()
                    print(Fore.GREEN + f"✅ Ditemukan {len(desa_rows)} desa di Kecamatan {nama_kecamatan}")
                else:
                    # Kecamatan baru
                    idkecamatan = None
                    desa_rows = []
                    print(Fore.YELLOW + f"ℹ️ Kecamatan '{nama_kecamatan}' adalah baru, belum ada desa yang terdaftar.")
            except Exception as e:
                print(Fore.RED + f"❌ Error saat memuat desa: {e}")
                traceback.print_exc()
                input()
                cursor_temp.close()
                conn_temp.close()
                continue
            
            desa_list = [d[1] for d in desa_rows]
            desa_list.append("➕ Tambah Desa Baru")
            
            print(Fore.YELLOW + "Silakan pilih desa atau tambah baru.\n")
            
            pilihan_desa = q.select(
                "Pilih Desa (atau tambah baru):",
                choices=desa_list
            ).ask()
            
            if pilihan_desa == "➕ Tambah Desa Baru":
                while True:
                    nama_desa = q.text("Masukkan nama Desa baru (ctrl+c untuk batal): ").ask()
                    if nama_desa is None:
                        print(Fore.YELLOW + "\n⬅️ Registrasi dibatalkan - Kembali ke menu utama\n")
                        cursor_temp.close()
                        conn_temp.close()
                        return
                    
                    # Validasi: tidak boleh kosong
                    if not nama_desa.strip():
                        print(Fore.RED + "❌ Nama Desa tidak boleh kosong!")
                        input(Fore.WHITE + "Tekan Enter untuk ulang...")
                        bersih_terminal()
                        header()
                        buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                        continue
                    
                    # Format dengan proper_case
                    nama_desa = proper_case(nama_desa)
                    
                    # Cek apakah desa sudah ada di kecamatan ini (case-insensitive)
                    # Filter desa_list untuk menghilangkan tombol "Tambah Desa Baru"
                    desa_list_filter = [d for d in desa_list if d != "➕ Tambah Desa Baru"]
                    desa_list_lower = [d.lower() for d in desa_list_filter]
                    
                    if nama_desa.lower() in desa_list_lower:
                        print(Fore.RED + f"❌ Desa '{nama_desa}' sudah ada di Kecamatan {nama_kecamatan}!")
                        input(Fore.WHITE + "Tekan Enter untuk ulang...")
                        bersih_terminal()
                        header()
                        buat_judul(Fore.BLUE, "REGISTRASI AKUN PEMINJAM")
                        continue
                    break
            else:
                nama_desa = pilihan_desa
            
            cursor_temp.close()
            conn_temp.close()
            
            # ========== VERIFIKASI DATA ==========
            bersih_terminal()
            header()
            print(Fore.GREEN + Style.BRIGHT + "⚙️ VERIFIKASI DATA REGISTRASI")
            print(Fore.CYAN + "-" * 60)
            print(Fore.WHITE + f"Username      : {username}")
            print(Fore.WHITE + f"Password      : {'*' * len(password)}")
            print(Fore.WHITE + f"No. HP        : {no_hp}")
            print(Fore.WHITE + f"NIK           : {nik}")
            print(Fore.WHITE + f"Tanggal Lahir : {tanggal_lahir}")
            print(Fore.WHITE + f"Jalan         : {jalan}")
            print(Fore.WHITE + f"Desa          : {nama_desa}")
            print(Fore.WHITE + f"Kecamatan     : {nama_kecamatan}")
            print(Fore.CYAN + "-" * 60)
            
            konfirmasi = input(Fore.YELLOW + "Apakah data sudah benar? (y/n): " + Fore.WHITE).lower()
            
            if konfirmasi != "y":
                print(Fore.YELLOW + "🔁 Data dibatalkan, silakan input ulang.")
                input(Fore.WHITE + "Tekan Enter untuk mulai dari awal...")
                continue
            
            print(Fore.YELLOW + "⏳ Memproses registrasi...")
            
            # ========== SIMPAN KE DATABASE ==========
            conn, cursor = connectDB()
            if conn is None:
                print(Fore.RED + "❌ Gagal terhubung ke database")
                input()
                break
            
            # ====== CEK KEUNIKAN NIK DAN NOMOR HP ======
            try:
                cursor.execute("SELECT username, nohp, nik FROM Peminjam WHERE nohp = %s OR nik = %s", (no_hp, nik))
                exists_row = cursor.fetchone()
                if exists_row:
                    existing_username, existing_nohp, existing_nik = exists_row
                    msgs = []
                    if existing_nohp == no_hp:
                        msgs.append(f"No. HP {no_hp} sudah terdaftar (user: {existing_username}).")
                    if existing_nik == nik:
                        msgs.append(f"NIK {nik} sudah terdaftar (user: {existing_username}).")
                    print(Fore.RED + "❌ Gagal registrasi: " + " ".join(msgs))
                    input(Fore.WHITE + "Tekan Enter untuk ulang dan gunakan data lain...")
                    # Tutup koneksi dan ulangi loop registrasi
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
                    continue
            except Exception as e:
                # Jika query pengecekan gagal, rollback dan laporkan, lalu lanjutkan error handling
                if conn:
                    conn.rollback()
                print(Fore.RED + f"❌ Error saat memeriksa NIK/No HP: {e}")
                traceback.print_exc()
                input(Fore.WHITE + "Tekan Enter untuk coba lagi...")
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                continue
            
            # 1. Kecamatan
            cursor.execute(
                "SELECT idkecamatan FROM Kecamatan WHERE kecamatan = %s",
                (nama_kecamatan,)
            )
            row_kec = cursor.fetchone()
            
            if row_kec:
                idkecamatan = row_kec[0]
            else:
                cursor.execute(
                    "INSERT INTO Kecamatan (kecamatan) VALUES (%s) RETURNING idkecamatan",
                    (nama_kecamatan,)
                )
                idkecamatan = cursor.fetchone()[0]
            
            # 2. Desa (dengan idkecamatan)
            cursor.execute(
                "SELECT iddesa FROM Desa WHERE namadesa = %s AND idkecamatan = %s",
                (nama_desa, idkecamatan)
            )
            row_desa = cursor.fetchone()
            
            if row_desa:
                iddesa = row_desa[0]
            else:
                cursor.execute(
                    "INSERT INTO Desa (namadesa, idkecamatan) VALUES (%s, %s) RETURNING iddesa",
                    (nama_desa, idkecamatan)
                )
                iddesa = cursor.fetchone()[0]
            
            # 3. Alamat (dengan iddesa)
            cursor.execute(
                "INSERT INTO Alamat (jalan, iddesa) VALUES (%s, %s) RETURNING idalamat",
                (jalan, iddesa)
            )
            idalamat = cursor.fetchone()[0]
            
            # 4. Peminjam
            cursor.execute(
                """INSERT INTO Peminjam
                   (username, password, nohp, nik, tanggallahir, idalamat)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (username, password, no_hp, nik, tanggal_lahir, idalamat)
            )
            
            # SELESAI
            conn.commit()
            bersih_terminal()
            header()
            print(Fore.GREEN + "✅ Registrasi berhasil!")
            print(Fore.CYAN + "Silakan login dengan akun Anda.")
            input(Fore.WHITE + "\nTekan Enter untuk kembali...")
            break
        
        except psycopg2.Error as p:
            if conn:
                conn.rollback()
            bersih_terminal()
            header()
            print(Fore.RED + f"❌ Gagal registrasi: {p}")
            input(Fore.WHITE + "Tekan Enter untuk coba lagi...")
        
        except Exception as e:
            bersih_terminal()
            header()
            print(Fore.RED + f"❌ Error: {e}")
            traceback.print_exc()
            input(Fore.WHITE + "Tekan Enter untuk coba lagi...")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def validasi_username(username):
    conn, cur = connectDB()
    if conn is None:
        return username
    simbol =['!','@','#','$','%','^','&','*','(',')',',','_','-','=','[',']','~','+','{','}','<','>','?','/']
    while True:
        try:
            if any(s in username for s in simbol):
                print('Username Tidak Sesuai Harus Terdiri Dari Huruf')
                username = input('Masukkan Username: ')
                continue
            if username.isdigit():
                print("username tidak boleh pakai angka semua")
                username = input('Masukkan Username: ')
                continue
            if len(username) < 3:
                print("Username minimal 3 karakter")
                username = input("Masukkan Username: ")
                continue
            if not username.strip():
                print("Username tidak boleh kosong atau spasi saja!")
                username = input("Masukkan Username: ")
                continue
            query = "select * from Peminjam where username = %s"
            cur.execute(query, (username,))
            cocok = cur.fetchone()
            if cocok is not None:
                print('Username Sudah Dipakai')
                username = input('Masukkan Username: ')
                continue
        except Exception as e:
            print(f"Terjadi Kesalahan : {e}")
            username = input("Masukkan Username: ")
            continue
        break
    cur.close()
    conn.close()
    return username


# menu peminjam
def menu_peminjam():
    while True:
        header()
        buat_judul(Fore.GREEN, "MENU PEMINJAM")
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "📮 Pinjam Alat",
                "📋 Riwayat Peminjaman Saya",
                "↩ Kembalikan Alat",
                "❌ Logout"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
        if pilihan == "📮 Pinjam Alat":
            conn, cur = connectDB()
            ajukan_peminjaman_alat(conn, cur, peminjam_id, [])
        elif pilihan == "📋 Riwayat Peminjaman Saya":
            lihat_riwayat_peminjaman()
        elif pilihan == "↩ Kembalikan Alat":
            kembalikan_alat()
        elif pilihan == "❌ Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️ Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")



def ajukan_peminjaman_alat(conn, cur, peminjam_id, rows):
    """
    Fungsi untuk mengajukan peminjaman alat.
    - Support multiple alat dalam 1 peminjaman
    - DP dihitung dari total harga semua alat
    - User bisa pilih beberapa alat sebelum confirm
    """
    header()
    buat_judul(Fore.CYAN, "AJUKAN PEMINJAMAN ALAT")
    conn, cur = connectDB()
    if conn is None or cur is None:
        print(Fore.RED + "\n❌ Gagal terhubung ke database.")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return
    
    try:
        # Ambil daftar alat yang tersedia
        query = """
        SELECT
            a.idalat AS ID, 
            a.namaalat AS Nama_Alat,
            a.hargaalat AS Harga,
            a.deskripsialat AS Deskripsi,
            COALESCE(a.diskonalat, 0) AS Diskon,
            o.username AS Pemilik_Alat,
            k.kondisi AS Nama_Kondisi,
            s.status AS Status_Alat
        FROM AlatPertanian a
        JOIN Owners o ON a.idowner = o.idowners
        JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
        JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
        WHERE s.status = 'Tersedia' AND k.kondisi = 'Baik'
        ORDER BY a.idalat
        """
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:
            print(Fore.YELLOW + "\n⚠️ Tidak ada alat pertanian yang tersedia saat ini.")
            input(Fore.WHITE + "\nTekan Enter untuk kembali...")
            return None

        # Tampilkan tabel alat
        df_all = pd.DataFrame(rows, columns=['ID', 'Nama Alat', 'Harga', 'Deskripsi', 'Diskon', 'Pemilik', 'Kondisi', 'Status'])
        def fmt_money(x):
            try:
                return f"Rp. {int(x)}"
            except Exception:
                return str(x)
        df_all['Harga'] = df_all['Harga'].apply(fmt_money)
        df_all['Diskon'] = df_all['Diskon'].apply(fmt_money)
        print(Fore.WHITE + tb.tabulate(df_all, headers='keys', tablefmt='fancy_grid', showindex=False))

        # Minta durasi peminjaman satu kali untuk semua item
        while True:
            lama_str = q.text("Lama pinjam untuk semua item (hari, ctrl+c untuk batal):").ask()
            if lama_str is None:
                print(Fore.YELLOW + "\n⬅️ Batal - Kembali ke menu peminjam")
                return
            try:
                lama_global = int(lama_str)
                if lama_global <= 0:
                    print(Fore.RED + "❌ Lama pinjam harus lebih dari 0 hari.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "❌ Masukkan angka untuk lama pinjam.")

        # Loop untuk menambahkan beberapa alat (menggunakan satu durasi sama)
        selected = []
        while True:
            pilih = q.text("Masukkan ID alat untuk ditambahkan, ketik 'selesai' atau 's' jika sudah selesai, atau 'batal' atau 'b' untuk kembali:").ask()
            if pilih is None:
                print(Fore.YELLOW + "\n⬅️ Batal - Kembali ke menu peminjam")
                return
            pilih_lc = pilih.strip().lower()
            if pilih_lc in ['selesai', 'done', 's']:
                break
            if pilih_lc in ['batal', 'cancel', 'b']:
                print(Fore.YELLOW + "\n⬅️ Dibatalkan - Kembali ke menu peminjam")
                return

            try:
                idalat = int(pilih)
            except ValueError:
                print(Fore.RED + "❌ ID harus angka. Coba lagi.")
                continue

            # cek ketersediaan alat — pastikan sama dengan query daftar (status 'Tersedia' dan kondisi 'Baik')
            cur.execute(
                """
                SELECT a.idalat, a.namaalat, a.hargaalat, COALESCE(a.diskonalat,0)
                FROM AlatPertanian a
                JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
                JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
                WHERE a.idalat = %s AND s.status = 'Tersedia' AND k.kondisi = 'Baik'
                """,
                (idalat,)
            )
            alat_row = cur.fetchone()
            if not alat_row:
                print(Fore.RED + "❌ Alat tidak ditemukan atau tidak tersedia. Coba lagi.")
                continue

            # Cegah duplikasi pemilihan
            if any(item['idalat'] == idalat for item in selected):
                print(Fore.YELLOW + f"⚠️ Alat '{alat_row[1]}' sudah ditambahkan.")
                continue

            # tambahkan ke daftar menggunakan harga tetap per item (tidak dikalikan durasi)
            harga = int(alat_row[2])
            diskon = int(alat_row[3])
            # Harga adalah harga satuan/flat untuk peminjaman (tidak per-hari)
            subtotal = harga
            selected.append({'idalat': idalat, 'nama': alat_row[1], 'harga': harga, 'diskon': diskon, 'lama': lama_global, 'subtotal': subtotal})
            print(Fore.GREEN + f"✔️ Alat '{alat_row[1]}' ditambahkan (lama {lama_global} hari).")

        if not selected:
            print(Fore.YELLOW + "⚠️ Tidak ada alat yang dipilih. Kembali ke menu peminjam.")
            input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")
            return

        # Hitung total
        tanggal_pinjam = date.today()
        total_harga = sum(item['subtotal'] for item in selected)
        dp = int(total_harga * 0.25)
        # Estimasi tenggat: gunakan maksimum lama dari semua item
        max_lama = max(item['lama'] for item in selected)
        tenggat = tanggal_pinjam + timedelta(days=max_lama)

        # Tampilkan ringkasan
        df_sel = pd.DataFrame(selected)
        df_sel_display = df_sel[['idalat', 'nama', 'harga', 'lama', 'subtotal']].rename(columns={
            'idalat': 'ID', 'nama': 'Nama Alat', 'harga': 'Harga', 'lama': 'Lama(hari)', 'subtotal': 'Subtotal'
        })
        df_sel_display['Harga'] = df_sel_display['Harga'].apply(lambda x: f"Rp. {x}")
        df_sel_display['Subtotal'] = df_sel_display['Subtotal'].apply(lambda x: f"Rp. {x}")
        print(Fore.CYAN + "\nRINGKASAN PEMINJAMAN")
        print(Fore.WHITE + tb.tabulate(df_sel_display, headers='keys', tablefmt='fancy_grid', showindex=False))
        print(Fore.WHITE + f"Total harga: Rp. {total_harga}")
        print(Fore.WHITE + f"DP (25%): Rp. {dp}")
        print(Fore.WHITE + f"Tenggat (estimasi): {tenggat}")

        konfirmasi = input(Fore.YELLOW + "\nKonfirmasi ajukan peminjaman untuk semua item di atas? (y/n): " + Fore.WHITE).lower()
        if konfirmasi != 'y':
            print(Fore.YELLOW + "🔁 Pembatalan peminjaman - kembali ke menu peminjam")
            input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")
            return

        # Simpan 1 record Peminjaman
        cur.execute(
            "INSERT INTO Peminjaman (idpeminjam, tanggalpeminjaman, tenggatpeminjaman, idstatuspeminjaman) VALUES (%s, %s, %s, %s) RETURNING idpeminjaman",
            (peminjam_id, tanggal_pinjam, tenggat, 1)
        )
        idpeminjaman = cur.fetchone()[0]

        # Simpan setiap item ke DetailPeminjaman dan update status alat
        for item in selected:
            cur.execute(
                "INSERT INTO DetailPeminjaman (idpeminjaman, idalat, harga, diskon) VALUES (%s, %s, %s, %s)",
                (idpeminjaman, item['idalat'], item['harga'], item['diskon'])
            )
            cur.execute(
                "UPDATE AlatPertanian SET idstatusalat = 3 WHERE idalat = %s",
                (item['idalat'],)
            )

        conn.commit()
        print(Fore.GREEN + "\n✅ Permintaan peminjaman berhasil diajukan dan berstatus Pending untuk semua item.")
        input(Fore.WHITE + "Tekan Enter untuk kembali ke menu...")
        return idpeminjaman
    except ValueError as e:
        print(Fore.RED + f"\n❌ Error Validasi: {e}")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None
    except Exception as e:
        if conn:
            conn.rollback()
        print(Fore.RED + f"\n❌ Terjadi kesalahan: {type(e).__name__}")
        print(Fore.RED + f"📝 Pesan: {e}")
        print(Fore.RED + "\n🐛 Detail error untuk debugging:")
        traceback.print_exc()
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return None
    finally:
        if conn:
            cur.close()
            conn.close()

def lihat_riwayat_peminjaman():
    global peminjam_id
    header()
    buat_judul(Fore.MAGENTA, "RIWAYAT PEMINJAMAN SAYA")
    
    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return
        
        query = """
        SELECT 
            p.idpeminjaman,
            a.namaalat,
            'Rp ' || dp.harga::TEXT as Harga,
            p.tanggalpeminjaman as Tgl_Pinjam,
            p.tenggatpeminjaman as Tgl_Tenggat,
            sp.statuspeminjaman as Status,
            COALESCE(pr.tanggalpengembalian::TEXT, '-') as Tgl_Kembali,
            COALESCE(
                'Rp ' || SUM(d.biayadenda)::TEXT,
                '-'
            ) as Denda_Nominal
        FROM Peminjaman p
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        LEFT JOIN Pengembalian pr ON p.idpeminjaman = pr.idpeminjaman
        LEFT JOIN DetailDenda dd ON pr.idpengembalian = dd.idpengembalian
        LEFT JOIN Denda d ON dd.iddenda = d.iddenda
        WHERE p.idpeminjam = %s
        GROUP BY p.idpeminjaman, a.namaalat, dp.harga, 
                 p.tanggalpeminjaman, p.tenggatpeminjaman, sp.statuspeminjaman,
                 pr.tanggalpengembalian
        ORDER BY p.idpeminjaman DESC
        """
        
        cur.execute(query, (peminjam_id,))
        rows = cur.fetchall()
        
        if not rows:
            print(Fore.YELLOW + "⚠️ Anda belum memiliki riwayat peminjaman.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
        
        df = pd.DataFrame(rows, columns=[
            'ID', 'Alat', 'Harga', 
            'Tgl Pinjam', 'Tgl Tenggat', 'Status', 'Tgl Kembali', 'Denda Nominal'
        ])
        
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        
        input(Fore.WHITE + "\nTekan Enter untuk kembali...")
        
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        traceback.print_exc()
        input()
    finally:
        if conn:
            cur.close()
            conn.close()

def kembalikan_alat():
    global peminjam_id
    header()
    buat_judul(Fore.BLUE, "KEMBALIKAN ALAT")
    
    try:
        conn, cur = connectDB()
        if conn is None or cur is None:
            print(Fore.RED + "\n❌ Gagal terhubung ke database.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
        
        # Query untuk lihat peminjaman yang statusnya "Disetujui" (sedang dipinjam)
        query = """
        SELECT p.idpeminjaman, a.namaalat, p.tanggalpeminjaman,
        p.tenggatpeminjaman, sp.statuspeminjaman
        FROM Peminjaman p
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        WHERE p.idpeminjam = %s AND sp.statuspeminjaman = 'Disetujui'
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
        
        idpeminjaman_str = q.text("Masukkan ID peminjaman yang ingin dikembalikan (ctrl+c untuk batal): ").ask()
        if idpeminjaman_str is None:
            print(Fore.YELLOW + "\n⬅️ Batal - Kembali ke menu peminjam")
            return
        
        idpeminjaman = int(idpeminjaman_str)
        
        # Cek tanggal tenggat untuk hitung denda
        cur.execute(
            "SELECT tenggatpeminjaman FROM Peminjaman WHERE idpeminjaman = %s AND idpeminjam = %s",
            (idpeminjaman, peminjam_id)
        )
        result = cur.fetchone()
        
        if not result:
            print(Fore.RED + "❌ ID peminjaman tidak ditemukan atau bukan milik Anda!")
            input()
            return
        
        tenggat = result[0]
        today = date.today()
        iddenda = None
        
        # ========== HITUNG DENDA JIKA TERLAMBAT ==========
        if today > tenggat:
            hari_telat = (today - tenggat).days
            print(Fore.RED + f"⚠️ Anda terlambat {hari_telat} hari!")
            
            # Insert denda baru
            query_denda = """
            INSERT INTO Denda (jenispelanggaran, biayadenda)
            VALUES (%s, %s)
            RETURNING iddenda
            """
            
            fines_to_link = []
            cur.execute(query_denda, (f"Keterlambatan {hari_telat} hari", 15000 * hari_telat))
            d_id = cur.fetchone()[0]
            fines_to_link.append(d_id)
            print(Fore.YELLOW + f"💰 Denda keterlambatan: RP. {15000 * hari_telat}")
        
        # ========== INSERT KE TABEL PENGEMBALIAN ==========
        # statuspengembalian: 1 = Belum Dikembalikan, 2 = Dikembalikan, 3 = Menunggu Pemeriksaan
        # Kita pakai 2 = Dikembalikan (langsung diterima)
        query_pengembalian = """
        INSERT INTO Pengembalian (tanggalpengembalian, idpeminjaman, idstatuspengembalian, iddenda)
        VALUES (%s, %s, %s, %s)
        """
        
        # Insert pengembalian: set to 'Menunggu Pemeriksaan' (3) so owner can review and add fines
        query_pengembalian = """
        INSERT INTO Pengembalian (tanggalpengembalian, idpeminjaman, idstatuspengembalian, iddenda)
        VALUES (%s, %s, %s, %s)
        RETURNING idpengembalian
        """


        cur.execute(query_pengembalian, (today, idpeminjaman, 3, None))
        idpengembalian = cur.fetchone()[0]

        if 'fines_to_link' in locals() and fines_to_link:
            for did in fines_to_link:
                try:
                    cur.execute("INSERT INTO PengembalianDenda (idpengembalian, iddenda) VALUES (%s, %s)", (idpengembalian, did))
                except Exception:
                    pass
        
        # ========== UPDATE STATUS PEMINJAMAN JADI "SELESAI" ==========
        # statusPeminjaman: 1 = Pending, 2 = Disetujui, 3 = Ditolak, 4 = Selesai
        cur.execute(
            "UPDATE Peminjaman SET idstatuspeminjaman = 4 WHERE idpeminjaman = %s",
            (idpeminjaman,)
        )
        
        # ========== UPDATE STATUS ALAT JADI "TERSEDIA" ==========
        # Ambil semua idalat dari DetailPeminjaman
        cur.execute(
            "SELECT idalat FROM DetailPeminjaman WHERE idpeminjaman = %s",
            (idpeminjaman,)
        )
        idalat_rows = cur.fetchall()
        
        # StatusAlat: 1 = Tersedia, 2 = Dipinjam, 3 = Pending, 4 = Tidak Tersedia
        # Set semua alat terkait menjadi tersedia kembali
        for r in idalat_rows:
            try:
                cur.execute(
                    "UPDATE AlatPertanian SET idstatusalat = 1 WHERE idalat = %s",
                    (r[0],)
                )
            except Exception:
                pass
        
        conn.commit()
        
        print()
        print(Fore.GREEN + "✅ Pengembalian berhasil diproses!")
        if iddenda:
            print(Fore.YELLOW + f"⚠️ Anda memiliki denda yang harus dibayar!")
        input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")
    
    except ValueError:
        print(Fore.RED + "❌ Input tidak valid!")
        input()
    
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(Fore.RED + f"❌ Error Database: {e}")
        input()
    
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        traceback.print_exc()
        input()
    
    finally:
        if conn:
            cur.close()
            conn.close()

# menu owner
def menu_owner():
    global owner_id_skrg
    while True:
        header()
        buat_judul(Fore.YELLOW, "MENU OWNER/PEMILIK")
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "🚜 Kelola Alat Pertanian",
                "📊 Lihat Peminjaman Aktif",
                "📋 Konfirmasi Persetujuan Peminjaman",
                "✅ Konfirmasi Pengembalian",
                "📜 Riwayat Peminjaman",
                "❌ Logout"
            ]
        ).ask()
        print(Fore.CYAN + "─" * 60)
        if pilihan == "🚜 Kelola Alat Pertanian":
            kelola_alat_pertanian()
        
        elif pilihan == "📊 Lihat Peminjaman Aktif":
            lihat_peminjaman_aktif()
        
        elif pilihan == "📋 Konfirmasi Persetujuan Peminjaman":
            konfirmasi_persetujuan_peminjaman()
        
        elif pilihan == "✅ Konfirmasi Pengembalian":
            konfirmasi_pengembalian()
        
        elif pilihan == "📜 Riwayat Peminjaman":
            lihat_riwayat_peminjaman_owner()
        
        elif pilihan == "❌ Logout":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        
        else:
            print(Fore.YELLOW + "\n⚠️ Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")

def kelola_alat_pertanian():
    global owner_id_skrg
    while True:
        header()
        buat_judul(Fore.YELLOW, "KELOLA ALAT PERTANIAN")
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "➕ Tambah alat pertanian",
                "🗑️ Hapus alat",
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
            if pilihan == "➕ Tambah alat pertanian":
                
                try:
                    nama_alat = q.text("Nama alat (ctrl+c untuk batal): ").ask()
                    validasi_username(nama_alat)
                    harga_str = q.text("Harga alat (ctrl+c untuk batal): ").ask()
                    
                    if harga_str is None:
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    harga = int(harga_str)
                    desk = q.text("Deskripsi (ctrl+c untuk batal): ").ask()
                    
                    if desk is None:
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    diskon_str = q.text("Diskon (ctrl+c untuk batal): ").ask()
                    
                    if diskon_str is None:
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    diskon = int(diskon_str)
                    kondisi_str = q.text("ID Kondisi 1=Sangat baik (ctrl+c untuk batal): ").ask()
                    
                    if kondisi_str is None:
                        print(Fore.YELLOW + "⬅️ Dibatalkan\n")
                        continue
                    kondisi = int(kondisi_str)
                    cur.execute("""
                    INSERT INTO AlatPertanian
                    (namaalat, hargaalat, deskripsialat, diskonalat, idowner, idstatusalat, idkondisialat)
                    VALUES (%s, %s, %s, %s, %s, 1, %s)
                    """, (nama_alat, harga, desk, diskon, owner_id_skrg, kondisi))
                    conn.commit()
                    print(Fore.GREEN + "\n✔ Alat berhasil ditambahkan!")
                    input("Tekan Enter untuk lanjut...")
                
                except ValueError:
                    print(Fore.RED + "❌ Input tidak valid (harus angka untuk harga/diskon/kondisi)!")
                    input("Tekan Enter untuk lanjut...")
            elif pilihan == "🗑️ Hapus alat":
                try:
                    # Tampilkan daftar alat milik owner
                    cur.execute(
                        "SELECT a.idalat, a.namaalat, a.hargaalat, s.status, k.kondisi FROM AlatPertanian a JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat WHERE a.idowner = %s ORDER BY a.idalat",
                        (owner_id_skrg,)
                    )
                    alat_rows = cur.fetchall()
                    if not alat_rows:
                        print(Fore.YELLOW + "⚠️ Anda belum memiliki alat terdaftar.")
                        input(Fore.WHITE + "Tekan Enter untuk kembali...")
                        continue
                    df = pd.DataFrame(alat_rows, columns=['ID', 'Nama Alat', 'Harga', 'Status', 'Kondisi'])
                    df['Harga'] = df['Harga'].apply(lambda x: f"Rp. {x}")
                    print(Fore.WHITE + tb.tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

                    id_str = q.text("Masukkan ID alat yang ingin dihapus (ctrl+c untuk batal):").ask()
                    if id_str is None:
                        print(Fore.YELLOW + "\n⬅️ Batal")
                        continue
                    idalat = int(id_str)

                    # Pastikan alat milik owner
                    cur.execute("SELECT idalat, namaalat FROM AlatPertanian WHERE idalat = %s AND idowner = %s", (idalat, owner_id_skrg))
                    found = cur.fetchone()
                    if not found:
                        print(Fore.RED + "❌ Alat tidak ditemukan atau bukan milik Anda.")
                        input(Fore.WHITE + "Tekan Enter untuk kembali...")
                        continue

                    konf = input(Fore.YELLOW + f"Yakin ingin menghapus alat ID {idalat} - {found[1]}? (y/n): " + Fore.WHITE).lower()
                    if konf != 'y':
                        print(Fore.YELLOW + "🔁 Dibatalkan")
                        input(Fore.WHITE + "Tekan Enter untuk kembali...")
                        continue

                    # Coba cari idkondisialat untuk label 'Tidak Tersedia' (case-insensitive)
                    cur.execute("SELECT idkondisialat FROM KondisiAlat WHERE LOWER(kondisi) = LOWER(%s)", ('Tidak Tersedia',))
                    row_kond = cur.fetchone()
                    idkond = row_kond[0] if row_kond else None

                    if idkond:
                        cur.execute("UPDATE AlatPertanian SET idstatusalat = 4, idkondisialat = %s WHERE idalat = %s", (idkond, idalat))
                    else:
                        cur.execute("UPDATE AlatPertanian SET idstatusalat = 4 WHERE idalat = %s", (idalat,))

                    conn.commit()
                    print(Fore.GREEN + "✅ Alat berhasil dihapus dari daftar alat.")
                    input(Fore.WHITE + "Tekan Enter untuk kembali...")
                except Exception as e:
                    if conn:
                        conn.rollback()
                    print(Fore.RED + f"❌ Gagal menghapus alat: {e}")
                    traceback.print_exc()
                    input(Fore.WHITE + "Tekan Enter untuk kembali...")
            
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
                idalat_str = q.text("Masukkan ID alat (ctrl+c untuk batal): ").ask()
                
                if idalat_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue

                idalat = int(idalat_str)
                #tambahan klo alat masih dipinjem belum bisa diubah status nya
                cur.execute("""
                    SELECT COUNT(*)
                    FROM DetailPeminjaman dp
                    JOIN Peminjaman p ON dp.idpeminjaman = p.idpeminjaman
                    WHERE dp.idalat = %s AND p.idstatuspeminjaman IN (1,2)
                """, (idalat,))
                masih_dipinjam = cur.fetchone()[0]

                if masih_dipinjam > 0:
                    print(Fore.RED + "\n❌ Alat ini masih dalam proses peminjaman atau sedang dipakai!")
                    print(Fore.YELLOW + "Status hanya bisa diubah setelah alat dikembalikan.")
                    input("Enter...")
                    continue

                print("\nStatus Baru:")
                print("1 = Tersedia")
                print("2 = Dipesan")
                print("3 = Dipinjam")
                print("4 = Tidak Aktif")
                status_baru_str = q.text("Pilih status baru (ctrl+c untuk batal): ").ask()

                if status_baru_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue
                status_baru = int(status_baru_str)
                cur.execute("""
                UPDATE AlatPertanian
                SET idstatusalat = %s
                WHERE idalat = %s AND idowner = %s
                """, (status_baru, idalat, owner_id_skrg))
                conn.commit()
                print(Fore.GREEN + "\n✔ Status alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")

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
                idalat_str = q.text("Masukkan ID alat (ctrl+c untuk batal): ").ask()
                
                if idalat_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue
                idalat = int(idalat_str)
                print("\nKondisi Baru:")
                print("1 = Baik")
                print("2 = Rusak")
                kondisi_baru_str = q.text("Pilih kondisi baru (ctrl+c untuk batal): ").ask()
              
                if kondisi_baru_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue
                kondisi_baru = int(kondisi_baru_str)
                cur.execute("""
                UPDATE AlatPertanian
                SET idkondisialat = %s
                WHERE idalat = %s AND idowner = %s
                """, (kondisi_baru, idalat, owner_id_skrg))
                conn.commit()
                print(Fore.GREEN + "\n✔ Kondisi alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")
            
            elif pilihan == "💸 Ubah diskon alat":
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
                idalat_str = q.text("Masukkan ID alat (ctrl+c untuk batal): ").ask()
                if idalat_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue
                idalat = int(idalat_str)
                diskon_baru_str = q.text("Masukkan diskon baru (ctrl+c untuk batal): ").ask()
                if diskon_baru_str is None:
                    print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                    continue
                diskon_baru = int(diskon_baru_str)
                cur.execute("""
                UPDATE AlatPertanian
                SET diskonalat = %s
                WHERE idalat = %s AND idowner = %s
                """, (diskon_baru, idalat, owner_id_skrg))
                conn.commit()
                print(Fore.GREEN + "\n✔ Diskon alat berhasil diubah!")
                input("Tekan Enter untuk lanjut...")
            
            elif pilihan == "📋 Lihat daftar alat":
                print(Fore.WHITE + "\nDaftar alat milik Anda:\n")
                cur.execute("""
                SELECT a.idalat, a.namaalat, a.hargaalat, s.status, k.kondisi
                FROM AlatPertanian a
                JOIN StatusAlat s ON a.idstatusalat = s.idstatusalat
                JOIN KondisiAlat k ON a.idkondisialat = k.idkondisialat
                WHERE a.idowner = %s
                ORDER BY a.idalat
                """, (owner_id_skrg,))
                rows = cur.fetchall()
                if rows:
                    df = pd.DataFrame(rows, columns=["ID", "Nama Alat", "Harga", "Status", "Kondisi"])
                    print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
                else:
                    print(Fore.YELLOW + "⚠ Tidak ada alat terdaftar.")
                input("\nTekan Enter untuk kembali...")
            elif pilihan == "❌ Keluar":
                break
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

def lihat_peminjaman_aktif():
    header()
    buat_judul(Fore.YELLOW, "PEMINJAMAN AKTIF")
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
    buat_judul(Fore.YELLOW, "KONFIRMASI PERSETUJUAN PEMINJAMAN")
    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return
        
        query = """
        SELECT
            p.idpeminjaman,
            pm.username AS peminjam,
            COUNT(dp.idalat) AS jumlah_alat,
            'RP ' || SUM(dp.harga)::TEXT AS total_harga,
            'RP ' || p.dp::TEXT AS dp,
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
        valid_ids = {r[0] for r in rows}
        while True:
            header()
            buat_judul(Fore.YELLOW, "KONFIRMASI PERSETUJUAN PEMINJAMAN")
            df = pd.DataFrame(rows, columns=['ID Pinjam', 'Peminjam', 'Jumlah Alat', 'Total Harga', 'DP', 'Tenggat'])
            print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
            print()
            id_input = q.text("Masukkan ID peminjaman (ctrl+c untuk batal): ").ask()
            if id_input is None:
                print(Fore.YELLOW + "⬅️ Dibatalkan")
                return

            id_input = id_input.strip()
            if not id_input.isdigit():
                print(Fore.RED + "❌ ID harus angka!")
                input("Enter...")
                continue

            idpeminjaman = int(id_input)
            if idpeminjaman not in valid_ids:
                print(Fore.RED + "❌ ID tersebut tidak ada di daftar!")
                input("Enter...")
                continue
            break

        # pilih setuju / tolak
        pilihan = q.select(
            "Setujui atau tolak peminjaman?",
            choices=["✔ Setujui", "❌ Tolak"]
        ).ask()

        if pilihan == "❌ Tolak":
            try:
                cur.execute("""
                    UPDATE Peminjaman
                    SET idstatuspeminjaman = 3   -- Ditolak
                    WHERE idpeminjaman = %s
                """, (idpeminjaman,))

                cur.execute("""
                    UPDATE AlatPertanian
                    SET idstatusalat = 1
                    WHERE idalat IN (
                        SELECT idalat FROM DetailPeminjaman WHERE idpeminjaman = %s
                    )
                """, (idpeminjaman,))

                conn.commit()
                print(Fore.RED + "\n❌ Peminjaman ditolak owner.")
                input("Enter...")
            except Exception as e:
                conn.rollback()
                print(Fore.RED + f"❌ Gagal menolak peminjaman: {e}")
                input()
            return

        # jika setuju
        try:
            cur.execute("""
                UPDATE Peminjaman
                SET idstatuspeminjaman = 2
                WHERE idpeminjaman = %s
            """, (idpeminjaman,))

            cur.execute("""
                UPDATE AlatPertanian
                SET idstatusalat = 3
                WHERE idalat IN (
                    SELECT idalat FROM DetailPeminjaman WHERE idpeminjaman = %s
                )
            """, (idpeminjaman,))

            conn.commit()
            print(Fore.GREEN + "\n✅ Peminjaman disetujui!")
            print(Fore.GREEN + "🔄 Status alat berubah menjadi 'Dipinjam'")
            input("Enter...")
        except Exception as e:
            conn.rollback()
            print(Fore.RED + f"❌ Gagal menyetujui peminjaman: {e}")
            input()

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
    buat_judul(Fore.MAGENTA, "RIWAYAT PEMINJAMAN ALAT SAYA")
    
    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return
        
        query = """
        SELECT 
            p.idpeminjaman,
            pm.username as Peminjam,
            a.namaalat,
            'Rp ' || dp.harga::TEXT as Harga,
            p.tanggalpeminjaman as Tgl_Pinjam,
            p.tenggatpeminjaman as Tgl_Tenggat,
            sp.statuspeminjaman as Status,
            COALESCE(pr.tanggalpengembalian::TEXT, '-') as Tgl_Kembali,
            COALESCE(
                'Rp ' || SUM(d.biayadenda)::TEXT,
                '-'
            ) as Denda_Nominal
        FROM Peminjaman p
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        JOIN StatusPeminjaman sp ON p.idstatuspeminjaman = sp.idstatuspeminjaman
        LEFT JOIN Pengembalian pr ON p.idpeminjaman = pr.idpeminjaman
        LEFT JOIN DetailDenda dd ON pr.idpengembalian = dd.idpengembalian
        LEFT JOIN Denda d ON dd.iddenda = d.iddenda
        WHERE a.idowner = %s
        GROUP BY p.idpeminjaman, pm.username, a.namaalat, dp.harga,
                 p.tanggalpeminjaman, p.tenggatpeminjaman, sp.statuspeminjaman,
                 pr.tanggalpengembalian
        ORDER BY p.idpeminjaman DESC
        """
        
        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()
        
        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada riwayat peminjaman untuk alat Anda.")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            return
        
        df = pd.DataFrame(rows, columns=[
            'ID', 'Peminjam', 'Alat', 'Harga',
            'Tgl Pinjam', 'Tgl Tenggat', 'Status', 'Tgl Kembali', 'Denda Nominal'
        ])
        
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        
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
    global owner_id_skrg
    header()
    buat_judul(Fore.YELLOW, "KONFIRMASI PENGEMBALIAN ALAT")
    print()
    
    try:
        conn, cur = connectDB()
        if conn is None:
            print(Fore.RED + "❌ Gagal terhubung ke database")
            input()
            return
        
        query = """
        SELECT pen.idpengembalian, pm.username, a.namaalat, pen.tanggalpengembalian,
        pen.idpeminjaman
        FROM Pengembalian pen
        JOIN Peminjaman p ON pen.idpeminjaman = p.idpeminjaman
        JOIN Peminjam pm ON p.idpeminjam = pm.idpeminjam
        JOIN DetailPeminjaman dp ON p.idpeminjaman = dp.idpeminjaman
        JOIN AlatPertanian a ON dp.idalat = a.idalat
        WHERE a.idowner = %s AND pen.idstatuspengembalian IN (1,3)
        """
        
        cur.execute(query, (owner_id_skrg,))
        rows = cur.fetchall()
        
        if not rows:
            print(Fore.YELLOW + "⚠️ Tidak ada pengembalian baru untuk dikonfirmasi.")
            input()
            return
        
        df = pd.DataFrame(rows, columns=['ID Return', 'Peminjam', 'Alat', 'Tgl Return', 'ID Pinjam'])
        print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()
        
        # Buat set dari valid IDs untuk validasi
        valid_ids = {r[0] for r in rows}
        
        while True:
            idpengembalian_str = q.text("Masukkan ID pengembalian (ctrl+c untuk batal): ").ask()
            if idpengembalian_str is None:
                print(Fore.YELLOW + "\n⬅️ Dibatalkan")
                return
            
            try:
                idpengembalian = int(idpengembalian_str)
            except ValueError:
                print(Fore.RED + "❌ ID harus berupa angka!")
                continue
            
            if idpengembalian not in valid_ids:
                print(Fore.RED + "❌ ID pengembalian tidak ada di daftar!")
                continue
            
            break
        
        total_added = 0
        while True:
            add_more = q.confirm("Tambahkan denda (rusak/hilang/lainnya) untuk pengembalian ini?").ask()
            if not add_more:
                break
            jenis = q.text("Jenis pelanggaran (mis. Rusak/Hilang):").ask()
            if jenis is None:
                print(Fore.YELLOW + "Batal menambahkan denda")
                continue
            while True:
                biaya_str = q.text("Masukkan jumlah denda (angka):").ask()
                if biaya_str is None:
                    biaya = None
                    break
                try:
                    biaya = int(biaya_str)
                    break
                except ValueError:
                    print(Fore.RED + "Masukkan angka yang valid untuk biaya.")
            if biaya is None:
                continue
            # insert into Denda and link to Pengembalian via PengembalianDenda
            cur.execute("INSERT INTO Denda (jenispelanggaran, biayadenda) VALUES (%s, %s) RETURNING iddenda", (jenis, biaya))
            new_did = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO PengembalianDenda (idpengembalian, iddenda) VALUES (%s, %s)", (idpengembalian, new_did))
            except Exception:
                # If linking table doesn't exist, just ignore linking but Denda is inserted
                pass
            total_added += biaya
            print(Fore.GREEN + f"✔️ Denda '{jenis}' sebesar Rp. {biaya} ditambahkan.")

        # finalize pengembalian
        cur.execute("UPDATE Pengembalian SET idstatuspengembalian = 2 WHERE idpengembalian = %s", (idpengembalian,))
        conn.commit()
        print()
        print(Fore.GREEN + "✅ Pengembalian telah dikonfirmasi dan diproses oleh owner!")
        if total_added > 0:
            print(Fore.YELLOW + f"⚠️ Total denda tambahan: Rp. {total_added}")
        input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")
    
    except ValueError:
        print(Fore.RED + "❌ Input tidak valid!")
        input()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(Fore.RED + f"❌ Error Database: {e}")
        input()
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        traceback.print_exc()
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