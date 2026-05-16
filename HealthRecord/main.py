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

import os
template_path = os.path.join("assets", "patient_template.csv")
if not os.path.exists(template_path):
    os.makedirs("assets", exist_ok=True)
    with open(template_path, "w", encoding="utf-8") as f:
        f.write("name,birth_year,gender,phone,address\n")
        f.write("Nguyễn Văn A,1990,Nam,0912345678,Hà Nội\n")
        f.write("Trần Thị B,1995,Nữ,0987654321,TP. Hồ Chí Minh\n")
        f.write("Lê Văn C,2000,Nam,0977123456,Đà Nẵng\n")
    print("Đã tạo file mẫu tại assets/patient_template.csv")

from views.main_view import MainView                  # Import lớp MainView
from controllers.patient_controller import PatientController   # Import controller
