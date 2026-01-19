from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

import tiktoken

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)


def extract_text_from_pdf(pdf_path:str)->str:
    # langchain Pdf loader 사용
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text = "\n".join(doc.page_content for doc in documents)
    return text

def spilt_text_into_chunks(text:str)->str:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 200,
        length_function = len
    ) 

    chunks = text_splitter.split_text(text)
    return chunks

def create_vector_store(chunks:list):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"

    )

    return FAISS.from_texts(chunks, embeddings)

def answer_question(question:str, knowledge_base)->str:
    docs = knowledge_base.similarity_search(question, k=5) # k=5 : 5개 유사도 검색

    # print("\n [검색된 관련 정크들]")
    # for i,doc in enumerate(docs, 1):
    #     # 150단어로 \n => ' '
    #     preview = doc.page_content[:150].replace("\n", " ")
    #     print(f"{i}, {preview}...")

    context = "\n\n".join([doc.page_content for doc in docs if doc.page_content])

    client = OpenAI()

    # client.response.create( 와 유사함
    #   model='',
    #   input=''
    #)
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                            "You are a helpful AI assistant. "
                            "You must answer questions strictly based on the provided document content. "
                            "If the answer is clearly stated in the document, provide a concise response. "
                            "If the information is not available, respond with '문서에서 확인할 수 없습니다.' "
                            "If the document content is in English, translate the answer into Korean."
                            )
                                # "content": (
                                #     "당신은 도움이 되는 AI 어시스턴트입니다. "
                                #     "제공된 문서 내용을 기반으로만 질문에 답변하세요. "
                                #     "문서에 답이 있는 경우 명확하고 간결하게 답변하세요. "
                                #     "문서에 없는 내용은 '문서에서 확인할 수 없습니다.'라고 답변하세요. "
                                #     "문서 내용이 영어인 경우, 답변은 한국어로 번역해서 제공하세요."
                                # )
            },
            {
                "role": "user",
                "content": f"Based on the following document content, please answer the question.\n\nDocument:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3, # temperature : 1로 갈수록 random 과 다양성 높아짐.  0에 가까워질수록 결정론적 deterministic 성격이 강해짐
        max_tokens=500
    )

    return res.choices[0].message.content


def main():
    # print("test")
    pdf_path = "data/summary.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    print(f"글자수 :  {len(pdf_text)}")
    print(f"토큰수 :  {len(enc.encode(pdf_text))}")

    # text => chunk로 나눔
    chunks = spilt_text_into_chunks(pdf_text)
    print(f"총 chunk수 : {len(chunks)}")

    # # 각 chunk 의 정보출력, enumerate(list, number) : number는 시작 숫자
    # for i, chunk in enumerate(chunks,1):
    #     token_count = len(enc.encode(chunk))
    #     print(f"chunk {i} : 글자수 :{len(chunk)}, 토큰수 :{token_count}")

    print("\n-----------------------벡터스토어 생성--------------------------")

    knowledge_base = create_vector_store(chunks)

    print("\n-----------------------질문응답 테스트--------------------------")
    question = "How can ChatGPT be used?"
    # where can i use chatGPT?
    # How can ChatGPT be used?
    # Ways to use ChatGPT
    # Applications of ChatGPT
    # Use cases of ChatGPT
    print(f"질문 : {question}")

    answer = answer_question(question, knowledge_base)

    print(f"\n 답변 :  \n {answer}")
    

if __name__ == "__main__":
    main()
    