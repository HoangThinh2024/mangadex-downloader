🚀 MANGADEX DOWNLOADER - VỨA CẬP NHẬT v2.0

================================================================================
LƯU Ý QUAN TRỌNG - ĐỌCNGAY
================================================================================

✅ Server đang chạy trên http://localhost:8000

Nếu server bị tắt, chạy lệnh này:
  cd C:\mangadex-downloader
  uv run python .\run_web.py

Sau đó mở: http://localhost:8000

================================================================================
MỀ CẬP NHẬT HOÀN THÀNH ✨
================================================================================

1. ✅ PHÂN TRANG (PAGINATION)
   - Khi tìm "One Piece" → Thấy 95 kết quả
   - Nhìn thấy buttons: Previous, [1] [2] [3]..., Next
   - Có thể chọn số kết quả mỗi trang (1-100)

2. ✅ HIỂN THỊ URL / ID
   - Mỗi card truyện: "ID: xxxxx..." (8 ký tự)
   - Tab Details: ID đầy đủ + Link MangaDex
   - Có thể copy ID để paste vào Download

3. ✅ CHỌN THƯ MỤC TẢI XUỐNG
   - Download tab → "Save Directory" field
   - Nhập: C:\Manga\One Piece
   - Để trống = dùng default

4. ✅ TÌM KIẾM THEO TÁC GIẢ
   - "Author (Search)" field trong Search tab
   - Ví dụ: Naruto + "Masashi Kishimoto"

5. ✅ TÌM KIẾM THEO HỌA SĨ
   - "Artist (Search)" field trong Search tab
   - Ví dụ: Naruto + tên họa sĩ

6. ✅ TOÀN BỘ 39 NGÔN NGỮ
   - Dropdown "Original Language"
   - Từ English, Japanese đến Vietnamese, Thai, Arabic...

7. ✅ LẤY TOÀN BỘ DỮ LIỆU
   - Phân trang cho phép duyệt tất cả truyện
   - Mỗi trang max 100 kết quả
   - Chỉ đọc (không upload lên MangaDex)

================================================================================
🎯 BẮTĐẦU NHANH (1 PHÚT)
================================================================================

BƯỚC 1: TÌM KIẾM
  - Mở http://localhost:8000
  - Tab "Search" (đang mở)
  - Nhập: "One Piece"
  - Click: "Search Manga"
  - Kết quả: 95 truyện + Pagination buttons

BƯỚC 2: PHÂN TRANG
  - Nhìn thấy buttons: Previous [1] [2] [3]... Next
  - Click trang 2, 3, ... để xem kết quả khác
  - Hoặc thay đổi "Results Per Page" (max 100)

BƯỚC 3: XEM CHI TIẾT
  - Click "View" button trên card
  - Xem: Cover, ID đầy đủ, URL MangaDex, Authors, Artists, Chapters

BƯỚC 4: TẢI XUỐNG
  - Click "Download" button (từ search)
  - Hoặc Tab "Download" → Paste ID/URL
  - Chọn Format (PDF, EPUB, CBZ)
  - Nhập thư mục: C:\Manga\One Piece (tùy chọn)
  - Click "Start Download"

================================================================================
📁 FILE HƯỚNG DẪN
================================================================================

1. SUMMARY_V2.0.txt (NGAY TẠI ĐÂY)
   - Tóm tắt tất cả tính năng
   - Quick start 1 phút

2. FEATURES_UPDATE_v2.txt
   - Chi tiết mỗi tính năng
   - API mới nào được thêm

3. USAGE_GUIDE_DETAILED.txt
   - Hướng dẫn chi tiết từng tab
   - Cách dùng từng field
   - Ví dụ thực tế

4. API_REFERENCE.txt
   - Tham khảo API endpoints
   - Parameters, response format
   - Curl examples

================================================================================
🎨 GIAO DIỆN CẦN NHÌN
================================================================================

HEADER:
  MangaDex Downloader
  [Search]  [Download]  [Details]

TAB 1: SEARCH
  ├─ Title* (bắt buộc)
  ├─ Author (tùy chọn)
  ├─ Artist (tùy chọn)
  ├─ Status: Any Status ▼
  ├─ Language: 39 ngôn ngữ ▼
  ├─ Rating: Any Rating ▼
  ├─ Results Per Page: 12
  └─ [Search Manga] button
  
  RESULTS:
  ├─ "Found 95 manga | Showing page 1"
  ├─ [Card 1] [Card 2] [Card 3]... (grid)
  │  ├─ Cover image
  │  ├─ Title
  │  ├─ Status
  │  ├─ ID: xxxxx...
  │  └─ [Download] [View]
  └─ Pagination: [< Previous] [1] [2] [3]... [Next >]

TAB 2: DOWNLOAD
  ├─ URL or ID* (bắt buộc)
  ├─ Format: Auto Detect ▼
  ├─ Language: Default ▼
  ├─ Start Chapter: 1
  ├─ End Chapter: latest
  ├─ Scanlation Group:
  ├─ Save Directory: (NỚI)
  ├─ ☐ Don't track
  └─ [Start Download] button
  
  STATUS:
  ├─ Status: downloading
  └─ Message: Downloaded 50 chapters...

