# ============================================================================
# FILE: views/add_edit_patient.py
# MỤC ĐÍCH: Cửa sổ popup dùng để thêm mới hoặc sửa thông tin bệnh nhân.
#           Hỗ trợ validation dữ liệu, đa ngôn ngữ, chế độ modal.
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import customtkinter as ctk        # Lệnh import thư viện customtkinter (lệnh thư viện), đặt tên là ctk (do người dùng đặt)
import re                          # Lệnh import module re (biểu thức chính quy) – dùng xử lý số điện thoại (lệnh thư viện)
from config.languages import LANGUAGES   # Lệnh import biến LANGUAGES (từ điển) từ file config/languages.py (do người dùng định nghĩa)

# ============================================================================
# 2. ĐỊNH NGHĨA LỚP AddEditPatientWindow (popup thêm/sửa)
# ============================================================================
class AddEditPatientWindow(ctk.CTkToplevel):
    # Dòng trên: Khai báo class AddEditPatientWindow kế thừa từ ctk.CTkToplevel (lệnh thư viện)
    """
    Cửa sổ con (popup) dùng để thêm mới hoặc sửa thông tin bệnh nhân.
    Kế thừa từ ctk.CTkToplevel (cửa sổ độc lập, nằm trên cửa sổ chính).
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả class

    # ------------------------------------------------------------------------
    # 2.1. HÀM KHỞI TẠO (__init__) - TẠO GIAO DIỆN POPUP
    # ------------------------------------------------------------------------
    def __init__(self, parent, controller, edit_mode=False, patient_data=None):
        # Dòng trên: định nghĩa hàm khởi tạo (do người dùng định nghĩa)
        # parent: cửa sổ cha (MainView) – do người dùng truyền
        # controller: PatientController – do người dùng truyền
        # edit_mode: True nếu sửa, False nếu thêm – do người dùng truyền
        # patient_data: dict dữ liệu cũ (nếu sửa) – do người dùng truyền

        # Gọi constructor của lớp cha (CTkToplevel) – lệnh thư viện
        super().__init__(parent)

        # ---- Lưu các tham số vào thuộc tính (biến do người dùng đặt) ----
        self.controller = controller          # Lưu controller để gọi các hàm CRUD
        self.edit_mode = edit_mode            # Lưu chế độ sửa hay thêm
        self.patient_data = patient_data      # Lưu dữ liệu cũ (nếu sửa)

        # --------------------------------------------------------------------
        # 2.1.1. Đăng ký cửa sổ con với controller (nếu có quản lý sub-window)
        # --------------------------------------------------------------------
        # Kiểm tra xem controller có phương thức register_sub_window không (do người dùng định nghĩa)
        if hasattr(self.controller, "register_sub_window"):
            # Nếu có, gọi phương thức đó để đăng ký cửa sổ này (giúp controller quản lý và đồng bộ ngôn ngữ)
            self.controller.register_sub_window(self)

        # --------------------------------------------------------------------
        # 2.1.2. Thiết lập kích thước và chế độ modal (grab)
        # --------------------------------------------------------------------
        self.geometry("400x480")              # Đặt kích thước cửa sổ (lệnh thư viện): rộng 400 pixel, cao 480 pixel

        # ---- Fix cho Linux (đảm bảo cửa sổ luôn ở trên cùng và grab được) ----
        self.attributes("-topmost", True)      # Đặt cửa sổ luôn hiển thị trên cùng các cửa sổ khác (lệnh thư viện)
        self.wait_visibility()                 # Chờ cho cửa sổ hiển thị hoàn toàn (lệnh thư viện)
        self.grab_set()                        # Chế độ modal: không cho tương tác với cửa sổ cha cho đến khi đóng popup (lệnh thư viện)

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

        # --------------------------------------------------------------------
        # 2.1.3. Tạo các widget (label, entry, combobox) - ban đầu chưa có text
        # --------------------------------------------------------------------
        # Label "Họ tên" – lệnh thư viện CTkLabel, text sẽ được set sau bằng update_ui_text
        self.lbl_name = ctk.CTkLabel(self, text="")
        # Đặt label: cách lề trên 10, lề trái/phải 20, căn trái (anchor="w") (lệnh thư viện pack)
        self.lbl_name.pack(pady=(10, 0), padx=20, anchor="w")

        # Ô nhập Họ tên – lệnh thư viện CTkEntry, font Arial 13
        self.entry_name = ctk.CTkEntry(self, font=("Arial", 13))
        # Đặt ô nhập: lề dưới 5, lề trái/phải 20, kéo dãn chiều ngang (fill="x") (lệnh thư viện pack)
        self.entry_name.pack(pady=5, padx=20, fill="x")

        # Label "Năm sinh"
        self.lbl_birth = ctk.CTkLabel(self, text="")
        self.lbl_birth.pack(pady=(10, 0), padx=20, anchor="w")

        # Ô nhập Năm sinh
        self.entry_birth = ctk.CTkEntry(self, font=("Arial", 13))
        self.entry_birth.pack(pady=5, padx=20, fill="x")

        # Label "Giới tính"
        self.lbl_gender = ctk.CTkLabel(self, text="")
        self.lbl_gender.pack(pady=(10, 0), padx=20, anchor="w")

        # Biến lưu giá trị giới tính (StringVar của customtkinter) – do người dùng đặt
        self.gender_var = ctk.StringVar()

        # Combobox chọn giới tính (lệnh thư viện CTkComboBox)
        self.combo_gender = ctk.CTkComboBox(self, variable=self.gender_var, font=("Arial", 13))
        # Đặt combobox: lề dưới 5, lề trái/phải 20, kéo dãn chiều ngang
        self.combo_gender.pack(pady=5, padx=20, fill="x")

        # Label "Số điện thoại"
        self.lbl_phone = ctk.CTkLabel(self, text="")
        self.lbl_phone.pack(pady=(10, 0), padx=20, anchor="w")

        # Ô nhập Số điện thoại
        self.entry_phone = ctk.CTkEntry(self, font=("Arial", 13))
        self.entry_phone.pack(pady=5, padx=20, fill="x")

        # Label "Địa chỉ"
        self.lbl_address = ctk.CTkLabel(self, text="")
        self.lbl_address.pack(pady=(10, 0), padx=20, anchor="w")

        # Ô nhập Địa chỉ
        self.entry_address = ctk.CTkEntry(self, font=("Arial", 13))
        self.entry_address.pack(pady=5, padx=20, fill="x")

        # ---- Khung chứa các nút (Lưu và Hủy) ----
        btn_frame = ctk.CTkFrame(self)       # Tạo frame để chứa hai nút (lệnh thư viện CTkFrame)
        btn_frame.pack(pady=20)              # Đặt frame: lề dưới 20 pixel

        # Nút Lưu (lệnh thư viện CTkButton), command=self.save
        self.btn_save = ctk.CTkButton(btn_frame, text="", command=self.save)
        # Đặt nút bên trái, cách nút Hủy 10 pixel
        self.btn_save.pack(side="left", padx=10)

        # Nút Hủy (đóng popup), command=self.destroy
        self.btn_cancel = ctk.CTkButton(btn_frame, text="", command=self.destroy)
        self.btn_cancel.pack(side="left", padx=10)

        # --------------------------------------------------------------------
        # 2.1.4. Cập nhật văn bản lần đầu (theo ngôn ngữ)
        # --------------------------------------------------------------------
        self.update_ui_text()                 # Gọi phương thức đồng bộ ngôn ngữ (do người dùng định nghĩa)

        # --------------------------------------------------------------------
        # 2.1.5. Nếu là chế độ sửa, điền dữ liệu cũ vào các ô
        # --------------------------------------------------------------------
        if edit_mode and patient_data:
            # Chèn tên cũ vào ô name (lệnh thư viện insert)
            self.entry_name.insert(0, patient_data.get("name", ""))
            # Chèn năm sinh cũ vào ô birth_year (chuyển thành chuỗi)
            self.entry_birth.insert(0, str(patient_data.get("birth_year", "")))
            # Chèn số điện thoại cũ
            self.entry_phone.insert(0, patient_data.get("phone", ""))
            # Chèn địa chỉ cũ
            self.entry_address.insert(0, patient_data.get("address", ""))

            # Lấy giới tính cũ (lưu trong DB là "Nam" hoặc "Nữ")
            old_gender = patient_data.get("gender", "Nam")
            # Lấy mã ngôn ngữ hiện tại từ controller (mặc định "vi")
            lang_code = getattr(self.controller, "current_lang", "vi")
            # Chuyển hiển thị theo ngôn ngữ: nếu là tiếng Anh thì "Male"/"Female"
            if lang_code == "en":
                self.gender_var.set("Male" if old_gender == "Nam" else "Female")
            else:
                self.gender_var.set(old_gender)

        # --------------------------------------------------------------------
        # 2.1.6. Sửa lỗi bộ gõ tiếng Việt trên Linux/Windows (IME delay)
        # --------------------------------------------------------------------
        # Khi gõ tiếng Việt, đôi khi ký tự không hiện ngay; dùng after để update
        for entry in [self.entry_name, self.entry_birth, self.entry_phone, self.entry_address]:
            # Gán sự kiện KeyRelease: khi thả phím, sau 1 mili giây gọi update_idletasks
            entry.bind("<KeyRelease>", lambda event: event.widget.after(1, lambda: event.widget.update_idletasks()))

    # ------------------------------------------------------------------------
    # 2.2. PHƯƠNG THỨC ĐỒNG BỘ NGÔN NGỮ (UI TEXT)
    # ------------------------------------------------------------------------
    def update_ui_text(self):
        """Cập nhật nhãn, placeholder, tiêu đề cửa sổ theo ngôn ngữ hiện tại."""
        # Lấy mã ngôn ngữ từ controller (nếu có), mặc định "vi"
        lang_code = getattr(self.controller, "current_lang", "vi")
        # Lấy bảng từ điển tương ứng (ví dụ LANGUAGES["vi"] hoặc LANGUAGES["en"])
        self.texts = LANGUAGES[lang_code]

        # Đặt tiêu đề cửa sổ (thêm " - Sửa" nếu edit_mode)
        if self.edit_mode:
            self.title(self.texts["title_edit"])      # Ví dụ: "Sửa bệnh nhân"
        else:
            self.title(self.texts["title_add"])       # Ví dụ: "Thêm bệnh nhân"

        # Cập nhật nhãn (label)
        self.lbl_name.configure(text=self.texts["lbl_name"])          # "Họ tên:"
        self.lbl_birth.configure(text=self.texts["lbl_birth"])        # "Năm sinh:"
        self.lbl_gender.configure(text=self.texts["lbl_gender"])      # "Giới tính:"
        self.lbl_phone.configure(text=self.texts["lbl_phone"])        # "Số điện thoại:"
        self.lbl_address.configure(text=self.texts["lbl_address"])    # "Địa chỉ:"

        # Cập nhật placeholder (gợi ý trong ô nhập)
        self.entry_name.configure(placeholder_text=self.texts["plh_name"])        # "Nhập họ tên"
        self.entry_birth.configure(placeholder_text=self.texts["plh_birth"])      # "1990"
        self.entry_address.configure(placeholder_text=self.texts["plh_address"])  # "Địa chỉ"

        # Cập nhật văn bản trên nút
        self.btn_save.configure(text=self.texts["btn_save"])          # "Lưu"
        self.btn_cancel.configure(text=self.texts["btn_cancel"])      # "Hủy"

        # Cập nhật danh sách giới tính trong combobox (VD: ["Nam", "Nữ"] hoặc ["Male","Female"])
        # Lấy giá trị hiện tại của combobox
        curr_g = self.gender_var.get()
        # Đặt lại các giá trị có thể chọn
        self.combo_gender.configure(values=[self.texts["gender_male"], self.texts["gender_female"]])
        # Khôi phục lựa chọn hiện tại theo ngôn ngữ mới
        if curr_g in ["Nam", "Male"]:
            self.gender_var.set(self.texts["gender_male"])
        elif curr_g in ["Nữ", "Female"]:
            self.gender_var.set(self.texts["gender_female"])
        else:
            self.gender_var.set(self.texts["gender_male"])

    # ------------------------------------------------------------------------
    # 2.3. HIỂN THỊ HỘP THOẠI LỖI TÙY CHỈNH (THAY MESSAGEBOX)
    # ------------------------------------------------------------------------
    def show_error_dialog(self, title, message):
        """Tạo một cửa sổ lỗi nhỏ gọn, modal, thay thế messagebox."""
        # Tạo cửa sổ con (lệnh thư viện CTkToplevel)
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)                      # Đặt tiêu đề
        dialog.geometry("320x150")               # Đặt kích thước
        dialog.resizable(False, False)           # Không cho phép thay đổi kích thước
        dialog.attributes("-topmost", True)      # Đặt cửa sổ luôn trên cùng
        dialog.wait_visibility()                 # Chờ cửa sổ hiển thị hoàn toàn
        dialog.grab_set()                        # Chế độ modal

        # Căn giữa dialog so với cửa sổ cha (self)
        x = self.winfo_x() + (self.winfo_width() // 2) - 160
        y = self.winfo_y() + (self.winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")

        # Label hiển thị thông báo (lệnh thư viện CTkLabel)
        lbl = ctk.CTkLabel(dialog, text=message, wraplength=280, font=("Arial", 13))
        lbl.pack(expand=True, padx=20, pady=(20, 10))   # Đặt label, có giãn cách

        # Nút đóng (lệnh thư viện CTkButton)
        btn = ctk.CTkButton(dialog, text=self.texts["close"], width=80, command=dialog.destroy)
        btn.pack(pady=(0, 20))                  # Đặt nút, lề dưới 20

    # ------------------------------------------------------------------------
    # 2.4. PHƯƠNG THỨC LƯU DỮ LIỆU (VALIDATION VÀ GỌI CONTROLLER)
    # ------------------------------------------------------------------------
    def save(self):
        """Lấy dữ liệu từ form, kiểm tra hợp lệ, gọi controller để thêm hoặc sửa."""
        # Lấy giá trị từ các ô, strip() để bỏ khoảng trắng đầu cuối
        name = self.entry_name.get().strip()
        birth_str = self.entry_birth.get().strip()
        gender_display = self.gender_var.get()          # Có thể là "Nam"/"Nữ" hoặc "Male"/"Female"
        phone_raw = self.entry_phone.get().strip()
        address = self.entry_address.get().strip()

        # ---------- Kiểm tra Họ tên ----------
        if not name:
            self.show_error_dialog(self.texts["err_title"], self.texts["err_empty_name"])
            return

        # ---------- Kiểm tra Năm sinh ----------
        if not birth_str:
            self.show_error_dialog(self.texts["err_title"], self.texts["err_empty_birth"])
            return
        try:
            birth_year = int(birth_str)
            if birth_year < 1900 or birth_year > 2026:
                raise ValueError
        except ValueError:
            self.show_error_dialog(self.texts["err_title"], self.texts["err_invalid_birth"])
            return

        # ---------- Kiểm tra Số điện thoại (chuẩn hóa) ----------
        # Loại bỏ tất cả ký tự không phải số (dấu cách, gạch ngang, chữ cái...)
        phone_digits = re.sub(r'\D', '', phone_raw)
        # Yêu cầu đúng 10 chữ số
        if len(phone_digits) != 10:
            self.show_error_dialog(self.texts["err_title"], self.texts["err_invalid_phone"])
            return

        # ---------- Chuyển đổi giới tính từ hiển thị về giá trị lưu DB ----------
        # Nếu gender_display là "Nam" hoặc "Male" → lưu "Nam"; nếu là "Nữ" hoặc "Female" → lưu "Nữ"
        gender = "Nam" if gender_display in ["Nam", "Male"] else "Nữ"

        # ---------- Gọi controller tương ứng ----------
        if self.edit_mode:
            # Sửa: cập nhật bệnh nhân với ID cũ
            self.controller.update_patient(
                self.patient_data["id"], name, birth_year, gender, phone_digits, address
            )
        else:
            # Thêm mới
            self.controller.add_patient(name, birth_year, gender, phone_digits, address)

        # Đóng popup sau khi lưu thành công
        self.destroy()

    # ------------------------------------------------------------------------
    # 2.5. PHƯƠNG THỨC HỦY (OVERRIDE DESTROY ĐỂ HỦY ĐĂNG KÝ)
    # ------------------------------------------------------------------------
    def destroy(self):
        """Hủy đăng ký cửa sổ con (nếu có) trước khi đóng."""
        if hasattr(self.controller, "unregister_sub_window"):
            self.controller.unregister_sub_window(self)
        super().destroy()            # Gọi destroy của lớp cha (đóng cửa sổ)