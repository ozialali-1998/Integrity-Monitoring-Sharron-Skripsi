# Software Requirement Specification (SRS)

## Aplikasi Web File Integrity Monitoring (FIM) untuk Penelitian Cyber Security

### 1. Pendahuluan

#### 1.1 Tujuan Dokumen

Dokumen ini mendefinisikan kebutuhan perangkat lunak untuk aplikasi web **File Integrity Monitoring (FIM)** yang digunakan dalam konteks penelitian skripsi Cyber Security. Sistem dirancang untuk memantau integritas file pada direktori tertentu, membangun baseline hash, melakukan verifikasi integritas, mendeteksi perubahan file, menampilkan alert, menyimpan log aktivitas, serta melakukan benchmark algoritma hashing dan key derivation function.

#### 1.2 Ruang Lingkup Sistem

Aplikasi FIM berbasis web ini berfokus pada pemantauan file dalam lingkungan lokal atau server penelitian. Sistem tidak ditujukan sebagai solusi enterprise security penuh, melainkan sebagai aplikasi penelitian yang dapat menunjukkan proses deteksi perubahan file dan perbandingan performa beberapa algoritma.

Sistem mendukung tiga algoritma utama:

1. **SHA-256** untuk hashing cepat dan umum.
2. **PBKDF2** untuk pengujian fungsi derivasi kunci berbasis iterasi.
3. **Argon2id** untuk pengujian fungsi derivasi kunci modern yang memory-hard.

#### 1.3 Batasan Sistem

Sistem memiliki batasan sebagai berikut:

- Tidak wajib mendukung multi-user.
- Tidak wajib memiliki sistem login kompleks.
- Tidak wajib menggunakan AI.
- Tidak wajib berjalan di cloud.
- Tidak wajib menerapkan security enterprise seperti SIEM, EDR, RBAC kompleks, atau distributed agent.
- Tidak wajib menyediakan aplikasi mobile.
- Fokus utama adalah validitas proses FIM dan benchmark algoritma untuk kebutuhan penelitian.

#### 1.4 Definisi Istilah

| Istilah | Definisi |
| --- | --- |
| FIM | File Integrity Monitoring, proses pemantauan integritas file untuk mendeteksi perubahan tidak sah. |
| Baseline | Data referensi awal yang berisi daftar file, metadata, dan nilai hash. |
| Hash | Nilai digital yang dihasilkan dari isi file menggunakan algoritma tertentu. |
| Verification | Proses membandingkan kondisi file saat ini dengan baseline. |
| Modified File | File yang masih ada tetapi isi atau metadatanya berubah dibanding baseline. |
| Added File | File baru yang tidak terdapat pada baseline. |
| Deleted File | File yang tercatat pada baseline tetapi tidak ditemukan saat verifikasi. |
| Alert | Notifikasi sistem ketika ditemukan perubahan integritas file. |
| Benchmark | Pengukuran performa algoritma berdasarkan waktu eksekusi, ukuran file, dan parameter algoritma. |

---

## 2. Functional Requirements

### 2.1 Manajemen Direktori Monitoring

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-001 | Sistem harus menyediakan fitur untuk menentukan direktori yang akan dimonitor. | Must Have |
| FR-002 | Sistem harus memvalidasi bahwa path direktori tersedia dan dapat diakses oleh aplikasi. | Must Have |
| FR-003 | Sistem harus menolak path yang bukan direktori valid. | Must Have |
| FR-004 | Sistem harus menyimpan konfigurasi direktori monitoring ke database. | Must Have |
| FR-005 | Sistem dapat mendukung lebih dari satu konfigurasi direktori monitoring untuk kebutuhan pengujian. | Should Have |
| FR-006 | Sistem harus menampilkan daftar direktori yang telah dikonfigurasi. | Must Have |
| FR-007 | Sistem harus menyediakan fitur mengaktifkan atau menonaktifkan konfigurasi direktori monitoring. | Should Have |

### 2.2 Pembuatan Baseline Hash

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-008 | Sistem harus menyediakan fitur untuk membuat baseline dari direktori yang dipilih. | Must Have |
| FR-009 | Sistem harus membaca seluruh file dalam direktori target secara rekursif. | Must Have |
| FR-010 | Sistem harus menghasilkan hash untuk setiap file berdasarkan algoritma yang dipilih. | Must Have |
| FR-011 | Sistem harus mendukung algoritma SHA-256 untuk baseline. | Must Have |
| FR-012 | Sistem harus mendukung algoritma PBKDF2 untuk baseline penelitian/benchmark. | Must Have |
| FR-013 | Sistem harus mendukung algoritma Argon2id untuk baseline penelitian/benchmark. | Must Have |
| FR-014 | Sistem harus menyimpan path relatif file, ukuran file, timestamp modifikasi, algoritma, parameter algoritma, dan nilai hash ke database. | Must Have |
| FR-015 | Sistem harus mencatat waktu mulai, waktu selesai, total file, total ukuran, dan durasi proses baseline. | Must Have |
| FR-016 | Sistem harus membuat log aktivitas setiap kali baseline dibuat. | Must Have |
| FR-017 | Sistem harus menampilkan ringkasan hasil baseline kepada pengguna. | Must Have |

