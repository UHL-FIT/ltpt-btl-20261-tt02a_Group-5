# models/database.py
# Quản lý kết nối đến cơ sở dữ liệu SQLite và tạo bảng.

import sqlite3          # Thư viện kết nối SQLite (có sẵn trong Python)
import os               # Để làm việc với đường dẫn
from utils.logger import get_logger   # Import hàm lấy logger từ utils

# Tạo logger cho module này (tên logger là "models.database")
logger = get_logger(__name__)

# Xác định đường dẫn đến file cơ sở dữ liệu (health.db) trong thư mục data.
# BASE_DIR là thư mục gốc của dự án (step4_mvc).
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "health.db")

def get_connection():
    """
    Mở kết nối đến database. Nếu thư mục data chưa có, tự động tạo.
    Hàm trả về đối tượng kết nối (connection) để thực hiện các câu lệnh SQL.
    """
    # os.makedirs tạo thư mục data nếu chưa tồn tại.
    # os.path.dirname(DB_PATH) lấy đường dẫn thư mục chứa file health.db (chính là thư mục data).
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # sqlite3.connect(DB_PATH) mở kết nối; nếu file chưa tồn tại, nó sẽ tự tạo.
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """
    Khởi tạo bảng patients nếu bảng chưa tồn tại.
    Bảng gồm các cột: id (tự động tăng), name (tên), birth_year (năm sinh), gender, phone, address.
    """
    # Sử dụng 'with' để tự động đóng kết nối sau khi thực hiện xong.
    with get_connection() as conn:
        # conn.execute() thực thi câu lệnh SQL.
        # CREATE TABLE IF NOT EXISTS: chỉ tạo bảng nếu chưa có.
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
        # Ghi log thông báo đã khởi tạo database.
        logger.info("Database initialized at %s", DB_PATH)