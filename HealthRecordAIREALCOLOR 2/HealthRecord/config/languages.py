# ============================================================================
# FILE: config/languages.py
# MỤC ĐÍCH: Lưu trữ các chuỗi văn bản (giao diện, thông báo) cho hai ngôn ngữ:
#           Tiếng Việt ("vi") và Tiếng Anh ("en").
#           Các chuỗi này được sử dụng xuyên suốt ứng dụng để hỗ trợ đa ngôn ngữ.
# ============================================================================

# ============================================================================
# 1. TỪ ĐIỂN LANGUAGES (dict) - KHÓA CHÍNH LÀ MÃ NGÔN NGỮ
# ============================================================================
# Biến LANGUAGES là một dictionary (từ điển) do người dùng định nghĩa.
# Mỗi khóa là mã ngôn ngữ (vi hoặc en), giá trị là một dictionary con chứa các chuỗi.
LANGUAGES = {
    # Dòng trên: mở ngoặc nhọn bắt đầu dictionary LANGUAGES (lệnh gán biến)

    # ------------------------------------------------------------------------
    # 1.1. TIẾNG VIỆT (vi)
    # ------------------------------------------------------------------------
    "vi": {
        # Dòng trên: khóa "vi" (mã ngôn ngữ Tiếng Việt), giá trị là dictionary con (bắt đầu bằng {)

        # ------------------ Cửa sổ Thêm / Sửa Bệnh nhân (AddEditPatientWindow) ------------------
        "title_add": "Thêm bệnh nhân",
        # ^ Key "title_add" – chuỗi hiển thị trên tiêu đề cửa sổ khi thêm bệnh nhân.
        #   Giá trị: "Thêm bệnh nhân" (dòng chữ xuất hiện trên thanh tiêu đề).

        "title_edit": "Sửa bệnh nhân",
        # ^ Key "title_edit" – tiêu đề cửa sổ khi sửa bệnh nhân. Hiển thị "Sửa bệnh nhân".

        "lbl_name": "Họ tên:",
        # ^ Key "lbl_name" – nhãn (label) cho ô nhập họ tên. Hiển thị "Họ tên:".

        "plh_name": "Nhập họ tên",
        # ^ Key "plh_name" – placeholder (gợi ý) trong ô nhập họ tên. Hiển thị "Nhập họ tên".

        "lbl_birth": "Năm sinh:",
        # ^ Key "lbl_birth" – nhãn cho ô nhập năm sinh. Hiển thị "Năm sinh:".

        "plh_birth": "VD: 1990",
        # ^ Key "plh_birth" – placeholder năm sinh. Hiển thị "VD: 1990".

        "lbl_gender": "Giới tính:",
        # ^ Key "lbl_gender" – nhãn cho combobox giới tính. Hiển thị "Giới tính:".

        "gender_male": "Nam",
        # ^ Key "gender_male" – giá trị hiển thị cho giới tính Nam. Hiển thị "Nam".

        "gender_female": "Nữ",
        # ^ Key "gender_female" – giá trị hiển thị cho giới tính Nữ. Hiển thị "Nữ".

        "lbl_phone": "Số điện thoại:",
        # ^ Key "lbl_phone" – nhãn cho ô nhập số điện thoại. Hiển thị "Số điện thoại:".

        "lbl_address": "Địa chỉ:",
        # ^ Key "lbl_address" – nhãn cho ô nhập địa chỉ. Hiển thị "Địa chỉ:".

        "plh_address": "Địa chỉ",
        # ^ Key "plh_address" – placeholder địa chỉ. Hiển thị "Địa chỉ".

        "btn_save": "Lưu",
        # ^ Key "btn_save" – văn bản trên nút Lưu. Hiển thị "Lưu".

        "btn_cancel": "Hủy",
        # ^ Key "btn_cancel" – văn bản trên nút Hủy. Hiển thị "Hủy".

        "err_title": "Lỗi",
        # ^ Key "err_title" – tiêu đề hộp thoại lỗi. Hiển thị "Lỗi".

        "err_empty_name": "Họ tên không được để trống",
        # ^ Key "err_empty_name" – thông báo lỗi khi họ tên trống. Hiển thị "Họ tên không được để trống".

        "err_empty_birth": "Vui lòng nhập năm sinh",
        # ^ Key "err_empty_birth" – thông báo khi chưa nhập năm sinh.

        "err_invalid_birth": "Năm sinh phải từ 1900 đến 2026",
        # ^ Key "err_invalid_birth" – thông báo lỗi năm sinh sai.

        "err_invalid_phone": "Số điện thoại phải có đúng 10 chữ số",
        # ^ Key "err_invalid_phone" – thông báo lỗi số điện thoại.

        "close": "Đóng",
        # ^ Key "close" – văn bản trên nút Đóng của dialog lỗi tùy chỉnh. Hiển thị "Đóng".

        # ------------------ Cửa sổ Lịch sử Khám (MedicalHistoryWindow) ------------------
        "history_title": "Lịch sử khám bệnh",
        # ^ Key "history_title" – tiêu đề cửa sổ lịch sử khám (sẽ ghép thêm tên bệnh nhân). Hiển thị "Lịch sử khám bệnh".

        "lbl_visit_date": "Ngày khám (YYYY-MM-DD):",
        # ^ Key "lbl_visit_date" – nhãn cho ô nhập ngày khám. Hiển thị "Ngày khám (YYYY-MM-DD):".

        "lbl_height": "Chiều cao (cm):",
        # ^ Key "lbl_height" – nhãn chiều cao. Hiển thị "Chiều cao (cm):".

        "lbl_weight": "Cân nặng (kg):",
        # ^ Key "lbl_weight" – nhãn cân nặng. Hiển thị "Cân nặng (kg):".

        "lbl_systolic": "HATT (mmHg):",
        # ^ Key "lbl_systolic" – nhãn huyết áp tâm thu (Systolic). Hiển thị "HATT (mmHg):".

        "lbl_diastolic": "HATTr (mmHg):",
        # ^ Key "lbl_diastolic" – nhãn huyết áp tâm trương (Diastolic). Hiển thị "HATTr (mmHg):".

        "lbl_diagnosis": "Chẩn đoán:",
        # ^ Key "lbl_diagnosis" – nhãn chẩn đoán. Hiển thị "Chẩn đoán:".

        "lbl_prescription": "Thuốc kê:",
        # ^ Key "lbl_prescription" – nhãn thuốc kê. Hiển thị "Thuốc kê:".

        "btn_add_visit": "➕ Thêm lần khám",
        # ^ Key "btn_add_visit" – văn bản trên nút thêm lần khám. Hiển thị "➕ Thêm lần khám".

        "btn_ai_advice": "🤖 Trợ lý AI Tư vấn",
        # ^ Key "btn_ai_advice" – văn bản trên nút gọi AI. Hiển thị "🤖 Trợ lý AI Tư vấn".

        "ai_header": "💡 Khuyến nghị từ AI Agent:",
        # ^ Key "ai_header" – tiêu đề khung AI. Hiển thị "💡 Khuyến nghị từ AI Agent:".

        "ai_init_status": "Hệ thống AI sẵn sàng. Nhập Chẩn đoán & Thuốc để nhận tư vấn.",
        # ^ Key "ai_init_status" – trạng thái ban đầu của khung AI. Hiển thị dòng chữ hướng dẫn.

        "btn_delete_visit": "🗑️ Xóa lần khám được chọn",
        # ^ Key "btn_delete_visit" – văn bản trên nút xóa lần khám. Hiển thị "🗑️ Xóa lần khám được chọn".

        # ------------------ Bảng Bệnh nhân (Treeview) ------------------
        "col_id": "Mã BN",
        # ^ Key "col_id" – tiêu đề cột ID bệnh nhân. Hiển thị "Mã BN".

        "col_name": "Họ và Tên",
        # ^ Key "col_name" – tiêu đề cột Họ tên. Hiển thị "Họ và Tên".

        "col_birth": "Năm sinh",
        # ^ Key "col_birth" – tiêu đề cột Năm sinh. Hiển thị "Năm sinh".

        "col_gender": "Giới tính",
        # ^ Key "col_gender" – tiêu đề cột Giới tính. Hiển thị "Giới tính".

        "col_phone": "Số điện thoại",
        # ^ Key "col_phone" – tiêu đề cột Số điện thoại. Hiển thị "Số điện thoại".

        "col_address": "Địa chỉ",
        # ^ Key "col_address" – tiêu đề cột Địa chỉ. Hiển thị "Địa chỉ".

        # ------------------ Bảng Lịch sử Khám (Treeview) ------------------
        "col_date": "Ngày khám",
        # ^ Key "col_date" – tiêu đề cột Ngày khám. Hiển thị "Ngày khám".

        "col_height": "Cao (cm)",
        # ^ Key "col_height" – tiêu đề cột Chiều cao. Hiển thị "Cao (cm)".

        "col_weight": "Nặng (kg)",
        # ^ Key "col_weight" – tiêu đề cột Cân nặng. Hiển thị "Nặng (kg)".

        "col_systolic": "HATT",
        # ^ Key "col_systolic" – tiêu đề cột Huyết áp tâm thu. Hiển thị "HATT".

        "col_diastolic": "HATTr",
        # ^ Key "col_diastolic" – tiêu đề cột Huyết áp tâm trương. Hiển thị "HATTr".

        "col_diagnosis": "Chẩn đoán",
        # ^ Key "col_diagnosis" – tiêu đề cột Chẩn đoán. Hiển thị "Chẩn đoán".

        "col_prescription": "Thuốc kê",
        # ^ Key "col_prescription" – tiêu đề cột Thuốc kê. Hiển thị "Thuốc kê".

        # ------------------ Giao diện chính (MainView) - Menu, nút, tìm kiếm ------------------
        "menu_hoso": "🗂️ Quản Lý Hồ Sơ",
        # ^ Key "menu_hoso" – nhãn menu cha "Quản lý hồ sơ". Hiển thị "🗂️ Quản Lý Hồ Sơ".

        "menu_data": "📊 Dữ Liệu CSV",
        # ^ Key "menu_data" – nhãn menu cha "Dữ liệu CSV". Hiển thị "📊 Dữ Liệu CSV".

        "menu_hethong": "⚙️ Hệ Thống",
        # ^ Key "menu_hethong" – nhãn menu cha "Hệ thống". Hiển thị "⚙️ Hệ Thống".

        "btn_add": "➕ Thêm Bệnh Nhân",
        # ^ Key "btn_add" – văn bản nút Thêm (menu con hồ sơ). Hiển thị "➕ Thêm Bệnh Nhân".

        "btn_edit": "📝 Sửa Thông Tin",
        # ^ Key "btn_edit" – văn bản nút Sửa. Hiển thị "📝 Sửa Thông Tin".

        "btn_history": "📜 Lịch Sử Khám",
        # ^ Key "btn_history" – văn bản nút Lịch sử khám. Hiển thị "📜 Lịch Sử Khám".

        "btn_delete": "🗑️ Xóa Hồ Sơ",
        # ^ Key "btn_delete" – văn bản nút Xóa. Hiển thị "🗑️ Xóa Hồ Sơ".

        "btn_import": "📥 Nhập CSV",
        # ^ Key "btn_import" – văn bản nút Import CSV. Hiển thị "📥 Nhập CSV".

        "btn_export": "📤 Xuất CSV",
        # ^ Key "btn_export" – văn bản nút Export CSV. Hiển thị "📤 Xuất CSV".

        "btn_template": "📋 Tải File Mẫu",
        # ^ Key "btn_template" – văn bản nút xuất mẫu CSV. Hiển thị "📋 Tải File Mẫu".

        "btn_about": "ℹ️ Giới Thiệu",
        # ^ Key "btn_about" – văn bản nút About. Hiển thị "ℹ️ Giới Thiệu".

        "lbl_search_title": "🔍 Bộ lọc tìm kiếm:",
        # ^ Key "lbl_search_title" – tiêu đề bộ lọc tìm kiếm. Hiển thị "🔍 Bộ lọc tìm kiếm:".

        "plh_search": "Nhập tên hoặc số điện thoại để tìm kiếm bệnh nhân...",
        # ^ Key "plh_search" – placeholder ô tìm kiếm. Hiển thị dòng chữ hướng dẫn.

        "btn_search": "Tìm Kiếm",
        # ^ Key "btn_search" – văn bản nút Tìm kiếm. Hiển thị "Tìm Kiếm".

        "btn_refresh": "Làm Mới",
        # ^ Key "btn_refresh" – văn bản nút Làm mới. Hiển thị "Làm Mới".

        "btn_toggle_ime": "⌨️ Bộ gõ Linux",
        # ^ Key "btn_toggle_ime" – văn bản nút bật/tắt IME trên Linux. Hiển thị "⌨️ Bộ gõ Linux".

        "theme_prefix": "Giao diện: ",
        # ^ Key "theme_prefix" – tiền tố hiển thị tên theme. Hiển thị "Giao diện: ".

        # ------------------ Footer thống kê (Stats) ------------------
        "stats_total": "Tổng số bệnh nhân: {}",
        # ^ Key "stats_total" – định dạng hiển thị tổng số bệnh nhân. Dấu {} sẽ được thay bằng số.

        "stats_male": "Nam: {}",
        # ^ Key "stats_male" – định dạng số bệnh nhân nam. {} thay bằng số.

        "stats_female": "Nữ: {}",
        # ^ Key "stats_female" – định dạng số bệnh nhân nữ.

        "stats_avg_age": "Tuổi trung bình: {:.1f}",
        # ^ Key "stats_avg_age" – định dạng tuổi trung bình. {:.1f} hiển thị 1 số thập phân.

        # ------------------ Các thông báo (Messages) ------------------
        "msg_missing_info": "Thiếu thông tin",
        # ^ Key "msg_missing_info" – tiêu đề cảnh báo thiếu thông tin.

        "msg_enter_diagnosis": "Vui lòng nhập 'Chẩn đoán' để AI phân tích.",
        # ^ Key "msg_enter_diagnosis" – thông báo yêu cầu nhập chẩn đoán.

        "msg_sys_error": "Lỗi hệ thống",
        # ^ Key "msg_sys_error" – thông báo lỗi hệ thống chung.

        "msg_no_ai_agent": "Controller chưa cấu hình AI Agent.",
        # ^ Key "msg_no_ai_agent" – thông báo khi AI Agent chưa sẵn sàng.

        "msg_ai_processing": "🤖 AI đang phân tích dữ liệu lâm sàng, vui lòng đợi...",
        # ^ Key "msg_ai_processing" – thông báo trong khi AI đang xử lý.

        "msg_select_visit": "Chọn lần khám",
        # ^ Key "msg_select_visit" – tiêu đề hộp thoại chọn lần khám.

        "msg_warn_select_delete": "Vui lòng chọn một lần khám để xóa",
        # ^ Key "msg_warn_select_delete" – cảnh báo khi chưa chọn lần khám để xóa.

        "msg_confirm": "Xác nhận",
        # ^ Key "msg_confirm" – tiêu đề hộp thoại xác nhận.

        "msg_ask_delete": "Xóa lần khám này?",
        # ^ Key "msg_ask_delete" – câu hỏi xác nhận xóa.

        "msg_no_ai_data": "Lượt khám này không có dữ liệu tư vấn AI cũ."
        # ^ Key "msg_no_ai_data" – thông báo khi không có dữ liệu AI cho lần khám.
    },
    # Dòng trên: đóng ngoặc nhọn của dictionary "vi" và dấu phẩy ngăn cách với phần tử tiếp theo.

    # ------------------------------------------------------------------------
    # 1.2. TIẾNG ANH (en) - Cấu trúc giống hệt tiếng Việt, chỉ khác nội dung
    # ------------------------------------------------------------------------
    "en": {
        # Dòng trên: khóa "en" (mã ngôn ngữ Tiếng Anh), bắt đầu dictionary con.

        # Add/Edit Patient Window
        "title_add": "Add Patient",
        # ^ Key "title_add" – tiêu đề cửa sổ thêm bệnh nhân (tiếng Anh).

        "title_edit": "Edit Patient",
        "lbl_name": "Full Name:",
        "plh_name": "Enter full name",
        "lbl_birth": "Birth Year:",
        "plh_birth": "Ex: 1990",
        "lbl_gender": "Gender:",
        "gender_male": "Male",
        "gender_female": "Female",
        "lbl_phone": "Phone Number:",
        "lbl_address": "Address:",
        "plh_address": "Address",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "err_title": "Error",
        "err_empty_name": "Full name cannot be empty",
        "err_empty_birth": "Please enter birth year",
        "err_invalid_birth": "Birth year must be from 1900 to 2026",
        "err_invalid_phone": "Phone number must be exactly 10 digits",
        "close": "Close",

        # Medical History Window
        "history_title": "Medical History",
        "lbl_visit_date": "Visit Date (YYYY-MM-DD):",
        "lbl_height": "Height (cm):",
        "lbl_weight": "Weight (kg):",
        "lbl_systolic": "SBP (mmHg):",
        "lbl_diastolic": "DBP (mmHg):",
        "lbl_diagnosis": "Diagnosis:",
        "lbl_prescription": "Prescription:",
        "btn_add_visit": "➕ Add Record",
        "btn_ai_advice": "🤖 Ask AI Assistant",
        "ai_header": "💡 AI Agent Recommendations:",
        "ai_init_status": "AI System Ready. Enter Diagnosis & Prescription for guidance.",
        "btn_delete_visit": "🗑️ Delete Selected Record",

        # Patients Table (Treeview)
        "col_id": "ID",
        "col_name": "Full Name",
        "col_birth": "Birth Year",
        "col_gender": "Gender",
        "col_phone": "Phone Number",
        "col_address": "Address",

        # History Table (Treeview)
        "col_date": "Date",
        "col_height": "Height (cm)",
        "col_weight": "Weight (kg)",
        "col_systolic": "SBP",
        "col_diastolic": "DBP",
        "col_diagnosis": "Diagnosis",
        "col_prescription": "Prescription",

        # MainView UI
        "menu_hoso": "🗂️ Records Management",
        "menu_data": "📊 CSV Data",
        "menu_hethong": "⚙️ System Options",
        "btn_add": "➕ Add Patient",
        "btn_edit": "📝 Edit Profile",
        "btn_history": "📜 Medical History",
        "btn_delete": "🗑️ Delete Record",
        "btn_import": "📥 Import CSV",
        "btn_export": "📤 Export CSV",
        "btn_template": "📋 Get Template",
        "btn_about": "ℹ️ About App",
        "lbl_search_title": "🔍 Search Filter:",
        "plh_search": "Type name or phone to filter patients...",
        "btn_search": "Search",
        "btn_refresh": "Refresh",
        "btn_toggle_ime": "⌨️ Linux IME",
        "theme_prefix": "Theme: ",

        # Footer Stats
        "stats_total": "Total Patients: {}",
        "stats_male": "Male: {}",
        "stats_female": "Female: {}",
        "stats_avg_age": "Avg Age: {:.1f}",

        # Messages
        "msg_missing_info": "Missing Information",
        "msg_enter_diagnosis": "Please enter 'Diagnosis' for AI analysis.",
        "msg_sys_error": "System Error",
        "msg_no_ai_agent": "Controller is not configured with AI Agent.",
        "msg_ai_processing": "🤖 AI is analyzing clinical data, please wait...",
        "msg_select_visit": "Select Visit",
        "msg_warn_select_delete": "Please select a medical record to delete",
        "msg_confirm": "Confirmation",
        "msg_ask_delete": "Delete this medical record?",
        "msg_no_ai_data": "This record has no old AI consultation data."
        # ^ Các dòng tiếng Anh tương tự, nội dung là bản dịch.
    }
    # Dòng trên: đóng ngoặc nhọn của dictionary "en".
}
# Dòng trên: đóng ngoặc nhọn của dictionary LANGUAGES.