# Playwright Python Automation Project

---

## ✅ Requirements

กรุณาติดตั้งสิ่งเหล่านี้ก่อน

* Python **3.9 ขึ้นไป**
* Git

เช็กเวอร์ชัน Python

```bash
python --version
or
python3 --version
```

---

## 📦 วิธีติดตั้ง (ครั้งแรก)

### 1️⃣ Clone โปรเจกต์

```bash
git clone https://github.com/TeerasakChaisin/Playwright-Python.git
cd Playwright-Python
```

---

### 2️⃣ สร้าง Virtual Environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3️⃣ ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ ติดตั้ง Playwright Browser

```bash
playwright install
```

---

## ▶️ วิธีรัน Test

$env:ENV="DEV";
$env:ENV="UAT"; 
$env:ENV="PRD"; 



รันทั้งหมด

```bash
$env:ENV="DEV"; pytest
```

รันเฉพาะไฟล์

```bash
$env:ENV="DEV"; pytest src/tests/test_example.py
```

รันเฉพาะ case

```bash
$env:ENV="DEV"; pytest -k member_white_5000 -v
```

DEBUG Mode

```bash
$env:PWDEBUG="1"; pytest pytest -k member_white_5000 -v
```

Headed Mode

```bash
$env:ENV="DEV"; pytest --headed -k member_white_5000 -v
```

View Print

```bash
$env:ENV="DEV"; pytest -s -k AT- -v 
```

---

## 📁 โครงสร้างโปรเจกต์

```
Playwright-Python/
├── src/
│   ├── pages/        # Page Object
│   ├── tests/        # Test cases
│   ├── utils/        # Helper / Utils
│   └── apis/         # API helpers (ถ้ามี)
│
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🔐 Environment Variable (ถ้ามี)

สร้างไฟล์ `.env` ที่ root project

```env
BASE_URL=https://example.com
USERNAME=
PASSWORD=
```

> ❗ ไฟล์ `.env` **ไม่ถูก commit ขึ้น git**

---

## ⚠️ สิ่งที่ไม่ต้อง commit ขึ้น Git

รายการด้านล่างถูก ignore แล้ว

* `.venv/`
* test-results /
* reports /
* traces /
* `.env`

ถ้ามีปัญหาให้เช็ก `.gitignore` ก่อนเสมอ

---

## 🧠 Troubleshooting

### ❌ รันไม่ได้ / Browser ไม่ขึ้น

ให้รัน

```bash
playwright install
```

### ❌ Import error

ตรวจสอบว่า activate virtualenv แล้ว

```bash
which python
```

---

## 📌 หมายเหตุสำหรับทีม

* ห้าม commit `.venv`
* ห้าม hardcode username / password
* ใช้ Page Object ทุกหน้า

---

UPDATE PROJECT

1) สำรองโค้ดที่แก้ไว้ (เผื่อ rollback)
git stash

เก็บไฟล์ .env (ทำครั้งเดียว)
git update-index --skip-worktree .env
ยกเลิก
git update-index --no-skip-worktree .env

2) Update project
2.1) ดึงโค้ดล่าสุด
git pull origin main

2.2) ดึงโค้ดล่าสุดจาก GitHub แบบทับทั้งหมด
git fetch origin
git reset --hard origin/main

หมายเหตุ:
คำสั่งนี้จะทำให้โค้ดในเครื่องเหมือน GitHub 100%
ไฟล์ที่เคยแก้จะถูกลบทิ้งทั้งหมด

3) ลบ stash (ถ้าไม่ต้องการ rollback แล้ว)
git stash drop

4) ติดตั้ง dependencies ใหม่ (ถ้า requirements.txt เปลี่ยน)
pip install -r requirements.txt

5) ติดตั้ง/อัปเดต Playwright browser (ถ้า playwright version เปลี่ยน)
playwright install

--