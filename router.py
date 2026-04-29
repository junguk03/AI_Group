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

- gemini: 아래 중 하나라도 해당하면 무조건 gemini
  * 최신/최근/요즘/현재/2025/2026 등 시간 관련 표현 포함
  * 뉴스, 기사, 동향, 트렌드, 시장 관련
  * 검색해줘 / 찾아줘 / 알아봐줘 요청
  * 취업/진로/채용/연봉 상담
  * 자격증 일정, BOB, 강연, 전시회, 행사
  * 글쓰기, 감상문, 에세이, 건강 상담
  * 이미지/피그마/디자인 관련

- groq: 보안 지식, CTF, 워게임, Bandit, PortSwigger, 취약점 분석, 모의해킹, 악성코드, 암호학, 리눅스, 클라우드, 네트워크

- mistral: 코드 작성, 코드 리뷰, 프로그래밍 언어, 깃허브 사용법, 개발 관련

반드시 gemini, groq, mistral 중 하나만 소문자로 답해. 다른 말은 하지 마."""


def route(query: str) -> tuple[str, str]:
    for prefix, agent in PREFIXES.items():
        if query.lower().startswith(prefix):
            return agent, query[len(prefix):].strip()

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
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
