import csv
from collections import deque
from datetime import datetime

class FinanceManager:
    def __init__(self, filename):
        self.filename = filename
        self.transactions = {}  # Struktur data: HashMap
        self.history = deque()  # Struktur data: Queue
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    kategori = row["Kategori"]
                    jumlah = float(row["Jumlah"])
                    tipe = row["Tipe"]
                    tanggal = row.get("Tanggal", datetime.now().strftime("%Y-%m-%d"))
                    if kategori not in self.transactions:
                        self.transactions[kategori] = []
                    self.transactions[kategori].append((jumlah, tipe, tanggal))
                    self.history.append((kategori, jumlah, tipe, tanggal))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Kategori", "Jumlah", "Tipe", "Tanggal"])
            writer.writeheader()
            for kategori in self.transactions:
                for jumlah, tipe, tanggal in self.transactions[kategori]:
                    writer.writerow({"Kategori": kategori, "Jumlah": jumlah, "Tipe": tipe, "Tanggal": tanggal})

    def tambah_transaksi(self, kategori, jumlah, tipe, tanggal=None):
        if tanggal is None:
            tanggal = datetime.now().strftime("%Y-%m-%d")
        if kategori not in self.transactions:
            self.transactions[kategori] = []
        self.transactions[kategori].append((jumlah, tipe, tanggal))
        self.history.append((kategori, jumlah, tipe, tanggal))
        self.save_data()
        print("✅ Transaksi berhasil ditambahkan.")

    def tampilkan_transaksi(self):
        print("\n📋 Daftar Transaksi:")
        for kategori in self.transactions:
            for jumlah, tipe, tanggal in self.transactions[kategori]:
                print(f"- {tipe.upper()} | {kategori}: Rp {jumlah:.2f} pada {tanggal}")

    def hitung_saldo(self):
        saldo = 0
        for transaksi in self.history:
            _, jumlah, tipe, _ = transaksi
            if tipe == "pemasukan":
                saldo += jumlah
            elif tipe == "pengeluaran":
                saldo -= jumlah
        print(f"\n💰 Total Saldo: Rp {saldo:.2f}")

    def undo_transaksi(self):
        if not self.history:
            print("⚠️ Tidak ada transaksi untuk di-undo.")
            return
        kategori, jumlah, tipe, tanggal = self.history.pop()
        if kategori in self.transactions and (jumlah, tipe, tanggal) in self.transactions[kategori]:
            self.transactions[kategori].remove((jumlah, tipe, tanggal))
            if not self.transactions[kategori]:
                del self.transactions[kategori]
            self.save_data()
            print("↩️ Transaksi terakhir dibatalkan.")
        else:
            print("⚠️ Gagal undo transaksi.")

    def laporan_bulanan(self, tahun, bulan):
        total_masuk = total_keluar = 0
        print(f"\n📆 Laporan Bulan {bulan}/{tahun}")
        for transaksi in self.history:
            kategori, jumlah, tipe, tanggal = transaksi
            tgl = datetime.strptime(tanggal, "%Y-%m-%d")
            if tgl.year == tahun and tgl.month == bulan:
                print(f"- {tipe.upper()} | {kategori}: Rp {jumlah:.2f} pada {tanggal}")
                if tipe == "pemasukan":
                    total_masuk += jumlah
                elif tipe == "pengeluaran":
                    total_keluar += jumlah
        print(f"Total Pemasukan: Rp {total_masuk:.2f}")
        print(f"Total Pengeluaran: Rp {total_keluar:.2f}")

    def laporan_tahunan(self, tahun):
        total_masuk = total_keluar = 0
        print(f"\n📅 Laporan Tahun {tahun}")
        for transaksi in self.history:
            kategori, jumlah, tipe, tanggal = transaksi
            tgl = datetime.strptime(tanggal, "%Y-%m-%d")
            if tgl.year == tahun:
                print(f"- {tipe.upper()} | {kategori}: Rp {jumlah:.2f} pada {tanggal}")
                if tipe == "pemasukan":
                    total_masuk += jumlah
                elif tipe == "pengeluaran":
                    total_keluar += jumlah
        print(f"Total Pemasukan: Rp {total_masuk:.2f}")
        print(f"Total Pengeluaran: Rp {total_keluar:.2f}")


# ========== PROGRAM UTAMA ==========

def menu():
    fm = FinanceManager("keuangan.csv")

    while True:
        print("\n=== APLIKASI MANAJEMEN KEUANGAN PRIBADI ===")
        print("1. Tambah Transaksi")
        print("2. Tampilkan Transaksi")
        print("3. Hitung Total Saldo")
        print("4. Undo Transaksi Terakhir")
        print("5. Laporan Bulanan")
        print("6. Laporan Tahunan")
        print("7. Keluar")
        pilihan = input("Pilih menu (1-7): ")

        if pilihan == "1":
            kategori = input("Masukkan kategori (misal: Makanan, Gaji): ")
            jumlah = float(input("Masukkan jumlah (Rp): "))
            tipe = input("Tipe (pemasukan/pengeluaran): ").lower()
            tanggal = input("Masukkan tanggal (YYYY-MM-DD) [kosong = hari ini]: ")
            if not tanggal:
                tanggal = None
            if tipe in ["pemasukan", "pengeluaran"]:
                fm.tambah_transaksi(kategori, jumlah, tipe, tanggal)
            else:
                print("❌ Tipe tidak valid.")
        elif pilihan == "2":
            fm.tampilkan_transaksi()
        elif pilihan == "3":
            fm.hitung_saldo()
        elif pilihan == "4":
            fm.undo_transaksi()
        elif pilihan == "5":
            tahun = int(input("Masukkan tahun (YYYY): "))
            bulan = int(input("Masukkan bulan (1-12): "))
            fm.laporan_bulanan(tahun, bulan)
        elif pilihan == "6":
            tahun = int(input("Masukkan tahun (YYYY): "))
            fm.laporan_tahunan(tahun)
        elif pilihan == "7":
            print("👋 Terima kasih. Program selesai.")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
