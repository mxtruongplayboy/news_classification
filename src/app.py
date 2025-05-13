from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    # Get form data
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    content = request.form.get('content', '')
    
    # Mock response with example data (this would be replaced with actual classification logic)
    mock_response = {
        "predicted_topic": "Quỹ Hy vọng",
        "probabilities": [
            {"topic": "Quỹ Hy vọng", "probability": 0.3216},
            {"topic": "Tổ ấm", "probability": 0.2367},
            {"topic": "Hồ sơ phá án", "probability": 0.0581},
            {"topic": "Giải trí giới sao", "probability": 0.0499},
            {"topic": "Dân sinh", "probability": 0.0369},
            {"topic": "Tin tức sức khoẻ", "probability": 0.0344},
            {"topic": "Giải trí nhạc", "probability": 0.0313},
            {"topic": "Nhịp sống", "probability": 0.0290},
            {"topic": "Giải trí phim", "probability": 0.0281},
            {"topic": "Sân khấu mỹ thuật", "probability": 0.0273},
            {"topic": "Người Việt 5 châu", "probability": 0.0159},
            {"topic": "Hậu trường thể thao", "probability": 0.0155},
            {"topic": "Chân dung", "probability": 0.0149},
            {"topic": "Giải trí thời trang", "probability": 0.0104},
            {"topic": "Sống khoẻ", "probability": 0.0094},
            {"topic": "Tin tức Giáo dục", "probability": 0.0064},
            {"topic": "Thế giới tự nhiên", "probability": 0.0060},
            {"topic": "Các môn thể thao khác", "probability": 0.0058},
            {"topic": "Giải trí làm đẹp", "probability": 0.0057},
            {"topic": "Học tiếng anh", "probability": 0.0055},
            {"topic": "Ẩm thực", "probability": 0.0054},
            {"topic": "Giao thông", "probability": 0.0052},
            {"topic": "Việc làm", "probability": 0.0046},
            {"topic": "Giáo dục 4.0", "probability": 0.0041},
            {"topic": "Du học", "probability": 0.0040},
            {"topic": "Vũ trụ", "probability": 0.0034},
            {"topic": "Hàng hóa", "probability": 0.0030},
            {"topic": "Chính trị", "probability": 0.0027},
            {"topic": "Kinh doanh doanh nghiệp", "probability": 0.0027},
            {"topic": "Bóng đá", "probability": 0.0022},
            {"topic": "Chứng khoán", "probability": 0.0021},
            {"topic": "Thị trường xe", "probability": 0.0021},
            {"topic": "Chuyển đổi số", "probability": 0.0019},
            {"topic": "Kinh doanh quốc tế", "probability": 0.0019},
            {"topic": "AI", "probability": 0.0017},
            {"topic": "Ebank", "probability": 0.0015},
            {"topic": "Quân sự", "probability": 0.0014},
            {"topic": "Thiết bị", "probability": 0.0014}
        ]
    }
    
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(debug=True) 