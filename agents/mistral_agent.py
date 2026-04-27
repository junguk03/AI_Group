import os

try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

SYSTEM_PROMPT = """너는 정보보안 전공 대학생의 코딩 전문 어시스턴트야.

응답 원칙:
- 정확성: 코드 정확성 최우선. 작동 안 하는 코드는 내지 마.
- 균형: 여러 구현 방식이 있으면 각각의 장단점 보여줘.
- 창의성: 더 나은 대안이나 라이브러리가 있으면 먼저 꺼내줘.
- 보안 코드는 취약점 여부도 함께 체크해줘.
- 코드 블록은 항상 언어 명시해서 작성해."""

CLIENT = None


def get_client():
    global CLIENT
    if not MISTRAL_AVAILABLE:
        raise RuntimeError("mistralai 패키지가 설치되지 않았습니다. requirements.txt를 확인하세요.")
    if CLIENT is None:
        CLIENT = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    return CLIENT


def ask(query: str, history: list = []) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})

    response = get_client().chat.complete(
        model=os.getenv("MISTRAL_MODEL", "codestral-latest"),
        messages=messages,
    )
    return response.choices[0].message.content
