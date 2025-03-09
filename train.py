import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from scipy.io import arff
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB

# === 1. Load dữ liệu từ file ARFF ===
def load_data(filepath):
    data, meta = arff.loadarff(filepath)
    df = pd.DataFrame(data)
    df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)
    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    return df

data_file = "Training_Dataset_Cleaned.arff"
df = load_data(data_file)

# === 2. Tách tập dữ liệu ===
X = df.drop(columns=["Result"])
y = df["Result"]

# === 3. Chia train / test (70% train, 30% test) ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ============================
#  🔹 Mô hình Cây Quyết Định
# ============================
dt_model = DecisionTreeClassifier(criterion='gini', max_depth=9, random_state=42)
dt_model.fit(X_train, y_train)

# Dự đoán
y_pred_dt = dt_model.predict(X_test)

# Đánh giá
accuracy_dt = accuracy_score(y_test, y_pred_dt)
cm_dt = confusion_matrix(y_test, y_pred_dt)

print(f"🔹 Độ chính xác Decision Tree: {accuracy_dt:.2f}")
print("📌 Ma trận nhầm lẫn (Decision Tree):\n", cm_dt)

# Lưu mô hình
joblib.dump(dt_model, "decision_tree_model.pkl")

# === Vẽ cây quyết định ===
plt.figure(figsize=(35, 15))
plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=["Không lừa đảo", "Lừa đảo"], fontsize=8)
plt.savefig("decision_tree.png", dpi=300)

# ============================
#  🔹 Mô hình KNN
# ============================
k_values = range(1, 30)
accuracies = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k, metric='hamming')
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    accuracies.append(acc)

# Xác định k tối ưu
best_k = k_values[np.argmax(accuracies)]
knn_best = KNeighborsClassifier(n_neighbors=best_k, metric='hamming')
knn_best.fit(X_train, y_train)
y_pred_knn = knn_best.predict(X_test)

# Đánh giá KNN
accuracy_knn = accuracy_score(y_test, y_pred_knn)
cm_knn = confusion_matrix(y_test, y_pred_knn)

print(f"🔹 Độ chính xác KNN (k={best_k}): {accuracy_knn:.2f}")
print("📌 Ma trận nhầm lẫn (KNN):\n", cm_knn)

# Lưu mô hình KNN
joblib.dump(knn_best, "knn_model.pkl")

# === Vẽ biểu đồ độ chính xác theo K ===
plt.figure(figsize=(20, 10))
plt.plot(k_values, accuracies, marker='o', linestyle='dashed', color='b', label="Độ chính xác KNN")
plt.axvline(x=best_k, color='r', linestyle='--', label=f"K tối ưu ({best_k})")
plt.xlabel("Số hàng xóm (k)")
plt.ylabel("Độ chính xác")
plt.title("Chọn k tối ưu cho thuật toán KNN")
plt.legend()
plt.grid(True)
plt.savefig("knn_accuracy.png", dpi=300)

# ============================
#  🔹 Mô hình Naive Bayes
# ============================
nb_model = BernoulliNB()
nb_model.fit(X_train, y_train)
y_pred_nb = nb_model.predict(X_test)

# Đánh giá Naive Bayes
accuracy_nb = accuracy_score(y_test, y_pred_nb)
cm_nb = confusion_matrix(y_test, y_pred_nb)

print(f"🔹 Độ chính xác Naive Bayes: {accuracy_nb:.2f}")
print("📌 Ma trận nhầm lẫn (Naive Bayes):\n", cm_nb)

# Lưu mô hình Naive Bayes
joblib.dump(nb_model, "naive_bayes_model.pkl")

# Vẽ và lưu ma trận nhầm lẫn cho Decision Tree
plt.figure(figsize=(10, 8))
sns.heatmap(cm_dt, annot=True, fmt="d", cmap="Blues", xticklabels=["Không lừa đảo", "Lừa đảo"], 
            yticklabels=["Không lừa đảo", "Lừa đảo"])
plt.title("Ma trận nhầm lẫn - Decision Tree")
plt.xlabel("Giá trị dự đoán")
plt.ylabel("Giá trị thực tế")
plt.savefig("confusion_matrix_decision_tree.png", dpi=300)

# Vẽ và lưu ma trận nhầm lẫn cho KNN
plt.figure(figsize=(10, 8))
sns.heatmap(cm_knn, annot=True, fmt="d", cmap="Greens", xticklabels=["Không lừa đảo", "Lừa đảo"], 
            yticklabels=["Không lừa đảo", "Lừa đảo"])
plt.title(f"Ma trận nhầm lẫn - KNN (k={best_k})")
plt.xlabel("Giá trị dự đoán")
plt.ylabel("Giá trị thực tế")
plt.savefig("confusion_matrix_knn.png", dpi=300)

# Vẽ và lưu ma trận nhầm lẫn cho Naive Bayes
plt.figure(figsize=(10, 8))
sns.heatmap(cm_nb, annot=True, fmt="d", cmap="Oranges", xticklabels=["Không lừa đảo", "Lừa đảo"], 
            yticklabels=["Không lừa đảo", "Lừa đảo"])
plt.title("Ma trận nhầm lẫn - Naive Bayes")
plt.xlabel("Giá trị dự đoán")
plt.ylabel("Giá trị thực tế")
plt.savefig("confusion_matrix_naive_bayes.png", dpi=300)

# Vẽ tất cả 3 ma trận
plt.show()

