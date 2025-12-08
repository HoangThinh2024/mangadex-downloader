# MangaDex Downloader Web API

**Phiên bản:** 1.0.0  
**Framework:** FastAPI + MangaDex Downloader  
**Trạng thái:** ✅ Hoàn toàn tính năng

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [API Endpoints](#api-endpoints)
- [Ví dụ sử dụng](#ví-dụ-sử-dụng)

## ✨ Tính năng

### 🔍 Tìm kiếm & Lọc
- ✅ Tìm kiếm manga theo tiêu đề
- ✅ Lọc theo tác giả, họa sĩ
- ✅ Lọc theo trạng thái (đang tiếp tục, hoàn thành, tạm dừng)
- ✅ Lọc theo ngôn ngữ, xếp hạng nội dung
- ✅ Tìm kiếm tác giả và họa sĩ

### 📖 Thông tin Manga
- ✅ Xem chi tiết manga (tiêu đề, mô tả, tác giả, họa sĩ)
- ✅ Danh sách chapters với từng trang
- ✅ Lấy ảnh bìa manga
- ✅ Thông tin nhóm dịch (scanlation group)

### ⬇️ Tải về
- ✅ Tải manga từ URL
- ✅ Chọn định dạng (PDF, EPUB, CBZ, RAW, 7ZIP)
- ✅ Chọn chapters cụ thể
- ✅ Chọn nhóm dịch cụ thể
- ✅ Theo dõi tiến độ tải xuống real-time

### ⚙️ Cấu hình
- ✅ Lấy cấu hình hiện tại
- ✅ Cập nhật cấu hình
- ✅ Quản lý ngôn ngữ, định dạng, đường dẫn

## 🚀 Cài đặt

### Tùy chọn 1: Tự động (Khuyên dùng)
```bash
.\install-uv.ps1
```

### Tùy chọn 2: uv Sync (Manual)
```bash
uv sync
.\.venv\Scripts\Activate.ps1
```

### Tùy chọn 3: Không cần kích hoạt
```bash
uv run python .\run_web.py
```

### Tùy chọn 4: Pip truyền thống
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-uv.txt
```

## ▶️ Chạy ứng dụng

```bash
python .\run_web.py
```

Truy cập: **http://localhost:8000**

### Tài liệu API Interactive
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API Endpoints

### 🔍 Search - Tìm kiếm

#### Search Manga
```http
GET /api/search/manga?title=One+Piece&limit=10&offset=0
```

**Parameters:**
- `title` (string): Tên manga
- `authors` (string[]): ID tác giả
- `artists` (string[]): ID họa sĩ
- `year` (integer): Năm xuất bản
- `status` (string): `ongoing`, `completed`, `hiatus`, `cancelled`
- `languages` (string[]): Mã ngôn ngữ (e.g., `en`, `ja`, `zh`)
- `tags` (string[]): ID thẻ
- `excluded_tags` (string[]): ID thẻ loại trừ
- `content_rating` (string[]): `safe`, `suggestive`, `erotica`, `pornographic`
- `limit` (int): 1-100 (mặc định: 10)
- `offset` (int): Số trang (mặc định: 0)

**Response:**
```json
{
  "total": 15,
  "limit": 10,
  "offset": 0,
  "data": [
    {
      "id": "uuid",
      "title": "One Piece",
      "description": "...",
      "status": "ongoing",
      "year": 1997,
      "content_rating": "safe",
      "cover": "https://...",
      "last_volume": "104",
      "last_chapter": "1234"
    }
  ]
}
```

#### Search Authors
```http
GET /api/search/authors?name=Eiichiro+Oda&limit=10
```

#### Search Artists
```http
GET /api/search/artists?name=Eiichiro+Oda&limit=10
```

### 📖 Manga - Thông tin Manga

#### Get Manga Details
```http
GET /api/manga/{manga_id}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "One Piece",
  "description": "...",
  "status": "ongoing",
  "year": 1997,
  "cover": "https://...",
  "authors": [
    {
      "id": "uuid",
      "name": "Eiichiro Oda"
    }
  ],
  "artists": [...],
  "original_language": "ja",
  "alt_titles": {...}
}
```

#### Get Manga Chapters
```http
GET /api/manga/{manga_id}/chapters?language=en&limit=50&offset=0
```

**Response:**
```json
{
  "manga_id": "uuid",
  "total": 1234,
  "chapters": [
    {
      "id": "uuid",
      "volume": "1",
      "chapter": "1",
      "title": "Chapter 1: Dawn",
      "language": "en",
      "pages": 20,
      "groups": [
        {
          "id": "uuid",
          "name": "Scanlation Group"
        }
      ]
    }
  ]
}
```

#### Get Manga Feed (Latest Chapters)
```http
GET /api/manga/{manga_id}/feed?language=en&limit=20
```

### 🖼️ Covers - Ảnh bìa

#### Get Manga Covers
```http
GET /api/covers/manga/{manga_id}?limit=10
```

**Response:**
```json
{
  "manga_id": "uuid",
  "total": 5,
  "covers": [
    {
      "id": "uuid",
      "file_name": "filename.png",
      "volume": "1",
      "cover_url": "https://..."
    }
  ]
}
```

#### Get Cover Image
```http
GET /api/covers/{cover_id}/image?size=256
```

**Response:**
```json
{
  "id": "uuid",
  "manga_id": "uuid",
  "url": "https://...",
  "256px": "https://....256.jpg",
  "512px": "https://....512.jpg"
}
```

### 👥 Groups - Nhóm dịch

#### Get Group Info
```http
GET /api/groups/{group_id}
```

#### List Groups
```http
GET /api/groups?limit=10&offset=0
```

#### Get Manga Groups
```http
GET /api/manga/{manga_id}/groups
```

### 👤 Authors & Artists

#### Get Author Info
```http
GET /api/authors/{author_id}
```

#### Get Artist Info
```http
GET /api/artists/{artist_id}
```

### ⬇️ Download - Tải xuống

#### Start Download
```http
POST /api/url/download
Content-Type: application/json

{
  "url": "https://mangadex.org/title/...",
  "save_as": "pdf",
  "path": "./downloads",
  "chapters": "1-10",
  "start_chapter": "1",
  "end_chapter": "10",
  "start_page": 1,
  "end_page": 20,
  "language": "en",
  "groups": "group-id",
  "no_track": false,
  "log_level": "info"
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

#### Check Download Status
```http
GET /api/url/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "running",
  "manga_title": "One Piece",
  "progress": "Downloaded 5/10 chapters",
  "message": "Processing chapter 1...",
  "error": null,
  "created_at": "2024-01-01T12:00:00",
  "completed_at": null
}
```

#### Legacy Download (Simple)
```http
POST /api/download
Content-Type: application/json

{
  "url": "https://mangadex.org/title/..."
}
```

### ⚙️ Config - Cấu hình

#### Get Config
```http
GET /api/config
```

**Response:**
```json
{
  "language": "en",
  "save_as": "pdf",
  "path": "./downloads",
  "replace": false,
  "no_track": false,
  "use_alt_details": false,
  "log_level": "info",
  "cover": "best"
}
```

#### Update Config
```http
PUT /api/config
Content-Type: application/json

{
  "language": "en",
  "save_as": "epub",
  "path": "./my-manga"
}
```

### ❤️ Health Check
```http
GET /health
```

## 💻 Ví dụ sử dụng

### PowerShell

#### Tìm kiếm
```powershell
$search = Invoke-RestMethod -Uri "http://localhost:8000/api/search/manga?title=one+piece&limit=5"
$search.data | Format-Table title, status, year
```

#### Tải xuống
```powershell
$download = Invoke-RestMethod -Uri "http://localhost:8000/api/url/download" `
  -Method Post `
  -ContentType "application/json" `
  -Body (@{
    url = "https://mangadex.org/title/..."
    save_as = "pdf"
  } | ConvertTo-Json)

$jobId = $download.job_id

# Kiểm tra trạng thái
Invoke-RestMethod -Uri "http://localhost:8000/api/url/jobs/$jobId"
```

### cURL

#### Tìm kiếm
```bash
curl "http://localhost:8000/api/search/manga?title=one+piece&limit=5"
```

#### Tải xuống
```bash
curl -X POST "http://localhost:8000/api/url/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://mangadex.org/title/...",
    "save_as": "pdf"
  }'
```

### Python

```python
import requests
import json

BASE = "http://localhost:8000"

# Tìm kiếm
search = requests.get(f"{BASE}/api/search/manga", params={
    "title": "One Piece",
    "limit": 10
}).json()

print(f"Found {search['total']} manga")
for manga in search['data']:
    print(f"- {manga['title']} ({manga['status']})")

# Tải xuống
response = requests.post(f"{BASE}/api/url/download", json={
    "url": "https://mangadex.org/title/...",
    "save_as": "pdf"
})

job_id = response.json()['job_id']
print(f"Job ID: {job_id}")

# Kiểm tra trạng thái
status = requests.get(f"{BASE}/api/url/jobs/{job_id}").json()
print(f"Status: {status['status']}")
```

### JavaScript/Node.js

```javascript
const BASE = "http://localhost:8000";

// Tìm kiếm
async function searchManga(title) {
  const res = await fetch(`${BASE}/api/search/manga?title=${title}&limit=10`);
  const data = await res.json();
  return data;
}

// Tải xuống
async function downloadManga(url) {
  const res = await fetch(`${BASE}/api/url/download`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, save_as: "pdf" })
  });
  return await res.json();
}

