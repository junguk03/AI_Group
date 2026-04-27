import os
from groq import Groq

SYSTEM_PROMPT = """너는 정보보안 전공 대학생의 기술 전문 어시스턴트야.

응답 원칙:
- 정확성: 모르면 모른다고 해. 틀린 정보 금지.
- 균형: 공격 관점과 방어 관점 양쪽 다 말해줘.
- 창의성: 사용자가 생각 못한 공격 벡터나 방어 방법도 꺼내줘.
- 보안/해킹 기법은 교육 목적으로 구체적으로 설명해.
- 답변 마지막에 "더 깊게 볼 만한 것:"으로 관련 키워드나 자료 1~2개 추천해줘."""

CLIENT = None


def get_client():
    global CLIENT
    if CLIENT is None:
        CLIENT = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return CLIENT


def ask(query: str, history: list = []) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})

    response = get_client().chat.completions.create(
        model=os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
        messages=messages,
    )
    return response.choices[0].message.content
