# controllers/patient_controller.py
# Điều phối giữa View và Model. Nhận yêu cầu từ view, gọi model, sau đó yêu cầu view cập nhật.

from models import patient as model
from utils.logger import get_logger

logger = get_logger(__name__)   # Logger riêng cho controller

class PatientController:
    def __init__(self, view):
        """
        Khởi tạo controller.
        - view: đối tượng MainView (giao diện).
        - Lưu view, và gắn controller vào view.
        """
        self.view = view   # Lưu lại tham chiếu đến view
        # Gọi phương thức set_controller của view, truyền chính controller này.
        # Khi đó view có thể gọi các phương thức của controller.
        self.view.set_controller(self)

    def get_all_patients(self):
        """
        Lấy toàn bộ dữ liệu bệnh nhân từ model.
        Trả về pandas.DataFrame.
        """
        return model.get_all_patients()

    def add_patient(self, name, birth_year, gender, phone, address):
        """
        Thêm bệnh nhân mới.
        """
        model.add_patient(name, birth_year, gender, phone, address)
        logger.info(f"Controller: Đã thêm bệnh nhân {name}")
        self.view.refresh_table()   # Yêu cầu view làm mới bảng

    def update_patient(self, pid, name, birth_year, gender, phone, address):
        """
        Cập nhật thông tin bệnh nhân.
        """
        model.update_patient(pid, name, birth_year, gender, phone, address)
        logger.info(f"Controller: Đã cập nhật bệnh nhân id {pid}")
        self.view.refresh_table()

    def delete_patient(self, pid):
        """
        Xóa bệnh nhân theo id.
        """
        model.delete_patient(pid)
        logger.info(f"Controller: Đã xóa bệnh nhân id {pid}")
        self.view.refresh_table()