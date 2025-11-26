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

    while True:
        username = input(Fore.CYAN + "Username baru: " + Fore.WHITE)
        password = input(Fore.CYAN + "Password: " + Fore.WHITE)
        nama = input(Fore.CYAN + "Nama lengkap: " + Fore.WHITE)
        no_hp = input(Fore.CYAN + "No. HP: " + Fore.WHITE)
        alamat = input(Fore.CYAN + "Alamat: " + Fore.WHITE)
        desa = input(Fore.CYAN + "Desa: " + Fore.WHITE)
        kecamatan = input(Fore.CYAN + "Kecamatan: " + Fore.WHITE)

        try:
            conn, cursor = connectDB()
            query = "INSERT INTO peminjam (username, password, nama, no_hp, alamat, desa, kecamatan)" + " VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, password, nama, no_hp, alamat, desa))
            conn.commit()
        except Exception as e:
            print(Fore.RED + f"\n❌ Gagal registrasi: {e}")
            input(Fore.WHITE + "Tekan Enter untuk mencoba lagi...")
            continue
        finally:
            if conn:
                cursor.close()
                conn.close()

        print()
        print(Fore.YELLOW + "⏳ Memproses registrasi...")
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
        pilihan = q.select(
            "Pilih menu:",
            choices=[
                "🔍  Lihat Alat Tersedia",
                "📝  Ajukan Persetujuan Peminjaman",
                "📋  Riwayat Peminjaman Saya",
                "↩   Kembalikan Alat",
                "❌  Logout"
            ]
        ).ask()
        print()
        print(Fore.CYAN + "─" * 60)
        
        if pilihan == "🔍  Lihat Alat Tersedia":
            lihat_alat_tersedia()

        # elif pilihan == "2":
        #     ajukan_peminjaman()

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
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  ALAT YANG TERSEDIA                         " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    conn, cur = connectDB()
    
    if conn is None or cur is None:
        print(Fore.RED + "\n❌ Gagal terhubung ke database.")
        input(Fore.WHITE + "Tekan Enter untuk kembali...")
        return

    try:
        # Query yang lebih spesifik untuk memilih kolom yang ingin ditampilkan
        query = """
        SELECT 
            idalat AS ID,
            namaalat AS Nama_Alat,
            hargaalat AS Harga,
            desuripsialat AS Deskripsi,
            diskonalat AS Diskon,
            idkondisialat AS Kondisi
        FROM AlatPertanian 
        WHERE idsta = 1  -- Hanya tampilkan alat yang tersedia
        """
        cur.execute(query)
        rows = cur.fetchall()

        if rows:
            # Buat DataFrame dengan kolom yang spesifik
            df = pd.DataFrame(rows, columns=['ID', 'Nama Alat', 'Harga', 'Deskripsi', 'Diskon', 'Kondisi'])
            
            # Format harga menjadi lebih readable
            df['Harga'] = df['Harga'].apply(lambda x: f"Rp {x:,.0f}" if x else "Rp 0")
            
            # Format diskon menjadi persentase
            df['Diskon'] = df['Diskon'].apply(lambda x: f"{x}%" if x else "0%")
            
            # Map kondisi ke teks yang lebih jelas
            kondisi_map = {1: 'Baik', 2: 'Perlu Perawatan', 3: 'Rusak'}
            df['Kondisi'] = df['Kondisi'].map(kondisi_map)
            
            # Tampilkan tabel dengan format yang lebih baik
            print(Fore.WHITE + tb.tabulate(df, headers="keys", tablefmt="grid", showindex=False))
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
# def ajukan_peminjaman():
    
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
        menu_peminjam()
    except KeyboardInterrupt:
        bersih_terminal()
        print(Fore.RED + "\n\n❌ Program dihentikan oleh user.\n")
    except Exception:
        print(Fore.RED + f"\n❌ Error: {Exception}\n")