### 2.3 Verifikasi Integritas File

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-018 | Sistem harus menyediakan fitur untuk menjalankan verifikasi integritas terhadap baseline tertentu. | Must Have |
| FR-019 | Sistem harus membaca kondisi file terkini pada direktori monitoring secara rekursif. | Must Have |
| FR-020 | Sistem harus menghitung ulang hash file saat verifikasi menggunakan algoritma dan parameter yang sama dengan baseline. | Must Have |
| FR-021 | Sistem harus membandingkan hasil hash terkini dengan hash baseline. | Must Have |
| FR-022 | Sistem harus mengidentifikasi file yang berubah sebagai modified file. | Must Have |
| FR-023 | Sistem harus mengidentifikasi file baru sebagai added file. | Must Have |
| FR-024 | Sistem harus mengidentifikasi file yang hilang sebagai deleted file. | Must Have |
| FR-025 | Sistem harus menyimpan hasil verifikasi ke database. | Must Have |
| FR-026 | Sistem harus menampilkan ringkasan hasil verifikasi, termasuk jumlah unchanged, modified, added, dan deleted file. | Must Have |
| FR-027 | Sistem harus mencatat waktu mulai, waktu selesai, total file yang diperiksa, dan durasi verifikasi. | Must Have |

### 2.4 Deteksi Perubahan File

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-028 | Sistem harus menandai file sebagai `UNCHANGED` jika file ada pada baseline dan nilai hash sama. | Must Have |
| FR-029 | Sistem harus menandai file sebagai `MODIFIED` jika file ada pada baseline tetapi nilai hash berbeda. | Must Have |
| FR-030 | Sistem harus menandai file sebagai `ADDED` jika file ada pada kondisi terkini tetapi tidak ada pada baseline. | Must Have |
| FR-031 | Sistem harus menandai file sebagai `DELETED` jika file ada pada baseline tetapi tidak ditemukan pada kondisi terkini. | Must Have |
| FR-032 | Sistem harus menyimpan detail perubahan per file. | Must Have |
| FR-033 | Sistem dapat menyimpan metadata pembanding seperti ukuran lama, ukuran baru, modified time lama, dan modified time baru. | Should Have |

### 2.5 Alert

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-034 | Sistem harus membuat alert ketika ditemukan file dengan status `MODIFIED`, `ADDED`, atau `DELETED`. | Must Have |
| FR-035 | Sistem harus menampilkan daftar alert pada dashboard. | Must Have |
| FR-036 | Sistem harus memberikan severity default berdasarkan jenis perubahan. | Should Have |
| FR-037 | Sistem harus menyediakan status alert seperti `OPEN`, `ACKNOWLEDGED`, dan `RESOLVED`. | Should Have |
| FR-038 | Sistem harus menyediakan fitur untuk melihat detail alert. | Must Have |
| FR-039 | Sistem dapat menyediakan fitur acknowledge alert. | Could Have |
| FR-040 | Sistem harus mencatat pembuatan dan perubahan status alert ke log aktivitas. | Should Have |

Rekomendasi severity default:

| Jenis Perubahan | Severity |
| --- | --- |
| Modified | High |
| Deleted | High |
| Added | Medium |

### 2.6 Log Aktivitas

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-041 | Sistem harus menyimpan log aktivitas sistem. | Must Have |
| FR-042 | Log aktivitas harus mencatat jenis aktivitas, waktu, status, dan deskripsi. | Must Have |
| FR-043 | Sistem harus mencatat aktivitas konfigurasi direktori. | Must Have |
| FR-044 | Sistem harus mencatat aktivitas pembuatan baseline. | Must Have |
| FR-045 | Sistem harus mencatat aktivitas verifikasi integritas. | Must Have |
| FR-046 | Sistem harus mencatat aktivitas benchmark algoritma. | Must Have |
| FR-047 | Sistem harus menyediakan halaman untuk melihat log aktivitas. | Must Have |
| FR-048 | Sistem dapat menyediakan filter log berdasarkan tanggal, jenis aktivitas, dan status. | Should Have |

