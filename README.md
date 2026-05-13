# 🤖 OrchestrAI

> 질문 유형에 따라 최적의 AI를 자동으로 선택하는 멀티 에이전트 라우터

---

## 왜 만들었나

AI마다 잘하는 게 다릅니다. 검색은 Gemini, 보안 지식은 Groq, 코드는 Mistral. 매번 어떤 AI를 쓸지 고민하지 않고 질문 하나만 보내면 가장 잘 답할 수 있는 AI가 자동으로 선택됩니다.

---

## 사용 AI

| AI | 모델 | 특화 영역 | 비용 |
|---|---|---|---|
| 🔵 Gemini | gemini-2.5-flash | 실시간 검색 · 글쓰기 · 진로 · 이미지 분석 | 무료 |
| 🟠 Groq | llama-4-scout-17b | 보안 · CTF · 취약점 · 리눅스 · 암호학 | 무료 |
| 🟣 Mistral | codestral-latest | 코드 작성 · 리뷰 · 개발 | 무료 |

---

## 주요 기능

```
자동 라우팅      Groq Llama 4가 질문을 분류해 적합한 AI에게 전달
웹 검색         Gemini가 Google Search grounding으로 최신 정보 답변
이미지 분석     피그마, 스케치, 다이어그램 등 첨부 시 Gemini가 분석
문서 첨부       PDF · PPTX · DOCX 텍스트 추출 후 라우팅
세션 관리       대화 자동 저장, 사이드바에서 이전 대화 복원/삭제
모바일 대응     반응형 CSS로 폰에서도 사용 가능
접두어 모드     gemini: / groq: / code: 로 AI 직접 지정
```

---

## 라우팅 흐름

```
사용자 입력
    │
    ▼
접두어 검사 ── gemini: / groq: / code: / mistral: 있으면 해당 AI로 직행
    │
    ▼
[Groq Llama 4 라우터] ── 질문 주제 분류
    │
    ├── 검색 / 최신 / 글쓰기 / 진로 / 이미지   ──▶  🔵 Gemini
    ├── 보안 / CTF / 취약점 / 리눅스 / 암호학  ──▶  🟠 Groq
    └── 코드 / 개발 / 깃허브                  ──▶  🟣 Mistral
```

라우터를 Gemini가 아닌 **Groq**으로 둔 이유: Gemini의 무료 할당량을 답변용으로 아끼고, 라우팅 같은 단순 분류는 더 빠른 Groq Llama 4가 처리합니다.

---

## 주제별 담당 AI

| 주제 | 담당 |
|---|---|
| 보안 기사 · 트렌드 · BOB · 강연 / 전시회 / 자격증 일정 | 🔵 Gemini |
| 취업 · 진로 · 채용 · 연봉 (실제 채용 트렌드 기반) | 🔵 Gemini |
| 글쓰기 · 감상문 · 에세이 · 건강 상담 | 🔵 Gemini |
| 피그마 · 디자인 · 이미지 분석 | 🔵 Gemini |
| PortSwigger · Bandit · CTF · 워게임 · 모의해킹 · 악성코드 · 암호학 | 🟠 Groq |
| 리눅스 · 클라우드 · 네트워크 | 🟠 Groq |
| 프로그래밍 언어 · 코드 리뷰 · 깃허브 사용법 · 개발 일반 | 🟣 Mistral |

---

## 시스템 프롬프트

#### 공통 원칙
```
- 정확성: 불확실한 건 불확실하다고 말한다
- 균형: 장단점 양쪽 모두 말한다
- 창의성: 사용자가 생각 못한 관점도 꺼낸다
- 진로/취업: 공감 대신 실제 채용 트렌드와 데이터로 말한다
```

#### Gemini
```
검색이 필요한 질문은 Google Search grounding으로 최신 정보를 가져온 뒤 답변.
취업/진로 질문은 2026~2028년 보안 채용 시장 기준으로
실제 채용 공고와 트렌드를 근거로 구체적으로 답변.
공감형 위로보다 현실적인 정보 제공 우선.
```

#### Groq
```
보안/기술 질문 전담. 모르면 모른다고 한다.
취약점·해킹 기법은 교육 목적으로 정확하게 설명한다.
공격 관점과 방어 관점 양쪽 다 제시한다.
답변 끝에 더 깊게 볼 자료/키워드 1~2개 추천.
```

#### Mistral
```
코딩 전담. 코드 정확성 최우선.
여러 구현 방식이 있으면 각각의 장단점을 보여준다.
더 나은 대안이 있으면 먼저 꺼낸다.
```

---

## 시작하기

```bash
# 1. 설치
pip install -r requirements.txt

# 2. API 키 설정
cp .env.example .env
# .env에 GEMINI_API_KEY, GROQ_API_KEY, MISTRAL_API_KEY 입력

# 3. 실행
streamlit run app.py
```

### Streamlit Community Cloud 배포

1. GitHub repo 연결 후 `app.py` 지정
2. Secrets에 API 키 3종 추가
3. push 하면 자동 재배포

---

## 프로젝트 구조

```
.
├── app.py                  # Streamlit UI · 세션 · 파일 첨부
├── router.py               # Groq 기반 자동 라우팅
├── session_manager.py      # JSON 세션 저장/로드 (이미지 base64 인코딩)
├── agents/
│   ├── gemini_agent.py     # Gemini + Google Search + 이미지
│   ├── groq_agent.py       # Groq Llama 4 Scout
│   └── mistral_agent.py    # Mistral Codestral
├── sessions/               # 대화 기록 (gitignore)
└── requirements.txt
```

---

## 기술 스택

`Python` · `Streamlit` · `Google AI Studio` · `Groq` · `Mistral AI` · `python-pptx` · `pypdf` · `python-docx`
