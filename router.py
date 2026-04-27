from __future__ import annotations
import os
from groq import Groq

PREFIXES = {
    "gemini:":  "gemini",
    "groq:":    "groq",
    "code:":    "mistral",
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

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": ROUTER_PROMPT},
                {"role": "user", "content": f"질문: {query}"},
            ],
            temperature=0,
            max_tokens=10,
        )
        result = response.choices[0].message.content.strip().lower()
        if result not in ("gemini", "groq", "mistral"):
            result = "gemini"
    except Exception:
        result = "gemini"

    return result, query
