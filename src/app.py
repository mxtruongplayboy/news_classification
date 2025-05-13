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
    model_type = request.form.get('modelType', 'logistic_regression_model')
    
    # Mock responses based on model type
    if model_type == 'logistic_regression_model':
        # Mock response for Logistic Regression model
        mock_response = {
            "predicted_topic": "Quỹ Hy vọng",
            "model_info": {
                "type": "Machine Learning",
                "name": "Logistic Regression",
                "accuracy": "89.5%"
            },
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
    elif model_type == 'naive_bayes_model':
        # Mock response for Naive Bayes model
        mock_response = {
            "predicted_topic": "Quỹ Hy vọng",
            "model_info": {
                "type": "Machine Learning",
                "name": "Naive Bayes",
                "accuracy": "87.2%"
            },
            "probabilities": [
                {"topic": "Quỹ Hy vọng", "probability": 0.3420},
                {"topic": "Tổ ấm", "probability": 0.2215},
                {"topic": "Hồ sơ phá án", "probability": 0.0612},
                {"topic": "Giải trí giới sao", "probability": 0.0543},
                {"topic": "Dân sinh", "probability": 0.0387},
                {"topic": "Tin tức sức khoẻ", "probability": 0.0356},
                {"topic": "Giải trí nhạc", "probability": 0.0301},
                {"topic": "Nhịp sống", "probability": 0.0278},
                {"topic": "Giải trí phim", "probability": 0.0265},
                {"topic": "Sân khấu mỹ thuật", "probability": 0.0251},
                {"topic": "Người Việt 5 châu", "probability": 0.0165},
                {"topic": "Hậu trường thể thao", "probability": 0.0149},
                {"topic": "Chân dung", "probability": 0.0142},
                {"topic": "Giải trí thời trang", "probability": 0.0098},
                {"topic": "Sống khoẻ", "probability": 0.0087},
                {"topic": "Tin tức Giáo dục", "probability": 0.0070},
                {"topic": "Thế giới tự nhiên", "probability": 0.0065},
                {"topic": "Các môn thể thao khác", "probability": 0.0062},
                {"topic": "Giải trí làm đẹp", "probability": 0.0061},
                {"topic": "Học tiếng anh", "probability": 0.0059},
                {"topic": "Ẩm thực", "probability": 0.0058},
                {"topic": "Giao thông", "probability": 0.0056},
                {"topic": "Việc làm", "probability": 0.0050},
                {"topic": "Giáo dục 4.0", "probability": 0.0039},
                {"topic": "Du học", "probability": 0.0038},
                {"topic": "Vũ trụ", "probability": 0.0032},
                {"topic": "Hàng hóa", "probability": 0.0029},
                {"topic": "Chính trị", "probability": 0.0025},
                {"topic": "Kinh doanh doanh nghiệp", "probability": 0.0024},
                {"topic": "Bóng đá", "probability": 0.0020},
                {"topic": "Chứng khoán", "probability": 0.0018},
                {"topic": "Thị trường xe", "probability": 0.0016},
                {"topic": "Chuyển đổi số", "probability": 0.0015},
                {"topic": "Kinh doanh quốc tế", "probability": 0.0014},
                {"topic": "AI", "probability": 0.0013},
                {"topic": "Ebank", "probability": 0.0012},
                {"topic": "Quân sự", "probability": 0.0011},
                {"topic": "Thiết bị", "probability": 0.0010}
            ]
        }
    elif model_type == 'bigru_model':
        # Mock response for BiGRU Deep Learning model
        mock_response = {
            "predicted_topic": "Tổ ấm",
            "model_info": {
                "type": "Deep Learning",
                "name": "BiGRU",
                "accuracy": "92.7%"
            },
            "probabilities": [
                {"topic": "Tổ ấm", "probability": 0.3568},
                {"topic": "Quỹ Hy vọng", "probability": 0.2985},
                {"topic": "Hồ sơ phá án", "probability": 0.0621},
                {"topic": "Giải trí giới sao", "probability": 0.0489},
                {"topic": "Tin tức sức khoẻ", "probability": 0.0384},
                {"topic": "Dân sinh", "probability": 0.0359},
                {"topic": "Giải trí nhạc", "probability": 0.0325},
                {"topic": "Nhịp sống", "probability": 0.0301},
                {"topic": "Sân khấu mỹ thuật", "probability": 0.0284},
                {"topic": "Giải trí phim", "probability": 0.0271},
                {"topic": "Người Việt 5 châu", "probability": 0.0151},
                {"topic": "Hậu trường thể thao", "probability": 0.0145},
                {"topic": "Chân dung", "probability": 0.0139},
                {"topic": "Giải trí thời trang", "probability": 0.0114},
                {"topic": "Sống khoẻ", "probability": 0.0104},
                {"topic": "Tin tức Giáo dục", "probability": 0.0074},
                {"topic": "Thế giới tự nhiên", "probability": 0.0070},
                {"topic": "Các môn thể thao khác", "probability": 0.0066},
                {"topic": "Giải trí làm đẹp", "probability": 0.0063},
                {"topic": "Học tiếng anh", "probability": 0.0061},
                {"topic": "Ẩm thực", "probability": 0.0058},
                {"topic": "Giao thông", "probability": 0.0055},
                {"topic": "Việc làm", "probability": 0.0048},
                {"topic": "Giáo dục 4.0", "probability": 0.0045},
                {"topic": "Du học", "probability": 0.0042},
                {"topic": "Vũ trụ", "probability": 0.0038},
                {"topic": "Hàng hóa", "probability": 0.0033},
                {"topic": "Kinh doanh doanh nghiệp", "probability": 0.0029},
                {"topic": "Chính trị", "probability": 0.0026},
                {"topic": "Bóng đá", "probability": 0.0024},
                {"topic": "Chứng khoán", "probability": 0.0023},
                {"topic": "Thị trường xe", "probability": 0.0022},
                {"topic": "AI", "probability": 0.0021},
                {"topic": "Chuyển đổi số", "probability": 0.0020},
                {"topic": "Kinh doanh quốc tế", "probability": 0.0018},
                {"topic": "Ebank", "probability": 0.0016},
                {"topic": "Quân sự", "probability": 0.0014},
                {"topic": "Thiết bị", "probability": 0.0013}
            ]
        }
    else:  # bilstm_model
        # Mock response for BiLSTM Deep Learning model
        mock_response = {
            "predicted_topic": "Quỹ Hy vọng",
            "model_info": {
                "type": "Deep Learning",
                "name": "BiLSTM",
                "accuracy": "93.5%"
            },
            "probabilities": [
                {"topic": "Quỹ Hy vọng", "probability": 0.3654},
                {"topic": "Tổ ấm", "probability": 0.3127},
                {"topic": "Hồ sơ phá án", "probability": 0.0599},
                {"topic": "Giải trí giới sao", "probability": 0.0468},
                {"topic": "Dân sinh", "probability": 0.0379},
                {"topic": "Tin tức sức khoẻ", "probability": 0.0373},
                {"topic": "Giải trí nhạc", "probability": 0.0332},
                {"topic": "Nhịp sống", "probability": 0.0312},
                {"topic": "Giải trí phim", "probability": 0.0291},
                {"topic": "Sân khấu mỹ thuật", "probability": 0.0263},
                {"topic": "Người Việt 5 châu", "probability": 0.0149},
                {"topic": "Hậu trường thể thao", "probability": 0.0143},
                {"topic": "Chân dung", "probability": 0.0133},
                {"topic": "Giải trí thời trang", "probability": 0.0108},
                {"topic": "Sống khoẻ", "probability": 0.0099},
                {"topic": "Tin tức Giáo dục", "probability": 0.0078},
                {"topic": "Thế giới tự nhiên", "probability": 0.0072},
                {"topic": "Các môn thể thao khác", "probability": 0.0068},
                {"topic": "Giải trí làm đẹp", "probability": 0.0065},
                {"topic": "Học tiếng anh", "probability": 0.0059},
                {"topic": "Ẩm thực", "probability": 0.0057},
                {"topic": "Giao thông", "probability": 0.0053},
                {"topic": "Việc làm", "probability": 0.0047},
                {"topic": "Giáo dục 4.0", "probability": 0.0043},
                {"topic": "Du học", "probability": 0.0041},
                {"topic": "Vũ trụ", "probability": 0.0036},
                {"topic": "Hàng hóa", "probability": 0.0031},
                {"topic": "Chính trị", "probability": 0.0028},
                {"topic": "Kinh doanh doanh nghiệp", "probability": 0.0026},
                {"topic": "Bóng đá", "probability": 0.0023},
                {"topic": "Chứng khoán", "probability": 0.0022},
                {"topic": "Thị trường xe", "probability": 0.0021},
                {"topic": "AI", "probability": 0.0019},
                {"topic": "Chuyển đổi số", "probability": 0.0018},
                {"topic": "Kinh doanh quốc tế", "probability": 0.0017},
                {"topic": "Ebank", "probability": 0.0014},
                {"topic": "Quân sự", "probability": 0.0013},
                {"topic": "Thiết bị", "probability": 0.0010}
            ]
        }
    
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(debug=True) 