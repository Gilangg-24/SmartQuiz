
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import secrets
import random
from datetime import datetime

DB_NAME = "smartquiz.db"
JUMLAH_SOAL = 10

# =====================================================
# BANK SOAL
# Setiap materi memiliki 3 tingkat kesulitan.
# Setiap tingkat memiliki 10 soal.
# =====================================================

BANK_SOAL = {
    "Dasar Python": {
        "Mudah": [
            {"soal": "Apa fungsi print()?", "opsi": ["Menampilkan output", "Menghapus file", "Mengulang program", "Membuat database"], "jawaban": "Menampilkan output"},
            {"soal": "Tipe data untuk menyimpan teks adalah ...", "opsi": ["int", "str", "float", "bool"], "jawaban": "str"},
            {"soal": "Simbol komentar satu baris Python adalah ...", "opsi": ["//", "<!--", "#", "**"], "jawaban": "#"},
            {"soal": "Perintah menerima input pengguna adalah ...", "opsi": ["input()", "print()", "type()", "range()"], "jawaban": "input()"},
            {"soal": "Kata kunci untuk percabangan adalah ...", "opsi": ["repeat", "if", "define", "loop"], "jawaban": "if"},
            {"soal": "Perulangan untuk menelusuri list adalah ...", "opsi": ["for", "switch", "case", "goto"], "jawaban": "for"},
            {"soal": "Tipe data untuk True atau False adalah ...", "opsi": ["str", "int", "bool", "list"], "jawaban": "bool"},
            {"soal": "Operator untuk membandingkan dua nilai sama adalah ...", "opsi": ["=", "==", "!=", "+="], "jawaban": "=="},
            {"soal": "Fungsi len() digunakan untuk ...", "opsi": ["Menghitung panjang data", "Mencetak teks", "Mengubah angka", "Menghapus variabel"], "jawaban": "Menghitung panjang data"},
            {"soal": "Library bawaan untuk mengacak data adalah ...", "opsi": ["random", "sqlite3", "tkinter", "datetime"], "jawaban": "random"}
        ],

        "Sedang": [
            {"soal": "Apa hasil dari operasi 10 // 3?", "opsi": ["3.33", "3", "1", "4"], "jawaban": "3"},
            {"soal": "Manakah penamaan variabel yang benar?", "opsi": ["2nama = 'Budi'", "nama siswa = 'Budi'", "nama = 'Budi'", "class = 'Budi'"], "jawaban": "nama = 'Budi'"},
            {"soal": "Apa hasil x = [2, 4, 6]; print(x[1])?", "opsi": ["2", "4", "6", "1"], "jawaban": "4"},
            {"soal": "Apa fungsi range(5)?", "opsi": ["Angka 0 sampai 4", "Angka 1 sampai 5", "Menghentikan program", "Mengubah angka"], "jawaban": "Angka 0 sampai 4"},
            {"soal": "Apa hasil dari 7 % 3?", "opsi": ["1", "2", "3", "4"], "jawaban": "1"},
            {"soal": "Kata kunci untuk membuat fungsi adalah ...", "opsi": ["func", "define", "def", "function"], "jawaban": "def"},
            {"soal": "Apa hasil dari int('12')?", "opsi": ["'12'", "12", "12.0", "Error"], "jawaban": "12"},
            {"soal": "Struktur data pasangan kunci dan nilai adalah ...", "opsi": ["list", "tuple", "dictionary", "set"], "jawaban": "dictionary"},
            {"soal": "Apa fungsi append() pada list?", "opsi": ["Menghapus elemen", "Menambah elemen di akhir", "Mengurutkan data", "Menghitung elemen"], "jawaban": "Menambah elemen di akhir"},
            {"soal": "Apa hasil dari 3 ** 2?", "opsi": ["6", "8", "9", "12"], "jawaban": "9"}
        ],

        "Sulit": [
            {"soal": "Apa keluaran a=[1,2]; b=a; b.append(3); print(a)?", "opsi": ["[1, 2]", "[1, 2, 3]", "[3]", "Error"], "jawaban": "[1, 2, 3]"},
            {"soal": "Apa hasil dari bool([])?", "opsi": ["True", "False", "None", "Error"], "jawaban": "False"},
            {"soal": "Apa fungsi try-except?", "opsi": ["Mengulang program", "Menangani exception", "Membuat class", "Menghapus variabel"], "jawaban": "Menangani exception"},
            {"soal": "Apa hasil dari len({'a': 1, 'b': 2})?", "opsi": ["1", "2", "3", "Error"], "jawaban": "2"},
            {"soal": "Apa keluaran print([x*x for x in range(3)])?", "opsi": ["[0, 1, 4]", "[1, 4, 9]", "[0, 1, 2]", "[3, 6, 9]"], "jawaban": "[0, 1, 4]"},
            {"soal": "Apa perbedaan utama list dan tuple?", "opsi": ["List dapat diubah, tuple tidak", "Tuple selalu kosong", "List hanya angka", "Tidak ada perbedaan"], "jawaban": "List dapat diubah, tuple tidak"},
            {"soal": "Apa hasil dari 'Python'[1:4]?", "opsi": ["Pyt", "yth", "tho", "ytho"], "jawaban": "yth"},
            {"soal": "Jika fungsi tidak memiliki return, nilai default-nya adalah ...", "opsi": ["0", "False", "None", "True"], "jawaban": "None"},
            {"soal": "Apa tujuan if __name__ == '__main__'?", "opsi": ["Menjalankan bagian utama saat file dijalankan langsung", "Mengimpor semua library", "Menghapus database", "Membuat perulangan"], "jawaban": "Menjalankan bagian utama saat file dijalankan langsung"},
            {"soal": "Kompleksitas rata-rata pencarian kunci dictionary adalah ...", "opsi": ["O(1)", "O(n)", "O(n²)", "O(log n)"], "jawaban": "O(1)"}
        ]
    },

    "TKJ / Jaringan Komputer": {
        "Mudah": [
            {"soal": "Perangkat yang menghubungkan jaringan berbeda adalah ...", "opsi": ["Router", "Keyboard", "Monitor", "Printer"], "jawaban": "Router"},
            {"soal": "Kepanjangan LAN adalah ...", "opsi": ["Local Area Network", "Large Access Node", "Long Area Number", "Local Analog Network"], "jawaban": "Local Area Network"},
            {"soal": "Perangkat untuk menghubungkan banyak komputer dalam LAN adalah ...", "opsi": ["Switch", "Scanner", "Speaker", "Proyektor"], "jawaban": "Switch"},
            {"soal": "Jumlah bit dalam alamat IPv4 adalah ...", "opsi": ["16 bit", "32 bit", "64 bit", "128 bit"], "jawaban": "32 bit"},
            {"soal": "Protokol penerjemah nama domain menjadi IP adalah ...", "opsi": ["DNS", "DHCP", "FTP", "SMTP"], "jawaban": "DNS"},
            {"soal": "Perangkat yang menyediakan IP otomatis adalah ...", "opsi": ["DHCP server", "DNS server", "Repeater", "Patch panel"], "jawaban": "DHCP server"},
            {"soal": "Perintah untuk menguji konektivitas adalah ...", "opsi": ["ping", "mkdir", "copy", "format"], "jawaban": "ping"},
            {"soal": "Konektor yang umum digunakan pada kabel UTP adalah ...", "opsi": ["RJ45", "USB-C", "VGA", "HDMI"], "jawaban": "RJ45"},
            {"soal": "Lapisan OSI yang menangani routing adalah ...", "opsi": ["Network", "Physical", "Session", "Presentation"], "jawaban": "Network"},
            {"soal": "Fungsi utama access point adalah ...", "opsi": ["Menghubungkan perangkat nirkabel ke jaringan", "Menyimpan dokumen", "Mencetak gambar", "Mengolah angka"], "jawaban": "Menghubungkan perangkat nirkabel ke jaringan"}
        ],

        "Sedang": [
            {"soal": "Manakah alamat IPv4 yang valid untuk host?", "opsi": ["192.168.1.10", "300.168.1.10", "192.168.1.256", "192.168.1"], "jawaban": "192.168.1.10"},
            {"soal": "Protokol untuk memperoleh IP otomatis adalah ...", "opsi": ["DHCP", "HTTP", "SSH", "IMAP"], "jawaban": "DHCP"},
            {"soal": "Jumlah host yang dapat digunakan pada subnet /24 adalah ...", "opsi": ["254", "256", "255", "128"], "jawaban": "254"},
            {"soal": "Port default HTTP adalah ...", "opsi": ["21", "22", "80", "443"], "jawaban": "80"},
            {"soal": "Perangkat yang bekerja terutama pada Layer 2 OSI adalah ...", "opsi": ["Switch", "Router", "Modem", "Repeater"], "jawaban": "Switch"},
            {"soal": "Apa fungsi default gateway?", "opsi": ["Menghubungkan jaringan lokal ke jaringan lain", "Memberi nama komputer", "Menyimpan file", "Mengubah MAC address"], "jawaban": "Menghubungkan jaringan lokal ke jaringan lain"},
            {"soal": "Kabel straight-through umumnya digunakan untuk menghubungkan ...", "opsi": ["Perangkat berbeda jenis", "Dua PC langsung", "Dua switch lama", "Dua router serial"], "jawaban": "Perangkat berbeda jenis"},
            {"soal": "DNS menggunakan port standar ...", "opsi": ["53", "67", "80", "110"], "jawaban": "53"},
            {"soal": "Alamat loopback IPv4 yang umum adalah ...", "opsi": ["127.0.0.1", "192.168.1.1", "255.255.255.0", "0.0.0.0"], "jawaban": "127.0.0.1"},
            {"soal": "Topologi dengan satu perangkat pusat seperti switch disebut ...", "opsi": ["Star", "Bus", "Ring", "Mesh"], "jawaban": "Star"}
        ],

        "Sulit": [
            {"soal": "Jaringan 192.168.10.0/26 memiliki berapa host yang dapat digunakan?", "opsi": ["62", "64", "30", "126"], "jawaban": "62"},
            {"soal": "Network address dari 192.168.1.130/25 adalah ...", "opsi": ["192.168.1.0", "192.168.1.128", "192.168.1.130", "192.168.1.255"], "jawaban": "192.168.1.128"},
            {"soal": "Broadcast address dari 192.168.1.10/24 adalah ...", "opsi": ["192.168.1.0", "192.168.1.1", "192.168.1.254", "192.168.1.255"], "jawaban": "192.168.1.255"},
            {"soal": "Protokol untuk memetakan IPv4 ke alamat MAC adalah ...", "opsi": ["ARP", "DNS", "FTP", "NTP"], "jawaban": "ARP"},
            {"soal": "Routing paket antarjaringan berlangsung pada layer OSI ...", "opsi": ["Network", "Data Link", "Transport", "Application"], "jawaban": "Network"},
            {"soal": "Bandwidth 100 Mbps dibagi rata ke 4 pengguna. Tiap pengguna mendapat ...", "opsi": ["25 Mbps", "40 Mbps", "50 Mbps", "100 Mbps"], "jawaban": "25 Mbps"},
            {"soal": "Subnet mask untuk prefix /27 adalah ...", "opsi": ["255.255.255.0", "255.255.255.128", "255.255.255.224", "255.255.255.240"], "jawaban": "255.255.255.224"},
            {"soal": "Protokol routing dinamis yang menggunakan hop count adalah ...", "opsi": ["RIP", "OSPF", "BGP", "HTTP"], "jawaban": "RIP"},
            {"soal": "Apa tujuan VLAN pada switch?", "opsi": ["Memisahkan broadcast domain secara logis", "Mempercepat CPU", "Mengganti alamat MAC", "Menghapus routing"], "jawaban": "Memisahkan broadcast domain secara logis"},
            {"soal": "Bandwidth 1 Gbps setara dengan ...", "opsi": ["100 Mbps", "500 Mbps", "1000 Mbps", "1024 Mbps"], "jawaban": "1000 Mbps"}
        ]
    }
}


