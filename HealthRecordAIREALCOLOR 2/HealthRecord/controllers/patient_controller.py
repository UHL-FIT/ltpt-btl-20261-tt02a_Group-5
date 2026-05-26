# ============================================================================
# FILE: controllers/patient_controller.py
# MỤC ĐÍCH: Điều phối giữa View (giao diện) và Model (dữ liệu).
#           Nhận yêu cầu từ view, gọi model, xử lý nghiệp vụ, cập nhật view.
#           Tích hợp AI Agent, đa ngôn ngữ, quản lý cửa sổ con.
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import re
# ^ Lệnh import module re (lệnh thư viện) – biểu thức chính quy, dùng để xử lý số điện thoại.

from models import patient as model
# ^ Lệnh import module patient từ thư mục models, đặt tên là model (do người dùng đặt).
#   Module này chứa các hàm CRUD cho bảng patients.

from models import medical as medical_model
# ^ Lệnh import module medical từ thư mục models, đặt tên là medical_model (do người dùng đặt).
#   Module này chứa các hàm CRUD cho bảng medical_visits.

from utils.logger import get_logger
# ^ Lệnh import hàm get_logger từ module utils.logger (do người dùng định nghĩa).

from services.ai_agent import ClinicAIAgent
# ^ Lệnh import class ClinicAIAgent từ module services.ai_agent (do người dùng định nghĩa).

from config.languages import LANGUAGES
# ^ Lệnh import biến LANGUAGES (từ điển) từ file config/languages.py (do người dùng định nghĩa).

# ============================================================================
# 2. KHỞI TẠO LOGGER CHO CONTROLLER
# ============================================================================
# get_logger(__name__) trả về đối tượng logging (lệnh thư viện)
logger = get_logger(__name__)
# ^ Biến logger (do người dùng đặt) – tên logger là "controllers.patient_controller"

