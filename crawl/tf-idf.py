import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Giả sử bạn đã có DataFrame với cột 'cleaned_text' chứa dữ liệu văn bản đã được xử lý và 'category' là nhãn phân loại
# df = pd.read_csv("duong_dan_toi_du_lieu.csv")  # Đọc dữ liệu nếu cần

# Ví dụ DataFrame
# df = pd.DataFrame({
#     'cleaned_text': ["Tin tức về chính trị", "Bóng đá thế giới", "Kinh tế trong nước", "Thể thao Việt Nam"],
#     'category': ['Chính trị', 'Thể thao', 'Kinh tế', 'Thể thao']
# })

df = pd.read_csv(r'E:\LEARN_5\XuLyNgonNguTuNhien\vncorenlp\cleaned_news_data.csv')

# Tạo vectorizer TF-IDF
vectorizer = TfidfVectorizer()

# Chuyển đổi văn bản thành ma trận TF-IDF
X = vectorizer.fit_transform(df['text'])

# Nhãn phân loại
y = df['Topic']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tạo mô hình phân loại Naive Bayes
model = MultinomialNB()

# Huấn luyện mô hình
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Hiển thị các từ quan trọng nhất trong mỗi chủ đề
feature_names = vectorizer.get_feature_names_out()
for i, category in enumerate(model.classes_):
    top_words_idx = model.coef_[i].argsort()[-10:][::-1]  # 10 từ quan trọng nhất
    top_words = [feature_names[idx] for idx in top_words_idx]
    print(f"\nTop 10 từ quan trọng nhất trong chủ đề {category}:")
    print(top_words)
