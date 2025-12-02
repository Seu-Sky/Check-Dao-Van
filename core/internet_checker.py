import requests
import re
import os
from dotenv import load_dotenv

# 1. Nạp biến môi trường
load_dotenv()

# Lấy Key
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def check_internet_sources(text):
    """
    Hàm này tách văn bản thành câu và tìm trên Google.
    Trả về danh sách các link trùng lặp.
    """
    sources = []
    
    # 1. Làm sạch và tách câu (Tách theo dấu chấm, chấm than, chấm hỏi)
    # Lưu ý: Để tiết kiệm quota Google (chỉ có 100 request/ngày),
    # ta chỉ lấy 3 câu đầu tiên hoặc các câu dài để kiểm tra demo.
    sentences = re.split(r'[.!?]+', text)
    
    # Lọc các câu quá ngắn (dưới 20 ký tự thường không phải đạo văn)
    long_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    # Lấy tối đa 3 câu để check (tránh hết quota ngay lập tức)
    check_limit = long_sentences[:3] 

    url = "https://www.googleapis.com/customsearch/v1"

    for sentence in check_limit:
        params = {
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': f'"{sentence}"' # Dấu ngoặc kép để tìm chính xác cụm từ
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            # Nếu tìm thấy kết quả
            if 'items' in data:
                for item in data['items']:
                    sources.append({
                        'title': item['title'],
                        'link': item['link'],
                        'snippet': item['snippet'],
                        'match_text': sentence # Câu bị trùng
                    })
        except Exception as e:
            print(f"Lỗi kết nối Google: {e}")

    return sources