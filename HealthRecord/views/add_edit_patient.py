# views/add_edit_patient.py
import customtkinter as ctk
from tkinter import messagebox
import re

class AddEditPatientWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, edit_mode=False, patient_data=None):
        super().__init__(parent)
        self.controller = controller
        self.edit_mode = edit_mode
        self.patient_data = patient_data

        if edit_mode:
            self.title("Sửa bệnh nhân")
        else:
            self.title("Thêm bệnh nhân")

        self.geometry("400x450")
        self.resizable(True, True)
        self.grab_set()

        # Họ tên
        lbl_name = ctk.CTkLabel(self, text="Họ tên:")
        lbl_name.pack(pady=(10, 0), padx=20, anchor="w")
        self.entry_name = ctk.CTkEntry(self, placeholder_text="Nhập họ tên")
        self.entry_name.pack(pady=5, padx=20, fill="x")

        # Năm sinh
        lbl_birth = ctk.CTkLabel(self, text="Năm sinh:")
        lbl_birth.pack(pady=(10, 0), padx=20, anchor="w")
        self.entry_birth = ctk.CTkEntry(self, placeholder_text="VD: 1990")
        self.entry_birth.pack(pady=5, padx=20, fill="x")

        # Giới tính
        lbl_gender = ctk.CTkLabel(self, text="Giới tính:")
        lbl_gender.pack(pady=(10, 0), padx=20, anchor="w")
        self.gender_var = ctk.StringVar(value="Nam")
        self.combo_gender = ctk.CTkComboBox(self, values=["Nam", "Nữ"], variable=self.gender_var)
        self.combo_gender.pack(pady=5, padx=20, fill="x")

        # Số điện thoại
        lbl_phone = ctk.CTkLabel(self, text="Số điện thoại (10 số):")
        lbl_phone.pack(pady=(10, 0), padx=20, anchor="w")
        self.entry_phone = ctk.CTkEntry(self, placeholder_text="0912345678")
        self.entry_phone.pack(pady=5, padx=20, fill="x")

        # Địa chỉ
        lbl_address = ctk.CTkLabel(self, text="Địa chỉ:")
        lbl_address.pack(pady=(10, 0), padx=20, anchor="w")
        self.entry_address = ctk.CTkEntry(self, placeholder_text="Địa chỉ")
        self.entry_address.pack(pady=5, padx=20, fill="x")

        if edit_mode and patient_data:
            self.entry_name.insert(0, patient_data.get("name", ""))
            self.entry_birth.insert(0, str(patient_data.get("birth_year", "")))
            self.gender_var.set(patient_data.get("gender", "Nam"))
            self.entry_phone.insert(0, patient_data.get("phone", ""))
            self.entry_address.insert(0, patient_data.get("address", ""))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=20)
        self.btn_save = ctk.CTkButton(btn_frame, text="Lưu", command=self.save)
        self.btn_save.pack(side="left", padx=10)
        self.btn_cancel = ctk.CTkButton(btn_frame, text="Hủy", command=self.destroy)
        self.btn_cancel.pack(side="left", padx=10)

    def save(self):
        name = self.entry_name.get().strip()
        birth_str = self.entry_birth.get().strip()
        gender = self.gender_var.get()
        phone_raw = self.entry_phone.get().strip()
        address = self.entry_address.get().strip()

        # 1. Kiểm tra họ tên
        if not name:
            messagebox.showerror("Lỗi", "Họ tên không được để trống")
            return

        # 2. Kiểm tra năm sinh
        if not birth_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập năm sinh")
            return
        try:
            birth_year = int(birth_str)
            if birth_year < 1900 or birth_year > 2025:
                raise ValueError
        except:
            messagebox.showerror("Lỗi", "Năm sinh phải là số từ 1900 đến 2025")
            return

        # 3. Kiểm tra số điện thoại: chỉ giữ số, bắt buộc đủ 10 chữ số
        phone_digits = re.sub(r'\D', '', phone_raw)  # Xóa mọi ký tự không phải số
        if len(phone_digits) != 10:
            messagebox.showerror("Lỗi", "Số điện thoại phải có đúng 10 chữ số (VD: 0912345678)")
            return
        phone = phone_digits  # Dùng số đã chuẩn hóa

        # 4. Gọi controller
        if self.edit_mode:
            self.controller.update_patient(
                self.patient_data["id"],
                name, birth_year, gender, phone, address
            )
        else:
            self.controller.add_patient(name, birth_year, gender, phone, address)

        self.destroy()