# ============================================================================
# 3. ĐỊNH NGHĨA LỚP PatientController
# ============================================================================
class PatientController:
    # Dòng trên: Khai báo class PatientController (do người dùng đặt tên)
    """
    Lớp điều khiển chính, kết nối MainView và các model.
    Quản lý CRUD bệnh nhân, lịch sử khám, import/export CSV, AI, đa ngôn ngữ.
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả class

    # ------------------------------------------------------------------------
    # 3.1. HÀM KHỞI TẠO (__init__) - THIẾT LẬP BAN ĐẦU
    # ------------------------------------------------------------------------
    def __init__(self, view):
        # Dòng trên: định nghĩa hàm khởi tạo (do người dùng định nghĩa)
        # Tham số view: đối tượng MainView (giao diện chính) – do người dùng truyền vào
        """
        Khởi tạo controller.
        - view: đối tượng MainView (giao diện chính).
        - Lưu view, gắn controller vào view, khởi tạo các thành phần phụ trợ.
        """
        # ^ Docstring mô tả phương thức

        # Lưu tham chiếu đến view (biến do người dùng đặt)
        self.view = view

        # --- Biến quản lý đa ngôn ngữ và cửa sổ con ---
        # Biến current_lang (do người dùng đặt) – lưu mã ngôn ngữ hiện tại ("vi" hoặc "en")
        self.current_lang = "vi"

        # Biến _sub_windows (do người dùng đặt) – danh sách các cửa sổ con đang mở, dùng để đồng bộ ngôn ngữ
        self._sub_windows = []

        # Gắn chính controller này vào view (gọi phương thức set_controller của view)
        self.view.set_controller(self)

        # --- Khởi tạo dịch vụ AI Agent (nếu có lỗi thì gán None) ---
        try:
            # Tạo đối tượng ClinicAIAgent (do người dùng định nghĩa)
            self.ai_agent_service = ClinicAIAgent()
            # Ghi log thông báo khởi tạo thành công (lệnh thư viện logger.info)
            logger.info("AI Agent service initialized successfully")
        except Exception as e:
            # Nếu có lỗi, ghi log lỗi (lệnh thư viện logger.error)
            logger.error(f"Không thể khởi tạo ClinicAIAgent: {e}")
            # Gán ai_agent_service = None để tránh lỗi khi gọi sau này
            self.ai_agent_service = None

    # ------------------------------------------------------------------------
    # 3.2. QUẢN LÝ ĐĂNG KÝ / HỦY ĐĂNG KÝ CỬA SỔ CON (CHO ĐỒNG BỘ NGÔN NGỮ)
    # ------------------------------------------------------------------------
    def register_sub_window(self, window):
        # Dòng trên: định nghĩa phương thức register_sub_window (do người dùng đặt)
        # Tham số window: đối tượng cửa sổ con (CTkToplevel) – do người dùng truyền vào
        """
        Đăng ký cửa sổ con vào danh sách lắng nghe sự kiện đổi ngôn ngữ.
        Tham số: window - đối tượng cửa sổ con (CTkToplevel).
        """
        # ^ Docstring

        # Nếu window chưa có trong danh sách _sub_windows
        if window not in self._sub_windows:
            # Thêm window vào danh sách
            self._sub_windows.append(window)
            # Ghi log debug (lệnh thư viện logger.debug)
            logger.debug(f"Đã đăng ký cửa sổ con: {window.__class__.__name__}")

    def unregister_sub_window(self, window):
        # Dòng trên: định nghĩa phương thức unregister_sub_window (do người dùng đặt)
        """
        Xóa cửa sổ con khỏi danh sách lắng nghe khi cửa sổ đó bị đóng (destroy).
        Tham số: window - đối tượng cửa sổ con.
        """
        # ^ Docstring

        # Nếu window có trong danh sách _sub_windows
        if window in self._sub_windows:
            # Xóa window khỏi danh sách
            self._sub_windows.remove(window)
            # Ghi log debug
            logger.debug(f"Đã hủy đăng ký cửa sổ con: {window.__class__.__name__}")

    # ------------------------------------------------------------------------
    # 3.3. THAY ĐỔI NGÔN NGỮ TOÀN CỤC VÀ PHÁT TÍN HIỆU CẬP NHẬT GIAO DIỆN
    # ------------------------------------------------------------------------
    def change_global_language(self, chosen_lang):
        # Dòng trên: định nghĩa phương thức change_global_language (do người dùng đặt)
        # Tham số chosen_lang: chuỗi "vi", "Tiếng Việt", "en", ...
        """
        Thay đổi mã ngôn ngữ toàn cục và phát tín hiệu ép toàn bộ các giao diện đang hiển thị nạp lại chữ.
        Tham số: chosen_lang (str) - "vi", "Tiếng Việt", "en" hoặc tương tự.
        """
        # ^ Docstring

        # Xác định mã ngôn ngữ (vi hoặc en) dựa trên giá trị chosen_lang
        if chosen_lang in ["vi", "Tiếng Việt"]:
            self.current_lang = "vi"
        else:
            self.current_lang = "en"

        # Ghi log thông tin chuyển đổi ngôn ngữ (lệnh thư viện)
        logger.info(f"Hệ thống chuyển đổi sang ngôn ngữ: {self.current_lang}")

        # 1. Cập nhật cửa sổ chính (MainView)
        # Kiểm tra xem view có phương thức update_ui_text không (do người dùng định nghĩa)
        if hasattr(self.view, "update_ui_text"):
            # Nếu có, gọi phương thức đó để cập nhật giao diện chính
            self.view.update_ui_text()
        elif hasattr(self.view, "refresh_ui"):
            # Dự phòng nếu tên hàm khác
            self.view.refresh_ui()

        # 2. Duyệt qua toàn bộ cửa sổ con đang mở và gọi update_ui_text() của chúng
        # Sử dụng list(self._sub_windows) để tạo bản sao, tránh lỗi khi xóa phần tử trong vòng lặp
        for window in list(self._sub_windows):
            try:
                # Kiểm tra cửa sổ vẫn tồn tại (chưa bị đóng)
                if window.winfo_exists():
                    # Gọi phương thức update_ui_text() của cửa sổ con
                    window.update_ui_text()
            except Exception as e:
                # Ghi log lỗi (lệnh thư viện logger.error)
                logger.error(f"Lỗi khi cập nhật ngôn ngữ cho cửa sổ con: {e}")
                # Nếu lỗi, xóa cửa sổ khỏi danh sách (vì có thể nó đã bị đóng)
                if window in self._sub_windows:
                    self._sub_windows.remove(window)

    def get_localization(self):
        # Dòng trên: định nghĩa phương thức get_localization (do người dùng đặt)
        """Trả về từ điển chuỗi ký tự theo ngôn ngữ hiện tại (dùng trong các messagebox)."""
        # ^ Docstring

        # Trả về từ điển tương ứng với ngôn ngữ hiện tại (LANGUAGES là dict có khóa "vi", "en")
        return LANGUAGES[self.current_lang]

    # ------------------------------------------------------------------------
    # 3.4. QUẢN LÝ BỆNH NHÂN (CRUD)
    # ------------------------------------------------------------------------
    def get_all_patients(self):
        # Dòng trên: định nghĩa phương thức get_all_patients (do người dùng đặt)
        """
        Lấy toàn bộ dữ liệu bệnh nhân từ model.
        Trả về pandas.DataFrame.
        """
        # ^ Docstring

        # Gọi hàm get_all_patients từ model (do người dùng định nghĩa) và trả về kết quả
        return model.get_all_patients()

    def add_patient(self, name, birth_year, gender, phone, address):
        # Dòng trên: định nghĩa phương thức add_patient (do người dùng đặt)
        # Các tham số: name, birth_year, gender, phone, address – do người dùng truyền vào
        """Thêm bệnh nhân mới."""
        # ^ Docstring

        # Gọi hàm add_patient từ model (do người dùng định nghĩa)
        model.add_patient(name, birth_year, gender, phone, address)
        # Ghi log (lệnh thư viện)
        logger.info(f"Controller: Đã thêm bệnh nhân {name}")
        # Yêu cầu view làm mới bảng (cập nhật giao diện)
        self.view.refresh_table()

    def update_patient(self, pid, name, birth_year, gender, phone, address):
        # Dòng trên: định nghĩa phương thức update_patient (do người dùng đặt)
        """Cập nhật thông tin bệnh nhân."""
        # ^ Docstring

        model.update_patient(pid, name, birth_year, gender, phone, address)
        logger.info(f"Controller: Đã cập nhật bệnh nhân id {pid}")
        self.view.refresh_table()

    def delete_patient(self, pid):
        # Dòng trên: định nghĩa phương thức delete_patient (do người dùng đặt)
        """Xóa bệnh nhân theo id."""
        # ^ Docstring

        model.delete_patient(pid)
        logger.info(f"Controller: Đã xóa bệnh nhân id {pid}")
        self.view.refresh_table()

    # ------------------------------------------------------------------------
    # 3.5. IMPORT / EXPORT CSV
    # ------------------------------------------------------------------------
    def import_csv(self):
        # Dòng trên: định nghĩa phương thức import_csv (do người dùng đặt)
        """Import danh sách bệnh nhân từ file CSV (có xử lý ngôn ngữ và validation)."""
        # ^ Docstring

        # Import các module cần thiết (chỉ dùng trong hàm này)
        from tkinter import filedialog, messagebox
        import pandas as pd

        # Lấy từ điển ngôn ngữ hiện tại
        texts = self.get_localization()

        # Mở hộp thoại chọn file CSV (lệnh thư viện filedialog)
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        # Nếu người dùng hủy bỏ (không chọn file), thoát khỏi hàm
        if not filepath:
            return

        try:
            # Đọc file CSV, dtype=str giữ nguyên định dạng (không tự động chuyển số)
            df_import = pd.read_csv(filepath, dtype=str)

            # Danh sách các cột bắt buộc phải có
            required = ['name', 'birth_year', 'gender', 'phone', 'address']
            # Kiểm tra xem file có đủ các cột cần thiết không
            if not all(col in df_import.columns for col in required):
                # Tạo thông báo lỗi theo ngôn ngữ
                err_msg = ("File CSV phải có các cột: name, birth_year, gender, phone, address"
                           if self.current_lang == "vi"
                           else "CSV file must contain columns: name, birth_year, gender, phone, address")
                messagebox.showerror(texts["err_title"], err_msg)
                return

            count = 0  # Biến đếm số bệnh nhân import thành công

            # Duyệt từng dòng trong DataFrame
            for _, row in df_import.iterrows():
                # Lấy tên, bỏ khoảng trắng đầu cuối
                name = str(row['name']).strip()
                if not name:
                    continue  # Bỏ qua nếu tên rỗng

                # Xử lý năm sinh
                try:
                    birth_year = int(float(row['birth_year']))  # Chuyển sang số (có thể từ Excel thành float)
                    if birth_year < 1900 or birth_year > 2026:
                        continue  # Ngoài khoảng hợp lệ thì bỏ qua
                except:
                    continue  # Nếu không chuyển được thành số thì bỏ qua

                # Xử lý giới tính (chuẩn hóa về 'Nam' hoặc 'Nữ')
                gender = str(row['gender']).strip()
                if gender in ['Nam', 'Male']:
                    gender = 'Nam'
                elif gender in ['Nữ', 'Female']:
                    gender = 'Nữ'
                else:
                    gender = 'Nam'  # Mặc định là Nam

                # Xử lý số điện thoại
                phone_raw = str(row['phone']).strip()
                # Loại bỏ mọi ký tự không phải số (dấu cách, dấu gạch, chữ cái...)
                phone_digits = re.sub(r'\D', '', phone_raw)
                # Nếu chỉ còn 9 chữ số, thêm số 0 ở đầu (do Excel bỏ số 0)
                if len(phone_digits) == 9:
                    phone_digits = '0' + phone_digits
                # Nếu không đúng 10 số thì bỏ qua
                if len(phone_digits) != 10:
                    continue

                # Địa chỉ
                address = str(row['address']).strip()

                # Thêm bệnh nhân vào database
                model.add_patient(name, birth_year, gender, phone_digits, address)
                count += 1

            # Tạo thông báo thành công theo ngôn ngữ
            success_msg = ("Đã import thành công {count} bệnh nhân"
                           if self.current_lang == "vi"
                           else "Successfully imported {count} patients").format(count=count)
            messagebox.showinfo("Import CSV", success_msg)
            # Làm mới bảng dữ liệu trên giao diện
            self.view.refresh_table()
        except Exception as e:
            # Bắt lỗi chung (ví dụ file không đọc được)
            messagebox.showerror(texts["err_title"], f"{texts['msg_sys_error']}: {e}")

    def export_csv(self):
        # Dòng trên: định nghĩa phương thức export_csv (do người dùng đặt)
        """Xuất toàn bộ danh sách bệnh nhân ra file CSV."""
        # ^ Docstring

        from tkinter import filedialog, messagebox
        texts = self.get_localization()

        # Mở hộp thoại lưu file, mặc định đuôi .csv
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
        if filepath:
            # Lấy toàn bộ dữ liệu bệnh nhân dưới dạng DataFrame
            df = model.get_all_patients()
            # Xuất ra file CSV, không lưu chỉ mục, mã hóa utf-8-sig (hỗ trợ tiếng Việt)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            # Thông báo thành công theo ngôn ngữ
            success_msg = "Xuất dữ liệu thành công!" if self.current_lang == "vi" else "Data exported successfully!"
            messagebox.showinfo("Export CSV", success_msg)

    def export_template_csv(self):
        # Dòng trên: định nghĩa phương thức export_template_csv (do người dùng đặt)
        """Xuất file CSV mẫu (template) để người dùng nhập dữ liệu."""
        # ^ Docstring

        from tkinter import filedialog, messagebox
        texts = self.get_localization()

        # Hộp thoại lưu file, tên mặc định là patient_template.csv
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="patient_template.csv"
        )
        if filepath:
            # Nội dung mẫu của file CSV (3 dòng bệnh nhân)
            template_content = """name,birth_year,gender,phone,address
