# app.py
import os
from flask import Flask, render_template, request
from core.file_reader import read_file
from core.internet_checker import check_internet_sources

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def highlight_text(original_text, sources):
    """
    Hàm này nhận văn bản gốc và danh sách các nguồn trùng lặp.
    Nó sẽ bôi vàng (dùng thẻ <mark>) các câu bị trùng trong văn bản gốc.
    """
    highlighted_text = original_text
    
    # Lấy danh sách các câu bị trùng (loại bỏ trùng lặp)
    matched_sentences = set(item['match_text'] for item in sources)
    
    for sentence in matched_sentences:
        # Dùng replace để chèn thẻ <mark> vào câu bị trùng
        # Lưu ý: Cách này đơn giản, có thể highlight sai nếu câu đó quá ngắn và xuất hiện nhiều chỗ.
        # Nhưng với câu dài thì ok.
        if sentence.strip():
             # Sử dụng style trực tiếp để chắc chắn nó hiện màu
            replacement = f'<mark style="background-color: #fff3cd; color: #856404;">{sentence}</mark>'
            highlighted_text = highlighted_text.replace(sentence, replacement)
            
    return highlighted_text

@app.route('/', methods=['GET', 'POST'])
def home():
    text_content = ""
    highlighted_content = "" # Nội dung đã được tô màu
    sources = []
    
    if request.method == 'POST':
        if 'file1' in request.files:
            file1 = request.files['file1']
            if file1.filename != '':
                path1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(path1)
                
                # 1. Đọc file
                text_content = read_file(path1)
                
                # 2. Quét Internet (Mất thời gian)
                sources = check_internet_sources(text_content)

                # 3. Tạo phiên bản tô màu highlight
                highlighted_content = highlight_text(text_content, sources)

    return render_template('index.html', 
                           t1=text_content, 
                           highlighted_content=highlighted_content,
                           sources=sources)

if __name__ == '__main__':
    app.run(debug=True)