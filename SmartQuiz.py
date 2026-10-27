
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
# Setiap materi memiliki 12 soal, lalu dipilih 10 soal
# secara acak setiap sesi.
# =====================================================

BANK_SOAL = {
    "Dasar Python": [
        {
            "soal": "Apa fungsi dari print() dalam Python?",
            "opsi": ["Menampilkan output", "Menghapus file", "Mengulang program", "Membuat database"],
            "jawaban": "Menampilkan output"
        },
        {
            "soal": "Tipe data untuk menyimpan teks adalah ...",
            "opsi": ["int", "str", "float", "bool"],
            "jawaban": "str"
        },
        {
            "soal": "Simbol untuk komentar satu baris di Python adalah ...",
            "opsi": ["//", "<!--", "#", "**"],
            "jawaban": "#"
        },
        {
            "soal": "Manakah contoh variabel yang benar?",
            "opsi": ["2nama = 'Budi'", "nama siswa = 'Budi'",
                     "nama = 'Budi'", "class = 'Budi'"],
            "jawaban": "nama = 'Budi'"
        },
        {
            "soal": "Hasil dari operasi 10 // 3 adalah ...",
            "opsi": ["3.33", "3", "1", "4"],
            "jawaban": "3"
        },
        {
            "soal": "Perintah untuk menerima input dari pengguna adalah ...",
            "opsi": ["input()", "print()", "type()", "range()"],
            "jawaban": "input()"
        },
        {
            "soal": "Struktur percabangan dalam Python menggunakan kata ...",
            "opsi": ["repeat", "if", "define", "loop"],
            "jawaban": "if"
        },
        {
            "soal": "Perulangan yang umum digunakan untuk menelusuri list adalah ...",
            "opsi": ["for", "switch", "case", "goto"],
            "jawaban": "for"
        },
        {
            "soal": "Tipe data untuk nilai True atau False adalah ...",
            "opsi": ["str", "int", "bool", "list"],
            "jawaban": "bool"
        },
        {
            "soal": "Manakah operator untuk membandingkan dua nilai agar sama?",
            "opsi": ["=", "==", "!=", "+="],
            "jawaban": "=="
        },
        {
            "soal": "Fungsi len() digunakan untuk ...",
            "opsi": ["Menghitung panjang data", "Mencetak teks",
                     "Mengubah menjadi angka", "Menghapus variabel"],
            "jawaban": "Menghitung panjang data"
        },
        {
            "soal": "Library bawaan Python untuk mengacak urutan data adalah ...",
            "opsi": ["random", "sqlite3", "tkinter", "datetime"],
            "jawaban": "random"
        }
    ],

    "TKJ / Jaringan Komputer": [
        {
            "soal": "Perangkat yang menghubungkan jaringan berbeda adalah ...",
            "opsi": ["Router", "Keyboard", "Monitor", "Printer"],
            "jawaban": "Router"
        },
        {
            "soal": "Kepanjangan LAN adalah ...",
            "opsi": ["Local Area Network", "Large Access Node",
                     "Long Area Number", "Local Analog Network"],
            "jawaban": "Local Area Network"
        },
        {
            "soal": "Perangkat untuk menghubungkan banyak komputer dalam LAN adalah ...",
            "opsi": ["Switch", "Scanner", "Speaker", "Proyektor"],
            "jawaban": "Switch"
        },
        {
            "soal": "Berapa jumlah bit dalam alamat IPv4?",
            "opsi": ["16 bit", "32 bit", "64 bit", "128 bit"],
            "jawaban": "32 bit"
        },
        {
            "soal": "Protokol yang menerjemahkan nama domain menjadi alamat IP adalah ...",
            "opsi": ["DNS", "DHCP", "FTP", "SMTP"],
            "jawaban": "DNS"
        },
        {
            "soal": "Perangkat yang menyediakan alamat IP secara otomatis adalah ...",
            "opsi": ["DHCP server", "DNS server", "Repeater", "Patch panel"],
            "jawaban": "DHCP server"
        },
        {
            "soal": "Perintah umum untuk menguji konektivitas ke perangkat lain adalah ...",
            "opsi": ["ping", "mkdir", "copy", "format"],
            "jawaban": "ping"
        },
        {
            "soal": "Konektor yang umum digunakan pada kabel Ethernet UTP adalah ...",
            "opsi": ["RJ45", "USB-C", "VGA", "HDMI"],
            "jawaban": "RJ45"
        },
        {
            "soal": "Manakah alamat IPv4 yang valid untuk digunakan sebagai alamat host?",
            "opsi": ["192.168.1.10", "300.168.1.10",
                     "192.168.1.256", "192.168.1"],
            "jawaban": "192.168.1.10"
        },
        {
            "soal": "Lapisan OSI yang menangani pengalamatan logis dan routing adalah ...",
            "opsi": ["Network", "Physical", "Session", "Presentation"],
            "jawaban": "Network"
        },
        {
            "soal": "Fungsi utama access point adalah ...",
            "opsi": ["Menghubungkan perangkat nirkabel ke jaringan",
                     "Menyimpan dokumen", "Mencetak gambar",
                     "Mengolah angka"],
            "jawaban": "Menghubungkan perangkat nirkabel ke jaringan"
        },
        {
            "soal": "Protokol yang umum digunakan untuk memperoleh alamat IP otomatis adalah ...",
            "opsi": ["DHCP", "HTTP", "SSH", "IMAP"],
            "jawaban": "DHCP"
        }
    ]
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


def simpan_hasil(user_id, materi, skor, benar, total):
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with koneksi_db() as conn:
        conn.execute("""
            INSERT INTO hasil_kuis
            (user_id, materi, skor, benar, total, tanggal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, materi, skor, benar, total, tanggal))


def ambil_riwayat(user_id):
    with koneksi_db() as conn:
        return conn.execute("""
            SELECT materi, skor, benar, total, tanggal
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
            frame, text="Aplikasi Kuis dan Latihan Soal TKJ & Python"
        ).pack(pady=(0, 20))

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.entry_username = ttk.Entry(frame, width=35)
        self.entry_username.pack(pady=(4, 12))

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.entry_password = ttk.Entry(frame, width=35, show="*")
        self.entry_password.pack(pady=(4, 16))

        ttk.Button(
            frame, text="Login", command=self.proses_login
        ).pack(fill="x", pady=4)

        ttk.Button(
            frame, text="Daftar Akun Baru",
            command=self.proses_daftar
        ).pack(fill="x", pady=4)

        self.entry_password.bind("<Return>", lambda event: self.proses_login())

        ttk.Label(
            frame, text="Buat akun terlebih dahulu jika belum memiliki akun."
        ).pack(pady=(12, 0))

    def proses_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username.strip() or not password:
            messagebox.showwarning(
                "Peringatan", "Username dan password harus diisi."
            )
            return

        user = cek_login(username, password)

        if user is None:
            messagebox.showerror(
                "Login Gagal", "Username atau password salah."
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

        ttk.Label(frame, text="Pilih materi latihan:").pack(pady=(20, 5))

        self.pilihan_materi = ttk.Combobox(
            frame,
            values=list(BANK_SOAL.keys()),
            state="readonly",
            width=35
        )
        self.pilihan_materi.current(0)
        self.pilihan_materi.pack(pady=5)

        ttk.Button(
            frame, text="Mulai Kuis (10 Soal)",
            command=self.mulai_kuis
        ).pack(fill="x", pady=(15, 6))

        ttk.Button(
            frame, text="Lihat Riwayat Nilai",
            command=self.tampilkan_riwayat
        ).pack(fill="x", pady=6)

        ttk.Button(
            frame, text="Logout",
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
        self.daftar_soal = random.sample(
            BANK_SOAL[self.materi], JUMLAH_SOAL
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
            frame, text=self.materi,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 10))

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
            text="Soal Berikutnya" if self.indeks < JUMLAH_SOAL - 1
                 else "Selesaikan Kuis",
            command=self.proses_jawaban
        ).pack(anchor="e", pady=(25, 5))

    def proses_jawaban(self):
        pilihan = self.pilihan_jawaban.get()

        if not pilihan:
            messagebox.showwarning(
                "Pilih Jawaban", "Silakan pilih salah satu jawaban."
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
            frame, text=f"Materi: {self.materi}",
            font=("Arial", 12)
        ).pack(pady=5)

        ttk.Label(
            frame, text=f"Nilai Anda: {skor}",
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
            frame, text="Lihat Pembahasan Jawaban",
            command=self.tampilkan_pembahasan
        ).pack(fill="x", pady=(18, 6))

        ttk.Button(
            frame, text="Kembali ke Menu",
            command=self.tampilkan_menu
        ).pack(fill="x", pady=6)

        ttk.Button(
            frame, text="Lihat Riwayat Nilai",
            command=self.tampilkan_riwayat
        ).pack(fill="x", pady=6)

    def tampilkan_pembahasan(self):
        self.bersihkan()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        self.buat_judul(frame, "Pembahasan Jawaban")

        area = tk.Text(
            frame, wrap="word", font=("Arial", 10),
            width=75, height=18
        )
        area.pack(fill="both", expand=True)

        for nomor, soal in enumerate(self.daftar_soal, start=1):
            pilihan = self.jawaban_peserta[nomor - 1]
            status = "BENAR" if pilihan == soal["jawaban"] else "SALAH"

            area.insert("end", f"{nomor}. {soal['soal']}\n")
            area.insert("end", f"Jawaban Anda: {pilihan} ({status})\n")
            area.insert("end", f"Jawaban benar: {soal['jawaban']}\n\n")

        area.config(state="disabled")

        ttk.Button(
            frame, text="Kembali ke Hasil",
            command=lambda: self.tampilkan_hasil(
                round(self.jawaban_benar / JUMLAH_SOAL * 100)
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

        kolom = ("materi", "skor", "benar", "tanggal")

        tabel = ttk.Treeview(
            frame, columns=kolom, show="headings", height=14
        )

        tabel.heading("materi", text="Materi")
        tabel.heading("skor", text="Nilai")
        tabel.heading("benar", text="Jawaban Benar")
        tabel.heading("tanggal", text="Tanggal")

        tabel.column("materi", width=200)
        tabel.column("skor", width=70, anchor="center")
        tabel.column("benar", width=120, anchor="center")
        tabel.column("tanggal", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=tabel.yview
        )
        tabel.configure(yscrollcommand=scrollbar.set)

        tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for materi, skor, benar, total, tanggal in ambil_riwayat(
            self.user["id"]
        ):
            tabel.insert(
                "", "end",
                values=(materi, skor, f"{benar}/{total}", tanggal)
            )

        bagian_bawah = ttk.Frame(self.root, padding=10)
        bagian_bawah.pack(fill="x")

        ttk.Button(
            bagian_bawah, text="Kembali ke Menu",
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