Nguyễn Văn A,1990,Nam,0912345678,Hà Nội
Trần Thị B,1995,Nữ,0987654321,TP. Hồ Chí Minh
Lê Văn C,2000,Nam,0977123456,Đà Nẵng
"""
            try:
                # Ghi nội dung vào file với mã hóa utf-8-sig
                with open(filepath, "w", encoding="utf-8-sig") as f:
                    f.write(template_content)
                success_msg = "Đã xuất file mẫu thành công!" if self.current_lang == "vi" else "Template exported successfully!"
                messagebox.showinfo("CSV Template", success_msg)
            except Exception as e:
                messagebox.showerror(texts["err_title"], f"{texts['msg_sys_error']}: {e}")

    # ------------------------------------------------------------------------
    # 3.6. QUẢN LÝ LỊCH SỬ KHÁM BỆNH
    # ------------------------------------------------------------------------
    def add_medical_visit(self, patient_id, visit_date, height, weight, systolic, diastolic,
                          diagnosis, prescription, ai_advice=""):
        # Dòng trên: định nghĩa phương thức add_medical_visit (do người dùng đặt)
        """Thêm lần khám mới kèm theo lời khuyên từ AI (nếu có)."""
        # ^ Docstring

        # Gọi hàm add_visit từ medical_model (do người dùng định nghĩa)
        medical_model.add_visit(patient_id, visit_date, height, weight, systolic,
                                 diastolic, diagnosis, prescription, ai_advice)
        # Ghi log
        logger.info(f"Controller: Đã thêm lượt khám cho bệnh nhân ID {patient_id}")

    def get_medical_history(self, patient_id):
        # Dòng trên: định nghĩa phương thức get_medical_history (do người dùng đặt)
        """Lấy lịch sử khám của bệnh nhân (bao gồm cả cột ai_advice)."""
        # ^ Docstring

        # Gọi hàm get_visits_by_patient từ medical_model (do người dùng định nghĩa)
        return medical_model.get_visits_by_patient(patient_id)

    def delete_medical_visit(self, visit_id):
        # Dòng trên: định nghĩa phương thức delete_medical_visit (do người dùng đặt)
        """Xóa lần khám theo id."""
        # ^ Docstring

        # Gọi hàm delete_visit từ medical_model (do người dùng định nghĩa)
        medical_model.delete_visit(visit_id)
        # Ghi log
        logger.info(f"Controller: Đã xóa lượt khám ID {visit_id}")

    # ------------------------------------------------------------------------
    # 3.7. TƯƠNG TÁC VỚI AI AGENT
    # ------------------------------------------------------------------------
    def ask_ai_for_advice(self, diagnosis, prescription):
        # Dòng trên: định nghĩa phương thức ask_ai_for_advice (do người dùng đặt)
        """
        Gửi chẩn đoán và đơn thuốc lên AI Agent, nhận về lời khuyên.
        """
        # ^ Docstring

        # Lấy từ điển ngôn ngữ hiện tại
        texts = self.get_localization()
        # Nếu AI Agent chưa được khởi tạo, trả về thông báo lỗi (theo ngôn ngữ)
        if not self.ai_agent_service:
            return texts["msg_no_ai_agent"]

        try:
            # Gọi phương thức analyze_medical_visit của AI Agent (do người dùng định nghĩa)
            # Chỉ truyền diagnosis và prescription (phiên bản đơn giản)
            advice = self.ai_agent_service.analyze_medical_visit(diagnosis, prescription)
            return advice
        except Exception as e:
            # Ghi log lỗi và trả về thông báo lỗi kết hợp nội dung lỗi
            logger.error(f"Lỗi AI: {e}")
            return f"{texts['msg_sys_error']}: {str(e)}"