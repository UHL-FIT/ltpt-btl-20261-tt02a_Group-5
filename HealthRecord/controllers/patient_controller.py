# controllers/patient_controller.py
# Điều phối giữa View và Model. Nhận yêu cầu từ view, gọi model, sau đó yêu cầu view cập nhật.

from models import patient as model
from utils.logger import get_logger
import re  # để xử lý số điện thoại
from models import medical as medical_model

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

    # ------------------ Import / Export CSV ------------------
    def import_csv(self):
        """Import danh sách bệnh nhân từ file CSV."""
        from tkinter import filedialog, messagebox
        import pandas as pd
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        try:
            df_import = pd.read_csv(filepath, dtype=str)  # đọc tất cả dưới dạng string
            required = ['name', 'birth_year', 'gender', 'phone', 'address']
            if not all(col in df_import.columns for col in required):
                messagebox.showerror("Lỗi", "File CSV phải có các cột: name, birth_year, gender, phone, address")
                return
            count = 0
            for _, row in df_import.iterrows():
                name = str(row['name']).strip()
                if not name:
                    continue
                try:
                    birth_year = int(float(row['birth_year']))  # xử lý số thực nếu từ Excel
                    if birth_year < 1900 or birth_year > 2025:
                        continue
                except:
                    continue
                gender = str(row['gender']).strip()
                if gender not in ['Nam', 'Nữ']:
                    gender = 'Nam'
                # Xử lý số điện thoại
                phone_raw = str(row['phone']).strip()
                phone_digits = re.sub(r'\D', '', phone_raw)
                if len(phone_digits) == 9:
                    phone_digits = '0' + phone_digits
                if len(phone_digits) != 10:
                    continue
                address = str(row['address']).strip()
                model.add_patient(name, birth_year, gender, phone_digits, address)
                count += 1
            messagebox.showinfo("Import CSV", f"Đã import thành công {count} bệnh nhân")
            self.view.refresh_table()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đọc file: {e}")

    def export_csv(self):
        """Xuất toàn bộ danh sách bệnh nhân ra file CSV."""
        from tkinter import filedialog, messagebox
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            df = model.get_all_patients()
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Export CSV", "Xuất dữ liệu thành công!")

    def export_template_csv(self):
        """Xuất file CSV mẫu để người dùng nhập dữ liệu."""
        from tkinter import filedialog, messagebox
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="patient_template.csv"
        )
        if filepath:
            template_content = """name,birth_year,gender,phone,address
Nguyễn Văn A,1990,Nam,0912345678,Hà Nội
Trần Thị B,1995,Nữ,0987654321,TP. Hồ Chí Minh
Lê Văn C,2000,Nam,0977123456,Đà Nẵng
"""
            try:
                with open(filepath, "w", encoding="utf-8-sig") as f:
                    f.write(template_content)
                messagebox.showinfo("Xuất mẫu CSV", "Đã xuất file mẫu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể ghi file: {e}")

        # Trong PatientController, thêm các dòng sau (đặt sau các phương thức CRUD bệnh nhân)

    from models import medical as medical_model   # thêm dòng import ở đầu file

    def get_medical_history(self, patient_id):
        """Lấy lịch sử khám của bệnh nhân"""
        return medical_model.get_visits_by_patient(patient_id)

    def add_medical_visit(self, patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription):
        """Thêm lần khám mới"""
        medical_model.add_visit(patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription)

    def delete_medical_visit(self, visit_id):
        """Xóa lần khám"""
        medical_model.delete_visit(visit_id)