# ============================================================================
# FILE: views/main_view.py
# MỤC ĐÍCH: Giao diện chính của ứng dụng HealthRecord (cửa sổ chính)
#           Hỗ trợ đa ngôn ngữ, nhiều theme, menu động, tìm kiếm, thống kê...
# ============================================================================

# ============================================================================
# 1. IMPORT CÁC THƯ VIỆN VÀ MODULE
# ============================================================================
import customtkinter as ctk               # Lệnh import thư viện customtkinter (lệnh thư viện), đặt tên là ctk (do người dùng đặt)
from tkinter import ttk, messagebox       # Lệnh import ttk và messagebox từ tkinter (lệnh thư viện)
import platform                           # Lệnh import module platform (lệnh thư viện)
import pandas as pd                       # Lệnh import pandas, đặt tên là pd (lệnh thư viện)
from models import patient as model       # Lệnh import module patient (trong models) và đặt tên là model (do người dùng đặt)
from views.add_edit_patient import AddEditPatientWindow   # Lệnh import class AddEditPatientWindow (do người dùng định nghĩa)
from config.languages import LANGUAGES    # Lệnh import biến LANGUAGES từ config/languages.py (do người dùng định nghĩa)

# Thử import pywinstyles (chỉ dùng cho Windows, nếu có)
try:
    import pywinstyles                     # Lệnh import thư viện pywinstyles (lệnh thư viện)
except ImportError:
    pywinstyles = None                     # Nếu không có, gán pywinstyles = None (biến do người dùng đặt)

