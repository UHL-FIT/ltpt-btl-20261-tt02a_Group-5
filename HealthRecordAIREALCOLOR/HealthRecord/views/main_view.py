# views/main_view.py

import customtkinter as ctk
from tkinter import ttk, messagebox
import platform  
import pandas as pd
import datetime
from models import patient as model
from views.add_edit_patient import AddEditPatientWindow
from config.languages import LANGUAGES  # Đảm bảo import bảng ngôn ngữ

# 🔥 IMPORT Helper bộ gõ tiếng Việt toàn cục
from utils.ime_helper import LinuxIMEHelper

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HealthRecord")
        # --- Trạng thái hệ thống ---
        self.is_linux = platform.system().lower() == "linux"  
        # Đồng bộ trạng thái ban đầu từ IME Helper toàn cục
        self.linux_ime_active = LinuxIMEHelper.ime_active  
        self.current_lang = "vi"  
        self.current_theme_index = 0  
        self.current_active_menu = "hoso" 

        # =========================================================================
        # 🎨 KHO THEME ĐÃ ĐỒNG BỘ
        # =========================================================================
        self.THEME_PRESETS = [
            {
                "name": "Cyber Neon",
                "window_bg": "#12141A", "card_bg": "#1A1D24", "border_color": "#282C37",
                "text_highlight": "#00F2FE", "entry_bg": "#0D0F13",
                "btn_main": "#00F2FE", "btn_main_hover": "#00C2CE", "btn_main_text": "#000000"
            },
            {
                "name": "Pink Blossom 🌸",
                "window_bg": "#1A1216", "card_bg": "#25181E", "border_color": "#3D242F",
                "text_highlight": "#FF75A0", "entry_bg": "#130B0F",
                "btn_main": "#FF75A0", "btn_main_hover": "#E0537E", "btn_main_text": "#FFFFFF"
            },
            {
                "name": "Sunset Glow",
                "window_bg": "#1A1515", "card_bg": "#241D1D", "border_color": "#382A2A",
                "text_highlight": "#FF5E62", "entry_bg": "#140F0F",
                "btn_main": "#FF5E62", "btn_main_hover": "#FF3B40", "btn_main_text": "#FFFFFF"
            },
            {
                "name": "Emerald Mint",
                "window_bg": "#0B1411", "card_bg": "#12201B", "border_color": "#1F362E",
                "text_highlight": "#10B981", "entry_bg": "#070D0B",
                "btn_main": "#10B981", "btn_main_hover": "#059669", "btn_main_text": "#FFFFFF"
            }
        ]
        
        self.THEME_CONFIG = self.THEME_PRESETS[self.current_theme_index]

        # --- Thiết lập cửa sổ gốc ---
        self.geometry("1240x670")  
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.THEME_CONFIG["window_bg"])
        self.controller = None

        if pywinstyles and platform.system().lower() == "windows":
            pywinstyles.apply_style(self, "acrylic")

        # =========================================================================
        # 🛠️ KHUNG CÔNG CỤ (TOOLBAR PANEL)
        # =========================================================================
        self.toolbar = ctk.CTkFrame(self, fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"], border_width=1, corner_radius=16)
        self.toolbar.pack(fill="x", padx=15, pady=(15, 8))

        btn_container = ctk.CTkScrollableFrame(self.toolbar, orientation="horizontal", height=55, fg_color="transparent")
        btn_container.pack(fill="x", expand=True, padx=5, pady=5)

        btn_font = ("Segoe UI", 12, "bold")

        # Khởi tạo Menu Cha
        self.btn_parent_hoso = ctk.CTkButton(btn_container, text="", font=btn_font, width=140, height=38, corner_radius=10, command=lambda: self.switch_submenu("hoso"))
        self.btn_parent_hoso.pack(side="left", padx=4)

        self.btn_parent_data = ctk.CTkButton(btn_container, text="", font=btn_font, width=140, height=38, corner_radius=10, command=lambda: self.switch_submenu("data"))
        self.btn_parent_data.pack(side="left", padx=4)

        self.btn_parent_hethong = ctk.CTkButton(btn_container, text="", font=btn_font, width=140, height=38, corner_radius=10, command=lambda: self.switch_submenu("hethong"))
        self.btn_parent_hethong.pack(side="left", padx=4)

        self.lbl_menu_sep = ctk.CTkLabel(btn_container, text="➔", text_color=self.THEME_CONFIG["text_highlight"], font=("Segoe UI", 16, "bold"))
        self.lbl_menu_sep.pack(side="left", padx=15)

        # Khởi tạo Menu Con
        self.btn_add = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, command=self.on_add)
        self.btn_edit = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, command=self.on_edit)
        self.btn_history = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, command=self.on_history)
        self.btn_delete = ctk.CTkButton(btn_container, text="", font=btn_font, fg_color="#FF0844", hover_color="#D90434", text_color="#FFFFFF", corner_radius=10, height=35, command=self.on_delete)

        # Đồng bộ cấu hình style nút tính năng phụ
        self.btn_import = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, border_width=1, command=lambda: self.controller.import_csv() if self.controller else None)
        self.btn_export = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, border_width=1, command=lambda: self.controller.export_csv() if self.controller else None)
        self.btn_template = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, border_width=1, command=lambda: self.controller.export_template_csv() if self.controller else None)

        self.btn_lang = ctk.CTkButton(btn_container, text="VN / EN 🌐", font=btn_font, fg_color="#4A148C", hover_color="#6A1B9A", text_color="#FFFFFF", corner_radius=10, height=35, command=self.toggle_language)
        self.btn_theme_switcher = ctk.CTkButton(btn_container, text="", font=btn_font, fg_color="#2A2F3D", hover_color="#353B4D", text_color="#FFFFFF", corner_radius=10, height=35, command=self.switch_system_theme)
        self.btn_about = ctk.CTkButton(btn_container, text="", font=btn_font, corner_radius=10, height=35, border_width=1, command=self.show_about)

        # =========================================================================
        # 2. KHUNG TÌM KIẾM (SEARCH PANEL)
        # =========================================================================
        self.search_panel = ctk.CTkFrame(self, fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"], border_width=1, corner_radius=16)
        self.search_panel.pack(fill="x", padx=15, pady=8)

        self.lbl_search_title = ctk.CTkLabel(self.search_panel, text="", font=("Segoe UI", 13, "bold"), text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_search_title.pack(side="left", padx=(20, 10))

        self.entry_search = ctk.CTkEntry(self.search_panel, placeholder_text="", font=("Segoe UI", 13), fg_color=self.THEME_CONFIG["entry_bg"], border_color=self.THEME_CONFIG["border_color"], border_width=1, corner_radius=10, height=38)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=5, pady=10)

        # 🔍 Nút chuyển đổi bộ gõ: CHỈ hiển thị và đóng gói khi chạy trên hệ điều hành Linux
        if self.is_linux:
            # Xác định chữ hiển thị ban đầu dựa trên trạng thái của bộ gõ helper toàn cục
            ime_initial_text = "Bộ gõ: VN 🇻🇳" if self.linux_ime_active else "Bộ gõ: EN 🇬🇧"
            
            self.btn_toggle_ime = ctk.CTkButton(
                self.search_panel, 
                text=ime_initial_text, 
                font=btn_font, 
                width=140, 
                height=38, 
                fg_color="#D35400" if self.linux_ime_active else "#7F8C8D", 
                hover_color="#E67E22" if self.linux_ime_active else "#95A5A6", 
                text_color="#FFFFFF", 
                corner_radius=10, 
                command=self.toggle_linux_ime
            )
            self.btn_toggle_ime.pack(side="left", padx=5)

        self.btn_search = ctk.CTkButton(self.search_panel, text="", font=btn_font, width=110, height=38, corner_radius=10, command=self.on_search)
        self.btn_search.pack(side="left", padx=5)

        self.btn_refresh = ctk.CTkButton(self.search_panel, text="", font=btn_font, width=110, height=38, fg_color="#2A2F3D", hover_color="#353B4D", text_color="#ECEFF4", corner_radius=10, command=self.on_refresh_data)
        self.btn_refresh.pack(side="left", padx=(5, 20))

        # =========================================================================
        # 3. BẢNG HIỂN THỊ DỮ LIỆU (TREEVIEW PANEL)
        # =========================================================================
        self.tree_frame = ctk.CTkFrame(self, fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"], border_width=1, corner_radius=16)
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=8)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        columns = ("id", "name", "birth_year", "gender", "phone", "address")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=240)
        self.tree.column("birth_year", width=95, anchor="center")
        self.tree.column("gender", width=95, anchor="center")
        self.tree.column("phone", width=145, anchor="center")
        self.tree.column("address", width=220)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # =========================================================================
        # 4. THANH THỐNG KÊ (FOOTER PANEL)
        # =========================================================================
        self.stats_frame = ctk.CTkFrame(self, fg_color="#15181E", border_color=self.THEME_CONFIG["border_color"], border_width=1, corner_radius=12)
        self.stats_frame.pack(side="bottom", fill="x", padx=15, pady=(5, 15))

        self.lbl_total = ctk.CTkLabel(self.stats_frame, text="", font=("Segoe UI", 12, "bold"), text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_total.pack(side="left", padx=20, pady=8)

        self.lbl_male = ctk.CTkLabel(self.stats_frame, text="", font=("Segoe UI", 12), text_color="#8A95A5")
        self.lbl_male.pack(side="left", padx=20, pady=8)

        self.lbl_female = ctk.CTkLabel(self.stats_frame, text="", font=("Segoe UI", 12), text_color="#8A95A5")
        self.lbl_female.pack(side="left", padx=20, pady=8)

        self.lbl_avg_age = ctk.CTkLabel(self.stats_frame, text="", font=("Segoe UI", 12), text_color="#8A95A5")
        self.lbl_avg_age.pack(side="left", padx=20, pady=8)

        # Khởi chạy các cấu hình ban đầu
        self.apply_button_theme_colors()
        self.switch_submenu(self.current_active_menu)
        self.update_treeview_style()
        self.update_ui_text()

        # 🔥 ÁP DỤNG bộ gõ tiếng Việt tự chế tập trung cho ô tìm kiếm
        LinuxIMEHelper.apply_ime_to_widgets(self, [self.entry_search])

    def set_controller(self, controller):
        self.controller = controller
        self.on_refresh_data()

    def toggle_language(self):
        """Đổi ngôn ngữ hệ thống và đồng bộ toàn bộ app."""
        new_lang = "en" if self.current_lang == "vi" else "vi"
        self.current_lang = new_lang
        if self.controller:
            self.controller.change_global_language(new_lang)
        else:
            self.update_ui_text()

    def update_ui_text(self):
        """Đồng bộ ngôn ngữ nóng cho toàn bộ MainView."""
        if self.controller:
            self.current_lang = self.controller.current_lang

        texts = LANGUAGES[self.current_lang]

        # 1. Cập nhật tiêu đề Menu Cha
        self.btn_parent_hoso.configure(text=texts["menu_hoso"])
        self.btn_parent_data.configure(text=texts["menu_data"])
        self.btn_parent_hethong.configure(text=texts["menu_hethong"])

        # 2. Cập nhật nút Menu Con
        self.btn_add.configure(text=texts["btn_add"])
        self.btn_edit.configure(text=texts["btn_edit"])
        self.btn_history.configure(text=texts["btn_history"])
        self.btn_delete.configure(text=texts["btn_delete"])
        self.btn_import.configure(text=texts["btn_import"])
        self.btn_export.configure(text=texts["btn_export"])
        self.btn_template.configure(text=texts["btn_template"])
        self.btn_about.configure(text=texts["btn_about"])

        self.btn_theme_switcher.configure(text=f"{texts['theme_prefix']}{self.THEME_CONFIG['name']} 🎨")

        # 3. Khu vực tìm kiếm
        self.lbl_search_title.configure(text=texts["lbl_search_title"])
        self.entry_search.configure(placeholder_text=texts["plh_search"])
        self.btn_search.configure(text=texts["btn_search"])
        self.btn_refresh.configure(text=texts["btn_refresh"])
        
        # 🇻🇳 / 🇬🇧 Giữ vững trạng thái hiển thị VN/EN cho nút gõ của Linux kể cả khi đổi ngôn ngữ ứng dụng
        if self.is_linux and hasattr(self, "btn_toggle_ime"):
            ime_text = "Bộ gõ: VN 🇻🇳" if self.linux_ime_active else "Bộ gõ: EN 🇬🇧"
            self.btn_toggle_ime.configure(text=ime_text)

        # 4. Tiêu đề các cột trong bảng dữ liệu Treeview
        self.tree.heading("id", text=texts["col_id"])
        self.tree.heading("name", text=texts["col_name"])
        self.tree.heading("birth_year", text=texts["col_birth"])
        self.tree.heading("gender", text=texts["col_gender"])
        self.tree.heading("phone", text=texts["col_phone"])
        self.tree.heading("address", text=texts["col_address"])

        # 5. Cập nhật thông tin thống kê Footer
        self.refresh_stats_labels()

    def apply_button_theme_colors(self):
        """Đồng bộ màu sắc nút chức năng theo cấu hình Theme."""
        main_color = self.THEME_CONFIG["btn_main"]
        hover_color = self.THEME_CONFIG["btn_main_hover"]
        text_color = self.THEME_CONFIG["btn_main_text"]
        border_color = self.THEME_CONFIG["border_color"]

        # Các nút chính (Fill background)
        self.btn_add.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_edit.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_history.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)
        self.btn_search.configure(fg_color=main_color, hover_color=hover_color, text_color=text_color)

        # Các nút phụ dạng outline
        for btn in [self.btn_import, self.btn_export, self.btn_template, self.btn_about]:
            btn.configure(
                fg_color="transparent",
                hover_color="#232731",
                text_color="#ECEFF4",  
                border_color=border_color
            )

    def switch_submenu(self, menu_name):
        self.current_active_menu = menu_name
        for child_btn in [self.btn_add, self.btn_edit, self.btn_history, self.btn_delete, self.btn_import, self.btn_export, self.btn_template, self.btn_lang, self.btn_theme_switcher, self.btn_about]:
            child_btn.pack_forget()
            
        bg_inactive = "#2A2F3D"
        bg_active = self.THEME_CONFIG["btn_main"]
        txt_active = self.THEME_CONFIG["btn_main_text"]
        
        self.btn_parent_hoso.configure(fg_color=bg_active if menu_name == "hoso" else bg_inactive, text_color=txt_active if menu_name == "hoso" else "#FFFFFF")
        self.btn_parent_data.configure(fg_color=bg_active if menu_name == "data" else bg_inactive, text_color=txt_active if menu_name == "data" else "#FFFFFF")
        self.btn_parent_hethong.configure(fg_color=bg_active if menu_name == "hethong" else bg_inactive, text_color=txt_active if menu_name == "hethong" else "#FFFFFF")
        
        if menu_name == "hoso":
            self.btn_add.pack(side="left", padx=4)
            self.btn_edit.pack(side="left", padx=4)
            self.btn_history.pack(side="left", padx=4)
            self.btn_delete.pack(side="left", padx=4)
        elif menu_name == "data":
            self.btn_import.pack(side="left", padx=4)
            self.btn_export.pack(side="left", padx=4)
            self.btn_template.pack(side="left", padx=4)
        elif menu_name == "hethong":
            self.btn_lang.pack(side="left", padx=4)
            self.btn_theme_switcher.pack(side="left", padx=4)
            self.btn_about.pack(side="left", padx=4)

    def switch_system_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEME_PRESETS)
        self.THEME_CONFIG = self.THEME_PRESETS[self.current_theme_index]
        
        self.configure(fg_color=self.THEME_CONFIG["window_bg"])
        self.toolbar.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.search_panel.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.tree_frame.configure(fg_color=self.THEME_CONFIG["card_bg"], border_color=self.THEME_CONFIG["border_color"])
        self.stats_frame.configure(border_color=self.THEME_CONFIG["border_color"])
        
        self.lbl_menu_sep.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_search_title.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.lbl_total.configure(text_color=self.THEME_CONFIG["text_highlight"])
        self.entry_search.configure(fg_color=self.THEME_CONFIG["entry_bg"], border_color=self.THEME_CONFIG["border_color"])
        
        self.apply_button_theme_colors()
        self.switch_submenu(self.current_active_menu)
        self.update_treeview_style()
        self.update_ui_text()

    def update_treeview_style(self):
        self.style.configure("Treeview", background=self.THEME_CONFIG["card_bg"], fieldbackground=self.THEME_CONFIG["card_bg"], foreground="#ECEFF4", rowheight=32, font=("Segoe UI", 11), bordercolor=self.THEME_CONFIG["border_color"], borderwidth=0)
        self.style.configure("Treeview.Heading", background=self.THEME_CONFIG["window_bg"], foreground=self.THEME_CONFIG["text_highlight"], font=("Segoe UI", 11, "bold"), borderwidth=0)

    def refresh_table(self):
        self.on_refresh_data()

    def on_refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.controller:
            df = self.controller.get_all_patients()
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(row["id"], row["name"], row["birth_year"], row["gender"], row["phone"], row["address"]))
        self.refresh_stats_labels()

    def refresh_stats_labels(self):
        texts = LANGUAGES[self.current_lang]
        if not self.controller:
            self.lbl_total.configure(text=texts["stats_total"].format(0))
            self.lbl_male.configure(text=texts["stats_male"].format(0))
            self.lbl_female.configure(text=texts["stats_female"].format(0))
            self.lbl_avg_age.configure(text=texts["stats_avg_age"].format(0.0))
            return

        df = self.controller.get_all_patients()
        total = len(df)
        male = len(df[df["gender"] == "Nam"])
        female = len(df[df["gender"] == "Nữ"])
        
        current_year = datetime.datetime.now().year
        try:
            avg_age = (current_year - pd.to_numeric(df["birth_year"])).mean()
            if pd.isna(avg_age): avg_age = 0.0
        except:
            avg_age = 0.0

        self.lbl_total.configure(text=texts["stats_total"].format(total))
        self.lbl_male.configure(text=texts["stats_male"].format(male))
        self.lbl_female.configure(text=texts["stats_female"].format(female))
        self.lbl_avg_age.configure(text=texts["stats_avg_age"].format(avg_age))

    def on_add(self):
        if self.controller:
            AddEditPatientWindow(self, self.controller, edit_mode=False)

    def on_edit(self):
        selected = self.tree.selection()
        if not selected:
            texts = LANGUAGES[self.current_lang]
            messagebox.showwarning(texts["err_title"], "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient")
            return
        item_data = self.tree.item(selected[0])["values"]
        patient_data = {
            "id": item_data[0], "name": item_data[1], "birth_year": item_data[2],
            "gender": item_data[3], "phone": item_data[4], "address": item_data[5]
        }
        AddEditPatientWindow(self, self.controller, edit_mode=True, patient_data=patient_data)

    def on_history(self):
        selected_item = self.tree.selection()
        texts = LANGUAGES[self.current_lang]

        if not selected_item:
            messagebox.showwarning(texts["err_title"], "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient")
            return

        item_data = self.tree.item(selected_item[0])
        values = item_data.get("values", [])

        if not values:
            return

        patient_data = {
            "id": values[0], "name": values[1], "birth_year": values[2],
            "gender": values[3], "phone": values[4], "address": values[5]
        }

        try:
            from views.medical_history import MedicalHistoryWindow
            MedicalHistoryWindow(self, self.controller, patient_data)
        except ImportError:
            messagebox.showerror(texts["err_title"], "Không tìm thấy tệp giao diện lịch sử khám bệnh!" if self.current_lang == "vi" else "Medical history interface file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khởi chạy: {str(e)}")

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            texts = LANGUAGES[self.current_lang]
            messagebox.showwarning(texts["err_title"], "Vui lòng chọn một bệnh nhân" if self.current_lang == "vi" else "Please select a patient")
            return
        texts = LANGUAGES[self.current_lang]
        confirm = messagebox.askyesno(texts["msg_confirm"], "Xóa bệnh nhân này sẽ mất hết lịch sử khám?" if self.current_lang == "vi" else "Deleting this patient will clear all medical records?")
        if confirm:
            item_data = self.tree.item(selected[0])["values"]
            self.controller.delete_patient(item_data[0])

    def on_search(self):
        query = self.entry_search.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.controller:
            df = self.controller.get_all_patients()
            for _, row in df.iterrows():
                if query in str(row["name"]).lower() or query in str(row["phone"]):
                    self.tree.insert("", "end", values=(row["id"], row["name"], row["birth_year"], row["gender"], row["phone"], row["address"]))

    # 🔥 ĐỒNG BỘ Trạng thái bật/tắt bộ gõ toàn cục qua Helper và cập nhật nhãn VN / EN 
    def toggle_linux_ime(self):
        is_active = LinuxIMEHelper.toggle_ime()
        self.linux_ime_active = is_active
        
        # Thay đổi màu sắc và nội dung chữ hiển thị trực quan theo chế độ gõ
        if is_active:
            self.btn_toggle_ime.configure(
                text="Bộ gõ: VN 🇻🇳", 
                fg_color="#D35400", 
                hover_color="#E67E22"
            )
        else:
            self.btn_toggle_ime.configure(
                text="Bộ gõ: EN 🇬🇧", 
                fg_color="#7F8C8D", 
                hover_color="#95A5A6"
            )

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