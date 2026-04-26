import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """너는 정보보안 전공 대학생의 AI 어시스턴트야.

응답 원칙:
- 정확성: 불확실하면 불확실하다고 말해. 틀린 정보 절대 금지.
- 균형: 장단점 양쪽 다 말해. 한쪽만 밀지 마.
- 창의성: 사용자가 생각 못한 관점도 꺼내줘.
- 취업/진로: 공감 대신 실제 채용 트렌드와 데이터로 말해줘. 2026~2028년 보안 취업 시장 기준.
- 검색이 필요한 질문은 반드시 최신 정보를 가져온 뒤 답변해."""


def ask(query: str, history: list = [], image_bytes: bytes = None, mime_type: str = None) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(types.Content(
            role=role,
            parts=[types.Part(text=msg["content"])]
        ))

    user_parts = [types.Part(text=query)]
    if image_bytes and mime_type:
        user_parts.append(types.Part(
            inline_data=types.Blob(mime_type=mime_type, data=image_bytes)
        ))
    contents.append(types.Content(role="user", parts=user_parts))

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    return response.text
