# ============================================================================
# FILE: models/patient.py
# MỤC ĐÍCH: Các hàm thao tác với bảng patients (CRUD) trong SQLite.
#           Sử dụng pandas để trả về DataFrame, logger để ghi log.
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import pandas as pd
# ^ Lệnh import thư viện pandas (lệnh thư viện), đặt tên pd (quy ước chung).
#   Dùng để xử lý dữ liệu dạng bảng (DataFrame).

from models.database import get_connection, init_db
# ^ Lệnh import hai hàm get_connection (mở kết nối SQLite) và init_db (tạo bảng)
#   từ module models.database (do người dùng định nghĩa).

from utils.logger import get_logger
# ^ Lệnh import hàm get_logger (lấy logger) từ module utils.logger (do người dùng định nghĩa).

# ============================================================================
# 2. KHỞI TẠO LOGGER VÀ ĐẢM BẢO DATABASE ĐÃ SẴN SÀNG
# ============================================================================
# Tạo logger cho module này (tên logger là "models.patient")
logger = get_logger(__name__)
# ^ Biến logger (do người dùng đặt) – dùng để ghi log các hoạt động.

# Gọi init_db() ngay khi import module để đảm bảo bảng patients đã tồn tại (lệnh thư viện)
init_db()
# ^ Lệnh gọi hàm init_db() (do người dùng định nghĩa) – tạo bảng nếu chưa có.

# ============================================================================
# 3. HÀM get_all_patients() - LẤY TOÀN BỘ DANH SÁCH BỆNH NHÂN
# ============================================================================
def get_all_patients():
    # Dòng trên: định nghĩa hàm get_all_patients (do người dùng đặt)
    """
    Lấy toàn bộ danh sách bệnh nhân từ database.
    Trả về một pandas.DataFrame với các cột: id, name, birth_year, gender, phone, address.
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả hàm

    # Mở kết nối đến database (dùng with để tự động đóng kết nối)
    with get_connection() as conn:
        # ^ Gọi hàm get_connection() để mở kết nối, gán vào biến conn (do người dùng đặt)

        # pd.read_sql_query() thực thi câu lệnh SQL và trả về DataFrame (lệnh thư viện)
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY id", conn)
        # ^ Biến df (do người dùng đặt) – DataFrame chứa dữ liệu bệnh nhân

    # Trả về DataFrame (có thể rỗng nếu chưa có dữ liệu) – lệnh return
    return df

# ============================================================================
# 4. HÀM add_patient() - THÊM MỘT BỆNH NHÂN MỚI
# ============================================================================
def add_patient(name, birth_year, gender, phone, address):
    # Dòng trên: định nghĩa hàm add_patient với 5 tham số (do người dùng đặt)
    """
    Thêm một bệnh nhân mới vào bảng.
    Các tham số: name (bắt buộc), birth_year (số), gender, phone, address.
    Trả về id của bản ghi vừa thêm (để sử dụng nếu cần).
    """
    # ^ Docstring mô tả hàm

    with get_connection() as conn:
        # ^ Mở kết nối, gán vào conn

        # INSERT INTO ... VALUES (?,?,?,?,?) sử dụng placeholder ? để tránh SQL injection
        # Các dấu ? sẽ được thay thế bằng giá trị tương ứng trong tuple (lệnh thư viện)
        conn.execute("""
            INSERT INTO patients (name, birth_year, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, birth_year, gender, phone, address))
        # ^ Thực thi câu lệnh INSERT – thêm một dòng mới

        # Lấy id của bản ghi vừa thêm (hàm last_insert_rowid() trong SQLite)
        last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        # ^ Biến last_id (do người dùng đặt) – lưu id vừa được tạo tự động

        # Ghi log thông tin thêm bệnh nhân (lệnh thư viện)
        logger.info(f"Added patient: {name} (id={last_id})")
        # ^ Ghi log với mức INFO

        return last_id          # Trả về id (do người dùng đặt)

# ============================================================================
# 5. HÀM update_patient() - CẬP NHẬT THÔNG TIN BỆNH NHÂN
# ============================================================================
def update_patient(pid, name, birth_year, gender, phone, address):
    # Dòng trên: định nghĩa hàm update_patient với 6 tham số (do người dùng đặt)
    """
    Cập nhật thông tin bệnh nhân có id = pid.
    Cập nhật tất cả các cột (name, birth_year, gender, phone, address).
    """
    # ^ Docstring mô tả hàm

    with get_connection() as conn:
        # ^ Mở kết nối

        # UPDATE ... SET ... WHERE id = ?  (lệnh SQL với placeholder)
        conn.execute("""
            UPDATE patients
            SET name=?, birth_year=?, gender=?, phone=?, address=?
            WHERE id=?
        """, (name, birth_year, gender, phone, address, pid))
        # ^ Thực thi câu lệnh UPDATE – sửa dòng có id = pid

        # Ghi log cập nhật thành công
        logger.info(f"Updated patient id {pid}")

# ============================================================================
# 6. HÀM delete_patient() - XÓA MỘT BỆNH NHÂN THEO ID
# ============================================================================
def delete_patient(pid):
    # Dòng trên: định nghĩa hàm delete_patient với tham số pid (do người dùng đặt)
    """
    Xóa bệnh nhân có id = pid khỏi database.
    Lưu ý: Nếu có ràng buộc khóa ngoại (ON DELETE CASCADE) thì các lần khám liên quan cũng bị xóa.
    """
    # ^ Docstring mô tả hàm

    with get_connection() as conn:
        # ^ Mở kết nối

        # Thực thi câu lệnh DELETE với điều kiện id = ?
        conn.execute("DELETE FROM patients WHERE id=?", (pid,))
        # ^ Xóa dòng có id = pid

        # Ghi log xóa thành công
        logger.info(f"Deleted patient id {pid}")