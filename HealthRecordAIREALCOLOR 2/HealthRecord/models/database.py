# ============================================================================
# FILE: models/database.py
# MỤC ĐÍCH: Quản lý kết nối đến cơ sở dữ liệu SQLite và tạo các bảng.
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import sqlite3
# ^ Lệnh import thư viện sqlite3 (lệnh thư viện) – dùng để kết nối và thao tác với SQLite

import os
# ^ Lệnh import thư viện os (lệnh thư viện) – dùng để làm việc với đường dẫn, thư mục

from utils.logger import get_logger
# ^ Lệnh import hàm get_logger từ module utils.logger (do người dùng định nghĩa)

# ============================================================================
# 2. KHỞI TẠO LOGGER VÀ ĐƯỜNG DẪN CƠ SỞ DỮ LIỆU
# ============================================================================
# Tạo logger cho module này (tên logger là "models.database")
# get_logger(__name__) trả về đối tượng logging (lệnh thư viện)
logger = get_logger(__name__)
# ^ Biến logger (do người dùng đặt) – dùng để ghi log các hoạt động

# Xác định thư mục gốc của dự án (nơi chứa file main.py)
# os.path.dirname(__file__) lấy đường dẫn thư mục chứa file này (models)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# ^ Biến BASE_DIR (do người dùng đặt) – lưu đường dẫn tuyệt đối đến thư mục gốc của dự án

# Tạo đường dẫn đầy đủ đến file cơ sở dữ liệu: <BASE_DIR>/data/health.db
# os.path.join ghép các thành phần thành đường dẫn đúng cú pháp hệ điều hành (lệnh thư viện)
DB_PATH = os.path.join(BASE_DIR, "data", "health.db")
# ^ Biến DB_PATH (do người dùng đặt) – đường dẫn đến file health.db

# ============================================================================
# 3. HÀM get_connection() - MỞ KẾT NỐI ĐẾN DATABASE
# ============================================================================
def get_connection():
    # Dòng trên: định nghĩa hàm get_connection (do người dùng đặt)
    """
    Mở kết nối đến database. Nếu thư mục data chưa có, tự động tạo.
    Hàm trả về đối tượng kết nối (connection) để thực hiện các câu lệnh SQL.
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả hàm

    # Tạo thư mục data nếu chưa tồn tại
    # os.path.dirname(DB_PATH) lấy đường dẫn thư mục chứa file health.db (chính là thư mục data)
    # exist_ok=True: nếu thư mục đã tồn tại thì không báo lỗi (lệnh thư viện)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Kết nối đến SQLite; nếu file chưa tồn tại, nó sẽ tự động được tạo
    # sqlite3.connect là hàm thư viện (lệnh thư viện)
    conn = sqlite3.connect(DB_PATH)
    # ^ Biến conn (do người dùng đặt) – đối tượng kết nối

    return conn          # Trả về đối tượng kết nối (lệnh return)

# ============================================================================
# 4. HÀM init_db() - KHỞI TẠO CÁC BẢNG DỮ LIỆU
# ============================================================================
def init_db():
    # Dòng trên: định nghĩa hàm init_db (do người dùng đặt)
    """Khởi tạo bảng patients và medical_visits mới hoàn toàn với đầy đủ các cột"""
    # ^ Docstring mô tả hàm

    # Sử dụng with để tự động đóng kết nối sau khi thực hiện xong (lệnh thư viện)
    with get_connection() as conn:
        # ^ Gọi hàm get_connection() để mở kết nối, gán vào biến conn (do người dùng đặt)

        # --------------------------------------------------------------------
        # 4.1. TẠO BẢNG patients (thông tin bệnh nhân)
        # --------------------------------------------------------------------
        # CREATE TABLE IF NOT EXISTS: chỉ tạo bảng nếu chưa tồn tại (lệnh SQL)
        # conn.execute() là phương thức thực thi câu lệnh SQL (lệnh thư viện)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_year INTEGER,
                gender TEXT,
                phone TEXT,
                address TEXT
            )
        """)
        # ^ Câu lệnh SQL tạo bảng patients với các cột:
        #   id: khóa chính, tự động tăng
        #   name: tên bệnh nhân (bắt buộc)
        #   birth_year: năm sinh (số nguyên)
        #   gender: giới tính (lưu 'Nam' hoặc 'Nữ')
        #   phone: số điện thoại (chuỗi)
        #   address: địa chỉ (chuỗi)

        # --------------------------------------------------------------------
        # 4.2. TẠO BẢNG medical_visits (lịch sử khám bệnh)
        # --------------------------------------------------------------------
        # Đã cấu hình chuẩn cột ai_advice (lưu tư vấn từ AI)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS medical_visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                visit_date TEXT NOT NULL,
                height REAL,
                weight REAL,
                systolic INTEGER,
                diastolic INTEGER,
                diagnosis TEXT,
                prescription TEXT,
                ai_advice TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)
        # ^ Câu lệnh SQL tạo bảng medical_visits với các cột:
        #   id: khóa chính, tự động tăng
        #   patient_id: khóa ngoại tham chiếu đến patients.id
        #   visit_date: ngày khám (dạng YYYY-MM-DD)
        #   height: chiều cao (cm, số thực)
        #   weight: cân nặng (kg, số thực)
        #   systolic: huyết áp tâm thu (số nguyên, mmHg)
        #   diastolic: huyết áp tâm trương (số nguyên, mmHg)
        #   diagnosis: chẩn đoán (chuỗi)
        #   prescription: thuốc kê (chuỗi)
        #   ai_advice: văn bản tư vấn từ AI (chuỗi dài)
        #   FOREIGN KEY: ràng buộc khóa ngoại
        #   ON DELETE CASCADE: khi xóa bệnh nhân, tự động xóa các lần khám liên quan

        # Ghi log thông báo đã khởi tạo database (lệnh thư viện)
        # logger.info: ghi thông tin (lệnh thư viện)
        logger.info("Database initialized with patients and medical_visits tables (including ai_advice)")