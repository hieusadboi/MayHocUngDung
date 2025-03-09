import pandas as pd
from scipy.io import arff

# Đọc file ARFF
data, meta = arff.loadarff("Training_Dataset_Cleaned.arff")

# Chuyển thành DataFrame
df = pd.DataFrame(data)

# Lưu dưới dạng Excel
df = df.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else str(x).replace("b'", "").replace("'", ""))
df.to_excel("KNN.xlsx", index=False)
