# KHẮC PHỤC LỖI PAGINATION & CÁC TÍNH NĂNG

## ❌ CÁC VẤN ĐỀ ĐÃ PHÁT HIỆN

### 1. Pagination không hoạt động
- **Nguyên nhân**: JavaScript luôn gửi `title=` (empty string) ngay cả khi không nhập title
- **Hậu quả**: API không vào logic search by author/artist
- **Fix**: Chỉ append title vào params khi title có giá trị

### 2. Offset không được gửi
- **Nguyên nhân**: JavaScript không append `offset` parameter khi chuyển trang
- **Hậu quả**: Luôn hiển thị trang 1, không load kết quả trang 2+
- **Fix**: Thêm `params.append('offset', (currentPage - 1) * limit)`

### 3. Languages endpoint sai URL
- **URL hiện tại**: `/api/languages` (404 Not Found)
- **URL đúng**: `/api/search/languages`
- **Fix**: Cập nhật documentation

---

## ✅ ĐÃ SỬA

### File: `webapp/templates/index.html`

#### Fix #1: Chỉ gửi title khi có giá trị
```javascript
// TRƯỚC (SAI):
params.append('title', currentSearchParams.title);  // Gửi cả empty string

// SAU (ĐÚNG):
if (currentSearchParams.title) params.append('title', currentSearchParams.title);
```

#### Fix #2: Thêm offset parameter cho pagination
```javascript
// THÊM MỚI:
params.append('offset', (currentPage - 1) * currentSearchParams.limit);
```

**Vị trí**: Dòng 804-815 trong `webapp/templates/index.html`

---

## 🧪 CÁCH TEST

### Test 1: Search với nhiều kết quả (Pagination)
```
1. Mở http://localhost:8000
2. Search tab → Nhập "of" → Click Search
3. ✅ Kỳ vọng: Hiển thị "Found 13,331 manga | Showing page 1"
4. ✅ Kỳ vọng: Hiển thị nút Previous (disabled), 1, 2, 3, 4, 5, ..., Next
5. Click nút "2"
6. ✅ Kỳ vọng: Load 12 kết quả mới, hiển thị "Showing page 2"
7. ✅ Kỳ vọng: URL request: /api/search/manga?title=of&limit=12&offset=12
```

### Test 2: Search by Author (Không cần title)
```
1. Search tab → Để trống Title
2. Author field → Nhập "Oda"
3. Click Search
4. ✅ Kỳ vọng: Tìm thấy 2 manga của các tác giả họ Oda
5. ✅ Kỳ vọng: Không có lỗi "Title required"
6. ✅ Kỳ vọng: URL request: /api/search/manga?authors=Oda&limit=12&offset=0
   (Không có title= trong URL)
```

### Test 3: Search by Artist
```
1. Search tab → Để trống Title & Author
2. Artist field → Nhập "Oda"
3. Click Search
4. ✅ Kỳ vọng: Tìm manga của artist
5. ✅ Kỳ vọng: URL request: /api/search/manga?artists=Oda&limit=12&offset=0
```

### Test 4: Pagination với Author Search
```
1. Search tab → Title: "the" (nhiều kết quả)
2. Click Search
3. ✅ Kỳ vọng: Hiển thị > 12 results, pagination xuất hiện
4. Click page 2
5. ✅ Kỳ vọng: Offset=12 được gửi
6. ✅ Kỳ vọng: Load 12 kết quả mới
```

---

## 📊 API ENDPOINTS ĐÚNG

| Endpoint | Mô tả | Ví dụ |
|----------|-------|-------|
| `/api/search/manga` | Tìm manga | `?title=One+Piece&limit=12&offset=0` |
| `/api/search/manga` | Tìm by author | `?authors=Oda&limit=12&offset=0` |
| `/api/search/manga` | Pagination page 2 | `?title=of&limit=12&offset=12` |
| `/api/search/manga` | Pagination page 3 | `?title=of&limit=12&offset=24` |
| `/api/search/languages` | Lấy 60 ngôn ngữ | (không có params) |
| `/api/manga/{id}` | Chi tiết manga | `/api/manga/a1c7c817-4e59-43b7...` |
| `/api/manga/{id}/chapters` | Danh sách chapter | `?limit=50` |

---

