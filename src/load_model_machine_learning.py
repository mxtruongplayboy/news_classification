import joblib 
import os     
from text_cleaner import TextCleaner


# Đường dẫn đến các file stopwords và abbreviations
stopwords_file = '../crawl/stopwords.txt'
abbreviations_file = '../crawl/acronym.txt'
vncorenlp_model_dir = '../vncorenlp'

# Tạo instance của TextCleaner
if 'cleaner' not in globals():
	cleaner = TextCleaner(stopwords_file, abbreviations_file, vncorenlp_model_dir)
else:
	print("Instance of TextCleaner already exists. Skipping initialization.")

# Định nghĩa đường dẫn thư mục lưu mô hình
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    print(f"Đã tạo thư mục: {MODEL_DIR}")
else:
    print(f"Đang sử dụng thư mục models tại: {MODEL_DIR}")

# Đường dẫn đến các file mô hình
tfidf_vectorizer_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.joblib')
nb_model_path = os.path.join(MODEL_DIR, 'naive_bayes_model.joblib')
lr_model_path = os.path.join(MODEL_DIR, 'logistic_regression_model.joblib')


# --- Phần đọc mô hình ---
print("\n--- Đọc mô hình từ file ---")
# Đọc TF-IDF Vectorizer
try:
    if os.path.exists(tfidf_vectorizer_path):
        loaded_tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
        print(f"Đã đọc TF-IDF Vectorizer từ: {tfidf_vectorizer_path}")
    else:
        print(f"Không tìm thấy file TF-IDF Vectorizer tại: {tfidf_vectorizer_path}")
except Exception as e:
    print(f"Lỗi khi đọc TF-IDF Vectorizer: {e}")


# Đọc mô hình Naive Bayes
try:
    if os.path.exists(nb_model_path):
        loaded_nb_model = joblib.load(nb_model_path)
        print(f"Đã đọc mô hình Naive Bayes từ: {nb_model_path}")
    else:
        print(f"Không tìm thấy file mô hình Naive Bayes tại: {nb_model_path}")
except Exception as e:
    print(f"Lỗi khi đọc mô hình Naive Bayes: {e}")

# Đọc mô hình Logistic Regression
try:
    if os.path.exists(lr_model_path):
        loaded_lr_model = joblib.load(lr_model_path)
        print(f"Đã đọc mô hình Logistic Regression từ: {lr_model_path}")
    else:
        print(f"Không tìm thấy file mô hình Logistic Regression tại: {lr_model_path}")
except Exception as e:
    print(f"Lỗi khi đọc mô hình Logistic Regression: {e}")

print("\n--- Quá trình đọc mô hình hoàn tất! ---")


# Dữ liệu mẫu
title = "Pakistan công bố thương vong trong giao tranh với Ấn Độ"
description = "Quân đội Pakistan công bố báo cáo thương vong đầu tiên trong cuộc xung đột với Ấn Độ tuần qua, cho hay 51 quân nhân và dân thường đã thiệt mạng."
content = "Cơ quan Truyền thông Liên Quân chủng quân đội Pakistan (ISPR) ngày 13/5 công bố báo cáo về cuộc xung đột 19 ngày với Ấn Độ, kéo dài từ 22/4 đến 10/5, và đặt tên cho chiến dịch này là Marka-e-Haq (Trận chiến vì sự thật). ISPR thông báo 11 binh sĩ thuộc các đơn vị lục quân, không quân đã thiệt mạng trong các cuộc giao tranh, trong đó có chỉ huy phi đội Usman Yousuf. 78 quân nhân bị thương trong các đòn tập kích của lực lượng Ấn Độ. Pakistan cũng thống kê thương vong dân thường gồm 40 người thiệt mạng, trong đó có 7 phụ nữ và 15 trẻ em, cùng với 121 người bị thương, chủ yếu trong chiến dịch Sindoor của Ấn Độ vào rạng sáng 7/5. ISPR không thống kê bất cứ thiệt hại nào về khí tài trong báo cáo. Trước đó, quân đội Pakistan cho hay họ đã bắn hạ 5 tiêm kích và một máy bay không người lái của Ấn Độ. Quân đội Ấn Độ cũng thông báo đã vô hiệu hóa một số chiến đấu cơ Pakistan, nhưng không nêu chi tiết."

title_cleaned, description_cleaned, content_cleaned = cleaner.process_text(title, description, content)

text = title_cleaned + " " + description_cleaned + " " + content_cleaned
print("Text after cleaning: ", text)

def predict_new_text(text_input, vectorizer, model, model_name):
    print(f"\n--- Dự đoán với {model_name} cho văn bản mới ---")
    print(f"Văn bản: \"{text_input}\"")
    text_tfidf = vectorizer.transform([text_input])
    prediction = model.predict(text_tfidf)

    if hasattr(model, "predict_proba") and hasattr(model, "classes_"):
        prediction_proba = model.predict_proba(text_tfidf)
        print(f"Chủ đề dự đoán: {prediction[0]}")
        print("Xác suất dự đoán cho từng chủ đề:")
        for i, topic_class in enumerate(model.classes_):
            print(f"  - {topic_class}: {prediction_proba[0][i]:.4f}")
    else:
        print(f"Chủ đề dự đoán: {prediction[0]}")


predict_new_text(text, loaded_tfidf_vectorizer, loaded_nb_model, "Naive Bayes")
predict_new_text(text, loaded_tfidf_vectorizer, loaded_lr_model, "Logistic Regression")