### 2.7 Benchmark Algoritma

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-049 | Sistem harus menyediakan fitur benchmark untuk SHA-256, PBKDF2, dan Argon2id. | Must Have |
| FR-050 | Sistem harus mengukur waktu eksekusi hashing per file. | Must Have |
| FR-051 | Sistem harus mengukur total waktu eksekusi per algoritma. | Must Have |
| FR-052 | Sistem harus mencatat ukuran file yang diproses. | Must Have |
| FR-053 | Sistem harus mencatat parameter algoritma PBKDF2, seperti iterasi, salt length, dan output length. | Must Have |
| FR-054 | Sistem harus mencatat parameter algoritma Argon2id, seperti memory cost, time cost, parallelism, salt length, dan output length. | Must Have |
| FR-055 | Sistem harus menyimpan hasil benchmark ke database. | Must Have |
| FR-056 | Sistem harus menampilkan tabel perbandingan hasil benchmark. | Must Have |
| FR-057 | Sistem dapat menampilkan grafik perbandingan durasi algoritma. | Should Have |
| FR-058 | Sistem dapat menghitung metrik throughput seperti MB/s. | Should Have |
| FR-059 | Sistem harus mencatat benchmark ke log aktivitas. | Must Have |

### 2.8 Dashboard dan Laporan

| ID | Requirement | Prioritas |
| --- | --- | --- |
| FR-060 | Sistem harus menyediakan dashboard ringkasan status monitoring. | Must Have |
| FR-061 | Dashboard harus menampilkan jumlah direktori monitoring aktif. | Should Have |
| FR-062 | Dashboard harus menampilkan baseline terakhir. | Must Have |
| FR-063 | Dashboard harus menampilkan verifikasi terakhir. | Must Have |
| FR-064 | Dashboard harus menampilkan jumlah alert terbuka. | Must Have |
| FR-065 | Sistem harus menyediakan halaman detail hasil verifikasi. | Must Have |
| FR-066 | Sistem dapat menyediakan fitur ekspor hasil benchmark ke CSV. | Could Have |
| FR-067 | Sistem dapat menyediakan fitur ekspor hasil verifikasi ke CSV. | Could Have |

---

## 3. Non Functional Requirements

### 3.1 Performance

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Sistem harus mampu memproses direktori penelitian berisi minimal 1.000 file kecil sampai sedang. | Minimal 1.000 file |
| NFR-002 | Proses hashing tidak boleh membekukan antarmuka web. | Proses berat dijalankan sebagai background job atau request terkontrol |
| NFR-003 | Sistem harus mencatat durasi proses baseline, verifikasi, dan benchmark. | Akurasi minimal milidetik |
| NFR-004 | Halaman dashboard harus dapat dimuat dalam waktu wajar untuk dataset penelitian. | Target kurang dari 3 detik pada data normal |

### 3.2 Reliability

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-005 | Sistem harus menjaga konsistensi data baseline dan hasil verifikasi. | Menggunakan transaksi database untuk proses penyimpanan penting |
| NFR-006 | Sistem harus menangani file yang tidak dapat dibaca tanpa menghentikan seluruh proses. | File error dicatat sebagai log atau status error |
| NFR-007 | Sistem harus menyimpan error detail ketika proses baseline, verifikasi, atau benchmark gagal. | Error tersimpan di log aktivitas |

### 3.3 Security

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-008 | Sistem harus membatasi akses path agar tidak membaca direktori sensitif di luar kebutuhan penelitian jika mode pembatasan diaktifkan. | Allowlist base directory direkomendasikan |
| NFR-009 | Sistem harus melakukan validasi input path direktori. | Path traversal dan path kosong ditolak |
| NFR-010 | Sistem tidak boleh menyimpan isi file ke database, hanya metadata dan hash. | Tidak ada konten file tersimpan |
| NFR-011 | Jika login sederhana diterapkan, password harus disimpan dalam bentuk hash, bukan plaintext. | Password hashing menggunakan algoritma aman |

### 3.4 Usability

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-012 | Antarmuka harus mudah digunakan untuk pengguna penelitian non-enterprise. | Navigasi utama jelas |
| NFR-013 | Sistem harus menampilkan status proses secara informatif. | Pending, running, completed, failed |
| NFR-014 | Sistem harus menampilkan pesan error yang dapat dipahami pengguna. | Pesan error ringkas dan jelas |

### 3.5 Maintainability

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-015 | Kode aplikasi nantinya harus dipisahkan antara layer controller/API, service, repository, dan UI. | Struktur modular |
| NFR-016 | Logika hashing dan benchmark harus ditempatkan dalam modul terpisah agar mudah diuji. | Modul crypto/hasher terisolasi |
| NFR-017 | Sistem harus menyediakan dokumentasi konfigurasi dan cara menjalankan aplikasi. | README atau dokumen instalasi |

