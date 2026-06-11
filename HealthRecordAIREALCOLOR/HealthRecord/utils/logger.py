# utils/logger.py
# Mục đích: Ghi lại nhật ký (log) hoạt động của ứng dụng ra file, giúp theo dõi lỗi và sự kiện.

import os               # Thư viện để làm việc với đường dẫn, thư mục (hệ điều hành)
import logging          # Thư viện chuẩn để ghi log

# Xác định thư mục gốc của dự án (nơi chứa file main.py)
# os.path.dirname(__file__) trả về đường dẫn của file hiện tại (logger.py)
# .dirname lấy thư mục cha, lặp lại 2 lần để lên tới thư mục gốc (step4_mvc)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Tạo đường dẫn đến thư mục data (nằm cùng cấp với main.py)
# os.path.join ghép các thành phần thành đường dẫn đúng cú pháp của hệ điều hành.
DATA_DIR = os.path.join(BASE_DIR, "data")

# Đường dẫn đến file log: data/app.log
LOG_FILE = os.path.join(DATA_DIR, "app.log")

# Tạo thư mục data nếu nó chưa tồn tại.
# exist_ok=True: nếu đã tồn tại thì không báo lỗi, bỏ qua.
os.makedirs(DATA_DIR, exist_ok=True)

# Cấu hình logging để ghi ra file LOG_FILE.
# - filename : file đích.
# - level : mức độ ghi (INFO trở lên sẽ được ghi).
# - format : định dạng mỗi dòng log, bao gồm thời gian, mức độ, nội dung.
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger(name):
    """
    Hàm trả về một logger với tên cụ thể (ví dụ "main", "model", "controller").
    Tên này sẽ xuất hiện trong log để biết module nào ghi log.
    """
    # logging.getLogger(name) lấy hoặc tạo logger mang tên 'name'.
    return logging.getLogger(name)