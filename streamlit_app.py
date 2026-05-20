import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="헬스케어 가이드 챗봇",
    page_icon="🌿",
    layout="centered"
)
# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="세계 날씨 & 시간 챗봇",
    page_icon="🌍",
    layout="centered"
)

# -----------------------------------
# 제목
# -----------------------------------
st.title("🌍 세계 날씨 & 시간 챗봇")

st.write(
    """
세계 지역/도시의:
- 🌤️ 날씨
- 🕒 현재 시간
- 🌏 한국과의 시차
- ✈️ 여행 팁

을 알려주는 AI 챗봇입니다.
"""
)

# -----------------------------------
# OpenAI API Key 입력
# -----------------------------------
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

if not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.", icon="🗝️")
    st.stop()

# -----------------------------------
# OpenAI Client
# -----------------------------------
client = OpenAI(api_key=openai_api_key)

# -----------------------------------
# 시스템 프롬프트
# -----------------------------------
SYSTEM_PROMPT = """
당신은 세계 날씨와 시간 정보를 알려주는 AI 여행 도우미입니다.

역할:
- 세계 도시의 현재 날씨 설명
- 현재 시간 안내
- 한국(서울)과의 시차 설명
- 여행 팁 제공
- 친절하고 쉽게 설명

규칙:
- 답변은 간결하고 보기 쉽게 작성
- 리스트 형태 사용
- 이모지 적극 활용
- 도시와 국가명을 함께 설명
"""

# -----------------------------------
# 추천 질문
# -----------------------------------
st.subheader("추천 질문")

col1, col2 = st.columns(2)

with col1:
    if st.button("🇺🇸 뉴욕 날씨 알려줘"):
        st.session_state.example = "뉴욕 날씨와 현재 시간 알려줘"

    if st.button("🇯🇵 도쿄와 서울 시차는?"):
        st.session_state.example = "도쿄와 서울 시차 알려줘"

with col2:
    if st.button("🇫🇷 파리 여행 날씨"):
        st.session_state.example = "파리 현재 날씨와 여행 팁 알려줘"

    if st.button("🇦🇺 시드니 지금 몇 시야?"):
        st.session_state.example = "시드니 현재 시간 알려줘"

# -----------------------------------
# 세션 상태 초기화
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# 이전 메시지 출력
# -----------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------
# 입력창
# -----------------------------------
default_prompt = st.session_state.get("example", "")

prompt = st.chat_input(
    "도시 이름이나 질문을 입력하세요"
)

if default_prompt and not prompt:
    prompt = default_prompt
    st.session_state.example = ""

# -----------------------------------
# 사용자 입력 처리
# -----------------------------------
if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # 시스템 메시지 포함
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + st.session_state.messages

    # Assistant 응답
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True,
        )

        for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                full_response += delta
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    # 응답 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

# -----------------------------------
# 사이드바
# -----------------------------------
with st.sidebar:

    st.header("🌎 빠른 도시 검색")

    st.markdown("""
    추천 도시:
    - 서울
    - 도쿄
    - 뉴욕
    - 런던
    - 파리
    - 시드니
    - 방콕
    - 싱가포르
    - 로마
    - 두바이
    """)

    st.divider()

    st.markdown("""
    💡 예시 질문:
    - 런던 날씨 알려줘
    - 뉴욕 지금 몇 시야?
    - 파리와 서울 시차는?
    - 도쿄 여행 옷차림 추천
    """)

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()
