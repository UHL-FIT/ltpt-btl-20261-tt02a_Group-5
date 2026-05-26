# ============================================================================
# FILE: views/medical_history.py
# MỤC ĐÍCH: Cửa sổ popup hiển thị và quản lý lịch sử khám bệnh của một bệnh nhân.
#           Cho phép thêm, xóa lần khám, gọi AI tư vấn (dựa trên chẩn đoán và đơn thuốc).
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import customtkinter as ctk                # Lệnh import thư viện customtkinter (lệnh thư viện), đặt tên viết tắt là ctk (do người dùng đặt)
from tkinter import ttk, messagebox       # Lệnh import ttk (bảng Treeview) và messagebox (hộp thoại) từ tkinter (lệnh thư viện)
from datetime import datetime             # Lệnh import module datetime để xử lý ngày giờ (lệnh thư viện)
from config.languages import LANGUAGES    # Lệnh import biến LANGUAGES (từ điển) từ file config/languages.py (do người dùng định nghĩa)

# ============================================================================
# 2. ĐỊNH NGHĨA LỚP MedicalHistoryWindow (popup lịch sử khám)
# ============================================================================
class MedicalHistoryWindow(ctk.CTkToplevel):
    # Dòng trên: Khai báo class MedicalHistoryWindow kế thừa từ ctk.CTkToplevel (lệnh thư viện)
    """
    Lớp cửa sổ con (popup) hiển thị lịch sử khám bệnh của một bệnh nhân.
    Kế thừa từ ctk.CTkToplevel (cửa sổ độc lập).
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả class

    # ------------------------------------------------------------------------
    # 2.1. HÀM KHỞI TẠO (__init__) - TẠO GIAO DIỆN POPUP
    # ------------------------------------------------------------------------
    def __init__(self, parent, controller, patient_data):
        # Dòng trên: định nghĩa hàm khởi tạo (do người dùng định nghĩa)
        # parent: cửa sổ cha (MainView) – do người dùng truyền
        # controller: PatientController – do người dùng truyền
        # patient_data: dict chứa thông tin bệnh nhân – do người dùng truyền

        # Gọi constructor của lớp cha (CTkToplevel) – lệnh thư viện
        super().__init__(parent)

        # ---- Lưu các tham số vào thuộc tính (biến do người dùng đặt) ----
        self.controller = controller            # Lưu controller để gọi các hàm CRUD lịch sử khám
        self.patient_id = patient_data.get("id")        # Lấy id bệnh nhân từ dict (dùng get để tránh lỗi nếu thiếu key)
        self.patient_name = patient_data.get("name")    # Lấy tên bệnh nhân, dùng để hiển thị trên tiêu đề

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
        self.geometry("1000x550")                 # Đặt kích thước cửa sổ (lệnh thư viện): rộng 1000 pixel, cao 550 pixel
        self.attributes("-topmost", True)         # Đặt cửa sổ luôn hiển thị trên cùng các cửa sổ khác (lệnh thư viện)
        self.wait_visibility()                    # Chờ cho cửa sổ hiển thị hoàn toàn (lệnh thư viện)
        self.grab_set()                           # Chế độ modal: không cho tương tác với cửa sổ cha cho đến khi đóng popup (lệnh thư viện)

        # --------------------------------------------------------------------
        # Căn giữa popup so với cửa sổ cha (MainView)
        # --------------------------------------------------------------------
        self.update_idletasks()                   # Cập nhật kích thước thực tế của popup sau khi tạo các widget (lệnh thư viện)
        parent_x = parent.winfo_x()               # Lấy tọa độ X của cửa sổ cha (lệnh thư viện winfo_x)
        parent_y = parent.winfo_y()               # Lấy tọa độ Y của cửa sổ cha (lệnh thư viện winfo_y)
        parent_w = parent.winfo_width()           # Lấy chiều rộng của cửa sổ cha (lệnh thư viện winfo_width)
        parent_h = parent.winfo_height()          # Lấy chiều cao của cửa sổ cha (lệnh thư viện winfo_height)
        # Tính toán tọa độ X: (tọa độ trái cha + nửa chiều rộng cha) - nửa chiều rộng popup
        x = parent_x + (parent_w // 2) - (self.winfo_width() // 2)
        # Tính toán tọa độ Y: (tọa độ trên cha + nửa chiều cao cha) - nửa chiều cao popup
        y = parent_y + (parent_h // 2) - (self.winfo_height() // 2)
        # Đặt vị trí cửa sổ tại tọa độ (x, y) mà không thay đổi kích thước (lệnh thư viện geometry với dấu +)
        self.geometry(f"+{x}+{y}")

        # ====================================================================
        # 2.1.3. TẠO FORM NHẬP LIỆU PHÍA TRÊN
        # ====================================================================
        self.form_frame = ctk.CTkFrame(self)      # Tạo một Frame (khung) để chứa các widget nhập liệu (lệnh thư viện CTkFrame)
        # Đặt khung: cách lề trên 10, lề trái/phải 10, kéo dãn chiều ngang (lệnh thư viện pack)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # ---------- Ngày khám ----------
        # Label "Ngày khám" (lệnh thư viện CTkLabel), text sẽ được set sau bằng update_ui_text
        self.lbl_date = ctk.CTkLabel(self.form_frame, text="")
        # Đặt label bằng grid: hàng 0, cột 0, cách các cạnh 5 pixel, căn phải (sticky="e") (lệnh thư viện grid)
        self.lbl_date.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        # Ô nhập liệu cho ngày khám (lệnh thư viện CTkEntry), chiều rộng 120 pixel
        self.entry_date = ctk.CTkEntry(self.form_frame, width=120)
        # Chèn ngày hiện tại vào ô (lệnh thư viện insert), định dạng YYYY-MM-DD
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        # Đặt ô nhập ở hàng 0, cột 1 (lệnh thư viện grid)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        # ---------- Chiều cao ----------
        # Label "Chiều cao" – lệnh thư viện CTkLabel
        self.lbl_height = ctk.CTkLabel(self.form_frame, text="")
        # Đặt label ở hàng 0, cột 2, căn phải
        self.lbl_height.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        # Ô nhập chiều cao, rộng 80 pixel
        self.entry_height = ctk.CTkEntry(self.form_frame, width=80)
        # Đặt ô nhập ở hàng 0, cột 3
        self.entry_height.grid(row=0, column=3, padx=5, pady=5)

        # ---------- Cân nặng ----------
        # Label "Cân nặng"
        self.lbl_weight = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_weight.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        # Ô nhập cân nặng
        self.entry_weight = ctk.CTkEntry(self.form_frame, width=80)
        self.entry_weight.grid(row=0, column=5, padx=5, pady=5)

        # ---------- Huyết áp tâm thu ----------
        self.lbl_systolic = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_systolic.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_systolic = ctk.CTkEntry(self.form_frame, width=80)
        self.entry_systolic.grid(row=1, column=1, padx=5, pady=5)

        # ---------- Huyết áp tâm trương ----------
        self.lbl_diastolic = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_diastolic.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_diastolic = ctk.CTkEntry(self.form_frame, width=80)
        self.entry_diastolic.grid(row=1, column=3, padx=5, pady=5)

        # ---------- Chẩn đoán ----------
        self.lbl_diagnosis = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_diagnosis.grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.entry_diagnosis = ctk.CTkEntry(self.form_frame, width=150)
        self.entry_diagnosis.grid(row=1, column=5, padx=5, pady=5)

        # ---------- Thuốc kê ----------
        self.lbl_prescription = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_prescription.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_prescription = ctk.CTkEntry(self.form_frame, width=300)
        # colspan=5: chiếm từ cột 1 đến 5; sticky="ew": kéo dãn theo chiều ngang
        self.entry_prescription.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        # ---------- Nút Thêm lần khám ----------
        self.btn_add = ctk.CTkButton(self.form_frame, text="", command=self.add_visit)
        # Đặt nút ở hàng 3, cột 0, chiếm 2 cột, căn đều ngang, có padding
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        # ---------- Nút AI tư vấn ----------
        # Nút AI có màu nền #8E44AD, màu hover #732D91, khi bấm gọi hàm ask_ai
        self.btn_ai = ctk.CTkButton(
            self.form_frame, text="", fg_color="#8E44AD", hover_color="#732D91",
            command=self.ask_ai
        )
        # Đặt nút AI ở hàng 3, cột 2, chiếm 4 cột, căn đều ngang
        self.btn_ai.grid(row=3, column=2, columnspan=4, pady=10, padx=5, sticky="ew")

        # ====================================================================
        # 2.1.4. PHẦN HIỂN THỊ DỮ LIỆU (Bảng lịch sử + AI Agent)
        # ====================================================================
        # ---- Khung chứa bảng và nút xóa (bên trái) ----
        # Tạo frame làm nền, màu trong suốt (lệnh thư viện CTkFrame)
        main_bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Đặt frame này: kéo dãn cả chiều ngang và dọc, chiếm không gian dư, lề 10, lề dưới 5
        main_bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame con bên trái (chứa bảng)
        left_data_frame = ctk.CTkFrame(main_bottom_frame, fg_color="transparent")
        # Đặt frame bên trái, kéo dãn cả hai chiều, lề phải 5
        left_data_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Bảng Treeview hiển thị lịch sử khám (8 cột)
        self.tree = ttk.Treeview(
            left_data_frame,
            columns=("date", "height", "weight", "systolic", "diastolic",
                     "diagnosis", "prescription", "ai_advice"),
            show="headings"     # Chỉ hiển thị tiêu đề cột, ẩn cột #0
        )
        # Đặt bảng chiếm toàn bộ khung left_data_frame
        self.tree.pack(side="top", fill="both", expand=True)
        # Gán sự kiện khi chọn một dòng trong bảng (sẽ gọi hàm on_history_row_select)
        self.tree.bind("<<TreeviewSelect>>", self.on_history_row_select)

        # Nút xóa lần khám (màu đỏ)
        self.btn_delete = ctk.CTkButton(left_data_frame, text="", fg_color="red", command=self.delete_visit)
        # Đặt nút ở dưới cùng, căn trái (anchor="w"), lề dưới 10
        self.btn_delete.pack(side="bottom", pady=10, anchor="w")

        # ---- Khung AI Agent (bên phải) ----
        # Tạo frame có chiều rộng 330 pixel, viền dày 1, màu viền #8E44AD
        self.ai_frame = ctk.CTkFrame(main_bottom_frame, width=330, border_width=1, border_color="#8E44AD")
        # Đặt frame bên phải, kéo dãn dọc nhưng không kéo dãn ngang (expand=False)
        self.ai_frame.pack(side="right", fill="both", expand=False, padx=(5, 0))
        # Ngăn không cho frame co dãn theo nội dung (giữ kích thước cố định)
        self.ai_frame.pack_propagate(False)

        # Label tiêu đề của khung AI (chữ sẽ được set sau)
        self.lbl_ai_header = ctk.CTkLabel(
            self.ai_frame, text="", font=("Arial", 12, "bold"), text_color="#8E44AD"
        )
        # Đặt label, căn trái (anchor="w"), lề trái/phải 10, lề trên 10
        self.lbl_ai_header.pack(anchor="w", padx=10, pady=10)

        # Textbox để hiển thị phản hồi từ AI (có thanh cuộn, tự động xuống dòng)
        self.txt_ai_response = ctk.CTkTextbox(self.ai_frame, activate_scrollbars=True, wrap="word")
        # Đặt textbox chiếm toàn bộ không gian còn lại, có lề
        self.txt_ai_response.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ====================================================================
        # 2.1.5. ÁP DỤNG NGÔN NGỮ VÀ TẢI DỮ LIỆU BAN ĐẦU
        # ====================================================================
        self.update_ui_text()          # Gọi hàm đồng bộ văn bản theo ngôn ngữ (do người dùng định nghĩa)
        self.load_history()            # Gọi hàm tải lịch sử khám từ database

        # --------------------------------------------------------------------
        # 2.1.6. SỬA LỖI BỘ GÕ TIẾNG VIỆT (IME DELAY) CHO CÁC Ô NHẬP
        # --------------------------------------------------------------------
        # Danh sách các ô nhập cần fix lỗi bộ gõ
        for w in [self.entry_date, self.entry_height, self.entry_weight,
                  self.entry_systolic, self.entry_diastolic,
                  self.entry_diagnosis, self.entry_prescription]:
            # Gán sự kiện KeyRelease: khi thả phím, sau 1 mili giây gọi update_idletasks để cập nhật giao diện
            w.bind("<KeyRelease>", lambda e: e.widget.after(1, lambda: e.widget.update_idletasks()))

    # ------------------------------------------------------------------------
    # 2.2. PHƯƠNG THỨC ĐỒNG BỘ NGÔN NGỮ (UI TEXT)
    # ------------------------------------------------------------------------
    def update_ui_text(self):
        """Cập nhật tất cả văn bản (label, nút, tiêu đề cột) theo ngôn ngữ hiện tại."""
        # Lấy mã ngôn ngữ từ controller (nếu có), mặc định "vi"
        lang_code = getattr(self.controller, "current_lang", "vi")
        self.texts = LANGUAGES[lang_code]          # Lấy từ điển tương ứng (dict)

        # Đặt tiêu đề cửa sổ: "Lịch sử khám bệnh - [tên bệnh nhân]"
        self.title(f"{self.texts['history_title']} - {self.patient_name}")

        # Cập nhật label trong form nhập liệu (các dòng chữ hướng dẫn)
        self.lbl_date.configure(text=self.texts["lbl_visit_date"])
        self.lbl_height.configure(text=self.texts["lbl_height"])
        self.lbl_weight.configure(text=self.texts["lbl_weight"])
        self.lbl_systolic.configure(text=self.texts["lbl_systolic"])
        self.lbl_diastolic.configure(text=self.texts["lbl_diastolic"])
        self.lbl_diagnosis.configure(text=self.texts["lbl_diagnosis"])
        self.lbl_prescription.configure(text=self.texts["lbl_prescription"])

        # Cập nhật văn bản trên các nút
        self.btn_add.configure(text=self.texts["btn_add_visit"])          # "➕ Thêm lần khám"
        self.btn_ai.configure(text=self.texts["btn_ai_advice"])           # "🤖 Trợ lý AI Tư vấn"
        self.btn_delete.configure(text=self.texts["btn_delete_visit"])    # "🗑️ Xóa lần khám"
        self.lbl_ai_header.configure(text=self.texts["ai_header"])        # "💡 Khuyến nghị từ AI Agent"

        # Cập nhật tiêu đề các cột trong bảng Treeview
        self.tree.heading("date", text=self.texts["col_date"])                 # "Ngày khám"
        self.tree.heading("height", text=self.texts["col_height"])             # "Cao (cm)"
        self.tree.heading("weight", text=self.texts["col_weight"])             # "Nặng (kg)"
        self.tree.heading("systolic", text=self.texts["col_systolic"])         # "HATT"
        self.tree.heading("diastolic", text=self.texts["col_diastolic"])       # "HATTr"
        self.tree.heading("diagnosis", text=self.texts["col_diagnosis"])       # "Chẩn đoán"
        self.tree.heading("prescription", text=self.texts["col_prescription"]) # "Thuốc kê"

        # Đặt độ rộng và căn chỉnh cho các cột (ẩn cột ai_advice)
        for col in ["date", "height", "weight", "systolic", "diastolic"]:
            self.tree.column(col, width=70, anchor="center")
        self.tree.column("diagnosis", width=110, anchor="w")      # căn trái
        self.tree.column("prescription", width=130, anchor="w")
        self.tree.column("ai_advice", width=0)                    # độ rộng 0 -> ẩn cột này
        # Chỉ hiển thị các cột (trừ cột ai_advice)
        self.tree.configure(displaycolumns=("date", "height", "weight", "systolic",
                                            "diastolic", "diagnosis", "prescription"))

        # Nếu khung AI đang hiển thị nội dung mặc định (Sẵn sàng), cập nhật theo ngôn ngữ mới
        curr_ai_text = self.txt_ai_response.get("1.0", "end-1c").strip()
        if not curr_ai_text or "Hệ thống AI sẵn sàng" in curr_ai_text or "AI System Ready" in curr_ai_text:
            self.txt_ai_response.delete("1.0", "end")
            self.txt_ai_response.insert("1.0", self.texts["ai_init_status"])

    # ------------------------------------------------------------------------
    # 2.3. GỌI AI TƯ VẤN (dựa trên chẩn đoán và đơn thuốc)
    # ------------------------------------------------------------------------
    def ask_ai(self):
        """Lấy chẩn đoán và thuốc từ form, gửi lên AI (controller) để nhận tư vấn."""
        # Lấy nội dung từ ô chẩn đoán và thuốc, bỏ khoảng trắng đầu cuối
        diagnosis = self.entry_diagnosis.get().strip()
        prescription = self.entry_prescription.get().strip()

        if not diagnosis:
            # Nếu không có chẩn đoán, hiển thị cảnh báo
            messagebox.showwarning(self.texts["msg_missing_info"], self.texts["msg_enter_diagnosis"], parent=self)
            return

        # Xóa nội dung cũ trong textbox AI và hiển thị trạng thái "đang xử lý"
        self.txt_ai_response.delete("1.0", "end")
        self.txt_ai_response.insert("1.0", self.texts["msg_ai_processing"])
        self.update_idletasks()     # Cập nhật giao diện ngay lập tức

        try:
            # Kiểm tra xem controller có phương thức ask_ai_for_advice không
            if hasattr(self.controller, "ask_ai_for_advice"):
                # Gọi controller để lấy lời khuyên (chỉ dựa trên diagnosis và prescription)
                advice = self.controller.ask_ai_for_advice(diagnosis, prescription)
                self.txt_ai_response.delete("1.0", "end")
                self.txt_ai_response.insert("1.0", advice)
            else:
                # Nếu controller không có AI Agent, hiển thị lỗi
                messagebox.showerror(self.texts["msg_sys_error"], self.texts["msg_no_ai_agent"], parent=self)
        except Exception as e:
            # Bắt lỗi bất kỳ (mạng, API, ...) và hiển thị trong textbox
            self.txt_ai_response.delete("1.0", "end")
            self.txt_ai_response.insert("1.0", f"Error: {str(e)}")

    # ------------------------------------------------------------------------
    # 2.4. TẢI LỊCH SỬ KHÁM TỪ DATABASE LÊN BẢNG
    # ------------------------------------------------------------------------
    def load_history(self):
        """Lấy dữ liệu lịch sử khám từ controller (model) và hiển thị lên Treeview."""
        # Xóa tất cả các dòng cũ trong bảng (lệnh thư viện)
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Gọi controller để lấy DataFrame chứa lịch sử khám của bệnh nhân
        df = self.controller.get_medical_history(self.patient_id)

        # Duyệt qua từng dòng trong DataFrame (iterrows trả về (index, row))
        for _, r in df.iterrows():
            # Lấy nội dung AI advice nếu có, nếu không thì chuỗi rỗng
            ai_adv = r['ai_advice'] if 'ai_advice' in df.columns and r['ai_advice'] else ""
            # Chèn một dòng mới vào bảng (values là tuple các giá trị, tags lưu id lần khám)
            self.tree.insert("", "end", values=(
                r['visit_date'], r['height'] or "", r['weight'] or "",
                r['systolic'] or "", r['diastolic'] or "",
                r['diagnosis'], r['prescription'], ai_adv
            ), tags=(r['id'],))          # lưu id lần khám vào tag

    # ------------------------------------------------------------------------
    # 2.5. XỬ LÝ KHI CHỌN MỘT DÒNG TRONG BẢNG (HIỂN THỊ LỜI KHUYÊN AI)
    # ------------------------------------------------------------------------
    def on_history_row_select(self, event):
        """Khi chọn một dòng lịch sử, hiển thị nội dung AI advice tương ứng."""
        selected = self.tree.selection()      # Lấy danh sách các dòng được chọn (tuple)
        if not selected:
            return
        values = self.tree.item(selected[0], "values")   # Lấy giá trị của dòng đầu tiên (tuple)
        # Cột cuối (index 7) là ai_advice
        saved_ai_text = values[7] if len(values) > 7 else ""

        # Hiển thị nội dung AI advice vào textbox
        self.txt_ai_response.delete("1.0", "end")
        self.txt_ai_response.insert("1.0", saved_ai_text.strip() or self.texts["msg_no_ai_data"])

    # ------------------------------------------------------------------------
    # 2.6. THÊM LẦN KHÁM MỚI
    # ------------------------------------------------------------------------
    def add_visit(self):
        """Lấy dữ liệu từ form, kiểm tra hợp lệ, gọi controller để thêm lần khám."""
        # Lấy giá trị từ các ô nhập (strip() bỏ khoảng trắng đầu cuối)
        visit_date = self.entry_date.get().strip()
        height = self.entry_height.get().strip()
        weight = self.entry_weight.get().strip()
        systolic = self.entry_systolic.get().strip()
        diastolic = self.entry_diastolic.get().strip()
        diagnosis = self.entry_diagnosis.get().strip()
        prescription = self.entry_prescription.get().strip()

        # Lấy nội dung AI advice hiện tại (nếu có) để lưu vào database
        ai_advice_to_save = self.txt_ai_response.get("1.0", "end-1c").strip()
        # Nếu nội dung là các chuỗi trạng thái mặc định (đang xử lý, sẵn sàng) thì không lưu
        if any(x in ai_advice_to_save for x in ["Sẵn sàng", "Ready", "đang phân tích", "analyzing"]):
            ai_advice_to_save = ""

        # Kiểm tra định dạng ngày và chuyển đổi kiểu dữ liệu
        try:
            datetime.strptime(visit_date, "%Y-%m-%d")   # Kiểm tra ngày có đúng định dạng YYYY-MM-DD
            h = float(height) if height else None
            w = float(weight) if weight else None
            sys = int(systolic) if systolic else None
            dia = int(diastolic) if diastolic else None
        except ValueError:
            # Hiển thị lỗi nếu ngày sai hoặc số liệu không chuyển được
            messagebox.showerror(self.texts["err_title"],
                                 "Kiểm tra định dạng ngày (YYYY-MM-DD) hoặc số liệu đầu vào!",
                                 parent=self)
            return

        # Gọi controller để thêm lần khám (truyền đủ 9 tham số, trong đó ai_advice được lưu)
        self.controller.add_medical_visit(
            self.patient_id, visit_date, h, w, sys, dia, diagnosis, prescription, ai_advice_to_save
        )
        # Tải lại bảng để hiển thị dữ liệu mới
        self.load_history()

        # Xóa các ô nhập (trừ ngày khám giữ nguyên, vì ngày mặc định là hôm nay)
        for e in [self.entry_height, self.entry_weight, self.entry_systolic,
                  self.entry_diastolic, self.entry_diagnosis, self.entry_prescription]:
            e.delete(0, "end")
        # Reset khung AI về trạng thái ban đầu (hiển thị thông báo sẵn sàng theo ngôn ngữ)
        self.txt_ai_response.delete("1.0", "end")
        self.txt_ai_response.insert("1.0", self.texts["ai_init_status"])

    # ------------------------------------------------------------------------
    # 2.7. XÓA LẦN KHÁM ĐƯỢC CHỌN
    # ------------------------------------------------------------------------
    def delete_visit(self):
        """Xóa lần khám đang được chọn sau khi xác nhận."""
        selected = self.tree.selection()
        if not selected:
            # Nếu chưa chọn dòng nào, hiển thị cảnh báo
            messagebox.showwarning(self.texts["msg_select_visit"],
                                   self.texts["msg_warn_select_delete"],
                                   parent=self)
            return
        # Lấy id của lần khám (được lưu trong tags) – tags là tuple, phần tử đầu tiên
        visit_id = self.tree.item(selected[0], "tags")[0]
        # Hỏi xác nhận trước khi xóa
        if messagebox.askyesno(self.texts["msg_confirm"], self.texts["msg_ask_delete"], parent=self):
            self.controller.delete_medical_visit(visit_id)
            self.load_history()      # Tải lại danh sách sau khi xóa

    # ------------------------------------------------------------------------
    # 2.8. HỦY ĐĂNG KÝ CỬA SỔ CON KHI ĐÓNG
    # ------------------------------------------------------------------------
    def destroy(self):
        """Hủy đăng ký cửa sổ con (nếu có) trước khi đóng."""
        if hasattr(self.controller, "unregister_sub_window"):
            self.controller.unregister_sub_window(self)
        super().destroy()            # Gọi destroy của lớp cha (đóng cửa sổ)