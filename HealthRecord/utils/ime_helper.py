# utils/ime_helper.py
import customtkinter as ctk
import platform

class LinuxIMEHelper:
    """Helper quản lý toàn cục bộ gõ Telex tự chế dành riêng cho Linux"""
    
    # Trạng thái bật/tắt bộ gõ toàn cục (Mặc định là Bật)
    ime_active = True
    is_linux = platform.system().lower() == "linux"

    @classmethod
    def toggle_ime(cls):
        """Hàm bật tắt trạng thái gõ"""
        cls.ime_active = not cls.ime_active
        return cls.ime_active

    @classmethod
    def apply_ime_to_widgets(cls, window, widgets):
        """Gán sự kiện tự động sửa chữ Telex cho danh sách các ô nhập liệu"""
        if not cls.is_linux:
            # Nếu không phải Linux, chỉ bind cơ chế update_idletasks thông thường đề phòng lag phím
            for widget in widgets:
                widget.bind("<KeyRelease>", lambda event: event.widget.after(1, lambda: event.widget.update_idletasks()))
            return

        # Nếu là Linux, áp dụng thuật toán ép dịch Telex thông minh
        for widget in widgets:
            widget.bind("<KeyRelease>", cls.fix_vietnamese_ime)

    @classmethod
    def fix_vietnamese_ime(cls, event):
        widget = event.widget
        if not cls.ime_active or not cls.is_linux: return
        if event.keysym in ["BackSpace", "Delete", "Left", "Right", "Up", "Down", "Tab", "Escape", "Return"]: return
        
        if isinstance(widget, ctk.CTkTextbox):
            text = widget.get("1.0", "end-1c")
        elif hasattr(widget, "get"):
            text = widget.get()
        else:
            return

        if not text: return
        vowels_map = {"aa": "â", "aw": "ă", "ee": "ê", "oo": "ô", "ow": "ơ", "w": "ư", "dd": "đ", "AA": "Â", "AW": "Ă", "EE": "Ê", "OO": "Ô", "OW": "Ơ", "W": "Ư", "DD": "Đ"}
        tone_map = {
            "as": "á", "âs": "ấ", "ăs": "ắ", "es": "é", "ês": "ế", "is": "í", "os": "ó", "ôs": "ố", "ơs": "ớ", "us": "ú", "ưs": "ứ", "ys": "ý",
            "af": "à", "âf": "ầ", "ăf": "ằ", "ef": "è", "êf": "ề", "if": "ì", "of": "ò", "ôf": "ồ", "ơf": "ờ", "uf": "ù", "ưf": "ừ", "yf": "ỳ",
            "ar": "ả", "âr": "ẩ", "ăr": "ẳ", "er": "ẻ", "êr": "ể", "ir": "ỉ", "or": "ỏ", "ôr": "ổ", "ơr": "ở", "ur": "ủ", "ưr": "ử", "yr": "ỷ",
            "ax": "ã", "âx": "ẫ", "ăx": "ẵ", "ex": "ẽ", "êx": "ễ", "ix": "ĩ", "ox": "õ", "ôx": "ỗ", "ơx": "ỡ", "ux": "ũ", "ưx": "ữ", "yx": "ỹ",
            "aj": "ạ", "âj": "ậ", "ăj": "ặ", "ej": "ẹ", "êj": "ệ", "ij": "ị", "oj": "ọ", "ôj": "ộ", "ơj": "ợ", "uj": "ụ", "ưj": "ự", "yj": "ỵ"
        }
        
        new_text = text
        for telex, uni in vowels_map.items():
            if telex in new_text: new_text = new_text.replace(telex, uni)
        for telex, uni in tone_map.items():
            if telex in new_text: new_text = new_text.replace(telex, uni)
            
        if new_text != text:
            len_diff = len(text) - len(new_text)
            
            if isinstance(widget, ctk.CTkTextbox):
                current_cursor = widget.index(ctk.INSERT)
                widget.delete("1.0", ctk.END)
                widget.insert("1.0", new_text)
                widget.mark_set(ctk.INSERT, current_cursor)
            else:
                try:
                    current_cursor = int(widget.index(ctk.INSERT))
                    new_cursor = max(0, current_cursor - len_diff)
                    widget.delete(0, ctk.END)
                    widget.insert(0, new_text)
                    widget.icursor(new_cursor)
                except Exception:
                    widget.delete(0, ctk.END)
                    widget.insert(0, new_text)
                    widget.icursor(ctk.END)