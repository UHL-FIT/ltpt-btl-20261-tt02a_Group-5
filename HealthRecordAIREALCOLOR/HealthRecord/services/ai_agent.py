# services/ai_agent.py
# NÂNG CẤP: Sử dụng thư viện google-genai thế hệ mới của Google (Dán trực tiếp API Key)

from google import genai

class ClinicAIAgent:
    def __init__(self):
        """Khởi tạo Client bằng cách dán trực tiếp API Key"""
        # 🔑 ĐÃ SỬA: Điền trực tiếp chuỗi mã Key của bạn vào tham số api_key ở đây
        self.MY_API_KEY = "dán key ở dây"
        
        # Khởi tạo kết nối với Google bằng Key vừa khai báo
        self.client = genai.Client(api_key=self.MY_API_KEY)
        
        # Sử dụng dòng mô hình chuẩn thế hệ mới để đạt tốc độ phân tích tối ưu nhất
        self.model_name = "gemini-2.5-flash"

    def analyze_medical_visit(self, diagnosis, prescription, language="vi"):
        """Hàm gửi dữ liệu lâm sàng lên AI và nhận phân tích lời khuyên trực tuyến (Đã sửa lỗi nhận tham số language)"""
        
        # Phòng ngừa trường hợp chuỗi Key bị xóa nhầm hoặc để trống
        # ✅ ĐÃ SỬA: Chỉ kiểm tra xem key có bị bỏ trống hay không, không bắt bẻ tiền tố AIzaSy nữa
        if not self.MY_API_KEY or self.MY_API_KEY.strip() == "":
            return "❌ Thất bại: API Key trống. Vui lòng điền API Key vào mã nguồn."

        # Tự động thay đổi chỉ thị ngôn ngữ và tiêu đề các mục dựa trên tham số hệ thống truyền sang
        if language == "vi":
            lang_instruction = "Yêu cầu trả về kết quả bằng tiếng Việt, trình bày ngắn gọn, khoa học, dễ hiểu bao gồm các mục:"
            item_1 = "1. 📑 Đánh giá sơ bộ sự phù hợp giữa thuốc và chẩn đoán."
            item_2 = "2. ⚠️ Cảnh báo tương tác thuốc nguy hiểm hoặc tác dụng phụ cần lưu ý (nếu có)."
            item_3 = "3. 🥦 Khuyên bệnh nhân chế độ dinh dưỡng, sinh hoạt và nghỉ ngơi phù hợp với bệnh lý này."
        else:
            lang_instruction = "Please provide the response entirely in English, clear, structured, and easy to understand with the following sections:"
            item_1 = "1. 📑 Preliminary assessment of the suitability between the prescription and diagnosis."
            item_2 = "2. ⚠️ Warnings about potentially dangerous drug interactions or notable side effects (if any)."
            item_3 = "3. 🥦 Dietary, lifestyle, and rest recommendations tailored to this medical condition."

        # Xây dựng prompt yêu cầu AI đóng vai bác sĩ phân tích đơn thuốc độc quyền
        prompt = f"""
        Bạn là một trợ lý AI chuyên khoa lâm sàng cao cấp. Hãy phân tích thông tin khám bệnh sau:
        - Chẩn đoán của bác sĩ: {diagnosis}
        - Đơn thuốc được kê: {prescription}
        
        {lang_instruction}
        {item_1}
        {item_2}
        {item_3}
        """
        
        try:
            # CÚ PHÁP MỚI CHUẨN: Gọi hàm sinh nội dung qua client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            # Trả về chuỗi văn bản kết quả tư vấn từ Google Server
            return response.text
            
        except Exception as e:
            # Bắt lỗi mất mạng hoặc API Key bị Google khóa/hết hạn tự động
            return f"❌ Lỗi kết nối gọi AI trực tuyến: {str(e)}\n\nVui lòng kiểm tra lại đường truyền Internet hoặc tính hợp lệ của API Key."