// Sử dụng
searchManga("One Piece").then(data => {
  console.log(`Found ${data.total} results`);
  data.data.forEach(m => console.log(`- ${m.title}`));
});
```

## 📊 Tính năng nâng cao

### Lọc theo nhiều điều kiện

```http
GET /api/search/manga?title=manga&status=ongoing&content_rating=safe&languages=en,ja&limit=20
```

### Tìm kiếm theo thẻ

```http
GET /api/search/manga?tags=Action,Adventure&excluded_tags=Hentai
```

### Lấy chi tiết đầy đủ

```http
GET /api/manga/{id}?includes=author,artist,cover_art
```

### Theo dõi tải xuống

Mỗi lần tải xuống trả về `job_id` có thể dùng để theo dõi tiến độ:

```javascript
const pollStatus = async (jobId) => {
  const res = await fetch(`/api/url/jobs/${jobId}`);
  const status = await res.json();
  
  if (status.status === 'done') {
    console.log('Complete!');
  } else if (status.status === 'error') {
    console.error(status.error);
  } else {
    console.log(`${status.status}: ${status.message}`);
    setTimeout(() => pollStatus(jobId), 1500);
  }
};
```

## 🛠️ Khắc phục sự cố

### Lỗi: "Module not found"
```bash
uv sync --fresh
```

### Lỗi: "Port in use"
Chỉnh sửa `run_web.py`, đổi `port=8000` thành `port=8001`

### Lỗi: "Connection refused"
Đảm bảo server đang chạy: `python .\run_web.py`

### Lỗi: "Manga not found"
Kiểm tra ID manga đúng ở https://mangadex.org

## 📚 Tài liệu thêm

- [MangaDex API Docs](https://api.mangadex.org/docs)
- [MangaDex Downloader Docs](https://mangadex-downloader.readthedocs.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## 📄 Giấy phép

MIT - Xem LICENSE

## 👨‍💼 Tác giả

- **MangaDex Downloader Core**: Rahman Yusuf
- **Web Interface**: Copilot
