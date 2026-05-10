import customtkinter as ctk
from tkinter import ttk

app = ctk.CTk()
app.title("HealthRecord")
app.geometry("800x500")

# Toolbar
toolbar = ctk.CTkFrame(app)
toolbar.pack(fill="x", padx=10, pady=5)
btn_test = ctk.CTkButton(toolbar, text="Test")
btn_test.pack(side="left", padx=5)

# Bảng Treeview
tree = ttk.Treeview(app, columns=("ID","Họ tên","Năm sinh"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Họ tên", text="Họ tên")
tree.heading("Năm sinh", text="Năm sinh")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Thêm dòng mẫu
tree.insert("", "end", values=(1, "Nguyễn Văn A", 1990))
tree.insert("", "end", values=(2, "Trần Thị B", 1995))

app.mainloop()