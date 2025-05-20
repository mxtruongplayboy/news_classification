import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from text_cleaner import TextCleaner
import os

# Define base directory path (parent of the current file's directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_SAVE_DIR = os.path.join(BASE_DIR, 'models')

print(f"Sử dụng MODEL_SAVE_DIR: {MODEL_SAVE_DIR}")
if not os.path.exists(MODEL_SAVE_DIR):
    print(f"LỖI: Thư mục MODEL_SAVE_DIR '{MODEL_SAVE_DIR}' không tồn tại. Vui lòng kiểm tra lại đường dẫn.")
    exit()

TOKENIZER_PATH = os.path.join(MODEL_SAVE_DIR, 'tokenizer.pkl')
LABEL_ENCODER_PATH = os.path.join(MODEL_SAVE_DIR, 'label_encoder.pkl')
MAX_LEN_PATH = os.path.join(MODEL_SAVE_DIR, 'max_len.pkl')
BIGRU_MODEL_PATH = os.path.join(MODEL_SAVE_DIR, 'bigru_model.keras')
BILSTM_MODEL_PATH = os.path.join(MODEL_SAVE_DIR, 'bilstm_model.keras')

# Paths for TextCleaner
STOPWORDS_FILE = os.path.join(BASE_DIR, 'crawl', 'stopwords.txt')
ABBREVIATIONS_FILE = os.path.join(BASE_DIR, 'crawl', 'acronym.txt')
VNCORENLP_MODEL_DIR = os.path.join(BASE_DIR, 'vncorenlp')

# --- 1. Khởi tạo TextCleaner (Tương tự ví dụ của bạn) ---
print("--- Khởi tạo TextCleaner ---")
cleaner_instance = None
try:
    if not os.path.exists(STOPWORDS_FILE): print(f"CẢNH BÁO: File stopwords '{STOPWORDS_FILE}' không tồn tại.")
    if not os.path.exists(ABBREVIATIONS_FILE): print(f"CẢNH BÁO: File viết tắt '{ABBREVIATIONS_FILE}' không tồn tại.")
    if not os.path.exists(VNCORENLP_MODEL_DIR): print(f"CẢNH BÁO: Thư mục VnCoreNLP '{VNCORENLP_MODEL_DIR}' không tồn tại.")

    # Kiểm tra xem instance đã tồn tại chưa (mặc dù trong script độc lập này thì không cần thiết lắm)
    if 'cleaner_instance' not in globals() or cleaner_instance is None:
        cleaner_instance = TextCleaner(STOPWORDS_FILE, ABBREVIATIONS_FILE, VNCORENLP_MODEL_DIR)
        print("Đã tạo instance mới của TextCleaner.")
    else:
        print("Instance của TextCleaner đã tồn tại. Bỏ qua khởi tạo.")
except Exception as e:
    print(f"Lỗi khi khởi tạo TextCleaner: {e}. Không thể làm sạch văn bản.")
    # Để script có thể tiếp tục (nếu muốn test phần tải model), không exit() ở đây
    # nhưng hàm dự đoán sẽ không hoạt động nếu cleaner_instance là None.


# --- 2. Tải các thành phần đã lưu ---
print("\n--- Tải các thành phần đã lưu ---")
tokenizer = None
label_encoder = None
max_len = None
bigru_model = None
bilstm_model = None

try:
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
    print(f"Đã tải tokenizer từ {TOKENIZER_PATH}.")
except Exception as e:
    print(f"Lỗi khi tải tokenizer: {e}.")

try:
    with open(LABEL_ENCODER_PATH, 'rb') as handle:
        label_encoder = pickle.load(handle)
    print(f"Đã tải label encoder từ {LABEL_ENCODER_PATH}.")
except Exception as e:
    print(f"Lỗi khi tải label encoder: {e}.")

try:
    with open(MAX_LEN_PATH, 'rb') as handle:
        max_len = pickle.load(handle)
    print(f"Đã tải max_len: {max_len} từ {MAX_LEN_PATH}")
except Exception as e:
    print(f"Lỗi khi tải max_len: {e}.")

try:
    bigru_model = load_model(BIGRU_MODEL_PATH)
    print(f"Đã tải mô hình BiGRU từ {BIGRU_MODEL_PATH}.")
except Exception as e:
    print(f"Lỗi khi tải mô hình BiGRU: {e}.")

try:
    bilstm_model = load_model(BILSTM_MODEL_PATH)
    print(f"Đã tải mô hình BiLSTM từ {BILSTM_MODEL_PATH}.")
except Exception as e:
    print(f"Lỗi khi tải mô hình BiLSTM: {e}.")

