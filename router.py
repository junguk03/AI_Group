import os
from google import genai
from google.genai import types

PREFIXES = {
    "gemini:": "gemini",
    "groq:":   "groq",
    "code:":   "mistral",
    "mistral:": "mistral",
}

ROUTER_PROMPT = """다음 질문을 보고 어떤 AI가 담당할지 판단해줘.

- gemini: 최신 뉴스/기사, 취업/진로 상담, 자격증 일정, BOB 후기, 보안 강연/전시회, 글쓰기, 감상문, 건강 상담, 이미지/피그마 관련
- groq: 보안 지식, CTF, 워게임, Bandit, PortSwigger, 취약점 분석, 모의해킹, 악성코드, 암호학, 리눅스, 클라우드
- mistral: 코드 작성, 코드 리뷰, 프로그래밍 언어, 깃허브 사용법, 개발 관련

반드시 gemini, groq, mistral 중 하나만 소문자로 답해. 다른 말은 하지 마."""


def route(query: str) -> tuple[str, str]:
    for prefix, agent in PREFIXES.items():
        if query.lower().startswith(prefix):
            return agent, query[len(prefix):].strip()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model=os.getenv("GEMINI_ROUTER_MODEL", "gemini-2.0-flash"),
        contents=f"질문: {query}",
        config=types.GenerateContentConfig(
            system_instruction=ROUTER_PROMPT,
            temperature=0,
        ),
    )
    result = response.text.strip().lower()
    if result not in ("gemini", "groq", "mistral"):
        result = "gemini"
    return result, query