# =====================================================
# DATABASE
# =====================================================

def koneksi_db():
    return sqlite3.connect(DB_NAME)


def inisialisasi_database():
    with koneksi_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS hasil_kuis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                materi TEXT NOT NULL,
                skor INTEGER NOT NULL,
                benar INTEGER NOT NULL,
                total INTEGER NOT NULL,
                tanggal TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Memeriksa kolom database lama.
        # Jika belum ada, tambahkan kolom tingkat_kesulitan.
        kolom = [
            baris[1]
            for baris in conn.execute(
                "PRAGMA table_info(hasil_kuis)"
            ).fetchall()
        ]

        if "tingkat_kesulitan" not in kolom:
            conn.execute("""
                ALTER TABLE hasil_kuis
                ADD COLUMN tingkat_kesulitan TEXT NOT NULL DEFAULT 'Mudah'
            """)


def buat_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        200_000
    ).hex()


def daftar_user(username, password):
    username = username.strip()

    if len(username) < 3:
        return False, "Username minimal 3 karakter."

    if len(password) < 6:
        return False, "Password minimal 6 karakter."

    salt = secrets.token_hex(16)
    password_hash = buat_hash(password, salt)

    try:
        with koneksi_db() as conn:
            conn.execute(
                "INSERT INTO users (username, salt, password_hash) "
                "VALUES (?, ?, ?)",
                (username, salt, password_hash)
            )

        return True, "Registrasi berhasil. Silakan login."

    except sqlite3.IntegrityError:
        return False, "Username sudah digunakan."


