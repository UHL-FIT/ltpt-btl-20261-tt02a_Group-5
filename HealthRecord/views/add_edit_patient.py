# views/add_edit_patient.py
import customtkinter as ctk
import re
from config.languages import LANGUAGES

# 🔥 IMPORT Helper bộ gõ tiếng Việt toàn cục
from utils.ime_helper import LinuxIMEHelper

class AddEditPatientWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, edit_mode=False, patient_data=None):
        super().__init__(parent)
        self.controller = controller
        self.edit_mode = edit_mode
        self.patient_data = patient_data
        
        # Đăng ký cửa sổ này vào danh sách quản lý của MainWindow/Controller nếu có
        if hasattr(self.controller, "register_sub_window"):
            self.controller.register_sub_window(self)

        # 🛠️ TĂNG CHIỀU CAO LÊN 530: Đảm bảo giao diện thông thoáng, không bị tràn nút xuống dưới
        self.geometry("400x530")
        self.resizable(False, False)
        
        # Linux Grab Fix
        self.attributes("-topmost", True)
        self.wait_visibility()  
        self.grab_set()       

        # ---- Căn giữa popup so với cửa sổ cha (MainView) ----
        self.update_idletasks()                # Cập nhật kích thước thực tế của popup sau khi tạo các widget (lệnh thư viện)
        parent_x = parent.winfo_x()            # Lấy tọa độ X của cửa sổ cha (lệnh thư viện winfo_x)
        parent_y = parent.winfo_y()            # Lấy tọa độ Y của cửa sổ cha (lệnh thư viện winfo_y)
        parent_w = parent.winfo_width()        # Lấy chiều rộng của cửa sổ cha (lệnh thư viện winfo_width)
        parent_h = parent.winfo_height()       # Lấy chiều cao của cửa sổ cha (lệnh thư viện winfo_height)
        # Tính toán tọa độ X: (tọa độ trái cha + nửa chiều rộng cha) - nửa chiều rộng popup
        x = parent_x + (parent_w // 2) - (self.winfo_width() // 2)
        # Tính toán tọa độ Y: (tọa độ trên cha + nửa chiều cao cha) - nửa chiều cao popup
        y = parent_y + (parent_h // 2) - (self.winfo_height() // 2)
        # Đặt vị trí cửa sổ tại tọa độ (x, y) mà không thay đổi kích thước (lệnh thư viện geometry với dấu +)
        self.geometry(f"+{x}+{y}")  

        self.lang = self.controller.current_lang if self.controller else "vi"
        self.texts = LANGUAGES[self.lang]

        # =========================================================================
        # 🏗️ THIẾT KẾ CÁC THÀNH PHẦN GIAO DIỆN (WIDGETS)
        # =========================================================================
        # --- Họ tên ---
        self.lbl_name = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_name.pack(pady=(12, 0), padx=25, anchor="w")
        self.entry_name = ctk.CTkEntry(self, font=("Arial", 13), height=32)
        self.entry_name.pack(pady=4, padx=25, fill="x")

        # --- Năm sinh ---
        self.lbl_birth = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_birth.pack(pady=(10, 0), padx=25, anchor="w")
        self.entry_birth = ctk.CTkEntry(self, font=("Arial", 13), height=32)
        self.entry_birth.pack(pady=4, padx=25, fill="x")

        # --- Giới tính ---
        self.lbl_gender = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_gender.pack(pady=(10, 0), padx=25, anchor="w")
        self.combo_gender = ctk.CTkComboBox(self, values=[], state="readonly", height=32)
        self.combo_gender.pack(pady=4, padx=25, fill="x")

        # --- Số điện thoại ---
        self.lbl_phone = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_phone.pack(pady=(10, 0), padx=25, anchor="w")
        self.entry_phone = ctk.CTkEntry(self, font=("Arial", 13), height=32)
        self.entry_phone.pack(pady=4, padx=25, fill="x")

        # --- Địa chỉ ---
        self.lbl_address = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_address.pack(pady=(10, 0), padx=25, anchor="w")
        self.entry_address = ctk.CTkEntry(self, font=("Arial", 13), height=32)
        self.entry_address.pack(pady=4, padx=25, fill="x")

        # --- Vùng chứa nút bấm hành động ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25, padx=25, fill="x")

        self.btn_save = ctk.CTkButton(btn_frame, text="", font=("Arial", 13, "bold"), fg_color="#10B981", hover_color="#059669", height=36, command=self.save_patient)
        self.btn_save.pack(side="left", expand=True, padx=6)

        self.btn_cancel = ctk.CTkButton(btn_frame, text="", font=("Arial", 13, "bold"), fg_color="#7F8C8D", hover_color="#95A5A6", height=36, command=self.destroy)
        self.btn_cancel.pack(side="right", expand=True, padx=6)

        self.update_languages()
        self.load_patient_data()

        # 🔥 ÁP DỤNG bộ gõ Telex thông minh đồng bộ toàn cục cho Linux tại đây
        widgets_to_fix = [self.entry_name, self.entry_birth, self.entry_phone, self.entry_address]
        LinuxIMEHelper.apply_ime_to_widgets(self, widgets_to_fix)

    # =========================================================================
    # 🌟 HỘP THOẠI BÁO LỖI TỰ CHẾ NỔI TRÊN CÙNG (FIX CHÌM CỬA SỔ)
    # =========================================================================
    def show_custom_error(self, title, message):
        """Tạo hộp thoại thông báo lỗi bằng CustomTkinter ép nổi lên bề mặt."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x160")
        dialog.resizable(False, False)
        
        # Cấp quyền ưu tiên đè lên trên AddEditPatientWindow
        dialog.attributes("-topmost", True)
        dialog.wait_visibility()
        dialog.grab_set() 
        
        # Tọa độ chính giữa cửa sổ cha
        x = self.winfo_x() + (self.winfo_width() // 2) - 175
        y = self.winfo_y() + (self.winfo_height() // 2) - 80
        dialog.geometry(f"+{x}+{y}")

        lbl = ctk.CTkLabel(dialog, text=message, wraplength=310, font=("Segoe UI", 13))
        lbl.pack(expand=True, padx=20, pady=(20, 10))
        
        btn = ctk.CTkButton(dialog, text=self.texts.get("close", "Đóng"), width=90, fg_color="#FF0844", hover_color="#D90434", command=dialog.destroy)
        btn.pack(pady=(0, 20))

    def update_languages(self):
        if self.controller:
            self.lang = self.controller.current_lang
        self.texts = LANGUAGES[self.lang]

        title = self.texts["title_edit"] if self.edit_mode else self.texts["title_add"]
        self.title(title)

        self.lbl_name.configure(text=self.texts["lbl_name"])
        self.entry_name.configure(placeholder_text=self.texts["plh_name"])
        
        self.lbl_birth.configure(text=self.texts["lbl_birth"])
        self.entry_birth.configure(placeholder_text=self.texts["plh_birth"])
        
        self.lbl_gender.configure(text=self.texts["lbl_gender"])
        self.combo_gender.configure(values=[self.texts["gender_male"], self.texts["gender_female"]])
        if not self.edit_mode:
            self.combo_gender.set(self.texts["gender_male"])

        self.lbl_phone.configure(text=self.texts["lbl_phone"])
        self.entry_phone.configure(placeholder_text="09xxxxxxxx")
        
        self.lbl_address.configure(text=self.texts["lbl_address"])
        self.entry_address.configure(placeholder_text=self.texts["plh_address"])

        self.btn_save.configure(text=self.texts["btn_save"])
        self.btn_cancel.configure(text=self.texts["btn_cancel"])

    def load_patient_data(self):
        if self.edit_mode and self.patient_data:
            self.entry_name.insert(0, str(self.patient_data.get("name", "")))
            self.entry_birth.insert(0, str(self.patient_data.get("birth_year", "")))
            
            gender_db = self.patient_data.get("gender", "Nam")
            if gender_db == "Nam":
                self.combo_gender.set(self.texts["gender_male"])
            else:
                self.combo_gender.set(self.texts["gender_female"])

            self.entry_phone.insert(0, str(self.patient_data.get("phone", "")))
            self.entry_address.insert(0, str(self.patient_data.get("address", "")))

    def save_patient(self):
        name = self.entry_name.get().strip()
        birth = self.entry_birth.get().strip()
        
        selected_gender = self.combo_gender.get()
        gender = "Nam" if selected_gender == self.texts["gender_male"] else "Nữ"
        
        phone = self.entry_phone.get().strip()
        address = self.entry_address.get().strip()

        # 🔥 ĐÃ THAY ĐỔI: Chuyển toàn bộ sang hộp thoại báo lỗi show_custom_error độc quyền nổi lên trên
        if not name:
            self.show_custom_error(self.texts["err_title"], self.texts["err_empty_name"])
            return
        if not birth:
            self.show_custom_error(self.texts["err_title"], self.texts["err_empty_birth"])
            return
        if not birth.isdigit() or not (1900 <= int(birth) <= 2026):
            self.show_custom_error(self.texts["err_title"], self.texts["err_invalid_birth"])
            return
        if phone and not re.match(r"^\d{10}$", phone):
            self.show_custom_error(self.texts["err_title"], self.texts["err_invalid_phone"])
            return

        if self.edit_mode:
            p_id = self.patient_data["id"]
            self.controller.update_patient(p_id, name, birth, gender, phone, address)
        else:
            self.controller.add_patient(name, birth, gender, phone, address)
        
        self.destroy()

    def destroy(self):
        if hasattr(self.controller, "unregister_sub_window"):
            self.controller.unregister_sub_window(self)
        super().destroy()