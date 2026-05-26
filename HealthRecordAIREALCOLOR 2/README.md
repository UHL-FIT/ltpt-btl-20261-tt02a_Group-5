# 🏥 Ứng dụng Quản lý Hồ sơ Sức khỏe - HealthRecord

Ứng dụng quản lý thông tin bệnh nhân, theo dõi lịch sử khám bệnh và tích hợp Trợ lý AI tư vấn lâm sàng (phiên bản chạy Offline), được xây dựng bằng ngôn ngữ Python sử dụng giao diện đồ họa hiện đại CustomTkinter.

---

## 🛠️ Yêu cầu hệ thống
Trước khi tiến hành mở dự án, hãy đảm bảo máy tính đã cài đặt:
* **Python**: Phiên bản 3.10 trở lên (Khuyến nghị Python 3.14)
* **Hệ điều hành**: Linux (Fedora, Ubuntu...), Windows hoặc macOS

---

## 🚀 Hướng dẫn mở và chạy dự án (Trên Linux / VS Code)

Hãy thực hiện tuần tự theo các bước dưới đây để khởi chạy ứng dụng một cách chính xác nhất:

### Bước 1: Mở thư mục dự án bằng VS Code
1. Khởi động phần mềm **VS Code**.
2. Trên thanh menu, chọn **File** ➡️ **Open Folder** (hoặc nhấn `Ctrl + K Ctrl + O`).
3. Tìm và chọn chính xác thư mục gốc mang tên **`HealthRecord`**.

### Bước 2: Kích hoạt môi trường ảo (`.venv`)
Mở Terminal tích hợp của VS Code bằng tổ hợp phím **`Ctrl + Shift + ~`** (hoặc `View ➡️ Terminal`) và chạy các lệnh sau:

1. Di chuyển vào thư mục chứa mã nguồn và môi trường ảo:
   ```bash
   cd /home/hwng/Documents/vscode/HealthRecordAIREAL/HealthRecord/
   muốn chạy nhanh
   gemini-ai/.venv/bin/python main.py
   muốn chạy chậm
   cd gemini-ai
   Kích hoạt môi trường ảo .venv để nạp các thư viện đã cài đặt sẵn:
   source .venv/bin/activate

   > 💡 *Dấu hiệu thành công:* Đầu dòng dòng lệnh trong Terminal sẽ xuất hiện ký hiệu dạng `(.venv) [hwng@...]$`.

### Bước 3: Cấu hình Python Interpreter cho VS Code
Nếu VS Code hiển thị cảnh báo thiếu thư viện hoặc `Invalid Interpreter`, hãy thiết lập lại đường dẫn:
1. Nhấn tổ hợp phím **`Ctrl + Shift + P`** để mở Thanh lệnh (Command Palette).
2. Gõ tìm kiếm: `Python: Select Interpreter` và nhấn **Enter**.
3. Chọn chính xác dòng có đường dẫn chứa thư mục `.venv` của dự án (thường hiển thị là `python ('.venv': venv)` hoặc `./.venv/bin/python`).

### Bước 4: Khởi chạy ứng dụng
Tại giao diện Terminal đã được kích hoạt `.venv`, gõ lệnh dưới đây tùy thuộc vào hệ điều hành đang sử dụng:

* **Đối với hệ điều hành Linux (Tránh lỗi đồ họa tiêu điểm trên X11/Wayland):**
  ```bash
  GDK_BACKEND=x11 python main.py
  Đối với hệ điều hành Windows hoặc macOS:
  python main.py

  HƯỚNG DẪN CHẠY DỰ ÁN TRÊN MACOS 

Môi trường ảo của Windows/Linux không thể chạy trực tiếp trên macOS do khác biệt về kiến trúc chip xử lý và định dạng file hệ thống.
Để chạy dự án trên Mac mà không làm ảnh hưởng hay thay đổi cấu trúc môi trường ảo gốc của bạn, hãy bảo bạn của bạn mở Terminal và chạy lần lượt các lệnh sau: 

cd HealthRecordAIREAL/HealthRecord/
(Hoặc gõ cd  rồi kéo thả thư mục dự án vào Terminal).

2. Thiết lập môi trường và chạy ứng dụng
Copy và chạy toàn bộ cụm lệnh này (có thể dán cả cụm vào Terminal cùng lúc):

# Tạo một vùng môi trường riêng cho Mac (không đè lên venv cũ)
python3 -m venv venv_mac

# Kích hoạt môi trường trên Mac
source venv_mac/bin/activate

# Cài đặt các thư viện tương thích với chip và hệ điều hành Mac
pip install google-genai customtkinter pandas openpyxl

# Khởi chạy dự án
python3 main.py

💡 Lưu ý cho các lần mở sau:

Từ lần tiếp theo, bạn của bạn không cần tạo hay cài đặt lại nữa. Mỗi khi muốn mở ứng dụng, chỉ cần chạy 2 dòng này là xong:
source venv_mac/bin/activate
python3 main.py