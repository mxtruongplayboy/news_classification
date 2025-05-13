import requests
from readability import Document
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# URL của Google News hoặc trang bạn muốn crawl
url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"

# Gửi yêu cầu GET
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các phần tử có class 'PO9Zff Ccj79 kUVvS'
    elements = soup.find_all(class_="PO9Zff Ccj79 kUVvS")

    # Lặp qua từng element và lấy href của tất cả các thẻ con có class 'WwrzSb'
    for idx, element in enumerate(elements, 1):
        # Tìm tất cả các phần tử con có class 'WwrzSb' trong mỗi element
        links = element.find_all(class_="WwrzSb")
        
        # Lặp qua tất cả các link tìm được và xử lý chuyển tiếp
        for link_idx, link in enumerate(links, 1):
            href = link.get('href')
            
            # Bỏ dấu chấm đầu tiên và thêm https://news.google.com vào trước
            if href.startswith('.'):
                href = 'https://news.google.com' + href[1:]
                
            print(f"{idx}-{link_idx}. Đang truy cập vào: {href}")

            # Cấu hình Selenium WebDriver
            chrome_options = Options()
            chrome_options.add_argument('--disable-gpu')  # Tắt GPU để tiết kiệm tài nguyên
            chrome_options.add_argument('--enable-features=ReaderMode')  # Bật Reader Mode

            # Khởi tạo WebDriver
            service = Service("E:\\chromedriver-win64\\chromedriver.exe")  # Thay thế bằng đường dẫn ChromeDriver của bạn
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Truy cập vào link và đợi trang tải xong
            driver.get(href)

            # Đợi 5 giây để trang chuyển tiếp hoàn tất
            time.sleep(5)

            # Lấy nội dung trang web với Readability
            content = driver.page_source
            doc = Document(content)
            readable_html = doc.summary()  # Lấy nội dung dưới dạng HTML đã được xử lý

            # Hiển thị nội dung đọc được từ trang
            print(f"Nội dung sau khi xử lý Read Mode cho link {href}:\n")
            print(readable_html)

            # Đóng trình duyệt sau khi xử lý xong
            driver.quit()
else:
    print("Không thể tải trang Google News!")
