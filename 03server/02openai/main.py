from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import os
import json


# 로그인시 환경변수 재생성
load_dotenv(override=True)
app = FastAPI(
    title = "myAPI"

)

#print(os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# response = client.responses.create(
#     model ="gpt-4o-mini",
#     # input = "서울의 갈 만한 여행지 추천해줘"
#     input = [
#         {
#             "role":"system",
#             "content":(
#                 "너는 json 생성기다"
#                 "반드시 json 형식으로만 출력해줘"
#                 "설명, 말머리, 마크다운, 코드블록은 절대 포함하지 마"
#                 "제목, 설명내용, 5개만 json출력"
#             )
#         },
#         {
#             "role":"user",
#             "content":"서울의 갈 만한 여행지 추천해줘"

#         }
#     ]
# )

# print(response.output_text)

# class 선언
class UserRequest(BaseModel):
    content:str

@app.get("/")
def root():
    return {"message":"Hi openai"}

# @app.post("/generate")
# def openai(request:UserRequest):
#     return {"message": request.content}

@app.post("/generate")
def openai(request:UserRequest):
    prompt = f"""
{request.content}
아래 json 배열 형식으로만 응답해줘. 반드시 json 이어야 해
데이터는 5개 출력해줘
[
    {{
        "name":"장소명",
        "type":"관광/자연/음식",
        "desc":"간단설명",
        "trans":"대중교통팁"
    }},
    {{
        "name":"장소명",
        "type":"관광/자연/음식",
        "desc":"간단설명",
        "trans":"대중교통팁"
    }}

]

"""
    ####
    # 예시
    # 1. 여행지명
    #  - 관광, 음식, 자연
    #  - 간단한 서령
    #  - 교통편
    #  - 주소
    # 2. 여행지명
    #  - 관광, 음식, 자연
    #  - 간단한 서령
    #  - 교통편
    #  - 주소
    ####
    response = client.responses.create(
        model ="gpt-4o-mini",
        input = [
            {
                "role":"system",
                "content":(
                    "너는 json 생성기다"
                    "반드시 json 형식으로만 출력해줘"
                    "설명, 말머리, 마크다운, 코드블록은 절대 포함하지 마"
                )
            },
            {
                "role":"user",
                "content":prompt

            }
        ]
    )
    # json 형태 parser 사용
    # parsed_output = json.loads(response.output_text)
    # return {"message": parsed_output}
    try:
        parsed_output = json.loads(response.output_text)
        return {"message": parsed_output}
    except json.JSONDecodeError:
        return {"output":response.output_text,"error":"json parsing 실패"}