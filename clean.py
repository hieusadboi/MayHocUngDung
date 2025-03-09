from scipy.io import arff
import pandas as pd

def remove_duplicates_arff(input_file, output_file):
    # Đọc file ARFF
    data, meta = arff.loadarff(input_file)
    
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(data)
    df = df.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else str(x).replace("b'", "").replace("'", ""))
    # Loại bỏ các dòng trùng lặp
    df_cleaned = df.drop_duplicates()
    
    # Lưu lại dưới dạng ARFF
    with open(output_file, "w", encoding="utf-8") as f:
        # Ghi phần header của ARFF
        f.write(f"@RELATION {meta.name}\n\n")
        for attribute in meta.names():
            f.write(f"@ATTRIBUTE {attribute} {meta[attribute][0]}\n")
        f.write("\n@DATA\n")
        
        # Ghi dữ liệu
        for row in df_cleaned.itertuples(index=False):
            f.write(",".join(map(str, row)) + "\n")

# Sử dụng hàm
input_path = "Training Dataset.arff"  # Thay bằng đường dẫn file của bạn
output_path = "Training_Dataset_Cleaned.arff"
remove_duplicates_arff(input_path, output_path)

print(f"File đã xử lý được lưu tại: {output_path}")