### 3.6 Portability

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-018 | Sistem harus dapat berjalan pada sistem operasi umum untuk penelitian seperti Linux dan Windows. | Path handling lintas platform diperhatikan |
| NFR-019 | Database lokal ringan dapat digunakan untuk penelitian. | SQLite atau PostgreSQL direkomendasikan |

---

## 4. User Flow

### 4.1 Flow Utama Sistem

1. Pengguna membuka aplikasi web.
2. Pengguna melihat dashboard.
3. Pengguna menambahkan konfigurasi direktori monitoring.
4. Sistem memvalidasi path direktori.
5. Pengguna memilih algoritma hashing.
6. Pengguna membuat baseline.
7. Sistem membaca file secara rekursif dan menyimpan hash baseline.
8. Pengguna menjalankan verifikasi integritas.
9. Sistem membandingkan kondisi file terkini dengan baseline.
10. Sistem menampilkan hasil deteksi:
    - unchanged file,
    - modified file,
    - added file,
    - deleted file.
11. Sistem membuat alert untuk perubahan yang ditemukan.
12. Pengguna melihat detail alert dan hasil verifikasi.
13. Pengguna menjalankan benchmark algoritma.
14. Sistem menampilkan perbandingan performa SHA-256, PBKDF2, dan Argon2id.
15. Semua aktivitas penting tersimpan pada log aktivitas.

### 4.2 Flow Pembuatan Baseline

1. Pengguna memilih menu **Monitoring Directories**.
2. Pengguna memilih direktori yang sudah terdaftar.
3. Pengguna memilih algoritma:
   - SHA-256,
   - PBKDF2,
   - Argon2id.
4. Jika algoritma PBKDF2 dipilih, pengguna dapat mengatur parameter iterasi.
5. Jika algoritma Argon2id dipilih, pengguna dapat mengatur memory cost, time cost, dan parallelism.
6. Pengguna menekan tombol **Generate Baseline**.
7. Sistem memindai file dalam direktori.
8. Sistem menghitung hash dan metadata file.
9. Sistem menyimpan baseline.
10. Sistem menampilkan ringkasan baseline.

### 4.3 Flow Verifikasi Integritas

1. Pengguna memilih menu **Baselines**.
2. Pengguna memilih baseline yang ingin diverifikasi.
3. Pengguna menekan tombol **Run Verification**.
4. Sistem memindai ulang direktori target.
5. Sistem menghitung hash kondisi terkini.
6. Sistem membandingkan data terkini dengan baseline.
7. Sistem mengklasifikasikan status file.
8. Sistem menyimpan hasil verifikasi.
9. Sistem membuat alert jika ditemukan perubahan.
10. Sistem menampilkan ringkasan dan detail perubahan.

### 4.4 Flow Benchmark Algoritma

1. Pengguna memilih menu **Benchmark**.
2. Pengguna memilih direktori atau dataset file uji.
3. Pengguna memilih algoritma yang ingin dibandingkan.
4. Pengguna mengisi parameter benchmark untuk PBKDF2 dan Argon2id.
5. Pengguna menekan tombol **Run Benchmark**.
6. Sistem menjalankan hashing terhadap dataset uji.
7. Sistem mengukur durasi dan throughput.
8. Sistem menyimpan hasil benchmark.
9. Sistem menampilkan tabel dan grafik perbandingan.

---

## 5. Database Design

### 5.1 Entity Relationship Overview

Entitas utama sistem:

1. `monitoring_directories`
2. `baselines`
3. `baseline_files`
4. `verification_runs`
5. `verification_file_results`
6. `alerts`
7. `activity_logs`
8. `benchmark_runs`
9. `benchmark_results`

Relasi utama:

- Satu monitoring directory memiliki banyak baseline.
- Satu baseline memiliki banyak baseline file.
- Satu baseline memiliki banyak verification run.
- Satu verification run memiliki banyak verification file result.
- Satu verification run dapat menghasilkan banyak alert.
- Satu benchmark run memiliki banyak benchmark result.

### 5.2 Tabel `monitoring_directories`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID direktori monitoring |
| name | VARCHAR | Not Null | Nama konfigurasi |
| path | TEXT | Not Null | Path absolut direktori |
| is_active | BOOLEAN | Default true | Status aktif |
| created_at | DATETIME | Not Null | Waktu pembuatan |
| updated_at | DATETIME | Not Null | Waktu perubahan |

