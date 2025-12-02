from transformers import pipeline # pip install transformers

# Tải model phát hiện AI (Ví dụ model của roberta-base-openai-detector)
# Lần đầu chạy nó sẽ tải model về máy nên hơi lâu
ai_detector = pipeline("text-classification", model="roberta-base-openai-detector")

def check_ai_generated(text):
    """
    Hàm kiểm tra xem text có phải AI viết không.
    Trả về: Label (Real/Fake) và Score (Độ tin cậy)
    """
    # Cắt ngắn text vì model thường chỉ nhận khoảng 512 ký tự đầu
    short_text = text[:510] 
    
    result = ai_detector(short_text)
    # Kết quả trả về dạng: [{'label': 'Real', 'score': 0.98}] hoặc 'Fake'
    return result[0]