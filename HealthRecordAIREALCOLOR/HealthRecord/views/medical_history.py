# views/medical_history.py
import customtkinter as ctk
from tkinter import ttk
import datetime
from config.languages import LANGUAGES

# IMPORT Helper bộ gõ tiếng Việt toàn cục
from utils.ime_helper import LinuxIMEHelper

class MedicalHistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, patient_data):
        super().__init__(parent)
        self.controller = controller
        self.patient_data = patient_data
        
        # Biến tạm để lưu trữ câu trả lời của AI trước khi nhấn nút "Thêm lượt khám"
        self.current_ai_advice = ""
        
        if hasattr(self.controller, "register_sub_window"):
            self.controller.register_sub_window(self)

        self.geometry("1150x690")
        
        self.attributes("-topmost", True)
        self.wait_visibility()
        self.grab_set()

        self.lang = self.controller.current_lang if self.controller else "vi"
        self.texts = LANGUAGES[self.lang]
        self.title(f"{self.texts.get('history_title', 'Lịch sử khám bệnh')} - {self.patient_data['name']}")

        # Layout chính tách biệt Trái (Nhập/Xem bệnh án) & Phải (AI Trợ lý tư vấn)
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # =========================================================================
        # ⬅️ VÙNG BÊN TRÁI: QUẢN LÝ BỆNH ÁN CHI TIẾT
        # =========================================================================
        left_panel = ctk.CTkFrame(main_container, width=620, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Form điền thông số khám lâm sàng
        form_frame = ctk.CTkFrame(left_panel, corner_radius=12, border_width=1, border_color="#282C37")
        form_frame.pack(fill="x", pady=(0, 10))

        # Dòng 1: Ngày khám & Cân nặng & Chiều cao
        r1_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        r1_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(r1_frame, text=self.texts.get("lbl_visit_date", "Ngày khám:"), font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_date = ctk.CTkEntry(r1_frame, width=120)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)
        self.entry_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        ctk.CTkLabel(r1_frame, text=self.texts.get("lbl_height", "Chiều cao (cm):"), font=("Arial", 12)).grid(row=0, column=2, sticky="w", padx=5)
        self.entry_height = ctk.CTkEntry(r1_frame, width=70)
        self.entry_height.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(r1_frame, text=self.texts.get("lbl_weight", "Cân nặng (kg):"), font=("Arial", 12)).grid(row=0, column=4, sticky="w", padx=5)
        self.entry_weight = ctk.CTkEntry(r1_frame, width=70)
        self.entry_weight.grid(row=0, column=5, padx=5, pady=5)

        # Dòng 2: Chỉ số huyết áp tâm thu & tâm trương
        r2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        r2_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(r2_frame, text=self.texts.get("lbl_systolic", "HATT:"), font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_systolic = ctk.CTkEntry(r2_frame, width=80)
        self.entry_systolic.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(r2_frame, text=self.texts.get("lbl_diastolic", "HATTr:"), font=("Arial", 12)).grid(row=0, column=2, sticky="w", padx=5)
        self.entry_diastolic = ctk.CTkEntry(r2_frame, width=80)
        self.entry_diastolic.grid(row=0, column=3, padx=5, pady=5)

        # Dòng 3: Chẩn đoán y khoa sơ bộ
        r3_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        r3_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(r3_frame, text=self.texts.get("lbl_diagnosis", "Chẩn đoán:"), font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
        
        p_diag = self.texts.get("placeholder_diagnosis", self.texts.get("plh_diagnosis", "Nhập chẩn đoán sơ bộ..."))
        self.entry_diagnosis = ctk.CTkEntry(r3_frame, placeholder_text=p_diag)
        self.entry_diagnosis.pack(fill="x", padx=5, pady=2)

        # Dòng 4: Đơn thuốc chỉ định
        r4_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        r4_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(r4_frame, text=self.texts.get("lbl_prescription", "Đơn thuốc:"), font=("Arial", 12, "bold")).pack(anchor="w", padx=5)
        
        p_pres = self.texts.get("placeholder_prescription", self.texts.get("plh_prescription", "Nhập đơn thuốc chỉ định..."))
        self.entry_prescription = ctk.CTkEntry(r4_frame, placeholder_text=p_pres)
        self.entry_prescription.pack(fill="x", padx=5, pady=2)

        # Thanh nút lệnh thao tác bệnh án
        action_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        action_frame.pack(fill="x", pady=5)

        self.btn_add_visit = ctk.CTkButton(action_frame, text=self.texts.get("btn_add_visit", "Thêm lượt khám"), fg_color="#10B981", hover_color="#059669", font=("Arial", 12, "bold"), command=self.add_visit)
        self.btn_add_visit.pack(side="left", expand=True, padx=4, fill="x")

        self.btn_del_visit = ctk.CTkButton(action_frame, text=self.texts.get("btn_del_visit", "Xóa lượt khám"), fg_color="#FF0844", hover_color="#D90434", font=("Arial", 12, "bold"), command=self.delete_visit)
        self.btn_del_visit.pack(side="left", expand=True, padx=4, fill="x")

        # Bảng danh sách các lượt khám trước đó
        table_frame = ctk.CTkFrame(left_panel, fg_color="#1A1D24", corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=(5, 0))

        columns = ("id", "date", "diagnosis", "prescription")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text=self.texts.get("col_visit_date", "Ngày khám"))
        self.tree.heading("diagnosis", text=self.texts.get("lbl_diagnosis", "Chẩn đoán"))
        self.tree.heading("prescription", text=self.texts.get("lbl_prescription", "Đơn thuốc"))

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=95, anchor="center")
        self.tree.column("diagnosis", width=220)
        self.tree.column("prescription", width=220)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_visit)

        # =========================================================================
        # ➡️ VÙNG BÊN PHẢI: TRỢ LÝ AI AGENT CHẨN ĐOÁN LÂM SÀNG
        # =========================================================================
        right_panel = ctk.CTkFrame(main_container, corner_radius=16, fg_color="#1A1D24", border_width=1, border_color="#00F2FE")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ai_header = ctk.CTkLabel(right_panel, text=self.texts.get("ai_agent_title", "Trợ lý AI Agent"), font=("Segoe UI", 14, "bold"), text_color="#00F2FE")
        ai_header.pack(pady=8)

        # Khung chứa text cuộn hiển thị phân tích từ AI Agent
        self.txt_ai_advice = ctk.CTkTextbox(right_panel, font=("Segoe UI", 12), fg_color="#0D0F13", border_color="#282C37", text_color="#ECEFF4", wrap="word")
        self.txt_ai_advice.pack(fill="both", expand=True, padx=15, pady=5)
        self.txt_ai_advice.insert("1.0", self.texts.get("ai_welcome_msg", "Hệ thống AI đã sẵn sàng phân tích bệnh án..."))

        # Nút ra lệnh cho AI rà soát hồ sơ
        self.btn_ask_ai = ctk.CTkButton(right_panel, text=self.texts.get("btn_ask_ai", "Hỏi ý kiến AI Agent"), fg_color="#00F2FE", hover_color="#00C2CE", text_color="#000000", font=("Segoe UI", 12, "bold"), command=self.trigger_ai_agent)
        self.btn_ask_ai.pack(fill="x", padx=15, pady=12)

        self.load_history()

        # ÁP DỤNG bộ gõ tiếng Việt tự chế cho tất cả các ô viết thông tin lâm sàng trên Linux
        medical_widgets = [
            self.entry_date, self.entry_height, self.entry_weight, 
            self.entry_systolic, self.entry_diastolic, 
            self.entry_diagnosis, self.entry_prescription
        ]
        LinuxIMEHelper.apply_ime_to_widgets(self, medical_widgets)

    def show_custom_dialog(self, title, message, is_confirm=False, callback=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("380x180")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.wait_visibility()
        dialog.grab_set() 
        
        x = self.winfo_x() + (self.winfo_width() // 2) - 190
        y = self.winfo_y() + (self.winfo_height() // 2) - 90
        dialog.geometry(f"+{x}+{y}")

        lbl = ctk.CTkLabel(dialog, text=message, wraplength=340, font=("Segoe UI", 13))
        lbl.pack(expand=True, padx=20, pady=(20, 10))
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=(0, 20))

        if is_confirm:
            def on_yes():
                dialog.destroy()
                if callback: callback()
            btn_yes = ctk.CTkButton(btn_frame, text=self.texts.get("btn_confirm", "Đồng ý"), fg_color="#FF0844", hover_color="#D90434", width=100, command=on_yes)
            btn_yes.pack(side="left", padx=10)
            btn_no = ctk.CTkButton(btn_frame, text=self.texts.get("btn_cancel", "Hủy"), fg_color="#7F8C8D", hover_color="#95A5A6", width=100, command=dialog.destroy)
            btn_no.pack(side="right", padx=10)
        else:
            btn_close = ctk.CTkButton(btn_frame, text=self.texts.get("close", "Đóng"), width=100, command=dialog.destroy)
            btn_close.pack()

    def load_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.controller:
            df = self.controller.get_medical_history(self.patient_data["id"])
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(row["id"], row["visit_date"], row["diagnosis"], row["prescription"]))

    def on_select_visit(self, event):
        selected = self.tree.selection()
        if not selected: return
        visit_id = self.tree.item(selected[0])["values"][0]
        
        if self.controller:
            df = self.controller.get_medical_history(self.patient_data["id"])
            match = df[df["id"] == int(visit_id)]
            if not match.empty:
                ai_text = match.iloc[0]["ai_advice"]
                self.txt_ai_advice.delete("1.0", ctk.END)
                if ai_text and str(ai_text).strip() != "nan" and str(ai_text).strip() != "":
                    self.txt_ai_advice.insert("1.0", str(ai_text))
                else:
                    self.txt_ai_advice.insert("1.0", self.texts.get("ai_no_data_msg", "Không có dữ liệu khuyên dùng từ AI."))

    def trigger_ai_agent(self):
        """Hỏi ý kiến AI dựa trên thông tin đang nhập ở Form (Không cần chọn hàng bên dưới)"""
        diag = self.entry_diagnosis.get().strip()
        pres = self.entry_prescription.get().strip()

        if not diag:
            msg = self.texts.get("msg_ai_need_diagnosis", "Vui lòng nhập chẩn đoán trước khi gọi trợ lý AI!")
            self.show_custom_dialog(self.texts.get("err_title", "Lỗi"), msg)
            return

        self.txt_ai_advice.delete("1.0", ctk.END)
        self.txt_ai_advice.insert("1.0", self.texts.get("ai_processing_msg", "AI Agent đang phân tích hồ sơ lâm sàng, vui lòng đợi..."))
        self.update()

        if self.controller:
            # Gọi AI phân tích
            advice = self.controller.ask_ai_for_advice(diag, pres)
            
            # Hiển thị lên khung TextBox
            self.txt_ai_advice.delete("1.0", ctk.END)
            self.txt_ai_advice.insert("1.0", advice)
            
            # Lưu tạm vào biến giao diện, chờ người dùng bấm "Thêm lượt khám"
            self.current_ai_advice = advice

    def add_visit(self):
        """Nhấn nút Thêm lượt khám: Gom thông tin Form + ý kiến AI vừa tạo để lưu vào DB"""
        date_str = self.entry_date.get().strip()
        diag = self.entry_diagnosis.get().strip()
        pres = self.entry_prescription.get().strip()

        if not date_str or not diag:
            self.show_custom_dialog(self.texts.get("err_title", "Lỗi"), "Vui lòng điền Ngày khám & Chẩn đoán sơ bộ!")
            return

        h = self.entry_height.get().strip() or None
        w = self.entry_weight.get().strip() or None
        sys = self.entry_systolic.get().strip() or None
        dia = self.entry_diastolic.get().strip() or None

        if self.controller:
            # Truyền kèm self.current_ai_advice vào DB luôn lúc thêm mới
            self.controller.add_medical_visit(
                self.patient_data["id"], date_str, h, w, sys, dia, diag, pres, 
                ai_advice=self.current_ai_advice
            )
            self.load_history()
            
            # Xóa sạch Form nhập liệu và reset biến lưu tạm AI
            self.entry_diagnosis.delete(0, ctk.END)
            self.entry_prescription.delete(0, ctk.END)
            self.current_ai_advice = "" 

    def delete_visit(self):
        selected = self.tree.selection()
        if not selected:
            self.show_custom_dialog(self.texts.get("err_title", "Lỗi"), "Vui lòng chọn lượt khám cần xóa!")
            return
        
        def execute_deletion():
            visit_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete_medical_visit(visit_id)
            self.load_history()

        msg_confirm = "Bạn có chắc chắn muốn xóa lượt khám y khoa này?"
        self.show_custom_dialog(self.texts.get("msg_confirm", "Xác nhận"), msg_confirm, is_confirm=True, callback=execute_deletion)

    def destroy(self):
        if hasattr(self.controller, "unregister_sub_window"):
            self.controller.unregister_sub_window(self)
        super().destroy()