### 5.3 Tabel `baselines`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID baseline |
| monitoring_directory_id | UUID / BIGINT | Foreign Key | Referensi direktori monitoring |
| algorithm | VARCHAR | Not Null | SHA-256, PBKDF2, atau Argon2id |
| algorithm_params | JSON | Nullable | Parameter algoritma |
| total_files | INTEGER | Not Null | Jumlah file baseline |
| total_size_bytes | BIGINT | Not Null | Total ukuran file |
| started_at | DATETIME | Not Null | Waktu mulai |
| finished_at | DATETIME | Nullable | Waktu selesai |
| duration_ms | BIGINT | Nullable | Durasi proses |
| status | VARCHAR | Not Null | PENDING, RUNNING, COMPLETED, FAILED |
| error_message | TEXT | Nullable | Pesan error jika gagal |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

### 5.4 Tabel `baseline_files`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID file baseline |
| baseline_id | UUID / BIGINT | Foreign Key | Referensi baseline |
| relative_path | TEXT | Not Null | Path relatif file |
| file_size_bytes | BIGINT | Not Null | Ukuran file |
| last_modified_at | DATETIME | Nullable | Timestamp modifikasi file |
| hash_value | TEXT | Not Null | Nilai hash |
| hash_duration_ms | BIGINT | Nullable | Durasi hashing file |
| read_error | TEXT | Nullable | Error baca file jika ada |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

Index yang direkomendasikan:

- `idx_baseline_files_baseline_id`
- `idx_baseline_files_relative_path`
- Unique index pada `baseline_id` dan `relative_path`

### 5.5 Tabel `verification_runs`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID verifikasi |
| baseline_id | UUID / BIGINT | Foreign Key | Referensi baseline |
| started_at | DATETIME | Not Null | Waktu mulai |
| finished_at | DATETIME | Nullable | Waktu selesai |
| duration_ms | BIGINT | Nullable | Durasi proses |
| total_scanned_files | INTEGER | Default 0 | Jumlah file terkini yang dipindai |
| unchanged_count | INTEGER | Default 0 | Jumlah unchanged |
| modified_count | INTEGER | Default 0 | Jumlah modified |
| added_count | INTEGER | Default 0 | Jumlah added |
| deleted_count | INTEGER | Default 0 | Jumlah deleted |
| status | VARCHAR | Not Null | PENDING, RUNNING, COMPLETED, FAILED |
| error_message | TEXT | Nullable | Pesan error jika gagal |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

### 5.6 Tabel `verification_file_results`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID hasil file |
| verification_run_id | UUID / BIGINT | Foreign Key | Referensi verifikasi |
| relative_path | TEXT | Not Null | Path relatif file |
| status | VARCHAR | Not Null | UNCHANGED, MODIFIED, ADDED, DELETED, ERROR |
| baseline_hash | TEXT | Nullable | Hash dari baseline |
| current_hash | TEXT | Nullable | Hash saat verifikasi |
| baseline_size_bytes | BIGINT | Nullable | Ukuran file baseline |
| current_size_bytes | BIGINT | Nullable | Ukuran file terkini |
| baseline_modified_at | DATETIME | Nullable | Modified time baseline |
| current_modified_at | DATETIME | Nullable | Modified time terkini |
| hash_duration_ms | BIGINT | Nullable | Durasi hashing file saat verifikasi |
| error_message | TEXT | Nullable | Error jika ada |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

Index yang direkomendasikan:

- `idx_verification_results_run_id`
- `idx_verification_results_status`
- `idx_verification_results_relative_path`

### 5.7 Tabel `alerts`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID alert |
| verification_run_id | UUID / BIGINT | Foreign Key | Referensi verifikasi |
| verification_file_result_id | UUID / BIGINT | Foreign Key | Referensi hasil file |
| alert_type | VARCHAR | Not Null | FILE_MODIFIED, FILE_ADDED, FILE_DELETED |
| severity | VARCHAR | Not Null | LOW, MEDIUM, HIGH, CRITICAL |
| title | VARCHAR | Not Null | Judul alert |
| message | TEXT | Not Null | Detail alert |
| status | VARCHAR | Not Null | OPEN, ACKNOWLEDGED, RESOLVED |
| created_at | DATETIME | Not Null | Waktu alert dibuat |
| acknowledged_at | DATETIME | Nullable | Waktu acknowledge |
| resolved_at | DATETIME | Nullable | Waktu resolved |

### 5.8 Tabel `activity_logs`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID log |
| activity_type | VARCHAR | Not Null | DIRECTORY, BASELINE, VERIFICATION, ALERT, BENCHMARK |
| action | VARCHAR | Not Null | CREATE, UPDATE, RUN, COMPLETE, FAIL, ACKNOWLEDGE |
| status | VARCHAR | Not Null | INFO, SUCCESS, WARNING, ERROR |
| description | TEXT | Not Null | Deskripsi aktivitas |
| reference_type | VARCHAR | Nullable | Jenis entitas terkait |
| reference_id | UUID / BIGINT | Nullable | ID entitas terkait |
| metadata | JSON | Nullable | Data tambahan |
| created_at | DATETIME | Not Null | Waktu log dibuat |

