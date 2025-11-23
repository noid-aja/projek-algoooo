CREATE TABLE kabupaten (
    ID_kabupaten SERIAL PRIMARY KEY,
    kabupaten VARCHAR(50) NOT NULL
)

CREATE TABLE kecamatan (
    ID_kecamatan SERIAL PRIMARY KEY,
    kecamatan VARCHAR(50) NOT NULL,
    kabupaten_ID INTEGER REFERENCES kabupaten(ID_kabupaten)
)

CREATE TABLE alamat (
    ID_alamat SERIAL PRIMARY KEY,
    jalan VARCHAR(100),
    peminjam_ID INTEGER,
    owner_ID INTEGER,
    kecamatan_ID INTEGER REFERENCES kecamatan(ID_kecamatan),
    kabupaten_ID INTEGER REFERENCES kabupaten(ID_kabupaten)
)

CREATE TABLE owners (
    ID_owner SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    no_hp VARCHAR(20)
)

CREATE TABLE peminjam (
    ID_peminjam SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    no_hp VARCHAR(20)
)

CREATE TABLE status_alat (
    ID_status_alat SERIAL PRIMARY KEY,
    status_alat VARCHAR(50) NOT NULL
)

CREATE TABLE kondisi_alat (
    ID_kondisi_alat SERIAL PRIMARY KEY,
    kondisi_alat VARCHAR(50) NOT NULL
)

CREATE TABLE Alat_pertanian (
    ID_alat SERIAL PRIMARY KEY,
    nama_alat VARCHAR(50),
    harga_alat INTEGER,
    DP INTEGER,
    deskripsi_alat VARCHAR(100),
    diskon_alat INTEGER,
    owner_ID INTEGER REFERENCES owners(ID_owner),
    status_alat_ID INTEGER REFERENCES status_alat(ID_status_alat),
    kondisi_alat_ID INTEGER REFERENCES kondisi_alat(ID_kondisi_alat)
)

CREATE TABLE status_peminjaman (
    ID_status_peminjaman SERIAL PRIMARY KEY,
    status_peminjaman VARCHAR(50)
)

CREATE TABLE peminjaman (
    ID_peminjaman SERIAL PRIMARY KEY,
    ID_peminjam INTEGER REFERENCES Peminjam(ID_peminjam),
    tanggal_peminjaman DATE,
    tenggat_peminjaman DATE,
    DP INTEGER,
    deskripsi VARCHAR(100),
    status_peminjaman_ID INTEGER REFERENCES status_peminjaman(ID_status_peminjaman)
)

CREATE TABLE detail_peminjaman (
    ID_detail_peminjaman SERIAL PRIMARY KEY,
    ID_peminjaman INTEGER REFERENCES peminjaman(ID_peminjaman),
    ID_alat INTEGER REFERENCES alat_pertanian(ID_alat),
    diskon INTEGER
)

CREATE TABLE status_pengembalian (
    ID_status_pengembalian SERIAL PRIMARY KEY,
    status_pengembalian VARCHAR(50)
)

CREATE TABLE denda (
    ID_denda SERIAL PRIMARY KEY,
    jenis_pelanggaran VARCHAR(50),
    biaya_denda INTEGER,
    status_pengembalian_ID INTEGER REFERENCES Status_pengembalian(ID_status_pengembalian)
)

CREATE TABLE pengembalian (
    ID_pengembalian SERIAL PRIMARY KEY,
    tanggal_pengembalian DATE,
    peminjaman_ID INTEGER REFERENCES Peminjaman(ID_peminjaman),
    status_pengembalian_ID INTEGER REFERENCES Status_pengembalian(ID_status_pengembalian),
    denda_ID INTEGER REFERENCES Denda(ID_denda)
)







