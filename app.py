import streamlit as st
from dotenv import load_dotenv
from router import route
from agents.gemini_agent import ask as gemini_ask
from agents.groq_agent import ask as groq_ask
from agents.mistral_agent import ask as mistral_ask

load_dotenv()

AGENTS = {
    "gemini": {"label": "Gemini 2.5 Flash", "icon": "🔵", "desc": "검색 · 글쓰기 · 진로"},
    "groq":   {"label": "Groq / Llama 4",   "icon": "🟠", "desc": "보안 · CTF · 리눅스"},
    "mistral":{"label": "Mistral Codestral", "icon": "🟣", "desc": "코드 · 개발 · 리뷰"},
}

AGENT_FN = {
    "gemini":  gemini_ask,
    "groq":    groq_ask,
    "mistral": mistral_ask,
}

st.set_page_config(page_title="OrchestrAI", page_icon="🤖", layout="wide")

# 사이드바
with st.sidebar:
    st.title("🤖 OrchestrAI")
    st.caption("질문에 따라 최적의 AI를 자동 선택합니다")
    st.divider()
    st.markdown("#### 직접 지정하려면 접두어 사용")
    for prefix, agent in [("gemini:", "gemini"), ("groq:", "groq"), ("code:", "mistral")]:
        info = AGENTS[agent]
        st.markdown(f"`{prefix}` → {info['icon']} {info['label']}")
    st.divider()
    st.markdown("#### 담당 AI")
    for key, info in AGENTS.items():
        st.markdown(f"{info['icon']} **{info['label']}**  \n{info['desc']}")
    st.divider()
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# 채팅 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        info = AGENTS[msg.get("agent", "gemini")]
        with st.chat_message("assistant"):
            st.caption(f"{info['icon']} {info['label']}")
            st.write(msg["content"])

# 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    agent, clean_query = route(prompt)
    info = AGENTS[agent]

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-11:-1]
    ]

    with st.chat_message("assistant"):
        st.caption(f"{info['icon']} {info['label']}")
        with st.spinner(f"{info['label']} 처리 중..."):
            try:
                response = AGENT_FN[agent](clean_query, history)
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    import re
                    retry = re.search(r'retry[^0-9]*(\d+)', err)
                    wait = f"{retry.group(1)}초 후 재시도" if retry else "잠시 후 재시도"
                    response = f"⚠️ {info['label']} 무료 한도 초과\n\n{wait} 하거나 다른 AI 접두어를 사용해보세요.\n예) `groq:` 또는 `gemini:` 접두어 사용"
                    st.warning(f"🚫 {info['label']} 쿼터 초과 — {wait}")
                else:
                    response = f"오류: {err}\n\n모델 ID나 API 키를 확인해주세요."
        st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "agent": agent,
    })