def cek_login(username, password):
    with koneksi_db() as conn:
        user = conn.execute(
            "SELECT id, username, salt, password_hash "
            "FROM users WHERE username = ?",
            (username.strip(),)
        ).fetchone()

    if user is None:
        return None

    hash_input = buat_hash(password, user[2])

    if secrets.compare_digest(hash_input, user[3]):
        return {"id": user[0], "username": user[1]}

    return None


def simpan_hasil(user_id, materi, tingkat_kesulitan, skor, benar, total):
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with koneksi_db() as conn:
        conn.execute("""
            INSERT INTO hasil_kuis
            (user_id, materi, tingkat_kesulitan, skor, benar, total, tanggal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, materi, tingkat_kesulitan,
            skor, benar, total, tanggal
        ))


def ambil_riwayat(user_id):
    with koneksi_db() as conn:
        return conn.execute("""
            SELECT materi, tingkat_kesulitan, skor, benar, total, tanggal
            FROM hasil_kuis
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,)).fetchall()


# =====================================================
# APLIKASI TKINTER
# =====================================================

class SmartQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartQuiz - Kuis Pembelajaran")
        self.root.geometry("760x560")
        self.root.minsize(620, 480)

        self.user = None
        self.materi = None
        self.tingkat_kesulitan = None
        self.daftar_soal = []
        self.indeks = 0
        self.jawaban_benar = 0
        self.jawaban_peserta = []

        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.tampilkan_login()

    def bersihkan(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def buat_judul(self, induk, teks):
        ttk.Label(
            induk,
            text=teks,
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 15))

    # -------------------------------------------------
    # LOGIN DAN REGISTRASI
    # -------------------------------------------------

    def tampilkan_login(self):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        self.buat_judul(frame, "SMARTQUIZ")

        ttk.Label(
            frame,
            text="Aplikasi Kuis dan Latihan Soal TKJ & Python"
        ).pack(pady=(0, 20))

        ttk.Label(frame, text="Username").pack(anchor="w")

        self.entry_username = ttk.Entry(frame, width=35)
        self.entry_username.pack(pady=(4, 12))

        ttk.Label(frame, text="Password").pack(anchor="w")

        self.entry_password = ttk.Entry(
            frame, width=35, show="*"
        )
        self.entry_password.pack(pady=(4, 16))

        ttk.Button(
            frame,
            text="Login",
            command=self.proses_login
        ).pack(fill="x", pady=4)

        ttk.Button(
            frame,
            text="Daftar Akun Baru",
            command=self.proses_daftar
        ).pack(fill="x", pady=4)

        self.entry_password.bind(
            "<Return>",
            lambda event: self.proses_login()
        )

        ttk.Label(
            frame,
            text="Buat akun terlebih dahulu jika belum memiliki akun."
        ).pack(pady=(12, 0))

    def proses_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username.strip() or not password:
            messagebox.showwarning(
                "Peringatan",
                "Username dan password harus diisi."
            )
            return

        user = cek_login(username, password)

        if user is None:
            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah."
            )
            return

        self.user = user
        self.tampilkan_menu()

    def proses_daftar(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username.strip() or not password:
            messagebox.showwarning(
                "Peringatan",
                "Isi username dan password terlebih dahulu."
            )
            return

        berhasil, pesan = daftar_user(username, password)

        if berhasil:
            messagebox.showinfo("Registrasi", pesan)
        else:
            messagebox.showerror("Registrasi Gagal", pesan)

    # -------------------------------------------------
    # MENU UTAMA
    # -------------------------------------------------

    def tampilkan_menu(self):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(fill="both", expand=True)

        self.buat_judul(frame, "Menu Utama SmartQuiz")

        ttk.Label(
            frame,
            text=f"Selamat datang, {self.user['username']}!",
            font=("Arial", 12)
        ).pack(pady=5)

        ttk.Label(
            frame,
            text="Pilih materi latihan:"
        ).pack(pady=(20, 5))

        self.pilihan_materi = ttk.Combobox(
            frame,
            values=list(BANK_SOAL.keys()),
            state="readonly",
            width=35
        )
        self.pilihan_materi.current(0)
        self.pilihan_materi.pack(pady=5)

        # PILIHAN TINGKAT KESULITAN
        ttk.Label(
            frame,
            text="Pilih tingkat kesulitan:"
        ).pack(pady=(15, 5))

        self.pilihan_kesulitan = ttk.Combobox(
            frame,
            values=["Mudah", "Sedang", "Sulit"],
            state="readonly",
            width=35
        )
        self.pilihan_kesulitan.current(0)
        self.pilihan_kesulitan.pack(pady=5)

        ttk.Label(
            frame,
            text="Mudah: konsep dasar | Sedang: penerapan | Sulit: analisis",
            wraplength=520,
            justify="center"
        ).pack(pady=8)

        ttk.Button(
            frame,
            text="Mulai Kuis (10 Soal)",
            command=self.mulai_kuis
        ).pack(fill="x", pady=(15, 6))

        ttk.Button(
            frame,
            text="Lihat Riwayat Nilai",
            command=self.tampilkan_riwayat
        ).pack(fill="x", pady=6)

        ttk.Button(
            frame,
            text="Logout",
            command=self.logout
        ).pack(fill="x", pady=6)

        ttk.Label(
            frame,
            text="Nilai dan riwayat tersimpan di database SQLite."
        ).pack(pady=15)

    def logout(self):
        self.user = None
        self.tampilkan_login()

    # -------------------------------------------------
    # KUIS
    # -------------------------------------------------

    def mulai_kuis(self):
        self.materi = self.pilihan_materi.get()
        self.tingkat_kesulitan = self.pilihan_kesulitan.get()

        kumpulan_soal = BANK_SOAL[self.materi][self.tingkat_kesulitan]

        if len(kumpulan_soal) < JUMLAH_SOAL:
            messagebox.showerror(
                "Soal Tidak Cukup",
                "Jumlah soal pada kategori ini belum mencukupi."
            )
            return

        self.daftar_soal = random.sample(
            kumpulan_soal,
            JUMLAH_SOAL
        )

        self.indeks = 0
        self.jawaban_benar = 0
        self.jawaban_peserta = []

        self.tampilkan_soal()

    def tampilkan_soal(self):
        self.bersihkan()

        soal = self.daftar_soal[self.indeks]

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text=self.materi,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            frame,
            text=f"Tingkat Kesulitan: {self.tingkat_kesulitan}",
            font=("Arial", 10, "italic")
        ).pack(anchor="w", pady=(0, 8))

        ttk.Label(
            frame,
            text=f"Soal {self.indeks + 1} dari {JUMLAH_SOAL}",
            font=("Arial", 11)
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text=soal["soal"],
            font=("Arial", 13),
            wraplength=660,
            justify="left"
        ).pack(anchor="w", pady=(25, 20))

        self.pilihan_jawaban = tk.StringVar(value="")

        for opsi in soal["opsi"]:
            ttk.Radiobutton(
                frame,
                text=opsi,
                value=opsi,
                variable=self.pilihan_jawaban
            ).pack(anchor="w", pady=7)

        ttk.Button(
            frame,
            text=(
                "Soal Berikutnya"
                if self.indeks < JUMLAH_SOAL - 1
                else "Selesaikan Kuis"
            ),
            command=self.proses_jawaban
        ).pack(anchor="e", pady=(25, 5))

    def proses_jawaban(self):
        pilihan = self.pilihan_jawaban.get()

        if not pilihan:
            messagebox.showwarning(
                "Pilih Jawaban",
                "Silakan pilih salah satu jawaban."
            )
            return

        soal = self.daftar_soal[self.indeks]
        self.jawaban_peserta.append(pilihan)

        if pilihan == soal["jawaban"]:
            self.jawaban_benar += 1

        if self.indeks < JUMLAH_SOAL - 1:
            self.indeks += 1
            self.tampilkan_soal()
        else:
            self.selesaikan_kuis()

    def selesaikan_kuis(self):
        skor = round(
            self.jawaban_benar / JUMLAH_SOAL * 100
        )

        simpan_hasil(
            self.user["id"],
            self.materi,
            self.tingkat_kesulitan,
            skor,
            self.jawaban_benar,
            JUMLAH_SOAL
        )

        self.tampilkan_hasil(skor)

    # -------------------------------------------------
    # HASIL KUIS
    # -------------------------------------------------

    def tampilkan_hasil(self, skor):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(expand=True)

        self.buat_judul(frame, "Kuis Selesai!")

        ttk.Label(
            frame,
            text=f"Materi: {self.materi}",
            font=("Arial", 12)
        ).pack(pady=5)

        ttk.Label(
            frame,
            text=f"Tingkat Kesulitan: {self.tingkat_kesulitan}",
            font=("Arial", 11)
        ).pack(pady=3)

        ttk.Label(
            frame,
            text=f"Nilai Anda: {skor}",
            font=("Arial", 24, "bold")
        ).pack(pady=12)

        ttk.Label(
            frame,
            text=f"Jawaban benar: {self.jawaban_benar} dari {JUMLAH_SOAL}"
        ).pack(pady=5)

        ttk.Label(
            frame,
            text=f"Jawaban salah: {JUMLAH_SOAL - self.jawaban_benar}"
        ).pack(pady=5)

        ttk.Button(
            frame,
            text="Lihat Pembahasan Jawaban",
            command=self.tampilkan_pembahasan
        ).pack(fill="x", pady=(18, 6))

        ttk.Button(
            frame,
            text="Kembali ke Menu",
            command=self.tampilkan_menu
        ).pack(fill="x", pady=6)

        ttk.Button(
            frame,
            text="Lihat Riwayat Nilai",
            command=self.tampilkan_riwayat
        ).pack(fill="x", pady=6)

    def tampilkan_pembahasan(self):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        self.buat_judul(frame, "Pembahasan Jawaban")

        area = tk.Text(
            frame,
            wrap="word",
            font=("Arial", 10),
            width=75,
            height=18
        )
        area.pack(fill="both", expand=True)

        for nomor, soal in enumerate(self.daftar_soal, start=1):
            pilihan = self.jawaban_peserta[nomor - 1]
            status = (
                "BENAR"
                if pilihan == soal["jawaban"]
                else "SALAH"
            )

            area.insert(
                "end",
                f"{nomor}. {soal['soal']}\n"
            )
            area.insert(
                "end",
                f"Jawaban Anda: {pilihan} ({status})\n"
            )
            area.insert(
                "end",
                f"Jawaban benar: {soal['jawaban']}\n\n"
            )

        area.config(state="disabled")

        ttk.Button(
            frame,
            text="Kembali ke Hasil",
            command=lambda: self.tampilkan_hasil(
                round(
                    self.jawaban_benar / JUMLAH_SOAL * 100
                )
            )
        ).pack(pady=10)

    # -------------------------------------------------
    # RIWAYAT NILAI
    # -------------------------------------------------

    def tampilkan_riwayat(self):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        self.buat_judul(frame, "Riwayat Nilai Kuis")

        kolom = (
            "materi",
            "kesulitan",
            "skor",
            "benar",
            "tanggal"
        )

        tabel = ttk.Treeview(
            frame,
            columns=kolom,
            show="headings",
            height=14
        )

        tabel.heading("materi", text="Materi")
        tabel.heading("kesulitan", text="Kesulitan")
        tabel.heading("skor", text="Nilai")
        tabel.heading("benar", text="Jawaban Benar")
        tabel.heading("tanggal", text="Tanggal")

        tabel.column("materi", width=200)
        tabel.column("kesulitan", width=90, anchor="center")
        tabel.column("skor", width=70, anchor="center")
        tabel.column("benar", width=120, anchor="center")
        tabel.column("tanggal", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tabel.yview
        )
        tabel.configure(yscrollcommand=scrollbar.set)

        tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for materi, kesulitan, skor, benar, total, tanggal in ambil_riwayat(
            self.user["id"]
        ):
            tabel.insert(
                "",
                "end",
                values=(
                    materi,
                    kesulitan,
                    skor,
                    f"{benar}/{total}",
                    tanggal
                )
            )

        bagian_bawah = ttk.Frame(self.root, padding=10)
        bagian_bawah.pack(fill="x")

        ttk.Button(
            bagian_bawah,
            text="Kembali ke Menu",
            command=self.tampilkan_menu
        ).pack()


# =====================================================
# MENJALANKAN APLIKASI
# =====================================================

if __name__ == "__main__":
    inisialisasi_database()

    root = tk.Tk()
    aplikasi = SmartQuiz(root)
    root.mainloop()

