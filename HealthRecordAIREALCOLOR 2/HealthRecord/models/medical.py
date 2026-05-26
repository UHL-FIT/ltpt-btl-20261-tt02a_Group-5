# ============================================================================
# FILE: models/medical.py
# MỤC ĐÍCH: Quản lý lịch sử khám bệnh (medical_visits) trong database.
#           Cung cấp các hàm: thêm, lấy danh sách, xóa lần khám.
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import pandas as pd
# ^ Lệnh import thư viện pandas (lệnh thư viện), đặt tên viết tắt là pd (theo quy ước)

from models.database import get_connection
# ^ Lệnh import hàm get_connection từ module models.database (do người dùng định nghĩa)

from utils.logger import get_logger
# ^ Lệnh import hàm get_logger từ module utils.logger (do người dùng định nghĩa)

# ============================================================================
# 2. KHỞI TẠO LOGGER CHO MODULE NÀY
# ============================================================================
# get_logger(__name__) trả về đối tượng logging, giúp ghi log các sự kiện (lệnh thư viện)
logger = get_logger(__name__)
# ^ Biến logger (do người dùng đặt) – dùng để ghi log, tên logger là "models.medical"

# ============================================================================
# 3. HÀM get_visits_by_patient() - LẤY DANH SÁCH LẦN KHÁM CỦA MỘT BỆNH NHÂN
# ============================================================================
def get_visits_by_patient(patient_id):
    # Dòng trên: định nghĩa hàm (do người dùng đặt) với tham số patient_id (int)
    """
    Lấy tất cả các lần khám của một bệnh nhân, sắp xếp theo ngày mới nhất trước.
    Trả về pandas.DataFrame (bao gồm cả cột ai_advice).
    """
    # ^ Docstring mô tả hàm

    # Mở kết nối đến database (dùng with để tự động đóng) (lệnh thư viện)
    with get_connection() as conn:
        # ^ Gọi hàm get_connection() mở kết nối, gán vào biến conn

        # pd.read_sql_query: thực thi câu lệnh SQL và trả về DataFrame (lệnh thư viện)
        df = pd.read_sql_query("""
            SELECT id, patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice 
            FROM medical_visits
            WHERE patient_id = ?
            ORDER BY visit_date DESC
        """, conn, params=(patient_id,))
        # ^ Biến df (do người dùng đặt) – DataFrame chứa kết quả truy vấn

    # Trả về DataFrame (có thể rỗng nếu chưa có lần khám nào)
    return df

# ============================================================================
# 4. HÀM add_visit() - THÊM MỘT LẦN KHÁM MỚI
# ============================================================================
def add_visit(patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice=""):
    # Dòng trên: định nghĩa hàm add_visit (do người dùng đặt) với 9 tham số
    # Tham số mặc định: ai_advice="" (chuỗi rỗng)
    """
    Thêm một lần khám mới cho bệnh nhân kèm theo lời khuyên của AI.
    Tham số:
        patient_id (int): id bệnh nhân
        visit_date (str): ngày khám (định dạng YYYY-MM-DD)
        height (float): chiều cao (cm), có thể None
        weight (float): cân nặng (kg), có thể None
        systolic (int): huyết áp tâm thu, có thể None
        diastolic (int): huyết áp tâm trương, có thể None
        diagnosis (str): chẩn đoán
        prescription (str): thuốc kê
        ai_advice (str): lời khuyên từ AI (mặc định rỗng)
    """
    # ^ Docstring mô tả hàm và các tham số

    # Mở kết nối (lệnh thư viện with)
    with get_connection() as conn:
        # Thực thi câu lệnh INSERT với các placeholder ? để tránh SQL injection (lệnh thư viện)
        conn.execute("""
            INSERT INTO medical_visits
            (patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice))
        # ^ Tuple (patient_id, visit_date, ...) chứa các giá trị thay thế vào dấu ? (lệnh thư viện)

        # Lưu thay đổi (commit) – with sẽ tự động commit, nhưng gọi rõ ràng để an toàn (lệnh thư viện)
        conn.commit()

        # Ghi log thông tin (lệnh thư viện)
        logger.info(f"Added medical visit for patient {patient_id} on {visit_date} with AI advice")
        # ^ Dòng log sẽ ghi: "Added medical visit for patient X on YYYY-MM-DD with AI advice"

# ============================================================================
# 5. HÀM delete_visit() - XÓA MỘT LẦN KHÁM THEO ID
# ============================================================================
def delete_visit(visit_id):
    # Dòng trên: định nghĩa hàm delete_visit (do người dùng đặt) với tham số visit_id (int)
    """
    Xóa một lần khám theo id.
    Tham số: visit_id (int) - id của lần khám cần xóa.
    """
    # ^ Docstring mô tả hàm

    with get_connection() as conn:
        # Thực thi câu lệnh DELETE (lệnh thư viện)
        conn.execute("DELETE FROM medical_visits WHERE id=?", (visit_id,))
        # ^ (visit_id,) là tuple một phần tử

        conn.commit()
        # ^ Lưu thay đổi (lệnh thư viện)

        # Ghi log xóa thành công (lệnh thư viện)
        logger.info(f"Deleted medical visit id {visit_id}")
        # ^ Dòng log: "Deleted medical visit id X"