### 5.9 Tabel `benchmark_runs`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID benchmark |
| monitoring_directory_id | UUID / BIGINT | Nullable Foreign Key | Direktori dataset uji |
| dataset_path | TEXT | Nullable | Path dataset jika tidak menggunakan konfigurasi direktori |
| total_files | INTEGER | Default 0 | Jumlah file diuji |
| total_size_bytes | BIGINT | Default 0 | Total ukuran dataset |
| started_at | DATETIME | Not Null | Waktu mulai |
| finished_at | DATETIME | Nullable | Waktu selesai |
| duration_ms | BIGINT | Nullable | Total durasi benchmark |
| status | VARCHAR | Not Null | PENDING, RUNNING, COMPLETED, FAILED |
| error_message | TEXT | Nullable | Pesan error jika gagal |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

### 5.10 Tabel `benchmark_results`

| Kolom | Tipe | Constraint | Keterangan |
| --- | --- | --- | --- |
| id | UUID / BIGINT | Primary Key | ID hasil benchmark |
| benchmark_run_id | UUID / BIGINT | Foreign Key | Referensi benchmark run |
| algorithm | VARCHAR | Not Null | SHA-256, PBKDF2, Argon2id |
| algorithm_params | JSON | Nullable | Parameter algoritma |
| file_count | INTEGER | Not Null | Jumlah file diproses algoritma ini |
| total_size_bytes | BIGINT | Not Null | Total ukuran file |
| total_duration_ms | BIGINT | Not Null | Total durasi algoritma |
| average_duration_ms | DECIMAL | Nullable | Rata-rata durasi per file |
| throughput_mb_per_sec | DECIMAL | Nullable | Throughput |
| min_duration_ms | DECIMAL | Nullable | Durasi minimum per file |
| max_duration_ms | DECIMAL | Nullable | Durasi maksimum per file |
| created_at | DATETIME | Not Null | Waktu pembuatan record |

---

## 6. API Design

### 6.1 Prinsip API

- API menggunakan gaya REST.
- Format request dan response menggunakan JSON.
- Response standar menyertakan `success`, `message`, dan `data`.
- Endpoint proses berat seperti baseline, verifikasi, dan benchmark dapat mengembalikan job/run ID agar status dapat dipantau.

Contoh struktur response sukses:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

Contoh struktur response error:

```json
{
  "success": false,
  "message": "Directory path is invalid",
  "errors": []
}
```

### 6.2 Endpoint Dashboard

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/dashboard/summary` | Mengambil ringkasan dashboard |

Response data yang direkomendasikan:

```json
{
  "activeDirectories": 1,
  "latestBaseline": {},
  "latestVerification": {},
  "openAlerts": 3,
  "latestBenchmark": {}
}
```

### 6.3 Endpoint Monitoring Directories

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/monitoring-directories` | Mengambil daftar direktori monitoring |
| POST | `/api/monitoring-directories` | Menambahkan direktori monitoring |
| GET | `/api/monitoring-directories/{id}` | Mengambil detail direktori monitoring |
| PUT | `/api/monitoring-directories/{id}` | Mengubah konfigurasi direktori monitoring |
| DELETE | `/api/monitoring-directories/{id}` | Menghapus atau menonaktifkan direktori monitoring |
| POST | `/api/monitoring-directories/validate-path` | Memvalidasi path direktori |

Contoh request `POST /api/monitoring-directories`:

```json
{
  "name": "Dataset Skripsi",
  "path": "/home/user/dataset-fim",
  "isActive": true
}
```

### 6.4 Endpoint Baseline

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/baselines` | Mengambil daftar baseline |
| POST | `/api/baselines` | Membuat baseline baru |
| GET | `/api/baselines/{id}` | Mengambil detail baseline |
| GET | `/api/baselines/{id}/files` | Mengambil daftar file baseline |
| DELETE | `/api/baselines/{id}` | Menghapus baseline |

Contoh request `POST /api/baselines`:

```json
{
  "monitoringDirectoryId": "directory-id",
  "algorithm": "SHA-256",
  "algorithmParams": {}
}
```

Contoh request baseline PBKDF2:

```json
{
  "monitoringDirectoryId": "directory-id",
  "algorithm": "PBKDF2",
  "algorithmParams": {
    "iterations": 100000,
    "saltLength": 16,
    "outputLength": 32
  }
}
```

Contoh request baseline Argon2id:

```json
{
  "monitoringDirectoryId": "directory-id",
  "algorithm": "Argon2id",
  "algorithmParams": {
    "memoryCostKb": 65536,
    "timeCost": 3,
    "parallelism": 2,
    "saltLength": 16,
    "outputLength": 32
  }
}
```

### 6.5 Endpoint Verification

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/verifications` | Mengambil daftar verifikasi |
| POST | `/api/verifications` | Menjalankan verifikasi terhadap baseline |
| GET | `/api/verifications/{id}` | Mengambil detail verifikasi |
| GET | `/api/verifications/{id}/results` | Mengambil detail hasil per file |

