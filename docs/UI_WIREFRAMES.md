# UI/UX Wireframe Design

## Aplikasi Web File Integrity Monitoring (FIM)

Dokumen ini mendefinisikan wireframe dashboard dan halaman utama aplikasi File Integrity Monitoring (FIM). Peran dokumen ini adalah sebagai panduan UI/UX sebelum implementasi frontend. Dokumen ini tidak berisi kode.

---

## 1. Design Direction

### 1.1 Gaya Visual

Aplikasi menggunakan gaya visual:

- **Modern**: layout berbasis card, grid rapi, spacing konsisten, dan visual hierarchy jelas.
- **Clean**: menghindari elemen berlebihan, fokus pada data penting, dan menggunakan whitespace yang cukup.
- **Cyber Security**: warna gelap profesional, aksen cyan/blue/green, status severity yang jelas, dan nuansa monitoring/security operation.
- **Professional**: tabel informatif, filter lengkap, state proses jelas, dan navigasi mudah dipahami.

### 1.2 Rekomendasi Tema Warna

| Elemen | Warna | Keterangan |
| --- | --- | --- |
| Background utama | `#0F172A` | Navy gelap profesional. |
| Surface/card | `#111827` atau `#1E293B` | Panel konten. |
| Border | `#334155` | Batas halus antar elemen. |
| Primary accent | `#38BDF8` | Cyan untuk aksi utama. |
| Success | `#22C55E` | Status aman/valid. |
| Warning | `#F59E0B` | Perhatian. |
| Danger | `#EF4444` | Modified/deleted/high severity. |
| Text utama | `#F8FAFC` | Kontras tinggi. |
| Text sekunder | `#94A3B8` | Metadata dan helper text. |

### 1.3 Komponen UI Global

| Komponen | Fungsi |
| --- | --- |
| Sidebar Navigation | Navigasi utama ke Dashboard, Directory Monitoring, Baseline Manager, Verification, Benchmark, Logs, dan Settings. |
| Top Header | Menampilkan judul halaman, breadcrumb, status backend, dan waktu terakhir refresh. |
| Summary Card | Menampilkan metrik penting secara ringkas. |
| Status Badge | Menampilkan status seperti Active, Completed, Modified, Added, Deleted, Open, Resolved. |
| Data Table | Menampilkan data monitoring, baseline, logs, dan benchmark. |
| Filter Bar | Filter berdasarkan direktori, status, tanggal, algoritma, severity. |
| Action Button | Tombol aksi utama seperti Generate Baseline, Run Verification, Run Benchmark. |
| Empty State | Tampilan saat belum ada data. |
| Loading State | Tampilan saat proses scan, baseline, verifikasi, atau benchmark berjalan. |
| Toast/Notification | Feedback singkat setelah aksi berhasil atau gagal. |

