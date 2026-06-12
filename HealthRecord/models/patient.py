# models/patient.py
# Các hàm thao tác với bảng patients: lấy danh sách, thêm, sửa, xóa.
# Sử dụng pandas để dễ dàng trả về DataFrame (bảng dữ liệu).

import pandas as pd                     # Import pandas (thư viện xử lý dữ liệu dạng bảng)
from models.database import get_connection, init_db   # Import các hàm từ database
from utils.logger import get_logger

logger = get_logger(__name__)           # Tạo logger riêng cho module này

# Gọi init_db() ngay khi import module này để đảm bảo bảng đã tồn tại.
init_db()

def get_all_patients(search_keyword=""):
    """Lấy danh sách bệnh nhân từ cơ sở dữ liệu, hỗ trợ tìm kiếm theo tên hoặc SĐT"""
    import pandas as pd
    from . import get_connection # hoặc cách bạn import hàm lấy kết nối trong file đó
    
    query = "SELECT * FROM patients"
    params = []
    
    if search_keyword:
        query += " WHERE name LIKE ? OR phone LIKE ?"
        params.append(f"%{search_keyword}%")
        params.append(f"%{search_keyword}%")
        
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df

def add_patient(name, birth_year, gender, phone, address):
    """
    Thêm một bệnh nhân mới vào bảng.
    Các tham số: name (bắt buộc), birth_year (số), gender, phone, address.
    Trả về id của bản ghi vừa thêm (để sử dụng nếu cần).
    """
    with get_connection() as conn:
        # INSERT INTO ... VALUES (?,?,?,?,?) sử dụng placeholder để tránh SQL injection.
        # Các dấu ? sẽ được thay thế bằng giá trị tương ứng trong tuple.
        conn.execute("""
            INSERT INTO patients (name, birth_year, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, birth_year, gender, phone, address))
        
        # Lấy id của bản ghi vừa thêm (hàm last_insert_rowid() trong SQLite)
        last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Ghi log: thêm thành công, kèm tên và id
        logger.info(f"Added patient: {name} (id={last_id})")
        return last_id

def update_patient(pid, name, birth_year, gender, phone, address):
    """
    Cập nhật thông tin bệnh nhân có id = pid.
    Cập nhật tất cả các cột (name, birth_year, gender, phone, address).
    """
    with get_connection() as conn:
        # UPDATE ... SET ... WHERE id = ?
        conn.execute("""
            UPDATE patients
            SET name=?, birth_year=?, gender=?, phone=?, address=?
            WHERE id=?
        """, (name, birth_year, gender, phone, address, pid))
        logger.info(f"Updated patient id {pid}")

def delete_patient(pid):
    """
    Xóa bệnh nhân có id = pid khỏi database.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM patients WHERE id=?", (pid,))
        logger.info(f"Deleted patient id {pid}")# models/patient.py
# Các hàm thao tác với bảng patients: lấy danh sách, thêm, sửa, xóa.
# Sử dụng pandas để dễ dàng trả về DataFrame (bảng dữ liệu).

import pandas as pd                     # Import pandas (thư viện xử lý dữ liệu dạng bảng)
from models.database import get_connection, init_db   # Import các hàm từ database
from utils.logger import get_logger

logger = get_logger(__name__)           # Tạo logger riêng cho module này

# Gọi init_db() ngay khi import module này để đảm bảo bảng đã tồn tại.
init_db()

def get_all_patients():
    """
    Lấy toàn bộ danh sách bệnh nhân từ database.
    Trả về một pandas.DataFrame với các cột: id, name, birth_year, gender, phone, address.
    """
    # Mở kết nối
    with get_connection() as conn:
        # pd.read_sql_query() cho phép chạy câu lệnh SQL và trả về DataFrame.
        # Câu lệnh: chọn tất cả các cột, sắp xếp theo id tăng dần.
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY id", conn)
    # Trả về DataFrame (có thể rỗng nếu chưa có dữ liệu)
    return df

def add_patient(name, birth_year, gender, phone, address):
    """
    Thêm một bệnh nhân mới vào bảng.
    Các tham số: name (bắt buộc), birth_year (số), gender, phone, address.
    Trả về id của bản ghi vừa thêm (để sử dụng nếu cần).
    """
    with get_connection() as conn:
        # INSERT INTO ... VALUES (?,?,?,?,?) sử dụng placeholder để tránh SQL injection.
        # Các dấu ? sẽ được thay thế bằng giá trị tương ứng trong tuple.
        conn.execute("""
            INSERT INTO patients (name, birth_year, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, birth_year, gender, phone, address))
        
        # Lấy id của bản ghi vừa thêm (hàm last_insert_rowid() trong SQLite)
        last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Ghi log: thêm thành công, kèm tên và id
        logger.info(f"Added patient: {name} (id={last_id})")
        return last_id

def update_patient(pid, name, birth_year, gender, phone, address):
    """
    Cập nhật thông tin bệnh nhân có id = pid.
    Cập nhật tất cả các cột (name, birth_year, gender, phone, address).
    """
    with get_connection() as conn:
        # UPDATE ... SET ... WHERE id = ?
        conn.execute("""
            UPDATE patients
            SET name=?, birth_year=?, gender=?, phone=?, address=?
            WHERE id=?
        """, (name, birth_year, gender, phone, address, pid))
        logger.info(f"Updated patient id {pid}")

def delete_patient(pid):
    """
    Xóa bệnh nhân có id = pid khỏi database.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM patients WHERE id=?", (pid,))
        logger.info(f"Deleted patient id {pid}")