Contoh request `POST /api/verifications`:

```json
{
  "baselineId": "baseline-id"
}
```

Query filter untuk hasil file:

```text
GET /api/verifications/{id}/results?status=MODIFIED&page=1&limit=50
```

### 6.6 Endpoint Alerts

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/alerts` | Mengambil daftar alert |
| GET | `/api/alerts/{id}` | Mengambil detail alert |
| PATCH | `/api/alerts/{id}/acknowledge` | Menandai alert sebagai acknowledged |
| PATCH | `/api/alerts/{id}/resolve` | Menandai alert sebagai resolved |

Query filter:

```text
GET /api/alerts?status=OPEN&severity=HIGH&page=1&limit=20
```

### 6.7 Endpoint Activity Logs

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/activity-logs` | Mengambil daftar log aktivitas |
| GET | `/api/activity-logs/{id}` | Mengambil detail log aktivitas |

Query filter:

```text
GET /api/activity-logs?activityType=BASELINE&status=SUCCESS&from=2026-01-01&to=2026-01-31
```

### 6.8 Endpoint Benchmark

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/benchmarks` | Mengambil daftar benchmark |
| POST | `/api/benchmarks` | Menjalankan benchmark baru |
| GET | `/api/benchmarks/{id}` | Mengambil detail benchmark |
| GET | `/api/benchmarks/{id}/results` | Mengambil hasil benchmark per algoritma |
| GET | `/api/benchmarks/{id}/export` | Mengekspor hasil benchmark ke CSV jika fitur ekspor diterapkan |

Contoh request `POST /api/benchmarks`:

```json
{
  "monitoringDirectoryId": "directory-id",
  "algorithms": ["SHA-256", "PBKDF2", "Argon2id"],
  "params": {
    "PBKDF2": {
      "iterations": 100000,
      "saltLength": 16,
      "outputLength": 32
    },
    "Argon2id": {
      "memoryCostKb": 65536,
      "timeCost": 3,
      "parallelism": 2,
      "saltLength": 16,
      "outputLength": 32
    }
  }
}
```

---

## 7. Folder Structure

Struktur folder berikut direkomendasikan untuk implementasi aplikasi web yang modular. Struktur ini bersifat arsitektural dan belum mengikat pada framework tertentu.

```text
project-root/
├── docs/
│   ├── SRS.md
│   ├── architecture.md
│   └── user-guide.md
├── backend/
│   ├── src/
│   │   ├── config/
│   │   │   ├── database.config
│   │   │   └── app.config
│   │   ├── controllers/
│   │   │   ├── dashboard.controller
│   │   │   ├── monitoring-directory.controller
│   │   │   ├── baseline.controller
│   │   │   ├── verification.controller
│   │   │   ├── alert.controller
│   │   │   ├── activity-log.controller
│   │   │   └── benchmark.controller
│   │   ├── services/
│   │   │   ├── monitoring-directory.service
│   │   │   ├── baseline.service
│   │   │   ├── verification.service
│   │   │   ├── alert.service
│   │   │   ├── activity-log.service
│   │   │   └── benchmark.service
│   │   ├── repositories/
│   │   │   ├── monitoring-directory.repository
│   │   │   ├── baseline.repository
│   │   │   ├── verification.repository
│   │   │   ├── alert.repository
│   │   │   ├── activity-log.repository
│   │   │   └── benchmark.repository
│   │   ├── modules/
│   │   │   ├── file-scanner/
│   │   │   │   ├── file-scanner
│   │   │   │   └── path-validator
│   │   │   ├── hashing/
│   │   │   │   ├── sha256-hasher
│   │   │   │   ├── pbkdf2-hasher
│   │   │   │   ├── argon2id-hasher
│   │   │   │   └── hashing.types
│   │   │   ├── fim/
│   │   │   │   ├── baseline-generator
│   │   │   │   ├── integrity-verifier
│   │   │   │   └── change-classifier
│   │   │   └── benchmark/
│   │   │       ├── benchmark-runner
│   │   │       └── benchmark-calculator
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   ├── seeders/
│   │   │   └── schema
│   │   ├── middlewares/
│   │   │   ├── error-handler
│   │   │   └── request-logger
│   │   ├── utils/
│   │   │   ├── timer
│   │   │   ├── response-builder
│   │   │   └── csv-exporter
│   │   └── app
│   └── tests/
│       ├── unit/
│       └── integration/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard
│   │   │   ├── MonitoringDirectories
│   │   │   ├── Baselines
│   │   │   ├── Verifications
│   │   │   ├── Alerts
│   │   │   ├── ActivityLogs
│   │   │   └── Benchmarks
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── tables/
│   │   │   ├── charts/
│   │   │   ├── forms/
│   │   │   └── alerts/
│   │   ├── services/
│   │   │   ├── api-client
│   │   │   ├── dashboard-api
│   │   │   ├── monitoring-directory-api
│   │   │   ├── baseline-api
│   │   │   ├── verification-api
│   │   │   ├── alert-api
│   │   │   ├── activity-log-api
│   │   │   └── benchmark-api
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── utils/
│   │   └── main
│   └── tests/
├── storage/
│   ├── exports/
│   └── temp/
├── README.md
└── .env.example
```

### 7.1 Penjelasan Folder Utama

| Folder | Fungsi |
| --- | --- |
| `docs/` | Menyimpan dokumentasi proyek seperti SRS, arsitektur, dan panduan pengguna. |
| `backend/` | Menyimpan kode server, API, service, repository, modul hashing, dan database. |
| `frontend/` | Menyimpan kode antarmuka web. |
| `storage/exports/` | Menyimpan file ekspor seperti CSV hasil benchmark atau verifikasi. |
| `storage/temp/` | Menyimpan file sementara jika diperlukan. |

### 7.2 Modul Backend Penting

| Modul | Tanggung Jawab |
| --- | --- |
| `file-scanner` | Membaca daftar file secara rekursif dari direktori target. |
| `path-validator` | Memvalidasi path direktori dan mencegah input path tidak valid. |
| `sha256-hasher` | Menghasilkan hash SHA-256. |
| `pbkdf2-hasher` | Menghasilkan output PBKDF2 untuk kebutuhan baseline/benchmark penelitian. |
| `argon2id-hasher` | Menghasilkan output Argon2id untuk kebutuhan baseline/benchmark penelitian. |
| `baseline-generator` | Mengatur proses pembuatan baseline. |
| `integrity-verifier` | Mengatur proses verifikasi integritas file. |
| `change-classifier` | Mengklasifikasikan file menjadi unchanged, modified, added, atau deleted. |
| `benchmark-runner` | Menjalankan benchmark algoritma. |
| `benchmark-calculator` | Menghitung metrik benchmark seperti rata-rata durasi dan throughput. |

---

## 8. Acceptance Criteria

### 8.1 Baseline

- Sistem berhasil membuat baseline dari direktori valid.
- Sistem menyimpan minimal path relatif, ukuran file, modified time, algoritma, parameter algoritma, dan hash file.
- Sistem menampilkan jumlah file dan durasi baseline.

### 8.2 Verifikasi

- Sistem dapat mendeteksi file yang dimodifikasi.
- Sistem dapat mendeteksi file yang ditambahkan.
- Sistem dapat mendeteksi file yang dihapus.
- Sistem dapat menampilkan ringkasan hasil verifikasi.
- Sistem membuat alert untuk perubahan file.

### 8.3 Benchmark

- Sistem dapat menjalankan benchmark SHA-256, PBKDF2, dan Argon2id.
- Sistem menyimpan durasi setiap algoritma.
- Sistem menampilkan perbandingan hasil benchmark dalam tabel.
- Sistem mencatat parameter PBKDF2 dan Argon2id yang digunakan.

### 8.4 Logging

- Setiap proses baseline, verifikasi, benchmark, dan alert tercatat dalam log aktivitas.
- Log dapat dilihat melalui halaman aplikasi atau endpoint API.

---

## 9. Rekomendasi Prioritas Implementasi

### Fase 1: Core FIM

1. Konfigurasi direktori monitoring.
2. Scanner file rekursif.
3. Hash SHA-256.
4. Generate baseline.
5. Verifikasi integritas.
6. Deteksi modified, added, dan deleted file.
7. Log aktivitas dasar.

### Fase 2: Alert dan Dashboard

1. Dashboard ringkasan.
2. Alert perubahan file.
3. Detail hasil verifikasi.
4. Filter log aktivitas.

### Fase 3: Benchmark Penelitian

1. Implementasi PBKDF2.
2. Implementasi Argon2id.
3. Benchmark tiga algoritma.
4. Tabel dan grafik perbandingan.
5. Ekspor CSV jika diperlukan.

### Fase 4: Penyempurnaan

1. Validasi path yang lebih ketat.
2. Background job untuk proses berat.
3. Dokumentasi instalasi dan penggunaan.
4. Unit test untuk scanner, hasher, classifier, dan benchmark calculator.
