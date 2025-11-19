import psycopg2
import pandas as pd
import tabulate as tb
import pyfiglet
from colorama import init, Fore, Style

# koneksi antar python dengan database
def connectDB():
    try:
        conn = psycopg2.connect(
            host = "localhost",
            user = "postgres",
            password = "NOIDAJA",
            dbname = "bekerja",
        )
        cur = conn.cursor()
        print("Koneksi Berhasil")
        return conn, cur
    except Exception:
        print("Koneksi gagal, coba lagi")
        return None

connectDB()

# biar color berubah tanpa harus reset di setiap fungsi
init(autoreset=True)

# clear sistem untuk lebih jelas
def clear_screen():
    """Clear screen yang beneran"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

# judul program
def header():
    """Tampilan header dengan pyfiglet"""
    clear_screen()
    title = pyfiglet.figlet_format("SEWA ALAT", font="slant")
    print(Fore.GREEN + title)
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + Style.BRIGHT + "   SISTEM PEMINJAMAN & PENYEWAAN ALAT PERTANIAN")
    print(Fore.CYAN + "="*60)
    print()

# menu utama
def menu_utama():
    """Menu utama sistem"""
    while True:
        header()
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║" + Fore.CYAN + "                    MENU UTAMA                          " + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        print(Fore.GREEN + "  [1] 👤  Login sebagai Peminjam")
        print(Fore.YELLOW + "  [2] 🏪  Login sebagai Owner/Pemilik")
        print(Fore.BLUE + "  [3] 📝  Registrasi Akun Baru")
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
            clear_screen()
            print(Fore.GREEN + Style.BRIGHT + "\n✨ Terima kasih telah menggunakan sistem kami! ✨\n")
            break
        else:
            print(Fore.RED + "\n❌ Pilihan tidak valid! Tekan Enter untuk kembali...")
            input()

# login peminjam
def login_peminjam():
    """Form login untuk peminjam"""
    header()
    print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "              LOGIN SEBAGAI PEMINJAM                    " + Fore.GREEN + "║")
    print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    username = input(Fore.CYAN + "Username: " + Fore.WHITE)
    password = input(Fore.CYAN + "Password: " + Fore.WHITE)
    
    print()
    print(Fore.YELLOW + "⏳ Memproses login...")
    
    # Placeholder - nanti diganti dengan validasi database
    print(Fore.GREEN + "✅ Login berhasil!")
    print(Fore.CYAN + f"Selamat datang, {username}!")
    
    input(Fore.WHITE + "\nTekan Enter untuk melanjutkan...")
    menu_peminjam()

# login owner
def login_owner():
    """Form login untuk owner"""
    header()
    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + "           LOGIN SEBAGAI OWNER/PEMILIK                  " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    username = input(Fore.CYAN + "Username: " + Fore.WHITE)
    password = input(Fore.CYAN + "Password: " + Fore.WHITE)
    
    print()
    print(Fore.YELLOW + "⏳ Memproses login...")
    
    # Placeholder - nanti diganti dengan validasi database
    print(Fore.GREEN + "✅ Login berhasil!")
    print(Fore.CYAN + f"Selamat datang, {username}!")
    
    input(Fore.WHITE + "\nTekan Enter untuk melanjutkan...")
    menu_owner()

# registrasi owner dan peminjam
def registrasi():
    """Form registrasi akun baru"""
    header()
    print(Fore.BLUE + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
    print(Fore.BLUE + Style.BRIGHT + "║" + Fore.WHITE + "              REGISTRASI AKUN BARU                      " + Fore.BLUE + "║")
    print(Fore.BLUE + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
    print()
    
    print(Fore.CYAN + "Pilih jenis akun:")
    print(Fore.WHITE + "  [1] Peminjam")
    print(Fore.WHITE + "  [2] Owner/Pemilik Alat")
    print(Fore.WHITE + "  [0] Kembali")
    print()
    
    jenis = input(Fore.WHITE + "Pilihan: " + Fore.YELLOW)
    
    if jenis == "0":
        return
    
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

# menu peminjam
def menu_peminjam():
    """Menu untuk peminjam (placeholder)"""
    while True:
        header()
        print(Fore.GREEN + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.GREEN + Style.BRIGHT + "║" + Fore.WHITE + "                  MENU PEMINJAM                         " + Fore.GREEN + "║")
        print(Fore.GREEN + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        print(Fore.CYAN + "  [1] 🔍  Lihat Alat Tersedia")
        print(Fore.CYAN + "  [2] 📝  Ajukan Peminjaman")
        print(Fore.CYAN + "  [3] 📋  Riwayat Peminjaman Saya")
        print(Fore.CYAN + "  [4] ↩️   Kembalikan Alat")
        print(Fore.CYAN + "  [5] 👤  Profil Saya")
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

# menu owner
def menu_owner():
    """Menu untuk owner (placeholder)"""
    while True:
        header()
        print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════════════════════════════════╗")
        print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.WHITE + "                    MENU OWNER                          " + Fore.YELLOW + "║")
        print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════════════════════════════════╝")
        print()
        print(Fore.CYAN + "  [1] 🚜  Kelola Alat Pertanian")
        print(Fore.CYAN + "  [2] 📊  Lihat Peminjaman Aktif")
        print(Fore.CYAN + "  [3] 💰  Laporan Pendapatan")
        print(Fore.CYAN + "  [4] ✅  Konfirmasi Pengembalian")
        print(Fore.CYAN + "  [5] 👤  Profil Saya")
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
        clear_screen()
        print(Fore.RED + "\n\n❌ Program dihentikan oleh user.\n")
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {e}\n")