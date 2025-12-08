# MangaDex Downloader WebApp

## 📋 Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Chạy WebApp](#chạy-webapp)
- [Tính năng](#tính-năng)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Changelog](#changelog)

---

## 🎯 Giới thiệu

Web interface hiện đại cho MangaDex Downloader với đầy đủ tính năng search, filter, và download manga từ MangaDex.

**Công nghệ**: FastAPI + HTML5 + JavaScript (Vanilla)  
**Port**: `http://localhost:8000`

---

## 📦 Cài đặt

### Requirements
```bash
pip install -r requirements.txt
```

### Dependencies chính
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `mangadex-downloader` - Core library

---

## 🚀 Chạy WebApp

```powershell
# Windows PowerShell
cd c:\mangadex-downloader
python run_web.py
```

```bash
# Linux/Mac
cd /path/to/mangadex-downloader
python run_web.py
```

Truy cập: **http://localhost:8000**

---

## ✨ Tính năng

### 1. Search & Filter
- ✅ **Search by Title** - Tìm manga theo tên
- ✅ **Search by Author/Artist** - Tìm theo tác giả hoặc họa sĩ
- ✅ **Autocomplete Suggestions** ⭐ - Gợi ý tự động khi gõ
- ✅ **Tags Filtering** ⭐ - Lọc theo thể loại (Action, Romance, etc.)
  - Include tags - Chỉ hiện manga có tags này
  - Exclude tags - Loại bỏ manga có tags này
- ✅ **Status Filter** - Ongoing, Completed, Hiatus, Cancelled
- ✅ **Language Filter** - 20+ ngôn ngữ
- ✅ **Content Rating** - Safe, Suggestive, Erotica, Pornographic

### 2. Pagination
- ✅ Page numbers với ellipsis (...)
- ✅ Previous/Next buttons
- ✅ Configurable results per page (1-100)
- ✅ Offset-based pagination

### 3. Manga Details
- ✅ Cover image display
- ✅ Title, author, artist info
- ✅ Description/synopsis
- ✅ Tags/genres list
- ✅ Status và publication info
- ✅ Chapter count

### 4. Download
- ✅ **Folder Picker** ⭐ - Browse để chọn thư mục save
- ✅ **Auto Manga Folders** ⭐ - Tự động tạo folder riêng cho mỗi manga
- ✅ Multiple format support (PDF, EPUB, CBZ, RAW)
- ✅ Chapter range selection
- ✅ Download progress tracking
- ✅ Job management (check status, view results)

---

## 🔧 API Reference

### Search Endpoints

#### `GET /api/search/manga`
Search manga với filters và pagination

**Parameters:**
- `title` (string, optional) - Tên manga
- `author` (string, optional) - Tên tác giả
- `artist` (string, optional) - Tên họa sĩ
- `includedTags` (string, optional) - Comma-separated tag IDs
- `excludedTags` (string, optional) - Comma-separated tag IDs ⭐
- `status` (string, optional) - ongoing, completed, hiatus, cancelled
- `language` (string, optional) - Language code
- `contentRating` (array, optional) - safe, suggestive, erotica, pornographic
- `limit` (int, default: 12) - Results per page
- `offset` (int, default: 0) - Pagination offset

**Response:**
```json
{
  "data": [...],
  "total": 123,
  "limit": 12,
  "offset": 0
}
```

#### `GET /api/search/suggestions`
Autocomplete suggestions ⭐

**Parameters:**
- `q` (string, required, min 2 chars) - Search query
- `type` (string, required) - "manga" hoặc "author"

**Response:**
```json
{
  "suggestions": [
    {"id": "...", "title": "ONE PIECE"},
    {"id": "...", "title": "One Punch Man"}
  ]
}
```

#### `GET /api/search/tags`
Lấy tất cả tags/genres ⭐

**Response:**
```json
{
  "data": [
    {
      "id": "...",
      "name": "Action",
      "group": "genre"
    }
  ]
}
```

#### `GET /api/search/languages`
Lấy danh sách languages

#### `GET /api/search/authors`
Search authors

#### `GET /api/search/artists`
Search artists

### Manga Endpoints

#### `GET /api/manga/{manga_id}`
Chi tiết manga

#### `GET /api/manga/{manga_id}/chapters`
Danh sách chapters

**Parameters:**
- `language` (string, optional)
- `limit` (int, default: 100)
- `offset` (int, default: 0)

### Download Endpoints

#### `POST /api/url/download`
Start download job

**Body:**
```json
{
  "url": "https://mangadex.org/title/...",
  "path": "C:\\Downloads",
  "format": "pdf",
  "range": "1-10"
}
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "running"
}
```

#### `GET /api/url/jobs/{job_id}`
Check download status

**Response:**
```json
{
  "status": "completed",
  "message": "Download completed! Files saved in separate manga folder.",
  "output": "..."
}
```

---

## 🎨 Features Deep Dive

### Autocomplete Suggestions
**Hoạt động:**
1. Gõ ít nhất 2 ký tự vào Title/Author/Artist field
2. Sau 300ms debounce, API sẽ fetch suggestions
3. Dropdown hiện top 10 gợi ý
4. Click để chọn

**Tech Details:**
- Debounced 300ms để tránh spam API calls
- Sử dụng MangaDex API với relevance ordering
- Support cả manga titles và author names

### Tags Filtering (Include + Exclude)
**Hoạt động:**
1. Click "Select Tags" button
2. Modal mở với 2 tabs: **Include** và **Exclude** ⭐
3. **Include tab**: Chọn tags muốn tìm (Action, Romance, etc.)
   - Manga **PHẢI** có tất cả tags này
4. **Exclude tab**: Chọn tags muốn loại bỏ (Gore, Sexual Content, etc.)
   - Manga **KHÔNG ĐƯỢC** có bất kỳ tag nào này
5. Tags hiển thị dưới dạng colored badges (xanh = include, đỏ = exclude)
6. Click X để remove tag

**Tech Details:**
- Backend: `includedTags[]` và `excludedTags[]` parameters
- MangaDex API: AND logic cho included, OR logic cho excluded
- Frontend: Tab switching, color-coded badges

### Folder Picker & Auto Folders
**Hoạt động:**
1. Download tab → Save Directory
2. Click "Browse" button → Folder picker dialog ⭐
3. Chọn thư mục từ OS folder picker
4. Hoặc nhập path thủ công vào input field
5. Download → Files tự động tạo subfolder theo tên manga ⭐

**Folder Structure:**
```
C:\Downloads\
  ├── One Piece\
  │   ├── Chapter 1.pdf
  │   ├── Chapter 2.pdf
  │   └── Chapter 3.pdf
  └── Naruto\
      ├── Chapter 1.pdf
      └── Chapter 2.pdf
```

**Tech Details:**
- HTML5 `<input type="file" webkitdirectory>` cho folder picker
- Chrome/Edge/Opera support
- Fallback: Manual text input
- Backend: `--use-chapter-title` flag auto-creates manga folder

---

## 🐛 Troubleshooting

### Server không start
**Lỗi**: `Address already in use`

**Giải pháp:**
```powershell
# Kill process trên port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Hoặc đổi port
python run_web.py --port 8080
```

### Autocomplete không hoạt động
**Lỗi**: Dropdown không xuất hiện

**Checklist:**
- ✅ Gõ ít nhất 2 ký tự
- ✅ Đợi 300ms
- ✅ Check browser console (F12) có errors
- ✅ Test API: `/api/search/suggestions?q=one&type=manga`

### Tags modal không load
**Lỗi**: "Loading tags..." không biến mất

**Giải pháp:**
1. Check browser console (F12)
2. Test API: `/api/search/tags`
3. Restart server nếu 404/500
4. Hard refresh (Ctrl+F5)

### Folder picker không hoạt động
**Lỗi**: Folder picker không hiện

**Giải pháp:**
- Firefox không support `webkitdirectory`
- Dùng Chrome, Edge, hoặc Opera
- Hoặc nhập path thủ công vào input field

### Download không tạo folder riêng
**Lỗi**: Files download vào flat directory

**Checklist:**
- ✅ Verify `--use-chapter-title` flag trong code
- ✅ Check `webapp/routers/url.py` line ~30
- ✅ Restart server sau khi edit

### Include/Exclude tags không filter đúng
**Lỗi**: Kết quả không đúng với tags đã chọn

**Giải pháp:**
- MangaDex API có thể return ít kết quả với nhiều filters
- Thử giảm số lượng included tags
- Exclude tags có thể filter quá mạnh
- Test với 1-2 tags trước

---

## 🧪 Testing Guide

### Test Autocomplete
```
1. Search tab → Title field
2. Gõ "one"
3. ✅ Dropdown xuất hiện: "ONE PIECE", "One Punch Man", etc.
4. Click "ONE PIECE"
5. ✅ Title field filled
```

### Test Tags Include/Exclude
```
1. Click "Select Tags"
2. ✅ Modal mở với 2 tabs: Include, Exclude
3. Include tab → Check "Action", "Adventure"
4. Exclude tab → Check "Gore", "Sexual Content"
5. Click "Done"
6. ✅ 2 green badges (Action, Adventure) + 2 red badges (Gore, Sexual Content)
7. Search → Verify results
8. ✅ Results có Action + Adventure, KHÔNG có Gore hoặc Sexual Content
```

### Test Folder Picker
```
1. Download tab
2. Save Directory → Click "Browse"
3. ✅ Folder picker dialog xuất hiện
4. Chọn folder: C:\Downloads
5. ✅ Path filled vào input
6. Download manga
7. ✅ Check folder: C:\Downloads\{Manga Title}\
```

---

## 📊 Performance

| Operation | Time | Note |
|-----------|------|------|
| Page load | ~2s | Initial load |
| Tags load | ~1s | First modal open |
| Autocomplete | ~500ms | 300ms debounce + API |
| Search (no filters) | ~800ms | MangaDex API |
| Search (with tags) | ~1-2s | More filtering |
| Download start | <100ms | Job creation |

---

## 📝 Changelog

### v2.1.1 (Current) ⭐
- ✅ **Exclude Tags** - Loại bỏ manga có tags không mong muốn
- ✅ **Folder Picker** - Browse button để chọn thư mục
- ✅ **Improved Tags UI** - Tabs Include/Exclude với color-coded badges
- ✅ **Better Path Validation** - Validate folder path trước khi download
- ✅ **Cleanup Documentation** - Dọn dẹp files .txt cũ vào `docs_archive/`

### v2.1.0
- ✅ Autocomplete suggestions (title/author/artist)
- ✅ Tags filtering (include only)
- ✅ Auto manga folders on download

### v2.0.0
- ✅ Fixed cover image display
- ✅ Fixed pagination
- ✅ Fixed author/artist search
- ✅ Added folder browse button

---

## 🚀 Development

### Project Structure
```
mangadex-downloader/
├── webapp/
│   ├── main.py           # FastAPI app entry
│   ├── routers/
│   │   ├── search.py     # Search endpoints
│   │   ├── manga.py      # Manga endpoints
│   │   └── url.py        # Download endpoints
│   └── templates/
│       └── index.html    # Frontend UI
├── mangadex_downloader/  # Core library
├── docs/                 # Official docs
├── docs_archive/         # Old docs ⭐
├── run_web.py           # WebApp launcher
└── requirements.txt
```

### Adding New Features

1. **Backend**: Edit `webapp/routers/*.py`
2. **Frontend**: Edit `webapp/templates/index.html`
3. **Test**: Restart server + Ctrl+F5
4. **Document**: Update this README

### Code Style
- Backend: FastAPI best practices
- Frontend: Vanilla JS (no frameworks)
- Comments: Vietnamese OK trong Vietnamese projects

---

## 📞 Support

**Issues**: [GitHub Issues](https://github.com/HoangThinh2024/mangadex-downloader/issues)  
**Docs**: `docs/` folder  
**CLI Reference**: `docs/cli_ref/`

---

**Version**: 2.1.1  
**Last Updated**: December 8, 2025  
**Status**: Production Ready ✅
