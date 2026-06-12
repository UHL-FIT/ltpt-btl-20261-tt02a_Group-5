# controllers/patient_controller.py
# Điều phối giữa View và Model. Nhận yêu cầu từ view, gọi model, sau đó yêu cầu view cập nhật.

import re  # Để xử lý số điện thoại
from models import patient as model
from models import medical as medical_model
from utils.logger import get_logger
from services.ai_agent import ClinicAIAgent  # Import AI Agent
from config.languages import LANGUAGES  # Import từ điển đa ngôn ngữ

logger = get_logger(__name__)   # Logger riêng cho controller

class PatientController:
    def __init__(self, view):
        """
        Khởi tạo controller.
        - view: đối tượng MainView (giao diện).
        - Lưu view, và gắn controller vào view.
        """
        self.view = view   # Lưu lại tham chiếu đến view
        
        # --- ĐA NGÔN NGỮ TOÀN HỆ THỐNG ---
        self.current_lang = "vi"  # Ngôn ngữ mặc định ban đầu là Tiếng Việt
        self._sub_windows = []    # Danh sách theo dõi các cửa sổ con đang mở
        
        # Gắn chính controller này vào view để view có thể gọi các phương thức.
        self.view.set_controller(self)
        
        # Khởi tạo dịch vụ AI Agent sử dụng lâu dài
        try:
            self.ai_agent_service = ClinicAIAgent()
        except Exception as e:
            logger.error(f"Không thể khởi tạo ClinicAIAgent: {e}")
            self.ai_agent_service = None

    # ------------------ Quản lý Đăng ký / Phát tín hiệu Đổi Ngôn Ngữ ------------------
    def register_sub_window(self, window):
        """Đăng ký một cửa sổ con vào danh sách để quản lý đồng bộ ngôn ngữ."""
        if window not in self._sub_windows:
            self._sub_windows.append(window)

    def unregister_sub_window(self, window):
        """Xóa cửa sổ con khỏi danh sách quản lý khi nó bị đóng."""
        if window in self._sub_windows:
            self._sub_windows.remove(window)

    def change_system_language(self, lang_code):
        """
        HÀM 1: Thay đổi ngôn ngữ hệ thống theo chuẩn mã (vi, en).
        Duyệt qua cửa sổ chính và tất cả các cửa sổ con để ép dịch lại giao diện.
        """
        if lang_code in ["vi", "Tiếng Việt"]:
            self.current_lang = "vi"
        elif lang_code in ["en", "English"]:
            self.current_lang = "en"
        else:
            if lang_code not in ["vi", "en"]:
                return
            self.current_lang = lang_code

        logger.info(f"Hệ thống chuyển sang ngôn ngữ: {self.current_lang.upper()}")
        self._refresh_all_uis()

    def change_global_language(self, chosen_lang):
        """
        HÀM 2: Dự phòng tên gọi khác của hàm đổi ngôn ngữ nếu giao diện gọi tên này.
        """
        self.change_system_language(chosen_lang)

    def _refresh_all_uis(self):
        """Hàm nội bộ giúp ép tất cả các giao diện nạp lại ngôn ngữ mới"""
        # Dịch lại cửa sổ chính (Thử tất cả các tên hàm có thể có của MainView)
        if hasattr(self.view, "update_languages"):
            self.view.update_languages()
        elif hasattr(self.view, "update_ui_text"):
            self.view.update_ui_text()
        elif hasattr(self.view, "refresh_ui"):
            self.view.refresh_ui()
            
        # Dịch lại tất cả các cửa sổ phụ đang hoạt động
        for window in list(self._sub_windows):
            try:
                if hasattr(window, "update_languages"):
                    window.update_languages()
                elif hasattr(window, "update_ui_text"):
                    window.update_ui_text()
            except Exception as e:
                logger.error(f"Lỗi cập nhật ngôn ngữ cửa sổ con: {e}")

    def get_localization(self):
        """Hàm tiện ích giúp lấy nhanh từ điển ngôn ngữ hiện tại của hệ thống."""
        return LANGUAGES[self.current_lang]

    # ------------------ Quản lý dữ liệu bệnh nhân (Patients) ------------------
    def get_all_patients(self, search_keyword=""):
        """
        ĐỒNG BỘ CỬA SỔ CHÍNH: Trả về DataFrame chứa danh sách bệnh nhân.
        Giúp main_view.py chạy vòng lặp .iterrows() không bị lỗi NoneType.
        """
        return model.get_all_patients()

    def load_all_patients(self, search_keyword=""):
        """Tải danh sách bệnh nhân và tự động cập nhật bảng hiển thị trên giao diện."""
        df = model.get_all_patients()
        if hasattr(self.view, "update_table"):
            self.view.update_table(df)

    def add_patient(self, name, birth_year, gender, phone, address):
        """Thêm bệnh nhân mới."""
        model.add_patient(name, birth_year, gender, phone, address)
        logger.info(f"Controller: Đã thêm bệnh nhân mới: {name}")
        self.load_all_patients()

    def update_patient(self, patient_id, name, birth_year, gender, phone, address):
        """Cập nhật thông tin bệnh nhân."""
        model.update_patient(patient_id, name, birth_year, gender, phone, address)
        logger.info(f"Controller: Đã cập nhật bệnh nhân ID {patient_id}")
        self.load_all_patients()

    def delete_patient(self, patient_id):
        """Xóa bệnh nhân."""
        model.delete_patient(patient_id)
        logger.info(f"Controller: Đã xóa bệnh nhân ID {patient_id}")
        self.load_all_patients()

    def import_from_csv(self, file_path):
        """Nhập dữ liệu bệnh nhân từ tệp CSV."""
        success_count, error_msg = model.import_from_csv(file_path)
        if success_count > 0:
            logger.info(f"Controller: Import thành công {success_count} bệnh nhân từ {file_path}")
            self.load_all_patients()
        return success_count, error_msg

    def export_to_csv(self, file_path):
        """Xuất dữ liệu bệnh nhân ra tệp CSV."""
        success, error_msg = model.export_to_csv(file_path)
        if success:
            logger.info(f"Controller: Xuất dữ liệu bệnh nhân thành công ra {file_path}")
        return success, error_msg

    # ------------------ Quản lý lịch sử khám y khoa (Medical History) ------------------
    def add_medical_visit(self, patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice=""):
        """Thêm một lần khám mới cho bệnh nhân kèm nội dung tư vấn AI vừa sinh ra."""
        medical_model.add_visit(patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription, ai_advice)
        logger.info(f"Controller: Đã thêm lượt khám kèm tư vấn AI cho bệnh nhân ID {patient_id}")

    def get_medical_history(self, patient_id):
        """Lấy lịch sử khám của bệnh nhân (bao gồm cả cột dữ liệu AI)."""
        return medical_model.get_visits_by_patient(patient_id)

    def delete_medical_visit(self, visit_id):
        """Xóa lần khám."""
        medical_model.delete_visit(visit_id)
        logger.info(f"Controller: Đã xóa lượt khám ID {visit_id}")

    # ------------------ Tương tác với AI Agent ------------------
    def ask_ai_for_advice(self, diagnosis, prescription):
        """
        Gọi tới service AI Agent để xử lý dữ liệu và trả kết quả văn bản về cho giao diện.
        """
        texts = self.get_localization()
        if not self.ai_agent_service:
            return texts["msg_no_ai_agent"]
        
        try:
            advice = self.ai_agent_service.analyze_medical_visit(
                diagnosis=diagnosis, 
                prescription=prescription, 
                language=self.current_lang
            )
            return advice
        except Exception as e:
            logger.error(f"Lỗi khi gọi AI Agent: {e}")
            err_msg = "Không thể xử lý yêu cầu AI" if self.current_lang == "vi" else "Cannot process AI request"
            return f"{err_msg}: {e}"