## 🔍 DEBUG TRONG BROWSER

### Mở Browser Console (F12)
```javascript
// Check pagination được gọi:
console.log('Pagination setup called for total:', totalResults);

// Check offset được gửi:
console.log('Current page:', currentPage);
console.log('Offset:', (currentPage - 1) * limit);

// Check response từ API:
console.log('API Response:', data);
console.log('Total results:', data.total);
console.log('Results count:', data.results.length);
```

### Kiểm tra Network Tab (F12)
```
1. Mở F12 → Tab "Network"
2. Search "of" → Click Search
3. Tìm request: "manga?title=of&limit=12&offset=0"
4. Click vào request
5. Xem Response:
   {
     "results": [...12 items...],
     "total": 13331,
     "limit": 12,
     "offset": 0
   }
6. Click page 2
7. Tìm request mới: "manga?title=of&limit=12&offset=12"
8. Xem Response: offset = 12, kết quả khác page 1
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Server phải được RESTART sau khi sửa code:
```powershell
# Kill server hiện tại
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force

# Start server mới
cd c:\mangadex-downloader
python run_web.py
# hoặc
uvicorn webapp.app:app --host 0.0.0.0 --port 8000
```

### Browser phải REFRESH sau khi sửa HTML:
```
Ctrl + F5 (Hard refresh - xóa cache)
hoặc
Ctrl + Shift + R
```

---

## 📝 CHECKLIST SỬA LỖI

✅ **HTML JavaScript**: Thêm `offset` parameter  
✅ **HTML JavaScript**: Chỉ gửi `title` khi có giá trị  
✅ **Documentation**: Cập nhật URL `/api/search/languages`  
⏳ **Server**: Cần restart  
⏳ **Browser**: Cần hard refresh (Ctrl+F5)  
⏳ **Test**: Cần verify pagination hoạt động  

---

## 🎯 KẾT QUẢ KỲ VỌNG SAU KHI SỬA

### Pagination:
- ✅ Hiển thị nút page 1, 2, 3, 4, 5...
- ✅ Click page 2 → Load 12 kết quả mới
- ✅ Offset được gửi đúng: page 2 = offset 12, page 3 = offset 24
- ✅ Tổng số trang = ceil(total / limit)

### Search by Author/Artist:
- ✅ Không cần nhập title
- ✅ Tìm được manga của author/artist
- ✅ URL không có `title=` (empty)

### API Response:
- ✅ Trả về `total`, `limit`, `offset`, `results[]`
- ✅ `total` = tổng số manga tìm được
- ✅ `results.length` = limit (hoặc ít hơn nếu page cuối)

---

## 🚀 CÁCH VERIFY FIX THÀNH CÔNG

```powershell
# 1. Restart server
cd c:\mangadex-downloader
python -m uvicorn webapp.app:app --host 0.0.0.0 --port 8000

# 2. Test API trực tiếp
# Test pagination page 1
Invoke-WebRequest "http://localhost:8000/api/search/manga?title=of&limit=12&offset=0"

# Test pagination page 2
Invoke-WebRequest "http://localhost:8000/api/search/manga?title=of&limit=12&offset=12"

# Test search by author
Invoke-WebRequest "http://localhost:8000/api/search/manga?authors=Oda&limit=5"

# 3. Kiểm tra kết quả khác nhau giữa page 1 và page 2
```

**Nếu đúng:**
- Page 1 offset=0 → Kết quả A, B, C, D...
- Page 2 offset=12 → Kết quả M, N, O, P... (khác page 1)

---

## 📞 HỖ TRỢ

Nếu vẫn không hoạt động:

1. **Kiểm tra console log (F12)**
   - Có lỗi JavaScript?
   - API response có đúng format?

2. **Kiểm tra server log (terminal)**
   - Request có được gửi đến?
   - API có trả 200 OK?

3. **Verify fix đã được apply**
   - Xem source HTML trong browser (Ctrl+U)
   - Tìm dòng `params.append('offset'` - phải có

4. **Test trực tiếp API**
   - Dùng curl hoặc Postman
   - Xem response có `total` field không

---

**Tóm tắt:** Đã fix 2 lỗi JavaScript quan trọng để pagination và author/artist search hoạt động. Cần restart server và refresh browser để áp dụng.