### 1.4 Layout Global Aplikasi

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Top Header: Breadcrumb | Page Title | Backend Status | Last Refresh        │
├───────────────┬────────────────────────────────────────────────────────────┤
│ Sidebar       │ Main Content                                               │
│               │                                                            │
│ Dashboard     │ Page-specific summary, filters, table, charts, forms        │
│ Directories   │                                                            │
│ Baselines     │                                                            │
│ Verification  │                                                            │
│ Benchmark     │                                                            │
│ Logs          │                                                            │
│ Settings      │                                                            │
└───────────────┴────────────────────────────────────────────────────────────┘
```

---

## 2. Dashboard Page

### 2.1 Tujuan Halaman

Dashboard berfungsi sebagai pusat ringkasan kondisi sistem FIM. Pengguna dapat melihat status direktori monitoring, baseline terakhir, hasil verifikasi terakhir, alert perubahan file, dan ringkasan benchmark.

### 2.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Dashboard                                                          │
│ Subtitle: File Integrity Monitoring Overview                               │
├────────────────────────────────────────────────────────────────────────────┤
│ [Active Directories] [Baseline Files] [Open Alerts] [Last Verification]    │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Integrity Status Panel        │ Recent Security Events                     │
│                               │                                            │
│ Donut/Status Summary          │ - MODIFIED /etc/app/config.json            │
│ Unchanged | Modified | Added  │ - ADDED uploads/shell.php                  │
│ Deleted | Error               │ - DELETED docs/readme.txt                  │
│                               │                                            │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Latest Verification Summary                                                │
│ Directory | Algorithm | Checked At | Unchanged | Modified | Added | Deleted│
├────────────────────────────────────────────────────────────────────────────┤
│ Benchmark Snapshot                                                         │
│ SHA-256 duration | PBKDF2 duration | Argon2id duration | Fastest Algorithm │
├────────────────────────────────────────────────────────────────────────────┤
│ Quick Actions                                                              │
│ [Add Directory] [Generate Baseline] [Run Verification] [Run Benchmark]     │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Header | Page title + subtitle | Menjelaskan bahwa halaman adalah overview FIM. |
| Summary cards | 4 kartu metrik | Active directories, total baseline files, open alerts, last verification time. |
| Integrity status | Chart/panel | Distribusi status file: unchanged, modified, added, deleted, error. |
| Recent security events | Event list | Log perubahan terbaru dengan severity badge. |
| Latest verification | Compact table | Ringkasan verifikasi terakhir per direktori. |
| Benchmark snapshot | Metric cards | Perbandingan durasi algoritma terakhir. |
| Quick actions | Button group | Aksi cepat menuju halaman operasional. |

### 2.4 UX Notes

- Open alerts dan modified/deleted files harus paling mudah terlihat.
- Jika belum ada baseline, tampilkan empty state dengan CTA **Generate First Baseline**.
- Warna merah hanya digunakan untuk kondisi berisiko agar tidak kehilangan makna visual.

---

## 3. Directory Monitoring Page

### 3.1 Tujuan Halaman

Halaman Directory Monitoring digunakan untuk menambahkan, melihat, memvalidasi, mengaktifkan, dan menonaktifkan direktori yang dipantau.

### 3.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Directory Monitoring                         [Add Directory]       │
├────────────────────────────────────────────────────────────────────────────┤
│ Filter Bar                                                                 │
│ Search directory/name | Status: All/Active/Inactive | [Apply]             │
├────────────────────────────────────────────────────────────────────────────┤
│ Directory Table                                                            │
│ ┌────┬──────────────┬──────────────────────┬────────┬──────────┬────────┐ │
│ │ ID │ Name         │ Path                 │ Status │ Last Scan│ Action │ │
│ ├────┼──────────────┼──────────────────────┼────────┼──────────┼────────┤ │
│ │ 1  │ Dataset FIM  │ /home/user/dataset   │ Active │ 10:30    │ ...    │ │
│ └────┴──────────────┴──────────────────────┴────────┴──────────┴────────┘ │
├────────────────────────────────────────────────────────────────────────────┤
│ Right/Modal Form: Add or Edit Directory                                    │
│ Name                                                                       │
│ Absolute Path                                                              │
│ Description                                                                │
│ [Validate Path] [Save Directory]                                           │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Header | Title + Add Directory button | Tombol utama untuk membuka form tambah direktori. |
| Filter bar | Search + status filter | Memudahkan pencarian direktori. |
| Directory table | Data table | ID, name, path, status, last scan, total files, action. |
| Action menu | Dropdown/action buttons | View detail, validate path, activate, deactivate, delete. |
| Form panel/modal | Input form | Name, absolute path, description, active status. |

### 3.4 UX Notes

- Path direktori harus ditampilkan dengan monospace font agar mudah dibaca.
- Validasi path harus memiliki feedback visual: valid, invalid, permission denied.
- Untuk penelitian lokal, pengguna perlu diberi catatan bahwa path harus dapat diakses oleh backend FastAPI.

---

## 4. Baseline Manager Page

### 4.1 Tujuan Halaman

Baseline Manager digunakan untuk menghasilkan baseline hash dari direktori terpilih dan melihat daftar file baseline.

### 4.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Baseline Manager                         [Generate Baseline]       │
├────────────────────────────────────────────────────────────────────────────┤
│ Baseline Configuration Panel                                               │
│ Directory: [Select Directory]                                              │
│ Algorithm: [SHA-256 ▼]                                                     │
│ Parameters: dynamic fields for PBKDF2 / Argon2id                           │
│ [Generate Baseline]                                                        │
├────────────────────────────────────────────────────────────────────────────┤
│ Baseline Summary Cards                                                     │
│ [Total Files] [Total Size] [Algorithm] [Duration] [Created At]             │
├────────────────────────────────────────────────────────────────────────────┤
│ Baseline Files Table                                                       │
│ Search file | Algorithm filter | [Export optional]                         │
│ ┌────┬────────────────────┬────────────┬───────────┬──────────┬─────────┐ │
│ │ No │ Relative Path      │ Size       │ Algorithm │ Hash     │ Time ms │ │
│ └────┴────────────────────┴────────────┴───────────┴──────────┴─────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Configuration panel | Form baseline | Directory selector, algorithm selector, parameter fields. |
| Parameter fields | Conditional form | PBKDF2: iterations, salt length, dklen. Argon2id: time cost, memory cost, parallelism, hash length. |
| Summary cards | Baseline metrics | Total files, total size, selected algorithm, duration, timestamp. |
| Files table | Data table | Relative path, size, last modified, algorithm, hash prefix/full hash toggle, hash duration. |

### 4.4 UX Notes

- Hash value panjang sebaiknya dipotong dengan opsi copy full hash.
- Saat baseline berjalan, tampilkan progress state atau loading indicator.
- Parameter algoritma harus memiliki default value dari system settings.

---

## 5. Verification Page

### 5.1 Tujuan Halaman

Verification digunakan untuk menjalankan pemeriksaan integritas file berdasarkan baseline dan menampilkan hasil deteksi file modified, added, deleted, unchanged, atau error.

### 5.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Integrity Verification                    [Run Verification]       │
├────────────────────────────────────────────────────────────────────────────┤
│ Verification Control Panel                                                 │
│ Directory: [Select Directory] | Algorithm: [Auto from baseline]            │
│ Baseline Date: [Latest ▼]                                                  │
│ [Run Verification]                                                         │
├────────────────────────────────────────────────────────────────────────────┤
│ Result Summary                                                             │
│ [Unchanged] [Modified] [Added] [Deleted] [Errors] [Duration]               │
├────────────────────────────────────────────────────────────────────────────┤
│ Severity / Event Distribution                                              │
│ Left: Bar chart by event type        Right: Open findings list             │
├────────────────────────────────────────────────────────────────────────────┤
│ Verification Result Table                                                  │
│ Filter: Event Type | Severity | Status | Search Path                       │
│ ┌────┬───────────┬────────────────────┬──────────┬────────────┬─────────┐ │
│ │ No │ Event     │ Relative Path      │ Severity │ Checked At │ Action  │ │
│ └────┴───────────┴────────────────────┴──────────┴────────────┴─────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Control panel | Verification form | Directory selector, baseline selector, run button. |
| Result summary | Status cards | Unchanged, modified, added, deleted, errors, duration. |
| Distribution area | Chart + findings | Visualisasi status dan daftar temuan prioritas tinggi. |
| Result table | Data table | Event type, relative path, previous hash, current hash, severity, status, checked at. |
| Detail drawer/modal | Finding detail | Menampilkan previous/current metadata dan hash comparison. |

### 5.4 UX Notes

- Event `MODIFIED` dan `DELETED` harus diberi visual emphasis lebih kuat daripada `ADDED`.
- Filter event type harus mudah digunakan karena halaman ini menjadi halaman investigasi utama.
- Klik row membuka detail perubahan file agar hash lama dan baru dapat dibandingkan.

---

## 6. Benchmark Page

### 6.1 Tujuan Halaman

Benchmark digunakan untuk membandingkan performa SHA-256, PBKDF2, dan Argon2id pada dataset file yang dipilih.

### 6.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Algorithm Benchmark                         [Run Benchmark]        │
├────────────────────────────────────────────────────────────────────────────┤
│ Benchmark Configuration                                                    │
│ Directory/Dataset: [Select Directory]                                      │
│ Algorithms: [x] SHA-256 [x] PBKDF2 [x] Argon2id                            │
│ PBKDF2 Params: Iterations | Salt Length | DK Length                        │
│ Argon2id Params: Time Cost | Memory Cost | Parallelism | Hash Length       │
│ [Run Benchmark]                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ Benchmark Summary                                                          │
│ [Fastest] [Slowest] [Total Files] [Total Size] [Total Duration]            │
├────────────────────────────────────────────────────────────────────────────┤
│ Benchmark Charts                                                           │
│ Left: Duration Comparison Bar Chart                                        │
│ Right: Throughput MB/s Comparison                                          │
├────────────────────────────────────────────────────────────────────────────┤
│ Benchmark Result Table                                                     │
│ ┌───────────┬────────────┬──────────────┬────────────┬────────┬─────────┐ │
│ │ Algorithm │ Total Time │ Avg/File     │ Throughput │ Params │ Export  │ │
│ └───────────┴────────────┴──────────────┴────────────┴────────┴─────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Configuration | Benchmark form | Dataset selector, algorithm checkbox, parameter fields. |
| Summary | Metric cards | Fastest algorithm, slowest algorithm, total files, total size, total duration. |
| Charts | Bar/line charts | Total duration, average duration, throughput. |
| Result table | Data table | Algorithm, params, total files, total size, duration, average, min, max, throughput. |

### 6.4 UX Notes

- Parameter PBKDF2 dan Argon2id harus diberi helper text karena memengaruhi waktu proses.
- Hasil benchmark harus mudah dibandingkan secara visual.
- Gunakan warna konsisten per algoritma, contoh SHA-256 biru, PBKDF2 ungu, Argon2id hijau.

---

## 7. Logs Page

### 7.1 Tujuan Halaman

Logs digunakan untuk melihat aktivitas sistem dan hasil integritas secara historis. Halaman ini membantu audit penelitian dan investigasi perubahan file.

### 7.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Logs                                          [Export Logs]        │
├────────────────────────────────────────────────────────────────────────────┤
│ Filter Bar                                                                 │
│ Date Range | Directory | Event Type | Severity | Status | Search Path      │
│ [Apply Filter] [Reset]                                                     │
├────────────────────────────────────────────────────────────────────────────┤
│ Log Summary                                                                │
│ [Total Logs] [Open] [High Severity] [Modified] [Added] [Deleted]           │
├────────────────────────────────────────────────────────────────────────────┤
│ Logs Table                                                                 │
│ ┌────┬────────────┬───────────┬────────────┬──────────┬────────┬────────┐ │
│ │ No │ Time       │ Event     │ Path       │ Severity │ Status │ Detail │ │
│ └────┴────────────┴───────────┴────────────┴──────────┴────────┴────────┘ │
├────────────────────────────────────────────────────────────────────────────┤
│ Log Detail Drawer                                                          │
│ Previous Hash | Current Hash | Previous Size | Current Size | Message      │
└────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Detail Komponen

| Area | Komponen | Isi |
| --- | --- | --- |
| Filter bar | Advanced filters | Date range, directory, event type, severity, status, path keyword. |
| Summary | Log cards | Total logs, open logs, high severity, modified, added, deleted. |
| Logs table | Data table | Time, event, path, severity, status, message preview, detail action. |
| Detail drawer | Detail panel | Hash comparison, metadata comparison, message, checked time. |

### 7.4 UX Notes

- Logs harus mendukung pencarian path karena data file bisa banyak.
- Severity dan event type harus diberi badge warna.
- Detail drawer lebih baik daripada pindah halaman agar investigasi cepat.

---

## 8. Settings Page

### 8.1 Tujuan Halaman

Settings digunakan untuk mengatur konfigurasi default sistem, parameter algoritma, dan preferensi scanning.

### 8.2 Layout Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Header: Settings                                                           │
├────────────────────────────────────────────────────────────────────────────┤
│ Settings Tabs                                                              │
│ [General] [Hashing Defaults] [Scanning] [Benchmark]                        │
├────────────────────────────────────────────────────────────────────────────┤
│ General Tab                                                                │
│ Application Name                                                           │
│ Default Directory Base Path                                                │
│ Theme Preference                                                           │
│ [Save Changes]                                                             │
├────────────────────────────────────────────────────────────────────────────┤
│ Hashing Defaults Tab                                                       │
│ Default Algorithm: [SHA-256 ▼]                                             │
│ PBKDF2 Iterations | Salt Length | DK Length                                │
│ Argon2id Time Cost | Memory Cost | Parallelism | Hash Length               │
│ [Save Hashing Settings]                                                    │
├────────────────────────────────────────────────────────────────────────────┤
│ Scanning Tab                                                               │
│ Scan Hidden Files [toggle]                                                 │
│ Max File Size MB                                                           │
│ Excluded Extensions                                                        │
│ [Save Scanning Settings]                                                   │
└────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Detail Komponen

| Tab | Field | Fungsi |
| --- | --- | --- |
| General | Application name | Nama aplikasi pada header. |
| General | Default base path | Base directory yang direkomendasikan untuk validasi path. |
| General | Theme preference | Dark mode sebagai default. |
| Hashing Defaults | Default algorithm | Algoritma default untuk baseline. |
| Hashing Defaults | PBKDF2 parameters | Default iterations, salt length, dan output length. |
| Hashing Defaults | Argon2id parameters | Default time cost, memory cost, parallelism, dan hash length. |
| Scanning | Scan hidden files | Menentukan hidden file ikut dipindai atau tidak. |
| Scanning | Max file size MB | Batas ukuran file yang diproses. |
| Scanning | Excluded extensions | Ekstensi yang dikecualikan dari scan. |
| Benchmark | Default algorithms | Algoritma yang otomatis dipilih saat benchmark. |

### 8.4 UX Notes

- Settings yang berpengaruh pada performa harus diberi warning/help text.
- Tombol save dibuat per section agar perubahan lebih terkontrol.
- Jika field berasal dari `system_settings`, tampilkan value type atau helper text agar jelas.

---

## 9. Navigation Structure

### 9.1 Sidebar Menu

```text
┌──────────────────────┐
│ FIM Security Monitor │
├──────────────────────┤
│ ▣ Dashboard          │
│ ▣ Directories        │
│ ▣ Baselines          │
│ ▣ Verification       │
│ ▣ Benchmark          │
│ ▣ Logs               │
│ ▣ Settings           │
└──────────────────────┘
```

### 9.2 Informasi Header Global

| Elemen | Fungsi |
| --- | --- |
| Breadcrumb | Membantu orientasi halaman. |
| Page title | Menampilkan nama halaman aktif. |
| Backend status | Menunjukkan API online/offline. |
| Last refresh | Menunjukkan kapan data terakhir diperbarui. |
| Refresh button | Memuat ulang data halaman. |

---

## 10. Responsive Behavior

### 10.1 Desktop

- Sidebar permanen di kiri.
- Konten menggunakan grid 12 kolom.
- Summary cards tampil 4 sampai 6 kolom per baris.
- Tabel menggunakan horizontal scrolling jika kolom terlalu banyak.

### 10.2 Tablet

- Sidebar dapat collapse.
- Summary cards tampil 2 kolom.
- Form dan chart ditumpuk vertikal jika ruang terbatas.

### 10.3 Mobile

- Sidebar berubah menjadi drawer.
- Summary cards tampil 1 kolom.
- Tabel menggunakan compact mode atau card list.
- Aksi utama tetap terlihat sebagai sticky action button jika diperlukan.

---

## 11. Empty, Loading, and Error States

### 11.1 Empty State

| Halaman | Empty State | CTA |
| --- | --- | --- |
| Dashboard | Belum ada data monitoring. | Add Directory |
| Directory Monitoring | Belum ada direktori. | Add Directory |
| Baseline Manager | Belum ada baseline. | Generate Baseline |
| Verification | Belum ada hasil verifikasi. | Run Verification |
| Benchmark | Belum ada benchmark. | Run Benchmark |
| Logs | Belum ada log. | Run Verification |
| Settings | Setting belum tersedia. | Load Default Settings |

### 11.2 Loading State

- Gunakan skeleton loader untuk tabel dan cards.
- Gunakan progress indicator untuk proses baseline, verification, dan benchmark.
- Disable tombol aksi saat proses sedang berjalan.

### 11.3 Error State

- Error path invalid: tampilkan inline error pada form direktori.
- Error permission denied: tampilkan warning dengan rekomendasi perbaikan permission.
- Error hashing/benchmark: tampilkan detail ringkas dan simpan ke logs.

---

## 12. Prioritas Implementasi UI

### Fase 1: Core Monitoring UI

1. Dashboard.
2. Directory Monitoring.
3. Baseline Manager.
4. Verification.

### Fase 2: Research and Audit UI

1. Benchmark.
2. Logs.
3. Export button jika diperlukan.

### Fase 3: Configuration UI

1. Settings.
2. Parameter defaults.
3. Responsive refinement.

---

## 13. Catatan Final UI/UX

1. UI harus memprioritaskan keterbacaan hasil integritas file.
2. Status `MODIFIED`, `ADDED`, dan `DELETED` harus konsisten secara warna dan label pada semua halaman.
3. Dashboard harus menjadi halaman ringkasan, sedangkan Verification dan Logs menjadi halaman investigasi detail.
4. Benchmark harus menonjolkan perbandingan algoritma secara visual karena penting untuk kebutuhan penelitian skripsi.
5. Settings harus sederhana dan tidak terlihat seperti konfigurasi enterprise yang kompleks.
