# main.py
# Điểm khởi đầu của ứng dụng: tạo giao diện, tạo controller và chạy.

from views.main_view import MainView                  # Import lớp MainView
from controllers.patient_controller import PatientController   # Import controller

if __name__ == "__main__":
    # Bước 1: Tạo cửa sổ chính (view)
    app = MainView()
    
    # Bước 2: Tạo controller, truyền view vào. Controller sẽ tự động gắn và tải dữ liệu.
    controller = PatientController(app)
    
    # Bước 3: Chạy vòng lặp chính của ứng dụng.
    app.mainloop()# main.py
# Điểm khởi đầu của ứng dụng: tạo giao diện, tạo controller và chạy.


