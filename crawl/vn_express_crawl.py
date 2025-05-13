import requests
from bs4 import BeautifulSoup
import csv
import time
import unicodedata

def remove_vietnamese_accents(text):
    # Chuyển văn bản sang dạng không dấu và thay thế ký tự không hợp lệ thành dấu gạch dưới
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def crawl_article_details(article_url, writer, topic):
    # Gửi yêu cầu HTTP GET đến URL bài viết chi tiết
    response = requests.get(article_url)
    
    # Kiểm tra nếu phản hồi thành công (status code 200)
    if response.status_code == 200:
        # Phân tích HTML của trang bài viết chi tiết
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm tiêu đề bài viết trong thẻ <h1> có class 'title-detail'
        title_tag = soup.find('h1', class_='title-detail')
        title = title_tag.text.strip() if title_tag else 'Không tìm thấy tiêu đề'
        
        # Tìm ngày đăng (giả sử ngày đăng nằm trong thẻ có class 'publish-date')
        date_tag = soup.find('span', class_='date')
        date = date_tag.text.strip() if date_tag else 'Không tìm thấy ngày đăng'
        
        # Tìm mô tả bài viết trong thẻ <p> có class 'description'
        description_tag = soup.find('p', class_='description')
        description = description_tag.text.strip() if description_tag else 'Không tìm thấy mô tả'
        
        # Tìm tất cả các thẻ <p> có class 'Normal'
        paragraphs = soup.find_all('p', class_='Normal')
        content = []
        if paragraphs:
            # Lấy nội dung bài viết từ tất cả các thẻ <p> có class 'Normal', ngoại trừ thẻ cuối cùng
            for p in paragraphs[:-1]:  # Lấy tất cả các đoạn văn, trừ đoạn văn cuối (tác giả)
                content.append(p.text.strip())
            
            # Lấy tác giả từ thẻ <p> cuối cùng
            author = paragraphs[-1].text.strip()  # Thẻ <p> cuối cùng chứa tên tác giả
        else:
            content = 'Không tìm thấy nội dung bài viết'
            author = 'Không tìm thấy tác giả'
        
        # Ghi vào file CSV, thêm cột 'Topic' (chủ đề)
        writer.writerow([title, date, description, '\n'.join(content), author, topic])

def crawl_articles_from_csv(csv_file):
    # Đọc các URL từ file CSV và tạo file CSV riêng cho mỗi chủ đề
    with open(csv_file, mode='r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        next(reader)  # Bỏ qua dòng tiêu đề nếu có
        for row in reader:
            name, url = row[0], row[1]
            print(f"Crawling articles from {name} ({url})")
            
            # Biến đổi tên chủ đề thành tên file hợp lệ
            topic = remove_vietnamese_accents(name)
            file_name = f"{topic}_articles.csv"
            
            # Mở file CSV để ghi kết quả cho mỗi chủ đề
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Ghi tiêu đề các cột vào file CSV
                writer.writerow(['Title', 'Date', 'Description', 'Content', 'Author', 'Topic'])
                
                page_num = 1
                while page_num <= 15:  # Giới hạn crawl tối đa 15 trang
                    # Thêm số trang vào URL để phân trang
                    page_url = f"{url}-p{page_num}"
                    print(f"Đang crawl: {page_url}")
                    
                    # Gửi yêu cầu HTTP GET đến URL
                    response = requests.get(page_url)
                    
                    # Kiểm tra nếu phản hồi thành công (status code 200)
                    if response.status_code == 200:
                        # Phân tích HTML của trang web
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Tìm tất cả các thẻ <article>
                        articles = soup.find_all('article')
                        
                        if not articles:
                            # Nếu không tìm thấy bài viết nào, chuyển sang URL khác
                            print(f"Không tìm thấy bài viết nào tại {page_url}, chuyển sang URL khác trong file CSV.")
                            break
                        
                        # Lặp qua các thẻ <article>
                        for index, article in enumerate(articles):
                            print(f"Article {index + 1}:")
                            
                            # Tìm thẻ <h2> có class là 'title-news'
                            h2_tag = article.find('h2', class_='title-news')
                            if h2_tag:
                                # Tìm thẻ <a> bên trong <h2> và lấy thuộc tính href
                                a_tag = h2_tag.find('a')
                                if a_tag and 'href' in a_tag.attrs:
                                    href = a_tag.attrs['href']
                                    print(f"Href: {href}")
                                    
                                    # Tạo liên kết đầy đủ nếu href là liên kết nội bộ
                                    if href.startswith('/'):
                                        href = 'https://vnexpress.net' + href
                                    
                                    # Gọi hàm crawl_article_details để lấy thông tin từ bài viết chi tiết và ghi vào CSV
                                    crawl_article_details(href, writer, name)
                                else:
                                    print("Không tìm thấy thẻ <a> với thuộc tính href trong <h2>.")
                            else:
                                print("Không tìm thấy thẻ <h2> với class 'title-news'.")
                            
                            print("-" * 80)
                        
                        # Tăng số trang để tiếp tục crawl các trang tiếp theo
                        page_num += 1
                    else:
                        # Kiểm tra nếu URL đã chuyển hướng
                        if response.status_code == 301 or response.status_code == 302:
                            print(f"URL đã chuyển hướng, đổi URL khác trong file CSV.")
                            break
                        else:
                            print(f"Không thể lấy dữ liệu từ trang web {name}. Mã lỗi: {response.status_code}")
                            break
                    
                    # Tạm dừng một chút trước khi tiếp tục crawl (để tránh bị chặn bởi website)
                    time.sleep(2)

# Đọc danh sách URL từ file CSV
csv_file = r'E:\LEARN_5\XuLyNgonNguTuNhien\project\crawl\source.csv'  # Thay đổi tên file CSV nếu cần
crawl_articles_from_csv(csv_file)
