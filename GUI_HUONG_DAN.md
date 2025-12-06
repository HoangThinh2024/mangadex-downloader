# Hướng Dẫn Sử Dụng Giao Diện GUI MangaDex Downloader

## Tổng Quan

MangaDex Downloader giờ đây có giao diện đồ họa hiện đại (GUI) được xây dựng với [customtkinter](https://github.com/TomSchimansky/CustomTkinter). Giao diện GUI cung cấp cách sử dụng trực quan để truy cập tất cả các tính năng CLI mà không cần dùng dòng lệnh.

## Cài Đặt

### Yêu Cầu

- Python 3.10 trở lên
- tkinter (thường đi kèm với Python)
- customtkinter (được cài đặt như dependency tùy chọn)

### Cài đặt với hỗ trợ GUI

```bash
# Cài đặt với tất cả các dependencies tùy chọn (khuyến nghị)
pip install mangadex-downloader[optional]

# Hoặc chỉ cài đặt GUI dependency
pip install mangadex-downloader customtkinter
```

### Yêu cầu riêng cho Linux

Trên hệ thống Linux, bạn có thể cần cài đặt python3-tk:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Chạy GUI

Có nhiều cách để khởi chạy GUI:

### Phương pháp 1: Module Python (khuyến nghị)

```bash
python3 -m mangadex_downloader.gui
```

### Phương pháp 2: Sử dụng lệnh console

```bash
# Sau khi cài đặt với [optional]
mangadex-dl-gui
```

### Phương pháp 3: Sử dụng script launcher

```bash
python3 run_gui.py
```

## Các Tính Năng GUI

### Tab Search (Tìm kiếm)

Tab Search cho phép bạn tìm kiếm manga trên MangaDex và duyệt kết quả với hình ảnh bìa.

**Tính năng:**
- **Search Input** (Nhập tìm kiếm): Nhập tên manga hoặc từ khóa để tìm kiếm
- **Search Results** (Kết quả tìm kiếm): Duyệt manga với:
  - Hình ảnh bìa (tự động tải)
  - Tiêu đề và tiêu đề thay thế
  - Tác giả và họa sĩ
  - Trạng thái và thể loại
  - Xem trước mô tả
- **Download Button** (Nút tải xuống): Nhấp vào bất kỳ kết quả tìm kiếm nào để tải nó vào tab Download

**Cách sử dụng:**
1. Nhập truy vấn tìm kiếm của bạn (ví dụ: "One Piece", "Naruto")
2. Nhấp vào nút Search
3. Duyệt qua kết quả với hình ảnh bìa
4. Nhấp "Download This Manga" trên bất kỳ kết quả nào để chuẩn bị tải xuống
5. Chuyển sang tab Download để cấu hình và bắt đầu tải xuống

### Tab Download (Tải xuống)

Tab chính để tải manga từ MangaDex.

**Các trường:**
- **URL Input**: Nhập URL MangaDex hoặc chọn file chứa nhiều URL
- **Download Type** (Loại tải xuống): Chọn từ:
  - Auto (tự động phát hiện)
  - Manga
  - Chapter (Chương)
  - List (Danh sách)
  - Cover (Bìa)
  - Legacy manga/chapter (cho URL cũ)
- **Language** (Ngôn ngữ): Chọn ngôn ngữ tải xuống (hỗ trợ tất cả ngôn ngữ MangaDex)
- **Format** (Định dạng): Chọn định dạng đầu ra:
  - Raw images (hình ảnh thô)
  - PDF
  - CBZ (Comic Book ZIP)
  - CB7 (Comic Book 7zip) - yêu cầu py7zr
  - EPUB - yêu cầu lxml
- **Cover Quality** (Chất lượng bìa): Chọn chất lượng hình ảnh bìa (original, 512px, 256px, none)
- **Tùy chọn**:
  - Replace existing files (Thay thế file đã tồn tại)
  - Use alternative details (Sử dụng chi tiết thay thế)
  - No oneshot chapters (Không tải oneshot)
  - Use compressed images (Sử dụng hình ảnh nén)
- **Chapter Range** (Phạm vi chương): Tùy chọn chỉ định chương bắt đầu và kết thúc

### Tab Authentication (Xác thực)

Đăng nhập vào MangaDex để truy cập thư viện của bạn và các tính năng yêu cầu xác thực.

**Các trường:**
- **Login Method** (Phương thức đăng nhập): Chọn OAuth2 (khuyến nghị) hoặc Legacy
- **Username** (Tên người dùng): Tên người dùng MangaDex của bạn
- **Password** (Mật khẩu): Mật khẩu MangaDex của bạn
- **Cache credentials** (Lưu thông tin đăng nhập): Lưu đăng nhập cho các phiên sau

**Các nút:**
- **Login**: Xác thực với MangaDex
- **Logout**: Xóa xác thực

### Tab Settings (Cài đặt)

Cấu hình các cài đặt ứng dụng và mạng.

**Cài đặt tải xuống:**
- **Download Path** (Đường dẫn tải xuống): Chọn nơi lưu manga đã tải

**Cài đặt mạng:**
- **Proxy**: Cấu hình HTTP/SOCKS proxy
- **Timeout**: Đặt timeout request (giây)
- **Delay**: Thêm độ trễ giữa các request
- **DNS over HTTPS**: Sử dụng DNS bảo mật (Google hoặc Cloudflare)

**Tùy chọn khác:**
- **Force HTTPS**: Luôn sử dụng HTTPS để tải xuống
- **Disable chapter tracking**: Không theo dõi các chương đã tải
- **Log Level** (Mức độ log): Đặt mức độ chi tiết log (DEBUG, INFO, WARNING, ERROR)

### Tab Logs (Nhật ký)

Xem log thời gian thực của tất cả các hoạt động.

**Tính năng:**
- Hiển thị log thời gian thực
- Hiển thị tiến trình tải xuống, lỗi và cảnh báo
- Nút Clear để đặt lại log

## Mẹo và Thực Hành Tốt Nhất

### Tải xuống hàng loạt

1. Tạo file text với một URL MangaDex trên mỗi dòng
2. Sử dụng nút Browse để chọn file
3. Cấu hình các cài đặt ưa thích của bạn
4. Nhấn Download

### Sử dụng xác thực

Để tải xuống từ thư viện của bạn hoặc truy cập nội dung hạn chế độ tuổi:
1. Đi đến tab Authentication
2. Nhập thông tin đăng nhập của bạn
3. Bật "Cache credentials" để lưu đăng nhập
4. Nhấn Login
5. Quay lại tab Download và tiếp tục bình thường

### Vấn đề mạng

Nếu bạn gặp vấn đề kết nối:
1. Đi đến tab Settings
2. Thử bật DNS over HTTPS
3. Nếu đằng sau proxy, cấu hình cài đặt proxy
4. Tăng timeout nếu tải xuống chậm

### Chọn định dạng

- **Raw**: Tốt nhất để đọc trên máy tính hoặc trình đọc tùy chỉnh
- **PDF**: Định dạng phổ biến, đọc được trên mọi thiết bị
- **CBZ/CB7**: Cho trình đọc truyện tranh
- **EPUB**: Cho máy đọc sách điện tử (yêu cầu lxml)

Volume vs Single vs Chapter:
- **Volume**: Một file cho mỗi tập
- **Single**: Tất cả chương trong một file
- **Default**: Một file cho mỗi chương

## Xử lý Sự Cố

### GUI không khởi động

**Lỗi: "No module named 'tkinter'"**
- Giải pháp: Cài đặt gói python3-tk cho hệ điều hành của bạn

**Lỗi: "No module named 'customtkinter'"**
- Giải pháp: Cài đặt với `pip install customtkinter` hoặc `pip install mangadex-downloader[optional]`

### Vấn đề tải xuống

**Lỗi: "Download failed"**
- Kiểm tra tab Logs để xem thông báo lỗi chi tiết
- Xác minh URL là chính xác
- Kiểm tra kết nối internet của bạn
- Thử bật DNS over HTTPS trong Settings

**Lỗi: "Authentication required"**
- Một số manga yêu cầu đăng nhập để tải xuống
- Đi đến tab Authentication và đăng nhập
- Thử tải xuống lại

### Hiệu suất

**Tải xuống chậm:**
- Tăng timeout trong Settings
- Kiểm tra kết nối internet của bạn
- Tạm thời tắt trình quét virus (nếu nó đang quét tải xuống)

**GUI bị đơ:**
- Điều này là bình thường trong quá trình tải xuống - GUI hiển thị tiến trình trong tab Logs
- Đừng đóng cửa sổ trong khi đang tải xuống

## CLI vs GUI

Tất cả các tính năng CLI đều có sẵn trong GUI. GUI gọi cùng một backend CLI, đảm bảo tính nhất quán.

**Ưu điểm CLI:**
- Có thể script hóa và tự động hóa
- Nhanh hơn cho người dùng chuyên nghiệp
- Có thể chạy trên server không có màn hình

**Ưu điểm GUI:**
- Giao diện thân thiện với người dùng
- Phản hồi trực quan với hình ảnh bìa
- Tìm kiếm manga với xem trước trực quan
- Không cần nhớ lệnh
- Quản lý cấu hình dễ dàng

Bạn có thể sử dụng cả hai tùy theo sở thích của mình!

## Đóng Góp

Nếu bạn tìm thấy lỗi hoặc muốn đề xuất cải tiến GUI:
1. Kiểm tra các vấn đề hiện có trên GitHub
2. Tạo vấn đề mới với:
   - Bạn đã cố gắng làm gì
   - Điều gì đã xảy ra thay thế
   - Screenshots (nếu có)
   - Đầu ra log từ tab Logs

## Tài Nguyên Bổ Sung

- [Tài liệu CLI](https://mangadex-dl.mansuf.link/)
- [Tài liệu API MangaDex](https://api.mangadex.org/docs/)
- [Kho lưu trữ GitHub](https://github.com/mansuf/mangadex-downloader)
- [Tài liệu customtkinter](https://github.com/TomSchimansky/CustomTkinter)

## Screenshot

![GUI Screenshot](https://github.com/user-attachments/assets/41c25f5d-dce2-4358-9984-fcb06cc59caa)

Giao diện GUI hiện đại với 4 tab chính:
1. **Download**: Tải manga với nhiều tùy chọn
2. **Authentication**: Đăng nhập MangaDex
3. **Settings**: Cấu hình ứng dụng
4. **Logs**: Xem tiến trình và lỗi
