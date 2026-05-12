# views/main_view.py
# Giao diện chính của ứng dụng: cửa sổ, toolbar, bảng Treeview, thanh trạng thái.

import customtkinter as ctk
from tkinter import ttk, messagebox
from models import patient as model   # Import model để gọi trực tiếp (sẽ thay bằng controller sau)

class MainView(ctk.CTk):
    """
    Lớp MainView kế thừa từ CTk (cửa sổ chính của customtkinter).
    Quản lý toàn bộ giao diện đồ họa.
    """

    def __init__(self):
        # Gọi hàm khởi tạo của lớp cha (ctk.CTk) để thiết lập cửa sổ cơ bản.
        super().__init__()

        # --- Các thiết lập chung cho cửa sổ ---
        # Đặt tiêu đề cửa sổ (dòng chữ trên thanh tiêu đề)
        self.title("HealthRecord - Quản lý hồ sơ bệnh nhân")
        # Đặt kích thước cửa sổ: rộng 900 pixel, cao 500 pixel
        self.geometry("900x500")
        # Đặt chế độ giao diện: "dark" (nền tối) hoặc "light". Ở đây chọn dark.
        ctk.set_appearance_mode("dark")
        # Đặt chủ đề màu sắc chính: "blue" (xanh dương)
        ctk.set_default_color_theme("blue")

        # Biến để lưu controller (sẽ được gán sau)
        self.controller = None

        # --- Tạo thanh toolbar (khung chứa các nút) ---
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=10)    # Kéo dài ngang, lề trái/phải 10, trên/dưới 10

        # Khung chứa các nút, có thể cuộn ngang nếu quá nhiều nút và cửa sổ hẹp.
        # CTkScrollableFrame cho phép cuộn; orientation="horizontal" là cuộn ngang.
        btn_container = ctk.CTkScrollableFrame(toolbar, orientation="horizontal", height=45)
        btn_container.pack(side="left", fill="x", expand=True)

        # Nút Thêm
        self.btn_add = ctk.CTkButton(btn_container, text="+ Thêm", command=self.on_add)
        self.btn_add.pack(side="left", padx=3)

        # Nút Sửa
        self.btn_edit = ctk.CTkButton(btn_container, text="✏️ Sửa", command=self.on_edit)
        self.btn_edit.pack(side="left", padx=3)

        # Nút Xóa (màu đỏ)
        self.btn_delete = ctk.CTkButton(btn_container, text="🗑️ Xóa", fg_color="red", command=self.on_delete)
        self.btn_delete.pack(side="left", padx=3)

        # --- Khung tìm kiếm (bên phải toolbar) ---
        search_frame = ctk.CTkFrame(toolbar)
        search_frame.pack(side="right", padx=5)   # Đặt bên phải, cách lề 5 pixel

        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Tìm theo tên", width=150)
        self.entry_search.pack(side="left", padx=3)

        self.btn_search = ctk.CTkButton(search_frame, text="Tìm", command=self.on_search)
        self.btn_search.pack(side="left")

        # --- Bảng hiển thị danh sách bệnh nhân (Treeview) ---
        # Các cột của bảng: id, name, birth_year, gender, phone, address
        columns = ("id", "name", "birth_year", "gender", "phone", "address")
        # Tạo Treeview, show="headings" chỉ hiện tiêu đề cột.
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Đặt tiêu đề cho mỗi cột (những tiêu đề này hiển thị trên giao diện)
        self.tree.heading("id", text="ID")                 # Cột ID
        self.tree.heading("name", text="Họ tên")           # Cột Họ tên
        self.tree.heading("birth_year", text="Năm sinh")   # Cột Năm sinh
        self.tree.heading("gender", text="Giới tính")      # Cột Giới tính
        self.tree.heading("phone", text="SĐT")             # Cột Số điện thoại
        self.tree.heading("address", text="Địa chỉ")       # Cột Địa chỉ

        # Đặt độ rộng cho từng cột (giá trị pixel)
        self.tree.column("id", width=50, anchor="center")       # Rộng 50, canh giữa
        self.tree.column("name", width=180)                     # Rộng 180, canh trái mặc định
        self.tree.column("birth_year", width=80, anchor="center")
        self.tree.column("gender", width=80, anchor="center")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("address", width=150)

        # Thêm thanh cuộn dọc cho bảng
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Đặt bảng và thanh cuộn vào cửa sổ
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0,10), pady=10)

        # --- Thanh trạng thái (status bar) ở dưới cùng ---
        self.status_label = ctk.CTkLabel(self, text="Sẵn sàng", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    # ------------------ Các phương thức kết nối với controller ------------------
    def set_controller(self, controller):
        """
        Gắn đối tượng controller vào view, đồng thời tải dữ liệu lần đầu.
        Tham số controller: instance của PatientController.
        """
        self.controller = controller
        self.refresh_table()   # Tải dữ liệu từ model lên bảng

    def refresh_table(self):
        """
        Lấy dữ liệu từ controller (thông qua controller.get_all_patients()) và cập nhật bảng.
        Xóa toàn bộ dòng cũ, sau đó thêm từng dòng mới từ DataFrame.
        """
        # Gọi controller để lấy DataFrame chứa danh sách bệnh nhân
        df = self.controller.get_all_patients()
        
        # Xóa tất cả các dòng hiện có trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Duyệt từng dòng trong DataFrame (df.iterrows() trả về (index, row))
        for _, row in df.iterrows():
            # Chèn một dòng vào cuối bảng, giá trị lấy từ row (các cột tương ứng)
            self.tree.insert("", "end", values=(
                row['id'], row['name'], row['birth_year'],
                row['gender'], row['phone'], row['address']
            ))
        
        # Cập nhật thanh trạng thái: hiển thị tổng số bệnh nhân
        # Ví dụ: "Tổng số bệnh nhân: 5"
        self.status_label.configure(text=f"Tổng số bệnh nhân: {len(df)}")

    def get_selected_patient(self):
        """
        Lấy thông tin bệnh nhân đang được chọn trên bảng.
        Trả về một dictionary (từ điển) gồm các key: id, name, birth_year, gender, phone, address.
        Nếu không có dòng nào được chọn, hiện cảnh báo và trả về None.
        """
        # tree.selection() trả về tuple các item ID đang được chọn (ở chế độ chọn một dòng)
        selected = self.tree.selection()
        if not selected:
            # messagebox.showwarning() hiển thị cửa sổ cảnh báo với tiêu đề và nội dung
            messagebox.showwarning("Chọn bệnh nhân", "Vui lòng chọn một bệnh nhân")
            return None
        
        # Lấy item đầu tiên (vì chúng ta chỉ cho chọn một dòng)
        item = self.tree.item(selected[0])
        # item['values'] là tuple các giá trị của dòng đó (theo thứ tự các cột)
        values = item['values']
        # Tạo dictionary với các tên trường tương ứng
        return {
            "id": values[0],
            "name": values[1],
            "birth_year": values[2],
            "gender": values[3],
            "phone": values[4],
            "address": values[5]
        }

    # ------------------ Các hàm xử lý sự kiện từ nút bấm ------------------
    def on_add(self):
        """
        Xử lý khi nhấn nút Thêm. Ở bước 4, chưa có popup riêng, tạm dùng simpledialog
        để nhập tên bệnh nhân (các trường khác để mặc định).
        """
        from tkinter import simpledialog
        # simpledialog.askstring() hiển thị hộp thoại yêu cầu nhập chuỗi.
        # Dòng chữ hiển thị trên hộp thoại: "Nhập họ tên:"
        name = simpledialog.askstring("Thêm bệnh nhân", "Nhập họ tên:")
        if name:
            # Gọi controller để thêm bệnh nhân (các trường khác dùng giá trị mặc định)
            self.controller.add_patient(name, 2000, "Nam", "", "")
            # Tải lại bảng để hiển thị dữ liệu mới
            self.refresh_table()

    def on_edit(self):
        """
        Xử lý khi nhấn nút Sửa. Lấy bệnh nhân đang chọn, yêu cầu nhập tên mới.
        """
        data = self.get_selected_patient()
        if not data:
            return
        from tkinter import simpledialog
        new_name = simpledialog.askstring("Sửa tên", "Nhập tên mới:", initialvalue=data['name'])
        if new_name and new_name != data['name']:
            self.controller.update_patient(
                data['id'], new_name, data['birth_year'],
                data['gender'], data['phone'], data['address']
            )
            self.refresh_table()

    def on_delete(self):
        """
        Xóa bệnh nhân đang chọn sau khi xác nhận.
        """
        data = self.get_selected_patient()
        if data:
            # messagebox.askyesno() hiện hộp thoại hỏi Có/Không, trả về True nếu chọn Yes.
            # Dòng chữ hiển thị: "Bạn có chắc muốn xóa Nguyễn Văn A?"
            if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa {data['name']}?"):
                self.controller.delete_patient(data['id'])
                self.refresh_table()

    def on_search(self):
        """
        Tìm kiếm bệnh nhân theo tên (không phân biệt hoa thường).
        Lấy từ khóa từ ô search_entry, lọc DataFrame, hiển thị kết quả lên bảng.
        """
        keyword = self.entry_search.get().strip().lower()   # Lấy chuỗi nhập, bỏ khoảng trắng đầu cuối, chuyển thành chữ thường
        # Lấy toàn bộ dữ liệu từ controller
        df = self.controller.get_all_patients()
        if keyword:
            # Lọc các dòng có tên chứa keyword (na=False bỏ qua giá trị null)
            df = df[df['name'].str.lower().str.contains(keyword, na=False)]
        # Xóa bảng cũ và hiển thị kết quả lọc
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, r in df.iterrows():
            self.tree.insert("", "end", values=(r['id'], r['name'], r['birth_year'], r['gender'], r['phone'], r['address']))
        # Hiển thị thông báo trên thanh trạng thái: số lượng tìm thấy và tổng số
        self.status_label.configure(text=f"Tìm thấy: {len(df)} bệnh nhân (trên tổng số {len(self.controller.get_all_patients())})")