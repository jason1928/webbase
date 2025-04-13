from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
from datetime import datetime
from flask import Response
import csv
import io

app = Flask(__name__)

# Koneksi MongoDB lokal
client = MongoClient("mongodb://localhost:27017/")
db = client["web_dashboard_db"]
collection = db["warta_db"]
keuangan_collection = db["keuangan_db"]
jadwal_colletion = db["keuangan_db"]
users = db["users_db"]

# Halaman Utama / Dashboard
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Halaman Jemaat
@app.route("/jemaat")
def jemaat():
    users = list(collection.find())
    return render_template("jemaat.html", users=users)

@app.route("/simpan-jemaat", methods=["POST"])
def simpan_jemaat():
    nama = request.form.get("nama")
    alamat = request.form.get("alamat")
    no_hp = request.form.get("no_hp")
    
    # Simpan ke MongoDB
    data = {
        "nama": nama,
        "alamat": alamat,
        "no_hp": no_hp
    }
    collection.insert_one(data)
    
    return redirect(url_for("jemaat"))


# Halaman Jadwal
@app.route("/jadwal")
def jadwal():
    return render_template("jadwal.html")

# Halaman Keuangan
@app.route('/keuangan')
def keuangan():
    transaksi_list = list(keuangan_collection.find())

    # Convert 'tanggal' from string to datetime (if it's a string)
    for transaksi in transaksi_list:
        if isinstance(transaksi['tanggal'], str):
            transaksi['tanggal'] = datetime.strptime(transaksi['tanggal'], "%Y-%m-%d")

    # Hitung total pemasukan dan pengeluaran
    total_pemasukan = sum(t.get('pemasukan', 0) for t in transaksi_list)
    total_pengeluaran = sum(t.get('pengeluaran', 0) for t in transaksi_list)
    saldo = total_pemasukan - total_pengeluaran

    return render_template(
        'keuangan.html',
        transaksi=transaksi_list,
        total_pemasukan=total_pemasukan,
        total_pengeluaran=total_pengeluaran,
        saldo=saldo
    )

@app.route('/keuangan/save', methods=['POST'])
def simpan_transaksi():
    tanggal = request.form.get("tanggal")
    keterangan = request.form.get("keterangan")
    pemasukan = request.form.get("pemasukan")
    pengeluaran = request.form.get("pengeluaran")

    data = {
        "tanggal": datetime.strptime(tanggal, "%Y-%m-%d"),
        "keterangan": keterangan,
        "pemasukan": int(pemasukan) if pemasukan else 0,
        "pengeluaran": int(pengeluaran) if pengeluaran else 0
    }

    keuangan_collection.insert_one(data)
    return redirect(url_for("keuangan"))

@app.route('/keuangan/download')
def download_keuangan():
    transaksi_list = list(keuangan_collection.find())

    # Buat buffer CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Header kolom CSV
    writer.writerow(['Tanggal', 'Keterangan', 'Pemasukan', 'Pengeluaran'])

    # Data baris CSV
    for t in transaksi_list:
        tanggal = t['tanggal'].strftime("%Y-%m-%d") if isinstance(t['tanggal'], datetime) else str(t['tanggal'])
        writer.writerow([
            tanggal,
            t.get('keterangan', ''),
            t.get('pemasukan', 0),
            t.get('pengeluaran', 0)
        ])

    # Reset posisi ke awal untuk di-read
    output.seek(0)

    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=keuangan.csv'}
    )

# Halaman Warta
@app.route("/warta", methods=["GET"])
def warta():
    warta_list = list(collection.find().sort("timestamp", -1))  # Urutkan berdasarkan timestamp
    print(warta_list)  # Menampilkan data warta di konsol
    return render_template("warta.html", warta_list=warta_list)

@app.route("/warta/save", methods=["POST"])
def save_warta():
    warta_baru = request.form.get("warta")
    if warta_baru:
        try:
            collection.insert_one({
                "warta": warta_baru,
                "timestamp": datetime.datetime.now()  # Menyimpan timestamp saat warta ditambahkan
            })
            print("Warta baru disimpan:", warta_baru)  # Menampilkan warta yang disimpan di konsol
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan warta: {e}")
    return redirect(url_for("warta"))

if __name__ == "__main__":
    app.run(debug=True)