# ============================================================================
# 2. ĐỊNH NGHĠA LỚP MainView (CỬA SỔ CHÍNH)
# ============================================================================
class MainView(ctk.CTk):
    # Dòng trên: Khai báo class MainView kế thừa từ ctk.CTk (lệnh thư viện)
    """Lớp cửa sổ chính, kế thừa từ ctk.CTk (cửa sổ gốc của customtkinter)."""
    # Dòng docstring (chú thích nhiều dòng) – mô tả class

    # ------------------------------------------------------------------------
    # 2.1. HÀM KHỞI TẠO __init__ (TẠO TOÀN BỘ GIAO DIỆN)
    # ------------------------------------------------------------------------
    def __init__(self):
        # Dòng trên: định nghĩa hàm khởi tạo (do người dùng định nghĩa)
        super().__init__()                 # Gọi constructor của lớp cha (ctk.CTk) – lệnh thư viện
        self.title("HealthRecord - Quản lý hồ sơ bệnh nhân")
        # Dòng trên: Đặt tiêu đề cửa sổ (lệnh thư viện), dòng chữ hiển thị là "HealthRecord - Quản lý hồ sơ bệnh nhân"

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2.1.1. Khởi tạo các biến trạng thái hệ thống (do người dùng đặt)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.linux_ime_active = True       # Biến bool (do người dùng đặt) – trạng thái IME trên Linux
        self.is_linux = platform.system().lower() == "linux"
        # Dòng trên: Gán True nếu hệ điều hành là Linux, False nếu không (lệnh thư viện platform)
        self.current_lang = "vi"           # Biến chuỗi (do người dùng đặt) – ngôn ngữ hiện tại ("vi" hoặc "en")
        self.current_theme_index = 0       # Biến số nguyên (do người dùng đặt) – chỉ số theme đang dùng
        self.current_active_menu = "hoso"  # Biến chuỗi (do người dùng đặt) – menu đang mở ("hoso", "data", "hethong")

        # ====================================================================
        # 2.1.2. KHO THEME ĐÃ ĐỒNG BỘ (4 theme với màu sắc khác nhau)
        # ====================================================================
        # Mỗi phần tử là một dict chứa các màu sắc cho từng thành phần (do người dùng định nghĩa)
        self.THEME_PRESETS = [              # Danh sách các theme (biến do người dùng đặt)
            {                               # Theme 0: Cyber Neon
                "name": "Cyber Neon",       # Tên theme (chuỗi hiển thị)
                "window_bg": "#12141A", "card_bg": "#1A1D24", "border_color": "#282C37",
                "text_highlight": "#00F2FE", "entry_bg": "#0D0F13",
                "btn_main": "#00F2FE", "btn_main_hover": "#00C2CE", "btn_main_text": "#000000"
            },
            {                               # Theme 1: Pink Blossom
                "name": "Pink Blossom 🌸",
                "window_bg": "#1A1216", "card_bg": "#25181E", "border_color": "#3D242F",
                "text_highlight": "#FF75A0", "entry_bg": "#130B0F",
                "btn_main": "#FF75A0", "btn_main_hover": "#E0537E", "btn_main_text": "#FFFFFF"
            },
            {                               # Theme 2: Sunset Glow
                "name": "Sunset Glow",
                "window_bg": "#1A1515", "card_bg": "#241D1D", "border_color": "#382A2A",
                "text_highlight": "#FF5E62", "entry_bg": "#140F0F",
                "btn_main": "#FF5E62", "btn_main_hover": "#FF3B40", "btn_main_text": "#FFFFFF"
            },
            {                               # Theme 3: Emerald Mint
                "name": "Emerald Mint",
                "window_bg": "#0B1411", "card_bg": "#12201B", "border_color": "#1F362E",
                "text_highlight": "#10B981", "entry_bg": "#070D0B",
                "btn_main": "#10B981", "btn_main_hover": "#059669", "btn_main_text": "#FFFFFF"
            }
        ]
        # Lấy theme hiện tại (lưu vào self.THEME_CONFIG) – biến do người dùng đặt
        self.THEME_CONFIG = self.THEME_PRESETS[self.current_theme_index]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2.1.3. Cài đặt cửa sổ gốc
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.geometry("1240x670")          # Đặt kích thước cửa sổ (lệnh thư viện) – rộng 1240px, cao 670px
        self.minsize(900, 300)   # chiều rộng tối thiểu 900, chiều cao tối thiểu 500
        ctk.set_appearance_mode("dark")    # Đặt chế độ giao diện của customtkinter là "dark" (lệnh thư viện)
        self.configure(fg_color=self.THEME_CONFIG["window_bg"])
        # Dòng trên: Đặt màu nền của cửa sổ (lệnh thư viện configure) – lấy từ theme
        self.controller = None             # Biến lưu controller (sẽ được gán sau) – do người dùng đặt

        # Nếu đang chạy trên Windows và có pywinstyles, áp dụng hiệu ứng acrylic (trong suốt)
        if pywinstyles and platform.system().lower() == "windows":
            # Dòng trên: Câu lệnh if kiểm tra (lệnh thư viện và biến do người dùng đặt)
            pywinstyles.apply_style(self, "acrylic")  # Lệnh thư viện pywinstyles (nếu có)
        # Kết thúc if

        # ====================================================================
        # 2.1.4. KHUNG CÔNG CỤ (TOOLBAR PANEL) – chứa các menu cha và con
        # ====================================================================
        self.toolbar = ctk.CTkFrame(       # Tạo một Frame (khung) để chứa toolbar – lệnh thư viện CTkFrame
            self,                          # Tham số: parent = self (cửa sổ chính)
            fg_color=self.THEME_CONFIG["card_bg"],           # Màu nền theo theme (từ dict)
            border_color=self.THEME_CONFIG["border_color"], # Màu viền theo theme
            border_width=1,                                 # Độ dày viền là 1 pixel
            corner_radius=16                                # Bo góc 16 pixel
        )
        self.toolbar.pack(fill="x", padx=15, pady=(15, 8))
        # Dòng trên: Đặt toolbar (lệnh thư viện pack) – kéo dài ngang, lề trái/phải 15, lề trên 15 dưới 8

        # Khung chứa các nút, có thanh cuộn ngang (lệnh thư viện CTkScrollableFrame)
        btn_container = ctk.CTkScrollableFrame(
            self.toolbar,                  # Frame cha là toolbar
            orientation="horizontal",      # Hướng cuộn ngang
            height=55,                     # Chiều cao 55 pixel
            fg_color="transparent"         # Nền trong suốt
        )
        btn_container.pack(fill="x", expand=True, padx=5, pady=5)
        # Dòng trên: Đặt container (lệnh thư viện pack) – kéo dài ngang, chiếm không gian dư, lề 5

        btn_font = ("Segoe UI", 12, "bold")
        # Dòng trên: Biến tuple chứa font chữ (do người dùng đặt) – (tên font, cỡ, kiểu)

        # ---------- Menu Cha (3 nút: Hồ sơ, Dữ liệu, Hệ thống) ----------
        self.btn_parent_hoso = ctk.CTkButton(  # Tạo nút menu cha "Hồ sơ" – lệnh thư viện CTkButton
            btn_container,                   # Cha là btn_container
            text="",                         # Chữ sẽ được set sau bằng update_ui_text
            font=btn_font,                   # Font chữ đã định nghĩa
            width=140, height=38,            # Kích thước nút
            corner_radius=10,                # Bo góc 10 pixel
            command=lambda: self.switch_submenu("hoso")
            # Khi bấm, gọi hàm switch_submenu với tham số "hoso" (lambda tạo hàm ẩn danh)
        )
        self.btn_parent_hoso.pack(side="left", padx=4)  # Đặt nút bên trái, cách 4 pixel (lệnh thư viện pack)

        self.btn_parent_data = ctk.CTkButton( # Tạo nút menu cha "Dữ liệu"
            btn_container, text="", font=btn_font, width=140, height=38,
            corner_radius=10, command=lambda: self.switch_submenu("data")
        )
        self.btn_parent_data.pack(side="left", padx=4)

        self.btn_parent_hethong = ctk.CTkButton( # Tạo nút menu cha "Hệ thống"
            btn_container, text="", font=btn_font, width=140, height=38,
            corner_radius=10, command=lambda: self.switch_submenu("hethong")
        )
        self.btn_parent_hethong.pack(side="left", padx=4)

        # Nhãn phân cách giữa menu cha và menu con (dấu ➔)
        self.lbl_menu_sep = ctk.CTkLabel(    # Tạo label (nhãn) – lệnh thư viện
            btn_container, text="➔",         # Nội dung label là ký tự "➔" (hiển thị ra màn hình)
            text_color=self.THEME_CONFIG["text_highlight"],  # Màu chữ theo theme
            font=("Segoe UI", 16, "bold")    # Font chữ
        )
        self.lbl_menu_sep.pack(side="left", padx=15)  # Đặt label bên trái, cách lề 15 pixel

        # ---------- Menu Con (các nút chức năng sẽ được hiển thị động) ----------
        # Các nút này chưa gán command vì sẽ pack/show theo submenu
        self.btn_add = ctk.CTkButton(        # Nút Thêm bệnh nhân
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            command=self.on_add              # Khi bấm, gọi hàm on_add
        )
        self.btn_edit = ctk.CTkButton(       # Nút Sửa
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            command=self.on_edit
        )
        self.btn_history = ctk.CTkButton(    # Nút Lịch sử khám
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            command=self.on_history
        )
        self.btn_delete = ctk.CTkButton(     # Nút Xóa (màu đỏ)
            btn_container, text="", font=btn_font, fg_color="#FF0844", hover_color="#D90434",
            text_color="#FFFFFF", corner_radius=10, height=35, command=self.on_delete
        )
        self.btn_import = ctk.CTkButton(     # Nút Import CSV
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            border_width=1,                  # Có viền
            command=lambda: self.controller.import_csv() if self.controller else None
            # Khi bấm, nếu có controller thì gọi import_csv(), nếu không thì None
        )
        self.btn_export = ctk.CTkButton(     # Nút Export CSV
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            border_width=1,
            command=lambda: self.controller.export_csv() if self.controller else None
        )
        self.btn_template = ctk.CTkButton(   # Nút Xuất mẫu CSV
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            border_width=1,
            command=lambda: self.controller.export_template_csv() if self.controller else None
        )
        self.btn_lang = ctk.CTkButton(       # Nút Đổi ngôn ngữ
            btn_container, text="VN / EN 🌐", font=btn_font, fg_color="#4A148C",
            hover_color="#6A1B9A", text_color="#FFFFFF", corner_radius=10, height=35,
            command=self.toggle_language
        )
        self.btn_theme_switcher = ctk.CTkButton(  # Nút Đổi theme
            btn_container, text="", font=btn_font, fg_color="#2A2F3D", hover_color="#353B4D",
            text_color="#FFFFFF", corner_radius=10, height=35, command=self.switch_system_theme
        )
        self.btn_about = ctk.CTkButton(      # Nút About (Giới thiệu)
            btn_container, text="", font=btn_font, corner_radius=10, height=35,
            border_width=1, command=self.show_about
        )

        # ====================================================================
        # 2.1.5. KHUNG TÌM KIẾM (SEARCH PANEL)
        # ====================================================================
        self.search_panel = ctk.CTkFrame(    # Tạo khung tìm kiếm
            self,
            fg_color=self.THEME_CONFIG["card_bg"],
            border_color=self.THEME_CONFIG["border_color"],
            border_width=1, corner_radius=16
        )
        self.search_panel.pack(fill="x", padx=15, pady=8)  # Đặt khung tìm kiếm (lệnh thư viện pack)

        # Label tiêu đề tìm kiếm (sẽ được cập nhật ngôn ngữ)
        self.lbl_search_title = ctk.CTkLabel(  # Label tiêu đề tìm kiếm – lệnh thư viện
            self.search_panel, text="", font=("Segoe UI", 13, "bold"),
            text_color=self.THEME_CONFIG["text_highlight"]
        )
        self.lbl_search_title.pack(side="left", padx=(20, 10))
        # Dòng trên: Đặt label bên trái, lề trái 20, phải 10 (lệnh thư viện pack)

        # Ô nhập từ khóa tìm kiếm
        self.entry_search = ctk.CTkEntry(    # Ô nhập liệu – lệnh thư viện CTkEntry
            self.search_panel, placeholder_text="", font=("Segoe UI", 13),
            fg_color=self.THEME_CONFIG["entry_bg"],
            border_color=self.THEME_CONFIG["border_color"],
            border_width=1, corner_radius=10, height=38
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        # Dòng trên: Đặt ô nhập bên trái, kéo dãn ngang, chiếm không gian dư, lề 5

        # Nếu là Linux, thêm nút bật/tắt IME (Input Method Editor)
        if self.is_linux:
            # Nếu đang dùng Linux, tạo nút IME
            self.btn_toggle_ime = ctk.CTkButton(
                self.search_panel, text="", font=btn_font, width=140, height=38,
                fg_color="#D35400", hover_color="#E67E22", text_color="#FFFFFF",
                corner_radius=10, command=self.toggle_linux_ime
            )
            self.btn_toggle_ime.pack(side="left", padx=5)  # Đặt nút bên trái
        # Kết thúc if

        # Nút Tìm kiếm
        self.btn_search = ctk.CTkButton(     # Nút Tìm kiếm – lệnh thư viện
            self.search_panel, text="", font=btn_font, width=110, height=38,
            corner_radius=10, command=self.on_search
        )
        self.btn_search.pack(side="left", padx=5)

        # Nút Làm mới dữ liệu (refresh)
        self.btn_refresh = ctk.CTkButton(    # Nút Làm mới – lệnh thư viện
            self.search_panel, text="", font=btn_font, width=110, height=38,
            fg_color="#2A2F3D", hover_color="#353B4D", text_color="#ECEFF4",
            corner_radius=10, command=self.on_refresh_data
        )
        self.btn_refresh.pack(side="left", padx=(5, 20))  # Lề trái 5, phải 20

                # ====================================================================
        # 2.1.6. BẢNG HIỂN THỊ DỮ LIỆU (TREEVIEW PANEL) + THANH THỐNG KÊ (FOOTER PANEL)
        # ====================================================================
        # Tạo scrollable frame bao container để có thanh cuộn dọc khi cửa sổ quá nhỏ,
        # giúp người dùng cuộn xuống thấy thanh thống kê.
        self.table_container = ctk.CTkScrollableFrame(self, orientation="vertical", fg_color="transparent")
        # Đặt container chiếm toàn bộ không gian còn lại (sau toolbar và search panel), co giãn cả 2 chiều
        self.table_container.pack(fill="both", expand=True, padx=15, pady=8)

        # ---------- Khung chứa bảng (Treeview) ----------
        self.tree_frame = ctk.CTkFrame(      # Tạo khung chứa bảng – lệnh thư viện CTkFrame
            self.table_container,            # Gắn vào container thay vì self
            fg_color="#2C3E50",              # Màu nền xanh đen (có thể đổi màu tùy ý)
            border_color="#E74C3C",          # Màu viền đỏ (có thể đổi màu tùy ý)
            border_width=1, corner_radius=16
        )
        # Đặt khung bảng chiếm hầu hết không gian trong container, co giãn cả 2 chiều,
        # có khoảng cách dưới 10px để tách biệt với footer.
        self.tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.style = ttk.Style()             # Tạo đối tượng Style để tùy chỉnh giao diện Treeview (lệnh thư viện)
        self.style.theme_use("clam")         # Chọn theme "clam" (lệnh thư viện)

        columns = ("id", "name", "birth_year", "gender", "phone", "address")
        # Dòng trên: Tuple tên các cột (do người dùng đặt)
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        # Dòng trên: Tạo Treeview (lệnh thư viện), chỉ hiện tiêu đề cột

        # Đặt độ rộng và căn lề cho từng cột (lệnh thư viện column)
        self.tree.column("id", width=60, anchor="center")      # Cột ID rộng 60, canh giữa
        self.tree.column("name", width=240)                    # Cột tên rộng 240
        self.tree.column("birth_year", width=95, anchor="center")
        self.tree.column("gender", width=95, anchor="center")
        self.tree.column("phone", width=145, anchor="center")
        self.tree.column("address", width=220)

        # Thanh cuộn dọc (lệnh thư viện Scrollbar)
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)    # Liên kết bảng với thanh cuộn
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        # Dòng trên: Đặt bảng bên trái, co giãn, lề trái 10 (lệnh thư viện pack)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        # Dòng trên: Đặt thanh cuộn bên phải, kéo dãn dọc, lề phải 10

        # ---------- Khung thống kê (Footer) – nằm dưới bảng, vẫn trong container ----------
        self.stats_frame = ctk.CTkFrame(     # Tạo khung thống kê dưới đáy – lệnh thư viện CTkFrame
            self.table_container,            # Gắn vào container, nằm dưới tree_frame
            fg_color="#15181E",
            border_color=self.THEME_CONFIG["border_color"],
            border_width=1, corner_radius=12
        )
        self.stats_frame.pack(fill="x", side="bottom", pady=(5, 0))
        # Dòng trên: Đặt khung ở dưới cùng của container, kéo dài ngang (lệnh thư viện pack)

        # Các label thống kê
        self.lbl_total = ctk.CTkLabel(       # Label tổng số bệnh nhân – lệnh thư viện
            self.stats_frame, text="", font=("Segoe UI", 12, "bold"),
            text_color=self.THEME_CONFIG["text_highlight"]
        )
        self.lbl_total.pack(side="left", padx=20, pady=8)      # Đặt bên trái (lệnh thư viện pack)

        self.lbl_male = ctk.CTkLabel(        # Label số bệnh nhân nam
            self.stats_frame, text="", font=("Segoe UI", 12),
            text_color="#8A95A5"
        )
        self.lbl_male.pack(side="left", padx=20, pady=8)

        self.lbl_female = ctk.CTkLabel(      # Label số bệnh nhân nữ
            self.stats_frame, text="", font=("Segoe UI", 12),
            text_color="#8A95A5"
        )
        self.lbl_female.pack(side="left", padx=20, pady=8)

        self.lbl_avg_age = ctk.CTkLabel(     # Label tuổi trung bình
            self.stats_frame, text="", font=("Segoe UI", 12),
            text_color="#8A95A5"
        )
        self.lbl_avg_age.pack(side="left", padx=20, pady=8)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2.1.8. Khởi chạy các cấu hình ban đầu (theme, menu, giao diện)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.apply_button_theme_colors()      # Gọi hàm cập nhật màu nút theo theme (do người dùng định nghĩa)
        self.switch_submenu(self.current_active_menu)  # Hiển thị menu con "hoso" ban đầu
        self.update_treeview_style()          # Cập nhật style bảng theo theme
        self.update_ui_text()                 # Cập nhật ngôn ngữ lần đầu
    # Kết thúc __init__

    # ------------------------------------------------------------------------
    # 2.2. CÁC PHƯƠNG THỨC KẾT NỐI CONTROLLER & CẬP NHẬT GIAO DIỆN
    # ------------------------------------------------------------------------
    def set_controller(self, controller):
        """Gắn controller và tải dữ liệu lần đầu."""
        self.controller = controller          # Lưu controller (biến do người dùng đặt)
        self.on_refresh_data()                # Gọi hàm làm mới dữ liệu

    def toggle_language(self):
        """Đổi ngôn ngữ hệ thống (Việt/Anh) và đồng bộ toàn bộ giao diện."""
        new_lang = "en" if self.current_lang == "vi" else "vi"
        # Dòng trên: Xác định ngôn ngữ mới (nếu đang "vi" thì "en", ngược lại "vi")
        self.current_lang = new_lang          # Cập nhật biến ngôn ngữ
        if self.controller:
            # Nếu có controller, gọi phương thức change_global_language để đồng bộ tất cả các cửa sổ
            self.controller.change_global_language(new_lang)
        else:
            self.update_ui_text()             # Tự cập nhật nếu chưa có controller

    def update_ui_text(self):
        """Cập nhật tất cả văn bản (nút, label, tiêu đề) theo ngôn ngữ hiện tại."""
        if self.controller:
            self.current_lang = self.controller.current_lang  # Lấy ngôn ngữ từ controller
        texts = LANGUAGES[self.current_lang]   # Lấy từ điển tương ứng (ví dụ LANGUAGES["vi"])

        # Cập nhật menu cha
        self.btn_parent_hoso.configure(text=texts["menu_hoso"])   # Đặt chữ cho nút "Hồ sơ"
        self.btn_parent_data.configure(text=texts["menu_data"])   # Đặt chữ cho nút "Dữ liệu"
        self.btn_parent_hethong.configure(text=texts["menu_hethong"]) # Đặt chữ cho nút "Hệ thống"

        # Cập nhật menu con
        self.btn_add.configure(text=texts["btn_add"])             # "Thêm bệnh nhân"
        self.btn_edit.configure(text=texts["btn_edit"])           # "Sửa"
        self.btn_history.configure(text=texts["btn_history"])     # "Lịch sử khám"
        self.btn_delete.configure(text=texts["btn_delete"])       # "Xóa"
        self.btn_import.configure(text=texts["btn_import"])       # "Nhập CSV"
        self.btn_export.configure(text=texts["btn_export"])       # "Xuất CSV"
        self.btn_template.configure(text=texts["btn_template"])   # "Tải file mẫu"
        self.btn_about.configure(text=texts["btn_about"])         # "Giới thiệu"
        self.btn_theme_switcher.configure(text=f"{texts['theme_prefix']}{self.THEME_CONFIG['name']} 🎨")
        # Dòng trên: Đặt chữ cho nút đổi theme, hiển thị "Giao diện: Cyber Neon 🎨"

        # Khu vực tìm kiếm
        self.lbl_search_title.configure(text=texts["lbl_search_title"])   # "Bộ lọc tìm kiếm:"
        self.entry_search.configure(placeholder_text=texts["plh_search"]) # "Nhập tên hoặc số điện thoại..."
        self.btn_search.configure(text=texts["btn_search"])               # "Tìm kiếm"
        self.btn_refresh.configure(text=texts["btn_refresh"])             # "Làm mới"
        if self.is_linux and hasattr(self, "btn_toggle_ime"):
            self.btn_toggle_ime.configure(text=texts["btn_toggle_ime"])   # "Bộ gõ Linux"

        # Tiêu đề các cột trong bảng (heading)
        self.tree.heading("id", text=texts["col_id"])          # "Mã BN"
        self.tree.heading("name", text=texts["col_name"])      # "Họ và tên"
        self.tree.heading("birth_year", text=texts["col_birth"]) # "Năm sinh"
        self.tree.heading("gender", text=texts["col_gender"])   # "Giới tính"
        self.tree.heading("phone", text=texts["col_phone"])     # "Số điện thoại"
        self.tree.heading("address", text=texts["col_address"]) # "Địa chỉ"

        # Cập nhật footer thống kê
        self.refresh_stats_labels()

    def apply_button_theme_colors(self):
        """Đồng bộ màu sắc cho các nút theo theme hiện tại."""
        main_color = self.THEME_CONFIG["btn_main"]          # Màu chính của nút (ví dụ #00F2FE)
        hover_color = self.THEME_CONFIG["btn_main_hover"]   # Màu khi rê chuột
        text_color = self.THEME_CONFIG["btn_main_text"]     # Màu chữ trên nút
        border_color = self.THEME_CONFIG["border_color"]    # Màu viền

        # Nút chính (fill background)
        self.btn_add.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_edit.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_history.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_search.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)

        # Nút phụ dạng outline (trong suốt, viền màu)
        for btn in [self.btn_import, self.btn_export, self.btn_template, self.btn_about]:
            btn.configure(
                fg_color="transparent",       # Nền trong suốt
                hover_color="#232731",        # Màu nền khi rê chuột
                text_color="#ECEFF4",         # Màu chữ sáng
                border_color=border_color     # Màu viền theo theme
            )

    def switch_submenu(self, menu_name):
        """Chuyển đổi menu con (hoso, data, hethong), ẩn/hiện các nút tương ứng."""
        self.current_active_menu = menu_name   # Lưu tên menu đang hoạt động
        # Ẩn tất cả nút con (đã pack trước đó)
        for child_btn in [self.btn_add, self.btn_edit, self.btn_history, self.btn_delete,
                          self.btn_import, self.btn_export, self.btn_template,
                          self.btn_lang, self.btn_theme_switcher, self.btn_about]:
            child_btn.pack_forget()             # Gỡ bỏ khỏi giao diện (ẩn)

        bg_inactive = "#2A2F3D"                # Màu nền khi không active (tối)
        bg_active = self.THEME_CONFIG["btn_main"]   # Màu nền khi active (lấy từ theme)
        txt_active = self.THEME_CONFIG["btn_main_text"]  # Màu chữ khi active

        # Cập nhật màu cho các nút cha
        self.btn_parent_hoso.configure(
            fg_color=bg_active if menu_name == "hoso" else bg_inactive,
            text_color=txt_active if menu_name == "hoso" else "#FFFFFF"
        )
        self.btn_parent_data.configure(
            fg_color=bg_active if menu_name == "data" else bg_inactive,
            text_color=txt_active if menu_name == "data" else "#FFFFFF"
        )
        self.btn_parent_hethong.configure(
            fg_color=bg_active if menu_name == "hethong" else bg_inactive,
            text_color=txt_active if menu_name == "hethong" else "#FFFFFF"
        )

        # Hiển thị các nút con tương ứng
        if menu_name == "hoso":
            for btn in [self.btn_add, self.btn_edit, self.btn_history, self.btn_delete]:
                btn.pack(side="left", padx=4)   # Hiển thị lại các nút quản lý hồ sơ
        elif menu_name == "data":
            for btn in [self.btn_import, self.btn_export, self.btn_template]:
                btn.pack(side="left", padx=4)   # Hiển thị nút liên quan đến dữ liệu
        elif menu_name == "hethong":
            for btn in [self.btn_lang, self.btn_theme_switcher, self.btn_about]:
                btn.pack(side="left", padx=4)   # Hiển thị nút hệ thống

    def switch_system_theme(self):
        """Chuyển sang theme tiếp theo trong danh sách và cập nhật giao diện."""
        # Tăng chỉ số theme (vòng tròn)
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEME_PRESETS)
        self.THEME_CONFIG = self.THEME_PRESETS[self.current_theme_index]  # Lấy theme mới

        # Cập nhật màu nền cho các khung
        self.configure(fg_color=self.THEME_CONFIG["window_bg"])           # Màu nền cửa sổ
        self.toolbar.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.search_panel.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.tree_frame.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.stats_frame.configure(border_color=self.THEME_CONFIG["border_color"])  # Chỉ đổi màu viền

        # Cập nhật màu chữ, ô nhập, và style bảng
        self.lbl_menu_sep.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_search_title.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_total.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.entry_search.configure(
            fg_color=self.THEME_CONFIG["entry_bg"],
            border_color=self.THEME_CONFIG["border_color"]
        )

        self.apply_button_theme_colors()        # Áp dụng màu mới cho nút
        self.switch_submenu(self.current_active_menu)  # Làm mới menu con (để cập nhật màu nút cha)
        self.update_treeview_style()            # Cập nhật style bảng
        self.update_ui_text()                   # Cập nhật văn bản (tên theme mới)

    def update_treeview_style(self):
        """Cập nhật style (màu nền, font) cho Treeview theo theme."""
        self.style.configure("Treeview",
            background=self.THEME_CONFIG["card_bg"],         # Màu nền các dòng
            fieldbackground=self.THEME_CONFIG["card_bg"],    # Màu nền vùng dữ liệu
            foreground="#ECEFF4", rowheight=32,              # Màu chữ, chiều cao dòng
            font=("Segoe UI", 11),
            bordercolor=self.THEME_CONFIG["border_color"],
            borderwidth=0
        )
        self.style.configure("Treeview.Heading",
            background=self.THEME_CONFIG["window_bg"],       # Màu nền tiêu đề cột
            foreground=self.THEME_CONFIG["text_highlight"], # Màu chữ tiêu đề
            font=("Segoe UI", 11, "bold"),
            borderwidth=0
        )

    # ------------------------------------------------------------------------
    # 2.3. CÁC HÀM XỬ LÝ DỮ LIỆU VÀ THỐNG KÊ
    # ------------------------------------------------------------------------
    def refresh_table(self):
        """Làm mới bảng (gọi lại on_refresh_data)."""
        self.on_refresh_data()

    def on_refresh_data(self):
        """Tải lại danh sách bệnh nhân từ controller và hiển thị lên bảng."""
        # Xóa tất cả dòng cũ trong Treeview (lệnh thư viện)
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.controller:
            df = self.controller.get_all_patients()   # Lấy DataFrame từ controller
            # Duyệt từng dòng trong DataFrame (iterrows trả về (index, row))
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(
                    row["id"], row["name"], row["birth_year"],
                    row["gender"], row["phone"], row["address"]
                ))  # Chèn dòng mới vào cuối bảng
        self.refresh_stats_labels()    # Cập nhật số liệu thống kê

    def refresh_stats_labels(self):
        """Tính toán lại các chỉ số thống kê (tổng, nam, nữ, tuổi TB) và hiển thị."""
        texts = LANGUAGES[self.current_lang]            # Lấy từ điển ngôn ngữ
        if not self.controller:
            # Nếu chưa có controller, hiển thị 0
            self.lbl_total.configure(text=texts["stats_total"].format(0))
            self.lbl_male.configure(text=texts["stats_male"].format(0))
            self.lbl_female.configure(text=texts["stats_female"].format(0))
            self.lbl_avg_age.configure(text=texts["stats_avg_age"].format(0.0))
            return

        df = self.controller.get_all_patients()        # Lấy dữ liệu
        total = len(df)                                 # Tổng số
        male = len(df[df["gender"] == "Nam"])           # Số nam (lọc DataFrame theo điều kiện)
        female = len(df[df["gender"] == "Nữ"])          # Số nữ

        import datetime
        current_year = datetime.datetime.now().year    # Lấy năm hiện tại (2026)
        try:
            # Chuyển cột birth_year thành số (pd.to_numeric), tính tuổi, lấy trung bình
            avg_age = (current_year - pd.to_numeric(df["birth_year"])).mean()
            if pd.isna(avg_age):   # Nếu không có dữ liệu (NaN)
                avg_age = 0.0
        except:
            avg_age = 0.0

        # Cập nhật các label bằng phương thức format (chèn số vào chuỗi)
        self.lbl_total.configure(text=texts["stats_total"].format(total))
        self.lbl_male.configure(text=texts["stats_male"].format(male))
        self.lbl_female.configure(text=texts["stats_female"].format(female))
        self.lbl_avg_age.configure(text=texts["stats_avg_age"].format(avg_age))

    # ------------------------------------------------------------------------
    # 2.4. XỬ LÝ SỰ KIỆN TỪ CÁC NÚT (ADD, EDIT, DELETE, SEARCH, ...)
    # ------------------------------------------------------------------------
    def on_add(self):
        """Mở popup thêm bệnh nhân."""
        if self.controller:
            AddEditPatientWindow(self, self.controller, edit_mode=False)

    def on_edit(self):
        """Mở popup sửa bệnh nhân nếu đã chọn một dòng."""
        selected = self.tree.selection()          # Lấy các dòng được chọn (tuple)
        if not selected:
            texts = LANGUAGES[self.current_lang]
            # Hiển thị cảnh báo (messagebox) bằng ngôn ngữ hiện tại
            messagebox.showwarning(
                texts["err_title"],
                "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient"
            )
            return
        item_data = self.tree.item(selected[0])["values"]  # Lấy giá trị dòng đầu tiên
        patient_data = {
            "id": item_data[0],
            "name": item_data[1],
            "birth_year": item_data[2],
            "gender": item_data[3],
            "phone": item_data[4],
            "address": item_data[5]
        }
        AddEditPatientWindow(self, self.controller, edit_mode=True, patient_data=patient_data)

    def on_history(self):
        """Mở cửa sổ lịch sử khám bệnh của bệnh nhân được chọn."""
        selected_item = self.tree.selection()
        texts = LANGUAGES[self.current_lang]
        if not selected_item:
            messagebox.showwarning(
                texts["err_title"],
                "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient"
            )
            return

        item_data = self.tree.item(selected_item[0]).get("values", [])
        if not item_data:
            return
        patient_data = {
            "id": item_data[0],
            "name": item_data[1],
            "birth_year": item_data[2],
            "gender": item_data[3],
            "phone": item_data[4],
            "address": item_data[5]
        }
        try:
            from views.medical_history import MedicalHistoryWindow   # Import động để tránh vòng lặp
            MedicalHistoryWindow(self, self.controller, patient_data)
        except ImportError:
            messagebox.showerror(
                texts["err_title"],
                "Không tìm thấy tệp giao diện lịch sử khám bệnh!" if self.current_lang == "vi" else "Medical history interface file not found!"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khởi chạy: {str(e)}")

    def on_delete(self):
        """Xóa bệnh nhân đã chọn sau khi xác nhận."""
        selected = self.tree.selection()
        if not selected:
            texts = LANGUAGES[self.current_lang]
            messagebox.showwarning(
                texts["err_title"],
                "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient"
            )
            return
        texts = LANGUAGES[self.current_lang]
        confirm = messagebox.askyesno(
            texts["msg_confirm"],
            "Xóa bệnh nhân này sẽ mất hết lịch sử khám?" if self.current_lang == "vi" else "Deleting this patient will clear all medical records?"
        )
        if confirm:
            item_data = self.tree.item(selected[0])["values"]
            self.controller.delete_patient(item_data[0])   # Gọi controller xóa

    def on_search(self):
        """Tìm kiếm bệnh nhân theo tên hoặc số điện thoại (không phân biệt hoa thường)."""
        query = self.entry_search.get().strip().lower()   # Lấy từ khóa, bỏ khoảng trắng, viết thường
        # Xóa bảng cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.controller and query:
            df = self.controller.get_all_patients()
            for _, row in df.iterrows():
                if query in str(row["name"]).lower() or query in str(row["phone"]):
                    self.tree.insert("", "end", values=(
                        row["id"], row["name"], row["birth_year"],
                        row["gender"], row["phone"], row["address"]
                    ))
        else:
            # Nếu không có từ khóa (query rỗng), làm mới toàn bộ
            self.on_refresh_data()

    def toggle_linux_ime(self):
        """Bật/tắt IME trên Linux (chỉ thay đổi trạng thái, chưa thực thi thực tế)."""
        self.linux_ime_active = not self.linux_ime_active
        # Có thể hiển thị thông báo hoặc thay đổi icon nếu muốn

    def show_about(self):
        """Hiển thị hộp thoại giới thiệu (About)."""
        texts = LANGUAGES[self.current_lang]
        if self.current_lang == "vi":
            msg = ("📋 PHẦN MỀM QUẢN LÝ HỒ SƠ BỆNH NHÂN\n\n"
                   "Phiên bản: 1.0.0\n"
                   "Tác giả: Nhóm 5 - Lập trình Python\n"
                   "   Trần Minh Hiếu\n"
                   "   Nguyễn Đức Đại Nam\n"
                   "   Nguyễn Quang Thái\n"
                   "   Hà Văn Tú\n"
                   "Trường Đại học Hạ Long (UHL)\n"
                   "Ngày phát hành: 05/2026\n\n"
                   "© 2026 - Bản quyền thuộc về nhóm phát triển.")
        else:
            msg = ("📋 PATIENT RECORD MANAGEMENT SOFTWARE\n\n"
                   "Version: 1.0.0\n"
                   "Authors: Group 5 - Python Programming\n"
                   "   Tran Minh Hieu\n"
                   "   Nguyen Duc Dai Nam\n"
                   "   Nguyen Quang Thai\n"
                   "   Ha Van Tu\n"
                   "Ha Long University (UHL)\n"
                   "Release Date: 05/2026\n\n"
                   "© 2026 - Copyright belongs to the development team.")
        messagebox.showinfo(texts["btn_about"], msg)   # Hiển thị hộp thoại với tiêu đề lấy từ texts