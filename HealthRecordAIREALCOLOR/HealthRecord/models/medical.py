# models/medical.py
# Quản lý lịch sử khám bệnh: thêm, lấy danh sách, xóa

import pandas as pd
from models.database import get_connection
from utils.logger import get_logger

logger = get_logger(__name__)

def get_visits_by_patient(patient_id):
    """
    Lấy tất cả các lần khám của một bệnh nhân, sắp xếp theo ngày mới nhất trước.
    Trả về pandas.DataFrame (Bao gồm cả cột ai_advice).
    """
    with get_connection() as conn:
        df = pd.read_sql_query("""
            SELECT id, patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice 
            FROM medical_visits
            WHERE patient_id = ?
            ORDER BY visit_date DESC
        """, conn, params=(patient_id,))
    return df

def add_visit(patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice=""):
    """Thêm một lần khám mới cho bệnh nhân kèm lời khuyên của AI."""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO medical_visits
            (patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice))
        conn.commit()
        logger.info(f"Added medical visit for patient {patient_id} on {visit_date} with AI advice")

def delete_visit(visit_id):
    """Xóa một lần khám theo id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM medical_visits WHERE id=?", (visit_id,))
        conn.commit()
        logger.info(f"Deleted medical visit id {visit_id}")