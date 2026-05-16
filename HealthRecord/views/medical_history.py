# views/medical_history.py
# Cửa sổ hiển thị lịch sử khám bệnh của một bệnh nhân, cho phép thêm và xóa

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class MedicalHistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller, patient_id, patient_name):
        super().__init__(parent)
        self.controller = controller
        self.patient_id = patient_id
        self.title(f"Lịch sử khám bệnh - {patient_name}")
        self.geometry("900x500")
        self.grab_set()

        # Form nhập liệu phía trên
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Ngày khám (mặc định hôm nay)
        ctk.CTkLabel(form_frame, text="Ngày khám (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_date = ctk.CTkEntry(form_frame, width=120)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        # Chiều cao, cân nặng
        ctk.CTkLabel(form_frame, text="Chiều cao (cm):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_height = ctk.CTkEntry(form_frame, width=80)
        self.entry_height.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Cân nặng (kg):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_weight = ctk.CTkEntry(form_frame, width=80)
        self.entry_weight.grid(row=0, column=5, padx=5, pady=5)

        # Huyết áp (tâm thu, tâm trương)
        ctk.CTkLabel(form_frame, text="HATT (mmHg):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_systolic = ctk.CTkEntry(form_frame, width=80)
        self.entry_systolic.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="HATTr (mmHg):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_diastolic = ctk.CTkEntry(form_frame, width=80)
        self.entry_diastolic.grid(row=1, column=3, padx=5, pady=5)

        # Chẩn đoán và thuốc
        ctk.CTkLabel(form_frame, text="Chẩn đoán:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.entry_diagnosis = ctk.CTkEntry(form_frame, width=150)
        self.entry_diagnosis.grid(row=1, column=5, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Thuốc kê:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_prescription = ctk.CTkEntry(form_frame, width=300)
        self.entry_prescription.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        # Nút thêm lần khám
        self.btn_add = ctk.CTkButton(form_frame, text="➕ Thêm lần khám", command=self.add_visit)
        self.btn_add.grid(row=3, column=0, columnspan=6, pady=10)

        # Bảng hiển thị lịch sử
        self.tree = ttk.Treeview(self, columns=("Ngày", "Cao", "Nặng", "HATT", "HATTr", "Chuẩn đoán", "Thuốc"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("Chuẩn đoán", width=150)
        self.tree.column("Thuốc", width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Nút xóa
        self.btn_delete = ctk.CTkButton(self, text="🗑️ Xóa lần khám được chọn", fg_color="red", command=self.delete_visit)
        self.btn_delete.pack(pady=5)

        self.load_history()

    def load_history(self):
        """Tải dữ liệu lịch sử khám của bệnh nhân lên bảng"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        df = self.controller.get_medical_history(self.patient_id)
        for _, r in df.iterrows():
            self.tree.insert("", "end", values=(
                r['visit_date'],
                r['height'] if r['height'] else "",
                r['weight'] if r['weight'] else "",
                r['systolic'] if r['systolic'] else "",
                r['diastolic'] if r['diastolic'] else "",
                r['diagnosis'],
                r['prescription']
            ), tags=(r['id'],))
        self.tree.tag_configure('odd', background='#f0f0f0')

    def add_visit(self):
        """Thêm lần khám mới vào database"""
        visit_date = self.entry_date.get().strip()
        height = self.entry_height.get().strip()
        weight = self.entry_weight.get().strip()
        systolic = self.entry_systolic.get().strip()
        diastolic = self.entry_diastolic.get().strip()
        diagnosis = self.entry_diagnosis.get().strip()
        prescription = self.entry_prescription.get().strip()

        # Kiểm tra ngày tháng (sơ bộ)
        if not visit_date:
            messagebox.showerror("Lỗi", "Vui lòng nhập ngày khám")
            return
        try:
            datetime.strptime(visit_date, "%Y-%m-%d")
        except:
            messagebox.showerror("Lỗi", "Ngày khám không đúng định dạng YYYY-MM-DD")
            return

        # Chuyển đổi số
        try:
            height = float(height) if height else None
            weight = float(weight) if weight else None
            systolic = int(systolic) if systolic else None
            diastolic = int(diastolic) if diastolic else None
        except:
            messagebox.showerror("Lỗi", "Chiều cao, cân nặng, huyết áp phải là số")
            return

        self.controller.add_medical_visit(self.patient_id, visit_date, height, weight, systolic, diastolic, diagnosis, prescription)
        self.load_history()
        # Xóa form
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_height.delete(0, "end")
        self.entry_weight.delete(0, "end")
        self.entry_systolic.delete(0, "end")
        self.entry_diastolic.delete(0, "end")
        self.entry_diagnosis.delete(0, "end")
        self.entry_prescription.delete(0, "end")

    def delete_visit(self):
        """Xóa lần khám đang được chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn lần khám", "Vui lòng chọn một lần khám để xóa")
            return
        item = selected[0]
        visit_id = self.tree.item(item, "tags")[0]  # lưu id trong tag
        if messagebox.askyesno("Xác nhận", "Xóa lần khám này?"):
            self.controller.delete_medical_visit(visit_id)
            self.load_history()