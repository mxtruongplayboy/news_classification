# Ứng Dụng Phân Loại Văn Bản

Ứng dụng web được xây dựng bằng Flask để phân loại văn bản tiếng Việt vào các chủ đề khác nhau.

## Cài đặt

1. Clone repository:

```bash
git clone <repository_url>
```

2. Di chuyển vào thư mục dự án:

```bash
cd <repository_folder>/src
```

3. Cài đặt các gói phụ thuộc:

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

1. Trong thư mục `src`, chạy lệnh:

```bash
python app.py
```

2. Mở trình duyệt và truy cập:

```
http://127.0.0.1:5000
```

## Sử dụng

1. Điền thông tin văn bản cần phân loại vào form bên trái:

   - Tiêu đề
   - Mô tả
   - Nội dung

2. Nhấn nút "Phân loại"

3. Kết quả sẽ hiển thị ở bên phải:
   - Chủ đề được dự đoán
   - Danh sách các chủ đề với xác suất tương ứng