TAB 3: DETAILS
  ├─ Manga ID: xxxxx...
  ├─ Manga URL: [link to mangadex.org]
  ├─ [Cover Image]
  ├─ Title
  ├─ Description
  ├─ Authors
  ├─ Artists
  ├─ Status, Year, Rating
  └─ Latest Chapters (50):
     ├─ Chapter 1 - Title | Pages: 20 | 2024-12-01
     └─ ...

================================================================================
💬 TÍNH NĂNG NỔI BẬT
================================================================================

PHÂN TRANG:
  - Trước: Chỉ 12 kết quả, không xem được thêm
  - Giờ: 95 kết quả One Piece, có phân trang
  - Click Previous/Next để duyệt

ID / URL:
  - Trước: Không thấy ID trên card
  - Giờ: Thấy ID (rút gọn) + URL đầy đủ ở Details
  - Copy để paste vào Download

NGÔN NGỮ:
  - Trước: 4 ngôn ngữ
  - Giờ: 39 ngôn ngữ từ MangaDex
  - English, Japanese, Chinese, Korean, Spanish, French, German...

AUTHOR/ARTIST:
  - Trước: Không thể tìm theo tác giả
  - Giờ: Có field riêng cho Author + Artist
  - Tìm chính xác truyện của tác giả cụ thể

THƯMỤC:
  - Trước: Không thể chọn thư mục
  - Giờ: Field "Save Directory"
  - Nhập: C:\Manga\ để lưu vào folder riêng

================================================================================
🔍 TEST NHANH - KIỂM TRA HOẠT ĐỘNG
================================================================================

TEST 1: Phân trang
  1. Search tab → Title: "Naruto"
  2. Results Per Page: 5
  3. [Search Manga]
  4. Thấy 5 kết quả
  5. Click [2] → Thấy 5 kết quả khác
  6. ✅ PASS

TEST 2: ID/URL
  1. Search tab → Title: "One Piece"
  2. Click [View] trên card
  3. Details tab → Thấy ID đầy đủ
  4. Thấy URL: https://mangadex.org/title/...
  5. ✅ PASS

TEST 3: Ngôn ngữ
  1. Search tab → Language dropdown
  2. Chọn "Vietnamese"
  3. Thấy 39 ngôn ngữ
  4. ✅ PASS

TEST 4: Download
  1. Copy ID từ Details
  2. Download tab → Paste ID
  3. Nhập: C:\Manga\One Piece
  4. [Start Download]
  5. Thấy "Status: downloading"
  6. ✅ PASS

================================================================================
⚡ SHORTCUTS / MẸO
================================================================================

1. Click "Download" từ Search → Tự điền ID vào Download tab
2. Click "View" từ Search → Chuyển tới Details tab + Load Details
3. Copy URL từ Details → Paste vào Download
4. Dùng "Results Per Page: 100" để xem nhiều kết quả cùng lúc

================================================================================
❓ HELP - GIẢI QUYẾT VẤN ĐỀ
================================================================================

Server không chạy?
  → cd C:\mangadex-downloader
  → uv run python .\run_web.py

Không tìm được kết quả?
  → Kiểm tra spelling tên truyện
  → Bỏ Author/Artist nếu có
  → Tăng "Results Per Page"

Không tải được?
  → Kiểm tra ID/URL đúng
  → Xác nhân thư mục tồn tại
  → Thử format khác (PDF → EPUB)

Hình cover không load?
  → Kiểm tra internet
  → Reload trang
  → MangaDex CDN có thể chậm

================================================================================
📚 HỮU DUNG THÊM
================================================================================

Ban đầu, chỉ tìm được 12 truyện → Không xem được thêm
Giờ với phân trang → Có thể xem 95 truyện One Piece

Ban đầu, không biết ID truyện
Giờ → ID rõ ràng, có thể copy-paste

Ban đầu, chỉ 4 ngôn ngữ
Giờ → 39 ngôn ngữ từ MangaDex

Ban đầu, không tìm theo tác giả
Giờ → Có thể tìm chính xác

Ban đầu, không chọn thư mục
Giờ → Có thể lưu vào folder khác nhau

================================================================================
🎁 TẬT CẢ ĐỀU HOÀN THÀNH ✨
================================================================================

✅ Phân trang - Thấy tất cả kết quả
✅ Hiển thị ID/URL - Biết ID đầy đủ
✅ Chọn thư mục - Lưu vào folder tùy chọn
✅ Tìm Author - Tìm chính xác theo tác giả
✅ Tìm Artist - Tìm chính xác theo họa sĩ
✅ 39 Ngôn ngữ - Từ tất cả các quốc gia
✅ Toàn bộ dữ liệu - Phân trang để xem tất cả

BƯỚC TIẾP THEO:
  1. Mở http://localhost:8000
  2. Thử "One Piece" → Thấy 95 kết quả
  3. Duyệt các trang
  4. Click "View" → Xem chi tiết
  5. Download một truyện
  6. Chúc mừng! Bạn đã sử dụng v2.0 thành công! 🎉

================================================================================
✨ Chúc bạn tải xuống truyện vui vẻ! 📚
================================================================================
