# views/main_view.py
# Giao diện chính của ứng dụng: cửa sổ, toolbar, bảng Treeview, thống kê.

import customtkinter as ctk
from tkinter import ttk, messagebox
from models import patient as model
from views.add_edit_patient import AddEditPatientWindow

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Cài đặt cửa sổ ---
        self.title("HealthRecord - Quản lý hồ sơ bệnh nhân")
        self.geometry("1200x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Controller sẽ được gán sau
        self.controller = None

        # --- Toolbar (thanh công cụ) ---
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=10)

        # Khung chứa các nút (có thể cuộn ngang)
        btn_container = ctk.CTkScrollableFrame(toolbar, orientation="horizontal", height=50)
        btn_container.pack(side="left", fill="x", expand=True)

        # Nút Thêm
        self.btn_add = ctk.CTkButton(btn_container, text="+ Thêm", command=self.on_add)
        self.btn_add.pack(side="left", padx=3)

        # Nút Sửa
        self.btn_edit = ctk.CTkButton(btn_container, text="✏️ Sửa", command=self.on_edit)
        self.btn_edit.pack(side="left", padx=3)

        # Nút Xóa
        self.btn_delete = ctk.CTkButton(btn_container, text="🗑️ Xóa", fg_color="red", command=self.on_delete)
        self.btn_delete.pack(side="left", padx=3)

        # Nút Lịch sử khám
        self.btn_history = ctk.CTkButton(btn_container, text="📋 Lịch sử khám", command=self.on_history)
        self.btn_history.pack(side="left", padx=3)

        # Nút Import CSV
        self.btn_import = ctk.CTkButton(btn_container, text="📂 Import CSV", command=lambda: self.controller.import_csv() if self.controller else None)
        self.btn_import.pack(side="left", padx=3)

        # Nút Export CSV
        self.btn_export = ctk.CTkButton(btn_container, text="💾 Export CSV", command=lambda: self.controller.export_csv() if self.controller else None)
        self.btn_export.pack(side="left", padx=3)

        # Nút Xuất mẫu CSV
        self.btn_template = ctk.CTkButton(btn_container, text="📄 Mẫu CSV", command=lambda: self.controller.export_template_csv() if self.controller else None)
        self.btn_template.pack(side="left", padx=3)

        # Nút About
        self.btn_about = ctk.CTkButton(btn_container, text="ℹ️ About", command=self.show_about)
        self.btn_about.pack(side="left", padx=3)

        # --- Khung tìm kiếm (bên phải) ---
        search_frame = ctk.CTkFrame(toolbar)
        search_frame.pack(side="right", padx=5)
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Tìm theo tên", width=150)
        self.entry_search.pack(side="left", padx=3)
        self.btn_search = ctk.CTkButton(search_frame, text="Tìm", command=self.on_search)
        self.btn_search.pack(side="left")

        # --- Bảng hiển thị danh sách bệnh nhân ---
        columns = ("id", "name", "birth_year", "gender", "phone", "address")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Họ tên")
        self.tree.heading("birth_year", text="Năm sinh")
        self.tree.heading("gender", text="Giới tính")
        self.tree.heading("phone", text="SĐT")
        self.tree.heading("address", text="Địa chỉ")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("birth_year", width=80, anchor="center")
        self.tree.column("gender", width=80, anchor="center")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("address", width=150)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)

        # --- Khung thống kê (thay thế thanh trạng thái) ---
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        self.lbl_total = ctk.CTkLabel(stats_frame, text="Tổng: 0", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side="left", padx=15)

        self.lbl_male = ctk.CTkLabel(stats_frame, text="Nam: 0", font=("Arial", 12))
        self.lbl_male.pack(side="left", padx=15)

        self.lbl_female = ctk.CTkLabel(stats_frame, text="Nữ: 0", font=("Arial", 12))
        self.lbl_female.pack(side="left", padx=15)

        self.lbl_avg_age = ctk.CTkLabel(stats_frame, text="Tuổi TB: 0.0", font=("Arial", 12))
        self.lbl_avg_age.pack(side="left", padx=15)

    # ------------------ Kết nối controller ------------------
    def set_controller(self, controller):
        self.controller = controller
        self.refresh_table()

    # ------------------ Cập nhật bảng và thống kê ------------------
    def refresh_table(self):
        df = self.controller.get_all_patients()
        # Xóa bảng cũ
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Thêm dữ liệu mới
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row['id'], row['name'], row['birth_year'],
                row['gender'], row['phone'], row['address']
            ))
        # Cập nhật thống kê
        total = len(df)
        male = len(df[df['gender'] == 'Nam']) if total > 0 else 0
        female = len(df[df['gender'] == 'Nữ']) if total > 0 else 0
        current_year = 2025
        avg_age = (current_year - df['birth_year']).mean() if total > 0 else 0
        self.lbl_total.configure(text=f"Tổng: {total}")
        self.lbl_male.configure(text=f"Nam: {male}")
        self.lbl_female.configure(text=f"Nữ: {female}")
        self.lbl_avg_age.configure(text=f"Tuổi TB: {avg_age:.1f}")

    # ------------------ Lấy bệnh nhân đang chọn ------------------
    def get_selected_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn bệnh nhân", "Vui lòng chọn một bệnh nhân")
            return None
        item = self.tree.item(selected[0])
        values = item['values']
        return {
            "id": values[0],
            "name": values[1],
            "birth_year": values[2],
            "gender": values[3],
            "phone": values[4],
            "address": values[5]
        }

    # ------------------ Xử lý sự kiện ------------------
    def on_add(self):
        AddEditPatientWindow(self, self.controller, edit_mode=False)

    def on_edit(self):
        data = self.get_selected_patient()
        if data:
            AddEditPatientWindow(self, self.controller, edit_mode=True, patient_data=data)

    def on_delete(self):
        data = self.get_selected_patient()
        if data and messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa {data['name']}?"):
            self.controller.delete_patient(data['id'])

    def on_history(self):
        data = self.get_selected_patient()
        if data:
            from views.medical_history import MedicalHistoryWindow
            MedicalHistoryWindow(self, self.controller, data['id'], data['name'])

    def on_search(self):
        keyword = self.entry_search.get().strip().lower()
        df = self.controller.get_all_patients()
        if keyword:
            df = df[df['name'].str.lower().str.contains(keyword, na=False)]
        # Hiển thị kết quả tìm kiếm lên bảng (tạm thời, không ảnh hưởng refresh sau)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, r in df.iterrows():
            self.tree.insert("", "end", values=(
                r['id'], r['name'], r['birth_year'], r['gender'], r['phone'], r['address']
            ))
        self.lbl_total.configure(text=f"Tìm thấy: {len(df)} (tổng: {len(self.controller.get_all_patients())})")

    def show_about(self):
        messagebox.showinfo(
            "Giới thiệu - HealthRecord",
            "📋 PHẦN MỀM QUẢN LÝ HỒ SƠ BỆNH NHÂN\n\n"
            "Phiên bản: 1.0.0\n"
            "Tác giả: Nhóm 5 - Lập trình Python\n"
            "   Trần Minh Hiếu\n"
            "   Nguyễn Đức Đại Nam\n"
            "   Nguyễn Quang Thái\n"
            "   Hà Văn Tú\n"
            "Trường Đại học Hạ Long (UHL)\n"
            "Ngày phát hành: 05/2026\n\n"
            "Chức năng chính:\n"
            "• Quản lý bệnh nhân (Thêm, Sửa, Xóa, Tìm kiếm)\n"
            "• Import/Export dữ liệu CSV\n"
            "• Thống kê sĩ số, giới tính, tuổi trung bình\n"
            "• Lưu trữ dữ liệu bằng SQLite\n\n"
            "© 2026 - Bản quyền thuộc về nhóm phát triển."
        )