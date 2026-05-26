# ============================================================================
# FILE: services/ai_agent.py
# MỤC ĐÍCH: Kết nối đến Google Gemini API, phân tích dựa trên chẩn đoán và đơn thuốc.
#           Cung cấp phương thức analyze_medical_visit để gửi dữ liệu và nhận phản hồi.
# ============================================================================

# ============================================================================
# 1. IMPORT THƯ VIỆN google.genai
# ============================================================================
from google import genai
# ^ Lệnh import thư viện genai từ package google (lệnh thư viện)
#   Thư viện này cung cấp các lớp và phương thức để tương tác với Gemini API.

# ============================================================================
# 2. ĐỊNH NGHĨA LỚP ClinicAIAgent
# ============================================================================
class ClinicAIAgent:
    # Dòng trên: Khai báo class ClinicAIAgent (do người dùng đặt tên)
    """
    Lớp đại diện cho một AI Agent chuyên khoa lâm sàng.
    Kết nối đến Google Gemini API và gửi yêu cầu phân tích dữ liệu khám bệnh.
    """
    # ^ Docstring (chú thích nhiều dòng) – mô tả class

    # ------------------------------------------------------------------------
    # 2.1. HÀM KHỞI TẠO (__init__) - THIẾT LẬP KẾT NỐI API
    # ------------------------------------------------------------------------
    def __init__(self):
        # Dòng trên: định nghĩa hàm khởi tạo (do người dùng định nghĩa)
        """Khởi tạo Client bằng cách dán trực tiếp API Key"""
        # ^ Docstring của phương thức __init__

        # 🔑 Biến lưu trữ API Key (chuỗi bí mật cung cấp bởi Google AI Studio)
        # Lưu ý bảo mật: Đây là key mẫu, khi triển khai thực tế cần thay bằng key thật.
        # Biến self.MY_API_KEY – do người dùng đặt.
        self.MY_API_KEY = "AIzaSyBTFnFCM_g3Sa1aiEut6sZ2-F2ePOK3PI4"

        # Khởi tạo client (đối tượng kết nối) của Google Gemini
        # genai.Client là lớp thư viện, yêu cầu tham số api_key (lệnh thư viện)
        self.client = genai.Client(api_key=self.MY_API_KEY)

        # Tên mô hình AI sẽ sử dụng ("gemini-2.5-flash")
        # Biến self.model_name – do người dùng đặt (chọn mô hình phù hợp)
        self.model_name = "gemini-2.5-flash"

    # ------------------------------------------------------------------------
    # 2.2. PHƯƠNG THỨC analyze_medical_visit - GỬI YÊU CẦU ĐẾN AI
    # ------------------------------------------------------------------------
    def analyze_medical_visit(self, diagnosis, prescription):
        # Dòng trên: định nghĩa phương thức analyze_medical_visit (do người dùng định nghĩa)
        # Tham số: diagnosis (str), prescription (str) – do người dùng truyền vào
        """Hàm gửi dữ liệu lâm sàng lên AI và nhận phân tích lời khuyên trực tuyến"""
        # ^ Docstring mô tả phương thức

        # ---- Bước 1: Kiểm tra API Key có hợp lệ không ----
        # Nếu API Key bị xóa hoặc không bắt đầu bằng "AIzaSy" (định dạng key của Google)
        if not self.MY_API_KEY or self.MY_API_KEY.startswith("AIzaSy") is False:
            # Trả về thông báo lỗi (string)
            return "❌ Thất bại: API Key trong mã nguồn không hợp lệ hoặc chưa được điền chính xác."

        # ---- Bước 2: Xây dựng prompt (câu lệnh cho AI) ----
        # prompt là một chuỗi văn bản mô tả nhiệm vụ của AI (do người dùng định nghĩa)
        prompt = f"""
        Bạn là một trợ lý AI chuyên khoa lâm sàng cao cấp. Hãy phân tích thông tin khám bệnh sau:
        - Chẩn đoán của bác sĩ: {diagnosis}
        - Đơn thuốc được kê: {prescription}
        
        Yêu cầu trả về kết quả bằng tiếng Việt, trình bày ngắn gọn, khoa học, dễ hiểu bao gồm các mục:
        1. 📑 Đánh giá sơ bộ sự phù hợp giữa thuốc và chẩn đoán.
        2. ⚠️ Cảnh báo tương tác thuốc nguy hiểm hoặc tác dụng phụ cần lưu ý (nếu có).
        3. 🥦 Khuyên bệnh nhân chế độ dinh dưỡng, sinh hoạt và nghỉ ngơi phù hợp với bệnh lý này.
        """
        # ^ prompt: biến do người dùng đặt, nội dung sẽ được gửi lên API

        # ---- Bước 3: Gửi yêu cầu đến Gemini API và xử lý phản hồi ----
        try:
            # Sử dụng phương thức generate_content của client (lệnh thư viện)
            # Cú pháp mới chuẩn: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name,      # Tên mô hình (do người dùng chọn)
                contents=prompt,            # Nội dung prompt (do người dùng tạo)
            )
            # Trả về chuỗi văn bản kết quả từ Google Server
            return response.text

        except Exception as e:
            # Bắt lỗi mạng, API key sai, hết hạn, hoặc lỗi từ phía Google
            # Trả về thông báo lỗi chi tiết (string)
            return f"❌ Lỗi kết nối gọi AI trực tuyến: {str(e)}\n\nVui lòng kiểm tra lại đường truyền Internet hoặc tính hợp lệ của API Key."