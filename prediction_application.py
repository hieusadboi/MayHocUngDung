import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from PIL import Image, ImageTk
import joblib
import os

# === Hàm dự đoán với cả 3 mô hình ===
def predict_phishing():
    try:
        # Lấy giá trị từ các combobox
        features = [int(combobox.get().split("(")[1].strip(")").strip()) for combobox in comboboxes]

        # Load 3 mô hình đã lưu
        dt_model = joblib.load("decision_tree_model.pkl")
        knn_model = joblib.load("knn_model.pkl")
        nb_model = joblib.load("naive_bayes_model.pkl")

        # Dự đoán với từng mô hình
        prediction_dt = dt_model.predict([features])[0]
        prediction_knn = knn_model.predict([features])[0]
        prediction_nb = nb_model.predict([features])[0]

        # Tạo thông báo kết quả
        result_message = "🔍 Kết quả dự đoán:\n\n"
        result_message += f"📌 KNN:{'KHÔNG LỪA ĐẢO ✅' if prediction_knn == 1 else 'LỪA ĐẢO ⚠️'}\n\n"
        result_message += f"🌳 Cây quyết định: {'KHÔNG LỪA ĐẢO ✅' if prediction_dt == 1 else 'LỪA ĐẢO ⚠️'}\n\n"
        result_message += f"🧠 Naive Bayes: {'KHÔNG LỪA ĐẢO ✅' if prediction_nb == 1 else 'LỪA ĐẢO ⚠️'}"

        # Hiển thị kết quả
        messagebox.showinfo("Kết quả dự đoán", result_message)

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# === Hàm hiển thị ma trận nhầm lẫn ===
def show_confusion_matrix(model_name):
    try:
        filename = f"confusion_matrix_{model_name}.png"
        if not os.path.exists(filename):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {filename}!")
            return

        new_window = Toplevel(root)
        new_window.title(f"Ma trận nhầm lẫn ({model_name.upper()})")

        img = Image.open(filename)
        img = img.resize((1400, 933), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        panel = tk.Label(new_window, image=img)
        panel.image = img
        panel.pack()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở ảnh: {e}")

# === Giao diện Tkinter ===
root = tk.Tk()
root.title("Dự đoán trang web lừa đảo")

# Danh sách các câu hỏi và giá trị
features_list = [
    ("URL chứa địa chỉ IP?", ["Không (1)", "Có (-1)"]),
    ("Độ dài URL?", ["Ngắn (1)", "Trung bình (0)", "Dài (-1)"]),
    ("Dùng dịch vụ rút gọn URL?", ["Không (1)", "Có (-1)"]),
    ("URL có ký tự @?", ["Không (1)", "Có (-1)"]),
    ("Có // bất thường?", ["Không (1)", "Có (-1)"]),
    ("Tên miền có dấu -?", ["Không (1)", "Có (-1)"]),
    ("Số subdomain?", ["Ít (1)", "Trung bình (0)", "Nhiều (-1)"]),
    ("Trạng thái SSL?", ["Hợp lệ (1)", "Không rõ (0)", "Không hợp lệ (-1)"]),
    ("Thời gian đăng ký?", ["Dài (1)", "Ngắn (-1)"]),
    ("Nguồn favicon?", ["Cùng miền (1)", "Khác (-1)"]),
    ("Cổng kết nối?", ["Chuẩn (1)", "Bất thường (-1)"]),
    ("Tên miền có 'https'?", ["Không (1)", "Có (-1)"]),
    ("Nguồn nội dung?", ["Cùng miền (1)", "Khác (-1)"]),
    ("Các liên kết trong trang trỏ đến?", ["Cùng trang (1)", "Một số khác (0)", "Nhiều trang khác (-1)"]),
    ("Thẻ script/link?", ["Cùng trang (1)", "Một số khác (0)", "Nhiều khác (-1)"]),
    ("Xử lý form?", ["Cùng miền (1)", "Không rõ (0)", "Khác (-1)"]),
    ("Gửi thẳng email?", ["Không (1)", "Có (-1)"]),
    ("URL khớp tên miền?", ["Có (1)", "Không (-1)"]),
    ("Số chuyển hướng?", ["Nhiều (1)", "Ít (0)"]),
    ("Thay đổi khi hover?", ["Không (1)", "Có (-1)"]),
    ("Cho phép chuột phải?", ["Có (1)", "Không (-1)"]),
    ("Cửa sổ popup?", ["Không (1)", "Có (-1)"]),
    ("Dùng iframe ẩn?", ["Không (1)", "Có (-1)"]),
    ("Tuổi tên miền?", ["Cũ (1)", "Mới (-1)"]),
    ("DNS hợp lệ?", ["Có (1)", "Không (-1)"]),
    ("Lưu lượng truy cập?", ["Cao (1)", "Trung bình (0)", "Thấp (-1)"]),
    ("PageRank?", ["Cao (1)", "Thấp (-1)"]),
    ("Google Index?", ["Có (1)", "Không (-1)"]),
    ("Các trang web khác liên kết trỏ đến trang này?", ["Nhiều (1)", "Một số (0)", "Ít (-1)"]),
    ("Trong danh sách phishing?", ["Không (1)", "Có (-1)"])
]

comboboxes = []

# Tạo frame chứa nội dung chính với thanh cuộn
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Sắp xếp các câu hỏi thành 2 cột
for i in range(0, len(features_list), 2):
    row = i // 2
    
    # Cột trái
    question_left, options_left = features_list[i]
    lbl_left = ttk.Label(scrollable_frame, text=question_left)
    lbl_left.grid(row=row, column=0, padx=20, pady=5, sticky="w")
    
    combo_left = ttk.Combobox(scrollable_frame, values=options_left, state="readonly", width=25)
    combo_left.grid(row=row, column=1, padx=20, pady=5, sticky="w")
    comboboxes.append(combo_left)
    
    # Cột phải (nếu có)
    if i + 1 < len(features_list):
        question_right, options_right = features_list[i + 1]
        lbl_right = ttk.Label(scrollable_frame, text=question_right)
        lbl_right.grid(row=row, column=3, padx=20, pady=5, sticky="w")
        
        combo_right = ttk.Combobox(scrollable_frame, values=options_right, state="readonly", width=25)
        combo_right.grid(row=row, column=4, padx=20, pady=5, sticky="w")
        comboboxes.append(combo_right)

# Thêm khoảng trống giữa 2 cột
scrollable_frame.grid_columnconfigure(2, minsize=50) 

# Đặt canvas và scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# === Phần nút chức năng ===
button_frame = ttk.Frame(root)

# Tạo các nút
predict_btn = ttk.Button(button_frame, text="🚀 Dự đoán", command=predict_phishing)
cm_dt_btn = ttk.Button(button_frame, text="📊 Ma trận nhầm lẫn cây quyết định", 
                      command=lambda: show_confusion_matrix("decision_tree"))
cm_knn_btn = ttk.Button(button_frame, text="📊 Ma trận nhầm lẫn knn", 
                       command=lambda: show_confusion_matrix("knn"))
cm_nb_btn = ttk.Button(button_frame, text="📊 Ma trận nhầm lẫn naive bayes", 
                      command=lambda: show_confusion_matrix("naive_bayes"))

# Sắp xếp layout sử dụng grid
predict_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
cm_dt_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
cm_knn_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
cm_nb_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Đảm bảo các cột có cùng chiều rộng
button_frame.grid_columnconfigure(0, weight=1)

# Đặt button_frame vào cửa sổ chính
button_frame.pack(fill="x", pady=20)

root.mainloop()
