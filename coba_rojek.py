import psycopg2
import pandas as pd
import tabulate as tb
import pyfiglet as pf
from colorama import init, Fore, Style
import questionary as q

# koneksi antar python dengan database
def connectDB():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "dizy1234",
            dbname = "ujialgo",
        )
        cur = conn.cursor()
        # print("Koneksi Berhasil") # buat ngasi kejelasan kalo db ini serius
        return conn, cur
    except Exception as e:
        print("Koneksi gagal, coba lagi")
        # v jaga2 kalo error nya di database v
        # print("Detail error:", e)
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
        print(Fore.GREEN + "  [1] 👤  Login sebagai Peminjam")
        print(Fore.YELLOW + "  [2] 🏪  Login sebagai Owner/Pemilik")
        print(Fore.BLUE + "  [3] 📝  Registrasi Akun Peminjam")
        print(Fore.RED + "  [0] ❌  Keluar")
        print()
        print(Fore.CYAN + "─" * 60)
        
        pilihan = input(Fore.WHITE + "Pilih menu: " + Fore.YELLOW)
        
        if pilihan == "1":
            login_peminjam()
        elif pilihan == "2":
            login_owner()
        elif pilihan == "3":
            registrasi()
        elif pilihan == "0":
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
    print(Fore.BLUE + Style.BRIGHT + "║" + Fore.WHITE + "          REGISTRASI AKUN PEMINJAM                     " + Fore.BLUE + "║")
    print(Fore.BLUE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()

    username = input(Fore.CYAN + "Username baru: " + Fore.WHITE)
    password = input(Fore.CYAN + "Password: " + Fore.WHITE)
    nama = input(Fore.CYAN + "Nama lengkap: " + Fore.WHITE)
    no_hp = input(Fore.CYAN + "No. HP: " + Fore.WHITE)

    print()
    print(Fore.YELLOW + "⏳ Memproses registrasi...")

    # Placeholder - nanti diganti dengan insert ke database
    print(Fore.GREEN + "✅ Registrasi berhasil!")
    print(Fore.CYAN + "Silakan login dengan akun Anda.")

    input(Fore.WHITE + "\nTekan Enter untuk kembali...")
    menu_utama()

# menu peminjam
def menu_peminjam():
    while True:
        header()
        print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  MENU PEMINJAM                         " + Fore.GREEN + "║")
        print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        print(Fore.CYAN + "  [1] 🔍  Lihat Alat Tersedia")
        print(Fore.CYAN + "  [2] 📝  Ajukan Persetujuan Peminjaman") 
        print(Fore.CYAN + "  [3] 📋  Riwayat Peminjaman Saya")
        print(Fore.CYAN + "  [4] ↩️   Kembalikan Alat") # gk tau kepake apa gk
        print(Fore.RED + "  [0] 🚪  Logout")
        print()
        print(Fore.CYAN + "─" * 60)
        
        pilihan = input(Fore.WHITE + "Pilih menu: " + Fore.YELLOW)
        
        if pilihan == "1":
            lihat_alat_tersedia()

        # elif pilihan == "2":
        #     ajukan_peminjaman()

        elif pilihan == "0":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")

# lihat alat tersedia
def lihat_alat_tersedia():
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  ALAT YANG TERSEDIA                         " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    conn, cur = connectDB()
    
    if conn is None or cur is None:
        print(Fore.RED + "\n❌ Gagal terhubung ke database.")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return

    try:
        query = "SELECT * FROM Alat_pertanian"
        cur.execute(query)
        rows = cur.fetchall()

        col_names = [desc[0] for desc in cur.description]
        if rows:
            df = pd.DataFrame(rows, columns=col_names)
        else:
            df = pd.DataFrame(columns=col_names)

        print(Fore.CYAN + "\nDaftar Alat Pertanian:\n")
        print(
            Fore.WHITE
            + tb.tabulate(
                df,
                headers="keys",
                tablefmt="fancy_grid",
                showindex=False
            )
        )

        if df.empty:
            print(Fore.YELLOW + "\n⚠ Belum ada data alat pertanian.")

        input(Fore.WHITE + "\nTekan Enter untuk kembali...")
        menu_peminjam()
        bersih_terminal()

    except Exception as e:
        print(Fore.RED + f"\n❌ Terjadi kesalahan saat mengambil data: {e}")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
    finally:
        cur.close()
        conn.close()

# menu owner
def menu_owner():
    while True:
        header()
        print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + "                    MENU OWNER                          " + Fore.YELLOW + "║")
        print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        print(Fore.CYAN + "  [1] 🚜  Kelola Alat Pertanian")
        print(Fore.CYAN + "  [2] 📊  Lihat Peminjaman Aktif")
        print(Fore.CYAN + "  [3] 📋  Konfirmasi Persetujuan Peminjaman")
        print(Fore.CYAN + "  [4] ✅  Konfirmasi Pengembalian")
        print(Fore.RED + "  [0] 🚪  Logout")
        print()
        print(Fore.CYAN + "─" * 60)
        
        pilihan = input(Fore.WHITE + "Pilih menu: " + Fore.YELLOW)
        
        if pilihan == "0":
            print(Fore.YELLOW + "\n👋 Logout berhasil!")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")
            break
        else:
            print(Fore.YELLOW + "\n⚠️  Input tidak valid...")
            input(Fore.WHITE + "Tekan Enter untuk kembali...")

# Jalanin Main program
if __name__ == "__main__":
    try:
        menu_utama()
    except KeyboardInterrupt:
        bersih_terminal()
        print(Fore.RED + "\n\n❌ Program dihentikan oleh user.\n")
    except Exception:
        print(Fore.RED + f"\n❌ Error: {Exception}\n")