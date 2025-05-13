import pandas as pd
import re
import py_vncorenlp

# Bước 1: Đọc dữ liệu từ file CSV
df = pd.read_csv('E:\\LEARN_5\\XuLyNgonNguTuNhien\\articles.csv')

# Bước 2: Giữ lại các cột cần thiết
df = df[['Title', 'Description', 'Content', 'Topic']]

# Bước 3: Loại bỏ giá trị thiếu
df = df.dropna(subset=['Title', 'Description', 'Content', 'Topic'])

# Bước 4: Chuyển văn bản thành chữ thường
df['Title'] = df['Title'].str.lower()
df['Description'] = df['Description'].str.lower()
df['Content'] = df['Content'].str.lower()

# Bước 5: Đọc stopwords từ file
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()
    return stopwords

stopwords = load_stopwords('E:\\LEARN_5\\XuLyNgonNguTuNhien\\project\\crawl\\stopwords.txt')

# Bước 6: Loại bỏ từ dừng (stopwords)
def remove_stopwords(text, stopwords):
    return ' '.join([word for word in text.split() if word not in stopwords])

df['Title'] = df['Title'].apply(lambda x: remove_stopwords(x, stopwords))
df['Description'] = df['Description'].apply(lambda x: remove_stopwords(x, stopwords))
df['Content'] = df['Content'].apply(lambda x: remove_stopwords(x, stopwords))

# Bước 7: Loại bỏ dấu câu và ký tự đặc biệt
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Loại bỏ dấu câu và ký tự đặc biệt
    return text

df['Title'] = df['Title'].apply(clean_text)
df['Description'] = df['Description'].apply(clean_text)
df['Content'] = df['Content'].apply(clean_text)

# Bước 8: Tokenization (tách từ bằng py_vncorenlp)
# Tải mô hình VnCoreNLP và load nó
# Đảm bảo bạn đã tải mô hình trước khi sử dụng
model = py_vncorenlp.VnCoreNLP(save_dir='E:/LEARN_5/XuLyNgonNguTuNhien/vncorenlp')

def tokenize_text(text):
    # Tokenize using VnCoreNLP
    return model.annotate_text(text)

# Áp dụng tokenization cho các cột văn bản
df['Title_tokens'] = df['Title'].apply(tokenize_text)
df['Description_tokens'] = df['Description'].apply(tokenize_text)
df['Content_tokens'] = df['Content'].apply(tokenize_text)

# Bước 9: Kết hợp các cột văn bản thành một cột duy nhất
df['text'] = df['Title'] + " " + df['Description'] + " " + df['Content']

# Bước 10: Lưu lại dữ liệu đã xử lý vào file CSV
df.to_csv('cleaned_news_data.csv', index=False)
