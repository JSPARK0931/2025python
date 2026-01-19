from PyPDF2 import PdfReader
import tiktoken


pdf_path = "data/summary.pdf"
#pdf_path = "data/sample01.pdf"
#pdf_path = "data/sample01_image.pdf" # 노트북 lm을 이용해서 뽑아낼수 있음 , 그냥은 못가지고옴
# pdf_reader = PdfReader(pdf_path)

# #print(pdf_reader.pages)

# total_text = ""
# for page in pdf_reader.pages:
#     total_text += page.extract_text()

# print(total_text)

# f = open("text.txt", "w")
# f.write("hello")
# f.close()

# with 표현문 as variable:
# with open("text.txt", "w") as f:
#     f.write("hello")

# enumerate list => 순번
# for i,v in enumerate(["a","b","c"]):
#     print(i,v)
# 0 a
# 1 b
# 2 c

# pdf_path:str : path변수 string  , -> str 내보내는 return값. 에러방지용
# page_text =""
def extract_text_from_pdf(pdf_path:str)->str:
    text = ""
    # 파일연결, DB연결, socket연결, close를 안하므로 유리함
    # rb : read binary로 읽음
    with open(pdf_path,"rb") as f:
        reader = PdfReader(f)
        for i,page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"


    return text

pdf_text = extract_text_from_pdf(pdf_path)
enc = tiktoken.encoding_for_model("gpt-4o-mini")

print(f"글자수 : ", len(pdf_text))
print(f"토근수 : ", len(enc.encode(pdf_text)))


extract_text_from_pdf(pdf_path)

