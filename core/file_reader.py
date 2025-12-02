import os
import docx
from PyPDF2 import PdfReader

def read_file(file_path):
    """
    Hàm này nhận vào đường dẫn file và trả về nội dung text.
    Hỗ trợ: .txt, .docx, .pdf
    """
    # Lấy đuôi file (extension) để biết cách xử lý
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    text = ""

    try:
        # Xử lý file Word (.docx)
        if file_extension == '.docx':
            doc = docx.Document(file_path)
            # Nối từng đoạn văn (paragraph) lại với nhau
            text = '\n'.join([para.text for para in doc.paragraphs])

        # Xử lý file PDF (.pdf)
        elif file_extension == '.pdf':
            reader = PdfReader(file_path)
            # Lặp qua từng trang để lấy text
            for page in reader.pages:
                text += page.extract_text() + "\n"

        # Xử lý file Text (.txt)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return ""

    return text