# --- 3. Dữ liệu mẫu và làm sạch (Tương tự ví dụ của bạn) ---
print("\n--- Chuẩn bị dữ liệu mẫu ---")
sample_title = "Pakistan công bố thương vong trong giao tranh với Ấn Độ"
sample_description = "Quân đội Pakistan công bố báo cáo thương vong đầu tiên trong cuộc xung đột với Ấn Độ tuần qua, cho hay 51 quân nhân và dân thường đã thiệt mạng."
sample_content = "Cơ quan Truyền thông Liên Quân chủng quân đội Pakistan (ISPR) ngày 13/5 công bố báo cáo về cuộc xung đột 19 ngày với Ấn Độ, kéo dài từ 22/4 đến 10/5, và đặt tên cho chiến dịch này là Marka-e-Haq (Trận chiến vì sự thật). ISPR thông báo 11 binh sĩ thuộc các đơn vị lục quân, không quân đã thiệt mạng trong các cuộc giao tranh, trong đó có chỉ huy phi đội Usman Yousuf. 78 quân nhân bị thương trong các đòn tập kích của lực lượng Ấn Độ. Pakistan cũng thống kê thương vong dân thường gồm 40 người thiệt mạng, trong đó có 7 phụ nữ và 15 trẻ em, cùng với 121 người bị thương, chủ yếu trong chiến dịch Sindoor của Ấn Độ vào rạng sáng 7/5. ISPR không thống kê bất cứ thiệt hại nào về khí tài trong báo cáo. Trước đó, quân đội Pakistan cho hay họ đã bắn hạ 5 tiêm kích và một máy bay không người lái của Ấn Độ. Quân đội Ấn Độ cũng thông báo đã vô hiệu hóa một số chiến đấu cơ Pakistan, nhưng không nêu chi tiết."

cleaned_sample_text = ""
if cleaner_instance:
    try:
        title_c, desc_c, content_c = cleaner_instance.process_text(sample_title, sample_description, sample_content)
        cleaned_sample_text = title_c + " " + desc_c + " " + content_c
        print("Dữ liệu mẫu đã được làm sạch.")
        print(f"Văn bản đã làm sạch (200 ký tự đầu): \"{cleaned_sample_text[:200]}...\"")
    except Exception as e:
        print(f"Lỗi khi làm sạch dữ liệu mẫu: {e}")
else:
    print("TextCleaner không khả dụng, không thể làm sạch dữ liệu mẫu.")

# --- 4. Hàm dự đoán (Tương tự ví dụ của bạn, nhưng cho RNN) ---
def predict_new_text_rnn(cleaned_text_input, model_to_use, model_name_str,
                         tokenizer_loaded, label_encoder_loaded, max_len_loaded):
    # Kiểm tra các thành phần cần thiết
    if model_to_use is None:
        print(f"Mô hình {model_name_str} chưa được tải hoặc có lỗi. Bỏ qua dự đoán.")
        return
    if tokenizer_loaded is None:
        print("Tokenizer chưa được tải. Bỏ qua dự đoán.")
        return
    if label_encoder_loaded is None:
        print("Label encoder chưa được tải. Bỏ qua dự đoán.")
        return
    if max_len_loaded is None:
        print("Max_len chưa được tải. Bỏ qua dự đoán.")
        return
    if not cleaned_text_input or not cleaned_text_input.strip():
        print("Văn bản đầu vào (đã làm sạch) rỗng. Không thể dự đoán.")
        return

    print(f"\n--- Dự đoán với {model_name_str} cho văn bản mới ---")
    print(f"Văn bản đầu vào (200 ký tự đầu): \"{cleaned_text_input[:200]}...\"")

    # Tokenize and Pad
    try:
        sequence = tokenizer_loaded.texts_to_sequences([cleaned_text_input])
        padded_sequence = pad_sequences(sequence, maxlen=max_len_loaded, padding='post', truncating='post')
    except Exception as e:
        print(f"Lỗi trong quá trình tokenize hoặc padding: {e}")
        return

    # Predict
    try:
        prediction_proba = model_to_use.predict(padded_sequence)
        predicted_class_index = np.argmax(prediction_proba, axis=1)[0]
        predicted_class_label = label_encoder_loaded.inverse_transform([predicted_class_index])[0]
    except Exception as e:
        print(f"Lỗi trong quá trình dự đoán của mô hình: {e}")
        return

    print(f"Chủ đề dự đoán: {predicted_class_label}")
    print("Xác suất dự đoán cho từng chủ đề:")
    if hasattr(label_encoder_loaded, 'classes_'):
        for i, topic_class_name in enumerate(label_encoder_loaded.classes_):
            print(f"  - {topic_class_name}: {prediction_proba[0][i]:.4f}")
    else:
        print("Không thể lấy tên các lớp từ label_encoder.")

# --- 5. Thực hiện dự đoán (Tương tự ví dụ của bạn) ---
print("\n--- Thực hiện dự đoán cho dữ liệu mẫu ---")
if cleaned_sample_text: # Chỉ dự đoán nếu văn bản đã được làm sạch
    if bigru_model:
        predict_new_text_rnn(cleaned_sample_text, bigru_model, "BiGRU",
                             tokenizer, label_encoder, max_len)
    else:
        print("Mô hình BiGRU không khả dụng để dự đoán.")

    if bilstm_model:
        predict_new_text_rnn(cleaned_sample_text, bilstm_model, "BiLSTM",
                             tokenizer, label_encoder, max_len)
    else:
        print("Mô hình BiLSTM không khả dụng để dự đoán.")

    if not bigru_model and not bilstm_model:
        print("Không có mô hình RNN nào được tải thành công để thực hiện dự đoán.")
elif cleaner_instance is None:
    print("Không thể dự đoán vì TextCleaner không được khởi tạo.")
else:
    print("Không thể dự đoán vì dữ liệu mẫu chưa được làm sạch (có thể do lỗi ở TextCleaner).")


